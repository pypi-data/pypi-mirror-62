# Copyright 2019 Jij Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import numpy as np
import openjij
from openjij.sampler import BaseSampler
from openjij.utils.decorator import deprecated_alias
from openjij.model import BinaryHigherOrderModel
from .hubo_simulated_annealing import hubo_sa_sampling
from .hubo_simulated_annealing import default_schedule
import cxxjij


class SASampler(BaseSampler):
    """Sampler with Simulated Annealing (SA).

    Inherits from :class:`openjij.sampler.sampler.BaseSampler`.

    Args:
        beta_min (float):
            Minmum beta (inverse temperature).
            You can overwrite in methods .sample_*.

        beta_max (float):
            Maximum beta (inverse temperature).
            You can overwrite in methods .sample_*.

        num_reads (int):
            number of sampling (algorithm) runs. defaults None.
            You can overwrite in methods .sample_*.

        num_sweeps (int):
            number of MonteCarlo steps during SA. defaults None.
            You can overwrite in methods .sample_*.

        schedule_info (dict):
            Information about an annealing schedule.

    Attributes:
        energy_bias (float):
            Energy bias.

        var_type (str):
            Type of variables: 'SPIN' or 'BINARY' which mean {-1, 1} or {0, 1}.

        indices (int):
            Indices of `openjij.model.model.BinaryQuadraticModel` object.

        N (int):
            Number of the indices.

    Raises:
        ValueError: If schedules or variables violate as below.
        - not list or numpy.array.
        - not list of tuple (beta : float, step_length : int).
        - beta is less than zero.

    """

    @property
    def parameters(self):
        return {
            'beta_min': ['parameters'],
            'beta_max': ['parameters'],
        }

    @deprecated_alias(iteration='num_reads')
    def __init__(self,
                 beta_min=None, beta_max=None,
                 num_sweeps=1000, schedule=None,
                 num_reads=1,
                 **kwargs):

        self.beta_min = beta_min
        self.beta_max = beta_max
        self.num_sweeps = num_sweeps
        self.schedule = schedule
        self.num_reads = num_reads
        self._schedule_setting = {
            'beta_min': beta_min,
            'beta_max': beta_max,
            'num_sweeps': num_sweeps,
            'num_reads': num_reads,
        }

        self._make_system = {
            'singlespinflip': cxxjij.system.make_classical_ising_Eigen,
            'swendsenwang': cxxjij.system.make_classical_ising
        }
        self._algorithm = {
            'singlespinflip': cxxjij.algorithm.Algorithm_SingleSpinFlip_run,
            'swendsenwang': cxxjij.algorithm.Algorithm_SwendsenWang_run
        }


    def _convert_validation_schedule(self, schedule):
        if not isinstance(schedule, (list, np.array)):
            raise ValueError("schedule should be list or numpy.array")

        if isinstance(schedule[0], cxxjij.utility.ClassicalSchedule):
            return schedule

        if len(schedule[0]) != 2:
            raise ValueError(
                "schedule is list of tuple or list (beta : float, step_length : int)")

        # schedule validation  0 <= beta
        beta = np.array(schedule).T[0]
        if not np.all(0 <= beta):
            raise ValueError("schedule beta range is '0 <= beta'.")

        # convert to cxxjij.utility.ClassicalSchedule
        cxxjij_schedule = []
        for beta, step_length in schedule:
            _schedule = cxxjij.utility.ClassicalSchedule()
            _schedule.one_mc_step = step_length
            _schedule.updater_parameter.beta = beta
            cxxjij_schedule.append(_schedule)
        return cxxjij_schedule

    def sample_ising(self, h, J, beta_min=None, beta_max=None,
                     num_sweeps=None, num_reads=1, schedule=None,
                     initial_state=None, updater='single spin flip',
                     reinitialize_state=True, seed=None,
                     **kwargs):

        model = openjij.BinaryQuadraticModel(
            linear=h, quadratic=J, var_type='SPIN'
        )
        return self._sampling(model, beta_min, beta_max,
                              num_sweeps, num_reads, schedule,
                              initial_state, updater,
                              reinitialize_state, seed, **kwargs)

    def _sampling(self, model, beta_min=None, beta_max=None,
                     num_sweeps=None, num_reads=1, schedule=None,
                     initial_state=None, updater='single spin flip',
                     reinitialize_state=True, seed=None,
                     **kwargs):
        ising_graph = model.get_cxxjij_ising_graph()

        self._setting_overwrite(
            beta_min=beta_min, beta_max=beta_max,
            num_sweeps=num_sweeps, num_reads=num_reads
        )


        # set annealing schedule -------------------------------
        if schedule or self.schedule:
            self._schedule = self._convert_validation_schedule(
                schedule if schedule else self.schedule
            )
            self.schedule_info = {'schedule': 'custom schedule'}
        else:
            self._schedule, beta_range = geometric_ising_beta_schedule(
                model=model,
                beta_max=self._schedule_setting['beta_max'],
                beta_min=self._schedule_setting['beta_min'],
                num_sweeps=self._schedule_setting['num_sweeps']
            )
            self.schedule_info = {
                'beta_max': beta_range[0],
                'beta_min': beta_range[1],
                'num_sweeps': self._schedule_setting['num_sweeps']
            }
        # ------------------------------- set annealing schedule

        # make init state generator --------------------------------
        if initial_state is None:
            def _generate_init_state(): return ising_graph.gen_spin()
        else:
            # validate initial_state size
            if len(initial_state) != ising_graph.size():
                raise ValueError(
                    "the size of the initial state should be {}"
                    .format(ising_graph.size()))
            if isinstance(initial_state, dict):
                initial_state = [initial_state[k] for k in model.indices]
            _init_state = np.array(initial_state)
            def _generate_init_state(): return np.array(_init_state)
        # -------------------------------- make init state generator

        # choose updater -------------------------------------------
        _updater_name = updater.lower().replace('_', '').replace(' ', '')
        if _updater_name not in self._make_system:
            raise ValueError('updater is one of "single spin flip or swendsen wang"')
        algorithm = self._algorithm[_updater_name]
        sa_system = self._make_system[_updater_name](_generate_init_state(), ising_graph)
        # ------------------------------------------- choose updater
        response = self._cxxjij_sampling(
            model, _generate_init_state,
            algorithm, sa_system,
            reinitialize_state, seed, **kwargs
        )

        response.info['schedule'] = self.schedule_info

        return response

    def sample_hubo(self, interactions: list, var_type,
                    beta_min=None, beta_max=None, schedule=None,
                    num_sweeps=100, num_reads=1,
                    init_state=None, seed=None):
        """sampling from higher order unconstrainted binary optimization
        Args:
            interactions (list of dict): ordered by degree of interaction. [linear, quadratic, ...]
            var_type (str, openjij.VarType): "SPIN" or "BINARY"
            beta_min (float, optional): Minimum beta (initial inverse temperature). Defaults to None.
            beta_max (float, optional): Maximum beta (final inverse temperature). Defaults to None.
            schedule (list, optional): [description]. Defaults to None.
            num_sweeps (int, optional): [description]. Defaults to 100.
            num_reads (int, optional): [description]. Defaults to 1.
            init_state (list, optional): initial state. Defaults to None.
            seed (int, optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """

        self._setting_overwrite(
            beta_min=beta_min, beta_max=beta_max,
            num_sweeps=num_sweeps, num_reads=num_reads
        )

        bhom = BinaryHigherOrderModel(interactions)

        if schedule or self.schedule:
            self._schedule = self._convert_validation_schedule(
                schedule if schedule else self.schedule
            )
            self.schedule_info = {'schedule': 'custom schedule'}
        else:
            schedule = default_schedule(
                bhom,
                beta_min=self._schedule_setting['beta_min'],
                beta_max=self._schedule_setting['beta_max'],
                num_sweeps=self._schedule_setting['num_sweeps'])
            self.schedule_info = {
                'beta_max': schedule[-1][0],
                'beta_min': schedule[0][0],
                'num_sweeps': self._schedule_setting['num_sweeps']
            }

        response = hubo_sa_sampling(
            bhom, var_type,
            schedule=schedule, schedule_info=self.schedule_info,
            num_sweeps=self._schedule_setting['num_sweeps'],
            num_reads=self._schedule_setting['num_reads'],
            init_state=init_state, seed=seed
        )
        return response


def geometric_ising_beta_schedule(model: openjij.model.BinaryQuadraticModel,
                                  beta_max=None, beta_min=None,
                                  num_sweeps=1000):
    """make geometric cooling beta schedule

    Args:
        model (openjij.BinaryQuadraticModel)
        beta_max (float, optional): [description]. Defaults to None.
        beta_min (float, optional): [description]. Defaults to None.
        num_sweeps (int, optional): [description]. Defaults to 1000.
    Returns:
        list of cxxjij.utility.ClassicalSchedule, list of beta range [max, min]
    """
    if beta_min is None or beta_max is None:
        ising_interaction = np.abs(model.ising_interactions())
        abs_bias = np.sum(ising_interaction, axis=1)

        min_delta_energy = np.min(ising_interaction[ising_interaction > 0])
        max_delta_energy = np.max(abs_bias[abs_bias > 0])

    beta_min = np.log(2) / max_delta_energy if beta_min is None else beta_min
    beta_max = np.log(100) / min_delta_energy if beta_max is None else beta_max

    num_sweeps_per_beta = max(1, num_sweeps // 1000)

    schedule = cxxjij.utility.make_classical_schedule_list(
        beta_min=beta_min, beta_max=beta_max,
        one_mc_step=num_sweeps_per_beta,
        num_call_updater=num_sweeps
    )

    return schedule, [beta_max, beta_min]

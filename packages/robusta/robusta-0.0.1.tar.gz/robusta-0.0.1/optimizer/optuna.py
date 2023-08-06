import pandas as pd
import numpy as np

import optuna

from .base import BaseOptimizer, qround


__all__ = ['OptunaCV', 'RandomSearchCV']




class OptunaCV(BaseOptimizer):


    def _get_space(self, base_space):
        return base_space


    def _get_params(self, trial):

        space = self.space
        params = {}

        for param, btype in self.btypes.items():

            if btype is 'choice':
                params[param] = trial.suggest_categorical(param, space[param])

            elif btype is 'uniform':
                a, b = space[param]
                params[param] = trial.suggest_uniform(param, a, b)

            elif btype is 'quniform':
                a, b, q = space[param]
                b = qround(b, a, b, q)
                params[param] = trial.suggest_discrete_uniform(param, a, b, q)

            elif btype is 'quniform_int':
                a, b = space[param][:2]
                params[param] = trial.suggest_int(param, a, b)

            elif btype is 'loguniform':
                a, b = space[param][:2]
                params[param] = trial.suggest_loguniform(param, a, b)

            elif btype is 'const':
                pass

        return params


    def _fit(self, X, y, groups=None):

        optuna.logging.set_verbosity(optuna.logging.FATAL)
        optuna.logging.disable_default_handler()

        def objective(trial):
            params = self._get_params(trial)
            score = self.eval_params(params, X, y, groups)
            return score

        if not hasattr(self, 'study'):
            # TODO: set seed & other params
            sampler = optuna.samplers.TPESampler(seed=0)
            self.study = optuna.create_study(direction='maximize', sampler=sampler)

        self.study.optimize(objective)

        return self




class RandomSearchCV(OptunaCV):

    def _fit(self, X, y, groups=None):

        optuna.logging.set_verbosity(optuna.logging.FATAL)
        optuna.logging.disable_default_handler()

        def objective(trial):
            params = self._get_params(trial)
            score = self.eval_params(params, X, y, groups)
            return score

        if not hasattr(self, 'study'):
            # TODO: set seed & other params
            sampler = optuna.samplers.RandomSampler(seed=0)
            self.study = optuna.create_study(direction='maximize', sampler=sampler)

        self.study.optimize(objective)

        return self

import numpy as np
import pandas as pd
from tqdm import tqdm

from EstimatorSpectrum import Landweber
from Generator import LSWW
from SVD import LordWillisSpektor


def BETA(x):
    return 20 * x ** 3 * (1 - x)


def kernel(x, y):
    return np.where(x >= y, 2 * y, 0)


size = 10000
replications = 50

if __name__ == '__main__':
    parameter_landweber = []
    oracle_landweber = []
    oracle_error_landweber = []
    solutions_landweber = []
    residual_landweber = []
    lsww = LSWW(pdf=BETA, sample_size=size, seed=123)
    for _ in tqdm(range(replications)):

        try:
            lsw = LordWillisSpektor(transformed_measure=False)

            obs = lsww.generate()
            landweber = Landweber(kernel=kernel, singular_values=lsw.singular_values,
                                  left_singular_functions=lsw.left_functions,
                                  right_singular_functions=lsw.right_functions,
                                  observations=obs, sample_size=size, max_size=100, tau=1)

            landweber.estimate()
            landweber.oracle(BETA)
            solution = list(landweber.solution(np.linspace(0, 1, 10000)))
            parameter_landweber.append(landweber.regularization_param)
            oracle_landweber.append(landweber.oracle_param)
            oracle_error_landweber.append(landweber.oracle_loss)
            solutions_landweber.append(solution)
            residual_landweber.append(landweber.residual)
            landweber.client.close()
        except:
            pass

    results_landweber = pd.DataFrame(
        {'Parameter': parameter_landweber, 'Oracle': oracle_landweber, 'Oracle_loss': oracle_error_landweber,
         'Residual': residual_landweber, 'Solution': solutions_landweber})
    results_landweber.to_csv('Simulation_BETA_landweber_{}.csv'.format(size))

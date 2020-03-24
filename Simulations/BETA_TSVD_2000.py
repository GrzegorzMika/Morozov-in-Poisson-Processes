import numpy as np
import pandas as pd
from tqdm import tqdm

from EstimatorSpectrum import TSVD
from Generator import LSWW
from SVD import LordWillisSpektor


def BETA(x):
    return 20 * x ** 3 * (1 - x)


def kernel(x, y):
    return np.where(x >= y, 2 * y, 0)


size = 2000
replications = 50

if __name__ == '__main__':
    parameter_tsvd = []
    oracle_tsvd = []
    oracle_error_tsvd = []
    solutions_tsvd = []
    residual_tsvd = []

    lsww = LSWW(pdf=BETA, sample_size=size, seed=123)
    for _ in tqdm(range(replications)):

        try:
            lsw = LordWillisSpektor(transformed_measure=False)
            obs = lsww.generate()
            tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                        left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                        observations=obs, sample_size=size, max_size=100, tau=1)

            tsvd.estimate()
            tsvd.oracle(BETA)
            solution = list(tsvd.solution(np.linspace(0, 1, 10000)))
            parameter_tsvd.append(tsvd.regularization_param)
            oracle_tsvd.append(tsvd.oracle_param)
            oracle_error_tsvd.append(tsvd.oracle_loss)
            solutions_tsvd.append(solution)
            residual_tsvd.append(tsvd.residual)
            tsvd.client.close()
        except:
            pass
    results_tsvd = pd.DataFrame(
        {'Parameter': parameter_tsvd, 'Oracle': oracle_tsvd, 'Oracle_loss': oracle_error_tsvd,
         'Residual': residual_tsvd, 'Solution': solutions_tsvd})
    results_tsvd.to_csv('Simulation_BETA_tsvd_{}.csv'.format(size))

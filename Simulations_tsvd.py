import numpy as np
import pandas as pd
from tqdm import tqdm

from EstimatorSpectrum import TSVD
from Generator import LSWW
from SVD import LordWillisSpektor


def BETA(x):
    return 20 * x ** 3 * (1 - x)


def SMLA(x):
    return np.where(x <= 0.5, 4 * x ** 2, 2 - 4 * (1 - x) ** 2)


def SMLB(x):
    return 1.241 * np.multiply(np.power(2 * x - x ** 2, -1.5),
                               np.exp(1.21 * (1 - np.power(2 * x - x ** 2, -1))))


def NM(x):
    return 0.7 / (np.sqrt(2 * np.pi) * 0.08) * np.exp(-np.power(x - 0.7, 2) / (2 * 0.08 ** 2)) + 0.3 // (
            np.sqrt(2 * np.pi) * 0.08) * np.exp(-np.power(x - 0.35, 2) / (2 * 0.08 ** 2))


def kernel(x, y):
    return np.where(x >= y, 2 * y, 0)


size = 10000
replications = 50

if __name__ == '__main__':
    parameter_tsvd = []
    oracle_tsvd = []
    oracle_error_tsvd = []
    solutions_tsvd = []
    residual_tsvd = []

    lsw = LordWillisSpektor(transformed_measure=False)
    lsww = LSWW(pdf=SMLA, sample_size=size)
    obs = lsww.generate()

    tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                observations=obs, sample_size=size, max_size=100, tau=1)
    lsww = LSWW(pdf=SMLA, sample_size=size, seed=123)
    for _ in tqdm(range(replications)):

        try:
            lsw = LordWillisSpektor(transformed_measure=False)
            obs = lsww.generate()
            tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                        left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                        observations=obs, sample_size=size, max_size=100, tau=1)

            tsvd.estimate()
            tsvd.oracle(SMLA)
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
    results_tsvd.to_csv('Simulation_SMLA_tsvd_{}.csv'.format(size))

    ##############################################################################################################################
    parameter_tsvd = []
    oracle_tsvd = []
    oracle_error_tsvd = []
    solutions_tsvd = []
    residual_tsvd = []

    lsw = LordWillisSpektor(transformed_measure=False)
    lsww = LSWW(pdf=SMLB, sample_size=size)
    obs = lsww.generate()

    tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                observations=obs, sample_size=size, max_size=100, tau=1)
    lsww = LSWW(pdf=SMLB, sample_size=size, seed=123)
    for _ in tqdm(range(replications)):

        try:
            lsw = LordWillisSpektor(transformed_measure=False)
            obs = lsww.generate()
            tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                        left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                        observations=obs, sample_size=size, max_size=100, tau=1)

            tsvd.estimate()
            tsvd.oracle(SMLB)
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
    results_tsvd.to_csv('Simulation_SMLB_tsvd_{}.csv'.format(size))

    ##############################################################################################################################
    parameter_tsvd = []
    oracle_tsvd = []
    oracle_error_tsvd = []
    solutions_tsvd = []
    residual_tsvd = []

    lsw = LordWillisSpektor(transformed_measure=False)
    lsww = LSWW(pdf=NM, sample_size=size)
    obs = lsww.generate()
    tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                observations=obs, sample_size=size, max_size=100, tau=1)
    lsww = LSWW(pdf=NM, sample_size=size, seed=123)
    for _ in tqdm(range(replications)):

        try:
            lsw = LordWillisSpektor(transformed_measure=False)
            obs = lsww.generate()
            tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                        left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                        observations=obs, sample_size=size, max_size=100, tau=1)

            tsvd.estimate()
            tsvd.oracle(NM)
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
    results_tsvd.to_csv('Simulation_NM_tsvd_{}.csv'.format(size))

    ##############################################################################################################################
    parameter_tsvd = []
    oracle_tsvd = []
    oracle_error_tsvd = []
    solutions_tsvd = []
    residual_tsvd = []

    lsw = LordWillisSpektor(transformed_measure=False)
    lsww = LSWW(pdf=BETA, sample_size=size)
    obs = lsww.generate()
    tsvd = TSVD(kernel=kernel, singular_values=lsw.singular_values,
                left_singular_functions=lsw.left_functions, right_singular_functions=lsw.right_functions,
                observations=obs, sample_size=size, max_size=100, tau=1)
    lsww = LSWW(pdf=NM, sample_size=size, seed=123)
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

import sys
from os import path

import numpy as np
import pandas as pd
from test_functions import kernel_transformed, STEP

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from EstimatorSpectrum import Tikhonov
from Generator import LSW
from SVD import LordWillisSpektor

replications = 10
size = [2000, 10000, 1000000]
max_size = 50
order = 2
functions = [STEP]
functions_name = ['STEP']
taus = [1., 1.1, 1.2, 1.3, 1.4, 1.5]
taus_name = ['10', '11', '12', '13', '14', '15']

if __name__ == '__main__':
    for s in size:
        for i, fun in enumerate(functions):
            for j, tau in enumerate(taus):
                generator = LSW(pdf=fun, sample_size=s, seed=914)
                results = {'selected_param': [], 'oracle_param': [], 'oracle_loss': [], 'loss': [], 'solution': [],
                           'oracle_solution': []}
                for _ in range(replications):
                    try:
                        spectrum = LordWillisSpektor(transformed_measure=True)
                        obs = generator.generate()
                        landweber = Tikhonov(kernel=kernel_transformed, singular_values=spectrum.singular_values,
                                             left_singular_functions=spectrum.left_functions,
                                             right_singular_functions=spectrum.right_functions,
                                             observations=obs, sample_size=s, max_size=max_size, tau=tau,
                                             order=order, transformed_measure=True, njobs=-1)
                        landweber.estimate()
                        landweber.oracle(fun)
                        solution = list(landweber.solution(np.linspace(0, 1, 10000)))
                        results['selected_param'].append(landweber.regularization_param)
                        results['oracle_param'].append(landweber.oracle_param)
                        results['oracle_loss'].append(landweber.oracle_loss)
                        results['loss'].append(landweber.residual)
                        results['solution'].append(solution)
                        results['oracle_solution'].append(list(landweber.oracle_solution))
                        landweber.client.close()
                    except:
                        pass
                pd.DataFrame(results).to_csv('Tikhonov_{}_{}_tau_{}.csv'.format(functions_name[i], s, taus_name[j]))

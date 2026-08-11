import numpy as np
from racf_models_ns import *

def log_likelihood(params, t, data, model, errors) -> float:
    '''
    Calculate the log likelihood of the data given the model parameters.
    '''
    model = model(t, *params)
    sigma2 = errors ** 2 

    return -0.5 * np.sum((data - model) ** 2 / sigma2 + np.log(sigma2))

def prior_transform(u, bounds):

    return [i * (b[1] - b[0]) for i, b in zip(u, bounds)]
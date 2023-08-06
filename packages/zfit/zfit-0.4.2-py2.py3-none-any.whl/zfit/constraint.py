#  Copyright (c) 2019 zfit

from .util import ztyping
from .core.constraint import SimpleConstraint, GaussianConstraint
import tensorflow as tf



__all__ = ["nll_gaussian", "SimpleConstraint", "GaussianConstraint"]


def nll_gaussian(params: ztyping.ParamTypeInput, observation: ztyping.NumericalScalarType,
                 uncertainty: ztyping.NumericalScalarType) -> tf.Tensor:
    """Return negative log likelihood graph for gaussian constraints on a list of parameters.
    Args:
        params (list(zfit.Parameter)): The parameters to constraint
        observation (numerical, list(numerical)): observed values of the parameter
        uncertainty (numerical, list(numerical) or array/tensor): Uncertainties or covariance/error
            matrix of the observed values. Can either be a single value, a list of values, an array or a tensor
    Returns:
        `GaussianConstraint`: the constraint object
    Raises:
        ShapeIncompatibleError: if params, mu and sigma don't have the same size
    """

    return GaussianConstraint(params=params, observation=observation, uncertainty=uncertainty)

# def nll_pdf(constraints: dict):
#     if not constraints:
#         return z.constant(0.)  # adding 0 to nll
#     probs = []
#     for param, dist in constraints.items():
#         probs.append(dist.pdf(param))
#     # probs = [dist.pdf(param) for param, dist in constraints.items()]
#     constraints_neg_log_prob = -tf.reduce_sum(tf.log(probs))
#     return constraints_neg_log_prob

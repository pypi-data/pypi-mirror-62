# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 09:12:36 2016

@module:    choice_calcs.py
@name:      Choice Calculations
@author:    Timothy Brathwaite
            José Ángel Martín Baos
@summary:   Contains generic functions necessary for calculating choice
            probabilities and for estimating the choice models.
"""

import numpy as np
import scipy.stats
import scipy.linalg
from scipy.linalg import block_diag
from scipy.sparse import hstack

try:
    # Python 3.x does not natively support xrange
    from past.builtins import xrange
except ImportError:
    pass

# Define the boundary values which are not to be exceeded during computation
min_exponent_val = -700
max_exponent_val = 700

max_comp_value = 1e300
min_comp_value = 1e-300
# The value below was determined since its the smallest value, x, for which
# 1 - x != 1
# min_comp_value = 1e-16


def calc_probabilities(beta,
                       design,
                       alt_IDs,
                       rows_to_obs,
                       rows_to_alts,
                       utility_transform,
                       intercept_params=None,
                       shape_params=None,
                       chosen_row_to_obs=None,
                       return_long_probs=False):
    """
    Parameters
    ----------
    beta : 1D or 2D ndarray.
        All elements should by ints, floats, or longs. If 1D, should have 1
        element for each utility coefficient being estimated (i.e.
        num_features). If 2D, should have 1 column for each set of coefficients
        being used to predict the probabilities of each alternative being
        chosen. There should be one row per index coefficient.
    design : 2D or 3D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs. If `len(design.shape) == 3`,
        then beta MUST be 1D.
    alt_IDs : 1D ndarray.
        All elements should be ints. There should be one row per obervation per
        available alternative for the given observation. Elements denote the
        alternative corresponding to the given row of the design matrix.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    rows_to_alts : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per possible alternative. This matrix maps the rows of the
        design matrix to the possible alternatives for this dataset.
    utility_transform : callable.
        Should accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, and miscellaneous args and kwargs. Should return a 1D
        array whose elements contain the appropriately transformed systematic
        utility values, based on the current model being evaluated.
    intercept_params : 1D ndarray, or None, optional.
        If an array, each element should be an int, float, or long. For
        identifiability, there should be J- 1 elements where J is the total
        number of observed alternatives for this dataset. Default == None.
    shape_params : 1D ndarray, or None, optional.
        If an array, each element should be an int, float, or long. There
        should be one value per shape parameter of the model being used.
        Default == None.
    chosen_row_to_obs :  2D scipy sparse array, or None, optional.
        There should be one row per observation per available alternative and
        one column per observation. This matrix indicates, for each observation
        (on the columns), which rows of the design matrix were the realized
        outcome. If an array is passed then an array of shape
        (num_observations,) will be returned and each element will be the
        probability of the realized outcome of the given observation.
        Default == None.
    return_long_probs :  bool, optional.
        Indicates whether or not the long format probabilities (a 1D numpy array
        with one element per observation per available alternative) should be
        returned. Default == False.

    Returns
    -------
    numpy array or tuple of two numpy arrays.
        If `chosen_row_to_obs` is passed AND `return_long_probs is True`, then
        the tuple `(chosen_probs, long_probs)` is returned. If
        `return_long_probs is True` and `chosen_row_to_obs is None`, then
        `long_probs` is returned. If `chosen_row_to_obs` is passed and
        `return_long_probs is False` then `chosen_probs` is returned.

        `chosen_probs` is a 1D numpy array of shape (num_observations,). Each
        element is the probability of the corresponding observation being
        associated with its realized outcome.

        `long_probs` is a 1D numpy array with one element per observation per
        available alternative for that observation. Each element is the
        probability of the corresponding observation being associated with that
        rows corresponding alternative.

        If `beta` is a 2D array, `chosen_probs` and `long_probs` will also be
        2D arrays, with as many columns as there are sets of parameters being
        used to calculate probabilities with.

        It is NOT valid to have `chosen_row_to_obs == None` and
        `return_long_probs == False`.
    """
    # Check argument validity
    if (len(beta.shape) >= 2) and (len(design.shape) >= 3):
        msg_1 = "Cannot calculate probabilities with both 3D design matrix AND"
        msg_2 = " 2D coefficient array."
        raise ValueError(msg_1 + msg_2)
    if chosen_row_to_obs is None and return_long_probs is False:
        msg = "chosen_row_to_obs is None AND return_long_probs is False"
        raise ValueError(msg)

    # Calculate the systematic utility for each alternative for each individual
    sys_utilities = design.dot(beta)

    # Calculate the probability from the transformed utilities
    # The transformed utilities will be of shape (num_rows, 1)
    transformed_utilities = utility_transform(sys_utilities,
                                              alt_IDs,
                                              rows_to_alts,
                                              shape_params,
                                              intercept_params)

    # The following commands are to guard against numeric under/over-flow
    too_small_idx = transformed_utilities < min_exponent_val
    too_large_idx = transformed_utilities > max_exponent_val

    transformed_utilities[too_small_idx] = min_exponent_val
    transformed_utilities[too_large_idx] = max_exponent_val

    # Exponentiate the transformed utilities
    long_exponentials = np.exp(transformed_utilities)

    # long_probs will be of shape (num_rows,) Each element will provide the
    # probability of the observation associated with that row having the
    # alternative associated with that row as the observation's outcome
    individual_denominators = np.asarray(rows_to_obs.transpose().dot(
                                                    long_exponentials))
    long_denominators = np.asarray(rows_to_obs.dot(individual_denominators))
    if len(long_exponentials.shape) > 1 and long_exponentials.shape[1] > 1:
        long_probs = (long_exponentials / long_denominators)
    else:
        long_probs = (long_exponentials / long_denominators).ravel()

    # Guard against underflow
    long_probs[long_probs == 0] = min_comp_value

    if chosen_row_to_obs is None:
        chosen_probs = None
    else:
        # chosen_probs will be of shape (num_observations,)
        chosen_exponentials = np.asarray(
                         chosen_row_to_obs.transpose().dot(long_exponentials))
        if len(long_exponentials.shape) > 1 and long_exponentials.shape[1] > 1:
            chosen_probs = chosen_exponentials / individual_denominators
        else:
            chosen_probs = (chosen_exponentials /
                            individual_denominators).ravel()

    # Return the long form and chosen probabilities if desired
    if return_long_probs and chosen_probs is not None:
        return chosen_probs, long_probs
    # If working with predictions, return just the long form probabilities
    elif return_long_probs and chosen_probs is None:
        return long_probs
    # If estimating the model and storing fitted probabilities or testing the
    # model on data for which we know the chosen alternative, just return the
    # chosen probabilities.
    elif chosen_probs is not None:
        return chosen_probs


def calc_log_likelihood(beta,
                        design,
                        alt_IDs,
                        rows_to_obs,
                        rows_to_alts,
                        choice_vector,
                        utility_transform,
                        intercept_params=None,
                        shape_params=None,
                        PMLE=None,
                        PMLE_lambda=0,
                        weights=None):
    """
    Parameters
    ----------
    beta : 1D ndarray.
        All elements should by ints, floats, or longs. Should have 1 element
        for each utility coefficient being estimated (i.e. num_features).
    design : 2D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    alt_IDs : 1D ndarray.
        All elements should be ints. There should be one row per obervation per
        available alternative for the given observation. Elements denote the
        alternative corresponding to the given row of the design matrix.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    rows_to_alts : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per possible alternative. This matrix maps the rows of the
        design matrix to the possible alternatives for this dataset.
    choice_vector : 1D ndarray.
        All elements should be either ones or zeros. There should be one row
        per observation per available alternative for the given observation.
        Elements denote the alternative which is chosen by the given
        observation with a 1 and a zero otherwise.
    utility_transform:  callable.
        Should accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, and miscellaneous args and kwargs. Should return a 1D
        array whose elements contain the appropriately transformed systematic
        utility values, based on the current model being evaluated.
    intercept_params:   1D ndarray, or None, optional.
        If an array, each element should be an int, float, or long. For
        identifiability, there should be J- 1 elements where J is the total
        number of observed alternatives for this dataset. Default == None.
    shape_params: 1D ndarray, or None, optional.
        If an array, each element should be an int, float, or long. There
        should be one value per shape parameter of the model being used.
        Default == None.
    PMLE: None or string value: ['LASSO', 'RIDGE' or 'Tikhonov']
        It determines if a Penalized Maximum Likelihood Estimation should be
        executed. The value of the parameter determines the type of PMLE. The
        None value states that no PMLE is executed. Default = None.
    PMLE_lambda : int, float, long, or None, optional.
        Lambda parameter for LASSO or ridge regression. It should be an int,
        float or long and determines the penalty for the optimization.
        Default = 0.
    weights : 1D ndarray or None, optional.
        Allows for the calculation of weighted log-likelihoods. The weights can
        represent various things. In stratified samples, the weights may be
        the proportion of the observations in a given strata for a sample in
        relation to the proportion of observations in that strata in the
        population. In latent class models, the weights may be the probability
        of being a particular class.

    Returns
    -------
    log_likelihood : float. The log likelihood of the multinomial choice model.
    """
    # Calculate the probability of each individual choosing each available
    # alternative for that individual.
    long_probs = calc_probabilities(beta,
                                    design,
                                    alt_IDs,
                                    rows_to_obs,
                                    rows_to_alts,
                                    utility_transform,
                                    intercept_params=intercept_params,
                                    shape_params=shape_params,
                                    return_long_probs=True)

    # Calculate the weights for the sample
    if weights is None:
        weights = 1

    # Calculate the log likelihood
    log_likelihood = choice_vector.dot(weights * np.log(long_probs))

    if PMLE is None:
        return log_likelihood
    else:
        param_list = [x for x in [shape_params, intercept_params, beta]
                      if x is not None]
        if len(param_list) > 1:
            params = np.concatenate(param_list, axis=0)
        else:
            params = param_list[0]

        if PMLE == "LASSO":
            return log_likelihood - PMLE_lambda * np.absolute(params).sum()

        elif PMLE == "RIDGE":
            return log_likelihood - PMLE_lambda * np.square(params).sum()

        elif PMLE == "Tikhonov":
            # TODO: Not implemented.
            msg = "Tikhonov Penalized Maximum Likelihood Estimation is not yet"
            msg_2 = "implemented. It would be available in a future version."
            msg_3 = "\nUse another PMLE type instead or None for no PMLE."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)

        else:
            msg_1 = "Error! {} is not a valid value for PMLE.\n".format(PMLE)
            msg_2 = "Penalized Maximum Likelihood Estimation (MPLE) only"
            msg_3 = "implements methods: 'LASSO', 'RIDGE' and 'Tikhonov' (only"
            msg_4 = "for kernel models)."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)


def calc_gradient(beta,
                  design,
                  alt_IDs,
                  rows_to_obs,
                  rows_to_alts,
                  choice_vector,
                  utility_transform,
                  transform_first_deriv_c,
                  transform_first_deriv_v,
                  transform_deriv_alpha,
                  intercept_params,
                  shape_params,
                  PMLE,
                  PMLE_lambda,
                  weights):
    """
    Parameters
    ----------
    beta : 1D ndarray.
        All elements should by ints, floats, or longs. Should have 1 element
        for each utility coefficient being estimated (i.e. num_features).
    design : 2D ndarray.
        Tjere should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    alt_IDs : 1D ndarray.
        All elements should be ints. There should be one row per obervation per
        available alternative for the given observation. Elements denote the
        alternative corresponding to the given row of the design matrix.
    rows_to_obs : 2D scipy sparse array.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    rows_to_alts : 2D scipy sparse array
        There should be one row per observation per available alternative and
        one column per possible alternative. This matrix maps the rows of the
        design matrix to the possible alternatives for this dataset.
    choice_vector : 1D ndarray.
        All elements should be either ones or zeros. There should be one row
        per observation per available alternative for the given observation.
        Elements denote the alternative which is chosen by the given
        observation with a 1 and a zero otherwise.
    utility_transform : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, and miscellaneous args and kwargs. Should return a 1D
        array whose elements contain the appropriately transformed systematic
        utility values, based on the current model being evaluated.
    transform_first_deriv_c : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, the `rows_to_alts` array, (shape parameters if there
        are any) and miscellaneous args and kwargs. Should return a 2D matrix
        or sparse array whose elements contain the derivative of the tranformed
        utility vector with respect to the vector of shape parameters. The
        dimensions of the returned vector should be
        `(design.shape[0], num_alternatives)`. If there are no shape parameters
        then the callable should return None.
    transform_first_deriv_v : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, (shape parameters if there are any) and miscellaneous
        args and kwargs. Should return a 2D array whose elements contain the
        derivative of the tranformed utility vector with respect to the vector
        of systematic utilities. The dimensions of the returned vector should
        be `(design.shape[0], design.shape[0])`.
    transform_deriv_alpha : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, the `rows_to_alts` array, (intercept parameters if
        there are any) and miscellaneous args and kwargs. Should return a 2D
        array whose elements contain the derivative of the tranformed utility
        vector with respect to the vector of shape parameters. The dimensions
        of the returned vector should be
        `(design.shape[0], num_alternatives - 1)`. If there are no intercept
        parameters, the callable should return None.
    intercept_params : 1D numpy array or None.
        If an array, each element should be an int, float, or long. For
        identifiability, there should be J- 1 elements where J is the total
        number of observed alternatives for this dataset. Default == None.
    shape_params : 1D ndarray or None.
       If an array, each element should be an int, float, or long. There should
       be one value per shape parameter of the model being used.
       Default == None.
    PMLE: None or string value: ['LASSO', 'RIDGE' or 'Tikhonov']
        It determines if a Penalized Maximum Likelihood Estimation should be
        executed. The value of the parameter determines the type of PMLE. The
        None value states that no PMLE is executed. Default = None.
    PMLE_lambda : int, float, long, or None, optional.
        Lambda parameter for LASSO or ridge regression. It should be an int,
        float or long and determines the penalty for the optimization.
        Default = 0.
    weights : 1D ndarray or None.
        Allows for the calculation of weighted log-likelihoods. The weights can
        represent various things. In stratified samples, the weights may be
        the proportion of the observations in a given strata for a sample in
        relation to the proportion of observations in that strata in the
        population. In latent class models, the weights may be the probability
        of being a particular class.

    Returns
    -------
    gradient : 1D ndarray.
       It's shape is (beta.shape[0], ). It is the second derivative of the log-
       likelihood with respect to beta.
    """
    # Calculate the systematic utility for each alternative for each individual
    sys_utilities = design.dot(beta)

    # Calculate the probability of each individual choosing each available
    # alternative for that individual.
    long_probs = calc_probabilities(beta,
                                    design,
                                    alt_IDs,
                                    rows_to_obs,
                                    rows_to_alts,
                                    utility_transform,
                                    intercept_params=intercept_params,
                                    shape_params=shape_params,
                                    return_long_probs=True)

    # Calculate the weights for the sample
    if weights is None:
        weights = 1

    ##########
    # Get the required matrices
    ##########
    # Differentiate the transformed utilities with respect to the shape params
    # Note that dh_dc should be a sparse array
    dh_dc = transform_first_deriv_c(sys_utilities, alt_IDs,
                                    rows_to_alts, shape_params)
    # Differentiate the transformed utilities by the intercept params
    # Note that dh_d_alpha should be a sparse array
    dh_d_alpha = transform_deriv_alpha(sys_utilities, alt_IDs,
                                       rows_to_alts, intercept_params)
    # Differentiate the transformed utilities with respect to the systematic
    # utilities. Note that dh_dv should be a sparse matrix
    dh_dv = transform_first_deriv_v(sys_utilities, alt_IDs,
                                    rows_to_alts, shape_params)
    # Differentiate the transformed utilities with respect to the utility
    # coefficients. Note that dh_db should be a dense **matrix**, not a dense
    # 2D array. This is because the dot product of a 2D scipy sparse array and
    # a 2D dense numpy array yields a 2D dense numpy matrix
    dh_db = dh_dv.dot(design)
    # Differentiate the log likelihood w/ respect to the transformed utilities
    # Note that d_ll_dh will be a dense 2D numpy array.
    d_ll_dh = np.multiply(weights, choice_vector - long_probs)[np.newaxis, :]

    # Calculate the gradient of the log-likelihood with respect to the betas
    d_ll_d_beta = d_ll_dh.dot(dh_db)

    ##########
    # Form and return the gradient
    ##########
    if shape_params is not None and intercept_params is not None:
        # Note that we use d_ll_dh * dh_dc and d_ll_dh * dh_d_alpha because
        # that is how one computes the dot product between a dense 2D numpy
        # array and a 2D sparse matrix. This is due to numpy ndarrays and
        # scipy sparse matrices not playing nicely together. However, numpy
        # ndarrays and numpy matrices can be dot producted together,
        # hence d_ll_dh.dot(dh_db).

        # Note that the 'np.asarray' is because dll_dh * dh_dc will be a row
        # matrix, but we want a 1D numpy array.
        gradient = np.concatenate((np.asarray(d_ll_dh * hstack((dh_dc,
                                                                dh_d_alpha),
                                                               format='csr')),
                                   d_ll_d_beta), axis=1).ravel()
        params = np.concatenate((shape_params, intercept_params, beta),
                                axis=0)

    elif shape_params is not None and intercept_params is None:
        # Note that we use d_ll_dh * dh_dc because that is how one computes
        # the dot product between a dense 2D numpy array and a 2D sparse matrix
        # This is due to numpy ndarrays and scipy sparse matrices not playing
        # nicely together. However, numpy ndarrays and numpy matrices can be
        # dot producted together, hence d_ll_dh.dot(dh_db).

        # Note that the 'np.asarray' is because dll_dh * dh_dc will be a row
        # matrix, but we want a 1D numpy array.
        gradient = np.concatenate((np.asarray(d_ll_dh * dh_dc), d_ll_d_beta),
                                  axis=1).ravel()
        params = np.concatenate((shape_params, beta), axis=0)

    elif shape_params is None and intercept_params is not None:
        # Note that we use d_ll_dh * dh_d_alpha because that's how one computes
        # the dot product between a dense 2D numpy array and a 2D sparse matrix
        # This is due to numpy ndarrays and scipy sparse matrices not playing
        # nicely together. However, numpy ndarrays and numpy matrices can be
        # dot producted together, hence d_ll_dh.dot(dh_db).

        # Note 'np.asarray' is used because dll_dh * dh_d_alpha will be a row
        # matrix, but we want a 1D numpy array.
        gradient = np.concatenate((np.asarray(d_ll_dh * dh_d_alpha),
                                   d_ll_d_beta), axis=1).ravel()
        params = np.concatenate((intercept_params, beta), axis=0)

    else:
        gradient = d_ll_d_beta.ravel()
        params = beta

    if PMLE is not None:
        if PMLE == "LASSO":
            gradient -= 2 * PMLE_lambda * np.sign(params)

        elif PMLE == "RIDGE":
            gradient -= 2 * PMLE_lambda * params

        elif PMLE == "Tikhonov":
            # TODO: Not implemented.
            msg = "Tikhonov Penalized Maximum Likelihood Estimation is not yet"
            msg_2 = "implemented. It would be available in a future version."
            msg_3 = "\nUse another PMLE type instead or None for no PMLE."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)

        else:
            msg_1 = "Error! {} is not a valid value for PMLE.\n".format(PMLE)
            msg_2 = "Penalized Maximum Likelihood Estimation (MPLE) only"
            msg_3 = "implements methods: 'LASSO', 'RIDGE' and 'Tikhonov' (only"
            msg_4 = "for kernel models)."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)

    return gradient


##########
# The three functions below are used, jointly, to construct dP_dV, the block
# diagonal matrix that is the derivative of the long probability vector with
# respect to the long vector of index values = X*beta.
##########
def create_matrix_block_indices(row_to_obs):
    """
    Parameters
    ----------
    row_to_obs: 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).

    Returns
    -------
    output_indices : list of arrays.
        There will be one array per column in `row_to_obs`. The array will note
        which rows correspond to which observations.
    """
    # Initialize the list of index arrays to be returned
    output_indices = []
    # Determine the number of observations in the dataset
    num_obs = row_to_obs.shape[1]
    # Get the indices of the non-zero elements and their values
    row_indices, col_indices, values = scipy.sparse.find(row_to_obs)
    # Iterate over each observation, i.e. each column in row_to_obs, and
    # determine which rows belong to that observation (i.e. the rows with ones
    # in them).
    for col in xrange(num_obs):
        # Store the array of row indices belonging to the current observation
        output_indices.append(row_indices[np.where(col_indices == col)])

    return output_indices


def robust_outer_product(vec_1, vec_2):
    """
    Calculates a 'robust' outer product of two vectors that may or may not
    contain very small values.

    Parameters
    ----------
    vec_1 : 1D ndarray
    vec_2 : 1D ndarray

    Returns
    -------
    outer_prod : 2D ndarray. The outer product of vec_1 and vec_2
    """
    mantissa_1, exponents_1 = np.frexp(vec_1)
    mantissa_2, exponents_2 = np.frexp(vec_2)
    new_mantissas = mantissa_1[None, :] * mantissa_2[:, None]
    new_exponents = exponents_1[None, :] + exponents_2[:, None]
    return new_mantissas * np.exp2(new_exponents)


def create_matrix_blocks(long_probs, matrix_block_indices):
    """
    Parameters
    ----------
    long_probs : 1D ndarray.
        There should be one row per observation per available alternative. The
        elements of the array will indicate the probability of the alternative
        being the outcome associated with the corresponding observation.
    matrix_block_indices : list of arrays.
        There will be one array per observation. The arrays will note which
        rows correspond to which observations.

    Returns
    -------
    output_matrices : list of matrices.
        Each matrix will contain the derivative of P_i with respect to H_i, and
        there will be one matrix for each observations i. P_i is the array of
        probabilities of each observation being associated with its available
        alternatives. H_i is the array of transformed index values for each
        alternative that is available to observation i.
    """
    # Initialize the list of matrices that is to be returned.
    output_matrices = []
    # Iterate over each observation, i.e. over each list of rows that
    # corresponds to each observation.
    for indices in matrix_block_indices:
        # Isolate P_i, the vector of probabilities of each alternative that
        # is associated with the current observation
        current_probs = long_probs[indices]
        # Get the outer product of the current probabilities
        # probability_outer_product = np.outer(current_probs, current_probs)
        probability_outer_product = robust_outer_product(current_probs,
                                                         current_probs)

        # Create the desired dP_i/dh_i matrix
        dP_i_dh_i = np.diag(current_probs) - probability_outer_product
        # Ensure that the diagonal is positive and non-zero, since it must be.
        diag_idx = np.diag_indices_from(dP_i_dh_i)
        diag_values = dP_i_dh_i[diag_idx].copy()
        diag_values[diag_values == 0] = min_comp_value
        dP_i_dh_i[diag_idx] = diag_values
        # Guard against underflow on the off-diagonals
        underflow_idxs = np.where(dP_i_dh_i == 0)
        for i in xrange(underflow_idxs[0].size):
            row_idx, col_idx = underflow_idxs[0][i], underflow_idxs[1][i]
            if row_idx != col_idx:
                # Since this type of underflow essentially comes from
                # multiplying two very small numbers, just set the overall
                # result to a small number
                dP_i_dh_i[row_idx,
                          col_idx] = -1 * min_comp_value
        # Store the desired dP_i/dh_i matrix
        output_matrices.append(dP_i_dh_i)

    return output_matrices


def calc_hessian(beta,
                 design,
                 alt_IDs,
                 rows_to_obs,
                 rows_to_alts,
                 utility_transform,
                 transform_first_deriv_c,
                 transform_first_deriv_v,
                 transform_deriv_alpha,
                 block_matrix_idxs,
                 intercept_params,
                 shape_params,
                 PMLE,
                 PMLE_lambda,
                 weights):
    """
    Parameters
    ----------
    beta : 1D ndarray.
        All elements should by ints, floats, or longs. Should have 1 element
        for each utility coefficient being estimated (i.e. num_features).
    design : 2D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    alt_IDs : 1D ndarray.
        All elements should be ints. There should be one row per obervation per
        available alternative for the given observation. Elements denote the
        alternative corresponding to the given row of the design matrix.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    rows_to_alts: 2D ndarray.
        There should be one row per observation per available alternative and
        one column per possible alternative. This matrix maps the rows of the
        design matrix to the possible alternatives for this dataset.
    utility_transform : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, and miscellaneous args and kwargs. Should return a 1D
        array whose elements contain the appropriately transformed systematic
        utility values, based on the current model being evaluated.
    transform_first_deriv_c : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, the `rows_to_alts` array, (shape parameters if there
        are any) and miscellaneous args and kwargs. Should return a 2D array
        whose elements contain the derivative of the tranformed utilities with
        respect to the vector of shape parameters. The dimensions of the
        returned vector should be `(design.shape[0], num_alternatives)`.
    transform_first_deriv_v : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, (shape parameters if there are any) and miscellaneous
        args and kwargs. Should return a 2D array whose elements contain the
        derivative of the tranformed utility vector with respect to the vector
        of systematic utilities. The dimensions of the returned vector should
        be `(design.shape[0], design.shape[0])`.
    transform_deriv_alpha : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, the rows_to_alts array, (intercept parameters if
        there are any) and miscellaneous args and kwargs. Should return a 2D
        array whose elements contain the derivative of the tranformed utilities
        with respect to the vector of shape parameters. The dimensions of the
        returned vector should be `(design.shape[0], num_alternatives - 1)`. If
        `intercept_params == None`, the callable should return None.
    block_matrix_idxs : list of arrays.
        There will be one array per observation. The arrays will note which
        rows correspond to which observations.
    intercept_params : 1D ndarray.
        Each element should be an int, float, or long. For identifiability,
        there should be J- 1 elements where J is the total number of observed
        alternatives in the dataset.
    shape_params: None or 1D ndarray.
        If an array, each element should be an int, float, or long. There
        should be one value per shape parameter of the model being used.
        Default == None.
    PMLE: None or string value: ['LASSO', 'RIDGE' or 'Tikhonov']
        It determines if a Penalized Maximum Likelihood Estimation should be
        executed. The value of the parameter determines the type of PMLE. The
        None value states that no PMLE is executed. Default = None.
    PMLE_lambda : int, float, long, or None, optional.
        Lambda parameter for LASSO or ridge regression. It should be an int,
        float or long and determines the penalty for the optimization.
        Default = 0.
    weights : 1D ndarray or None.
        Allows for the calculation of weighted log-likelihoods. The weights can
        represent various things. In stratified samples, the weights may be
        the proportion of the observations in a given strata for a sample in
        relation to the proportion of observations in that strata in the
        population. In latent class models, the weights may be the probability
        of being a particular class.

    Returns
    -------
    hess : 2D ndarray.
        It's shape is `(beta.shape[0], beta.shape[0])`. It is the second
        derivative of the log likelihood with respect to beta.
    """
    # Calculate the systematic utility for each alternative for each individual
    sys_utilities = design.dot(beta)

    # Calculate the probability of each individual choosing each available
    # alternative for that individual.
    long_probs = calc_probabilities(beta,
                                    design,
                                    alt_IDs,
                                    rows_to_obs,
                                    rows_to_alts,
                                    utility_transform,
                                    intercept_params=intercept_params,
                                    shape_params=shape_params,
                                    return_long_probs=True)

    # Calculate the weights for the sample
    if weights is None:
        weights = np.ones(design.shape[0])

    ##########
    # Get the required matrices
    ##########
    # Differentiate the transformed utilities with respect to the shape params
    # Note that dh_dc will be a 2D scipy sparse matrix
    dh_dc = transform_first_deriv_c(sys_utilities, alt_IDs,
                                    rows_to_alts, shape_params)
    # Differentiate the transformed utilities with respect to the systematic
    # utilities. Note that dh_dv will be a 2D scipy sparse matrix.
    dh_dv = transform_first_deriv_v(sys_utilities, alt_IDs,
                                    rows_to_alts, shape_params)
    # Differentiate the transformed utilities by the intercept params
    # Note that dh_d_alpha should be a sparse array
    dh_d_alpha = transform_deriv_alpha(sys_utilities, alt_IDs,
                                       rows_to_alts, intercept_params)
    # Differentiate the transformed utilities with respect to the utility
    # coefficients. Note that dh_db will be a 2D dense numpy matrix
    dh_db = dh_dv.dot(design)

    # Differentiate the probabilities with respect to the transformed utilities
    # Note that dp_dh will be a 2D dense numpy array
    block_matrices = create_matrix_blocks(long_probs, block_matrix_idxs)
    dp_dh = block_diag(*block_matrices) * weights[None, :]

    ##########
    # Calculate the second and mixed partial derivatives within the hessian
    ##########
    # Calculate the second derivative of the log-likelihood with repect to the
    # utility coefficients. Should have shape (design.shape[0],
    # design.shape[0]). Since dp_dh is a 2D dense numpy array and dh_db is a
    # 2D dense numpy matrix, using the .dot() syntax should work to compute
    # the dot product.
    d2_ll_db2 = -1 * dh_db.T.dot(dp_dh.dot(dh_db))

    ##########
    # Form and return the hessian
    ##########
    if shape_params is not None and intercept_params is not None:
        # Calculate the second derivative of the log-likelihood with respect
        # to the shape parameters. Should have shape (shape_params.shape[0],
        # shape_params.shape[0]). Note that since dp_dh is a 2D dense numpy
        # array and dh_dc is a sparse matrix or dense numpy matrix, to
        # compute the dot product we need to use the * operator
        d2_ll_dc2 = -1 * dh_dc.T.dot(dp_dh * dh_dc)

        # Calculate the second derivative of the log-likelihood with respect
        # to the intercept parameters. Should have shape (J - 1, J - 1) where
        # J is the total number of observed alternatives for this dataset.
        # Note that since dp_dh is a 2D dense numpy array and dh_d_alpha is a
        # sparse matrix or dense numpy matrix, to compute the dot product
        # we need to use the * operator
        d2_ll_d_alpha2 = -1 * dh_d_alpha.T.dot(dp_dh * dh_d_alpha)

        # Calculate the mixed second derivative of the log-likelihood with
        # respect to the intercept and shape parameters. Should have shape
        # (dh_d_alpha.shape[1], dh_dc.shape[1]). Note that since dp_dh is a 2D
        # dense numpy array and dh_dc is a sparse matrix or dense numpy
        # matrix, to compute the dot product we need to use the * operator
        d2_ll_dc_d_alpha = -1 * dh_d_alpha.T.dot(dp_dh * dh_dc)

        # Calculate the mixed partial derivative of the log-likelihood with
        # respect to the utility coefficients and then with respect to the
        # shape parameters. Should have shape (design.shape[0],
        # shape_params.shape[0]). Note that since dp_dh is a 2D dense numpy
        # array and dh_dc is a sparse matrix or dense numpy matrix, to
        # compute the dot product we need to use the * operator
        d2_ll_dc_db = -1 * dh_db.T.dot(dp_dh * dh_dc)

        # Calculate the mixed partial derivative of the log-likelihood with
        # respect to the utility coefficients and then with respect to the
        # intercept parameters. Should have shape (design.shape[0],
        # intercept_params.shape[0]). Note that since dp_dh is a 2D dense numpy
        # array and dh_d_alpha is a sparse matrix or dense numpy matrix, to
        # compute the dot product we need to use the * operator
        d2_ll_d_alpha_db = -1 * dh_db.T.dot(dp_dh * dh_d_alpha)

        # Form the 3 by 3 partitioned hessian of 2nd derivatives
        top_row = np.concatenate((d2_ll_dc2,
                                  d2_ll_dc_d_alpha.T,
                                  d2_ll_dc_db.T), axis=1)
        middle_row = np.concatenate((d2_ll_dc_d_alpha,
                                     d2_ll_d_alpha2,
                                     d2_ll_d_alpha_db.T), axis=1)
        last_row = np.concatenate((d2_ll_dc_db,
                                   d2_ll_d_alpha_db,
                                   d2_ll_db2), axis=1)
        hess = np.concatenate((top_row,
                               middle_row,
                               last_row), axis=0)

    elif shape_params is not None and intercept_params is None:
        # Calculate the second derivative of the log-likelihood with respect
        # to the shape parameters. Should have shape (shape_params.shape[0],
        # shape_params.shape[0]). Note that since dp_dh is a 2D dense numpy
        # array and dh_dc is a sparse matrix or dense numpy matrix, to
        # compute the dot product we need to use the * operator
        d2_ll_dc2 = -1 * dh_dc.T.dot(dp_dh * dh_dc)

        # Calculate the mixed partial derivative of the log-likelihood with
        # respect to the utility coefficients and then with respect to the
        # shape parameters. Should have shape (design.shape[0],
        # shape_params.shape[0]). Note that since dp_dh is a 2D dense numpy
        # array and dh_dc is a sparse matrix or dense numpy matrix, to
        # compute the dot product we need to use the * operator
        d2_ll_dc_db = -1 * dh_db.T.dot(dp_dh * dh_dc)

        hess = np.concatenate((np.concatenate((d2_ll_dc2,
                                               d2_ll_dc_db.T), axis=1),
                               np.concatenate((d2_ll_dc_db,
                                               d2_ll_db2), axis=1)), axis=0)

    elif shape_params is None and intercept_params is not None:
        # Calculate the second derivative of the log-likelihood with respect
        # to the intercept parameters. Should have shape (J - 1, J - 1) where
        # J is the total number of observed alternatives for this dataset.
        # Note that since dp_dh is a 2D dense numpy array and dh_d_alpha is a
        # sparse matrix or dense numpy matrix, to compute the dot product
        # we need to use the * operator
        d2_ll_d_alpha2 = -1 * dh_d_alpha.T.dot(dp_dh * dh_d_alpha)

        # Calculate the mixed partial derivative of the log-likelihood with
        # respect to the utility coefficients and then with respect to the
        # intercept parameters. Should have shape (design.shape[0],
        # intercept_params.shape[0]). Note that since dp_dh is a 2D dense numpy
        # array and dh_d_alpha is a sparse matrix or dense numpy matrix, to
        # compute the dot product we need to use the * operator
        d2_ll_d_alpha_db = -1 * dh_db.T.dot(dp_dh * dh_d_alpha)

        hess = np.concatenate((np.concatenate((d2_ll_d_alpha2,
                                               d2_ll_d_alpha_db.T), axis=1),
                               np.concatenate((d2_ll_d_alpha_db,
                                               d2_ll_db2), axis=1)), axis=0)
    else:
        hess = d2_ll_db2

    if PMLE is not None:
        if PMLE == "LASSO":
            # Do nothing because the expression should be hess -= 0
            pass

        elif PMLE == "RIDGE":
            hess -= 2 * PMLE_lambda

        elif PMLE == "Tikhonov":
            # TODO: Not implemented.
            msg = "Tikhonov Penalized Maximum Likelihood Estimation is not yet"
            msg_2 = "implemented. It would be available in a future version."
            msg_3 = "\nUse another PMLE type instead or None for no PMLE."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)

        else:
            msg_1 = "Error! {} is not a valid value for PMLE.\n".format(PMLE)
            msg_2 = "Penalized Maximum Likelihood Estimation (MPLE) only"
            msg_3 = "implements methods: 'LASSO', 'RIDGE' and 'Tikhonov' (only"
            msg_4 = "for kernel models)."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)

    # Make sure we are returning standard numpy arrays
    if isinstance(hess, np.matrixlib.defmatrix.matrix):
        hess = np.asarray(hess)

    return hess


def calc_fisher_info_matrix(beta,
                            design,
                            alt_IDs,
                            rows_to_obs,
                            rows_to_alts,
                            choice_vector,
                            utility_transform,
                            transform_first_deriv_c,
                            transform_first_deriv_v,
                            transform_deriv_alpha,
                            intercept_params,
                            shape_params,
                            PMLE,
                            PMLE_lambda,
                            weights):
    """
    Parameters
    ----------
    beta : 1D ndarray.
        All elements should by ints, floats, or longs. Should have 1 element
        for each utility coefficient being estimated (i.e. num_features).
    design : 2D ndarray.
        There should be one row per observation per available alternative.
        There should be one column per utility coefficient being estimated. All
        elements should be ints, floats, or longs.
    alt_IDs : 1D ndarray.
        All elements should be ints. There should be one row per obervation per
        available alternative for the given observation. Elements denote the
        alternative corresponding to the given row of the design matrix.
    rows_to_obs : 2D ndarray.
        There should be one row per observation per available alternative and
        one column per observation. This matrix maps the rows of the design
        matrix to the unique observations (on the columns).
    rows_to_alts : 2D ndarray
        There should be one row per observation per available alternative and
        one column per possible alternative. This matrix maps the rows of the
        design matrix to the possible alternatives for this dataset.
    choice_vector : 1D ndarray.
        All elements should be either ones or zeros. There should be one row
        per observation per available alternative for the given observation.
        Elements denote the alternative which is chosen by the given
        observation with a 1 and a zero otherwise.
    utility_transform : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, and miscellaneous args and kwargs. Should return a
        1D array whose elements contain the appropriately transformed
        systematic utility values, based on the current model being evaluated.
    transform_first_deriv_c : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
        alternative IDs, the `rows_to_alts` array, (shape parameters if there
        are any) and miscellaneous args and kwargs. Should return a 2D array
        whose elements contain the derivative of the tranformed utilities with
        respect to the vector of shape parameters. The dimensions of the
        returned vector should be `(design.shape[0], num_alternatives)`.
    transform_first_deriv_v : callable.
        Must accept a 1D array of systematic utility values, a 1D array of
         alternative IDs, (shape parameters if there are any) and miscellaneous
         args and kwargs. Should return a 2D array whose elements contain the
         derivative of the utility tranformation vector with respect to the
         vector of systematic utilities. The dimensions of the returned vector
         should be `(design.shape[0],  design.shape[0])`.
    shape_params : None or 1D ndarray.
        If an array, each element should be an int, float, or long. There
        should be one value per shape parameter of the model being used.
        Default == None.
    PMLE: None or string value: ['LASSO', 'RIDGE' or 'Tikhonov']
        It determines if a Penalized Maximum Likelihood Estimation should be
        executed. The value of the parameter determines the type of PMLE. The
        None value states that no PMLE is executed. Default = None.
    PMLE_lambda : int, float, long, or None, optional.
        Lambda parameter for LASSO or ridge regression. It should be an int,
        float or long and determines the penalty for the optimization.
        Default = 0.
    weights : 1D ndarray or None.
        Allows for the calculation of weighted log-likelihoods. The weights can
        represent various things. In stratified samples, the weights may be
        the proportion of the observations in a given strata for a sample in
        relation to the proportion of observations in that strata in the
        population. In latent class models, the weights may be the probability
        of being a particular class.

    Returns
    -------
    fisher_matrix : 2D numpy array.
        It will be a square matrix, with one row and one column for each shape,
        intercept, and index coefficient. Contains the BHHH approximation to
        the Fisher Information matrix of the log likelihood.
    """
    # Calculate the systematic utility for each alternative for each individual
    sys_utilities = design.dot(beta)

    # Calculate the probability that the individual associated with a given row
    # chooses the alternative associated with a given row.
    long_probs = calc_probabilities(beta,
                                    design,
                                    alt_IDs,
                                    rows_to_obs,
                                    rows_to_alts,
                                    utility_transform,
                                    intercept_params=intercept_params,
                                    shape_params=shape_params,
                                    return_long_probs=True)

    # Calculate the weights for the sample
    if weights is None:
        weights = np.ones(design.shape[0])
    weights_per_obs =\
        np.max(rows_to_obs.toarray() * weights[:, None], axis=0)

    ##########
    # Get the required matrices
    ##########
    # Differentiate the transformed utilities with respect to the shape params
    dh_dc = transform_first_deriv_c(sys_utilities, alt_IDs,
                                    rows_to_alts, shape_params)
    # Differentiate the transformed utilities with respect to the systematic
    # utilities
    dh_dv = transform_first_deriv_v(sys_utilities, alt_IDs,
                                    rows_to_alts, shape_params)
    # Differentiate the transformed utilities by the intercept params
    # Note that dh_d_alpha should be a sparse array
    dh_d_alpha = transform_deriv_alpha(sys_utilities, alt_IDs,
                                       rows_to_alts, intercept_params)
    # Differentiate the transformed utilities with respect to the utility
    # coefficients. This should be a dense numpy array.
    dh_db = np.asarray(dh_dv.dot(design))
    # Differentiate the log likelihood w/ respect to the transformed utilities
    d_ll_dh = (choice_vector - long_probs)[np.newaxis, :]

    ##########
    # Create the matrix where each row represents the gradient of a particular
    # observations log-likelihood with respect to the shape parameters and
    # beta, depending on whether there are shape parameters being estimated
    ##########
    if shape_params is not None and intercept_params is not None:
        if isinstance(dh_dc, np.matrixlib.defmatrix.matrix):
            # Note that the '.A' transforms the matrix into a numpy ndarray
            gradient_vec = d_ll_dh.T * np.concatenate((dh_dc.A,
                                                       dh_d_alpha.toarray(),
                                                       dh_db), axis=1)
        else:
            gradient_vec = d_ll_dh.T * np.concatenate((dh_dc.toarray(),
                                                       dh_d_alpha.toarray(),
                                                       dh_db), axis=1)
    elif shape_params is not None and intercept_params is None:
        if isinstance(dh_dc, np.matrixlib.defmatrix.matrix):
            # Note that the '.A' transforms the matrix into a numpy ndarray
            gradient_vec = d_ll_dh.T * np.concatenate((dh_dc.A, dh_db), axis=1)
        else:
            gradient_vec = d_ll_dh.T * np.concatenate((dh_dc.toarray(),
                                                       dh_db), axis=1)
    elif shape_params is None and intercept_params is not None:
        # Note '.to_array()' is used because dh_d_alpha will be a sparse
        # matrix, but we want a 2D numpy array.
        gradient_vec = d_ll_dh.T * np.concatenate((dh_d_alpha.toarray(),
                                                   dh_db), axis=1)
    else:
        gradient_vec = d_ll_dh.T * dh_db

    # Make sure that we calculate the gradient PER OBSERVATION
    # and then take the outer products of those gradients.
    # Note that this is different than taking the outer products of the
    # gradient of the log-likelihood per available alternative per observation
    gradient_vec = rows_to_obs.T.dot(gradient_vec)

    # Compute and return the outer product of each row of the gradient
    # with itself. Then sum these individual matrices together. The line below
    # does the same computation just with less memory and time.
    fisher_matrix =\
        gradient_vec.T.dot(np.multiply(weights_per_obs[:, None], gradient_vec))

    if PMLE is not None:
        if PMLE == "LASSO":
            # Do nothing because the expression should be fisher_matrix -= 0
            # The rational behind adding 0 is that the fisher information
            # matrix should approximate the hessian and in the hessian we add
            # 0 at the end. I don't know if this is the correct way to
            # calculate the Fisher Information in ridge regression models.
            pass

        elif PMLE == "RIDGE":
            # The rational behind adding 2*ridge is that the fisher information
            # matrix should approximate the hessian and in the hessian we add
            # 2*ridge at the end. I don't know if this is the correct way to
            # calculate the Fisher Information in ridge regression models.
            fisher_matrix -= 2 * PMLE_lambda

        elif PMLE == "Tikhonov":
            # TODO: Not implemented.
            msg = "Tikhonov Penalized Maximum Likelihood Estimation is not yet"
            msg_2 = "implemented. It would be available in a future version."
            msg_3 = "\nUse another PMLE type instead or None for no PMLE."
            total_msg = " ".join([msg_1, msg_2, msg_3])
            raise ValueError(total_msg)

        else:
            msg_1 = "Error! {} is not a valid value for PMLE.\n".format(PMLE)
            msg_2 = "Penalized Maximum Likelihood Estimation (MPLE) only"
            msg_3 = "implements methods: 'LASSO', 'RIDGE' and 'Tikhonov' (only"
            msg_4 = "for kernel models)."
            total_msg = " ".join([msg_1, msg_2, msg_3, msg_4])
            raise ValueError(total_msg)

    return fisher_matrix


def calc_asymptotic_covariance(hessian, fisher_info_matrix):
    """
    Parameters
    ----------
    hessian : 2D ndarray.
        It should have shape `(num_vars, num_vars)`. It is the matrix of second
        derivatives of the total loss across the dataset, with respect to each
        pair of coefficients being estimated.
    fisher_info_matrix : 2D ndarray.
        It should have a shape of `(num_vars, num_vars)`.  It is the
        approximation of the negative of the expected hessian formed by taking
        the outer product of (each observation's gradient of the loss function)
        with itself, and then summing across all observations.

    Returns
    -------
    huber_white_matrix : 2D ndarray.
        Will have shape `(num_vars, num_vars)`. The entries in the returned
        matrix are calculated by the following formula:
        `hess_inverse * fisher_info_matrix * hess_inverse`.
    """
    # Calculate the inverse of the hessian
    hess_inv = scipy.linalg.inv(hessian)

    return np.dot(hess_inv, np.dot(fisher_info_matrix, hess_inv))

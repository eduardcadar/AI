from math import exp, log

import numpy as np


def relu(x):
    return max(0, x)


def sigmoid(x):
    return 1 / (1 + exp(-x))


def softplus(x):
    return log(1 + exp(x))


def tanh(x):
    return np.tanh(x)


def tanh_prime(x):
    return 1-np.tanh(x)**2


def mean_squared_error_list(real_values, computed_values):
    errors = [mean_squared_error(r, c) for r, c in zip(real_values, computed_values)]
    return 1/len(real_values) * sum(errors)


def mean_squared_error(real_value, computed_value):
    return (1/2) * ((real_value - computed_value) ** 2)


def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2))


def mse_prime(y_true, y_pred):
    return 2*(y_pred-y_true)/len(y_true)


def dot(a, b):
    # if not isinstance(b[0], list):
    #     a, b = b, a
    result = [0 for _ in range(len(b[0]))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            result[j] += a[i] * b[i][j]
    return result


def transpose_matrix(matrix):
    if not isinstance(matrix[0], list):
        return [[matrix[i]] for i in range(len(matrix))]
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def to_categorical(a):
    size = len(set(a))
    result = []
    for i in a:
        result.append([0 for _ in range(size)])
        result[-1][i] = 1
    return result

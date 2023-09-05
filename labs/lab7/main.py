import random

import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

import file_utils
import matrix_utils


def test_function(inputs, computed_outputs, outputs):
    plt.plot(inputs, computed_outputs, 'yo', label='computed data')
    plt.plot(inputs, outputs, 'g^', label='real data')
    plt.show()

    error = 0.0
    for t1, t2 in zip(computed_outputs, outputs):
        error += (t1 - t2) ** 2
    error_manual = error / len(outputs)
    error_tool = mean_squared_error(outputs, computed_outputs)
    print('prediction error (manual):', error_manual)
    print('prediction error (tool):', error_tool)


def plot_data(w0, w1, train_inputs, train_outputs, x_label, y_label):
    no_points = 100
    x_ref = []
    val = min(train_inputs)
    step = (max(train_inputs) - min(train_inputs)) / no_points
    for i in range(1, no_points):
        x_ref.append(val)
        val += step
    y_ref = [w0 + w1 * el for el in x_ref]

    plt.plot(train_inputs, train_outputs, 'ro', label='training data')
    plt.plot(x_ref, y_ref, 'b-', label='learnt model')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


def split_data(data_in, data_out):
    random.seed()
    train_indexes = random.sample(range(len(data_in)), int(0.8 * len(data_in)))
    test_indexes = [i for i in range(len(data_in)) if i not in train_indexes]

    train_in = [data_in[i] for i in train_indexes]
    train_out = [data_out[i] for i in train_indexes]
    test_in = [data_in[i] for i in test_indexes]
    test_out = [data_out[i] for i in test_indexes]
    return train_in, train_out, test_in, test_out


def train_by_tool(train_inputs, train_outputs):
    regressor = linear_model.LinearRegression()
    regressor.fit(train_inputs, train_outputs)
    w0, w1, w2 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1]
    print('model learnt by tool: f(x) =', w0, '+', w1, '* x1 +', w2, '* x2')
    results = [w0, w1, w2]
    return regressor, results


def train_by_my_alg(train_inputs1, train_inputs2, train_outputs):
    # At * A * W = At * Z
    # W = inv(At * A) * At * Z
    train_outputs_column = [[train_outputs[i]] for i in range(len(train_outputs))]
    a = list(zip([1] * len(train_inputs1), train_inputs1, train_inputs2))
    a_t = matrix_utils.transpose_matrix(a)
    b = matrix_utils.multiply_matrices(a_t, a)  # b = At * A
    b_inv = matrix_utils.inverse(b)
    c = matrix_utils.multiply_matrices(b_inv, a_t)  # c = inv(At * A) * At
    w = matrix_utils.multiply_matrices(c, train_outputs_column)
    results = []
    for i in range(len(w)):
        results.append(w[i][0])

    return results


def solve():
    data_labels, data_inputs1, data_inputs2, data_outputs = file_utils.load_data(
        'data/v1_world-happiness-report-2017.csv',
        'Economy..GDP.per.Capita.',
        'Freedom',
        'Happiness.Score')
    data_inputs = list(zip(data_inputs1, data_inputs2))
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(data_inputs, data_outputs)
    for i in range(len(train_inputs)):
        train_inputs[i] = list(train_inputs[i])

    train_inputs1, train_inputs2 = [x[0] for x in train_inputs], [x[1] for x in train_inputs]

    regressor, tool_results = train_by_tool(train_inputs, train_outputs)

    my_results = train_by_my_alg(train_inputs1, train_inputs2, train_outputs)

    print('tool results:', tool_results)
    print('my results:', my_results)

    print('---TOOL ERROR---')
    tool_outputs = regressor.predict(test_inputs)
    test_function(test_inputs, tool_outputs, test_outputs)
    print('---MY ERROR---')
    w0, w1, w2 = my_results[0], my_results[1], my_results[2]
    my_outputs = [w0 + w1*x1 + w2*x2 for (x1, x2) in test_inputs]
    test_function(test_inputs, my_outputs, test_outputs)


solve()

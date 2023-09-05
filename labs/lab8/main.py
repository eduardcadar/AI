import random
from matplotlib import pyplot as plt
import file_utils
import normalisation
import train


def test_function(inputs, computed_outputs, outputs):
    plt.plot(inputs, computed_outputs, 'yo', label='computed data')
    plt.plot(inputs, outputs, 'g^', label='real data')
    plt.show()

    error = 0.0
    for t1, t2 in zip(computed_outputs, outputs):
        error += (t1 - t2) ** 2
    error_manual = error / len(outputs)
    print('prediction error:', error_manual)


def split_data(data_in, data_out):
    # data_in - lista de liste, in fiecare lista sunt atributele unui test
    # data_out - lista de valori output
    random.seed()
    train_indexes = random.sample(range(len(data_in)), int(0.8 * len(data_in)))
    test_indexes = [i for i in range(len(data_in)) if i not in train_indexes]

    train_in = [data_in[i] for i in train_indexes]
    train_out = [data_out[i] for i in train_indexes]
    test_in = [data_in[i] for i in test_indexes]
    test_out = [data_out[i] for i in test_indexes]
    return train_in, train_out, test_in, test_out


def solve():
    data_labels, data_inputs, data_outputs = file_utils.load_data(
        'data/v1_world-happiness-report-2017.csv',
        'Economy..GDP.per.Capita.',
        'Freedom',
        'Happiness.Score')
    train_in, train_out, test_in, test_out = split_data(data_inputs, data_outputs)

    regressor = train.train_by_tool(train_in, train_out)
    tool_outputs = regressor.predict(test_in)
    test_function(test_in, tool_outputs, test_out)

    my_regressor = train.train_by_my_stochastic_algorithm(train_in, train_out)
    my_outputs = my_regressor.predict(test_in)
    test_function(test_in, my_outputs, test_out)

    print("\n---NORMALISED---")
    train_in1 = [el[0] for el in train_in]
    train_in2 = [el[1] for el in train_in]
    test_in1 = [el[0] for el in test_in]
    test_in2 = [el[1] for el in test_in]

    train_in1, mean1, std1 = normalisation.statistical_normalisation(train_in1)
    train_in2, mean2, std2 = normalisation.statistical_normalisation(train_in2)

    test_in1 = normalisation.statistical_normalisation(test_in1, mean1, std1)[0]
    test_in2 = normalisation.statistical_normalisation(test_in2, mean2, std2)[0]
    train_in = [[el[0], el[1]] for el in zip(train_in1, train_in2)]
    test_in = [[el[0], el[1]] for el in zip(test_in1, test_in2)]
    my_regressor = train.train_by_my_stochastic_algorithm(train_in, train_out)
    my_outputs = my_regressor.predict(test_in)
    test_function(test_in, my_outputs, test_out)

    """ BATCH """
    print("\n---BATCH---")
    my_regressor = train.train_by_my_batch_algorithm(train_in, train_out)
    my_outputs = my_regressor.predict(test_in)
    test_function(test_in, my_outputs, test_out)

    """ NON LINEAR """
    print("\n---STOCHASTIC NON LINEAR---")
    non_linear_regressor = train.train_nonlinear_by_stochastic_algorithm(train_in, train_out)
    non_linear_outputs = non_linear_regressor.predict(test_in)
    test_function(test_in, non_linear_outputs, test_out)


solve()

import random

import normalisation
from train import test_function
import train
from data import load_data_cancer, load_data_flowers


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


def solve_cancer():
    print('---CANCER---')
    inputs, outputs = load_data_cancer()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(inputs, outputs)
    train_inputs1, train_inputs2 = [el[0] for el in train_inputs], [el[1] for el in train_inputs]
    test_inputs1, test_inputs2 = [el[0] for el in test_inputs], [el[1] for el in test_inputs]
    train_inputs1, mean1, std1 = normalisation.statistical_normalisation(train_inputs1)
    train_inputs2, mean2, std2 = normalisation.statistical_normalisation(train_inputs2)
    test_inputs1 = normalisation.statistical_normalisation(test_inputs1, mean1, std1)[0]
    test_inputs2 = normalisation.statistical_normalisation(test_inputs2, mean2, std2)[0]
    train_inputs = [[el[0], el[1]] for el in zip(train_inputs1, train_inputs2)]
    test_inputs = [[el[0], el[1]] for el in zip(test_inputs1, test_inputs2)]

    classifier = train.train_by_tool(train_inputs, train_outputs)
    computed_outputs = classifier.predict(test_inputs)
    test_function(computed_outputs, test_outputs)

    my_classifier = train.train_by_my_algorithm(train_inputs, train_outputs)
    my_computed_outputs = my_classifier.predict(test_inputs)
    test_function(my_computed_outputs, test_outputs)


def solve_flowers():
    print('---FLOWERS---')
    inputs, outputs = load_data_flowers()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(inputs, outputs)
    train_in1, train_in2 = [el[0] for el in train_inputs], [el[1] for el in train_inputs]
    train_in3, train_in4 = [el[2] for el in train_inputs], [el[3] for el in train_inputs]
    test_in1, test_in2 = [el[0] for el in test_inputs], [el[1] for el in test_inputs]
    test_in3, test_in4 = [el[2] for el in test_inputs], [el[3] for el in test_inputs]
    train_in1, mean1, std1 = normalisation.statistical_normalisation(train_in1)
    train_in2, mean2, std2 = normalisation.statistical_normalisation(train_in2)
    train_in3, mean3, std3 = normalisation.statistical_normalisation(train_in3)
    train_in4, mean4, std4 = normalisation.statistical_normalisation(train_in4)
    test_in1 = normalisation.statistical_normalisation(test_in1, mean1, std1)[0]
    test_in2 = normalisation.statistical_normalisation(test_in2, mean2, std2)[0]
    test_in3 = normalisation.statistical_normalisation(test_in3, mean3, std3)[0]
    test_in4 = normalisation.statistical_normalisation(test_in4, mean4, std4)[0]
    train_inputs = [[el[0], el[1], el[2], el[3]] for el in zip(train_in1, train_in2, train_in3, train_in4)]
    test_inputs = [[el[0], el[1], el[2], el[3]] for el in zip(test_in1, test_in2, test_in3, test_in4)]

    classifier = train.train_by_tool(train_inputs, train_outputs)
    computed_outputs = classifier.predict(test_inputs)
    test_function(computed_outputs, test_outputs)
    print()

    my_classifier = train.train_by_my_algorithm(train_inputs, train_outputs, batch=False)
    my_computed_outputs = my_classifier.predict(test_inputs)
    test_function(my_computed_outputs, test_outputs)
    print()

    my_classifier = train.train_by_my_algorithm_cross_validation(train_inputs, train_outputs, batch=False, k_fold=5)
    my_computed_outputs = my_classifier.predict(test_inputs)
    test_function(my_computed_outputs, test_outputs)


def solve():
    # solve_cancer()
    solve_flowers()


solve()

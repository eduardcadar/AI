import math
from math import sqrt

import readFile
import utils


def mean_absolute_error(real_values, predicted_values):
    diffs = []
    for real, predicted in zip(real_values, predicted_values):
        diffs.append([abs(r - c) for r, c in zip(real, predicted)])
    for i in range(len(diffs)):
        diffs[i] = sum(diffs[i]) / len(diffs[i])
    error_l1 = sum(diffs) / len(real_values)
    return error_l1


def root_mean_square_error(real_values, predicted_values):
    diffs = []
    for real, predicted in zip(real_values, predicted_values):
        diffs.append([(r - c) ** 2 for r, c in zip(real, predicted)])
    for i in range(len(diffs)):
        diffs[i] = sum(diffs[i]) / len(diffs[i])
    error_l2 = sqrt(sum(diffs) / len(diffs))
    return error_l2


def solve_regression(params):
    print("-------REGRESSION-------")

    real_values, predicted_values = params['real_values'], params['predicted_values']
    # MAE - mean absolute error
    print("Mean absolute error:", mean_absolute_error(real_values, predicted_values))

    # RMSE - root mean square error
    print("Root mean square error:", root_mean_square_error(real_values, predicted_values))


def solve_classification(params):
    print("-------CLASSIFICATION-------")
    real, predicted = params['real'], params['predicted']
    tp, fp, tn, fn = {}, {}, {}, {}
    for label in params['labels']:
        tp[label] = sum(1 if (real[i] == label and predicted[i] == label) else 0 for i in range(len(real)))
        fp[label] = sum(1 if (real[i] != label and predicted[i] == label) else 0 for i in range(len(real)))
        tn[label] = sum(1 if (real[i] != label and predicted[i] != label) else 0 for i in range(len(real)))
        fn[label] = sum(1 if (real[i] == label and predicted[i] != label) else 0 for i in range(len(real)))

    precision, recall = {}, {}
    for label in params['labels']:
        precision[label] = tp[label] / (tp[label] + fp[label])
        recall[label] = tp[label] / (tp[label] + fn[label])
    accuracy = sum(tp[label] for label in params['labels']) / len(real)

    confusion_matrix = utils.get_confusion_matrix(params['labels'], real, predicted)
    print("CONFUSION MATRIX")
    utils.print_matrix(confusion_matrix, params['labels']), print()

    print("accuracy:", accuracy)
    for label in params['labels']:
        print(label, 'precision:', precision[label])
        print(label, 'recall:', recall[label])


def solve_loss_multi_class(params):
    print("------LOSS FOR MULTI-CLASS-------")
    labels, real_labels = params['labels'], params['real_labels']
    real_outputs = [labels.index(label) for label in real_labels]
    computed_outputs = params['computed_outputs']
    dataset_size = len(real_labels)
    ce = 0.0
    for i in range(len(computed_outputs)):
        current_outputs = computed_outputs[i]
        exp_values = [math.exp(val) for val in current_outputs]
        sum_exp_val = sum(exp_values)
        mapped_outputs = [val / sum_exp_val for val in exp_values]
        # print(mapped_outputs, ' sum: ', sum(mapped_outputs))
        ce += - math.log(mapped_outputs[real_outputs[i]])

    print(ce / dataset_size)


def solve_loss_multi_class_probabilities(params):
    print("------LOSS FOR MULTI-CLASS PROBABILITIES------")
    # for each set (real label and computed probabilities),
    # add the negative of log of(computed probability of the real label)
    labels, real_labels = params['labels'], params['real_labels']
    real_outputs = [labels.index(label) for label in real_labels]
    computed_outputs = params['computed_outputs']
    data_set_size = len(real_labels)

    # cross_entropy = 0.0
    # for i in range(len(computed_outputs)):
    #     data_set = computed_outputs[i]
    #     cross_entropy += - math.log(data_set[real_outputs[i]])
    cross_entropy = sum([- math.log(computed_outputs[i][real_outputs[i]]) for i in range(len(computed_outputs))])

    print(cross_entropy / data_set_size)


def solve_loss_multi_label_probabilities(params):
    print("---LOSS FOR MULTI LABEL PROBABILITIES---")
    # sigmoid cross entropy loss
    labels, real_outputs, computed_outputs = params['labels'], params['real_outputs'], params['computed_outputs']
    no_labels = len(labels)
    dataset_size = len(real_outputs)

    ce = 0.0
    for i in range(len(computed_outputs)):
        real, current_outputs = real_outputs[i], computed_outputs[i]
        map_outputs = [1 / (1 + math.exp(-val)) for val in current_outputs]
        # print(map_outputs, ' sum: ', sum(map_outputs))
        ce += - sum([real[j] * math.log(map_outputs[j]) for j in range(no_labels)])

    print(ce / dataset_size)


def run():
    # pb_regression = readFile.read_regression("input/countries.csv")
    pb_regression = readFile.read_regression("input/sport.csv")
    solve_regression(pb_regression)
    print()

    pb_classification = readFile.read_classification("input/flowers.csv")
    solve_classification(pb_classification)
    print()

    pb_loss_class_probabilities = readFile.read_class_probabilities("input/spam.csv")
    solve_loss_multi_class_probabilities(pb_loss_class_probabilities)

    pb_loss_multi_class = readFile.read_class_probabilities("input/odd.csv")
    solve_loss_multi_class(pb_loss_multi_class)

    pb_loss_multi_label_probabilities = readFile.read_multi_label_probabilities("input/medical.csv")
    solve_loss_multi_label_probabilities(pb_loss_multi_label_probabilities)


run()

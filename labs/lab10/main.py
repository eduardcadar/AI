import data
import results
import train
import utils


def normalise_data(train_in, test_in):
    normalised_train_in, normalised_test_in = [[] for _ in range(len(train_in))], [[] for _ in range(len(test_in))]
    for i in range(len(train_in[0])):
        feature = [el[i] for el in train_in]
        tr_in, mean, std = data.statistical_normalisation(feature)
        te_in = [el[i] for el in test_in]
        te_in = data.statistical_normalisation(te_in, mean, std)[0]
        for j in range(len(normalised_train_in)):
            normalised_train_in[j].append(tr_in[j])
        for j in range(len(normalised_test_in)):
            normalised_test_in[j].append(te_in[j])
    return normalised_train_in, normalised_test_in


def solve_ann(layers, data_name, tool=False):
    inputs, outputs, label_names = data.load_data(data_name)
    train_in, train_out, test_in, test_out = data.split_data(inputs, outputs)
    train_in, test_in = normalise_data(train_in, test_in)

    print('--------------------', data_name, '--------------------')
    # tool
    if tool:
        classifier = train.train_by_tool(train_in, train_out, layers)
        predicted_labels = classifier.predict(test_in)
        acc, prec, recall, conf = results.eval_results(test_out, predicted_labels, label_names)
        print('---TOOL---')
        print('acc: ', acc), print('precision: ', prec), print('recall: ', recall)

    # my algorithm
    train_out = utils.to_categorical(train_out)
    classifier = train.train_by_my_mlp(train_in, train_out, layers)
    predicted_labels = classifier.predict(test_in)
    acc, prec, recall, conf = results.eval_results(test_out, predicted_labels, label_names)
    print('---MY ALGORITHM---')
    print('acc: ', acc), print('precision: ', prec), print('recall: ', recall)
    print('real', test_out)
    print('predicted', predicted_labels)


def solve_images_ann(layers, nr_iterations=100):
    inputs, outputs = data.load_images()
    for j, image in enumerate(inputs):
        for i, pixel in enumerate(image):
            a = sum(pixel) / len(pixel)
            inputs[j][i] = a
    train_in, train_out, test_in, test_out = data.split_data(inputs, outputs)
    train_in, test_in = normalise_data(train_in, test_in)

    print('---SEPIA---')
    train_out = utils.to_categorical(train_out)
    classifier = train.train_by_my_mlp(train_in, train_out, layers, nr_iterations=nr_iterations)
    predicted_labels = classifier.predict(test_in)
    acc, prec, recall, conf = results.eval_results(test_out, predicted_labels, label_names=range(2))
    print('acc: ', acc), print('precision: ', prec), print('recall: ', recall)
    print('real', test_out)
    print('predicted', predicted_labels)


def solve():
    layers_iris = (5,)
    layers_digits = (10, 10)
    layers_images = (5,)
    solve_ann(layers_iris, 'flowers', True)
    solve_ann(layers_digits, 'digits', True)
    solve_images_ann(layers_images, nr_iterations=100)


solve()

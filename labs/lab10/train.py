from sklearn import neural_network

import my_mlp


def train_by_tool(train_in, train_out, layers, nr_iterations=100):
    classifier = neural_network.MLPClassifier(hidden_layer_sizes=layers, activation='relu', max_iter=nr_iterations, solver='sgd',
                                              random_state=1, learning_rate_init=.1)
    classifier.fit(train_in, train_out)
    return classifier


def train_by_my_mlp(train_in, train_out, layers, nr_iterations=100):
    classifier = my_mlp.MyMlp(layers_format=layers, nr_iterations=nr_iterations)
    classifier.fit(train_in, train_out)
    return classifier

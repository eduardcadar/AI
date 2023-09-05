from sklearn import neural_network


def train_by_tool(train_in, train_out, layers, nr_iterations=100):
    classifier = neural_network.MLPClassifier(
        hidden_layer_sizes=layers, activation='relu', max_iter=nr_iterations,
        solver='sgd', random_state=1, learning_rate_init=.01)
    classifier.fit(train_in, train_out)
    return classifier

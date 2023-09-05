import random

import numpy as np

import utils


class MyMlp:
    def __init__(self, layers_format=(5,), loss_prime=utils.mse_prime,
                 learning_rate=0.01, nr_iterations=100):
        self.layers_format = layers_format
        self.layers = []
        self.learning_rate = learning_rate
        self.nr_iterations = nr_iterations
        self.loss_prime = loss_prime

    def add(self, layer):
        self.layers.append(layer)

    def fit(self, inputs, outputs):
        samples = len(inputs)
        first, last = len(inputs[0]), len(outputs[0])
        if len(self.layers_format) == 0:
            self.add(MyFCLayer(first, last))
            self.add(MyActivationLayer(utils.tanh, utils.tanh_prime))
        else:
            self.add(MyFCLayer(first, self.layers_format[0]))
            self.add(MyActivationLayer(utils.tanh, utils.tanh_prime))
            for index_layer, layer in enumerate(self.layers_format[1:]):
                self.add(MyFCLayer(self.layers_format[index_layer], layer))
                self.add(MyActivationLayer(utils.tanh, utils.tanh_prime))
            self.add(MyFCLayer(self.layers_format[-1], last))
            self.add(MyActivationLayer(utils.tanh, utils.tanh_prime))

        print(self.nr_iterations, 'iterations:', end=' ')

        for k in range(self.nr_iterations):
            for i in range(samples):
                output = inputs[i]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                error = self.loss_prime(outputs[i], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, self.learning_rate)
            if k % 2 == 0:
                print(k, end=' ')
        print()

    def predict(self, inputs):
        samples = len(inputs)
        result = []
        for i in range(samples):
            output = inputs[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            output = output.tolist()
            result.append(output.index(max(output)))
        return result


class MyLayer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagation(self, inp):
        pass

    def backward_propagation(self, output_error, learning_rate):
        pass


class MyFCLayer(MyLayer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = [[random.random() - 0.5 for _ in range(output_size)] for _ in range(input_size)]
        self.bias = [random.random() - 0.5 for _ in range(output_size)]

    def forward_propagation(self, inp):
        self.input = inp
        self.output = np.dot(self.input, self.weights).tolist()
        self.output = [a + b for a, b in zip(self.output, self.bias)]
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, utils.transpose_matrix(self.weights)).tolist()
        weights_error = np.dot(utils.transpose_matrix(self.input), [output_error]).tolist()
        self.weights -= np.multiply(weights_error, learning_rate)
        self.weights = self.weights.tolist()
        self.bias -= np.multiply(output_error, learning_rate)
        return input_error


class MyActivationLayer(MyLayer):
    def __init__(self, activation, activation_prime):
        super().__init__()
        self.activation = activation
        self.activation_prime = activation_prime

    def forward_propagation(self, inp):
        self.input = inp
        self.output = self.activation(self.input)
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error

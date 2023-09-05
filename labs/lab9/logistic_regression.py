import random
from math import exp


def sigmoid(x):
    return 1 / (1 + exp(-x))


class MyBinaryLogisticRegression:
    def __init__(self):
        self.intercept_ = 0.0
        self.coef_ = []

    def fit(self, x, y, learning_rate=0.001, no_epochs=1000, batch=False):
        self.coef_ = [random.random() for _ in range(len(x[0]))]
        if not batch:
            # stochastic
            for epoch in range(no_epochs):
                for i in range(len(x)):
                    y_computed = sigmoid(self.eval(x[i]))
                    crt_error = y_computed - y[i]
                    for j in range(len(x[0])):  # updating the coefs and intercept after every test
                        self.coef_[j] -= learning_rate * crt_error * x[i][j]
                    self.intercept_ -= learning_rate * crt_error * 1
        else:
            # batch
            x_mean = [[el[i] for el in x] for i in range(len(x[0]))]
            x_mean = [sum(el) / len(el) for el in x_mean]
            for epoch in range(no_epochs):
                error = 0.0
                for i in range(len(x)):
                    y_computed = sigmoid(self.eval(x[i]))
                    error += y_computed - y[i]
                error /= len(x)  # updating the coefs and intercept after every epoch
                for j in range(len(x[0])):
                    self.coef_[j] -= learning_rate * error * x_mean[j]
                self.intercept_ -= learning_rate * error * 1

    def eval(self, xi):
        yi = self.intercept_
        for j in range(len(xi)):
            yi += self.coef_[j] * xi[j]
        return yi

    def predict_one_sample(self, sample):
        threshold = 0.5
        computed_float_value = self.eval(sample)
        computed_sigmoid_value = sigmoid(computed_float_value)
        computed_label = 0 if computed_sigmoid_value < threshold else 1
        return computed_label

    def predict(self, inputs):
        computed_labels = [self.predict_one_sample(sample) for sample in inputs]
        return computed_labels


class MyMulticlassLogisticRegression:
    def __init__(self):
        self.intercept_ = []
        self.coef_ = []

    @property
    def intercept(self):
        return self.intercept_

    @intercept.setter
    def intercept(self, value):
        self.intercept_ = value

    @property
    def coef(self):
        return self.coef_

    @coef.setter
    def coef(self, value):
        self.coef_ = value

    def fit(self, x, y, learning_rate=0.001, no_epochs=1000, batch=False):
        binary_outputs = [[1 if el == value else 0 for el in y] for value in set(y)]
        self.intercept_ = [0.0 for _ in range(len(binary_outputs))]  # intercepts for each one vs all
        self.coef_ = [[random.random() for _ in range(len(x[0]))] for _ in range(len(binary_outputs))]
        if not batch:
            # stochastic
            for epoch in range(no_epochs):
                for i in range(len(x)):
                    for k in range(len(binary_outputs)):
                        y_computed = sigmoid(self.eval(x[i], self.intercept_[k], self.coef_[k]))
                        crt_error = y_computed - binary_outputs[k][i]
                        for j in range(len(x[0])):  # updating the coefs and intercept after every epoch
                            self.coef_[k][j] -= learning_rate * crt_error * x[i][j]
                        self.intercept_[k] -= learning_rate * crt_error * 1
        else:
            # batch
            x_mean = [[el[i] for el in x] for i in range(len(x[0]))]
            x_mean = [sum(el) / len(el) for el in x_mean]
            for epoch in range(no_epochs):
                error = [0.0 for _ in range(len(binary_outputs))]
                for i in range(len(x)):
                    for k in range(len(binary_outputs)):
                        y_computed = sigmoid(self.eval(x[i], self.intercept_[k], self.coef_[k]))
                        error[k] += y_computed - binary_outputs[k][i]
                for k in range(len(error)):
                    error[k] /= len(x)
                for k in range(len(binary_outputs)):  # updating the coefs and intercept after every epoch
                    for j in range(len(x[0])):
                        self.coef_[k][j] -= learning_rate * error[k] * x_mean[j]
                    self.intercept_[k] -= learning_rate * error[k] * 1

    def eval(self, xi, intercept, coef):
        yi = intercept
        for j in range(len(xi)):
            yi += coef[j] * xi[j]
        return yi

    def predict_one_sample(self, sample):
        values = []
        for i in range(len(self.intercept_)):
            computed_float_value = self.eval(sample, self.intercept_[i], self.coef_[i])
            computed_sigmoid_value = sigmoid(computed_float_value)
            values.append(computed_sigmoid_value)
        computed_label = values.index(max(values))
        return computed_label

    def predict(self, inputs):
        computed_labels = [self.predict_one_sample(sample) for sample in inputs]
        return computed_labels

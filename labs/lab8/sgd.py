import random


class MySgdRegression:
    def __init__(self):
        self.intercept_ = 0.0
        self.coef_ = []

    def fit(self, x, y, learning_rate=0.01, no_epochs=1000):
        self.coef_ = [random.random() for _ in range(len(x[0]))]
        for epoch in range(no_epochs):
            for i in range(len(x)):
                y_computed = self.eval(x[i])
                crt_error = y_computed - y[i]
                for j in range(len(x[0])):
                    self.coef_[j] -= learning_rate * crt_error * x[i][j]
                self.intercept_ -= learning_rate * crt_error * 1

    def eval(self, xi):
        yi = self.intercept_
        for j in range(len(xi)):
            yi += self.coef_[j] * xi[j]
        return yi

    def predict(self, x):
        y_computed = [self.eval(xi) for xi in x]
        return y_computed


class MyBgdRegression:
    def __init__(self):
        self.intercept_ = 0.0
        self.coef_ = []

    def fit(self, x, y, learning_rate=0.01, no_epochs=1000):
        self.coef_ = [random.random() for _ in range(len(x[0]))]
        x_mean = [[el[i] for el in x] for i in range(len(x[0]))]
        x_mean = [sum(el) / len(el) for el in x_mean]
        for epoch in range(no_epochs):
            error = 0.0
            for i in range(len(x)):
                y_computed = self.eval(x[i])
                error += y_computed - y[i]
            error /= len(x)
            for j in range(len(x[0])):
                self.coef_[j] -= learning_rate * error * x_mean[j]
            self.intercept_ -= learning_rate * error * 1

    def eval(self, xi):
        yi = self.intercept_
        for j in range(len(xi)):
            yi += self.coef_[j] * xi[j]
        return yi

    def predict(self, x):
        y_computed = [self.eval(xi) for xi in x]
        return y_computed

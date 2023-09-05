from sklearn import linear_model
from sgd import MySgdRegression, MyBgdRegression


def train_by_tool(trainInputs, trainOutputs):
    regressor = linear_model.SGDRegressor(alpha=0.01, max_iter=1000)
    regressor.fit(trainInputs, trainOutputs)
    w0, w1, w2 = regressor.intercept_[0], regressor.coef_[0], regressor.coef_[1]
    print('the learnt model: f(x) = ', w0, ' + ', w1, ' * x1 + ', w2, ' * x2' )
    return regressor


def train_by_my_stochastic_algorithm(train_inputs, train_outputs):
    regressor = MySgdRegression()
    regressor.fit(train_inputs, train_outputs)
    w0, w1, w2 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1]
    print('my learnt model: f(x1, x2) =', w0, '+', w1, '*x1 +', w2, '*x2')
    return regressor


def train_by_my_batch_algorithm(train_inputs, train_outputs):
    regressor = MyBgdRegression()
    regressor.fit(train_inputs, train_outputs)
    w0, w1, w2 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1]
    print('my learnt model: f(x1, x2) =', w0, '+', w1, '*x1 +', w2, '*x2')
    return regressor


def train_nonlinear_by_stochastic_algorithm(train_inputs, train_outputs):
    regressor = MySgdRegression()
    f1 = [el[0] for el in train_inputs]
    f2 = [el[1] for el in train_inputs]
    f3 = [x * x for x in f1]
    f4 = [f1[i] * f2[i] for i in range(len(f1))]
    f5 = [y * y for y in f2]
    train_in = [[el[0], el[1], el[2], el[3], el[4]] for el in zip(f1, f2, f3, f4, f5)]
    regressor.fit(train_in, train_outputs)
    w0, w1, w2, w3, w4, w5 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1],\
        regressor.coef_[2], regressor.coef_[3], regressor.coef_[4]
    print('my learnt model: f(a, b) =', w0, '+', w1, '*a +', w2, '*b +', w3, '*a^2 +', w4, '*ab +', w5, '*b^2')
    return regressor

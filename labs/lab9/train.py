from sklearn import linear_model

import logistic_regression


def train_by_tool(train_inputs, train_outputs):
    classifier = linear_model.LogisticRegression()
    classifier.fit(train_inputs, train_outputs)
    print('tool intercepts:', classifier.intercept_)
    print('tool coefficients:', classifier.coef_)
    return classifier


def train_by_my_algorithm(train_inputs, train_outputs, batch=False):
    if len(set(train_outputs)) == 2:
        classifier = logistic_regression.MyBinaryLogisticRegression()
    else:
        classifier = logistic_regression.MyMulticlassLogisticRegression()
    classifier.fit(train_inputs, train_outputs, batch=batch)
    print('my intercepts:', classifier.intercept_)
    print('my coefficients:', classifier.coef_)
    return classifier


def train_by_my_algorithm_cross_validation(train_inputs, train_outputs, batch=False, k_fold=5):
    if len(set(train_outputs)) == 2:
        classifier = logistic_regression.MyBinaryLogisticRegression()
    else:
        classifier = logistic_regression.MyMulticlassLogisticRegression()
    size = len(train_inputs) // k_fold
    folds = [train_inputs[k*size:(k+1)*size] for k in range(k_fold)]  # list of the k folds
    intercepts, coefs = [], []
    for fold in folds:
        fold_input = []
        for fold2 in folds:
            if fold2 is not fold:
                fold_input += fold2  # fold_input is k-1 folds
        classifier.fit(fold_input, train_outputs, batch=batch)
        intercepts.append(classifier.intercept_), coefs.append(classifier.coef_)

    intercepts = [[el[i] for el in intercepts] for i in range(len(intercepts[0]))]
    intercepts = [sum(el) / len(el) for el in intercepts]  # intercept is mean of the k trainings
    classifier.intercept = intercepts

    coefs2 = []
    for i in range(len(coefs[0])):
        coefs2.append([0.0 for _ in range(len(coefs[0][0]))])
    for k in range(len(coefs)):
        for i in range(len(coefs[k])):
            for j in range(len(coefs[k][i])):
                coefs2[i][j] += coefs[k][i][j]
    for i in range(len(coefs[0])):
        for j in range(len(coefs[i][0])):
            coefs2[i][j] /= len(coefs)  # coefs are mean of the k trainings
    classifier.coef_ = coefs2

    print('my intercepts:', classifier.intercept_)
    print('my coefficients:', classifier.coef_)
    return classifier


def test_function(computed_outputs, outputs):
    correct = 0.0
    for t1, t2 in zip(computed_outputs, outputs):
        if t1 == t2:
            correct += 1
    accuracy = correct / len(outputs)
    print('accuracy:', accuracy)

from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_iris


def load_data_cancer():
    data = load_breast_cancer()
    inputs = data['data']
    outputs = data['target']
    feature_names = list(data['feature_names'])
    i1, i2 = feature_names.index('mean radius'), feature_names.index('mean texture')
    inputs = [[feat[i1], feat[i2]] for feat in inputs]
    return inputs, outputs


def load_data_flowers():
    data = load_iris()
    inputs = data['data']
    outputs = data['target']
    feature_names = list(data['feature_names'])
    i1, i2 = feature_names.index('sepal length (cm)'), feature_names.index('sepal width (cm)')
    i3, i4 = feature_names.index('petal length (cm)'), feature_names.index('petal width (cm)')
    inputs = [[feat[i1], feat[i2], feat[i3], feat[i4]] for feat in inputs]
    return inputs, outputs


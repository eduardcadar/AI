import itertools

from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score

import my_classifier


def train_by_tool(train_features, n_clusters):
    unsupervised_classifier = KMeans(n_clusters=n_clusters, random_state=0)
    unsupervised_classifier.fit(train_features)
    return unsupervised_classifier


def train_by_my_algorithm(train_features, max_iterations, n_clusters):
    unsupervised_classifier = my_classifier.MyUnsupervisedClassifier(n_clusters=n_clusters)
    unsupervised_classifier.fit(train_features, max_iterations=max_iterations)
    return unsupervised_classifier


def accuracy(real, computed):
    accs, labels = [], set(computed)

    perms = itertools.permutations(labels)
    for perm in perms:
        legend = {}
        for i, label in enumerate(labels):
            legend[label] = perm[i]
        accs.append(accuracy_score(real, [legend[value] for value in computed]))
    return max(accs)

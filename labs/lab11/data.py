import csv
import os
import random

import gensim as gensim
import numpy as np
from sklearn.datasets import load_iris
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def load_data_iris():
    data = load_iris()

    inputs = data['data']
    outputs = data['target']
    return inputs, outputs, list(data.target_names)


def load_data(file_name):
    crt_dir = os.getcwd()
    filename = os.path.join(crt_dir, 'data', file_name)

    data = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                data_names = row
            else:
                data.append(row)
            line_count += 1

    inputs, outputs = [data[i][0] for i in range(len(data))], [data[i][1] for i in range(len(data))]
    label_names = list(set(outputs))
    return inputs, outputs, label_names


def split_data(data_in, data_out):
    # data_in - lista de liste, in fiecare lista sunt atributele unui test
    # data_out - lista de valori output
    random.seed()
    train_indexes = random.sample(range(len(data_in)), int(0.8 * len(data_in)))
    test_indexes = [i for i in range(len(data_in)) if i not in train_indexes]

    train_in = [data_in[i] for i in train_indexes]
    train_out = [data_out[i] for i in train_indexes]
    test_in = [data_in[i] for i in test_indexes]
    test_out = [data_out[i] for i in test_indexes]
    return train_in, train_out, test_in, test_out


def bag_of_words(train_inputs, test_inputs, n=1, max_features=50):
    vectorizer = CountVectorizer(max_features=max_features, ngram_range=(n, n))
    train_features = vectorizer.fit_transform(train_inputs)
    test_features = vectorizer.transform(test_inputs)
    return vectorizer.get_feature_names_out(), train_features.toarray().tolist(), test_features.toarray().tolist()


def word_granularity(train_inputs, test_inputs, n=1, max_features=50):
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(n, n))
    train_features = vectorizer.fit_transform(train_inputs)
    test_features = vectorizer.transform(test_inputs)
    return vectorizer.get_feature_names_out(), train_features.toarray().tolist(), test_features.toarray().tolist()


def word2vec(train_inputs, test_inputs):
    crt_dir = os.getcwd()
    model_path = os.path.join(crt_dir, 'models', 'GoogleNews-vectors.negative300.bin')

    word2vec_model300 = gensim.models.keyedvectors.load_word2vec_format(model_path, binary=True)
    return word2vec_model300


def feature_computation(model, data):
    features = []
    phrases = [phrase.split() for phrase in data]
    for phrase in phrases:
        vectors = [model[word] for word in phrase if (len(word) > 2) and (word in model.vocab.keys())]
        if len(vectors) == 0:
            result = [0.0] * model.vector_size
        else:
            result = np.sum(vectors, axis=0) / len(vectors)
        features.append(result)
    return features

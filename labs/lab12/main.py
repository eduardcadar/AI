import os
from math import sqrt

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from deepface import DeepFace
from fer import FER
from mtcnn import MTCNN
from skimage.feature import hog
from sklearn.metrics import accuracy_score

import data
import train


def plane_euclidean_distance(p1, p2):
    dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    return sqrt(dist)


def normalise_data(train_in, test_in):
    normalised_train_in, normalised_test_in = [[] for _ in range(len(train_in))], [[] for _ in range(len(test_in))]
    for i in range(len(train_in[0])):
        feature = [el[i] for el in train_in]
        tr_in, mean, std = data.statistical_normalisation(feature)
        te_in = [el[i] for el in test_in]
        te_in = data.statistical_normalisation(te_in, mean, std)[0]
        for j in range(len(normalised_train_in)):
            normalised_train_in[j].append(tr_in[j])
        for j in range(len(normalised_test_in)):
            normalised_test_in[j].append(te_in[j])
    return normalised_train_in, normalised_test_in


def flatten(t):
    return [item for sublist in t for item in sublist]


# def extract_face(filename, required_size=(160, 160)):
#     # load image from file
#     image = Image.open(filename)
#     image = image.convert('RGB')
#     pixels = np.asarray(image)
#     detector = MTCNN()
#     results = detector.detect_faces(pixels)
#     x1, y1, width, height = results[0]['box']
#     x1, y1 = abs(x1), abs(y1)
#     x2, y2 = x1 + width, y1 + height
#     face = pixels[y1:y2, x1:x2]
#     image = Image.fromarray(face)
#     image = image.resize(required_size)
#     face_array = np.asarray(image)
#     return face_array


def solve_iter1(inputs, outputs, layers):
    inputs = [flatten(x) for x in inputs]
    train_in, train_out, test_in, test_out = data.split_data(inputs, outputs)
    train_in, test_in = normalise_data(train_in, test_in)

    classifier = train.train_by_tool(train_in, train_out, layers=layers)
    predicted_labels = classifier.predict(test_in)
    acc = accuracy_score(test_out, predicted_labels)
    return acc


def solve_iter2(inputs, outputs):
    predicted_dominant_fer = []
    emotion_detector = FER(mtcnn=True)
    for i, img in enumerate(inputs):
        test_img = cv2.imread(img)
        print('---------------- FER', i, '----------------')
        emotion = emotion_detector.top_emotion(test_img)[0]
        predicted_dominant_fer.append(emotion)

    for i, em in enumerate(predicted_dominant_fer):
        if em is None:
            predicted_dominant_fer[i] = ''

    predicted_dominant_deepface, predicted_all_deepface = [], []
    for i, img in enumerate(inputs):
        print('---------------- DEEPFACE', i, '----------------')
        result = DeepFace.analyze(img_path=img, enforce_detection=False)
        predicted_dominant_deepface.append(result['dominant_emotion'])
        pred_labels = {}
        for emotion, value in result['emotion'].items():
            if value >= 2:
                pred_labels[emotion] = value
        predicted_all_deepface.append(pred_labels)

    fer_acc = accuracy_score(outputs, predicted_dominant_fer)
    deepface_acc = accuracy_score(outputs, predicted_dominant_deepface)
    return fer_acc, deepface_acc, predicted_all_deepface


def solve_iter3_hog(inputs, outputs, layers):
    hog_inputs = []
    for i, imagePath in enumerate(inputs):
        image = cv2.imread(imagePath)
        hog_feature = hog(image, orientations=8, pixels_per_cell=(4, 4),
                          cells_per_block=(2, 2), visualize=False, channel_axis=-1)
        hog_inputs.append(hog_feature)

    train_in, train_out, test_in, test_out = data.split_data(hog_inputs, outputs)
    train_in, test_in = normalise_data(train_in, test_in)

    classifier = train.train_by_tool(train_in, train_out, layers=layers)
    predicted_labels = classifier.predict(test_in)
    acc = accuracy_score(test_out, predicted_labels)
    return acc


def solve_iter3_mtcnn(inputs, outputs, layers):
    detector = MTCNN()
    mtcnn_inputs = []
    bad = []
    for i, img in enumerate(inputs):
        print('------------ MTCNN', i, '------------')
        image = cv2.imread(img)
        result = detector.detect_faces(image)
        if len(result) < 1:
            bad.append(img)
            outputs.pop(i)
            continue
        keypoints, coordinates, distances = result[0]['keypoints'], [], []
        pixels = list(keypoints.values())
        # for key, value in keypoints.items():
        #     coordinates.append(value[0])
        #     coordinates.append(value[1])
        # mtcnn_inputs.append(coordinates)
        for j in range(len(pixels)):
            p1 = pixels[j]
            for k in range(j + 1, len(pixels)):
                p2 = pixels[k]
                distances.append(plane_euclidean_distance(p1, p2))
        mtcnn_inputs.append(distances)
    print("images where it didn't detect face:", len(bad))

    train_in, train_out, test_in, test_out = data.split_data(mtcnn_inputs, outputs)
    train_in, test_in = normalise_data(train_in, test_in)

    classifier = train.train_by_tool(train_in, train_out, layers=layers)
    predicted_labels = classifier.predict(test_in)
    acc = accuracy_score(test_out, predicted_labels)
    return acc


def solve():
    inputs_sad, outputs_sad = data.load_emoji_images('sad')
    inputs_happy, outputs_happy = data.load_emoji_images('happy')
    inputs_emoji, outputs_emoji = inputs_happy + inputs_sad, outputs_happy + outputs_sad
    inputs_faces, outputs_faces = data.load_all_faces(nr=200)
    layers_emojis = (20, 20)
    layers_hog = (48, 96, 48)
    layers_mtcnn = (10, 20, 10)
    emoji_acc = solve_iter1(inputs_emoji, outputs_emoji, layers_emojis)
    fer_acc, deepface_acc, deepface_labels = solve_iter2(inputs_faces, outputs_faces)
    hog_acc = solve_iter3_hog(inputs_faces, outputs_faces, layers=layers_hog)
    mtcnn_acc = solve_iter3_mtcnn(inputs_faces, outputs_faces, layers=layers_mtcnn)
    print('(iter 1) emojis accuracy:', emoji_acc)
    print('(iter 2) fer accuracy:', fer_acc)
    print('(iter 2) deepface accuracy:', deepface_acc)
    print('multilabel deepface:', deepface_labels[:5])
    print('(iter 3 - manual) hog accuracy:', hog_acc)
    print('(iter 3 - automatic) mtcnn accuracy:', mtcnn_acc)


solve()

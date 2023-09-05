import os
import random

from PIL import Image


def load_all_faces(nr=-1):
    inp_angry, out_angry = load_faces_data('angry', n=nr)
    inp_disgust, out_disgust = load_faces_data('disgust', n=nr)
    inp_fear, out_fear = load_faces_data('fear', n=nr)
    inp_happy, out_happy = load_faces_data('happy', n=nr)
    inp_neutral, out_neutral = load_faces_data('neutral', n=nr)
    inp_sad, out_sad = load_faces_data('sad', n=nr)
    inp_surprise, out_surprise = load_faces_data('surprise', n=nr)
    inputs = inp_angry + inp_disgust + inp_fear + inp_happy + inp_neutral + inp_sad + inp_surprise
    outputs = out_angry + out_disgust + out_fear + out_happy + out_neutral + out_sad + out_surprise
    return inputs, outputs


def load_faces_data(expression, n=-1):
    directory = './images/faces/' + expression
    if n > 0:
        inputs = [directory + '/' + filename for filename in os.listdir(directory)[:n]]
    else:
        inputs = [directory + '/' + filename for filename in os.listdir(directory)]
    outputs = [expression] * len(inputs)

    return inputs, outputs


def load_emoji_images(sentiment):
    directory = os.fsencode('./images/emojis/' + sentiment)
    inputs, outputs = [], []

    for filename in os.listdir(directory):
        image = os.fsdecode(filename)
        img = Image.open('./images/emojis/' + sentiment + '/' + image)
        px = img.load()
        image_pixels = []
        width, height = img.size
        for i in range(width):
            for j in range(height):
                image_pixels.append(px[(i, j)])
        inputs.append(image_pixels)
        outputs.append(sentiment)
    return inputs, outputs


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


def statistical_normalisation(features, mean_value=None, std_dev_value=None):
    if mean_value is None:
        mean_value = sum(features) / len(features)
    features = [feat - mean_value for feat in features]
    if std_dev_value is None:
        std_dev_value = ((1 / len(features)) * sum([feat ** 2 for feat in features])) ** 0.5
    if std_dev_value == 0:
        normalised_features = [0 for _ in features]
    else:
        normalised_features = [feat / std_dev_value for feat in features]
    return normalised_features, mean_value, std_dev_value

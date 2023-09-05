import os
import random

from PIL import Image
from sklearn.datasets import load_digits
from sklearn.datasets import load_iris


def resize_images():
    directory = os.fsencode('./images/img')
    for filename in os.listdir(directory):
        image = os.fsdecode(filename)
        img = Image.open('./images/img/' + image)
        img.resize((60, 60)).save('./images/img/' + image)


def load_images():
    directory = os.fsencode('./images/img')
    inputs, outputs = [], []
    x_size, y_size = 60, 60
    with open('./images/images.txt', "r") as fout:
        for line in fout:
            line = line.rstrip()
            image_info = line.split(',')
            filename, output = image_info[0], int(image_info[1])
            image = os.fsdecode(filename)
            img = Image.open(image)
            px = img.load()
            image_pixels = []
            for i in range(x_size):
                for j in range(y_size):
                    image_pixels.append(px[(i, j)])

            inputs.append(image_pixels)
            outputs.append(output)
            if len(outputs) >= 100:
                break
    return inputs, outputs


def load_data(data_name):
    data = None
    if data_name == 'flowers':
        data = load_iris()
    if data_name == 'digits':
        data = load_digits()

    inputs = data['data']
    outputs = data['target']
    return inputs, outputs, list(data.target_names)


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


def sepia(image_path: str) -> Image:
    img = Image.open(image_path)
    width, height = img.size

    pixels = img.load()  # create the pixel map

    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    return img

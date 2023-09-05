
def read_regression(file_name):
    real_values, predicted_values = [], []
    with open(file_name, "r") as fin:
        first_line = fin.readline().split(",")
        attributes = first_line[:len(first_line)//2]
        line = fin.readline()
        while line:
            values = line.split(",")
            values[-1] = values[-1].strip()

            middle = len(values)//2
            real_str = values[:middle]
            predicted_str = values[middle:]

            real, predicted = [], []
            for i in range(len(real_str)):
                real.append(float(real_str[i]))
                predicted.append(float(predicted_str[i]))

            real_values.append(real)
            predicted_values.append(predicted)
            line = fin.readline()

    params = {
        'attributes': attributes,
        'real_values': real_values,
        'predicted_values': predicted_values
    }
    return params


def read_classification(file_name):
    real_labels, predicted_labels = [], []
    with open(file_name, "r") as fin:
        # skip first line
        fin.readline()
        line = fin.readline()
        while line:
            values = line.split(",")
            real_labels.append(values[0])
            predicted_labels.append(values[1].strip())
            line = fin.readline()

    params = {
        'labels': list(set(real_labels)),
        'real': real_labels,
        'predicted': predicted_labels
    }
    return params


def read_class_probabilities(file_name):
    real_labels, computed_outputs = [], []
    with open(file_name, "r") as fin:
        line = fin.readline()
        labels = line.split(",")
        labels[-1] = labels[-1].strip()
        line = fin.readline()
        while line:
            values = line.split(",")
            values[-1] = values[-1].strip()
            real_labels.append(values[0])
            computed_outputs.append(list(float(value) for value in values[1:]))
            line = fin.readline()
    params = {
        'labels': labels,
        'real_labels': real_labels,
        'computed_outputs': computed_outputs
    }
    return params


def read_multi_label_probabilities(file_name):
    with open(file_name, "r") as fin:
        line = fin.readline()
        labels = line.split(",")
        labels[-1] = labels[-1].strip()

        line = fin.readline()
        real_outputs, computed_outputs = [], []
        while line:
            values = line.split(",")
            values[-1] = values[-1].strip()
            n = len(values)
            real = []
            for value in values[:n//2]:
                real.append(int(value))
            real_outputs.append(real)

            dataset_outputs = []
            for value in values[n//2:]:
                dataset_outputs.append(float(value))

            computed_outputs.append(dataset_outputs)
            line = fin.readline()

    params = {
        'labels': labels,
        'real_outputs': real_outputs,
        'computed_outputs': computed_outputs
    }
    return params


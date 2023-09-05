from collections import defaultdict


def get_confusion_matrix(labels, real, predicted):
    matrix = {}
    for label in labels:
        matrix[label] = defaultdict(int)

    for i in range(len(real)):
        matrix[real[i]][predicted[i]] += 1

    return matrix


def print_matrix(matrix, labels):
    a = []
    header = ['R \\ P']
    for real_label in labels:
        header.append(real_label)
    a.append(header)

    for real_label in labels:
        row = [real_label]
        for predicted_label in labels:
            row.append(matrix[real_label][predicted_label])
        a.append(row)

    s = [[str(e) for e in row] for row in a]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

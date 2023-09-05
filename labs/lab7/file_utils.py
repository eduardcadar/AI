import csv


def load_data(file_name, input_name1, input_name2, output_name):
    data, data_labels = [], []
    with open(file_name, "r") as fin:
        csv_reader = csv.reader(fin)
        first = True
        for row in csv_reader:
            if first:
                data_labels = row
            else:
                data.append(row)
            first = False

    out_idx = data_labels.index(output_name)
    inp_idx1 = data_labels.index(input_name1)
    inp_idx2 = data_labels.index(input_name2)
    data_inputs1 = [float(data[i][inp_idx1]) for i in range(len(data))]
    data_inputs2 = [float(data[i][inp_idx2]) for i in range(len(data))]
    data_outputs = [float(data[i][out_idx]) for i in range(len(data))]

    return data_labels, data_inputs1, data_inputs2, data_outputs

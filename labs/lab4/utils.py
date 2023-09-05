import re


def read_input(abs_file_path):
    with open(abs_file_path, "r") as fin:
        lines = fin.readlines()
    # print(lines)
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()

    matrix = []
    n = int(lines[0])
    i = 0
    while len(matrix) < n:
        matrix_line = []
        while len(matrix_line) < n:
            line = lines[i + 1]
            line = line.strip()
            values = re.split(",| +", line)
            for value in values:
                matrix_line.append(float(value))
            i += 1
        matrix.append(matrix_line)
    params = {"no_nodes": n,
              "matrix": matrix,
              "source": int(lines[-2]) - 1,
              "destination": int(lines[-1]) - 1
              }
    return params

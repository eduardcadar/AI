
def transpose_matrix(matrix):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def multiply_matrices(matrix_a, matrix_b):
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError('No. columns of first matrix is not the same as no. rows of second matrix')
    a, b = matrix_a, matrix_b
    result = [[] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            p = 0
            for k in range(len(a[i])):
                p += a[i][k] * b[k][j]
            result[i].append(p)
    return result


def determinant(matrix):
    a = matrix
    if len(a) != len(a[0]):
        raise ValueError('not square matrix')
    if len(a) == 1:
        return a[0][0]
    if len(a) == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    result = 0
    factor = 1
    for i in range(len(a)):
        b = minor(a, 0, i)
        result += factor * a[0][i] * determinant(b)
        factor *= -1
    return result


def minor(matrix, i, j):
    return [[matrix[h][k] for k in range(len(matrix[0])) if k != j] for h in range(len(matrix)) if h != i]


def cofactor(matrix, i, j):
    return ((-1) ** (i+j)) * determinant(minor(matrix, i, j))


def adjoint(matrix):
    a = [[cofactor(matrix, i, j) for j in range(len(matrix[0]))] for i in range(len(matrix))]
    return transpose_matrix(a)


def inverse(matrix):
    d = determinant(matrix)
    if d == 0:
        raise ValueError('Matrix determinant = 0')
    adj = adjoint(matrix)
    for i in range(len(adj)):
        for j in range(len(adj[i])):
            adj[i][j] *= 1/d
    return adj

import chromosome
import chromosome_inv


def calculate_cost(ch, matrix):
    path = None
    if isinstance(ch, chromosome.Chromosome):
        path = ch.repres
    elif isinstance(ch, chromosome_inv.ChromosomeInv):
        path = ch.path()
    cost = 0
    for i in range(len(path)):
        cost += matrix[path[i-1]][path[i]]
    return cost


def calculate_path_cost(ch, matrix):
    cost = 0
    path = ch.repres
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i+1]]
    return cost

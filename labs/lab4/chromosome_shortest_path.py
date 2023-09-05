import random


class ChromosomeShortestPath:
    def __init__(self, repres, no_nodes):
        self.__repres = repres
        self.__fitness = 1000000
        self.__no_nodes = no_nodes

    @property
    def repres(self):
        return self.__repres

    @repres.setter
    def repres(self, value):
        self.__repres = value

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        self.__fitness = value

    def crossover(self, c, a):
        common_points = []
        for i in range(min(len(self.__repres), len(c.repres))):
            if self.__repres[i] == c.repres[i]:
                common_points.append(i)
        j = random.randint(0, len(common_points) - 1)
        unique: list = c.repres[j:]
        new_repres = self.__repres[:j]
        for node in new_repres:
            if node in unique:
                unique.remove(node)
        return ChromosomeShortestPath(new_repres + unique, self.__no_nodes)

    def mutate(self):
        r = random.random()
        if len(self.__repres) == self.__no_nodes or (len(self.__repres) > 2 and r >= 0.5):
            a = random.randint(1, len(self.__repres) - 2)
            self.__repres.pop(a)
        else:
            values = [i for i in range(self.__no_nodes)]
            for value in self.__repres:
                values.remove(value)
            a = random.randint(1, len(self.__repres) - 1)
            self.__repres = self.__repres[:a] + random.sample(values, 1) + self.__repres[a:]

    def same_fitness(self, c):
        return self.__fitness == c.fitness

    def is_fitter_than(self, c):
        return self.__fitness < c.fitness

    def __str__(self):
        indexed = self.__repres[:]
        for i in range(len(indexed)):
            indexed[i] += 1
        return str(len(indexed)) + " nodes: " + str(indexed) + ", cost: " + str(self.__fitness)

    def __eq__(self, other):
        if not isinstance(other, ChromosomeShortestPath):
            return False
        return self.__repres == other.repres


def get_random_chromosome(n, source, destination):
    length = random.randint(0, n - 2)
    values = [i for i in range(n)]
    values.remove(source), values.remove(destination)
    return ChromosomeShortestPath([source] + random.sample(values, length) + [destination], n)

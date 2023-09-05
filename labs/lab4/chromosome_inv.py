import random


class ChromosomeInv:
    def __init__(self, repres):
        # representation as inversion sequence
        self.__repres = repres
        self.__fitness = 1000000

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

    def crossover(self, c, pos):
        return ChromosomeInv(self.__repres[:pos] + c.repres[pos:])

    def mutate(self):
        i = random.randint(0, len(self.__repres) - 1)
        self.__repres[i] = random.randint(0, len(self.__repres) - i - 1)

    def path_to_inv(self, p):
        inv = [0] * len(self.__repres)
        for i in range(len(self.__repres)):
            inv[i] = 0
            m = 0
            while p[m] != i:
                if p[m] > i:
                    inv[i] += 1
                m += 1
        self.__repres = inv

    def path(self):
        pos = [0] * len(self.__repres)
        path = [0] * len(self.__repres)
        i = len(self.__repres) - 1
        while i >= 0:
            for m in range(i+1, len(self.__repres)):
                if pos[m] >= self.__repres[i]:
                    pos[m] += 1
            pos[i] = self.__repres[i]
            i -= 1
        for i in range(len(self.__repres)):
            path[pos[i]] = i
        return path

    def same_fitness(self, c):
        return self.__fitness == c.fitness

    def is_fitter_than(self, c):
        return self.__fitness < c.fitness

    def __str__(self):
        indexed = self.path()
        for i in range(len(indexed)):
            indexed[i] += 1
        return str(indexed) + ", cost: " + str(self.__fitness)

    def __eq__(self, other):
        if not isinstance(other, ChromosomeInv):
            return False
        return self.__repres == other.repres


def generate_random_chromosome(n):
    seq = []
    for i in range(n):
        seq.append(random.randint(0, n-i-1))
    return ChromosomeInv(seq)

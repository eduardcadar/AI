import math
import random

import fitness


class Chromosome:
    def __init__(self, repres):
        self.__repres = repres
        self.__fitness = 1000000

    @property
    def repres(self):
        return self.__repres

    @repres.setter
    def repres(self, r):
        self.__repres = r

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, f):
        self.__fitness = f

    def crossover(self, c, a):
        # return self.crossover1(c)
        # return self.crossover2(c)
        return self.crossover3(c)

    def crossover1(self, c):
        a = random.randint(1, len(self.__repres) - 1)
        b = random.randint(a, len(self.__repres))
        new_repres = [-1] * len(self.__repres)
        used = [False] * len(self.__repres)
        for i in range(a, b):
            new_repres[i] = self.__repres[i]
            used[new_repres[i]] = True
        j = b
        for i in range(b, len(self.__repres)):
            if j >= len(self.__repres):
                j = 0
            while used[c.repres[j]]:
                j += 1
                if j >= len(self.__repres):
                    j = 0
            new_repres[i] = c.repres[j]
            used[new_repres[i]] = True
            j += 1
        return Chromosome(new_repres)

    def crossover2(self, c):
        new_repres = []
        used = [False] * len(self.__repres)
        i = 0
        while len(new_repres) < len(self.__repres):
            first = self.__repres[i]
            if not used[first]:
                used[first] = True
                new_repres.append(first)
            if len(new_repres) == len(self.__repres):
                break
            second = c.repres[i]
            if not used[second]:
                used[second] = True
                new_repres.append(second)
            i += 1
        return Chromosome(new_repres)

    def crossover3(self, c):
        new_repres = c.repres[:]
        a = random.randint(1, len(self.__repres) - 1)
        b = random.randint(a + 1, len(self.__repres))
        for gene in self.__repres[a:b]:
            new_repres.remove(gene)
        new_repres += random.sample(self.__repres[a:b], b - a)
        return Chromosome(new_repres)

    def mutate(self):
        a, b = random.randint(1, len(self.__repres) - 1), random.randint(1, len(self.__repres) - 1)
        self.__repres[a], self.__repres[b] = self.__repres[b], self.__repres[a]

    def same_fitness(self, c):
        return self.__fitness == c.fitness

    def is_fitter_than(self, c):
        return self.__fitness < c.fitness

    def __str__(self):
        indexed = self.__repres[:]
        for i in range(len(indexed)):
            indexed[i] += 1
        return str(indexed) + ", cost: " + str(self.__fitness)

    def __eq__(self, other):
        if not isinstance(other, Chromosome):
            return False
        return self.__repres == other.repres


def generate_new_chromosome(n):
    return random.sample(range(0, n), n)


def fix_path(p, f, matrix):
    path2 = p[:]
    n = len(p)
    for i in random.sample(range(1, len(p) - 1), math.ceil(math.sqrt(n))):
        path2[i], path2[i+1] = path2[i+1], path2[i]
        f2 = fitness.calculate_cost(Chromosome(path2), matrix)
        if f2 < f:
            f = f2
        else:
            path2[i], path2[i + 1] = path2[i + 1], path2[i]
    return path2

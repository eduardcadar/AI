from random import randint


class Chromosome:
    def __init__(self, communities, max_value):
        # repr = communities
        self.__representation = communities
        self.__fitness = 0.0
        self.__max_value = max_value

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness):
        self.__fitness = fitness

    @property
    def representation(self):
        return self.__representation

    @representation.setter
    def representation(self, communities):
        self.__representation = communities

    def crossover(self, c):
        vertex = randint(0, len(self.__representation) - 1)
        com_number = self.__representation[vertex]
        new_communities = c.representation[:]
        for i in range(len(self.__representation)):
            if self.__representation[i] == com_number:
                new_communities[i] = com_number

        return Chromosome(new_communities, self.__max_value)

    def mutation(self):
        pos = randint(0, len(self.__representation) - 1)
        self.__representation[pos] = randint(0, self.__max_value)

    def is_fitter_than(self, c):
        return self.__fitness > c.fitness

    def __str__(self) -> str:
        return str(self.__representation)

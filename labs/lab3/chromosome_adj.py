from random import randint


class ChromosomeAdj:
    def __init__(self, adj_list, max_value):
        # repr = adj list
        self.__representation = adj_list
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
    def ads_list(self, adj_list):
        self.__representation = adj_list

    def crossover(self, c):
        binary_vector = [randint(0, 1) for _ in range(len(self.__representation))]
        new_adj_list = len(self.__representation) * [0]
        for i in range(len(self.__representation)):
            if binary_vector[i]:
                new_adj_list[i] = self.__representation[i]
            else:
                new_adj_list[i] = c.representation[i]
        return ChromosomeAdj(new_adj_list, self.__max_value)

    def mutation(self, i, j):
        self.__representation[i] = j

    def is_fitter_than(self, c):
        return self.__fitness > c.fitness

    def __str__(self) -> str:
        return str(self.__representation)

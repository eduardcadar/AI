import copy
import math
import os.path
import random
import time

import chromosome
import chromosome_inv
import chromosome_shortest_path
import fitness
import selection
import utils


def solve(params, pb):
    population = []
    for _ in range(pb["population_size"]):
        population.append(random_chromosome(params["no_nodes"]))
    for ch in population:
        ch.fitness = fitness.calculate_cost(ch, params["matrix"])

    for ch in population:
        ch.repres = chromosome.fix_path(ch.repres, ch.fitness, params["matrix"])

    new_ch = chromosome.Chromosome(population[0].repres)
    new_ch.fitness = population[0].fitness
    best_list = [new_ch]

    for generation in range(pb["no_generations"]):
        for ch in population:
            ch.fitness = fitness.calculate_cost(ch, params["matrix"])
            if ch.same_fitness(best_list[0]) and ch not in best_list:
                new_ch = copy.copy(ch)
                new_ch.repres = ch.repres[:]
                new_ch.fitness = ch.fitness
                best_list.append(new_ch)
            elif ch.is_fitter_than(best_list[0]):
                new_ch = copy.copy(ch)
                new_ch.repres = ch.repres[:]
                new_ch.fitness = ch.fitness
                best_list = [new_ch]

        children = []
        children += selection.tournament_selection(
            population, pb["population_size"] - pb["no_elites"], pb["no_tournament_participants"])

        population = sorted(population, key=lambda c: c.fitness)
        children += population[:pb["no_elites"]]
        children = sorted(children, key=lambda c: c.fitness)

        for ch in population[:math.ceil(math.sqrt(len(population)))]:
            path = ch.repres
            p = chromosome.fix_path(path, ch.fitness, params["matrix"])
            ch.repres = p

        for ch in children:
            if random.random() < pb["mutation_chance"]:
                ch.mutate()

        if generation % 100 == 0:
            print(generation, best_list[0].fitness)

    print()
    print("TSP")
    for ch in best_list:
        print(ch)


def random_chromosome(n):
    return chromosome.Chromosome([0] + random.sample(range(1, n), n-1))
    # return chromosome_inv.generate_random_chromosome(n)


def solve_shortest_path(params, pb):
    population = []
    for _ in range(pb["population_size"]):
        population.append(chromosome_shortest_path.get_random_chromosome(
            params["no_nodes"], params["source"], params["destination"]))

    new_ch = chromosome_shortest_path.ChromosomeShortestPath(population[0].repres, params["no_nodes"])
    new_ch.fitness = population[0].fitness
    best_list = [new_ch]

    for generation in range(pb["no_generations"]):
        for ch in population:
            ch.fitness = fitness.calculate_path_cost(ch, params["matrix"])
            if ch.same_fitness(best_list[0]) and ch not in best_list:
                new_ch = copy.copy(ch)
                new_ch.repres = ch.repres[:]
                new_ch.fitness = ch.fitness
                best_list.append(new_ch)
            elif ch.is_fitter_than(best_list[0]):
                new_ch = copy.copy(ch)
                new_ch.repres = ch.repres[:]
                new_ch.fitness = ch.fitness
                best_list = [new_ch]

        children = selection.tournament_selection(
            population, pb["population_size"] - pb["no_elites"], pb["no_tournament_participants"])

        population = sorted(population, key=lambda c: c.fitness)
        children += population[:pb["no_elites"]]

        for ch in children:
            if random.random() < pb["mutation_chance"]:
                ch.mutate()

        # if generation % 100 == 0:
        #     print(generation, best_list[0].fitness)

    print()
    print("SHORTEST PATH", params["source"] + 1, "-", params["destination"] + 1)
    for ch in best_list:
        print(ch)


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "inputs/kn57_dist.txt")
    pb_params = {
                "no_generations": 200,
                "population_size": 50,
                "no_elites": 4,
                "no_tournament_participants": 4,
                "mutation_chance": 0.1,
                }
    random.seed(time.time())
    # file_params is dictionary with keys: no_nodes, matrix, source, destination
    file_params = utils.read_input(file_path)
    start = time.time()
    solve(file_params, pb_params)
    end = time.time()
    print("time:", end - start)
    start = time.time()
    solve_shortest_path(file_params, pb_params)
    end = time.time()
    print("time:", end - start)

"""
4 easy_01_tsp - cost minim: 14
9 test1 - cost minim: 21.8 ?
6 test2 - cost minim: 76
57 kn57_dist - cost minim: 34282 ?
48 att48_d - cost minim: 33523
42 dantzig42_d - cost minim: 699
128 sgb128_dist - cost minim: 95634 ?
312 usca312_dist - cost minim: 260826 ?
"""

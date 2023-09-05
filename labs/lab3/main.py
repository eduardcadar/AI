import random
import time

import modularitydensity.metrics
import networkx as nx
import numpy as np
from modularitydensity.fine_tuned_modularity_density import fine_tuned_clustering_qds

import fitness
import selection
import utils
from chromosome import Chromosome
from chromosome_adj import ChromosomeAdj


def fix_chromosome(graph, graph_label, chromosome):
    if isinstance(chromosome, ChromosomeAdj):
        return
    communities = chromosome.representation
    some = random.sample(range(0, len(communities)), 2)
    for index in some:
        for neighbour in graph[graph_label[index]]:
            communities[graph.nodes[neighbour]['id']] = communities[index]


def solve(file, params):
    if params['population_size'] % 2 == 1:
        print("population_size should be an even number")
        return

    graph = nx.read_gml(file, label=None)
    no_nodes = len(graph.nodes)

    # graph_label[id_nod] = label_nod
    graph_label = {}
    i = 0
    for node in graph.nodes:
        graph_label[i] = node
        i += 1

    # graph.nodes[label_nod]['id'] = id_nod
    i = 0
    for node in graph.nodes:
        graph.nodes[node].update({'id': i})
        i += 1

    # max_value = params['no_communities'] - 1
    max_value = len(graph.nodes) - 1
    best_chromosome = get_random_chromosome(graph, max_value)
    best_chromosome.fitness = calculate_fitness(graph, best_chromosome)

    population = []
    random.seed(time.time())

    # random chromosomes
    for _ in range(params['population_size']):
        new_chromosome = get_random_chromosome(graph, max_value)
        fix_chromosome(graph, graph_label, new_chromosome)
        population.append(new_chromosome)

    for generation in range(params['no_generations']):
        for chromosome in population:
            chromosome.fitness = calculate_fitness(graph, chromosome)
            if chromosome.is_fitter_than(best_chromosome):
                best_chromosome = chromosome
        population = sorted(population, reverse=True, key=lambda c: c.fitness)
        children = population[:params['no_elites']]

        # children = selection.roulette_selection(population, len(population))
        children += selection.tournament_selection(
            population, len(population) - params['no_elites'], params['no_tournament_participants'])

        population = children
        for chromosome in population:
            if random.random() < params['mutation_chance']:
                if isinstance(chromosome, Chromosome):
                    chromosome.mutation()
                elif isinstance(chromosome, ChromosomeAdj):
                    pos = random.randint(0, no_nodes - 1)
                    node = graph_label[pos]
                    neighbour = random.sample(list(graph[node]), 1)[0]
                    neighbour_id = graph.nodes[neighbour]['id']
                    chromosome.mutation(pos, neighbour_id)

        if isinstance(population[0], Chromosome):
            for chromosome in population:
                fitness.clean_up(
                    graph, chromosome.representation,
                    params['variance_threshold'], int(params['percent_nodes_variance_check'] * no_nodes))

        if generation % 10 == 0:
            print(generation, end=' ')
            print(best_chromosome.fitness)

    print()
    utils.print_answer(best_chromosome, graph_label)

    if isinstance(best_chromosome, Chromosome):
        communities = best_chromosome.representation
    elif isinstance(best_chromosome, ChromosomeAdj):
        communities = utils.adj_to_communities(best_chromosome.representation)
    adj = nx.to_scipy_sparse_array(graph)
    print(modularitydensity.metrics.modularity_density(adj, communities, np.unique(communities)))
    utils.draw_communities(graph, best_chromosome)


def get_random_chromosome(graph, max_value):
    return ChromosomeAdj(utils.get_random_adj_list(graph), max_value)
    # return Chromosome(utils.get_random_communities(len(graph.nodes), max_value), max_value)


def calculate_fitness(graph, chromosome):
    if isinstance(chromosome, Chromosome):
        communities = chromosome.representation
    elif isinstance(chromosome, ChromosomeAdj):
        communities = utils.adj_to_communities(chromosome.representation)

    adj = nx.to_scipy_sparse_array(graph)
    # return fitness.modularity(graph, communities)
    return fitness.modularity_density(graph, communities)
    # return modularitydensity.metrics.modularity_density(adj, communities, np.unique(communities))
    # return fitness.community_score(graph, communities)


if __name__ == '__main__':
    parameters = {}
    parameters['no_generations'] = 200
    parameters['mutation_chance'] = 0.1
    parameters['crossover_chance'] = 1
    parameters['population_size'] = 50
    parameters['no_tournament_participants'] = 4
    parameters['no_elites'] = 2
    parameters['variance_threshold'] = 0.6
    parameters['percent_nodes_variance_check'] = 0.4

    # parameters['no_communities'] = 3

    start = time.time()
    solve(utils.get_abs_path("graphs/lesmis.gml"), parameters)
    end = time.time()
    print("time:", end - start)

"""
1. karate - 2 communities
2. football - 12 communities
3. dolphins - 2 communities
4. krebs - 3 communities

5. myGraph - 4 communities
6. adjnoun - 69 communities
7. news_2cl1_0.1 - 2 communities
8. lesmis - 7 communities
9. celegansneural - 6 communities
10. jazz - 2 communities?
"""
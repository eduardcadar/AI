import os
import random
from collections import defaultdict
from random import randint

import matplotlib.pyplot as plt
import networkx as nx

from chromosome import Chromosome
from chromosome_adj import ChromosomeAdj


def get_abs_path(file):
    return os.path.join(os.path.dirname(__file__), file)


def get_random_communities(no_nodes, max_value):
    communities = []
    for _ in range(no_nodes):
        communities.append(randint(0, max_value))
    return communities


def get_random_adj_list(graph):
    adj_list = []
    for node in graph.nodes:
        neighbour = random.sample(list(graph[node]), 1)[0]
        adj_list.append(graph.nodes[neighbour]['id'])
    return adj_list


def adj_to_communities(adj_list):
    crt_com = 1
    previous = [-1] * len(adj_list)
    communities = [-1] * len(adj_list)
    for i in range(len(adj_list)):
        ctr = 0
        if communities[i] == -1:
            communities[i] = crt_com
            neighbour = adj_list[i]
            previous[ctr] = i
            ctr += 1
            while communities[neighbour] == -1:
                previous[ctr] = neighbour
                communities[neighbour] = crt_com
                neighbour = adj_list[neighbour]
                ctr += 1
            if communities[neighbour] != crt_com:
                ctr -= 1
                while ctr >= 0:
                    communities[previous[ctr]] = communities[neighbour]
                    ctr -= 1
            else:
                crt_com += 1
    # no_communities = crt_com
    return communities


def get_adj_matrix(graph):
    adj_matrix = defaultdict(dict)
    for i in graph.nodes:
        adj_matrix[i] = defaultdict(bool)
        for j in graph.nodes:
            if (i, j) in graph.edges:
                adj_matrix[i][j] = True
    return adj_matrix


def print_answer(chromosome, graph_label):
    networks = defaultdict(list)
    i = 1
    visited = {}
    if isinstance(chromosome, Chromosome):
        communities = chromosome.representation
    elif isinstance(chromosome, ChromosomeAdj):
        communities = adj_to_communities(chromosome.representation)

    for j in range(len(communities)):
        community = communities[j]
        if community not in visited:
            visited[community] = i
            i += 1
        networks[visited[community]].append(graph_label[j])

    for network in networks:
        print("Community ", network, ": ", networks[network], sep='')

    print("Fitness:", chromosome.fitness)


def draw_communities(graph, chromosome):
    if isinstance(chromosome, Chromosome):
        communities = chromosome.representation
    elif isinstance(chromosome, ChromosomeAdj):
        communities = adj_to_communities(chromosome.representation)

    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(graph, pos, node_size=100, cmap=plt.cm.RdYlBu, node_color=communities)
    nx.draw_networkx_edges(graph, pos, alpha=0.3)
    plt.show()

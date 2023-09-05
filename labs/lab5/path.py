import random
from collections import defaultdict

from ant import Ant


def calculate_path_length(g, path):
    dist = g.edges[path[-1], path[0]]['weight']
    for i in range(len(path) - 1):
        dist += g.edges[path[i], path[i+1]]['weight']
    return dist


def get_ant(g, start, alpha, beta):
    ant = Ant(get_path(g, start, alpha, beta))
    ant.length = calculate_path_length(g, ant.path)
    return ant


def get_path(g, start, alpha, beta):
    visited = defaultdict(bool)
    visited[start] = True
    path = [start]
    while len(path) < len(g.nodes):
        # participants are edges adjacent to last node added to path
        participants = [edge for edge in g.edges(path[-1]) if not visited[edge[1]]]
        next_node = roulette_selection(g, participants, alpha, beta)
        visited[next_node] = True
        path.append(next_node)
    return path


def roulette_selection(g, participants, alpha, beta):
    probabilities = [pow(g.edges[edge]['pheromone'], alpha) * pow(1 / g.edges[edge]['weight'], beta)
                     for edge in participants]
    probs_sum = sum(probabilities)
    probabilities_percent = [p / probs_sum for p in probabilities]
    probs = [sum(probabilities_percent[:i+1]) for i in range(len(probabilities_percent))]

    r = random.random()
    for (i, edge) in enumerate(participants):
        if r <= probs[i]:
            return edge[1]


def update_pheromone(g, ants, rho, q):
    for edge in g.edges:
        g.edges[edge]['pheromone'] *= 1 - rho
    for ant in ants:
        for i in range(len(ant.path)):
            node, prev_node = ant.path[i], ant.path[i-1]
            g.edges[prev_node, node]['pheromone'] += q / ant.length

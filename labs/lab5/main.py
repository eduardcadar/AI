import random
import time

import file_utils
import path


def solve(g, params):
    random.seed(time.time())
    node_label = []
    i = 0
    for node in g.nodes:
        g.nodes[node]['id'] = 0
        node_label.append(node)
        i += 1
    start = node_label[0]
    min_weight, max_weight = 10000000, 0
    for edge in graph.edges:
        graph.edges[edge]['pheromone'] = params['initial_pheromone']
        if graph.edges[edge]['weight'] < min_weight:
            min_weight = graph.edges[edge]['weight']
        if graph.edges[edge]['weight'] > max_weight:
            max_weight = graph.edges[edge]['weight']
    # best_ant = path.get_ant(g, start, params['pheromone_weight'], params['visibility_weight'])
    ants = []
    print("START")
    for iteration in range(params['no_iterations']):

        if random.random() < params['dynamic_rate']:
            edge_to_change = random.sample(list(graph.edges), 1)[0]
            new_weight = round(random.uniform(min_weight, max_weight), 2)
            graph.edges[edge_to_change]['weight'] = new_weight

        ants = []
        for i in range(params['population_size']):
            ants.append(path.get_ant(g, start, params['pheromone_weight'], params['visibility_weight']))
        # for ant in ants:
        #     if ant.is_fitter_than(best_ant):
        #         best_ant = ant
        path.update_pheromone(g, ants, params['evaporation_rate'], params['ant_pheromone'])

        if iteration % 10 == 0:
            print("it", iteration, "len", min(ants, key=lambda a: a.length))

    print("final", min(ants, key=lambda a: a.length))


if __name__ == '__main__':
    pb_params = {
        'no_iterations': 100,
        'population_size': 4,
        'initial_pheromone': 10 ** -6,  # tau
        'evaporation_rate': 0.5,  # rho
        'pheromone_weight': 1,  # alpha - the importance of the pheromone on the edge in choosing the next city
        'visibility_weight': 5,  # beta - the importance of the length of the edge in choosing the next city
        'ant_pheromone': 1,
        'dynamic_rate': 0.5
            }

    file = "graphs/dj38.tsp"

    graph = file_utils.tspToNxGraph(file)

    solve(graph, pb_params)

"""
wi29.tsp - 27603
dj38.tsp - 6656
xqf131.tsp - 564
qa194.tsp - 9352

uy734.tsp - 79114
zi929.tsp - 95345
lu980.tsp - 11340
"""
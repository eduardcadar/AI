# Press Shift+F10 to execute it or replace it with your code.
import operator
import os.path
import time
from collections import defaultdict

from graphUtils import GraphUtils
from readGraphs import ReadGraphs
from utils import Utils


def greedyCommunitiesDetection(neighbours_dict, vertices_list, nr_of_edges_here, expected_nr_of_communities):
    networks_here = GraphUtils.get_networks(neighbours_dict, vertices_list)

    while len(networks_here) < expected_nr_of_communities and not Utils.dict_is_empty(neighbours_dict):
        edge_betweenness = defaultdict(float)
        for node in neighbours_dict.keys():
            nr_of_shortest_paths, node_level = GraphUtils.bfs(neighbours_dict, node)

            # nr_of_shortest_paths = GraphUtils.get_nr_of_shortest_paths(adj_matrix, levels)

            current_edge_betweenness = \
                GraphUtils.get_edge_betweenness_dict(neighbours_dict, node_level, nr_of_shortest_paths)

            for edge, value in current_edge_betweenness.items():
                edge_betweenness[edge] += value / 2

        # we sort the edges by their betweenness, we choose the ones with the biggest betweenness
        # [0] to get the key (the edge), [1] to get the betweenness
        edges = sorted(edge_betweenness.items(), reverse=True, key=operator.itemgetter(1))
        max_betweenness = edges[0][1]
        edges_to_remove = list(filter(lambda x: (x[1] == max_betweenness), edges))

        # we make a list from the frozen set; on [0] and [1] we will have the two vertices of the edge
        for edge in edges_to_remove:
            edge_vertices = list(edge[0])
            v1, v2 = edge_vertices[0], edge_vertices[1]
            neighbours_dict[v1].remove(v2), neighbours_dict[v2].remove(v1)
        nr_of_edges_here -= len(edges_to_remove)
        networks_here = GraphUtils.get_networks(neighbours_dict, vertices_list)

    return networks_here


if __name__ == '__main__':
    inputFile1 = "graphs/karate.gml"
    inputFile2 = "graphs/football.gml"
    inputFile3 = "graphs/dolphins.gml"
    inputFile4 = "graphs/krebs.gml"
    inputFile5 = "graphs/adjnoun.gml"
    inputFile6 = "graphs/news_2cl1_01.gml"
    inputFile7 = "graphs/lesmis.gml"
    inputFile8 = "graphs/myGraph.gml"
    inputFile9 = "graphs/celegansneural.gml"
    inputFile10 = "graphs/jazz.gml"

    # tests = [(inputFile1, 2), (inputFile2, 12), (inputFile3, 2), (inputFile4, 3), (inputFile5, 69),
    #          (inputFile6, 2), (inputFile7, 7), (inputFile8, 4), (inputFile9, 6), (inputFile10, 2)]

    tests = [(inputFile3, 2)]

    dirname = os.path.dirname(__file__)

    for test in tests:
        file, nr_of_communities = test[0], test[1]
        print(test)
        inAbsPath = os.path.join(dirname, file)
        neighbours, vertices, nr_of_edges = ReadGraphs.read_gml(inAbsPath)
        print(len(vertices), "vertices, ", nr_of_edges, "edges")
        start = time.time()
        networks = greedyCommunitiesDetection(neighbours, vertices, nr_of_edges, nr_of_communities)
        end = time.time()
        for network in networks:
            print("network ", network, ": ", sorted(networks[network]), sep="")
        print("time:", end - start)
        print()

    # outputFile = "graphs/ans.txt"
    # outAbsPath = os.path.join(dirname, outputFile)
    # fout = open(outAbsPath, "w")
    # for network in networks:
    #     for vertex in sorted(networks[network]):
    #         fout.write(str(vertex) + " ")
    #     fout.write("\n")
    # fout.close()

"""
1. karate - 2 communities
2. football - 12 communities
3. dolphins - 2 communities
4. krebs - 3 communities

5. adjnoun - 69 communities
6. news_2cl1_0.1 - 2 communities
7. lesmis - 7 communities
8. myGraph - 4 communities
9. celegansneural - 6 communities
10. jazz - 2 communities?
"""

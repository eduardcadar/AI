from collections import defaultdict

import networkx as nx


class ReadGraphs:
    @staticmethod
    def read_neighbour_list(abs_path):
        edge_list = []
        fin = open(abs_path, "r")
        for line in fin:
            if line.strip() == "":
                continue
            line = line.split()
            v1 = line[0]
            for v2 in line[1:]:
                edge_list.append((v1, v2))
        fin.close()
        for edge in edge_list:
            print(edge[0], edge[1])
        graph = nx.Graph(edge_list)
        nx.write_gml(graph, abs_path + "gml")

    @staticmethod
    def read_edge_list2(abs_path):
        edge_list = []
        fin = open(abs_path, "r")
        for line in fin:
            if line.strip() == "":
                continue
            line = line.split()
            v1 = line[0]
            v2 = line[1]
            edge_list.append((v1, v2))
        fin.close()
        for edge in edge_list:
            print(edge[0], edge[1])
        graph = nx.Graph(edge_list)
        nx.write_gml(graph, abs_path + "gml")

    @staticmethod
    def read_edge_list(abs_path):
        graph = nx.read_edgelist(abs_path, create_using=nx.DiGraph(), nodetype=int)
        nx.write_gml(graph, abs_path)

    @staticmethod
    def write_gml(abs_path):
        graph = nx.Graph([(1, 2), (1, 3), (1, 4), (2, 3), (4, 5), (4, 6),
                          (4, 7), (5, 6), (6, 7), (6, 8), (7, 9), (8, 9),
                          (8, 11), (9, 10), (10, 11), (11, 12), (12, 13), (12, 14), (13, 14)])
        nx.write_gml(graph, abs_path)

    @staticmethod
    def read_txt(abs_path):
        neighbours_dict = defaultdict(list)
        fin = open(abs_path, "r")
        nr_of_edges_here = 0

        for line in fin:
            if line.strip() == "":
                continue
            nr_of_edges_here += 1
            v1, v2 = line.split()
            if v1 == v2:
                continue
            neighbours_dict[int(v1)].append(int(v2))
            neighbours_dict[int(v2)].append(int(v1))
        return neighbours_dict

    @staticmethod
    def read_gml(abs_path):
        neighbours_dict = defaultdict(list)

        my_gml = nx.read_gml(abs_path)
        vertices = my_gml.nodes
        for edge in my_gml.edges:
            v1, v2 = edge[0], edge[1]
            neighbours_dict[v1].append(v2)
            neighbours_dict[v2].append(v1)

        return neighbours_dict, vertices, len(my_gml.edges)

from collections import defaultdict


class GraphUtils:
    @staticmethod
    def bfs(neighbours_dict, source):
        # O(n+m)
        nr_of_shortest_paths = defaultdict(int)
        nr_of_shortest_paths[source] = 1
        queue = [source]
        # source is on level 0
        node_level = {source: 0}
        nr_of_shortest_paths[source] = 1
        while queue:
            node = queue.pop(0)

            for neighbour in neighbours_dict[node]:
                if neighbour not in node_level:
                    # level of neighbour is level of node + 1
                    node_level[neighbour] = node_level[node] + 1
                    nr_of_shortest_paths[neighbour] += nr_of_shortest_paths[node]
                    queue.append(neighbour)
                elif node_level[neighbour] == node_level[node] + 1:
                    nr_of_shortest_paths[neighbour] += nr_of_shortest_paths[node]

        return nr_of_shortest_paths, node_level

    @staticmethod
    def getAdjacencyMatrix(neighbours_dict: dict, vertices):
        adj_matrix = defaultdict(defaultdict)
        for node in vertices:
            adj_matrix[node] = defaultdict(bool)

        for node in neighbours_dict.keys():
            for neighbour in neighbours_dict[node]:
                adj_matrix[node][neighbour] = True
                adj_matrix[neighbour][node] = True

        return adj_matrix

    @staticmethod
    def get_nr_of_shortest_paths(adj_matrix, levels_dict: dict):
        # O(n^2)
        nr_of_shortest_paths = defaultdict(int)
        # source node
        for node in levels_dict[0]:
            nr_of_shortest_paths[node] = 1
        # neighbours of source node
        for node in levels_dict[1]:
            nr_of_shortest_paths[node] = 1
        previous_level = 0
        # starting from level 2 nodes
        for node_list in list(levels_dict.values())[2:]:
            previous_level += 1
            for node in node_list:
                nr_of_shortest_paths[node] = 0
                for previous_node in levels_dict[previous_level]:
                    if adj_matrix[previous_node][node]:
                        nr_of_shortest_paths[node] += nr_of_shortest_paths[previous_node]

        return nr_of_shortest_paths

    @staticmethod
    def get_networks(neighbours_dict: dict, vertices):
        # O(n+m)
        network_here = defaultdict(list)
        current_network = 0
        visited = {}
        for node in vertices:
            if node not in visited:
                current_network += 1
                network_here[current_network].append(node)
                visited[node] = True
                queue = [node]
                while queue:
                    node = queue.pop(0)
                    for neighbour in neighbours_dict[node]:
                        if neighbour not in visited:
                            network_here[current_network].append(neighbour)
                            queue.append(neighbour)
                            visited[neighbour] = True
        return network_here

    @staticmethod
    def get_edge_betweenness_dict(neighbours_dict: dict, node_level: dict, nr_of_shortest_paths):
        # O(n+m)
        edge_betweenness_dict = defaultdict(float)
        # initially the nodes have a value of 0.0
        vertex_value = defaultdict(float)

        # we start from the last level
        for pair in sorted(node_level.items(), reverse=True, key=lambda item: item[1]):
            node = pair[0]
            vertex_value[node] += 1
            for neighbour in neighbours_dict[node]:
                if node_level[neighbour] == node_level[node] - 1:
                    edge_betweenness_dict[frozenset((node, neighbour))] = \
                        (nr_of_shortest_paths[neighbour] / nr_of_shortest_paths[node]) * vertex_value[node]
                    vertex_value[neighbour] += edge_betweenness_dict[frozenset((node, neighbour))]

        return edge_betweenness_dict

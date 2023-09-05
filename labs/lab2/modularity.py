from copy import copy


class Modularity:
    groups = []

    @staticmethod
    def calculate_two_vertices(neighbours_dict: dict, i, j, nr_of_edges):
        if i in neighbours_dict[j]:
            a = 1
        else:
            a = 0
        ki = len(neighbours_dict[i])
        kj = len(neighbours_dict[j])
        return a - ((ki * kj) / (2 * nr_of_edges))

    @staticmethod
    def increment_group(group: list):
        group[-1] += 1
        for i in range(len(group) - 1, -1, -1):
            if group[i] == 2:
                group[i] = 0
                group[i-1] += 1
        return group

    @staticmethod
    def get_groups(nr_of_vertices):
        if not Modularity.groups:
            group = nr_of_vertices * [0]
            groups2 = [copy(group)]
            while not group == nr_of_vertices * [1]:
                group = Modularity.increment_group(group)
                groups2.append(copy(group))
            Modularity.groups = groups2
        return Modularity.groups

    @staticmethod
    def calculate_modularity(neighbours_dict, nr_of_edges, nr_of_vertices):
        total_sum = 0
        sum_list = []
        for group in Modularity.get_groups(nr_of_vertices):
            mod_sum = 0
            for i in range(0, nr_of_vertices - 1):
                for j in range(i + 1, nr_of_vertices):
                    if group[i] == group[j]:
                        mod_sum += Modularity.calculate_two_vertices(neighbours_dict, i+1, j+1, nr_of_edges)
            total_sum += mod_sum
            sum_list += [mod_sum / (2 * nr_of_edges)]
        return sum_list
        # return total_sum / (2 * nr_of_edges)

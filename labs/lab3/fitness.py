import collections
import random
import statistics


def modularity(graph, communities):
    no_edges = len(graph.edges)
    m = 2 * no_edges
    q = 0.0
    for i in graph.nodes:
        for j in graph.nodes:
            if communities[graph.nodes[i]['id']] == communities[graph.nodes[j]['id']]:
                if graph.has_edge(i, j):
                    q += 1 - ((graph.degree[i] * graph.degree[j]) / m)
                else:
                    q -= (graph.degree[i] * graph.degree[j]) / m
    return q / m


def community_variance(graph, communities, node_label):
    diff_community = 0
    for neighbour in graph.neighbors(node_label):
        if communities[graph.nodes[node_label]['id']] != communities[graph.nodes[neighbour]['id']]:
            diff_community += 1
    return diff_community / graph.degree[node_label]


def reallocate(graph, communities, node):
    neighbours_communities = []
    for neighbour in graph.neighbors(node):
        neighbours_communities.append(communities[graph.nodes[neighbour]['id']])
    most_common_community = statistics.mode(neighbours_communities)
    communities[graph.nodes[node]['id']] = most_common_community
    for neighbour in graph.neighbors(node):
        communities[graph.nodes[neighbour]['id']] = most_common_community


def clean_up(graph, communities, variance_threshold, no_nodes_to_check):
    nodes = random.choices(list(graph.nodes), k=no_nodes_to_check)
    for node in nodes:
        if community_variance(graph, communities, node) > variance_threshold:
            reallocate(graph, communities, node)


def modularity_density(graph, communities, lmbd=0.5):
    kint, kout = collections.defaultdict(int), collections.defaultdict(int)
    for edge in graph.edges:
        i = graph.nodes[edge[0]]['id']
        j = graph.nodes[edge[1]]['id']
        if communities[i] == communities[j]:
            kint[i] += 1
            kint[j] += 1
        else:
            kout[i] += 1
            kout[j] += 1
    answer = 0.0
    comm_sum = collections.defaultdict(float)
    counter = collections.Counter(communities)
    for node in graph.nodes:
        i = graph.nodes[node]['id']
        comm_sum[communities[i]] += 2 * lmbd * kint[i] - 2 * (1 - lmbd) * kout[i]

    for community in counter:
        answer += comm_sum[community] / counter[community]
    return answer / len(graph.nodes)


def community_score(graph, communities, alpha=0.3):
    kint = collections.defaultdict(int)
    for edge in graph.edges:
        i = graph.nodes[edge[0]]['id']
        j = graph.nodes[edge[1]]['id']
        if communities[i] == communities[j]:
            kint[i] += 1
            kint[j] += 1

    counter = collections.Counter(communities)
    answer = 0.0
    comm_sum = collections.defaultdict(float)
    comm_int = collections.defaultdict(int)
    for node in graph.nodes:
        i = graph.nodes[node]['id']
        comm_sum[communities[i]] += pow(kint[i] / counter[communities[i]], alpha)
        comm_int[communities[i]] += kint[i]

    for community in counter:
        answer += (comm_sum[community] * comm_int[community]) / counter[community]

    return answer

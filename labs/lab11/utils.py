from math import sqrt


def euclidean_distance(p1, p2):
    dist = 0.0
    for i, value in enumerate(p1):
        dist += (p2[i] - value) ** 2
    dist = sqrt(dist)
    return dist


def center(points):
    size = len(points)
    c = [sum([p[i] for p in points]) / size for i in range(len(points[0]))]
    return c

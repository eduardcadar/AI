import utils


class MyUnsupervisedClassifier:
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters
        self.centroids = []
        self.prev_centroids = []

    def fit(self, inputs, max_iterations):
        # initialize centroids
        self.centroids, self.prev_centroids = [], []
        cl_size = len(inputs) // self.n_clusters
        for i in range(self.n_clusters):
            self.centroids.append(utils.center(inputs[i * cl_size:(i+1)*cl_size]))

        clusters = {}
        for i in range(len(self.centroids)):
            clusters[i] = []

        print('it:', end=' ')
        # cluster the inputs
        for it in range(max_iterations):
            if not it % 2:
                print(it, end=' ')
            for i in range(len(self.centroids)):
                clusters[i] = []
            for inp in inputs:
                j = self.closest_cluster_index(inp)
                clusters[j].append(inp)
            self.prev_centroids = self.centroids
            self.centroids = [utils.center(c) if len(c) > 0 else self.prev_centroids[i] for i, c in enumerate(clusters.values())]
            if self.prev_centroids == self.centroids:
                print('no change', end='')
                break
        print()

    def closest_cluster_index(self, point):
        dists = [utils.euclidean_distance(point, c) for c in self.centroids]
        j = dists.index(min(dists))
        return j

    def predict(self, inputs):
        outputs = []
        for inp in inputs:
            j = self.closest_cluster_index(inp)
            outputs.append(j)
        return outputs

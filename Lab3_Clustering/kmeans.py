import numpy as np
from scipy.spatial.distance import sqeuclidean
import pandas

import sys


class IslamKMeans:
    def __init__(self, k=5, init='k-means++', n_init=10,
                 max_iter=300, tol=0.0001):
        """
        Initialization of K-Means algorithm
        :param k: number of clusters
        :param init: method for initialization k-means++ or random
        :param n_init: number of time the k-means algorithm will be run
                       with different centroid seeds
        :param max_iter: Maximum number of iterations of
                         the k-means algorithm for a single run
        :param tol: relative tolerance
        """
        self.k = k
        self.init = init
        self.n_init = n_init
        self.max_iter = max_iter
        self.tol = tol

        self.X = ''
        self.inertia_ = float(sys.maxsize)
        self.cluster_centers_ = list()
        self.labels_ = ''
        self.clusters = [[] for _ in range(self.k)]
        self.n_samples = int
        self.n_features = int

    def k_means_plus(self):
        """
        Selects initial cluster centers for
        k-mean clustering in a smart way to speed up convergence
        :return: None
        """
        centroids_buf = list()
        random_sample_id = np.random.choice(self.n_samples, 1,
                                            replace=False)
        centroids_buf.append(self.X[random_sample_id])
        for id in range(self.k - 1):
            dist = []
            for i in range(self.n_samples):
                point = self.X[i, :]
                d = sys.maxsize
                for j in range(len(centroids_buf)):
                    temp_dist = sqeuclidean(point, centroids_buf[j])
                    d = min(d, temp_dist)
                dist.append(d)
            dist = np.array(dist)
            next_centroid = self.X[np.argmax(dist), :]
            centroids_buf.append(next_centroid)
        self.cluster_centers_ = list(centroids_buf)

    def random_find(self):
        """
        Choose n_clusters observations (rows) at random
        from data for the initial centroids
        :return: None
        """
        random_sample_idxs = np.random.choice(self.n_samples,
                                              self.k,
                                              replace=False)
        self.cluster_centers_ = [self.X[idx] for idx in random_sample_idxs]

    def fit(self, data):
        """
        Compute k-means clustering.
        :param data: algorithm training data
        :return: None
        """
        best_labels = self.labels_
        best_inertia = float(sys.maxsize)
        best_centroids = self.cluster_centers_
        self.X = data
        self.n_samples, self.n_features = data.shape
        for _ in range(self.n_init):
            if self.init == 'k-means++':
                self.k_means_plus()
            else:
                self.random_find()
            for _ in range(self.max_iter):
                self.clusters = self.add_to_cluster(self.cluster_centers_)
                self.cluster_centers_ = self.get_centres(self.clusters)
                if self.check_inertia() is True:
                    break
            if self.inertia_ < best_inertia:
                self.get_labels(clusters=self.clusters)
                best_labels = self.labels_.copy()
                best_centroids = self.cluster_centers_.copy()
                best_inertia = self.inertia_
        self.labels_ = best_labels.copy()
        self.cluster_centers_ = best_centroids.copy()
        self.inertia_ = best_inertia

    def predict(self, data):
        """
        Predict the closest cluster each sample in X belongs to.
        :param data: algorithm prediction data
        :return: list of the labels
        """
        self.X = data
        self.n_samples, self.n_features = data.shape
        other_clusters = self.create_clusters(self.cluster_centers_)
        return self.get_labels(other_clusters)

    def get_labels(self, clusters):
        """
        Turns the list of clusters into an easy-to-process list
        :param clusters: list of clusters
        :return: None
        """
        self.labels_ = np.empty(self.n_samples, dtype=int)
        for cluster_idx, cluster in enumerate(clusters):
            for sample_index in cluster:
                self.labels_[sample_index] = cluster_idx

    def add_to_cluster(self, centroids):
        """
        Creates and adds points to specific clusters
        :param centroids: list of centroids
        :return: list of clusters
        """
        clusters = list()
        for _ in range(self.k):
            clusters.append([])
        for idx, sample in enumerate(self.X):
            centroid_idx = self.nearest_centroid(sample, centroids)
            clusters[centroid_idx].append(idx)
        return clusters

    @staticmethod
    def nearest_centroid(element, centroids):
        """
        Find the nearest centroid
        :param element: a definite point in our data
        :param centroids: list of centroids
        :return: numpy array with the nearest centroid
        """
        distances = list()
        for val in centroids:
            cur_dist = sqeuclidean(element, val)
            distances.append(cur_dist)
        index = np.argmin(distances)
        return index

    def get_centres(self, clusters):
        """
        Initialize centres for clusters
        :param clusters: list of clusters
        :return: array of centroids
        """
        centroids = np.zeros((self.k, self.n_features))
        for cluster_idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(self.X[cluster], axis=0)
            centroids[cluster_idx] = cluster_mean
        return centroids

    def check_inertia(self):
        """
        Finds inertia and determines when
        the algorithm needs to end the action
        :return: bool
        """
        distance = 0
        for i in range(len(self.clusters)):
            for j in range(len(self.clusters[i])):
                point = self.X[self.clusters[i][j]]
                distance += sqeuclidean(point, self.cluster_centers_[i])
        if abs(distance - self.inertia_) < self.tol:
            return True
        else:
            self.inertia_ = distance
            return False
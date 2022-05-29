import numpy as np
from collections import Counter


def euclidean_dist(x1, x2):
    return np.sqrt(np.sum(x1 - x2) ** 2)


class KNN:

    def __init__(self, k=3, dist='Euclidean'):
        self.X_train = None
        self.y_train = None
        self.k = k
        self.dist = dist

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        PredLabel = [self._predict(x) for x in X]
        return np.array(PredLabel)

    def _predict(self, x):
        if self.dist == 'Euclidean':
            distances = [euclidean_dist(x, x_train) for x_train in self.X_train]
            k_ind = np.argsort(distances)[:self.k]
            k_labels = [self.y_train[i] for i in k_ind]
            most_common = Counter(k_labels).most_common(1)
            return most_common[0][0]

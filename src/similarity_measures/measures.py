from __future__ import division

import numpy as np


def cosine_similarity(vector_a, vector_b):
    """ Cosine similarity between two unit vectors. """
    return vector_a.dot(vector_b.T)


def euclidean_similarity(vector_a, vector_b):
    """ Euclidean distance (similarity). """
    return np.linalg.norm(vector_a - vector_b)


def chisq_similarity(vector_a, vector_b, eps=1e-10):
    """ Chi-Squared distance. """
    return 0.5 * np.sum((vector_a - vector_b)**2 / (vector_a + vector_b + eps))


def kl_similarity(vector_a, vector_b):
    """ K-L Divergence distance. """
    mask = np.logical_and(vector_a != 0, vector_b != 0)
    return np.sum(vector_a[mask] * np.log2(vector_a[mask] / vector_b[mask]))

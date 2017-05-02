from __future__ import division

import numpy as np


def cosine_similarity(vector_a, vector_b):
    """ Cosine similarity between two unit vectors. """
    return vector_a.dot(vector_b.T)


def euclidean_similarity(vector_a, vector_b):
    """ Euclidean distance (similarity). """
    return np.linalg.norm(vector_a - vector_b)


def chisq_similarity(vector_a, vector_b, eps=1e-10):
    """ Chi-Squared distance between two histograms (distributions). """
    return 0.5 * np.sum((vector_a - vector_b)**2 / (vector_a + vector_b + eps))


def kl_similarity(vector_a, vector_b):
    """ K-L Divergence distance betwen two histograms (distributions). """
    mask = np.logical_and(vector_a != 0, vector_b != 0)
    return np.sum(vector_a[mask] * np.log2(vector_a[mask] / vector_b[mask]))


def bhattacharyya_similarity(vector_a, vector_b):
    """ Bhattacharyya similarity (distributions). """
    return - np.log(np.sum(np.sqrt(vector_a * vector_b)))


def intersection_similarity(vector_a, vector_b):
    """ Intersections of two histograms (distributions). """
    return np.sum(np.minimum(vector_a, vector_b)) / np.minimum(vector_a.sum(), vector_b.sum())


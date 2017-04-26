from __future__ import division

import numpy as np


def cosine_similarity(vector_a, vector_b):
    """ Cosine similarity between two unit vectors. """
    return vector_a.dot(vector_b.T)


def euclidean_similarity(vector_a, vector_b):
    """ Euclidean distance (similarity). """
    return np.linalg.norm(vector_a - vector_b)

from __future__ import absolute_import

import os
import numpy as np
import cPickle as pickle


from src.indexes.base_index import BaseIndex
from src.similarity_measures.measures import *


class MemoryIndex(BaseIndex):
    """
    Naive implementation of in memory index, only for simple and fast test cases.
    The class does not generate unique document IDs.
    """

    def __init__(self, index_path=None):
        """
        Initialize MemoryIndex

        :param index_field:
        :param index_path:
        """
        self._index_path = index_path
        self._index = self._initialize_index()
        # similarities= (function_pointer, flag_whether_reverse_sorting)
        self._similarities = {
            'euclidean': (euclidean_similarity, False),
            'cosine': (cosine_similarity, True),
            'intersection': (intersection_similarity, True),
            'kl': (kl_similarity, False),
            'chi2': (chisq_similarity, False),
            'bhattacharyya': (bhattacharyya_similarity, False)
        }

    def _initialize_index(self):
        if self._index_path is not None and os.path.isfile(self._index_path):
            with open(self._index_path) as fd:
                return pickle.load(fd)
        else:
            return []

    def insert_document(self, document_dict):
        self._index.append(document_dict)
        return 0

    def query_index(self, query_dict, similarity, extractor, return_score=False):
        # get appropriate similarity measure
        similarity_fn, reverse_order = self._similarities[similarity]

        # get query features
        query_features = query_dict['features']

        # compare and rank indexed images
        results = [(indexed_dict['doc_name'], similarity_fn(np.array(indexed_dict[extractor]), np.array(query_features))) for indexed_dict in self._index]
        results_sorted = sorted(results, reverse=reverse_order, key=lambda x: x[1])

        if return_score:
            return results_sorted
        else:
            return [result[0] for result in results_sorted]

    def persist_index(self):
        if self._index_path is not None:
            with open(self._index_path, 'wb') as fd:
                pickle.dump(self._index, fd, protocol=2)


if __name__ == '__main__':

    mem_index = MemoryIndex('')
    doc_1 = {'doc_name': '1', 'cnn_basic': [1, 2, 3, 4]}
    doc_2 = {'doc_name': '2', 'cnn_basic': [1, 2, 3, 3]}
    doc_3 = {'doc_name': '3', 'cnn_basic': [4, 5, 6, 7]}
    doc_4 = {'doc_name': '4', 'cnn_basic': [7, 8, 9, 0]}
    doc_test = {'doc_name': '5', 'features': [7, 8, 9, 2]}

    mem_index.insert_document(doc_1)
    mem_index.insert_document(doc_2)
    mem_index.insert_document(doc_3)
    mem_index.insert_document(doc_4)

    print mem_index.query_index(doc_test, 'euclidean', 'cnn_basic')




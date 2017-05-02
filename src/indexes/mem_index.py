from __future__ import absolute_import

import os
import numpy as np
import cPickle as pickle

from src.indexes.base_index import BaseIndex
from src.similarity_measures.measures import euclidean_similarity


class MemoryIndex(BaseIndex):
    """
    Naive implementation of in memory index, only for simple and fast test cases.
    It assumes that the files are index by one field that is an array of floats.
    To retrieve documents in uses cosine similarity.
    The class does not generate unique document IDs.
    """

    def __init__(self, index_field, index_path=None):
        """
        Initialize MemoryIndex

        :param index_field:
        :param index_path:
        """
        self._index_field = index_field
        self._index_path = index_path
        self._index = self._initialize_index()

    def _initialize_index(self):
        if self._index_path is not None and os.path.isfile(self._index_path):
            with open(self._index_path) as fd:
                return pickle.load(fd)
        else:
            return {}

    def insert_document(self, document_dict):
        doc_key = tuple(document_dict[self._index_field])
        self._index[doc_key] = document_dict
        return 0

    def query_index(self, query_dict, query_fields):
        query_key = np.array(query_dict[self._index_field])
        results = sorted(self._index.iteritems(), key=lambda (k, v): euclidean_similarity(np.array(k), query_key))
        return [result[1] for result in results]

    def persist_index(self):
        if self._index_path is not None:
            with open(self._index_path, 'wb') as fd:
                pickle.dump(self._index, fd)


if __name__ == '__main__':

    mem_index = MemoryIndex('features')
    doc_1 = {'doc_name': '1', 'features': [1, 2, 3, 4]}
    doc_2 = {'doc_name': '2', 'features': [1, 2, 3, 3]}
    doc_3 = {'doc_name': '3', 'features': [4, 5, 6, 7]}
    doc_4 = {'doc_name': '4', 'features': [7, 8, 9, 0]}
    doc_test = {'doc_name': '5', 'features': [7, 8, 9, 2]}

    mem_index.insert_document(doc_1)
    mem_index.insert_document(doc_2)
    mem_index.insert_document(doc_3)
    mem_index.insert_document(doc_4)

    print mem_index.query_index(doc_test, '')




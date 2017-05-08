from __future__ import absolute_import

import os
import datetime
import numpy as np
import cPickle as pickle

from src.indexes.base_index import BaseIndex
from src.similarity_measures.measures import euclidean_similarity


class FileIndex(BaseIndex):
    """
    This is NOT a real index. This class collects the parsed images in a list and
    saves them to disk as a cPickle file when `persist_index` is called.

    USE ONLY TO PERSIST PARSED IMAGES TO FILE
    """

    def __init__(self, index_field, index_path=None):
        """
        Initialize MemoryIndex

        :param index_field:
        :param index_path:
        """
        self._parsed_images = []
        self._file_basename = 'parsed_images'

    def insert_document(self, document_dict):
        self._parsed_images.append(document_dict)
        return 0

    def query_index(self, query_dict, query_fields):
        return

    def persist_index(self):
        suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
        filename = '_'.join([self._file_basename, suffix]) + '.p'

        with open(filename, 'wb') as fd:
            pickle.dump(self._parsed_images, fd)


if __name__ == '__main__':

    file_index = FileIndex('features')
    doc_1 = {'doc_name': '1', 'features': [1, 2, 3, 4]}
    doc_2 = {'doc_name': '2', 'features': [1, 2, 3, 3]}
    doc_3 = {'doc_name': '3', 'features': [4, 5, 6, 7]}
    doc_4 = {'doc_name': '4', 'features': [7, 8, 9, 0]}
    doc_test = {'doc_name': '5', 'features': [7, 8, 9, 2]}

    file_index.insert_document(doc_1)
    file_index.insert_document(doc_2)
    file_index.insert_document(doc_3)
    file_index.insert_document(doc_4)

    file_index.persist_index()

    print file_index.query_index(doc_test, '')




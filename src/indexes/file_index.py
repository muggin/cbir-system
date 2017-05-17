from __future__ import absolute_import

import datetime
import cPickle as pickle

from src.indexes.base_index import BaseIndex


class FileIndex(BaseIndex):
    """
    This is NOT a real index. This class collects the parsed images in a list and
    saves them to disk as a cPickle file when `persist_index` is called.

    USE ONLY TO PERSIST PARSED IMAGES TO FILE
    """

    def __init__(self, parsed_path):
        """
        Initialize MemoryIndex

        :param index_field:
        :param index_path:
        """
        self._parsed_images = []
        self._parsed_path = parsed_path

    def insert_document(self, document_dict):
        self._parsed_images.append(document_dict)
        return 0

    def query_index(self, query_dict, similarity, extractor):
        return

    def persist_index(self):
        with open(self._parsed_path, 'wb') as fd:
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




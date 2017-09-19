import abc


class BaseIndex(object):
    """
    Class that is a persistent index
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def insert_document(self, document_dict):
        """
        Method inserts document into persisted index.

        :param: document_dict - dictionary holding all fields that describe a document
        :return: generated document id
        """
        return

    @abc.abstractmethod
    def query_index(self, query_dict, similarity, extractor):
        """
        Method queries persisted index.

        :param: query_dict - dictionary holding features extracted from the query
        :param: similarity - name of similarity function to use for ranking
        :param: extractor - name of index to use for retrieval
        :return: documents retrieved from index that match query
        """
        return

    @abc.abstractmethod
    def persist_index(self):
        """
        Method makes all necessary steps to persist index

        :return: None
        """
        return


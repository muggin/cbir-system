import abc


class BaseParser(object):
    """
     Class that handles extracting all types of features from the images
     """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def prepare_query(self, query_image):
        """
        Prepares image to be used as query, extracts necessary features.

        :param: image that came as a query
        :return: dictionary holding image features (ready to be used as query)
        """
        return

    @abc.abstractmethod
    def prepare_document(self, image_name, image):
        """
        Prepares image to be stored in index, extracts necessary features.

        :param: name of prepared image
        :param: image to be stored in index
        :return: dictionary holding image information (ready to be stored in index)
        """
        return

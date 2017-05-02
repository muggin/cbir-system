from .base_parser import BaseParser
from src.feature_extractors.hist_ext import HistogramExtractor


class SimpleParser(BaseParser):
    """
    Class prepared documents for storage or query.
    This version of the parser uses only histogram features, it can be used for fast testing.

    Document template:
    {
        'doc_name': String,
        'features': Array[Float]
    }
    """
    def __init__(self):
        self._extractor = HistogramExtractor(nbins_per_ch=(12, 8, 3), use_hsv=True)

    def prepare_query(self, query_image):
        """
        Prepares image to be used as query, extracts necessary features.

        :param: image that came as a query
        :return: dictionary holding image features (ready to be used as query)
        """
        image_features = self._extractor.extract(query_image)
        return {'doc_name': None, 'features': image_features}

    def prepare_document(self, image_name, image):
        """
        Prepares image to be stored in index, extracts necessary features.

        :param: image to be stored in index
        :return: dictionary holding image information (ready to be stored in index)
        """
        image_features = self._extractor.extract(image)
        return {'doc_name': image_name, 'features': image_features}

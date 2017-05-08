from .base_parser import BaseParser
from src.feature_extractors.hist_ext import HistogramExtractor
from src.feature_extractors.cnn_ext import CNNExtractor


class V1ImageParser(BaseParser):
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
        self._hist_ext = HistogramExtractor(nbins_per_ch=(9, 3, 3), use_hsv=True, use_regions=True)
        self._cnn_ext = CNNExtractor(output_layers=['block1_pool', 'block2_pool', 'block3_pool',
                                                    'block4_pool', 'block5_pool', 'fc2'])

    def prepare_query(self, query_image):
        """
        Prepares image to be used as query, extracts necessary features.

        :param: image that came as a query
        :return: dictionary holding image features (ready to be used as query)
        """
        return {'doc_name': None, 'features': None}

    def prepare_document(self, image_name, image):
        """
        Prepares image to be stored in index, extracts necessary features.

        :param: image to be stored in index
        :return: dictionary holding image information (ready to be stored in index)
        """
        return {'doc_name': image_name, 'features': None}

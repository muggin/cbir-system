from __future__ import division

import numpy as np
from .base_parser import BaseParser
from src.feature_extractors.hist_ext import HistogramExtractor
from src.feature_extractors.cnn_ext import CNNExtractor


class V1ImageParser(BaseParser):
    """
    Class prepared documents for storage or query.
    This version will be used in the final report. It computes histograms, conv features, and
    a mix of conv features and histograms.

    Document template:
    {
        'doc_name': String,
        'cnn_basic': Array[Float]
        'hist_basic': Array[Float]
        'cnn_hist': Array[Float]
    }
    """

    def __init__(self):
        self._hist_ext = HistogramExtractor(nbins_per_ch=(9, 3, 3), use_hsv=True, use_regions=True)
        self._cnn_ext = CNNExtractor(output_layers=['block1_conv2', 'block2_conv2', 'block3_conv2',
                                                    'block4_conv2', 'block5_conv2', 'fc2'])

    def _extract_features(self, image):
        # extract features
        cnn_features = self._cnn_ext.extract(image)
        hist_features = self._hist_ext.extract(image)

        # split conv net feature layers
        cnn_convs = np.array(cnn_features[:-1])
        cnn_fc = np.array(cnn_features[-1])

        # compute intermediate feature map histograms
        cnn_hist = np.array([])
        for layer_ix in xrange(cnn_convs.shape[0]):
            feat_maps = cnn_convs[layer_ix]
            feat_maps_scaled = (feat_maps - feat_maps.min(axis=2, keepdims=True)) / (
                feat_maps.max(axis=2, keepdims=True) - feat_maps.min(axis=2, keepdims=True))
            feat_maps_scaled[np.isnan(feat_maps_scaled)] = 0.
            feat_maps_hist = np.array(
                [np.histogram(feat_maps_scaled[:, :, ch], bins=3, range=[0., 1.])[0] for ch in
                 range(feat_maps_scaled.shape[2])], dtype=np.float32)
            feat_maps_hist /= feat_maps_hist.sum(axis=1, keepdims=True)
            cnn_hist = np.hstack((cnn_hist, feat_maps_hist.reshape(-1)))

        # scale vectors
        hist_features /= np.sum(hist_features, keepdims=True)
        cnn_hist /= np.sum(cnn_hist, keepdims=True)
        cnn_fc /= np.linalg.norm(cnn_fc, keepdims=True)

        return {'cnn_basic': cnn_fc.tolist(), 'hist_basic': hist_features.tolist(),
                'cnn_hist': cnn_hist.tolist()}

    def prepare_query(self, query_image):
        """
        Prepares image to be used as query, extracts necessary features.

        :param: image that came as a query
        :return: dictionary holding image features (ready to be used as query)
        """
        return self._extract_features(query_image)

    def prepare_document(self, image_name, image):
        """
        Prepares image to be stored in index, extracts necessary features.

        :param: image to be stored in index
        :return: dictionary holding image information (ready to be stored in index)
        """
        extracted_features = self._extract_features(image)
        extracted_features['doc_name'] = image_name
        return extracted_features

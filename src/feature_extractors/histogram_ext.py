from src.feature_extractors.base_ext import BaseExtractor


class HistogramExtractor(BaseExtractor):
    """Class defines a Histogram based feature extractor."""

    def __init__(self, bins_per_channel=2):
        """

        :param bins_per_channel:
        """
        self._bins_per_channel = bins_per_channel

    def extract(self, image):
        """Extracts histogram features from the given image."""
        # TODO: Compute histogram representation of given image
        pass

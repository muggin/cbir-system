from src.feature_extractors.base_ext import BaseExtractor


class CNNExtractor(BaseExtractor):
    """Class defines a ConvNet based feature extractor."""

    def __init__(self):
        """

        """
        # TODO: Create VGG Keras model and load ImageNet weights
        pass

    def extract(self, image):
        """Extracts abstract features from the given image."""
        # TODO: Pass image through VGG model and return extracted features
        pass

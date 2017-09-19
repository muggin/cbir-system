import abc


class BaseExtractor(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def extract(self, image):
        """Extracts features from the given image using a specific class-dependent technique."""
        return

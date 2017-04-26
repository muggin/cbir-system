import numpy as np
import skimage.transform as sktrans

from src.feature_extractors.base_ext import BaseExtractor
from keras.applications.vgg16 import preprocess_input
from keras.applications import VGG16
from keras.models import Model


class CNNExtractor(BaseExtractor):
    """Class defines a ConvNet based feature extractor."""

    def __init__(self, input_size=(224, 224), output_layer='fc2', normalize=True):
        """Initialize CNN Feature Extractor."""
        self._input_shape = input_size
        self._output_layer = output_layer
        self._normalize = normalize
        self._model = self._initialize_model()

    def _initialize_model(self):
        """Initialize VGG16 net and remove appropriate layers from the top."""
        vgg = VGG16(include_top=True)
        feat_extractor = Model(inputs=vgg.input, outputs=vgg.get_layer(self._output_layer).output)
        return feat_extractor

    def extract(self, image):
        """Extracts abstract features from the given image."""
        # reshape input image if necessary
        if image.shape[:2] != self._input_shape:
            image = sktrans.resize(image, self._input_shape, preserve_range=True)

        # process input image (mean subtraction, etc.) and extract features
        image = np.expand_dims(image, axis=0)
        image_proc = preprocess_input(image)
        image_feats = self._model.predict(image_proc)

        # normalize feature values
        if self._normalize:
            image_feats /= np.linalg.norm(image_feats)

        return image_feats


if __name__ == '__main__':
    import os
    import argparse
    import matplotlib.pyplot as plt
    import skimage.io as io

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='Path to folder containing')
    ap.add_argument('-q', '--queries', required=True, help='Number of example queries')
    args = vars(ap.parse_args())
    data_path = args['dataset']
    query_num = args['queries']

    print 'Loading images...'
    for root, dirs, files in os.walk(data_path, topdown=True):
        imgs = np.array([io.imread(os.path.join(data_path, file_name)) for file_name in files])

    print 'Extracting features...'
    cnn_ext = CNNExtractor()
    preds = np.array([cnn_ext.extract(img, normalized=True)[0] for img in imgs])

    print 'Finding similar images...'
    for _ in xrange(query_num):
        query_idx = np.random.randint(imgs.shape[0])
        query_img = preds[query_idx]
        sims = np.array([query_img.dot(other.T) for other in preds])
        most_sim = np.argsort(sims)

        plt.subplot(1, 4, 1)
        plt.title('Query')
        plt.imshow(imgs[query_idx])
        plt.subplot(1, 4, 2)
        plt.title('Result #1 (Sim: %.2f)' % sims[most_sim[-2]])
        plt.imshow(imgs[most_sim[-2]])
        plt.subplot(1, 4, 3)
        plt.title('Result #2 (Sim: %.2f)' % sims[most_sim[-3]])
        plt.imshow(imgs[most_sim[-3]])
        plt.subplot(1, 4, 4)
        plt.title('Result #3 (Sim: %.2f)' % sims[most_sim[-4]])
        plt.imshow(imgs[most_sim[-4]])
        plt.show()
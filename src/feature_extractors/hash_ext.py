import utils
import numpy as np

from PIL import Image
from src.feature_extractors.base_ext import BaseExtractor


class HashExtractor(BaseExtractor):
    """Class defines a ConvNet based feature extractor."""

    def __init__(self, hash_method='ahash', **hash_args):
        """Initialize CNN Feature Extractor."""
        self._hash_args = hash_args
        self._hash_fn = utils.hashing_functions.get(hash_method, 'ahash')

    def extract(self, image):
        """Extracts abstract features from the given image."""
        return self._hash_fn(image, **self._hash_args)


if __name__ == '__main__':
    import os
    import argparse
    import matplotlib.pyplot as plt

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='Path to folder containing')
    ap.add_argument('-q', '--queries', required=True, help='Number of example queries')
    args = vars(ap.parse_args())
    data_path = args['dataset']
    query_num = args['queries']

    print 'Loading images...'
    for root, dirs, files in os.walk(data_path, topdown=True):
        imgs = [Image.open(os.path.join(data_path, file_name)) for file_name in files]

    print 'Extracting features...'
    hash_ext = HashExtractor(hash_method='ahash')
    preds = np.array([hash_ext.extract(img) for img in imgs])

    print 'Finding similar images...'
    for _ in xrange(int(query_num)):
        query_idx = np.random.randint(len(imgs))
        query_img = preds[query_idx]
        sims = np.array([query_img - other for other in preds])
        most_sim = np.argsort(sims)
        print query_img

        plt.subplot(1, 4, 1)
        plt.title('Query')
        plt.imshow(imgs[query_idx])
        plt.subplot(1, 4, 2)
        plt.title('Result #1 (Sim: %.2f)' % sims[most_sim[1]])
        plt.imshow(imgs[most_sim[-2]])
        plt.subplot(1, 4, 3)
        plt.title('Result #2 (Sim: %.2f)' % sims[most_sim[2]])
        plt.imshow(imgs[most_sim[-3]])
        plt.subplot(1, 4, 4)
        plt.title('Result #3 (Sim: %.2f)' % sims[most_sim[3]])
        plt.imshow(imgs[most_sim[4]])
        plt.show()
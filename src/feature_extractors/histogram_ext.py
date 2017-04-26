from __future__ import division

import numpy as np
import skimage.exposure as skexp

from skimage import img_as_float
from src.feature_extractors.base_ext import BaseExtractor


class HistogramExtractor(BaseExtractor):
    """Class defines a Histogram based feature extractor."""

    def __init__(self, bins_per_ch=16, use_regions=False, normalize=True):
        """
        :param bins_per_ch:
        """
        self._bins_per_ch = bins_per_ch
        self._use_regions = use_regions
        self._normalize = normalize

    def _extract_regions(self, image):
        region_coords = [
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ]

        # create eliptical mask in the center of the image
        # create corner masks
        # extract regions and return as list
        pass

    def extract(self, image):
        """Extracts histogram features from the given image."""
        # convert image to floats
        image_flt = img_as_float(image)

        # split image into regions if necessary
        image_regions = self._extract_regions(image_flt) if self._use_regions else [image_flt]

        # compute channel histograms for each region
        hists = np.array([skexp.histogram(image_flt[:, :, ch], nbins=self._bins_per_ch)[0]
                          for ch in xrange(image.shape[-1])])

        # normalize (per channel) and flatten histograms
        hists_norm_ch = hists / hists.sum(axis=1, keepdims=True)

        # flatten regions
        # TODO: flatten list of regions

        if self._normalize:
            hists_norm_ch /= np.linalg.norm(hists_norm_ch)

        return hists_norm_ch


if __name__ == '__main__':
    import os
    import argparse
    import matplotlib.pyplot as plt
    import skimage.io as io
    from src.similarity_measures.measures import euclidean_similarity, cosine_similarity

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='Path to folder containing')
    ap.add_argument('-q', '--queries', required=True, help='Number of example queries')
    args = vars(ap.parse_args())
    data_path = args['dataset']
    query_num = int(args['queries'])

    print 'Loading images...'
    for root, dirs, files in os.walk(data_path, topdown=True):
        imgs = np.array([io.imread(os.path.join(data_path, file_name)) for file_name in files])

    print 'Extracting features...'
    hist_ext = HistogramExtractor()
    preds = np.array([hist_ext.extract(img) for img in imgs])

    print 'Finding similar images...'
    for _ in xrange(query_num):
        query_idx = np.random.randint(imgs.shape[0])
        query_img = preds[query_idx]
        sims = np.array([euclidean_similarity(query_img, other) for other in preds])
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

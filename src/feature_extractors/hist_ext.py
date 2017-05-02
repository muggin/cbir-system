from __future__ import division

import numpy as np

from skimage import color, draw, img_as_float
from src.feature_extractors.base_ext import BaseExtractor


class HistogramExtractor(BaseExtractor):
    """ Class defines a 3D Histogram based feature extractor, optionally incorporating regions.

        The size of the output feature vector depends on the number of
        bins used per channel and whether the regions option is used.

        The size can be calculated using the formula:
        size(feature_vector) = bins_ch_1 * bins_ch_2 * bins_ch_3 * num_regions
    """

    def __init__(self, nbins_per_ch=(16,), use_hsv=False, use_regions=False, radius=0.6,
                 normalize=True):
        """
        Initialize Histogram extractor.

        :param nbins_per_ch: number of bins per channel (tuple)
        :param use_hsv: whether to convert image to HSV space (boolean)
        :param use_regions: whether image should be split into regions (boolean)
        :param radius: radius of central part of image (float: 0.0-1.0)
        :param normalize: whether feature vector should be normalized (boolean)
        """
        self._bins_per_ch = nbins_per_ch if len(nbins_per_ch) == 3 else 3 * nbins_per_ch
        self._use_regions = use_regions
        self._use_hsv = use_hsv
        self._radius = radius
        self._normalize = normalize

    def _preprocess_image(self, image):
        # convert image to floats
        image_flt = img_as_float(image)
        if self._use_hsv:
            image_flt = color.rgb2hsv(image_flt)

        return image_flt

    def _extract_regions(self, image):
        height, width = image.shape[:2]
        corners = [
            (0, height // 2, 0, width // 2),  # top left corner
            (height // 2, height, 0, width // 2),  # bottom left corner
            (height // 2, height, width // 2, width),  # bottom right corner
            (0, height // 2, width // 2, width)  # top right corner
        ]

        # cutout center region
        r, c = draw.ellipse(height // 2, width // 2, int(self._radius * height / 2),
                            int(self._radius * width / 2))
        center_mask = np.zeros(image.shape)
        center_mask[r, c, :] = 1
        regions = [image * center_mask]
        # cutout corner regions
        for (start_x, end_x, start_y, end_y) in corners:
            corner_mask = np.zeros(image.shape)
            corner_mask[start_x:end_x, start_y:end_y, :] = 1
            regions.append(image * corner_mask)
        return regions

    def extract(self, image):
        """
        Extracts abstract features from the given image.

        :param image: image from which features should be extracted
        :return: a numpy array with features, dimensionality depends on class settings.
        """
        # preprocess image (change to float, possibly move to hsv, etc.)
        image = self._preprocess_image(image)

        # split image into regions if necessary
        image_regions = self._extract_regions(image) if self._use_regions else [image]

        regions_hists = []
        for region in image_regions:
            # compute channel histograms for each region
            hists, _ = np.histogramdd(region.reshape(-1, 3), bins=self._bins_per_ch,
                                      range=[(0., 1.)]*3, normed=True)
            regions_hists.extend(hists.reshape(-1))

        if self._normalize:
            regions_hists /= np.linalg.norm(regions_hists)

        return np.array(regions_hists)


if __name__ == '__main__':
    import os
    import argparse
    import matplotlib.pyplot as plt
    import skimage.io as io
    import src.similarity_measures.measures as measures

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
    hist_ext = HistogramExtractor(nbins_per_ch=(12, 8, 3), use_hsv=True, use_regions=False)
    preds = np.array([hist_ext.extract(img) for img in imgs])

    print 'Finding similar images...'
    for _ in xrange(query_num):
        query_idx = np.random.randint(imgs.shape[0])
        query_img = preds[query_idx]

        sims = np.array([-measures.chisq_similarity(query_img, other) for other in preds])
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


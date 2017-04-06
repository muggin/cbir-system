import os

import image
import index as idx

def computeIndex(dataPath='.'):
    '''
    Find information and enlarge the index
    :param dataPath: location of image data set. The folder and sub-folders will be scanned.
    :return: index
    '''
    index = idx.buildIndex()
    for subdir, dirs, files in os.walk(dataPath):
        for f in files:
            # Todo : check if it's actually an image.
            filepath = os.path.join(subdir, f)
            img = image.loadImg(filepath)
            features = image.extractFeatures(img)
            idx.addToIndex(index, features, filepath)
    return index
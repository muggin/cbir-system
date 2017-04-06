'''
Representation of images.
'''

from PIL import Image
import imagehash

def loadImg(filepath):
    return Image.open(filepath)

def extractFeatures(img=None):
    return imagehash.dhash(img)
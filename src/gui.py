from PIL import Image

import image


def display(filenames):
    '''
    :param filenames: list of images to display
    '''
    for f in filenames:
        img = image.loadImg(f)
        img = img.resize((300,160),Image.ANTIALIAS)
        img.show()

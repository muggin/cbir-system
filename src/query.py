import image
import index as idx

def search(index, filename):
    '''
    Perform the search
    :param index: existing index
    :param filename: location of the file to perform the query on
    :return: List of information to retrieve
    '''
    img = image.loadImg(filename)
    qfeatures = image.extractFeatures(img)

    similarities = idx.score(index, qfeatures)
    ranking = idx.order(similarities)
    result = idx.extractInfo(index, ranking)
    return result

'''
Set of primitives functions which manipulate the index.
Beware : most of the functions are not pure and mutate the state (in general the first argument) as
Python give references.
'''

def buildIndex():
    '''
    Initiate the structure for the index.
    :return: a reference to the initiated index
    '''
    # For now, the index is a dictionary with the data abstraction (image feature) for keys
    # and file's location as values.
    index = {}
    return index

def addToIndex(index, key, value):
    '''
    Mutate index to add a new entry
    :param index: existing index
    :param key: key of the new entry (features)
    :param value: (filename)
    '''
    index[key] = value

def score(index, key):
    '''
    :param index: existing index
    :param key: data abstraction
    :return: list of dictionaries containing the score (field 'score') and information to retrieve
            the associated source (field 'key')
    '''
    return [{'score':(k - key), 'key':k} for k in index]

def order(answer):
    '''
    :param answer: list of dictionaries containing the score (field 'score') and information to retrieve
            the associated source (field 'key')
    :return: sorted list of dictionaries with respect of the score field
    '''
    return sorted(answer, key=lambda entry: entry['score'])

def extractInfo(index, answer):
    '''
    :param index: existing index
    :param answer: list of dictionaries containing the score (field 'score') and information to retrieve
            the associated source (field 'key')
    :return: list of file names. Keep the order of answer
    '''
    return [index[entry['key']] for entry in answer]

import os
import argparse
import cPickle as pickle
import src.indexes.mem_index as mem
import src.parsers.v1image_parser as v1

from skimage import io

# names of sections in config file

if __name__ == '__main__':
    # setup arg parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--parsed', required=True, help='Path to file containing parsed images')
    ap.add_argument('-d', '--dataset', required=True, help='Path to folder containing test data')
    ap.add_argument('-b', '--blacklist', default=None, help='Path to file with blacklist IDs')
    ap.add_argument('-m', '--metric', required=True, choices=['euclidean', 'intersection', 'cosine', 'chi2', 'kl', 'bhattacharyya'], 
                                                    help='Name of metric')
    ap.add_argument('-e', '--extractor', required=True, choices=['cnn_basic', 'hist_basic', 'cnn_hist'], 
                                                    help='Name of extractor')
    ap.add_argument('-k', '--topk', required=False, default=100, help='Nuber of results to return')
    ap.add_argument('-s', '--score', required=False, action='store_true', default=False, help='Nuber of results to return')

    # parse arguments
    args = vars(ap.parse_args())
    parsed_path = args['parsed']
    data_path = args['dataset']
    blacklist_path = args['blacklist']
    metric = args['metric']
    extractor = args['extractor']
    top_k = int(args['topk'])
    show_score = args['score']

    # load blacklist
    if blacklist_path is not None:
        with open(blacklist_path, 'r') as fd:
            blacklist = (['im' + img_id.strip() + '.jpg' for img_id in fd])
    else:
        blacklist = set([])

    # create parser
    print 'Setting up parser...'
    parser = v1.V1ImageParser()

    # create index
    print 'Setting up index...'
    index = mem.MemoryIndex(parsed_path)


    # evaluate images
    print 'Evaluating images...'
    for root, dirs, files in os.walk(data_path, topdown=True):
        for file_name in files:
            if file_name.endswith(('.jpg', '.png')) and file_name not in blacklist:
                image_path = os.path.join(root, file_name)
                query_image = io.imread(image_path)
                query_parsed = parser.prepare_document(file_name, query_image)
                query_doc = {'doc_name': None, 'features': query_parsed[extractor]}
                results = index.query_index(query_doc, metric, extractor, show_score)
                results = results[:top_k]
                print 'Results for query image: {}'.format(file_name)
                if show_score:
                    for result_name, score in results:
                        print '{} -- {}'.format(result_name, score)
                else:
                    for result_name in results:
                        print '{}'.format(result_name)

import os
import src.indexes
import src.parsers
import argparse
import ConfigParser as cp
import cPickle as pickle

from tqdm import tqdm
from skimage import io

# names of sections in config file
_CFG_GENERAL = 'General'
_CFG_GENERAL_INDEX = 'index'
_CFG_GENERAL_PARSER = 'parser'
_CFG_PARSER = 'ParserParams'
_CFG_INDEX = 'IndexParams'

if __name__ == '__main__':
    # setup arg parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='Path to folder containing data')
    ap.add_argument('-c', '--config', required=True, help='Path to the config file')
    ap.add_argument('-q', '--quiet', default=False, action='store_true', help='Work in quiet mode')
    ap.add_argument('-b', '--blacklist', default=None, help='Path to file with blacklist IDs')
    ap.add_argument('-i', '--import', default=None, required=False, help='Path to cPickle file with'
                                                                         ' parsed images')

    # parse arguments
    args = vars(ap.parse_args())
    data_path = args['dataset']
    config_path = args['config']
    blacklist_path = args['blacklist']
    feats_path = args['import']
    quiet_mode = args['quiet']

    # read config and blacklist files
    config_file = cp.SafeConfigParser()
    config_file.readfp(open(config_path))

    if blacklist_path is not None:
        with open(blacklist_path, 'r') as fd:
            blacklist = (['im' + img_id.strip() + '.jpg' for img_id in fd])
    else:
        blacklist = set([])

    # read sections
    parser_classname = config_file.get(_CFG_GENERAL, _CFG_GENERAL_PARSER)
    parser_class = getattr(src.parsers, parser_classname)
    parser_params = dict(config_file.items(_CFG_PARSER)) if config_file.has_section(
        _CFG_PARSER) else {}
    parser = parser_class(**parser_params)

    index_classname = config_file.get(_CFG_GENERAL, _CFG_GENERAL_INDEX)
    index_class = getattr(src.indexes, index_classname)
    index_params = dict(config_file.items(_CFG_INDEX)) if config_file.has_section(
        _CFG_INDEX) else {}
    index = index_class(**index_params)

    # index images

    if feats_path is None:
        if not quiet_mode:
            print 'Indexing images...'

        indexed_count = 0
        for root, dirs, files in os.walk(data_path, topdown=True):
            for file_name in tqdm(files):
                if file_name.endswith(('.jpg', '.png')) and file_name not in blacklist:
                    image_path = os.path.join(root, file_name)
                    image = io.imread(image_path)
                    image_parsed = parser.prepare_document(file_name, image)
                    index.insert_document(image_parsed)

                    indexed_count += 1
                    if not quiet_mode and indexed_count % 500 == 0:
                        print 'Indexed {} images...'.format(indexed_count)
    else:

        with open(feats_path, 'r') as fd:
            if not quiet_mode:
                print 'Loading parsed images to memory'
            parsed_images = pickle.load(fd)

            if not quiet_mode:
                print 'Indexing parsed images...'
            for image_parsed in tqdm(parsed_images):
                if image_parsed['doc_name'] not in blacklist:
                    index.insert_document(image_parsed)

    # persist index
    if not quiet_mode:
        print 'Persisting index...'
    index.persist_index()

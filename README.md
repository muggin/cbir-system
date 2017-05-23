# DD2476 Project - Content Based Image Retrieval Systems

## Description
For our project we chose to implement a simple Content-Based Image Retrieval System.
The system is based on two feature extractors, one using 2D color histograms and the other based on the VGG16 convolutional neural network. The system is backed by ElasticSearch.

## File organization

`src` directory - holds most of the code
- `feature_extractors` - packages holding all feature extractors
  - `base_ext.BaseExtractor` - base class for all extractors
  - `cnn_ext.CNNExtractor` - convnet histogram extractor
  - `hist_ext.HistogramExtractor` - 2D histogram feature extractor
- `indexes` - package holding all indexes
  - `base_index.BaseIndex` - base class for all indexes
  - `mem_index.MemoryIndex` - very simple in-memory index only for small test cases
  - `es_index.ESIndex` - elasticsearch based index
- `parsers` - package holding all image parsers
  - `base_parser.BaseParser` - base class for all parsers
  - `simple_parser.SimpleParser` - very simple parser using histograms as features
- `similarity_mesaures` - packages holding similarity measure functions
  - `cosine_similarity` - cosine similarity of two vectors
  - `euclidean_similarity` - euclidean distance between to vectors
  - `chisq_similarity` - chi-squared similarity of two distributions
  - `kl_similarity` - kullback-leibler divergence of two distributions
  - `bhattacharyya_similarity` - bhattacharyya similarity of two distributions
  - `intersection_similarity` - intersections of two distributions

`data` directory - holds small datasets for local testing
- `small` - small dataset for quick local tests
- `xsmall` - super small dataset, only 4 imgaes for prototyping
- `flickr_25k` - not in repo but should be placed here (locally)
- `flickr_25k/meta/annotations` - not in the repo. Should contains the annotations files provided.

`scripts` directory - holds all scripts related to the image retrieval system
- `index_data.py` - script that runs indexing, requires config in appropriate format (look below for details).

`configs` directory - holds `index_data.py` configurations
- `simple_test.cfg` - simple indexing using SimpleParser and MemoryIndex

`frontend` directory - holds the React-based frontend for the project. Uses webpack to build JavaScript and package it to a bundle. See the README in the frontend directory for more instructions.

`server.py` file - contains a light-weight flask application for receiving HTTP-requests from the frontend.

## Execution
### Image indexing
The `index_data.py` script is responsible for indexing images. the script takes as arguments a path to the directory holding the files and a path to the config file.

Example call: `python scripts/index_data.py -d data/xsmall -c configs/simple_test.cfg`

The config file should be in the following format
```python
[General]
parsers=ParserClassName # this is mandatory, names as found in the `parsers` package (without package prefix)
index=IndexClassName # this is mandatory, names as found in the `indexes` package (without package prefix)

[ParserParams]
key=value # these params will be passed to the class on init, this section can be empty

[IndexParams]
key=value # these params will be passed to the class on init this section can be empty
```

## Servers

There are two docker containers necessary in order to run this application.

Elasticsearch is run by first increasing the vm limit, then building and running the docker container

`sudo sysctl -w vm.max_map_count=262144`

`docker-compose build elasticsearch`

`docker-compose up elasticsearch`

The backend server is built and run with the following commands:

`docker-compose build server`

`docker-compose up server`

In order to index or debug within the server container you can run bash inside the server docker container:

`docker-compose run server bash`






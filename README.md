# DD2476 Project - Content Based Image Retrieval Systems

## File organization

`src` directory - holds most of the code
- `feature_extractors` - packages holding all feature extractors
  - `base_ext.BaseExtractor` - base class for all extractors
  - `cnn_ext.CNNExtractor` - ConvNet histogram extractor
  - `hist_ext.HistogramExtractor` - 2D histogram feature extractor
- `indexes` - package holding all indexes
  - `base_index.BaseIndex` - base class for all indexes
  - `mem_index.MemoryIndex` - very simple in-memory index only for small test cases
  - `es_index.ESIndex` - ElasticSearch based index
- `parsers` - 
  - `base_parser.BaseParser` - base class for all parsers
  - `simple_parser.SimpleParser` - very simple parser using histograms as features
- `similarity_mesaures` - packages holding similarity measure functions
  - `cosine_similarity` - cosine similarity of two vectors
  - `euclidean_similarity` - euclidean distance between to vectors
  - `chisq_similarity` - chi-Squared similarity of two distributions
  - `kl_similarity` - KL divergence of two distributions
  - `bhattacharyya_similarity` - Bhattacharyya similarity of two distributions
  - `intersection_similarity` - Intersections of two distributions
  


`data` directory - holds small datasets for local testing
- `small` - small dataset for quick local tests
- `xsmall` - super small dataset, only 4 imgaes for prototyping
- `flickr_25k` - not in repo but should be placed here (locally)

`scripts` directory - holds all scripts related to the image retrieval system
- `index_data.py` - script that runs indexing, requires config in appropriate format. refer to help or source for more details.

`configs` directory - holds `index_data.py` configurations
- `simple_test.cfg` - simple indexing using SimpleParser and MemoryIndex

## Description

 

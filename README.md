# kth-seir-project

# Components

- `image.py` : regroups functions to manipulate images. Side effects : i/o (mainly reading disk)
- `index.py` : index representation/abstraction. Function may mutate the index state. 
- `indexer.py` : smart part to build the index. Rely on the two first representations.
- `query.py` : all elements to perform a query. Rely on the two first representations.
- `gui.py` : dirty graphical user interface.
- `seir.py` : main

# Description

The code is based on notions from functional programming and mainly implements pure functions. Elements are represented
 with 'primitive' types (only dictionary, list, ...)

 

import argparse

import gui as ui
import indexer
import query

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True, help="Path to folder containing")
    ap.add_argument("-q", "--query", required=True, help="Path to the query image")
    args = vars(ap.parse_args())

    dataPath = args["dataset"]
    queryFilename = args["query"]

    index = indexer.computeIndex(dataPath)
    result = query.search(index, queryFilename)
    ui.display(result) # Todo, decrease correlation of the view with the result structure.

if __name__ == '__main__':
    main()

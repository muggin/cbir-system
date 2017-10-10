import os
import re
import argparse
import random
import matplotlib.pyplot as plt
import os
import argparse
import cPickle as pickle
import src.indexes.mem_index as mem
import src.parsers.v1image_parser as v1

from skimage import io


import numpy as np

def apk(relevant, predicted, k=10):
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if relevant[i] and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not relevant:
        return 0.0

    return score

def mapk(actual, predicted, k=10):
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

if __name__ == "__main__":

    # setup arg parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--parsed', required=True, help='Path to file containing parsed images')
    ap.add_argument('-b', '--blacklist', default=None, help='Path to file with blacklist IDs')
    ap.add_argument('-d', '--datapath', required=True, help='Path to folder containing images')
    ap.add_argument('-t', '--topic', required=True, help='Path to folder containing images topics as text files')
    ap.add_argument('-a', '--annotation', required=True, help='Path to folder containing Flickr annotations')
    ap.add_argument('-k', '--topk', required=False, default=100, help='Nuber of results to return')


    # parse arguments
    args = vars(ap.parse_args())
    parsed_path = args['parsed']
    blacklist_path = args['blacklist']
    data_path = args['datapath']
    topic_path = args['topic']
    annotation_path = args['annotation']
    K = int(args['topk'])
    show_score = True

    metrics = ['euclidean', 'intersection', 'cosine', 'chi2', 'kl', 'bhattacharyya']
    extractors = ['cnn_basic', 'hist_basic', 'cnn_hist']
    extractor = 'cnn_basic'
    metric = 'cosine'

    mean_avg_pre = np.zeros((len(extractors), len(metrics)))


    avg_pre = np.zeros((K))

    # load blacklist
    if blacklist_path is not None:
        with open(blacklist_path, 'r') as fd:
            img_ids = map(int, fd)
            file_names = (['im' + str(id) + '.jpg' for id in img_ids])
    else:
        file_names = set([])


    # create parser
    print 'Setting up parser...'
    parser = v1.V1ImageParser()

    # create index
    print 'Setting up index...'
    index = mem.MemoryIndex(parsed_path)


    for a, extractor in enumerate(extractors):
        print
        print extractor
        for b, metric in enumerate(metrics):
            print metric

            for j in range(len(img_ids)):
            #for j in range(2):
                    print j
                    id = img_ids[j]
                    img_name = file_names[j]

                    image_path = os.path.join(data_path, img_name)
                    query_image = io.imread(image_path)
                    query_parsed = parser.prepare_document(img_name, query_image)
                    query_doc = {'doc_name': None, 'features': query_parsed[extractor]}
                    ranked_results = index.query_index(query_doc, metric, extractor, show_score)
                    ranked_results = [x for x in ranked_results if x[0] not in file_names]
                    ranked_results = ranked_results[:K]
                    if False :
                        print 'Results for query image: {}'.format(img_name)
                        if show_score:
                            for result_name, score in ranked_results:
                                print '{} -- {}'.format(result_name, score)
                        else:
                            for result_name in ranked_results:
                                print '{}'.format(result_name)

                    #print ranked_results
                    ranked_results_id = [int(name[0].strip().split('.')[0][2:]) for name in
                                         ranked_results]


                    # find image topic
                    with open(os.path.join(topic_path, str(id)+".topic.txt"), 'r') as topics_fd:
                        same_topics_ids = []
                        # load ids related to topic
                        topics = []
                        for t in topics_fd:
                            topics.append(t.strip())
                            with open(os.path.join(annotation_path, t[:-1]+"_r1.txt"), 'r') as f:
                                same_topics_ids.extend(map(int, f))
                        # determine relevancy for each returned file
                        relevance = [True if doc_id in same_topics_ids else False for i, doc_id in
                                     enumerate(ranked_results_id) if i < K]

                        # cumulative sum of number of relevant document
                        cumsum_relevance = reduce(lambda c,x: c+[c[-1]+x], map(int, relevance), [0])[1:]

                        nb_rel_doc = len(set(same_topics_ids))
                        precision = map(lambda (i,x): float(x)/(i+1), enumerate(cumsum_relevance))
                        recall = map(lambda x: float(x) / nb_rel_doc, cumsum_relevance)

                        avg_pre[j] = apk(relevance, ranked_results_id, k=K)

                        if False:
                            fig, ax = plt.subplots()
                            fig.suptitle("Image query\n feature extractor : "+extractor+" - similarity metric : "+metric)
                            fig = plt.subplot(2,2,1)
                            fig.set_title("query : " + img_name + "\ntopics : " + ' - '.join(topics))
                            fig = plt.imshow(io.imread(image_path))
                            fig.axes.get_xaxis().set_visible(False)
                            fig.axes.get_yaxis().set_visible(False)

                            fig = plt.subplot(2, 2, 2)
                            fig.set_title("Evolution of recall and precision - P@{}={}".format(K, avg_pre[i]))
                            ax = fig.axes
                            ax.plot(recall, color='Red')
                            ax.set_ylabel('Recall', color='Red')
                            ax.tick_params(axis='y', colors='Red')
                            ax = fig.axes.twinx()
                            ax.plot(precision, color='Blue')
                            ax.set_ylabel('Precision', color='Blue')
                            ax.tick_params(axis='y', colors='Blue', direction='out')

                            for i in range(10):
                                fig = plt.subplot(4,5,11+i)
                                fig.set_title("result "+str(i+1))
                                fig = plt.imshow(io.imread(os.path.join(data_path, ranked_results[i][0])))
                                fig.axes.get_xaxis().set_visible(False)
                                fig.axes.get_yaxis().set_visible(False)


                            print relevance
                            print cumsum_relevance
                            print precision
                            print recall

                            plt.show()


            mean_avg_pre[a,b] = avg_pre.mean()

    print mean_avg_pre
    mean_avg_pre.tofile('map.csv',sep=',',format='%10.8f')



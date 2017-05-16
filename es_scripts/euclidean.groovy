int distance = 0
int max_score = 9363600
def docvalues

if(extractor == "cnn_basic") {
	docvalues = _source.cnn_basic
} else if(extractor == "cnn_hist") {
	docvalues = _source.cnn_hist
} else if(extractor == "hist_basic") {
	docvalues = _source.hist_basic
}

def newvalues = features
if(docvalues.size() != newvalues.size()) {
    distance = max_score
} else {
    int i = 0
    for(val in docvalues) {
        diff = val - features[i]
        distance += (diff * diff)
        i += 1
    }
}

return distance
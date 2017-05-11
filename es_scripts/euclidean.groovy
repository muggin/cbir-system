int distance = 0
int max_score = 9363600
def docvalues = _source.features
def newvalues = features
if(docvalues.size() != newvalues.size()) {
    distance = max_score
} else {
    int i = 0
    for(val in docvalues){
        diff = val - features[i]
        distance += (diff * diff)
        i += 1
    }
}

return distance
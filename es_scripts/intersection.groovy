double sum = 0

def docvalues

if(extractor == "cnn_basic") {
	docvalues = _source.cnn_basic
} else if(extractor == "cnn_hist") {
	docvalues = _source.cnn_hist
} else if(extractor == "hist_basic") {
	docvalues = _source.hist_basic
} else {
	return -1
}

def newvalues = features

if(docvalues.size() == newvalues.size()) {
	int i = 0
	for(val in docvalues) {
		sum += min(val, newvalues[i])
		i += 1
	}
}

return sum
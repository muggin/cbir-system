
double sum = 0

def docvalues = _source.features
def newvalues = features

if(docvalues.size() == newvalues.size()) {
	int i = 0
	for(val in docvalues) {
		sum += min(val, newvalues[i])
		i += 1
	}
}

return sum
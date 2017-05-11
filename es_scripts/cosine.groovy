

double sum = 0
double first_norm = 0
double second_norm = 0

def docvalues = _source.features
def newvalues = features

if(docvalues.size() != newvalues.size()) {
	score = 0
} else {
	int i = 0
	for(val in docvalues) {
		sum += val * newvalues[i]
		first_norm += pow(val, 2)
		second_norm += pow(newvalues[i], 2)
		i += 1
	}
}

return sum / (sqrt(first_norm) * sqrt(second_norm))
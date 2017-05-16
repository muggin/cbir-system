from base_index import BaseIndex
import json
import httplib
import re
from base64 import b64encode

INDEX_PATH = "/image/"

auth = b64encode(b"elastic:changeme").decode("ascii")

class ESIndex():
	def __init__(self, url, threshold=500):
		self.URL = url
		self.counter = 1 # Document ID
		self.doc_buffer = [] # Hold documents until threshold is reached or persist_index() is called
		self.DOC_THRESHOLD = threshold # The amount of documents required to trigger the indexing
		self.connection = httplib.HTTPConnection(self.URL)
		self.connection.close()
	# Stores a document in the buffer
	# When a certain threshold is met, indexes them all at once
	def insert_document(self, document_dict):
		
		self.doc_buffer.append(document_dict)

		if len(self.doc_buffer) >= self.DOC_THRESHOLD:
			self.index_docs();

	# Does the actual indexing
	def index_docs(self):
		
		self.connection = httplib.HTTPConnection(self.URL)
		for doc in self.doc_buffer:
			# Index data

			self.connection.request('POST', INDEX_PATH + str(self.counter), json.JSONEncoder().encode({"doc_name" : doc["doc_name"], "cnn_basic" : doc["cnn_basic"], "hist_basic" : doc["hist_basic"], "cnn_hist" : doc["cnn_hist"]}), { "Content-Type" : "application/json", "Authorization" : "Basic " + auth })
			# Retrieve response for debug, could be relevant to use for error handling
			response = json.loads(self.connection.getresponse().read().decode())
			print response
			self.counter += 1

		self.connection.close()
		self.doc_buffer = []

	# Query ES with specified image
	def query_index(self, query_dict, similarity, extractor):
		
		tmpdict = {"sort" : { "_score" : "asc" }, "query" : {"function_score" : {"script_score" : {"script" : { "file" : "", "lang" : "groovy", "params" : {"features" : query_dict["features"], "extractor" : ""}}}}}}
		# Set similarity computation
		tmpdict["query"]["function_score"]["script_score"]["script"]["file"] = similarity
		# Set extractor features
		tmpdict["query"]["function_score"]["script_score"]["script"]["params"]["extractor"] = extractor
		
		# Put together query string
		query_string = json.JSONEncoder().encode(tmpdict)

		print query_string

		self.connection = httplib.HTTPConnection(self.URL)
		auth = b64encode(b"elastic:changeme").decode("ascii")
		
		# Submit the search query to ES
		self.connection.request('GET', '/_search', query_string, { "Content-Type": "application/json", 'Authorization' : 'Basic ' + auth })

		# Retrieve response
		response = json.loads(self.connection.getresponse().read().decode())
		print response
		
		self.connection.close()
		return response
 
	# If there are documents in the buffer, this method is called to finalize the indexing
	def persist_index(self):
		if len(self.doc_buffer) > 0:
			self.index_docs()

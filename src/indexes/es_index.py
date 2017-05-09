from base_index import BaseIndex
import json
import httplib
import re

INDEX_PATH = "/images/"


class ESIndex():
	def __init__(self, url, threshold=500):
		self.URL = url
		self.counter = 1 # Document ID
		self.doc_buffer = [] # Hold documents until threshold is reached or persist_index() is called
		self.DOC_THRESHOLD = threshold # The amount of documents required to trigger the indexing

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
			#print json.JSONEncoder().encode({"doc_name" : doc["doc_name"], "query_feature" : doc["features"]})
			# Index data
			self.connection.request('POST', INDEX_PATH + str(self.counter), json.JSONEncoder().encode({"doc_name" : doc["doc_name"], "features" : doc["features"]}), { "Content-Type": "application/json" })
			# Retrieve response for debug, could be relevant to use for error handling
			response = json.loads(self.connection.getresponse().read().decode())
			print response
			self.counter += 1

		self.connection.close()
		self.doc_buffer = []

	# Query ES with specified image
	def query_index(self, query_dict, query_fields):
		# Put together query string
		query_string = json.JSONEncoder().encode({"sort" : { "_score" : "asc" }, "query" : {"function_score" : {"script_score" : {"script" : { "file" : "eucl", "lang" : "groovy", "params" : {"features" : query_dict["features"]}}}}}})
		
		self.connection = httplib.HTTPConnection(self.URL)
		
		# Print query string for debug purposes
		print query_string
		
		# Submit the search query to ES
		self.connection.request('GET', '/images/_search', query_string)

		# Retrieve response
		response = json.loads(self.connection.getresponse().read().decode())
		print response
		
		self.connection.close()
		return response
 
	# If there are documents in the buffer, this method is called to finalize the indexing
	def persist_index(self):
		if len(self.doc_buffer) > 0:
			self.index_docs()
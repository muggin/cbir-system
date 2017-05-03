from base_index import BaseIndex
import json
import httplib

URL = "localhost:9200"
INDEX_PATH = "images/image/"

class ESIndex():
	def __init__(self):
		self.counter = 1

	def insert_document(self, document_dict):
		with open(document_dict, 'r') as file:
			data = file.read()
		self.connection = httplib.HTTPConnection(URL)
		self.connection.request('POST', INDEX_PATH + str(self.counter), data, { "Content-Type": "application/json" })
		response = json.loads(self.connection.getresponse().read().decode())
		self.counter += 1
		self.connection.close()
		return response

	# On it, just need to read up on docs
	def query_index(self, query_dict, query_fields):
		pass

	# On hold
	def persist_index(self):
		pass
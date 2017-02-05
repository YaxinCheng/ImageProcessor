from pymongo import MongoClient

class MongoDB:
	uri = 'mongodb://heroku_glcz6m5s:s9aov2qcf0abptsradc630bc3v@ds143559.mlab.com:43559/heroku_glcz6m5s'
	def __init__(self):
		self._client = MongoClient(MongoDB.uri)
		self.cursor = self._client.heroku_glcz6m5s

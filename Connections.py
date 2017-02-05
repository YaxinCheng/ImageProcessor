from pymongo import MongoClient

class MongoDB:
	uri = 'mongodb://heroku_pl2gkfc9:uph4v7gjr1jr58qqo5pr42lumv@ds161038.mlab.com:61038/heroku_pl2gkfc9'
	def __init__(self):
		self._client = MongoClient(MongoDB.uri)
		self.cursor = self._client.heroku_pl2gkfc9

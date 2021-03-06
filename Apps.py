from flask_restful import Resource
from flask import stream_with_context, request, Response
import json
from processor import *
from ImageExporter import *
from Connections import MongoDB
from bson.objectid import ObjectId
import pymongo
from six.moves import cPickle as pickle
from numpy import *

def getJSON(request):
	return json.loads(json.dumps(request.get_json(force = True)))	

class imageCollector(Resource): 
	def get(self):
		def generate():
			db = MongoDB()
			cursor = db.cursor.imageLibrary.find({'label': {'$ne': '0,0,0,0,0,0,0,0,0,0,0,0'}})
			while cursor.alive:
				for imagePackage in cursor:
					img, label = imagePackage['img'], imagePackage['label']
					exporter = ImageExporter(image = img, label = label)
					images, labels = exporter.downloadImagesFromServer()
					for image, label in zip(images, labels):
						yield pickle.dumps((image, label), pickle.HIGHEST_PROTOCOL)
		return Response(stream_with_context(generate()), mimetype = 'application/pickle', headers = {'Content-Disposition': 'attachment; filename=data.pickle', 'Content-type': 'application/pickle'})

	def post(self):
		content = getJSON(request)
		processor = Processor()
		try:
			id = processor.processImgAtServer(image = content['img'], label = content['label'], mode = content['mode'], id = content['id'])
		except:
			return {'Result': 'Failed processing image'} 
		return {'Result': str(id)}
	
	def put(self):
		content = getJSON(request)
		print(content)
		db = MongoDB()
		db.cursor.imageLibrary.remove({'_id': ObjectId(content['_id'])})
		return {'Result': 'Removed'}


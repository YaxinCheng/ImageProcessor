from flask_restful import Resource
from flask import request
import json
from processor import *
from ImageExporter import *
from Connections import MongoDB
from bson.objectid import ObjectId

def getJSON(request):
	return json.loads(json.dumps(request.get_json(force = True)))	

class imageCollector(Resource):
	def get(self):
		imgExporter = ImageExporter()
		return json.dumps(imgExporter.downloadImagesFromServer())

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

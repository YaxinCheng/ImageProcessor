from flask_restful import Resource
from flask import request
import json
from processor import *
from ImageExporter import *

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

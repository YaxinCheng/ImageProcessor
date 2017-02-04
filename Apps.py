from flask_restful import Resource
from flask import request
import json
from Processor import *

def getJSON(request):
	return json.loads(json.dumps(request.get_json(force = True)))	

class imageCollector(Resource):
	def get(self):
		return {'index': 'hello world'}
	
	def post(self):
		content = getJSON(request)
		processor = Processor()
		try:
			processor.processImgAtServer(image = content['img'], label = content['label'])
		except:
			return {'Result': 'Failed processing image'} 
		return {'Result': 'Success'}

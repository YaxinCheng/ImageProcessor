from PIL import Image
from numpy import *
import requests
from pymongo import MongoClient
from Connections import MongoDB
import base64
from io import BytesIO
#

class Processor:
	def __init__(self, desiredSize = (300, 300)):
		self._desiredSize = desiredSize
	
	@staticmethod
	def openImg(name):
		img = Image.open(name)
		return img

	def _scaleImg(self, img, size = None):
		if size is None:
			size = self._desiredSize
		return img.resize(size, Image.LANCZOS)

	def _decodeImage(self, img):
		return Image.open(BytesIO(base64.b64decode(img)))
	
	def _encodeImage(self, img): 
		imageBuffer = BytesIO()
		img.save(imageBuffer, format = "JPEG")
		return base64.encodestring(imageBuffer.getvalue())
	
	def processImgAtServer(self, image, label):
		if type(image) == str:
			image = self._decodeImage(image)
		if (image.width, image.height) != self._desiredSize:
			image = self._scaleImg(image)
		imageString = self._encodeImage(image)
		mongodb = MongoDB()
		mongodb.cursor.imageLibrary.insert({'img': imageString, 'label': label}) 

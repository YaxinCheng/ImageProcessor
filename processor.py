from PIL import Image
from numpy import *
import requests
from pymongo import MongoClient
import MongoURI
import base64
from io import BytesIO

class Processor:
	def __init__(self, desiredSize = (300, 300)):
		self._desiredSize = desiredSize
	
	@staticmethod
	def openImg(name):
		img = Image.open(name)
		return img

	def _rotate(self, image, angle = 45):
		return image.rotate(angle)
	
	def _imgToArray(self, image):
		return asarray(image, dtype = uint8).T
	
	def _arrayToString(self, imgArray):
		return imgArray.tostring()
	
	def _matchImgToLabels(self, images, labels):
		imageList = list()
		for (img, label) in zip(images, labels):
			matchedResult = dict()
			imgData = self._imgToArray(img)
			shape = imgData.shape
			print(shape)
			matchedResult['img'] = self._arrayToString(imgData)
			matchedResult['label'] = label
			matchedResult['shape'] = shape
			imageList.append(matchedResult)
		return imageList
	
	def _saveToServer(self, images, labels):
		#connect to the server
		if len(images) != len(labels):
			raise ValueError
		host = 'http://localhost'
		port = '8000'
		data = self._matchImgToLabels(images, labels)
		response = requests.post(host + port, data)
	
	def _scaleImg(self, img, size = None):
		if size is None:
			size = self._desiredSize
		return img.resize(size, Image.LANCZOS)

	def _decodeImage(self, img):
		return Image.open(BytesIO(base64.b64decode(img)))
	
	def processImgAtServer(self, image, label):
		if type(image) == str:
			image = self._decodeImage(image)
		if (image.width, image.height) != self._desiredSize:
			image = self._scaleImg(image)
		imageBuffer = BytesIO()
		image.save(imageBuffer, format = "JPEG")
		imageString = base64.encodestring(imageBuffer.getvalue()).strip()
		client = MongoClient(MongoURI.uri)
		cursor = client.heroku_pl2gkfc9
		cursor.imageLibrary.insert({'img': imageString, 'label': label})
	
	def processImgsAtLocal(self, images, labels):
		if len(images) != len(labels):
			raise ValueError
		for index, img in enumerate(images):
			if (img.width, img.height) != self._desiredSize:
				images[index] = self._scaleImg(img)
		self._saveToServer(images, labels)
		for _ in range(7):
			images = list(map(self._rotate, images))
			self._saveToServer(images, labels)

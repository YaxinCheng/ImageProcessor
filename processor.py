from PIL import Image
from numpy import *
import requests

class processor:
	def __init__(self, desiredSize = (400, 400)):
		self._desiredSize = desiredSize
	
	@staticmethod
	def openImg(name):
		img = Image.open(name)
		return img

	def _rotate(self, image, angle = 45):
		return image.rotate(angle)
	
	def _imgToArray(self, image):
		return asarray(image, dtype = uint8).T
	
	def _matchImgToLabels(self, images, labels):
		matchedResult = dict()
		for (img, label) in zip(images, labels):
			matchedResult[img] = labels 
		return matchedResult
	
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
		return img.thumbnail(size, Image.ANTIALIAS)	
	
	def processImgs(self, images, labels):
		if len(images) != len(labels):
			raise ValueError
		for index, img in enumerate(images):
			if (img.width, img.height) != self._desiredSize:
				images[index] = self._scaleImg(img)
		self._saveToServer(images, labels)
		for _ in range(7):
			images = list(map(self._rotate, images))
			self._saveToServer(images, labels)

from PIL import Image
from Connections import MongoDB
import base64
from io import BytesIO
from numpy import *

class ImageExporter:
	def __init__(self, image, label):
		self._image = image
		self._label = label

	def _rotate(self, image, angle):
		return image.rotate(angle)
	
	def _imgToArray(self, image):
		return array(image)
	
	def _scaleImg(self, img, size = None):
		if size is None:
			size = self._desiredSize
		return img.resize(size, Image.LANCZOS)
	
	def _decodeImage(self):
		return Image.open(BytesIO(base64.b64decode(self._image)))

	def _encodeImage(self, img):
		imageBuffer = BytesIO()
		img.save(imageBuffer, format = "JPEG")
		return base64.encodestring(imageBuffer.getvalue())
	
	def _processImage(self):
		images = list()
		labels = list()
		originalImg = self._decodeImage()
		img = originalImg
		flipped = originalImg.transpose(Image.FLIP_LEFT_RIGHT)
		label = array(list(map(lambda element: uint8(element), self._label.split(','))))
		for eachImg in [img, flipped]:
			img = eachImg
			for angle in range(0, 360, 90):
				try:
					imgData = self._imgToArray(img) 
					images.append(imgData)
					labels.append(label) 
					img = self._rotate(img, angle = angle)
				except:
					continue
		return  (images, labels) 
		 
	def downloadImagesFromServer(self):
		return self._processImage()
	

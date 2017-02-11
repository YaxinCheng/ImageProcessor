from PIL import Image
from Connections import MongoDB
import base64
from io import BytesIO
from numpy import *

class ImageExporter:
	def __init__(self, compressToSize = None):
		self._size = compressToSize

	def _rotate(self, image, angle):
		return image.rotate(angle)
	
	def _imgToArray(self, image):
		return array(image).T
	
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
	
	def _processImage(self, imagePackage):
		images = list()
		labels = list()
		for each in imagePackage:
			try:
				eachImg = each['img']
				originalImg = self._decodeImage(eachImg)
				img = originalImg
				label = list(map(lambda x: int(x), each['label'].split(',')))
				for angle in range(0, 361, 45):
								try:
									imgData = self._imgToArray(img) 
									images.append(imgData.tolist())
									labels.append(label) 
									img = self._rotate(originalImg, angle = angle)
								except:
									continue
			except:
				continue
		return [ images, labels] 
		 
	def downloadImagesFromServer(self):
		mongodb = MongoDB()
		imgPackage = mongodb.cursor.imageLibrary.find({}) 
		return self._processImage(imgPackage)
	

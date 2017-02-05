from ImageExporter import *
from numpy import *
import json

ie = ImageExporter()
value = ie.downloadImagesFromServer()
print(type(value))
result = json.loads(value)

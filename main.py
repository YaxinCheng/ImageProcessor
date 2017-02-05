from flask import Flask, make_response
from flask_restful import Api
from bson.json_util import dumps
import Apps

app = Flask(__name__)
api = Api(app)
def output_json(obj, code, headers = None):
	resp = make_response(dumps(obj), code)
	resp.headers.extend(headers or {})
	return resp
api.representations = {'application/json': output_json}

api.add_resource(Apps.imageCollector, '/')

if __name__ == '__main__':
	app.run(host = '127.0.0.1', port = 8000, debug = True)

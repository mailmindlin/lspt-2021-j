import os
from flask import Flask, json, jsonify
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.wrappers import request
from route_cofig import *

app = Flask( __name__.split('.')[0])
api = Api(app)
if __name__ == "__main__":
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host = host, port = port, threaded = True)
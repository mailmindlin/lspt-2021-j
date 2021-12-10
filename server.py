import os
from flask import Flask
from mock import inject_mocks
from routes import blueprint
from argparse import ArgumentParser

app = Flask(__name__.split('.')[0])
app.register_blueprint(blueprint)

parser = ArgumentParser()
parser.add_argument("--mock", action="store_true")
parser.add_argument("--port", type=int, default=8080)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.mock:
        inject_mocks()
    
    host = os.environ.get('IP', '0.0.0.0')
    port = int(args.port)
    app.run(host = host, port = port, threaded = True)
# app.py
#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, make_response, jsonify, request
from flask_restful import Resource
from flask_cors import CORS

# Local imports
from config import app, db, api

# Add your model imports

app = Flask(__name__)

CORS(app)

# Views go here!
@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)


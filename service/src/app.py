#!/usr/bin/python

import sys
from flask import Flask, jsonify
from flask_cors import CORS

from services.user_service import user_service
from services.room_service import room_service
from services.round_service import round_service
from services.image_service import image_service
from services.rating_service import rating_service
from services.word_service import word_service
from services.exceptions import InvalidUsage
from database.database import session
import logging

data_dir = "/Users/silleknarf/Code/art-master/data"

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_service)
app.register_blueprint(room_service)
app.register_blueprint(round_service)
app.register_blueprint(image_service)
app.register_blueprint(rating_service)
app.register_blueprint(word_service)

@app.route("/")
def home():
    return "Welcome to the art-master api"

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

if __name__ == "__main__":
    logging.basicConfig(filename='art-master.log',level=logging.INFO)
    app.run(host="localhost", port=5000, debug=True, threaded=True)

#!/usr/bin/python

import sys
from flask import Flask, jsonify
from flask_cors import CORS
import database.database
from flask_sqlalchemy_session import flask_scoped_session

import logging

data_dir = "/Users/silleknarf/Code/art-master/data"
logfile = logging.getLogger("file")

app = Flask(__name__)
CORS(app)
database.database.session = flask_scoped_session(database.database.session_maker, app)

from services.user_service import user_service
from services.room_service import room_service
from services.round_service import round_service
from services.image_service import image_service
from services.rating_service import rating_service
from services.word_service import word_service
from services.exceptions import InvalidUsage

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
def shutdown_session(response):
    database.database.session.remove()

format_str = "%(asctime)s %(levelname)s %(message)s"
formatter = logging.Formatter(format_str)

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logger = logging.getLogger(name)
    logger.addHandler(handler)

@app.before_first_request
def initialise():
    # Create a specific logger for the service
    logging.basicConfig(filename="art-master.service.log",level=logging.ERROR, format=format_str)

    setup_logger("file", "art-master.log")
    setup_logger("sqlalchemy.engine", "art-master.sql.log")

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True, threaded=True)

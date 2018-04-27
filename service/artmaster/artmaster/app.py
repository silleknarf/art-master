#!/usr/bin/python

import sys
from flask import Flask, jsonify
from flask_cors import CORS

from artmaster.services.user_service import user_service
from artmaster.services.room_service import room_service
from artmaster.services.round_service import round_service
from artmaster.services.image_service import image_service
from artmaster.services.rating_service import rating_service
from artmaster.services.word_service import word_service
from artmaster.services.exceptions import InvalidUsage
from artmaster.database.database import session
import logging

data_dir = "/Users/silleknarf/Code/art-master/data"
logfile = logging.getLogger("file")

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

#!/usr/bin/python

import sys
import logging
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from database.database import session
from werkzeug.exceptions import HTTPException

data_dir = "/Users/silleknarf/Code/art-master/data"
logfile = logging.getLogger("file")

app = Flask(__name__)
CORS(app)

from services.user_service import user_service
from services.room_service import room_service
from services.round_service import round_service
from services.image_service import image_service
from services.rating_service import rating_service
from services.word_service import word_service
from services.minigame_service import minigame_service
from services.exceptions import InvalidUsage

app.register_blueprint(user_service)
app.register_blueprint(room_service)
app.register_blueprint(round_service)
app.register_blueprint(image_service)
app.register_blueprint(rating_service)
app.register_blueprint(word_service)
app.register_blueprint(minigame_service)

@app.route("/")
def home():
    return "Welcome to the art-master api"

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    logfile.error(str(e))
    logfile.error(traceback.format_exc())
    return jsonify(error=str(e)), code

@app.teardown_appcontext
def shutdown_session(response):
    session.remove()

format_str = "%(asctime)s %(levelname)s %(message)s"
formatter = logging.Formatter(format_str)

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)

@app.before_first_request
def initialise():
    setup_logger("werkzeug", "art-master.service.log")
    setup_logger("file", "art-master.log")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)

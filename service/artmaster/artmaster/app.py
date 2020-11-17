#!/usr/bin/python

import sys
import logging
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from database.database import session
from werkzeug.exceptions import HTTPException
from config import Config
from flask_socketio import SocketIO
from celery import Celery, signals
from celery.utils.log import get_task_logger

celery_logfile = get_task_logger("file")
logfile = logging.getLogger("file")

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SOCKETIO_PASSWORD
CORS(app, resources={r"/*":{ "origins": Config.CORS_URL }})
socketio = SocketIO(
    app,
    message_queue="redis://redis:6379",
    cors_allowed_origins=Config.CORS_URL
)

app.config.update(
    CELERY_BROKER_URL='redis://redis:6379',
    CELERY_RESULT_BACKEND='redis://redis:6379'
)

# Celery integration with Flask - adapted from:
# https://flask.palletsprojects.com/en/0.12.x/patterns/celery/
def make_celery(flask_app):
    new_celery = Celery(flask_app.import_name, 
        backend=flask_app.config['CELERY_RESULT_BACKEND'],
        broker=flask_app.config['CELERY_BROKER_URL'])
    new_celery.conf.update(flask_app.config)
    TaskBase = new_celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    new_celery.Task = ContextTask
    return new_celery

celery = make_celery(app)

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
    return "Welcome to the Craicbox API"

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
    setup_logger("werkzeug", "craicbox.service.log")
    setup_logger("file", "craicbox.log")

@signals.after_setup_logger.connect
def setup_loggers(*args, **kwargs):
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    celery_logfile.addHandler(sh)

    fh = logging.FileHandler("craicbox.log")
    fh.setFormatter(formatter)
    celery_logfile.addHandler(fh)
    celery_logfile.setLevel(logging.INFO)

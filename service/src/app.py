#!/usr/bin/python

import sys
from flask import Flask
from flask_cors import CORS

from services.user_service import user_service
from services.room_service import room_service
from services.round_service import round_service
from services.image_service import image_service
from services.rating_service import rating_service
from services.word_service import word_service

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

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)

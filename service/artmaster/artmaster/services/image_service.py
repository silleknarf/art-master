#/usr/bin/python

import base64
import logging
import os
from flask import Blueprint, jsonify, request
from repositories import image_repository, round_repository
from .round_state_machine import RoundStateMachine

logfile = logging.getLogger('file')
image_service = Blueprint('image_service', __name__)
data_dir = "../../../ui/public/data"

@image_service.route("/image", methods=["POST"])
def upload_drawing():
    user_id = int(request.args.get("userId"))
    round_id = int(request.args.get("roundId"))
    logfile.info("Adding drawing for user: %s for round: %s" % (user_id, round_id))
    image_base_64 = request.get_json()["imageBase64"]

    drawing = image_repository.create_image(user_id, image_base_64, round_id)

    round_entity = round_repository.get_round(round_id)
    round_state_machine = RoundStateMachine(round_entity)
    round_state_machine.maybe_end_drawing_early()

    return jsonify({ 
        "imageId": drawing.ImageId,
        "roundId": drawing.RoundId,
        "imageBase64": drawing.ImageBase64
    })

@image_service.route("/images", methods=["GET"])
def get_drawings():
    round_id = int(request.args.get("roundId"))

    round_images = image_repository.get_round_images(round_id)
    images = [{ "imageId": ri.ImageId, "imageBase64": ri.ImageBase64, "userId": ri.UserId } 
                for ri in round_images]
    return jsonify(images)
#/usr/bin/python

import base64
import logging
import os
from flask import Blueprint, jsonify, request
from repositories import image_repository, round_repository
from round_state_machine import RoundStateMachine

logfile = logging.getLogger('file')
image_service = Blueprint('image_service', __name__)
data_dir = "../../../ui/public/data"

@image_service.route("/image", methods=["POST"])
def upload_drawing():
    user_id = int(request.args.get("userId"))
    round_id = int(request.args.get("roundId"))
    logfile.info("Adding drawing for user: %s for round: %s" % (user_id, round_id))
    drawing_base64 = request.get_json()["drawingBase64"]

    drawing_file_name = str(user_id) + ".png"
    drawing_folder = os.path.join(data_dir, str(round_id))
    drawing_file_path = os.path.join(drawing_folder, drawing_file_name)
    drawing_file_location = os.path.join(str(round_id), drawing_file_name)

    drawing_base64 = drawing_base64.replace("data:image/png;base64,", "")
    drawing_data = base64.b64decode(drawing_base64) 

    if not os.path.exists(drawing_folder):
        os.makedirs(drawing_folder) 
    with open(drawing_file_path, "wb") as fh: 
        fh.write(drawing_data)

    drawing = image_repository.create_image(user_id, drawing_file_location, round_id)

    round_entity = round_repository.get_round(round_id)
    round_state_machine = RoundStateMachine(round_entity)
    round_state_machine.maybe_end_drawing_early()

    return jsonify({ 
        "imageId": drawing.ImageId,
        "roundId": drawing.RoundId,
        "location": drawing.Location
    })

@image_service.route("/images", methods=["GET"])
def get_drawings():
    round_id = int(request.args.get("roundId"))

    round_images = image_repository.get_round_images(round_id)
    locations = [{ "imageId": ri.ImageId, "location": ri.Location } 
                for ri in round_images]
    return jsonify(locations)
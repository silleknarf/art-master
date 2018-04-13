#/usr/bin/python

from flask import Blueprint, jsonify, request

from database.database import session
from database.data_model import Image
import base64

image_service = Blueprint('image_service', __name__)
data_dir = "../../data"

#provide the image in the body
@image_service.route("/image", methods=["POST"])
def add_drawing():
    user_id = int(request.args.get("userId"))
    round_id = int(request.args.get("roundId"))
    drawing_base64 = request.form["drawingBase64"]

    drawing_file_name = round_id + "/" + user_id + ".png"
    drawing_file_path = data_dir + "/" + drawing_file_name
    with open(drawing_file_path, "wb") as fh:    
      fh.write(base64.decodebytes(drawing_base64))
    drawing = Image(
        UserId=user_id, 
        Location=drawing_file_name, 
        RoundId=round_id)
    session.add(drawing)
    session.commit()
    return ({ 
        "imageId": drawing.ImageId,
        "roundId": drawing.RoundId,
        "location": drawing.Location
    })

# returns two images to rate
@image_service.route("/images", methods=["GET"])
def get_drawings():
    round_id = int(request.args.get("roundId"))

    round_images = (session
        .query(Image)
        .filter(Image.RoundId==round_id)
        .all())
    locations = [(rt.RoundId, ri.Image.Location) for ri in round_images]
    if locations == 2:
        return jsonify(locations)
    return jsonify({})
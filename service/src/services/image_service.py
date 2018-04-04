#/usr/bin/python

from flask import Blueprint, jsonify, request

from database.database import Database
from database.data_model import Image, RoundImage

image_service = Blueprint('image_service', __name__)

#provide the image in the body
@image_service.route("/image", methods=["POST"])
def add_drawing():
    user_id = request.args.get("userId")
    round_id = request.args.get("roundId")
    drawing_file = request.files("drawing")

    drawing_file_name = round_id + "/" + user_id + ".png"
    f.save(data_dir + "/" + drawing_file_name);
    sesh = Database().get_session()
    drawing = Image(UserId=user_id, Location=drawing_file_name)
    sesh.add(drawing)
    sesh.flush()
    round_drawing = RoundImage(RoundId=round_id, ImageId=drawing.ImageId)
    sesh.commit()
    return ({ 
        "imageId": drawing.ImageId,
        "roundImageId": round_drawing.RoundImageId
    })

# returns two images to rate
@image_service.route("/images", methods=["GET"])
def get_drawings():
    round_id = request.args.get("roundId")

    sesh = Database().get_session()
    round_images = (sesh
        .query(RoundImage)
        .filter(RoundImage.RoundId==round_id)
        .all())
    locations = [(rt.RoundId, ri.Image.Location) for ri in round_images]
    if locations == 2:
        return jsonify(locations)
    return jsonify({})

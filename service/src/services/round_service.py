#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Image, RoundImage, Rating

round_service = Blueprint('round_service', __name__)

#provide the image in the body
@round_service.route("/round/<int:round_id>/image", methods=["POST"])
def add_drawing(round_id):
    user_id = request.args.get("userId")
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
@round_service.route("/round/<int:round_id>/images", methods=["GET"])
def get_drawings(round_id):
    sesh = Database().get_session()
    round_images = (sesh
        .query(RoundImage)
        .filter(RoundImage.RoundId==round_id)
        .all())
    locations = [(rt.RoundId, ri.Image.Location) for ri in round_images]
    if locations == 2:
        return jsonify(locations)
    return jsonify({})

# provides the round info including who won
@round_service.route("/round/<int:round_id>/ratings", methods=["GET"])
def get_round_info(round_id):
    sesh = Database().get_session()
    round_ratings = (sesh
        .query(Rating) 
        .join(Rating.RoundImage)
        .filter(Round.RoundId==round_id)
        .all())

    results = {}
    for rr in round_ratings:
        if rr.Rating != 0:
            if rr.ImageId in results:
                results[key] += 1
            else:
                results[key] = 1
    winner_image_id = None
    winner_rating = 0
    for image_id, rating in results:
        if rating >= winner_rating:
            winner_image_id = image_id
            winner_rating = rating

    winning_image_location = filter(
        lambda rr: rr.RoundImage.ImageId == winner_image_id,
        round_ratings)[0].Location

    round_info = { 
        "round_id": round_id,
        "winner_id": winner_id,
        "winning_image_location": winning_image_location
    }
    return jsonify(round_info)

# provide the rating
@round_service.route("/round/<int:round_id>/image/<int:image_id>/rating", methods=["POST"])
def provide_rating(round_id, image_id):
    rating = request.args.get("rating")
    user_id = request.args.get("raterUserId")
    rating_entity = Rating(Rating=rating, RaterUserId=raterUserId, ImageId=image_id)
    sesh = Database().get_session()
    sesh.add(rating_entity)
    sesh.commit()
    return jsonify({
        "ratingId", rating_entity.RatingId
    })
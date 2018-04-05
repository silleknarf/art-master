#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Round, Image, RoundImage, Rating

rating_service = Blueprint('rating_service', __name__)
        
# provides the round info including who won
@rating_service.route("/rating/round/<int:round_id>/ratings", methods=["GET"])
def get_ratings(round_id):
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
@rating_service.route("/rating/round/<int:round_id>/image/<int:image_id>/rating", methods=["POST"])
def set_rating(round_id, image_id):
    rating = request.args.get("rating")
    user_id = request.args.get("raterUserId")
    rating_entity = Rating(Rating=rating, RaterUserId=raterUserId, ImageId=image_id)
    sesh = Database().get_session()
    sesh.add(rating_entity)
    sesh.commit()
    return jsonify({
        "ratingId", rating_entity.RatingId
})
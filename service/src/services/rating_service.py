#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Round, Image, Rating

rating_service = Blueprint('rating_service', __name__)
        
# provides the round info including who won
@rating_service.route("/ratings", methods=["GET"])
def get_ratings():
    round_id = int(request.args.get("roundId"))
    sesh = Database().get_session()
    round_ratings = (sesh
        .query(Rating, Image) 
        .join(Image)
        .join(Round)
        .filter(Round.RoundId==round_id)
        .all())

    ratings = [rr[0] for rr in round_ratings]
    images = [rr[1] for rr in round_ratings]

    results = {}
    for rr in ratings:
        if rr.Rating != 0:
            if rr.ImageId in results:
                results[rr.ImageId] += 1
            else:
                results[rr.ImageId] = 1
    winner_image_id = None
    winner_rating = 0
    for image_id, rating in results.iteritems():
        if rating >= winner_rating:
            winner_image_id = image_id
            winner_rating = rating
    image = [image for image in images 
             if image.ImageId == winner_image_id][0]

    round_info = { 
        "round_id": round_id,
        "winner_id": image.UserId,
        "winning_image_location": image.Location
    }
    return jsonify(round_info)

# provide the rating
@rating_service.route("/rating", methods=["POST"])
def set_rating():
    image_id = int(request.args.get("imageId"))
    rating = int(request.args.get("rating"))
    user_id = int(request.args.get("raterUserId"))
    rating_entity = Rating(
        Rating=rating, 
        RaterUserId=user_id, 
        ImageId=image_id)
    sesh = Database().get_session()
    sesh.add(rating_entity)
    sesh.commit()
    return jsonify({
        "ratingId": rating_entity.RatingId
    })
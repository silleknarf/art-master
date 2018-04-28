#!/usr/bin/python

from flask import Blueprint, jsonify, request
from artmaster.repositories import rating_repository, user_repository
from exceptions import InvalidUsage

rating_service = Blueprint('rating_service', __name__)
        
# provides the round info including who won
@rating_service.route("/ratings", methods=["GET"])
def get_ratings():
    round_id = int(request.args.get("roundId"))
    round_ratings = rating_repository.get_ratings(round_id)

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

    winning_user = user_repository.get_user(image.UserId)
        
    round_info = { 
        "roundId": round_id,
        "winnerId": winning_user.UserId,
        "winnerUsername": winning_user.Username,
        "winningImageLocation": image.Location
    }
    return jsonify(round_info)

# provide the rating
@rating_service.route("/rating", methods=["POST"])
def set_rating():
    image_id = int(request.args.get("imageId"))
    rating = int(request.args.get("rating"))
    user_id = int(request.args.get("raterUserId"))
    has_existing_rating = rating_repository.has_existing_rating(image_id, user_id)
        
    if is_existing_rating:
        error_text = "Cannot rate more than one image per round"
        raise InvalidUsage(error_text)
    rating_entity = rating_repository.create_rating(image_id, rating, user_id)
    return jsonify({
        "ratingId": rating_entity.RatingId
    })
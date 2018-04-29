#!/usr/bin/python

from repositories import rating_repository
from repositories import user_repository
from flask import Blueprint, jsonify, request
from exceptions import InvalidUsage

rating_service = Blueprint('rating_service', __name__)

# provides the round info including who won
@rating_service.route("/ratings", methods=["GET"])
def get_ratings():
    round_id = int(request.args.get("roundId"))
    round_ratings = rating_repository.get_ratings(round_id)

    if len(round_ratings) == 0:
        return jsonify([])

    ratings = [rr[0] for rr in round_ratings]
    images = [rr[1] for rr in round_ratings]

    results = {}
    for rr in ratings:
        if rr.Rating != 0:
            if rr.ImageId in results:
                results[rr.ImageId] += 1
            else:
                results[rr.ImageId] = 1

    winning_image_ids = []
    winning_rating = 0
    for image_id, rating in results.iteritems():
        if rating == winning_rating:
            winning_image_ids.append(image_id)
        elif rating >= winning_rating:
            winning_image_ids = [image_id]
            winning_rating = rating

    winning_images = []
    for winning_image_id in winning_image_ids:
        winning_image = [i for i in images if i.ImageId == winning_image_id][0]
        winning_images.append(winning_image)

    results = []
    for winning_image in winning_images:
        winning_user = user_repository.get_user(winning_image.UserId)
        result = { 
            "roundId": round_id,
            "winnerId": winning_user.UserId,
            "winnerUsername": winning_user.Username,
            "winningImageLocation": winning_image.Location,
        }
        results.append(result)

    return jsonify(results)

# provide the rating
@rating_service.route("/rating", methods=["POST"])
def set_rating():
    image_id = int(request.args.get("imageId"))
    rating = int(request.args.get("rating"))
    user_id = int(request.args.get("raterUserId"))
    has_existing_rating = rating_repository.has_existing_rating(image_id, user_id)
        
    if has_existing_rating:
        error_text = "Cannot rate more than one image per round"
        raise InvalidUsage(error_text)
    rating_entity = rating_repository.create_rating(image_id, rating, user_id)
    return jsonify({
        "ratingId": rating_entity.RatingId
    })
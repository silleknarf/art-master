#!/usr/bin/python

from flask import Blueprint, jsonify, request
from artmaster.database.database import session
from artmaster.database.data_model import Round, Image, Rating
from exceptions import InvalidUsage

rating_service = Blueprint('rating_service', __name__)
        
# provides the round info including who won
@rating_service.route("/ratings", methods=["GET"])
def get_ratings():
    round_id = int(request.args.get("roundId"))
    round_ratings = (session
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

    winning_user = (session
        .query(User)
        .filter(User.UserId==image.UserId)
        .first())
        
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
    round_id = (session
        .query(Image)
        .filter(Image.ImageId==image_id)
        .first()
        .RoundId)
    is_existing_rating = (session
        .query(Rating)
        .join(Image)
        .filter(Image.RoundId==round_id)
        .any())
        
    if is_existing_rating:
        error_text = "Cannot rate more than one image per round"
        raise InvalidUsage(error_text)
    rating_entity = Rating(
        Rating=rating, 
        RaterUserId=user_id, 
        ImageId=image_id)
    session.add(rating_entity)
    session.commit()
    return jsonify({
        "ratingId": rating_entity.RatingId
    })
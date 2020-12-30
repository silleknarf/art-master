#!/usr/bin/python

from repositories import rating_repository, image_repository, user_repository, entry_repository
from flask import Blueprint, jsonify, request
from .exceptions import InvalidUsage
from services.round_state_machine import RoundStateMachine
import logging

logfile = logging.getLogger('file')

rating_service = Blueprint('rating_service', __name__)

# provides the round info including who won
@rating_service.route("/ratings", methods=["GET"])
def get_ratings():
    round_id = int(request.args.get("roundId"))
    ratings = rating_repository.get_round_rating_results(round_id)
    return jsonify(ratings)

# provide the rating
@rating_service.route("/rating", methods=["POST"])
def set_rating():
    image_id_raw = request.args.get("imageId")
    image_id = int(image_id_raw) if image_id_raw is not None and image_id_raw.isdigit() else None
    entry_id_raw = request.args.get("entryId")
    entry_id = int(entry_id_raw) if entry_id_raw is not None and entry_id_raw.isdigit() else None
    rating = int(request.args.get("rating"))
    user_id = int(request.args.get("raterUserId"))
    round_id = int(request.args.get("roundId"))

    has_existing_rating = rating_repository.has_existing_rating(round_id, user_id)

    if has_existing_rating:
        error_text = "Cannot rate more than one thing per round"
        raise InvalidUsage(error_text)
    rating_entity = rating_repository.create_rating(image_id, entry_id, round_id, rating, user_id)

    round_entity = None
    if image_id is not None:
        round_entity = image_repository.get_round(image_id)
    else:
        round_entity = entry_repository.get_round(entry_id)

    round_state_machine = RoundStateMachine(round_entity)
    round_state_machine.maybe_end_critiquing_early()

    return jsonify({
        "ratingId": rating_entity.RatingId
    })

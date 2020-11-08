#!/usr/bin/python

import logging
from flask import Blueprint, request
from repositories import round_repository, word_repository
from .exceptions import InvalidUsage
from .round_state_machine import RoundStateMachine, run_round
from utils.round_utils import to_round_dto

round_service = Blueprint('round_service', __name__)
logfile = logging.getLogger("file")

# Create a new round and then returns the round info
@round_service.route("/round", methods=["GET", "POST"])
def create_round():
    round_entity = None
    if request.method == "POST":
        room_id = int(request.args.get("roomId"))
        user_id = int(request.args.get("userId"))
        word = word_repository.get_random_word_for_room(room_id)
        if word is None:
            raise InvalidUsage("Cannot start around without any words")
        round_entity = round_repository.create_round(room_id, user_id, word.WordId)
        run_round.apply_async(kwargs={"round_id": round_entity.RoundId})
    else:
        round_id = request.args.get("roundId")
        round_entity = round_repository.get_round(round_id)

    return to_round_dto(round_entity)

#!/usr/bin/python

import logging
from flask import Blueprint, jsonify, request
from repositories import round_repository
from datetime import datetime, timedelta

round_service = Blueprint('round_service', __name__)
logfile = logging.getLogger("file")

# Create a new round and then returns the round info
@round_service.route("/round", methods=["GET", "POST"])
def poll_or_create_round():
    if request.method == "POST":
        room_id = int(request.args.get("roomId"))
        user_id = int(request.args.get("userId"))
        round_entity = round_repository.create_round(room_id, user_id)
        update_stage(round_entity)
    else:
        round_id = request.args.get("roundId")
        round_entity = round_repository.get_round(round_id)
        maybe_update_stage(round_entity)
    
    return to_round_dto(round_entity)
    
def to_round_dto(round_entity):
    return jsonify({
        "roundId": round_entity.RoundId,
        "stageStateId": round_entity.StageStateId,
        "timeRemaining": get_time_remaining(round_entity)     
    })
    
def get_time_remaining(round_entity):
    time_remaining = None
    if round_entity.StageStateStartTime is not None and \
       round_entity.StageStateEndTime is not None:
       time_remaining = (round_entity.StageStateEndTime - datetime.utcnow()).total_seconds()
    return time_remaining

def maybe_update_stage(round_entity):
    time_remaining = get_time_remaining(round_entity)
    if time_remaining <= 0:
        update_stage(round_entity)

# stages = ["Drawing", "Critiquing", "Reviewing", "Done"]       
def update_stage(round_entity):
    duration = 0
    stage_state_id = round_entity.StageStateId
    if stage_state_id == None:
        stage_state_id = 0      
        duration = 10
        round_repository.update_room_round(round_entity.RoomId, round_entity.RoundId)
    elif stage_state_id == 0:
        stage_state_id += 1
        duration = 10
    elif stage_state_id == 1:
        stage_state_id += 1
        duration = 20
    elif stage_state_id == 2:
        duration = 0
        round_repository.update_room_round(round_entity.RoomId, None)

    start_time = datetime.utcnow()
    end_time = start_time + timedelta(seconds=duration)
    round_repository.update_round(round_entity.RoundId, stage_state_id, start_time, end_time)
    

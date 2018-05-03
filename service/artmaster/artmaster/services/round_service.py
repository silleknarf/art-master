#!/usr/bin/python

import logging
from flask import Blueprint, jsonify, request
from repositories import round_repository, word_repository
from datetime import datetime, timedelta
from exceptions import InvalidUsage

round_service = Blueprint('round_service', __name__)
logfile = logging.getLogger("file")

# Create a new round and then returns the round info
@round_service.route("/round", methods=["GET", "POST"])
def poll_or_create_round():
    if request.method == "POST":
        room_id = int(request.args.get("roomId"))
        user_id = int(request.args.get("userId"))
        word = word_repository.get_random_word_for_room(room_id)
        if word is None:
            raise InvalidUsage("Cannot start around without any words")
        round_entity = round_repository.create_round(room_id, user_id, word.WordId)
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
        "timeRemaining": get_time_remaining(round_entity),
        "drawingWordId": round_entity.DrawingWordId
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

class RoundStateMachine:
    stages = ["Drawing", "Critiquing", "Reviewing", "Done"]       

    def __init__(self, round_id, drawing_word_id):
        self.round_id = round_id
        self.drawing_word_id = drawing_word_id

    def to_drawing(self):
        stage_state_id = 0      
        duration = 45
        round_repository.update_room_round(round_entity.RoomId, round_entity.RoundId)
        self.update_round(stage_state_id, duration)

    def to_critiquing(self):
        stage_state_id = 1
        duration = 15
        self.update_round(stage_state_id, duration)

    def to_reviewing(self):
        stage_state_id = 2
        duration = 10
        self.update_round(stage_state_id, duration)

    def to_done(self):
        stage_state_id = 3
        duration = 0
        word_id_to_remove = drawing_word_id
        self.drawing_word_id = None
        round_repository.update_room_round(round_entity.RoomId, None)
        self.update_round(stage_state_id, duration)
        word_repository.remove_word(word_id_to_remove)

    def update_round(self, stage_state_id, duration):
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=duration)
        round_repository.update_round(
            self.round_id,
            stage_state_id, 
            start_time, 
            end_time, 
            self.drawing_word_id)

    def next_stage(self, stage_state_id):
        if stage_state_id is None:
            self.to_drawing()
        elif self.stages[stage_state_id] == "Drawing":
            self.to_critiquing()
        elif self.stages[stage_state_id] == "Critiquing":
            self.to_reviewing()
        elif self.stages[stage_state_id] == "Reviewing":
            self.to_done()

def update_stage(round_entity):
    duration = 0
    stage_state_id = round_entity.StageStateId
    drawing_word_id = round_entity.DrawingWordId
    word_id_to_remove = None
    if stage_state_id == None:
        stage_state_id = 0      
        duration = 45
        round_repository.update_room_round(round_entity.RoomId, round_entity.RoundId)
    elif stage_state_id == 0:
        stage_state_id += 1
        duration = 15
    elif stage_state_id == 1:
        stage_state_id += 1
        duration = 10
    elif stage_state_id == 2:
        stage_state_id += 1
        duration = 0
        word_id_to_remove = drawing_word_id
        drawing_word_id = None
        round_repository.update_room_round(round_entity.RoomId, None)

    start_time = datetime.utcnow()
    end_time = start_time + timedelta(seconds=duration)
    round_repository.update_round(
        round_entity.RoundId, 
        stage_state_id, 
        start_time, 
        end_time, 
        drawing_word_id)
        
    if stage_state_id == 3:
        word_repository.remove_word(word_id_to_remove)
    

#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Room, Round, RoomUser
from random import randint
from datetime import datetime

room_service = Blueprint('room_service', __name__)

# Create a new round and then returns the round info
@room_service.route("/room/<room_id>/round", methods=["GET", "POST"])
def create_round(room_id):
    sesh = Database().get_session()
    round = None
    if request.method == "GET":
        current_round_id = (sesh
            .query(Room)
            .filter(Room.RoomId==room_id)
            .first()
            .CurrentRoundId)
        round = (sesh
            .query()
            .filter(Round.RoundId==current_round_id)
            .order_by(Room.StartTime)
            .first())
    else:
        room = (sesh
            .query(Room)
            .filter(Room.RoomId==room_id)
            .first())
        start_time = datetime.utcnow()
        round = Round(RoomId=room_id, StartTime=start_time)
        sesh.add(round)
        sesh.flush() 
        room.CurrentRoundId = round.RoundId
        sesh.commit()
    start_time = round.StartTime.isoformat() + 'Z'
    return jsonify({ 
        "roundId": round.RoundId,
        "startTime": start_time
    })
    
@room_service.route("/room", methods=["GET", "POST"])
def get_or_create_room():
    sesh = Database().get_session() 
    room = None

    if request.method == "GET":
        roomCode = request.args.get("roomCode")
        room = (sesh.query(Room)
            .filter(Room.RoomCode==roomCode)
            .first())
    else:
        roomCode = get_room_code()
        room = Room(RoomCode=roomCode)
        sesh.add(room)
        sesh.commit()

    return jsonify({
        "roomId": room.RoomId,
        "roomCode": room.RoomCode,
        "currentRoundId": room.CurrentRoundId
    })

@room_service.route("/room/<int:room_id>/user/<int:user_id>", methods=["POST"])
def add_user_to_room(room_id, user_id):
    sesh = Database().get_session()
    room_user = RoomUser(RoomId=room_id, UserId=user_id)
    sesh.add(room_user)
    sesh.commit()
    return jsonify({})

def get_room_code():
    first_chr = 65
    return "".join([chr(first_chr+randint(0, 25)) for i in range(0, 4)])
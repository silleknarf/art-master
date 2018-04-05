#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Room, Round, RoomUser
from random import randint
from datetime import datetime

room_service = Blueprint('room_service', __name__)
            
@room_service.route("/room", methods=["GET", "POST"])
def poll_or_create_room():
    sesh = Database().get_session() 
    room = None

    if request.method == "GET":
        room_code = request.args.get("roomCode")
        room_id = request.args.get("roomId")
        room = None
        if room_id is not None:
            room = (sesh.query(Room)
                .filter(Room.RoomId==room_id)
                .first())
        elif room_code is not None:
            room = (sesh.query(Room)
                .filter(Room.RoomCode==room_code)
                .first())
        elif room_id is None and room_code is None:
            return "Please set the room id or code"
        else:
            return "Room code or room id doesn't exist"
    else:
        owner_user_id = request.args.get("userId")
        roomCode = get_room_code()
        room = Room(RoomCode=roomCode, OwnerUserId=owner_user_id)
        sesh.add(room)
        sesh.commit()
        add_user_to_room(room.RoomId, owner_user_id)

    return jsonify({
        "roomId": room.RoomId,
        "roomCode": room.RoomCode,
        "roomOwnerId": room.OwnerUserId,
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
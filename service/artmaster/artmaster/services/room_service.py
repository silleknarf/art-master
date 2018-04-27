#!/usr/bin/python

from flask import Blueprint, jsonify, request
from artmaster.database.database import session
from artmaster.database.data_model import Room, Round, RoomUser, User
from random import randint
from datetime import datetime
from exceptions import InvalidUsage
import logging

logfile = logging.getLogger('file')

room_service = Blueprint('room_service', __name__)
            
@room_service.route("/room", methods=["GET", "POST"])
def poll_or_create_room():
    room = None

    if request.method == "GET":
        room_code = request.args.get("roomCode")
        room_id = request.args.get("roomId")
        room = None
        if room_id is not None:
            room = (session.query(Room)
                .filter(Room.RoomId==int(room_id))
                .first())
        elif room_code is not None:
            room = (session.query(Room)
                .filter(Room.RoomCode==room_code)
                .first())
        elif room_id is None and room_code is None:
            error_text = "Please set the room id or code"
            raise InvalidUsage(error_text)
        else:
            error_text = "Room code or room id doesn't exist"
            raise InvalidUsage(error_text)
    else:
        owner_user_id = int(request.args.get("userId"))
        roomCode = get_room_code()
        info_text = "Creating room: %s for %s" % (roomCode, owner_user_id)
        logfile.info(info_text)
        room = Room(RoomCode=roomCode, OwnerUserId=owner_user_id)
        session.add(room)
        session.commit()
        add_user_to_room(room.RoomId, owner_user_id)

    return jsonify({
        "roomId": room.RoomId,
        "roomCode": room.RoomCode,
        "roomOwnerId": room.OwnerUserId,
        "currentRoundId": room.CurrentRoundId
    })

@room_service.route("/room/<int:room_id>/user/<int:user_id>", methods=["POST"])
def add_user_to_room(room_id, user_id):
    logfile.info("Adding user: %s to room: %s" % (user_id, room_id))
    room_user = RoomUser(RoomId=room_id, UserId=user_id)
    session.add(room_user)
    session.commit()
    return jsonify({})

@room_service.route("/room/<int:room_id>/users", methods=["GET"])
def get_users_in_room(room_id):
    room_user_entities = (session
        .query(User)
        .join(RoomUser)
        .filter(RoomUser.RoomId==room_id)
        .all())
    room_users = [{"userId": u.UserId, "username": u.Username }
                  for u in room_user_entities]
    return jsonify(room_users)

def get_room_code():
    first_chr = 65
    return "".join([chr(first_chr+randint(0, 25)) for i in range(0, 4)])
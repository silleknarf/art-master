#!/usr/bin/python

import logging
from app import socketio
from flask import Blueprint, jsonify, request
from repositories import room_user_repository, room_repository
from random import SystemRandom
from datetime import datetime
from .exceptions import InvalidUsage
from utils.room_utils import to_room_dto, to_room_dict
from flask_socketio import join_room

logfile = logging.getLogger('file')

randint = SystemRandom().randint

room_service = Blueprint('room_service', __name__)

@room_service.route("/room", methods=["GET", "POST"])
def get_or_create_room():
    room = None

    if request.method == "GET":
        room_id = request.args.get("roomId")
        room_id = int(room_id) if room_id is not None else None
        room_code = request.args.get("roomCode")
        room = room_repository.get_room(room_id, room_code)
    else:
        owner_user_id = int(request.args.get("userId"))
        room_code = get_room_code()
        room = room_repository.create_room(room_code, owner_user_id)
        room_user_repository.add_user_to_room(room.RoomId, owner_user_id)

    return to_room_dto(room)

@room_service.route("/room/<int:room_id>/user/<int:user_id>", methods=["POST"])
def add_user_to_room(room_id, user_id):
    room_user_repository.add_user_to_room(room_id, user_id)
    return ""

@room_service.route("/room/<int:room_id>/user/<int:user_id>", methods=["DELETE"])
def remove_user_from_room(room_id, user_id):
    room_user_repository.remove_user_from_room(room_id, user_id)
    return ""

@room_service.route("/room/<int:room_id>/minigame/<int:minigame_id>", methods=["POST"])
def set_minigame(room_id, minigame_id):
    room_repository.set_minigame(room_id, minigame_id)
    return ""

@room_service.route("/room/<int:room_id>/users", methods=["GET"])
def get_users_in_room(room_id):
    room_user_entities = room_user_repository.get_users_in_room(room_id)
    room_users = [{"userId": u.UserId, "username": u.Username, "score": u.Score }
                  for u in room_user_entities]
    return jsonify(room_users)

def get_room_code():
    first_chr = 65
    return "".join([chr(first_chr+randint(0, 25)) for i in range(0, 4)])

@socketio.on('join')
def on_join(room_id):
    join_room(str(room_id))
    logfile.info("Room: %s being joined", room_id)
    room = room_repository.get_room(room_id, None)
    socketio.emit("room", to_room_dict(room), room=str(room_id))

import logging
from database.database import session
from database.data_model import Room, RoomUser, User
from services.exceptions import InvalidUsage
from utils.room_utils import to_room_dict
from app import socketio

logfile = logging.getLogger("file")

def create_room(room_code):
    logfile.info("Creating room: %s", room_code)
    room = Room(RoomCode=room_code)
    session.add(room)
    session.commit()
    room.RoomUsers = []
    socketio.emit("room", to_room_dict(room), room=str(room.RoomId))
    return room

def get_room(room_id, room_code):
    room = None
    if room_id is not None:
        room = (session.query(Room)
            .populate_existing()
            .filter(Room.RoomId==room_id)
            .first())
    elif room_code is not None:
        room = (session.query(Room)
            .filter(Room.RoomCode==room_code)
            .first())
    elif room_id is None and room_code is None:
        error_text = "Please provide a room id or code"
        raise InvalidUsage(error_text)
    else:
        error_text = "Room code or room not specified"
        raise InvalidUsage(error_text)

    if room is not None:
        room_users = (session
            .query(User)
            .populate_existing()
            .join(RoomUser)
            .filter(RoomUser.RoomId==room.RoomId)
            .all())
        room.RoomUsers = room_users
    return room

def update_room_round(room_id, round_id):
    logfile.info("Updating room: %s to be on round: %s", room_id, round_id)
    room = get_room(room_id=room_id, room_code=None)
    room.CurrentRoundId = round_id
    session.commit()
    socketio.emit("room", to_room_dict(room), room=str(room_id))

def get_number_of_players(room_id):
    number_of_players = len(get_room(room_id, None).RoomUsers)
    return number_of_players

def set_minigame(room_id, minigame_id):
    room = get_room(room_id=room_id, room_code=None)
    room.MinigameId = minigame_id
    session.commit()
    socketio.emit("room", to_room_dict(room), room=str(room_id))

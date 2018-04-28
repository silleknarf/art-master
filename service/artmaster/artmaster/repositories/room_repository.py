from artmaster.database.database import session
from artmaster.database.data_model import Room
import logging
logfile = logging.getLogger('file')

def create_room(room_code, owner_user_id):
    info_text = "Creating room: %s for %s" % (room_code, owner_user_id)
    logfile.info(info_text)
    room = Room(RoomCode=room_code, OwnerUserId=owner_user_id)
    session.add(room)
    session.commit()
    return room

def get_room(room_id, room_code):
    room = None
    if room_id is not None:
        room = (session.query(Room)
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
        error_text = "Room code or room id doesn't exist"
        raise InvalidUsage(error_text)
    return room
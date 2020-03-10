from database.database import session
from database.data_model import RoomUser, User
import logging

logfile = logging.getLogger('file')

def add_user_to_room(room_id, user_id):
    logfile.info("Adding user: %s to room: %s" % (user_id, room_id))
    room_user = RoomUser(RoomId=room_id, UserId=user_id)
    session.add(room_user)
    session.commit()

def remove_user_from_room(room_id, user_id):
    logfile.info("Removing user: %s from room: %s" % (user_id, room_id))
    room_user_entity = (session
        .query(RoomUser)
        .filter(RoomUser.RoomId==room_id)
        .filter(RoomUser.UserId==user_id)
        .first())
    session.delete(room_user_entity)
    session.commit()

def get_users_in_room(room_id):
    room_user_entities = (session
        .query(User)
        .join(RoomUser)
        .filter(RoomUser.RoomId==room_id)
        .all())
    return room_user_entities
from artmaster.database.database import session
from artmaster.database.data_model import RoomUser
import logging

logfile = logging.getLogger('file')

def add_user_to_room(room_id, user_id):
    logfile.info("Adding user: %s to room: %s" % (user_id, room_id))
    room_user = RoomUser(RoomId=room_id, UserId=user_id)
    session.add(room_user)
    session.commit()

def get_users_in_room(room_id):
    room_user_entities = (session
        .query(User)
        .join(RoomUser)
        .filter(RoomUser.RoomId==room_id)
        .all())
    return room_user_entities
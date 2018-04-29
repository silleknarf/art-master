from database.database import session
from database.data_model import Room, Round
import logging

logfile = logging.getLogger('file')

def update_room_round(room_id, round_id):
    room = (session
        .query(Room)
        .filter(Room.RoomId==room_id)
        .first())
    room.CurrentRoundId = round_id

def create_round(room_id, user_id):
    logfile.info(
        "Creating room: %s for user: %s" %
        (room_id, user_id))
    if room_id is None or user_id is None:
        return "Please set the roomId and userId"
    room = (session
        .query(Room)
        .filter(Room.RoomId==room_id)
        .first())
    if room.OwnerUserId != user_id:
        return "Only the room owner can start rounds"
    round_entity = Round(RoomId=room_id)
    session.add(round_entity)
    session.commit() 
    return round_entity

def get_round(round_id):
    round_entity = (session
        .query(Round)
        .filter(Round.RoundId==round_id)
        .first())

    if round_entity is None:
        return "No round for given roundId"
    return round_entity

def update_round(round_id, stage_state_id, start_time, end_time):
    logfile.info("Setting round: %s to be in state: %s" %
        (round_id, stage_state_id))

    round_entity = get_round(round_id)
    round_entity.StageStateId = stage_state_id
    round_entity.StageStateStartTime = start_time
    round_entity.StageStateEndTime = end_time

    session.commit()
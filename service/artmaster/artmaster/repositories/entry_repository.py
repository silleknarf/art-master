import logging
from random import SystemRandom
from sqlalchemy.exc import IntegrityError
from app import socketio
from database.database import session
from database.data_model import Entry, EntryComponent, Round, Room
from repositories import round_repository, room_user_repository
from services.round_state_machine import RoundStateMachine
from utils.entry_utils import to_entries_dto

logfile = logging.getLogger('file')

randint = SystemRandom().randint

def get_random_entry_for_room(room_id):
    room_entity = session.query(Room).filter(Room.RoomId==room_id).first()
    entry_entities = (session
        .query(Entry)
        .filter(Entry.RoomId==room_id)
        .filter(Entry.RoundId==None)
        .filter(Entry.MinigameId==room_entity.MinigameId)
        .all())
    if len(entry_entities) == 0:
        return None

    random_entry_entity = entry_entities[randint(0, len(entry_entities)-1)]

    return random_entry_entity

def remove_entry(entry_id):
    logfile.info("Removing entry with id: %s", entry_id)
    if entry_id is None:
        return
    entry_entity = (session
        .query(Entry)
        .filter(Entry.EntryId==entry_id)
        .first())
    session.delete(entry_entity)
    session.commit()
    push_entries_for_entry_change(entry_entity.RoomId)

def create_entry(room_id, user_id, round_id, entry_components):
    room_entity = session.query(Room).filter(Room.RoomId==room_id).first()
    try:
        entry_entity = Entry(
            RoomId=room_id,
            UserId=user_id,
            RoundId=round_id,
            MinigameId=room_entity.MinigameId)
        session.add(entry_entity)
        session.commit()

        for key, value in entry_components:
            trimmed_value = value.strip()
            if trimmed_value == "":
                continue
            entry_component_entity = EntryComponent(
                EntryId=entry_entity.EntryId,
                Key=key,
                Value=trimmed_value)
            session.add(entry_component_entity)

        session.commit()

        push_entries_for_entry_change(room_id, round_id)
    except IntegrityError:
        session.rollback()
        return

    if round_id is not None:
        round_entity = round_repository.get_round(round_id)
        round_state_machine = RoundStateMachine(round_entity)
        round_state_machine.maybe_end_submitting_entries_early()

    return entry_entity

def get_entries(room_id, round_id):
    room_entity = (session.query(Room)
        .filter(Room.RoomId==room_id)
        .first())
    entry_entities = (session.query(Entry)
        .filter(Entry.RoomId==room_id)
        .filter(Entry.RoundId==round_id)
        .filter(Entry.MinigameId==room_entity.MinigameId)
        .all())
    return entry_entities

def are_all_entries_submitted(room_id, round_id):
    round_sentences_count = len(get_entries(room_id, round_id))
    room_users_count = len(room_user_repository.get_users_in_room(room_id))
    logfile.info("Entries submitted: %s", round_sentences_count)
    return round_sentences_count == room_users_count

def get_entry(entry_id):
    entry = (session.query(Entry)
        .filter(Entry.EntryId==entry_id)
        .first())
    return entry

def get_entry_components(entry_entities):
    entry_ids = [e.EntryId for e in entry_entities]
    entry_components = (session.query(EntryComponent)
        .filter(EntryComponent.EntryId.in_(entry_ids))
        .all())
    return entry_components

def get_round(entry_id):
    round_entity = (session.query(Round)
        .populate_existing()
        .join(Entry)
        .filter(Entry.EntryId==entry_id)
        .first())
    return round_entity

def set_player_round_entries(room_id, round_id, user_entries):
    for user_entry in user_entries:
        user_id = user_entry["userId"]
        entry = user_entry["entry"]
        # Convert a dict to anonymous obj
        entry_components = [type("", (), e)() for e in entry]
        create_entry(room_id, user_id, round_id, entry_components)

def push_entries_for_entry_change(room_id, round_id=None):
    entry_entities = get_entries(room_id=room_id, round_id=round_id)
    entry_component_entities = get_entry_components(entry_entities)
    logfile.info("Pushing %s entries for room id: %s", len(entry_entities), room_id)
    socketio.emit(
        "entries",
        to_entries_dto(entry_entities, entry_component_entities),
        room=str(room_id))

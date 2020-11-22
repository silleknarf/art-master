import logging
from random import SystemRandom
from sqlalchemy.exc import IntegrityError
from app import socketio
from database.database import session
from database.data_model import Word, Round, Room
from repositories import round_repository, room_user_repository
from services.round_state_machine import RoundStateMachine
from utils.word_utils import to_words_dict

logfile = logging.getLogger('file')

randint = SystemRandom().randint

def get_random_word_for_room(room_id):
    room_entity = session.query(Room).filter(Room.RoomId==room_id).first()
    word_entities = (session
        .query(Word)
        .filter(Word.RoomId==room_id)
        .filter(Word.RoundId==None)
        .filter(Word.MinigameId==room_entity.MinigameId)
        .all())
    if len(word_entities) == 0:
        return None

    random_word_entity = word_entities[randint(0, len(word_entities)-1)]

    return random_word_entity

def remove_word(word_id):
    logfile.info("Removing word with id: %s", word_id)
    if word_id is None:
        return
    word_entity = (session
        .query(Word)
        .filter(Word.WordId==word_id)
        .first())
    session.delete(word_entity)
    session.commit()
    push_words_for_word_change(word_entity.RoomId)

def create_word(room_id, user_id, round_id, word):
    trimmed_word = word.strip()
    if trimmed_word == "":
        return
    room_entity = session.query(Room).filter(Room.RoomId==room_id).first()
    word_entity = Word(
        RoomId=room_id,
        UserId=user_id,
        RoundId=round_id,
        MinigameId=room_entity.MinigameId,
        Word=trimmed_word)
    session.add(word_entity)
    try:
        session.commit()
        push_words_for_word_change(room_id)
    except IntegrityError:
        session.rollback()
        return

    if round_id is not None:
        round_entity = round_repository.get_round(round_id)
        round_state_machine = RoundStateMachine(round_entity)
        round_state_machine.maybe_end_submitting_sentences_early()

    return word_entity

def get_words(room_id, round_id):
    room_entity = (session.query(Room)
        .filter(Room.RoomId==room_id)
        .first())
    word_entities = (session.query(Word)
        .filter(Word.RoomId==room_id)
        .filter(Word.RoundId==round_id)
        .filter(Word.MinigameId==room_entity.MinigameId)
        .all())
    return word_entities

def are_all_sentences_submitted(room_id, round_id):
    round_sentences_count = len(get_words(room_id, round_id))
    room_users_count = len(room_user_repository.get_users_in_room(room_id))
    logfile.info("Sentences submitted: %s", round_sentences_count)
    return round_sentences_count == room_users_count

def get_word(word_id):
    word = (session.query(Word)
        .filter(Word.WordId==word_id)
        .first())
    return word

def get_round(word_id):
    round_entity = (session.query(Round)
        .populate_existing()
        .join(Word)
        .filter(Word.WordId==word_id)
        .first())
    return round_entity

def push_words_for_word_change(room_id):
    word_entities = get_words(room_id=room_id, round_id=None)
    logfile.info("Pushing %s words for room id: %s", len(word_entities), room_id)
    socketio.emit("words", to_words_dict(word_entities), room=str(room_id))

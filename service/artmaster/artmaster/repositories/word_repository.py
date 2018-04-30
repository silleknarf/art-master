from database.database import session
from database.data_model import Word
from random import randint
import logging

logfile = logging.getLogger('file')

def get_random_word_for_room(room_id):
    word_entities = (session
        .query(Word)
        .filter(Word.RoomId==room_id)
        .all())
    if len(word_entities) == 0:
        return None

    random_word_entity = word_entities[randint(0, len(word_entities)-1)]

    return random_word_entity

def remove_word(word_id):
    logfile.info("Removing word with id: %s" % (word_id))
    if word_id is None:
        return
    word_entity = (session
        .query(Word)
        .filter(Word.WordId==word_id)
        .delete(synchronize_session=False))
    session.commit()

def create_word(room_id, user_id, word):
    trimmed_word = word.strip()
    if trimmed_word == "":
        return
    existing_word = (session
        .query(Word)
        .filter(Word.RoomId==room_id)
        .filter(Word.Word==trimmed_word)
        .first())
    if existing_word is not None:
        return 
    word_entity = Word(RoomId=room_id, UserId=user_id, Word=trimmed_word)
    session.add(word_entity)
    session.commit()
    return word_entity

def remove_word(word_id):
    word_entity = (session
        .query(Word)
        .filter(Word.WordId==word_id)
        .first())
    session.delete(word_entity)
    session.commit()

def get_words(room_id):
    word_entities = (session.query(Word)
        .filter(Word.RoomId==room_id)
        .all())
    return word_entities

def get_word(word_id):
    word = (session.query(Word)
        .filter(Word.WordId==word_id)
        .first())
    return word

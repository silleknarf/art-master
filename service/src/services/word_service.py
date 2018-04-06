#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Word

word_service = Blueprint('word_service', __name__)
            
@word_service.route("/word", methods=["POST", "DELETE"])
def add_or_remove_word():
    sesh = Database().get_session()
    if request.method == "POST":
        room_id = int(request.args.get("roomId"))
        user_id = int(request.args.get("userId"))
        word = request.args.get("word")
        existing_word = (sesh
            .query(Word)
            .filter(Word.Word==word)
            .first())
        if existing_word is not None:
            return "Can't re-add existing word"
        word_entity = Word(RoomId=room_id, UserId=user_id, Word=word)
        sesh.add(word_entity)
    elif request.method == "DELETE":
        word_id = int(request.args.get("wordId"))
        word_entity = (sesh
            .query(Word)
            .filter(Word.WordId==word_id)
            .first())
        sesh.delete(word_entity)

    sesh.commit()
    return jsonify({})

@word_service.route("/words", methods=["GET"])
def get_words():
    sesh = Database().get_session()
    room_id = int(request.args.get("roomId"))
    word_entities = (sesh.query(Word)
        .filter(Word.RoomId==room_id)
        .all())
    words = [{ 
        "wordId": w.WordId, 
        "userId": w.UserId,
        "word": w.Word
    } for w in word_entities]
    return jsonify(words)



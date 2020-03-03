#!/usr/bin/python

from flask import Blueprint, jsonify, request
from repositories import word_repository
from services.exceptions import InvalidUsage

word_service = Blueprint('word_service', __name__)
            
@word_service.route("/word", methods=["POST", "DELETE"])
def add_or_remove_word():
    if request.method == "POST":
        room_id = int(request.args.get("roomId"))
        user_id = int(request.args.get("userId"))
        round_id_raw = request.args.get("roundId")
        round_id = int(round_id_raw) if round_id_raw.isdigit() else None
        word = request.args.get("word")
        word_repository.create_word(room_id, user_id, round_id, word)
    elif request.method == "DELETE":
        word_id = int(request.args.get("wordId"))
        word_repository.remove_word(word_id)

    return ""

@word_service.route("/words", methods=["GET"])
def get_words():
    room_id = int(request.args.get("roomId"))
    round_id_raw = request.args.get("roundId")
    round_id = int(round_id_raw) if round_id_raw.isdigit() else None
    word_entities = word_repository.get_words(room_id, round_id)
    words = [{ 
        "wordId": w.WordId, 
        "userId": w.UserId,
        "word": w.Word
    } for w in word_entities]
    return jsonify(words)

@word_service.route("/word", methods=["GET"])
def get_word():
    word_id = int(request.args.get("wordId"))
    w = word_repository.get_word(word_id)
    word = { 
        "wordId": w.WordId, 
        "userId": w.UserId,
        "word": w.Word
    } 
    return jsonify(word)

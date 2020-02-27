from flask import Blueprint, jsonify
from repositories import minigame_repository

minigame_service = Blueprint('minigame_service', __name__)

minigame_service.route("/minigames", methods=["GET"])
def get_minigames():
    room_id = int(request.args.get("roomId"))
    minigames = minigame_repository.get_minigames(room_id)
    return jsonify(minigames)
    
minigame_service.route("/minigame/<int:minigame_id>", methods=["GET"])
def get_minigame(minigame_id):
    minigame = minigame_repository.get_minigame(minigame_id)
    return jsonify(minigame)
    
    
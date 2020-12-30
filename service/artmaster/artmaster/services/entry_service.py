#!/usr/bin/python

from flask import Blueprint, jsonify, request
from repositories import entry_repository
from utils.entry_utils import to_entry_components_json

entry_service = Blueprint('entry_service', __name__)

@entry_service.route("/entry", methods=["POST", "DELETE"])
def add_or_remove_entry():
    if request.method == "POST":
        room_id = int(request.args.get("roomId"))
        user_id = int(request.args.get("userId"))
        round_id_raw = request.args.get("roundId")
        round_id = (int(round_id_raw)
            if round_id_raw is not None and round_id_raw.isdigit()
            else None)
        entry_components = request.get_json()
        entry_repository.create_entry(room_id, user_id, round_id, entry_components)
    elif request.method == "DELETE":
        entry_id = int(request.args.get("entryId"))
        entry_repository.remove_entry(entry_id)

    return "{}"

@entry_service.route("/entries", methods=["GET"])
def get_entries():
    room_id = int(request.args.get("roomId"))
    round_id_raw = request.args.get("roundId")
    round_id = int(round_id_raw) if round_id_raw is not None and round_id_raw.isdigit() else None
    entry_entities = entry_repository.get_entries(room_id, round_id)
    entry_component_entitites = entry_repository.get_entry_components(entry_entities)
    entry_components_json = to_entry_components_json(entry_entities, entry_component_entitites)
    return entry_components_json

@entry_service.route("/entry", methods=["GET"])
def get_entry():
    entry_id = int(request.args.get("entryId"))
    entry_entity = entry_repository.get_entry(entry_id)
    entry_component_entities = entry_repository.get_entry_components([entry_entity])
    entry_components_json = to_entry_components_json([entry_entity], entry_component_entities)
    return entry_components_json

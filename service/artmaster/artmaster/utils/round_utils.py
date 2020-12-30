from flask import Blueprint, jsonify, request
from datetime import datetime

def to_round_dto(round_entity):
    return jsonify(to_round_dict(round_entity))

def to_round_dict(round_entity):
    return {
        "roundId": round_entity.RoundId,
        "stageStateId": round_entity.StageStateId,
        "timeRemaining": get_time_remaining(round_entity),
        "entryId": round_entity.EntryId
    }

def get_time_remaining(round_entity):
    time_remaining = None
    if round_entity.StageStateStartTime is not None and \
        round_entity.StageStateEndTime is not None:
        time_delta = round_entity.StageStateEndTime - datetime.utcnow()
        time_remaining = time_delta.total_seconds()
    return time_remaining

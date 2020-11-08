from flask import jsonify

def to_room_dto(room):
    return jsonify(to_room_dict(room))

def to_room_dict(room):
    return {
        "roomId": room.RoomId,
        "roomCode": room.RoomCode,
        "ownerUserId": room.OwnerUserId,
        "currentRoundId": room.CurrentRoundId,
        "minigameId": room.MinigameId,
        "roomUsers": [{"username": r.Username, "userId": r.UserId, "score": r.Score } for r in room.RoomUsers]
    }

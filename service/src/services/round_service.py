#!/usr/bin/python

from flask import Blueprint, jsonify, request
from database.database import Database
from database.data_model import Round, Room, Image, RoundImage, Rating
from datetime import datetime, timedelta

round_service = Blueprint('round_service', __name__)

# Create a new round and then returns the round info
@round_service.route("/round", methods=["GET", "POST"])
def poll_or_create_round():
    sesh = Database().get_session()
    if request.method == "POST":
        room_id = request.args.get("roomId")
        user_id = request.args.get("userId")
        if room_id is None or user_id is None:
            return "Please set the roomId and userId"
        room = (sesh
				        .query(Room)
				        .filter(Room.RoomId==round_entity.RoomId)
				        .first())
				    if room.OwnerUserId != user_id:
				        return "Only the room owner can start rounds"
        round_entity = Round(RoomId=room_id)
        sesh.add(round_entity)
        sesh.flush() 
        update_stage(sesh, round_entity)
        sesh.commit()
    else:
        round_id = request.args.get("roundId")
        round_entity = (sesh.query(Round)
           .filter(Round.RoundId==round_id)
           .first())
        if round_entity is None:
            return "No round for given roundId"
        maybe_update_stage(sesh, round_entity)
    
    return to_round_dto(round_entity)
    
def to_round_dto(round_entity):
    return jsonify({
        "roundId": round_entity.RoundId,
        "stageStateId": round_entity.StageStateId,
        "timeRemaining": get_time_remaining(round_entity)     
    })
    
def get_time_remaining(round_entity):
    time_remaining = None
    if round_entity.StageStateStartTime is not None and \
       round_entity.StageStateEndTime is not None:
       time_remaining = (round_entity.StageStateEndTime - datetime.utcnow()).total_seconds()
    return time_remaining

def maybe_update_stage(sesh, round_entity):
    time_remaining = get_time_remaining(round_entity)
    if time_remaining <= 0:
        update_stage(sesh, round_entity)

# stages = ["Drawing", "Critiquing", "Reviewing", "Done"]       
def update_stage(sesh, round_entity):
    duration = 0
    if round_entity.StageStateId == None:
        round_entity.StageStateId = 0      
        duration = 30
        update_room(sesh, round_entity)
    elif round_entity.StageStateId == 0:
        round_entity.StageStateId += 1
        duration = 10
    elif round_entity.StageStateId == 1:
        round_entity.StageStateId += 1
        duration = 20
    else:
        round_entity.StageStateId += 1
        
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(seconds=duration)
    round_entity.StageStateStartTime = start_time
    round_entity.StageStateEndTime = end_time
    sesh.commit()
    
def update_room(sesh, round_entity):
    room = (sesh
        .query(Room)
        .filter(Room.RoomId==round_entity.RoomId)
        .first())
    room.CurrentRoundId = round_entity.RoundId
        
# provides the round info including who won
@round_service.route("/round/<int:round_id>/ratings", methods=["GET"])
def get_ratings(round_id):
    sesh = Database().get_session()
    round_ratings = (sesh
        .query(Rating) 
        .join(Rating.RoundImage)
        .filter(Round.RoundId==round_id)
        .all())

    results = {}
    for rr in round_ratings:
        if rr.Rating != 0:
            if rr.ImageId in results:
                results[key] += 1
            else:
                results[key] = 1
    winner_image_id = None
    winner_rating = 0
    for image_id, rating in results:
        if rating >= winner_rating:
            winner_image_id = image_id
            winner_rating = rating

    winning_image_location = filter(
        lambda rr: rr.RoundImage.ImageId == winner_image_id,
        round_ratings)[0].Location

    round_info = { 
        "round_id": round_id,
        "winner_id": winner_id,
        "winning_image_location": winning_image_location
    }
    return jsonify(round_info)

# provide the rating
@round_service.route("/round/<int:round_id>/image/<int:image_id>/rating", methods=["POST"])
def set_rating(round_id, image_id):
    rating = request.args.get("rating")
    user_id = request.args.get("raterUserId")
    rating_entity = Rating(Rating=rating, RaterUserId=raterUserId, ImageId=image_id)
    sesh = Database().get_session()
    sesh.add(rating_entity)
    sesh.commit()
    return jsonify({
        "ratingId", rating_entity.RatingId
})
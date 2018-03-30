#!/usr/bin/python

import sys
from database.database import Database
from database.data_model import User, Round, Image, RoundImage, Rating, Room, RoomUser
from flask import Flask, request, jsonify
from random import randint

data_dir = "/Users/silleknarf/Code/art-master/data"

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the art-master api"

# Creates a new user if the name isn't already taken
@app.route("/user/<string:username>", methods=["POST"])
def create_user(username):
    sesh = Database().get_session()
    existing_user = (sesh.query(User)
        .filter(User.Username==username).first())
    if existing_user is None:
        new_user = User(Username=username)
        sesh.add(new_user)
        sesh.commit()
        return jsonify({
                "userId": new_user.UserId,
                "username": new_user.Username
            })
    return jsonify({})

# Create a new round and then returns the round info
@app.route("/round", methods=["POST"])
def create_round():
    sesh = Database().get_session()
    round = Round()
    sesh.add(round)
    sesh.commit()
    return jsonify({ "roundId": round.RoundId })

#provide the image in the body
@app.route("/round/<int:round_id>/user/<int:user_id>/drawing", methods=["POST"])
def add_drawing(round_id, user_id):
    drawing_file = request.files("drawing")
    drawing_file_name = round_id + "/" + user_id + ".png"
    f.save(data_dir + "/" + drawing_file_name);
    sesh = Database().get_session()
    drawing = Image(UserId=user_id, Location=drawing_file_name)
    sesh.add(drawing)
    sesh.flush()
    round_drawing = RoundImage(RoundId=round_id, ImageId=drawing.ImageId)
    sesh.commit()
    return ({ 
        "imageId": drawing.ImageId,
        "roundImageId": round_drawing.RoundImageId
    })

# returns two images to rate
@app.route("/round/<int:round_id>/drawings", methods=["GET"])
def get_drawings(round_id):
    sesh = Database().get_session()
    round_images = (sesh
        .query(RoundImage)
        .filter(RoundImage.RoundId==round_id)
        .all())
    locations = [ri.Image.Location for ri in round_images]
    return jsonify(locations)

# provides the round info including who won
@app.route("/round/<int:round_id>", methods=["GET"])
def get_round_info(round_id):
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
@app.route("/drawing/<int:image_id>/", methods=["POST"])
def provide_rating(round_id, image_id):
    rating = request.args.get("rating")
    user_id = request.args.get("raterUserId")
    rating_entity = Rating(Rating=rating, RaterUserId=raterUserId, ImageId=image_id)
    sesh = Database().get_session()
    sesh.add(rating_entity)
    sesh.commit()
    return jsonify({
        "ratingId", rating_entity.RatingId
    })

@app.route("/room", methods=["GET", "POST"])
def get_or_create_room():
    sesh = Database().get_session() 
    room = None

    if request.method == "GET":
        roomCode = request.args.get("roomCode")
        room = (sesh.query(Room)
            .filter(Room.RoomCode==roomCode)
            .first())
    else:
        roomCode = get_room_code()
        room = Room(RoomCode=roomCode)
        sesh.add(room)
        sesh.commit()

    return jsonify({
        "roomId": room.RoomId,
        "roomcode": room.RoomCode
    })

@app.route("/room/<int:room_id>/user/<int:user_id>", methods=["POST"])
def add_user_to_room(room_id, user_id):
    sesh = Database().get_session()
    room_user = RoomUser(RoomId=room_id, UserId=user_id)
    sesh.add(room_user)
    sesh.commit()
    return jsonify({})

def get_room_code():
    first_chr = 65
    return "".join([chr(first_chr+randint(0, 25)) for i in range(0, 4)])

if __name__ == "__main__":
    app.run(host="192.168.0.90", port=5000, debug=True)


#!/usr/bin/python

import sys
sys.path.append("../database")
from database import Database, User
from flask import Flask, request

data_dir = "/Users/silleknarf/Code/art-master/data"

app = Flask(__name__)

# Creates a new user if the name isn't already taken
@app.route("/user/<string:username>", methods=["POST"])
def create_user(username):
    sesh = Database().get_session()
    existing_user = sesh.query(User).filter(Username=username).first()
    if existing_user is None:
        new_user = User(Username=username)
        sesh.add(new_user)
        sesh.commit()
        return new_user
    return None

# Create a new round and then returns the round info
@app.route("/round", methods=["POST"])
def create_round():
    sesh = Database().get_session()
    round = Round()
    sesh.add(round)
    sesh.commit()
    return round

#provide the image in the body
@app.route("round/<int:round_id>/user/<int:user_id>/drawing", methods=["POST"])
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

# returns two images to rate
@app.route("round/<int:round_id>/drawings", methods=["GET"])
def get_drawings(round_id):
    sesh = Database().get_session()
    round_images = sesh.query(RoundImage).filter(RoundId==round_id).all()
    locations = [ri.Image.Location for ri in round_images]
    return locations

# provides the round info including who won
@app.route("round/<int:round>", methods=["GET"]):
def get_round_info():
    sesh = Database().get_session()
    round_ratings = sesh.query(Rating)
        .join(Rating.RoundImage)
        .filter(Round.RoundId==round_id)
        .all()

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

    winning_image_location = round_ratings
        .filter(lambda rr: rr.RoundImage.ImageId == winner_image_id)[0]
        .Location

    round_info = { 
        "round_id": round_id,
        "winner_id": winner_id,
        "winning_image_location": winning_image_location
    }
    return round_info 

# provide the rating
@app.route("drawing/<int:image_id>/", methods=["POST"])
def provide_ratiing(round_id, image_id)
    rating = request.args.get("rating")
    user_id = request.args.get("raterUserId")
    round_entity = Rating(Rating=rating, RaterUserId=raterUserId, ImageId=image_id)
    sesh = Database().get_session()
    sesh.add(round_entity)
    sesh.commit()

if __name__ == "__main__":
    app.run(debug=True)


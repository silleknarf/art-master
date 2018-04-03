#!/usr/bin/python

from flask import Blueprint, jsonify
from database.database import Database
from database.data_model import User

user_service = Blueprint('user_service', __name__)

# Creates a new user if the name isn't already taken
@user_service.route("/user/<string:username>", methods=["POST"])
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

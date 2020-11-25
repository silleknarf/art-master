#!/usr/bin/python

from flask import Blueprint, jsonify
from repositories import user_repository

user_service = Blueprint('user_service', __name__)

# Creates a new user if the name isn't already taken
@user_service.route("/user/<string:username>", methods=["POST"])
def create_user(username):
    new_user = user_repository.create_user(username)
    return jsonify({
        "userId": new_user.UserId,
        "username": new_user.Username
    })

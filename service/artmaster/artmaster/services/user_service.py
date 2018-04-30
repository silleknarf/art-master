#!/usr/bin/python

from flask import Blueprint, jsonify, abort
from repositories import user_repository
from services.exceptions import InvalidUsage
import logging 

logfile = logging.getLogger('file')
user_service = Blueprint('user_service', __name__)

# Creates a new user if the name isn't already taken
@user_service.route("/user/<string:username>", methods=["POST"])
def create_user(username):
    logfile.info("Checking for existing user: %s" % username)
    new_user = user_repository.create_user(username)
    return jsonify({
        "userId": new_user.UserId,
        "username": new_user.Username
    })
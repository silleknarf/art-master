#!/usr/bin/python

from flask import Blueprint, jsonify, abort
from artmaster.database.database import session
from artmaster.database.data_model import User
from artmaster.services.exceptions import InvalidUsage
import logging 

logfile = logging.getLogger('file')
user_service = Blueprint('user_service', __name__)

# Creates a new user if the name isn't already taken
@user_service.route("/user/<string:username>", methods=["POST"])
def create_user(username):
    logfile.info("Checking for existing user: %s" % username)
    existing_user = (session
        .query(User)
        .filter(User.Username==username)
        .first())
    if existing_user is None:
        logfile.info("Creating new user: %s" % username)
        new_user = User(Username=username)
        session.add(new_user)
        session.commit()
        return jsonify({
                "userId": new_user.UserId,
                "username": new_user.Username
            })
    else:
        error_text = "User: %s already exists" % username
        raise InvalidUsage(error_text)
    return jsonify({})

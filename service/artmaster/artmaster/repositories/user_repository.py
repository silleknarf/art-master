import logging
from database.database import session
from database.data_model import User
from services.exceptions import InvalidUsage

logfile = logging.getLogger('file')

def get_user(user_id):
    user_entity = (session
        .query(User)
        .filter(User.UserId==user_id)
        .first())
    return user_entity

def create_user(username):
    logfile.info("Creating new user: %s", username)
    new_user = User(Username=username)
    session.add(new_user)
    session.commit()
    return new_user

def increase_user_score(user_id, score):
    existing_user = (session
        .query(User)
        .filter(User.UserId==user_id)
        .first())

    if existing_user is None:
        error_text = "User: %s doesn't exist" % user_id
        raise InvalidUsage(error_text)

    existing_user.Score += score
    session.commit()

    return existing_user

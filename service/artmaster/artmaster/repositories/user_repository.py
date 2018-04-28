from artmaster.database.database import session
from artmaster.database.data_model import User

def get_user(user_id):
    user_entity = (session
        .query(User)
        .filter(User.UserId==user_id)
        .first())
    return user_entity
from repositories import room_user_repository 
from database.database import session
from sqlalchemy.exc import IntegrityError
from database.data_model import Image, Round
import logging

logfile = logging.getLogger('file')

def create_image(user_id, image_base_64, round_id):
    (session
        .query(Image)
        .filter(Image.UserId==user_id)
        .filter(Image.RoundId==round_id)
        .delete())
    drawing = Image(
        UserId=user_id, 
        ImageBase64=image_base_64, 
        RoundId=round_id)
    session.add(drawing)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    
    return drawing

def get_round_images(round_id):
    round_images = (session
        .query(Image)
        .filter(Image.RoundId==round_id)
        .all())
    return round_images

def get_round(image_id):
    round_entity = (session
        .query(Round)
        .join(Image)
        .filter(Image.ImageId==image_id)
        .first())
    return round_entity

def are_all_images_submitted(round_id, room_id):
    round_images_count = len(get_round_images(round_id))
    room_users_count = len(room_user_repository.get_users_in_room(room_id))
    logfile.info("Images count: %s" % (round_images_count))
    return round_images_count == room_users_count

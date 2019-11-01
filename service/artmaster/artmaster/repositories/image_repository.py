from repositories import room_user_repository 
from database.database import session
from database.data_model import Image, Round

def create_image(user_id, image_base_64, round_id):
    drawing = Image(
        UserId=user_id, 
        ImageBase64=image_base_64, 
        RoundId=round_id)
    session.add(drawing)
    session.commit()
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
    return round_images_count == room_users_count

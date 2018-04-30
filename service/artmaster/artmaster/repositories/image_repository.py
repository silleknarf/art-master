from database.database import session
from database.data_model import Image

def create_image(user_id, drawing_file_location, round_id):
    drawing = Image(
        UserId=user_id, 
        Location=drawing_file_location, 
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
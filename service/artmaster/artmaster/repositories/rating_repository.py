from database.database import session
from database.data_model import Round, Image, Rating

def get_ratings(round_id):
    round_ratings = (session
        .query(Rating, Image) 
        .join(Image)
        .join(Round)
        .filter(Round.RoundId==round_id)
        .all())

def has_existing_rating(image_id, user_id):
    round_id = (session
        .query(Image)
        .filter(Image.ImageId==image_id)
        .first()
        .RoundId)
    any_existing_rating = len(session
        .query(Rating)
        .join(Image)
        .filter(Rating.RaterUserId==user_id)
        .all()) > 0
    return any_existing_rating

def create_rating(image_id, rating, user_id):
    rating_entity = Rating(
        Rating=rating, 
        RaterUserId=user_id, 
        ImageId=image_id)
    session.add(rating_entity)
    session.commit()
    return rating_entity
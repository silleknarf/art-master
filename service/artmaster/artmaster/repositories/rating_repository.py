from repositories import room_user_repository, user_repository
from database.database import session
from database.data_model import Round, Image, Rating

def get_ratings(round_id):
    round_ratings = (session
        .query(Rating, Image) 
        .join(Image)
        .join(Round)
        .filter(Round.RoundId==round_id)
        .all())
    return round_ratings

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
        .filter(Image.RoundId==round_id)
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

def are_all_votes_submitted(round_id, room_id):
    round_votes_count = len(session
        .query(Rating)
        .join(Image)
        .filter(Image.RoundId==round_id)
        .all())
    room_users_count = len(room_user_repository.get_users_in_room(room_id))
    return round_votes_count == room_users_count

def get_round_rating_results(round_id):
    round_ratings = get_ratings(round_id)

    if len(round_ratings) == 0:
        return []

    ratings = [rr[0] for rr in round_ratings]
    images = [rr[1] for rr in round_ratings]

    results = {}
    for rr in ratings:
        if rr.Rating != 0:
            if rr.ImageId in results:
                results[rr.ImageId] += 1
            else:
                results[rr.ImageId] = 1

    winning_image_ids = []
    winning_rating = 0
    for image_id, rating in results.items():
        if rating == winning_rating:
            winning_image_ids.append(image_id)
        elif rating >= winning_rating:
            winning_image_ids = [image_id]
            winning_rating = rating

    winning_images = []
    for winning_image_id in winning_image_ids:
        winning_image = [i for i in images if i.ImageId == winning_image_id][0]
        winning_images.append(winning_image)

    results = []
    for winning_image in winning_images:
        winning_user = user_repository.get_user(winning_image.UserId)
        result = { 
            "roundId": round_id,
            "winnerId": winning_user.UserId,
            "winnerUsername": winning_user.Username,
            "winningImageBase64": winning_image.ImageBase64,
        }
        results.append(result)
    return results

def update_score_for_highest_rating(round_id):
    ratings = get_round_rating_results(round_id)
    for rating in ratings:
        user_repository.increase_user_score(rating["winnerId"], 10)
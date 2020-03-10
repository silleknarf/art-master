from repositories import room_user_repository, user_repository
from database.database import session
from database.data_model import Round, Image, Rating, Word
import logging

logfile = logging.getLogger('file')

def get_ratings(round_id):
    round_ratings = (session
        .query(Rating, Image, Word) 
        .outerjoin(Image)
        .outerjoin(Word)
        .filter(Rating.RoundId==round_id)
        .all())
    return round_ratings

def has_existing_rating(round_id, user_id):
    any_existing_rating = len(session
        .query(Rating)
        .filter(Rating.RaterUserId==user_id)
        .filter(Rating.RoundId==round_id)
        .all()) > 0
    return any_existing_rating

def create_rating(image_id, word_id, round_id, rating, user_id):
    rating_entity = Rating(
        Rating=rating, 
        RaterUserId=user_id, 
        RoundId=round_id,
        WordId=word_id,
        ImageId=image_id)
    session.add(rating_entity)
    session.commit()
    return rating_entity

def are_all_votes_submitted(round_id, room_id):
    round_votes_count = len(session
        .query(Rating)
        .filter(Rating.RoundId==round_id)
        .all())
    room_users_count = len(room_user_repository.get_users_in_room(room_id))
    return round_votes_count == room_users_count

def get_round_rating_results(round_id):
    round_ratings = get_ratings(round_id)

    logfile.info("Ratings Count: %s" % len(round_ratings))
    if len(round_ratings) == 0:
        return []

    ratings = [rr[0] for rr in round_ratings]
    images = [rr[1] for rr in round_ratings if rr[1] is not None]
    words = [rr[2] for rr in round_ratings if rr[2] is not None]

    image_votes = {}
    for rr in ratings:
        if rr.Rating != 0 and rr.ImageId is not None:
            if rr.ImageId in image_votes:
                image_votes[rr.ImageId] += 1
            else:
                image_votes[rr.ImageId] = 1

    winning_image_ids = []
    winning_rating = 0
    for image_id, rating in image_votes.items():
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
            "votes": image_votes[winning_image.ImageId]
        }
        results.append(result)

    word_votes = {}
    for rr in ratings:
        if rr.Rating != 0 and rr.WordId is not None:
            if rr.ImageId in word_votes:
                word_votes[rr.WordId] += 1
            else:
                word_votes[rr.WordId] = 1

    winning_word_ids = []
    winning_rating = 0
    for image_id, rating in word_votes.items():
        if rating == winning_rating:
            winning_word_ids.append(image_id)
        elif rating >= winning_rating:
            winning_word_ids = [image_id]
            winning_rating = rating

    winning_words = []
    for winning_word_id in winning_word_ids:
        winning_word = [w for w in words if w.WordId == winning_word_id][0]
        winning_words.append(winning_word)

    for winning_word in winning_words:
        winning_user = user_repository.get_user(winning_word.UserId)
        result = { 
            "roundId": round_id,
            "winnerId": winning_user.UserId,
            "winnerUsername": winning_user.Username,
            "word": winning_word.Word,
            "votes": word_votes[winning_word.WordId]
        }
        results.append(result)

    return results

def update_score_for_highest_rating(round_id):
    ratings = get_round_rating_results(round_id)
    for rating in ratings:
        user_repository.increase_user_score(rating["winnerId"], 10)
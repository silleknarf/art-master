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

def get_rating_results(
    ratings,
    entities,
    round_id,
    entity_id_selector,
    entity_content_key,
    entity_content_value_selector):

    votes = {}
    for rr in ratings:
        entity_id = entity_id_selector(rr)
        if rr.Rating != 0 and entity_id is not None:
            if entity_id in votes:
                votes[entity_id] += 1
            else:
                votes[entity_id] = 1

    winning_entity_ids = []
    winning_rating = 0
    for entity_id, rating in votes.items():
        if rating == winning_rating:
            winning_entity_ids.append(entity_id)
        elif rating >= winning_rating:
            winning_entity_ids = [entity_id]
            winning_rating = rating

    winning_entities = []
    for winning_entity_id in winning_entity_ids:
        winning_entity = [e for e in entities if entity_id_selector(e) == winning_entity_id][0]
        winning_entities.append(winning_entity)

    results = []
    for winning_entity in winning_entities:
        winning_user = user_repository.get_user(winning_entity.UserId)
        result = {
            "roundId": round_id,
            "winnerId": winning_user.UserId,
            "winnerUsername": winning_user.Username,
            entity_content_key: entity_content_value_selector(winning_entity),
            "votes": votes[entity_id_selector(winning_entity)]
        }
        results.append(result)
    return results

def get_round_rating_results(round_id):
    logfile.info("Getting round rating results")
    round_ratings = get_ratings(round_id)

    logfile.info("Ratings Count: %s", len(round_ratings))
    if len(round_ratings) == 0:
        return []

    ratings = [rr[0] for rr in round_ratings]
    images = [rr[1] for rr in round_ratings if rr[1] is not None]
    words = [rr[2] for rr in round_ratings if rr[2] is not None]

    image_results = get_rating_results(
        ratings,
        images,
        round_id,
        lambda image : image.ImageId,
        "winningImageBase64",
        lambda image : image.ImageBase64
    )
    word_results = get_rating_results(
        ratings,
        words,
        round_id,
        lambda word : word.WordId,
        "word",
        lambda word : word.Word,
    )
    results = image_results + word_results
    return results

def update_score_for_highest_rating(round_id):
    ratings = get_round_rating_results(round_id)
    for rating in ratings:
        user_repository.increase_user_score(rating["winnerId"], 10)

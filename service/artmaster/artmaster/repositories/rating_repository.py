from repositories import room_user_repository, user_repository, entry_repository
from database.database import session
from database.data_model import Round, Image, Rating, Entry
from utils.entry_utils import to_entry_components_dto
import logging

logfile = logging.getLogger('file')

def get_ratings(round_id):
    round_ratings = (session
        .query(Rating, Image, Entry)
        .outerjoin(Image)
        .outerjoin(Entry)
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

def create_rating(image_id, entry_id, round_id, rating, user_id):
    rating_entity = Rating(
        Rating=rating,
        RaterUserId=user_id,
        RoundId=round_id,
        EntryId=entry_id,
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

    results = []
    distinct_entities = {entity_id_selector(e): e for e in entities}.values()
    for entity in distinct_entities:
        user = user_repository.get_user(entity.UserId)
        result = {
            "roundId": round_id,
            "userId": user.UserId,
            "username": user.Username,
            entity_content_key: entity_content_value_selector(entity),
            "votes": votes[entity_id_selector(entity)]
        }
        results.append(result)
    return results

def get_entry_component_dtos(entry):
    entry_component_entities = entry_repository.get_entry_components([entry])
    entry_component_dtos = to_entry_components_dto(entry_component_entities)
    return entry_component_dtos

def get_round_rating_results(round_id):
    logfile.info("Getting round rating results")
    round_ratings = get_ratings(round_id)

    logfile.info("Ratings Count: %s", len(round_ratings))
    if len(round_ratings) == 0:
        return []

    ratings = [rr[0] for rr in round_ratings]
    images = [rr[1] for rr in round_ratings if rr[1] is not None]
    entries = [rr[2] for rr in round_ratings if rr[2] is not None]

    image_results = get_rating_results(
        ratings,
        images,
        round_id,
        lambda image : image.ImageId,
        "imageBase64",
        lambda image : image.ImageBase64
    )
    entry_results = get_rating_results(
        ratings,
        entries,
        round_id,
        lambda entry : entry.EntryId,
        "entryComponents",
        get_entry_component_dtos
    )
    results = image_results + entry_results
    results.sort(key=lambda x : x["votes"], reverse=True)
    return results

def update_score_for_highest_rating(round_id):
    results = get_round_rating_results(round_id)
    winning_rating = 0
    winning_user_ids = []
    for result in results:
        rating = result["votes"]
        user_id = result["userId"]
        if rating == winning_rating:
            winning_user_ids.append(user_id)
        elif rating >= winning_rating:
            winning_user_ids = [user_id]
            winning_rating = rating

    for winning_user_id in winning_user_ids:
        user_repository.increase_user_score(winning_user_id, 10)

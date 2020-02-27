from database.database import session
from database.data_model import Minigame

def get_minigame(minigame_id):
    minigame_entity = (session
        .query(Minigame)
        .filter(Minigame.MinigameId==minigame_id)
        .first())
    return minigame_entity

def get_minigames():
    minigame_entities = (session
        .query(Minigame)
        .all())
    return minigame_entities
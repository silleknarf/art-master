from database.database import session
from database.data_model import Minigame
from repositories import minigame_logic_repository

def get_minigame(minigame_id):
    minigame_entity = (session
        .query(Minigame)
        .filter(Minigame.MinigameId==minigame_id)
        .first())
    enrich_minigame(minigame_entity)
    return minigame_entity

def get_minigames():
    minigame_entities = (session
        .query(Minigame)
        .all())
    for minigame_entity in minigame_entities:
        enrich_minigame(minigame_entity)

    return minigame_entities

def enrich_minigame(minigame):
    minigame_config = minigame_logic_repository.get_minigame_config(minigame.MinigameId)
    minigame.Description = minigame_config["description"]
    minigame.CanSeeOwnWordsOnly = minigame_config["canSeeOwnWordsOnly"]
    minigame.EntryComponents = minigame_config["entryComponents"]

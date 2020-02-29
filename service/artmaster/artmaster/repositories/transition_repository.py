from database.database import session
from database.data_model import Transition

def get_transitions(minigame_id):
    transitions = (session
        .query(Transition)
        .filter(Transition.MinigameId==minigame_id)
        .all())
    return transitions


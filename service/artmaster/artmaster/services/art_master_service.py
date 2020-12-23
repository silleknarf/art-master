import logging
from repositories import transition_repository, user_repository

logfile = logging.getLogger('file')

def get_next_stage(stage_state_id):
    art_master_minigame_id = 1
    transitions = transition_repository.get_transitions(art_master_minigame_id)
    transition = [t for t in transitions if t.StateFrom == stage_state_id][0]
    return {
        "nextStageId": transition.StateTo
    }

def get_minigame_config():
    return {
        "canSeeOwnWordsOnly": True,
        "description": [
            "Add a word to the list below.",
            "Each round, one entry will be selected at random.",
            "Every player will have to draw it.",
            "Players will then vote on which drawing is the best."
        ],
        "entryComponents": ["Word"]
    }

def init_round(room_id, round_id):
    return {}

def init_drawing(round_id, entry):
    word = entry["word"]
    return {
        "durationInSeconds": 90,
        "word": word
    }

# Not required for art master
# def init_filling_in_blanks()
# duration: 60s

def init_critiquing(round_id, num_players):
    return {
        "durationInSeconds": 15 * num_players,
    }

def init_reviewing(round_id, round_ratings):
    return {
        "durationInSeconds": 15
   }

def init_done(round_id):
    return {}

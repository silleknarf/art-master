import logging
from repositories import transition_repository, user_repository

logfile = logging.getLogger('file')

def get_next_stage(stage_state_id):
    sentenced_to_death_minigame_id = 1
    transitions = transition_repository.get_transitions(sentenced_to_death_minigame_id)
    transition = [t for t in transitions if t.StateFrom == stage_state_id][0]
    return {
        "nextStageId": transition.StateTo
    }

def get_minigame_config():
    return {
        "canSeeOwnWordsOnly": True,
        "description": [
            "Add a phrase with words to fill in represented by underscores.",
            "For example: 'The _ fox jumped over the _.'",
            "Each round, one entry will be selected at random.",
            "Every player will have to fill in the gaps with words.",
            "Players will then vote on which complete sentence is the funniest."
        ],
        "entryComponents": ["Phrase with gaps"]
    }

def init_round(room_id, round_id):
    return {}

# Not required for sentenced to death
#def init_drawing(round_id, entry):

# Not required for art master
def init_filling_in_blanks(round_id):
    return {
        "durationInSeconds": 60
    }

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

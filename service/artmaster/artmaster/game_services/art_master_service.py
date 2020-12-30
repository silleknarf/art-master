import logging

logfile = logging.getLogger('file')

ENTRY_COMPONENT_KEY = "Word"

def get_next_stage(stage_state_id):
    transitions = [
        { "state_from": None, "state_to": 0 },
        { "state_from": 0, "state_to": 2 },
        { "state_from": 2, "state_to": 3 },
        { "state_from": 3, "state_to": 4 }
    ]
    next_stage_id = [t["state_to"] for t in transitions if t["state_from"] == stage_state_id][0]
    return {
        "nextStageId": next_stage_id
    }

def get_minigame_config():
    return {
        "canSeeOwnWordsOnly": False,
        "description": [
            "Add a word to the list below.",
            "Each round, one entry will be selected at random.",
            "Every player will have to draw it.",
            "Players will then vote on which drawing is the best."
        ],
        "entryComponents": [ENTRY_COMPONENT_KEY]
    }

def init_round(round_id):
    return {}

def init_drawing(round_id, user_ids, entry):
    drawing_entry = [
        {
            "key": ENTRY_COMPONENT_KEY,
            "value": entry[ENTRY_COMPONENT_KEY]
        }
    ]

    return {
        "durationInSeconds": 90,
        "userEntries": [{ "userId": u, "entry": drawing_entry }
            for u in user_ids]
    }

# Not required for art master
# def init_filling_in_blanks()

def init_critiquing(round_id, player_ids):
    num_players = len(player_ids)
    return {
        "durationInSeconds": 15 * num_players,
    }

def init_reviewing(round_id):
    return {
        "durationInSeconds": 15
    }

def init_done(round_id):
    return {}

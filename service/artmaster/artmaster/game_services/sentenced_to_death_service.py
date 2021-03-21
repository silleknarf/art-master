import logging

logfile = logging.getLogger('file')

ENTRY_COMPONENT_KEY = "Phrase with gaps"

def get_next_stage(stage_state_id):
    transitions = [
        { "state_from": None, "state_to": 1 },
        { "state_from": 1, "state_to": 2 },
        { "state_from": 2, "state_to": 3 },
        { "state_from": 3, "state_to": 4 }
    ]
    next_stage_id = [t["state_to"] for t in transitions if t["state_from"] == stage_state_id][0]

    return {
        "nextStageId": next_stage_id
    }

def get_minigame_config():
    return {
        "canSeeOwnEntriesOnly": True,
        "description": [
            "Add a phrase with words to fill in represented by underscores.",
            "For example: 'The _ fox jumped over the _.'",
            "Each round, one entry will be selected at random.",
            "Every player will have to fill in the gaps with words.",
            "Players will then vote on which complete sentence is the funniest."
        ],
        "entryComponents": [ENTRY_COMPONENT_KEY]
    }

def init_round(round_id):
    return {}

# Not required for sentenced to death
#def init_drawing(round_id, entry):

def init_filling_in_blanks(user_ids, entry):
    filling_in_blanks_entry = [
        {
            "key": ENTRY_COMPONENT_KEY,
            "value": entry[ENTRY_COMPONENT_KEY]
        }
    ]
    return {
        "durationInSeconds": 60,
        "userEntries": [{ "userId": u, "entry": filling_in_blanks_entry }
            for u in user_ids]
    }

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

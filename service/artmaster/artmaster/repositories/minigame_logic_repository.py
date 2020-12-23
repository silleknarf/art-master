from services import art_master_service

def get_next_stage(minigame_id, stage_stage_id):
    return art_master_service.get_next_stage(stage_stage_id)

def get_minigame_config(minigame_id):
    return art_master_service.get_minigame_config()

def init_round(minigame_id, round_id):
    return art_master_service.init_round(round_id)

def init_drawing(minigame_id, round_id, user_ids):
    return art_master_service.init_drawing(round_id, user_ids)

def init_filling_in_blanks(minigame_id, user_ids):
    return art_master_service.init_filling_in_blanks(user_ids)

def init_critiquing(minigame_id, round_id, user_ids):
    return art_master_service.init_critiquing(round_id, user_ids)

def init_reviewing(minigame_id, round_id, round_ratings):
    return art_master_service.init_reviewing(round_id, round_ratings)

def init_done(minigame_id, round_id):
    return art_master_service.done(round_id)

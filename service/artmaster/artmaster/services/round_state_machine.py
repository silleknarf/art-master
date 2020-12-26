import logging
import time
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from app import celery
from repositories import round_repository, word_repository, image_repository
from repositories import rating_repository, room_repository
from repositories import minigame_logic_repository
from utils.round_utils import get_time_remaining

logfile = logging.getLogger("file")
celery_logfile = get_task_logger("file")

class RoundState:
    DRAWING = 0
    FILLING_IN_BLANKS = 1
    CRITIQUING = 2
    REVIEWING = 3
    DONE = 4

class RoundStateMachine:
    _grace_duration_in_seconds = 2

    def __init__(self, round_entity):
        self.round_entity = round_entity

    def _cleanup_round(self):
        rating_repository.update_score_for_highest_rating(self.round_entity.RoundId)
        word_id_to_remove = self.round_entity.DrawingWordId
        self.round_entity.DrawingWordId = None
        room_repository.update_room_round(self.round_entity.RoomId, None)
        self._update_round(RoundState.DONE, 0)
        word_repository.remove_word(word_id_to_remove)

    def _update_round(self, stage_state_id, duration):
        celery_logfile.info("Updating round to set the time on the stage")
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=duration)
        round_repository.update_round(
            self.round_entity.RoundId,
            stage_state_id,
            start_time,
            end_time,
            self.round_entity.DrawingWordId)

    def _should_start_next_stage(self):
        time_remaining = self.get_time_remaining()
        return time_remaining <= 0

    def maybe_end_drawing_early(self):
        are_all_images_submitted = image_repository.are_all_images_submitted(
            self.round_entity.RoundId,
            self.round_entity.RoomId)
        if are_all_images_submitted:
            round_repository.end_stage(self.round_entity.RoundId)

    def maybe_end_submitting_sentences_early(self):
        are_all_sentences_submitted = word_repository.are_all_sentences_submitted(
            self.round_entity.RoomId,
            self.round_entity.RoundId)
        if are_all_sentences_submitted:
            round_repository.end_stage(self.round_entity.RoundId)

    def maybe_end_critiquing_early(self):
        are_all_votes_submitted = rating_repository.are_all_votes_submitted(
            self.round_entity.RoundId,
            self.round_entity.RoomId)
        if are_all_votes_submitted:
            round_repository.end_stage(self.round_entity.RoundId)

    def get_time_remaining(self):
        self.round_entity = round_repository.get_round(self.round_entity.RoundId)
        time_remaining = get_time_remaining(self.round_entity)
        return time_remaining

    def next_stage(self):
        minigame_id = room_repository.get_room(self.round_entity.RoomId, None).MinigameId
        get_next_stage_result =  minigame_logic_repository.get_next_stage(
            minigame_id,
            self.round_entity.StageStateId)

        next_stage_id = get_next_stage_result["nextStageId"]
        user_ids = room_repository.get_user_ids(self.round_entity.RoomId)
        duration = 0

        if next_stage_id == RoundState.DRAWING:
            drawing_result = minigame_logic_repository.init_drawing(
                minigame_id,
                self.round_entity.RoundId,
                user_ids)
            duration = (drawing_result["durationInSeconds"] +
                self._grace_duration_in_seconds)
        elif next_stage_id == RoundState.FILLING_IN_BLANKS:
            filling_in_blanks_result = minigame_logic_repository.init_filling_in_blanks(
                minigame_id,
                user_ids)
            duration = (filling_in_blanks_result["durationInSeconds"] +
                self._grace_duration_in_seconds)
        elif next_stage_id == RoundState.CRITIQUING:
            critiquing_result = minigame_logic_repository.init_critiquing(
                minigame_id,
                self.round_entity.RoundId,
                user_ids)
            duration = critiquing_result["durationInSeconds"]
        elif next_stage_id == RoundState.REVIEWING:
            reviewing_result = minigame_logic_repository.init_reviewing(
                minigame_id,
                self.round_entity.RoundId)
            duration = reviewing_result["durationInSeconds"]
        elif next_stage_id == RoundState.DONE:
            done_result = minigame_logic_repository.init_done(
                minigame_id,
                self.round_entity.RoundId)

        self._update_round(next_stage_id, duration)

        while not self._should_start_next_stage():
            time.sleep(1)

        if next_stage_id != RoundState.DONE:
            self.next_stage()
        else:
            self._cleanup_round()

@celery.task()
def run_round(round_id):
    round_entity = round_repository.get_round(round_id)
    round_state_machine = RoundStateMachine(round_entity)
    room_repository.update_room_round(round_entity.RoomId, round_entity.RoundId)
    minigame_id = room_repository.get_room(round_entity.RoomId, None).MinigameId
    minigame_logic_repository.init_round(minigame_id, round_entity.RoundId)
    round_state_machine.next_stage()

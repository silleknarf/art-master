import logging
import time
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from app import celery
from repositories import round_repository, word_repository, image_repository
from repositories import rating_repository, transition_repository, room_repository
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

    def _get_duration(self, state):
        if state == RoundState.DRAWING:
            return 90 + self._grace_duration_in_seconds
        elif state == RoundState.FILLING_IN_BLANKS:
            return 60 + self._grace_duration_in_seconds
        elif state == RoundState.CRITIQUING:
            number_of_players = room_repository.get_number_of_players(self.round_entity.RoomId)
            return 15 * number_of_players
        elif state == RoundState.REVIEWING:
            return 15

        return 0

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
        stage_state_id = self.round_entity.StageStateId
        minigame_id = room_repository.get_room(self.round_entity.RoomId, None).MinigameId
        transitions = transition_repository.get_transitions(minigame_id)

        celery_logfile.info("Minigame: %s in state: %s" % (minigame_id, stage_state_id))
        transition = [t for t in transitions if t.StateFrom == stage_state_id][0]

        celery_logfile.info(
            "Minigame: %s transitioning from %s to %s" %
            (minigame_id, transition.StateFrom, transition.StateTo))

        duration = self._get_duration(transition.StateTo)
        room_repository.update_room_round(self.round_entity.RoomId, self.round_entity.RoundId)
        self._update_round(transition.StateTo, duration)

        while not self._should_start_next_stage():
            time.sleep(1)

        celery_logfile.info("Ending state: %s", transition.StateTo)

        if transition.StateTo != RoundState.DONE:
            self.next_stage()
        else:
            self._cleanup_round()

@celery.task()
def run_round(round_id):
    round_entity = round_repository.get_round(round_id)
    round_state_machine = RoundStateMachine(round_entity)
    round_state_machine.next_stage()

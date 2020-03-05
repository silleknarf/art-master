from repositories import round_repository, word_repository, image_repository
from repositories import rating_repository, transition_repository, room_repository
from datetime import datetime, timedelta
import logging

logfile = logging.getLogger('file')

class RoundState:
    DRAWING = 0
    FILLING_IN_BLANKS = 1
    CRITIQUING = 2
    REVIEWING = 3
    DONE = 4 

class RoundStateMachine:
    def __init__(self, round_entity):
        self.round_entity = round_entity

    def _to_drawing(self):
        stage_state_id = RoundState.DRAWING      
        duration = 90
        round_repository.update_room_round(self.round_entity.RoomId, self.round_entity.RoundId)
        self._update_round(stage_state_id, duration)

    def _to_filling_in_blanks(self):
        stage_state_id = RoundState.FILLING_IN_BLANKS
        duration = 60
        round_repository.update_room_round(self.round_entity.RoomId, self.round_entity.RoundId)
        self._update_round(stage_state_id, duration)

    def _to_critiquing(self):
        stage_state_id = RoundState.CRITIQUING
        duration = 30
        self._update_round(stage_state_id, duration)

    def _to_reviewing(self):
        stage_state_id = RoundState.REVIEWING
        duration = 10
        self._update_round(stage_state_id, duration)

    def _to_done(self):
        stage_state_id = RoundState.DONE
        rating_repository.update_score_for_highest_rating(self.round_entity.RoundId)
        duration = 0
        word_id_to_remove = self.round_entity.DrawingWordId
        self.round_entity.DrawingWordId = None
        round_repository.update_room_round(self.round_entity.RoomId, None)
        self._update_round(stage_state_id, duration)
        word_repository.remove_word(word_id_to_remove)

    def _update_round(self, stage_state_id, duration):
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(seconds=duration)
        round_repository.update_round(
            self.round_entity.RoundId,
            stage_state_id, 
            start_time, 
            end_time, 
            self.round_entity.DrawingWordId)

    def maybe_end_drawing_early(self):
        are_all_images_submitted = image_repository.are_all_images_submitted(
            self.round_entity.RoundId, 
            self.round_entity.RoomId)
        if are_all_images_submitted:
            self._to_critiquing()

    def maybe_end_submitting_sentences_early(self):
        are_all_sentences_submitted = word_repository.are_all_sentences_submitted(
            self.round_entity.RoomId,
            self.round_entity.RoundId)
        if are_all_sentences_submitted:
            self._to_critiquing()

    def maybe_end_critiquing_early(self):
        are_all_votes_submitted = rating_repository.are_all_votes_submitted(
            self.round_entity.RoundId,
            self.round_entity.RoomId)
        if are_all_votes_submitted:
            self._to_reviewing()

    def maybe_next_stage(self):
        time_remaining = self.get_time_remaining()
        if time_remaining <= 0:
            self.next_stage()

    def get_time_remaining(self):
        time_remaining = None
        if self.round_entity.StageStateStartTime is not None and \
           self.round_entity.StageStateEndTime is not None:
           time_remaining = (self.round_entity.StageStateEndTime - datetime.utcnow()).total_seconds()
        return time_remaining

    def next_stage(self):
        stage_state_id = self.round_entity.StageStateId
        minigame_id = room_repository.get_room(self.round_entity.RoomId, None).MinigameId 
        transitions = transition_repository.get_transitions(minigame_id)

        logfile.info("Minigame: %s in state: %s" % (minigame_id, stage_state_id))
        transition = [t for t in transitions if t.StateFrom == stage_state_id][0]

        logfile.info("Minigame: %s transitioning from %s to %s" % (minigame_id, transition.StateFrom, transition.StateTo))
        if transition.StateTo == RoundState.DRAWING:
            self._to_drawing()
        elif transition.StateTo == RoundState.FILLING_IN_BLANKS:
            self._to_filling_in_blanks()
        elif transition.StateTo == RoundState.CRITIQUING:
            self._to_critiquing()
        elif transition.StateTo == RoundState.REVIEWING:
            self._to_reviewing()
        elif transition.StateTo == RoundState.DONE:
            self._to_done()
    
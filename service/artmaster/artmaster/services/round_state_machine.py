from repositories import round_repository, word_repository, image_repository, rating_repository
from datetime import datetime, timedelta

class RoundState:
    DRAWING = 0
    CRITIQUING = 1
    REVIEWING = 2
    DONE = 3 

class RoundStateMachine:
    def __init__(self, round_entity):
        self.round_entity = round_entity

    def _to_drawing(self):
        stage_state_id = RoundState.DRAWING      
        duration = 45
        round_repository.update_room_round(self.round_entity.RoomId, self.round_entity.RoundId)
        self._update_round(stage_state_id, duration)

    def _to_critiquing(self):
        stage_state_id = RoundState.CRITIQUING
        duration = 15
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
        if stage_state_id is None:
            self._to_drawing()
        elif stage_state_id == RoundState.DRAWING:
            self._to_critiquing()
        elif stage_state_id == RoundState.CRITIQUING:
            self._to_reviewing()
        elif stage_state_id == RoundState.REVIEWING:
            self._to_done()
    
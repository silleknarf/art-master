#!/usr/bin/python

import unittest
import mock
import json
from callee import Matching
from datetime import datetime
from services.round_state_machine import RoundStateMachine, RoundState
from .test_utils import Struct

class TestRoundStateMachine(unittest.TestCase):
    round_entity = Struct(**{
        "RoundId": 1,
        "RoomId": 1,
        "StageStateId": 0,
        "StageStateStartTime": None,
        "StageStateEndTime": None,
        "EntryId": 1
    })

    start_time = datetime(2018, 5, 1, 12, 0, 0)

    def setup_round_state_machine(
        self,
        stage_state_id,
        round_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining):
        self.round_entity.StageStateId = stage_state_id
        mock_datetime.utcnow.return_value = self.start_time
        room_repository.get_users_ids.return_value = [1,2,3]
        mock_get_time_remaining.return_value = 0
        round_repository.get_round.return_value = self.round_entity

        round_state_machine = RoundStateMachine(self.round_entity)
        return round_state_machine

    def transition_helper(
        self,
        round_repository,
        entry_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining,
        start_stage,
        end_stage,
        enforce_end_time=True):
        round_state_machine = self.setup_round_state_machine(
            start_stage,
            round_repository,
            room_repository,
            mock_datetime,
            mock_get_time_remaining)

        # Set minigame to Art Master
        room_repository.get_room.return_value = Struct(**{"MinigameId": 1})

        # We don't want to recursively call this function like
        # we normally do so we make a note of the original, mock it out
        # and then call the original function
        original_next_stage_func = round_state_machine.next_stage
        round_state_machine.next_stage = mock.Mock()
        original_next_stage_func()

        # Check assertions
        round_repository.update_round.assert_called_with(
            self.round_entity.RoundId,
            end_stage,
            self.start_time,
            Matching(lambda end_time: not enforce_end_time or end_time >= self.start_time),
            self.round_entity.EntryId)

    @mock.patch("services.round_state_machine.get_time_remaining")
    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.room_repository")
    @mock.patch("services.round_state_machine.image_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_end_drawing_round_early(
        self,
        round_repository,
        image_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining):
        round_state_machine = self.setup_round_state_machine(
            None,
            round_repository,
            room_repository,
            mock_datetime,
            mock_get_time_remaining)
        image_repository.are_all_images_submitted.return_value = True
        round_repository.reset_mock()
        round_state_machine.maybe_end_drawing_early()
        round_repository.end_stage.assert_called_once()

    @mock.patch("services.round_state_machine.get_time_remaining")
    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.room_repository")
    @mock.patch("services.round_state_machine.entry_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_start_round_state_machine(
        self,
        round_repository,
        entry_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining):
        self.transition_helper(
            round_repository,
            entry_repository,
            room_repository,
            mock_datetime,
            mock_get_time_remaining,
            None,
            RoundState.DRAWING)

    @mock.patch("services.round_state_machine.get_time_remaining")
    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.room_repository")
    @mock.patch("services.round_state_machine.entry_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_transition_to_critiquing(
        self,
        round_repository,
        entry_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining):
        self.transition_helper(
            round_repository,
            entry_repository,
            room_repository,
            mock_datetime,
            mock_get_time_remaining,
            RoundState.DRAWING,
            RoundState.CRITIQUING)

    @mock.patch("services.round_state_machine.get_time_remaining")
    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.room_repository")
    @mock.patch("services.round_state_machine.entry_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_transition_to_reviewing(
        self,
        round_repository,
        entry_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining):
        self.transition_helper(
            round_repository,
            entry_repository,
            room_repository,
            mock_datetime,
            mock_get_time_remaining,
            RoundState.CRITIQUING,
            RoundState.REVIEWING)

    @mock.patch("services.round_state_machine.get_time_remaining")
    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.room_repository")
    @mock.patch("services.round_state_machine.entry_repository")
    @mock.patch("services.round_state_machine.round_repository")
    @mock.patch("services.round_state_machine.rating_repository")
    def test_transition_to_done(
        self,
        rating_repository,
        round_repository,
        entry_repository,
        room_repository,
        mock_datetime,
        mock_get_time_remaining):
        entry_id_to_remove = self.round_entity.EntryId
        self.transition_helper(
            round_repository,
            entry_repository,
            room_repository,
            mock_datetime,
            mock_get_time_remaining,
            RoundState.REVIEWING,
            RoundState.DONE,
            enforce_end_time=False)
        room_repository.update_room_round.assert_called_once()
        entry_repository.remove_entry.assert_called_with(entry_id_to_remove)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoundStateMachine)
    suite.debug()

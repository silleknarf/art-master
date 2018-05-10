#!/usr/bin/python

import unittest
import mock
import json
from services.round_state_machine import RoundStateMachine, RoundState
from test_utils import *
from datetime import datetime
from callee import Matching

class TestRoundStateMachine(unittest.TestCase):
    round_entity = Struct(**{
        "RoundId": 1,
        "RoomId": 1,
        "StageStateId": None,
        "StageStateStartTime": None,
        "StageStateEndTime": None,
        "DrawingWordId": 1
    })
    start_time = datetime(2018, 05, 1, 12, 0, 0)

    def setup_round_state_machine(self, stage_state_id, round_repository, mock_datetime):
        self.round_entity.StageStateId = stage_state_id
        mock_datetime.utcnow.return_value = self.start_time
        round_state_machine = RoundStateMachine(self.round_entity)
        return round_state_machine

    def transition_helper(self, round_repository, word_repository, mock_datetime, start_stage, end_stage, enforce_end_time=True):
        # Go to the next stage
        round_state_machine = self.setup_round_state_machine(
            start_stage,
            round_repository, 
            mock_datetime)
        round_state_machine.next_stage()

        # Check assertions
        round_repository.update_round.assert_called_with(
            self.round_entity.RoundId,
            end_stage,
            self.start_time,
            Matching(lambda end_time: not enforce_end_time or end_time > self.start_time),
            self.round_entity.DrawingWordId)

    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.word_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_start_round_state_machine(self, round_repository, word_repository, mock_datetime):
        self.transition_helper(
            round_repository, 
            word_repository,
            mock_datetime, 
            None,
            RoundState.DRAWING)
        round_repository.update_room_round.assert_called_once()

    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.word_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_transition_to_critiquing(self, round_repository, word_repository, mock_datetime):
        self.transition_helper(
            round_repository, 
            word_repository,
            mock_datetime, 
            RoundState.DRAWING, 
            RoundState.CRITIQUING)

    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.word_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_transition_to_reviewing(self, round_repository, word_repository, mock_datetime):
        self.transition_helper(
            round_repository, 
            word_repository,
            mock_datetime, 
            RoundState.CRITIQUING, 
            RoundState.REVIEWING)

    @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.word_repository")
    @mock.patch("services.round_state_machine.round_repository")
    def test_transition_to_done(self, round_repository, word_repository, mock_datetime):
        word_to_remove = self.round_entity.DrawingWordId
        self.transition_helper(
            round_repository, 
            word_repository,
            mock_datetime, 
            RoundState.REVIEWING, 
            RoundState.DONE,
            enforce_end_time=False)
        round_repository.update_room_round.assert_called_once()
        word_repository.remove_word.assert_called_with(word_to_remove)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoundStateMachine)
    suite.debug()
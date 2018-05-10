#!/usr/bin/python

import unittest
import mock
import json
from services.round_state_machine import RoundStateMachine, RoundState
from test_utils import *
from datetime import datetime

class TestRoundStateMachine(unittest.TestCase):
    round = {
        "RoundId": 1,
        "RoomId": 1,
        "StageStateId": None,
        "StageStateStartTime": None,
        "StageStateEndTime": None,
        "DrawingWordId": 1
    }

    @mock.patch("services.round_state_machine.round_repository")
    def test_start_round_state_machine(self, round_repository):
        round_entity = Struct(**self.round)
        round_state_machine = RoundStateMachine(round_entity)
        round_state_machine.next_stage()
        round_repository.update_room_round.assert_called_once()
        round_repository.update_round.assert_called_once()

   @mock.patch("services.round_state_machine.datetime")
    @mock.patch("services.round_state_machine.round_repository")
    def test_go_through_rounds(self, round_repository, mock_datetime):
        round_entity = Struct(**self.round)
        start_time = datetime.datetime(2018, 05, 01, 12, 0, 0)
        mock_datetime.utc_now.return_value = start_time
        round_state_machine = RoundStateMachine(round_entity)
        round_state_machine.next_stage()
        round_state_machine.next_stage()
        expected_end_time = datetime.datetime(2018, 05, 01, 12, 0, 30)
        round_repository.update_round.assert_called_with(
            round_entity.RoundId,
            RoundState.CRITIQUING,
            start_time,
            expected_end_time,
            round_entity.DrawingWordId)
        round_state_machine.next_stage()
        round_repository.update_round.assert_called_once()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoundStateMachine)
    suite.debug()
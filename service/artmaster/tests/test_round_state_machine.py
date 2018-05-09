#!/usr/bin/python

import unittest
import mock
import json
from services.round_state_machine import RoundStateMachine
from test_utils import *

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoundStateMachine)
    suite.debug()
#!/usr/bin/python

import unittest 
import mock
import json
import app
from services import round_service
from .test_utils import *

class TestRoundService(unittest.TestCase):
    round = {
        "RoundId": 1,
        "RoomId": 1,
        "StageStateId": None,
        "StageStateStartTime": None,
        "StageStateEndTime": None,
        "DrawingWordId": 1
    }

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    @mock.patch("services.round_service.RoundStateMachine")
    @mock.patch("services.round_service.word_repository")
    @mock.patch("services.round_service.round_repository")
    def test_create_round(self, round_repository, word_repository, round_state_machine):
        round_repository.create_round.return_value = Struct(**self.round)
        mock_state_machine = mock.Mock()
        mock_state_machine.get_time_remaining.return_value = 30
        round_state_machine.return_value = mock_state_machine
        self.app.post("/round?roomId=1&userId=1")
        round_repository.create_round.assert_called_once()
        mock_state_machine.next_stage.assert_called_once()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()

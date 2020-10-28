#!/usr/bin/python

import unittest
import mock
import json
import app
from services import room_service
from .test_utils import *
from operator import eq

class TestRoomService(unittest.TestCase):
    room = {
        "RoomId": 1 ,
        "RoomCode": "ABCD",
        "OwnerUserId": 1,
        "CurrentRoundId": 1,
        "RoomUsers": [],
        "MinigameId": 1
    }

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    @mock.patch('services.room_service.room_user_repository')
    def test_add_user_to_room(self, room_user_repository):
        self.app.post("/room/1/user/1")
        room_user_repository.add_user_to_room.assert_called()

    @mock.patch('services.room_service.room_user_repository')
    def test_get_users_in_room(self, room_user_repository):
        self.app.get("/room/1/users")
        room_user_repository.get_users_in_room.assert_called()

    @mock.patch('services.room_service.room_user_repository')
    @mock.patch('services.room_service.room_repository')
    def test_create_room(self, room_repository, room_user_repository):
        room_repository.create_room.return_value = Struct(**self.room)
        room_created = self.app.post("/room?userId=1").data
        expected_room = dict_to_lower(self.room)
        actual_room = json.loads(room_created)
        self.assertEqual(actual_room, expected_room)
        room_user_repository.add_user_to_room.assert_called()

    @mock.patch('services.room_service.room_repository')
    def test_poll_room_by_room_code(self, room_repository):
        room_repository.get_room.return_value = Struct(**self.room)
        self.app.get("/room?roomCode=ABCD")
        room_repository.get_room.assert_called_with(None, "ABCD")

    @mock.patch('services.room_service.room_repository')
    def test_poll_room_by_room_id(self, room_repository):
        room_repository.get_room.return_value = Struct(**self.room)
        self.app.get("/room?roomId=1")
        room_repository.get_room.assert_called_with(1, None)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()



#!/usr/bin/python

import unittest
import mock
import json
import app
from services import rating_service
from .test_utils import *
from operator import eq

class TestRatingService(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        self.app.debug = True

    @mock.patch("services.rating_service.RoundStateMachine")
    @mock.patch("services.rating_service.image_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_set_rating(self, rating_repository, image_repository, round_state_machine):
        rating_repository.has_existing_rating.return_value = False
        rating_repository.create_rating.return_value = Struct(**{
            "RatingId": 1
        })
        self.app.post("/rating?imageId=1&rating=1&raterUserId=1&roundId=1")
        rating_repository.create_rating.assert_called()

    @mock.patch("services.rating_service.RoundStateMachine")
    @mock.patch("services.rating_service.image_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_set_rating_fails(self, rating_repository, image_repository, round_state_machine):
        rating_repository.has_existing_rating.return_value = True
        response = self.app.post("/rating?imageId=1&rating=1&raterUserId=1&roundId=1")
        error = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error["message"], "Cannot rate more than one thing per round")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()

#!/usr/bin/python

import unittest
import mock
import json
import sys
sys.path.append("../artmaster")
from artmaster.services import rating_service
from artmaster import app
from test_utils import *

class TestRatingService(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    @mock.patch("artmaster.services.rating_service.user_repository")
    @mock.patch("artmaster.services.rating_service.rating_repository")
    def test_get_ratings(self, rating_repository, user_repository):
        rating1 = Struct(**{
            "ImageId": 1,
            "Rating": 1
        })
        rating2 = Struct(**{
            "ImageId": 2,
            "Rating": 1
        })
        image1 = Struct(**{
            "ImageId": 1,
            "UserId": 1,
            "Location": "1.png"
        })
        image2 = Struct(**{
            "ImageId": 2,
            "UserId": 2,
            "Location": "2.png"
        })
        all_ratings = [
            (rating1, image1),
            (rating1, image1),
            (rating2, image2)
        ]
        rating_repository.get_ratings.return_value = all_ratings
        user = Struct(**{
            "UserId": 1,
            "Username": "1"
        })
        user_repository.get_user.return_value = user

        rating_response = self.app.get("/ratings?roundId=1").data
        actual_rating = json.loads(rating_response)
        expected_rating = {
            "roundId": 1,
            "winnerId": 1,
            "winnerUsername": "1",
            "winningImageLocation": "1.png"
        }
        expected_rating = Struct(**expected_rating)
        self.assertTrue(cmp(actual_rating, expected_rating))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()

#!/usr/bin/python

import unittest
import mock
import json
import app
from services import rating_service
from test_utils import *

class TestRatingService(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        self.app.debug = True

    @mock.patch("services.rating_service.user_repository")
    @mock.patch("services.rating_service.rating_repository")
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

    @mock.patch("services.rating_service.rating_repository")
    def test_set_rating(self, rating_repository):
        rating_repository.has_existing_rating.return_value = False
        rating_repository.create_rating.return_value = Struct(**{
            "RatingId": 1
        })
        self.app.post("/rating?imageId=1&rating=1&raterUserId=1")
        rating_repository.create_rating.assert_called()

    @mock.patch("services.rating_service.rating_repository")
    def test_set_rating(self, rating_repository):
        rating_repository.has_existing_rating.return_value = True
        response = self.app.post("/rating?imageId=1&rating=1&raterUserId=1")
        error = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error["message"], "Cannot rate more than one image per round")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()
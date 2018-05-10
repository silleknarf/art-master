
#!/usr/bin/python

import unittest
import mock
import json
import app
from services import rating_service
from test_utils import *

class TestRatingService(unittest.TestCase):
    rating1 = Struct(**{
        "ImageId": 1,
        "Rating": 1
    })
    rating2 = Struct(**{
        "ImageId": 2,
        "Rating": 1
    })
    image1 = Struct(**{
        "RoundId": 1,
        "ImageId": 1,
        "UserId": 1,
        "Location": "1.png"
    })
    image2 = Struct(**{
        "RoundId": 1,
        "ImageId": 2,
        "UserId": 2,
        "Location": "2.png"
    })
    expected_result1 =  {
        'roundId': 1, 
        'winnerUsername': '1', 
        'winningImageLocation': '1.png',
        'winnerId': 1
    }
    expected_result2 =  {
        'roundId': 1, 
        'winnerUsername': '2', 
        'winningImageLocation': '2.png',
        'winnerId': 2
    }

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        self.app.debug = True

    @mock.patch("services.rating_service.user_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_get_ratings(self, rating_repository, user_repository):
        ratings = [
            (self.rating1, self.image1),
            (self.rating1, self.image1),
            (self.rating2, self.image2)
        ]
        expected_results = [self.expected_result1]
        self.get_ratings_helper(rating_repository, user_repository, ratings, expected_results)

    @mock.patch("services.rating_service.user_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_get_ratings_draw(self, rating_repository, user_repository):
        ratings = [
            (self.rating1, self.image1),
            (self.rating2, self.image2)
        ]
        expected_results = [self.expected_result1, self.expected_result2]
        self.get_ratings_helper(rating_repository, user_repository, ratings, expected_results)

    @mock.patch("services.rating_service.user_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_get_ratings_none(self, rating_repository, user_repository):
        ratings = []
        expected_results = []
        self.get_ratings_helper(rating_repository, user_repository, ratings, expected_results)

    def get_ratings_helper(self, rating_repository, user_repository, ratings, expected_results):
        rating_repository.get_ratings.return_value = ratings
        def mock_get_user(user_id):
            return Struct(**{
                "UserId": user_id,
                "Username": str(user_id)
            })
        user_repository.get_user = mock_get_user
        rating_response = self.app.get("/ratings?roundId=1").data
        actual_rating = json.loads(rating_response)
        self.assertEqual(len(actual_rating), len(expected_results))
        for i, expected_result in enumerate(expected_results):
            self.assertTrue(cmp(actual_rating[i], expected_result) == 0)

    @mock.patch("services.rating_service.image_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_set_rating(self, rating_repository, image_repository):
        rating_repository.has_existing_rating.return_value = False
        rating_repository.create_rating.return_value = Struct(**{
            "RatingId": 1
        })
        self.app.post("/rating?imageId=1&rating=1&raterUserId=1")
        rating_repository.create_rating.assert_called()

    @mock.patch("services.rating_service.image_repository")
    @mock.patch("services.rating_service.rating_repository")
    def test_set_rating_fails(self, rating_repository, image_repository):
        rating_repository.has_existing_rating.return_value = True
        response = self.app.post("/rating?imageId=1&rating=1&raterUserId=1")
        error = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error["message"], "Cannot rate more than one image per round")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoomService)
    suite.debug()
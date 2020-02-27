import unittest
import mock
from repositories import rating_repository
from .test_utils import *
from operator import eq

class TestRatingRepository(unittest.TestCase):
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
        "ImageBase64": "1.png"
    })
    image2 = Struct(**{
        "RoundId": 1,
        "ImageId": 2,
        "UserId": 2,
        "ImageBase64": "2.png"
    })
    expected_result1 =  {
        'roundId': 1, 
        'winnerUsername': '1', 
        'winningImageBase64': '1.png',
        'winnerId': 1
    }
    expected_result2 =  {
        'roundId': 1, 
        'winnerUsername': '2', 
        'winningImageBase64': '2.png',
        'winnerId': 2
    }

    @mock.patch("repositories.rating_repository.user_repository")
    def test_get_ratings(self, user_repository):
        ratings = [
            (self.rating1, self.image1),
            (self.rating1, self.image1),
            (self.rating2, self.image2)
        ]
        expected_results = [self.expected_result1]
        self.get_ratings_repo_helper(rating_repository, user_repository, ratings, expected_results)

    @mock.patch("repositories.rating_repository.user_repository")
    def test_get_ratings_draw(self, user_repository):
        ratings = [
            (self.rating1, self.image1),
            (self.rating2, self.image2)
        ]
        expected_results = [self.expected_result1, self.expected_result2]
        self.get_ratings_repo_helper(rating_repository, user_repository, ratings, expected_results)

    @mock.patch("repositories.rating_repository.user_repository")
    def test_get_ratings_none(self, user_repository):
        ratings = []
        expected_results = []
        self.get_ratings_repo_helper(rating_repository, user_repository, ratings, expected_results)

    def get_ratings_repo_helper(self, rating_repository, user_repository, ratings, expected_results):
        def get_ratings(round_id):
            return ratings
        rating_repository.get_ratings = get_ratings
        def mock_get_user(user_id):
            return Struct(**{
                "UserId": user_id,
                "Username": str(user_id)
            })
        user_repository.get_user = mock_get_user
        rating_response = rating_repository.get_round_rating_results(1)
        actual_rating = rating_response
        self.assertEqual(len(actual_rating), len(expected_results))
        for i, expected_result in enumerate(expected_results):
            self.assertEqual(actual_rating[i], expected_result)
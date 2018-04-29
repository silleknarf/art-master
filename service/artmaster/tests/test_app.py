import unittest
import sys
import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
    
    def test_home(self):
        expected_string = "Welcome to the art-master api"
        self.assertEqual(self.app.get("/").data, expected_string)
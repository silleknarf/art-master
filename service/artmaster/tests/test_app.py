import app
import unittest

class TestApp(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_home(self):
        expected_string = b"Welcome to the Craicbox API"
        self.assertEqual(self.app.get("/").data, expected_string)

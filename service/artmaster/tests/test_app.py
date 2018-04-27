import unittest
from artmaster.app import *

class TestApp(unittest.TestCase):
    
    def test_home(self):
        expected_string = "Welcome to the art-master api"
        self.assertEqual(home(), expected_string)
import os
import unittest
import weatherdata

class TestWeatherData(unittest.TestCase):
    def setUp(self):
        self.apikey = os.environ["FORECASTIO_API_KEY"]

    def test_env(self):
        self.assertNotEqual(self.apikey, "")

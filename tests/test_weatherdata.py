import os
import unittest
import weatherdata

class TestWeatherData(unittest.TestCase):

    def setUp(self):
        forecastio_apikey = os.environ["FORECASTIO_API_KEY"]
        google_apikey = os.environ["GOOGLE_API_KEY"]
        self.wx = weatherdata.WeatherData(forecastio_apikey, google_apikey)

    def test_instantiation(self):
        self.assertIsNotNone(self.wx)

    def test_get_todays_stats_for_london(self):
        data = self.wx.get_stats('london')
        self.assertIsNotNone(data)
        self.assertIn('city', data)
        self.assertIn('datefrom', data)
        self.assertIn('dateto', data)

class TestGeocode(unittest.TestCase):

    def setUp(self):
        google_apikey = os.environ["GOOGLE_API_KEY"]
        self.geo = weatherdata.Geocode(google_apikey)

    def test_london(self):
        locations = self.geo.get('london')
        self.assertTrue(len(locations) > 0)
        name, lat, lng = locations[0]
        self.assertEqual(lat, 51.5073509)
        self.assertEqual(lng, -0.1277583)

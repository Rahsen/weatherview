import os
import unittest
import weatherdata
from datetime import datetime

class TestWeatherData(unittest.TestCase):

    def setUp(self):
        forecastio_apikey = os.environ["FORECASTIO_API_KEY"]
        google_apikey = os.environ["GOOGLE_API_KEY"]
        self.wx = weatherdata.WeatherData(forecastio_apikey, google_apikey)
        self.today = datetime.utcnow().date().isoformat()

    def test_instantiation(self):
        self.assertIsNotNone(self.wx)

    def test_get_todays_stats_for_london(self):
        results = self.wx.get_stats('london')
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['address'], 'London, UK')
        self.assertEqual(result['lat'], 51.5073509)
        self.assertEqual(result['lng'], -0.1277583)
        date_today = self.today
        stats = result['stats']
        self.assertEqual(stats['datefrom'], date_today)
        self.assertEqual(stats['dateto'], date_today)
        self._valid_temp(stats['temp_min'])
        self._valid_temp(stats['temp_max'])
        self._valid_temp(stats['temp_avg'])
        self._valid_temp(stats['temp_med'])
        self._valid_hum(stats['hum_min'])
        self._valid_hum(stats['hum_max'])
        self._valid_hum(stats['hum_avg'])
        self._valid_hum(stats['hum_med'])

    def test_get_dates_today(self):
        dates = self.wx._get_dates()
        self.assertEqual(len(dates), 1)
        self.assertEqual(dates[0], self.today)

    def test_get_dates_range(self):
        dates = self.wx._get_dates("2016-06-29", "2016-07-02")
        self.assertEqual(len(dates), 4)
        self.assertEqual(dates[0], "2016-06-29")
        self.assertEqual(dates[1], "2016-06-30")
        self.assertEqual(dates[2], "2016-07-01")
        self.assertEqual(dates[3], "2016-07-02")

    def test_get_raw_weather_data(self):
        dataset = self.wx._get_weather_raw('51.0', '0.0')
        self.assertEqual(len(dataset), 1)
        date, data = dataset[0]
        self.assertEqual(date, self.today)

    def _valid_temp(self, temp):
        self.assertTrue(temp > 0.0 and temp <= 35.0)

    def _valid_hum(self, hum):
        self.assertTrue(hum > 0.0 and hum <= 1.0)

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


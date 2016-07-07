import os
import requests

class Geocode:

    def __init__(self, google_apikey):
        self.apikey = google_apikey
        self.baseurl = r'https://maps.googleapis.com/maps/api/geocode'

    def get(self, city):
        locations = []
        url = self._makeurl(city)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            if data.get('status', '') == 'OK':
                results = data.get('results', [])
                locations = self._parse_locations(results)
        print(locations)
        return locations


    def _makeurl(self, address):
        url = r'{}/json?address={}&key={}'.format(self.baseurl, address, self.apikey)
        return url

    def _parse_locations(self, dataset):
        locations = []
        for data in dataset:
            address = data.get('formatted_address', None)
            geodata = data.get('geometry', {})
            locdata = geodata.get('location', {})
            lat = locdata.get('lat', '')
            lng = locdata.get('lng', '')

            if address != '' and lat != '' and lng != '':
                locations.append((address, lat, lng))
        return locations


class WeatherData:

    def __init__(self, forecastio_apikey, google_apikey):
        self.apikey = forecastio_apikey
        self.geo = Geocode(google_apikey)

    def get_stats(city, date=""):
        data = {}
        data['city'] = ""
        data['datefrom'] = ""
        data['dateto'] = ""
        return data

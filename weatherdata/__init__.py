import os
import requests
import statistics
from datetime import datetime, timedelta

class Geocode:

    def __init__(self, google_apikey):
        self.apikey = google_apikey
        self.baseurl = r'https://maps.googleapis.com/maps/api/geocode'

    def get(self, city):
        locations = []
        url = self._make_url(city)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            if data.get('status', '') == 'OK':
                results = data.get('results', [])
                locations = self._parse_locations(results)
        return locations


    def _make_url(self, address):
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


class WeatherStats:

    def __init__(self):
        self.clear()

    def clear(self):
        self._stats = {}
        self._temps = []
        self._hums = []

    def process_data(self, dataset):
        self.clear()
        for date, data in dataset:
            if 'datefrom' not in self._stats:
                self._stats['datefrom'] = date
            self._stats['dateto'] = date

            hourly_data = data.get('hourly', {})
            data_points = hourly_data.get('data', [])
            for data_point in data_points:
                if 'time' in data_point:
                    dp_date = datetime.fromtimestamp(data_point['time']).date().isoformat()
                    if dp_date == date:
                        self._process_data_point(data_point)

    def _process_data_point(self, data):
        if 'temperature' in data:
            self._temps.append(float(data['temperature']))
        if 'humidity' in data:
            self._hums.append(float(data['humidity']))

    def get(self):
        if len(self._temps) > 0:
            tmin = min(x for x in self._temps)
            tmax = max(x for x in self._temps)
            tavg = statistics.mean(self._temps)
            tmed = statistics.median(self._temps)
            data_temp = {}
            data_temp['labels'] = ['Min', 'Avg', 'Med', 'Max']
            data_temp['data'] = [tmin, tavg, tmed, tmax]
            self._stats['temperature'] = data_temp
        if len(self._hums) > 0:
            hmin = min(x for x in self._hums)
            hmax = max(x for x in self._hums)
            havg = statistics.mean(self._hums)
            hmed = statistics.median(self._hums)
            data_hum = {}
            data_hum['labels'] = ['Min', 'Avg', 'Med', 'Max']
            data_hum['data'] = [hmin, havg, hmed, hmax]
            self._stats['humidity'] = data_hum
        return self._stats


class WeatherData:

    def __init__(self, forecastio_apikey, google_apikey):
        self.apikey = forecastio_apikey
        self.geo = Geocode(google_apikey)
        self.baseurl = r'https://api.forecast.io/forecast'

    def get_stats(self, search, datefrom='', dateto=''):
        dataset = []
        locations = self.geo.get(search)
        if len(locations) > 0:
            address, lat, lng = locations[0]
            data = {}
            data['query'] = search
            data['address'] = address
            data['lat'] = lat
            data['lng'] = lng
            raw_data = self._get_weather_raw(lat, lng, datefrom, dateto)
            stats = WeatherStats()
            stats.process_data(raw_data)
            data['stats'] = stats.get()
            dataset.append(data)
        return dataset

    def _get_weather_raw(self, lat, lng, datefrom='', dateto=''):
        dates = self._get_dates(datefrom, dateto)
        dataset = []
        for date in dates:
            url = self._make_url(lat, lng, date)
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                dataset.append((date, data))
            else:
                print("Bad status code", r.status_code)
        return dataset

    def _get_dates(self, datefrom='', dateto=''):
        dates = []
        if datefrom == '':
            datefrom = datetime.utcnow()
            dateto = datefrom
        else:
            datefrom = datetime.strptime(datefrom, '%Y-%m-%d')
            dateto = datetime.strptime(dateto, '%Y-%m-%d')
        diff = dateto - datefrom
        for i in range(diff.days + 1):
            date = datefrom + timedelta(days=i)
            dates.append(date.date().isoformat())
        return dates

    def _make_url(self, lat, lng, date=''):
        url = r'{}/{}/{},{}'.format(self.baseurl, self.apikey, lat, lng)
        if date != '':
            url += r',{}T00:00:00-0000'.format(date)
        url += r'?units=si&exclude=currently,minutely,daily,alerts,flags'
        return url

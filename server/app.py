import os
from flask import Flask, render_template, request, jsonify
import weatherdata

print("starting flask app with name:", __name__)
app = Flask(__name__, static_folder="../dist")
app.config['DEBUG'] = (os.environ.get('DEBUG', 'False').lower() == "true")

apikey_google = os.environ['GOOGLE_API_KEY']
apikey_forecastio = os.environ['FORECASTIO_API_KEY']

wx = weatherdata.WeatherData(apikey_forecastio, apikey_google)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/wxstats/<address>', methods=['GET'])
def get_weather_stats(address):
    datefrom = ''
    dateto = ''
    print(request.args)
    if 'date' in request.args:
        datefrom = request.args['date']
        dateto = request.args['date']
    elif 'datefrom' in request.args and 'dateto' in request.args:
        datefrom = request.args['datefrom']
        dateto = request.args['dateto']

    data = {}
    data["query"] = address
    stats = []
    if datefrom == '':
        # Get Todays stats
        stats = wx.get_stats(address)
    else:
        # get stats in date range
        stats = wx.get_stats(address, datefrom, dateto)
    data['stats'] = stats
    return jsonify(data)

if __name__ == '__main__':
    app.run()

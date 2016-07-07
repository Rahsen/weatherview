import os
from flask import Flask, render_template

print("starting flask app with name:", __name__)
app = Flask(__name__, static_folder="../dist")
app.config['DEBUG'] = (os.environ.get('DEBUG', 'False').lower() == "true")

config = {}
config['GOOGLE_API_KEY'] = os.environ['GOOGLE_API_KEY']
config['FORECASTIO_API_KEY'] = os.environ['FORECASTIO_API_KEY']

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

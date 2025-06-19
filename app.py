from flask import Flask, render_template
import datetime
import requests
import time


app = Flask(__name__)

def is_kai_playing():
    kai_steam_id = 180760103
    url = f"https://api.opendota.com/api/players/{kai_steam_id}/recentMatches"
    response = requests.get(url)
    data = response.json()
    startTime = data[0]['start_time']
    dt = datetime.datetime.fromtimestamp(time.localtime(startTime))

    formatted_dt = dt.strftime("Played on %B %d at %I:%M %p")
    return formatted_dt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    return is_kai_playing()


if __name__ == "__main__":
    app.run(debug=True)


import requests
import datetime
import time

my_steam_id = 191236140
kai_steam_id = 180760103

url = f"https://api.opendota.com/api/players/{kai_steam_id}/recentMatches"

response = requests.get(url)

data = response.json()

startTime = data[0]['start_time']

startTimeReal = time.time() - startTime

# print(startTime)
# print(startTimeReal / 60)

dt = datetime.datetime.fromtimestamp(startTime)

formatted_dt = dt.strftime("Played on %B %d at %I:%M %p")

print(formatted_dt)

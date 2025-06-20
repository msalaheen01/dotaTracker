import requests
import datetime
import time
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# {'account_id': 418103605, 'hero_id': 128,


my_steam_id = 191236140
kai_steam_id = 180760103

# url = f"https://api.opendota.com/api/players/{kai_steam_id}/recentMatches"
# url2 = f"https://api.opendota.com/api/players/{kai_steam_id}/matches?limit=50"

# url3 = f"https://api.opendota.com/api/live"

get_heroes = f"https://api.opendota.com/api/heroes"

response_heroes = requests.get(get_heroes) 

heroes = response_heroes.json()


img_path = "hero_images/alchemist_lg.png"

print(os.path.exists(img_path))
img = Image.open(img_path)
img.show()


# for hero in heroes:
#     print(hero['id'], hero['name'])
#     hero_name = hero['name'].split()[1]
#     real_hero_name = hero_name.replace('npc_dota_hero_', '')

#     img = mpimg.imread(f"hero_images/alchemist_lg.png")
#     plt.imshow(img)
#     plt.show()

#     # openImage = Image.open(f"hero_images/{hero['name']}.webm")
#     # openImage.show()



# response3 = requests.get(url3)

# kai = response3.json()

# # print(response3.json()[:10])

# response = requests.get(url)
# response2 = requests.get(url2)
# matches = response2.json()

# # print(response2.json())
# data3 = response3.json()

# for n in data3:
#     players = n['players']
#     for player in players:
#         if player['account_id'] == 418103605:
#             print(player)
    
# print(matches[6])  

# data = response.json()
# data2 = response2.json()

# startTime = data[0]['start_time']

# startTimeReal = time.time() - startTime

# # print(startTime)
# # print(startTimeReal / 60)

# dt = datetime.datetime.fromtimestamp(startTime)

# formatted_dt = dt.strftime("Played on %B %d at %I:%M %p")

# print(formatted_dt)


# def is_currently_in_game(account_id):
#     url = f"https://api.opendota.com/api/players/{account_id}"
#     response = requests.get(url)
#     data = response.json()
#     print(data)
#     # Check if live_match field exists and has a value
#     return data.get("live_match") is not None

# print(is_currently_in_game(851507604))

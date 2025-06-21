import requests

hero_id = 120  # Pangolier
url = "https://api.opendota.com/api/live"
response = requests.get(url)
live_matches = response.json()

pangolier_players = []

for match in live_matches:
    for player in match.get("players", []):
        if player.get("hero_id") == hero_id:
            pangolier_players.append(player.get("account_id"))

# Print the account IDs (Steam32 IDs)
print("🎮 Pangolier is currently being played by:")
for account_id in pangolier_players:
    print(account_id)

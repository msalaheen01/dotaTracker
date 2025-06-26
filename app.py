from flask import Flask, render_template, jsonify
import datetime
import requests
import time
from datetime import datetime, timezone


app = Flask(__name__)



def is_kai_live():
    kai_steam_id = 180760103
    url = f"https://api.opendota.com/api/live"
    response = requests.get(url)
    data = response.json()

    for match in data:
        players = match['players']
        for player in players:
            if player['account_id'] == kai_steam_id:
                return True
    return False



def is_loss(match):
    is_radiant = match['player_slot'] < 128
    return match['radiant_win'] != is_radiant

def last_five_summary(matches):
    rows = []
    for i, m in enumerate(matches[:20], 1):
        slot   = m["player_slot"]
        is_rad = slot < 128
        team   = "Radiant" if is_rad else "Dire"
        win    = m["radiant_win"]
        result = "Win" if (win and is_rad) or (not win and not is_rad) else "Loss"
        rows.append(f"{i}. Match {m['match_id']} – {team} slot {slot} → {result}")
    return rows


from datetime import datetime, timezone

from datetime import datetime, timezone

def estimate_queue_likelihood(matches):
    now = datetime.now(timezone.utc).timestamp()
    hour = datetime.now(timezone.utc).hour
    day = datetime.now(timezone.utc).strftime('%A')

    score = 0
    log = []

    # 🔔 Highlight last match time
    last_match = matches[0]
    last_end = last_match["start_time"] + last_match["duration"]
    minutes_ago = int((now - last_end) / 60)

    if minutes_ago < 60:
        log.append(f"🚨 <b>Last match ended {minutes_ago} minute(s) ago</b>")
    elif minutes_ago < 120:
        log.append(f"⏰ Last match ended about {minutes_ago // 60} hour ago")
    else:
        log.append(f"⏰ Last match ended about {minutes_ago // 60} hours ago")

    # 🕐 Time-of-day & weekday bonuses
    active_hours = {*range(22, 24), *range(0, 4)}  # 10 PM–3 AM UTC
    active_days = {"Monday", "Tuesday", "Saturday"}

    if hour in active_hours:
        score += 20
        log.append(f"🕐 Active hour ({hour} UTC): +20")
    else:
        log.append(f"🕐 Inactive hour ({hour} UTC): +0")

    if day in active_days:
        score += 20
        log.append(f"📅 Active day ({day}): +20")
    else:
        log.append(f"📅 Inactive day ({day}): +0")

    # 🎮 Recent match recency scoring (diminishing scale)
    recent_pts = 0
    recent_games = 0

    for m in matches:
        match_end = m["start_time"] + m["duration"]
        ago = now - match_end
        mins = int(ago // 60)

        if ago <= 5 * 60:
            recent_pts += 80
            log.append(f"⚡️ Last game ended {mins} min ago → +50")
        elif ago <= 10 * 60:
            recent_pts += 40
            log.append(f"⚡️ Last game ended {mins} min ago → +40")
        elif ago <= 20 * 60:
            recent_pts += 20
            log.append(f"⚡️ Last game ended {mins} min ago → +30")
        elif ago <= 30 * 60:
            recent_pts += 10
            log.append(f"⌛️ Last game ended {mins} min ago → +20")
        elif ago <= 60 * 60:
            recent_pts += 5
            log.append(f"⌛️ Last game ended {mins} min ago → +10")
        elif ago <= 120 * 60:
            recent_pts += 2
            log.append(f"⌛️ Last game ended {mins} min ago → +5")

        if ago <= 2 * 3600:
            recent_games += 1

    score += min(recent_pts, 50)
    log.append(f"🎮 Played {recent_games} time(s) in last 2h → +{min(recent_pts, 50)}")

    # 💀 Loss streak in last 5 games
    loss_count = 0
    for match in matches[:5]:
        slot = match["player_slot"]
        is_radiant = slot < 128
        won = match["radiant_win"]
        is_win = (won and is_radiant) or (not won and not is_radiant)
        if not is_win:
            loss_count += 1

    loss_streak_score = min(loss_count * 5, 20)
    log.append(f"💀 Losses in last 5 games: {loss_count} → +{loss_streak_score}")
    score += loss_streak_score

    return min(score, 100), log, last_five_summary(matches)


def format_time_ago(minutes):
    """Format time ago in days if > 24 hours, hours and minutes if > 60 minutes, otherwise just minutes"""
    if minutes >= 1440:  # 24 hours = 1440 minutes
        days = minutes // 1440
        return f"{days}d ago"
    elif minutes >= 60:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours}h ago"
        else:
            return f"{hours}h {remaining_minutes}m ago"
    else:
        return f"{minutes}m ago"


def get_matches():
    kai_steam_id = 180760103
    url = f"https://api.opendota.com/api/players/{kai_steam_id}/matches?limit=50"
    response = requests.get(url)
    matches = response.json()
    return matches

def is_kai_playing():
    kai_steam_id = 180760103
    url = f"https://api.opendota.com/api/players/{kai_steam_id}/recentMatches"
    response = requests.get(url)
    data = response.json()
    startTime = data[0]['start_time']
    dt = datetime.datetime.fromtimestamp(startTime)

    formatted_dt = dt.strftime("Played on %B %d at %I:%M %p")
    return formatted_dt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    matches_data = get_matches()
    score, log, last5 = estimate_queue_likelihood(matches_data)

    status = (
        f"🔥 Likely queueing! ({score}%)" if score > 70 else
        f"🤔 Maybe queueing. ({score}%)"  if score > 40 else
        f"❄️ Likely not playing. ({score}%)"
    )

    details_log = "<br>".join(log)

    hero_data = requests.get("https://api.opendota.com/api/heroes").json()
    hero_map = {hero["id"]: hero["name"].replace("npc_dota_hero_", "") for hero in hero_data}

    matches_list = []
    for m in matches_data:
        hero_id = m.get('hero_id')
        hero_name = hero_map.get(hero_id, "unknown")
        win_class = "win" if not is_loss(m) else "loss"

        matches_list.append({
            'match_id': m.get('match_id'),
            'hero_name': hero_name.replace("_", " ").title(),
            'kills': m.get('kills'),
            'deaths': m.get('deaths'),
            'assists': m.get('assists'),
            'duration': round(m.get('duration', 0) / 60, 1),
            'ago': int((time.time() - m.get('start_time', time.time())) / 60),
            'ago_display': format_time_ago(int((time.time() - m.get('start_time', time.time())) / 60)),
            'win_class': win_class,
            'result_text': "Win" if win_class == "win" else "Loss",
            'img_url': f"https://cdn.dota2.com/apps/dota2/images/heroes/{hero_name}_lg.png"
        })

    return jsonify({
        'status': status,
        'log': details_log,
        'matches': matches_list,
        'last5_title': "Last 5 Matches:"
    })

@app.route('/checkTwo')
def checkTwo():
    var = is_kai_live()
    return f"Is Kai playing? {var}"

if __name__ == "__main__":
    app.run(debug=True)


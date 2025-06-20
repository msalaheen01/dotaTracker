import os
import requests


dota_heroes = [
    'abaddon', 'abyssal_underlord', 'alchemist', 'ancient_apparition', 'antimage', 'arc_warden', 'axe', 'bane',
    'batrider', 'beastmaster', 'bloodseeker', 'bounty_hunter', 'brewmaster', 'bristleback', 'broodmother', 'centaur',
    'chaos_knight', 'chen', 'clinkz', 'crystal_maiden', 'dark_seer', 'dark_willow', 'dawnbreaker', 'dazzle',
    'death_prophet', 'disruptor', 'doom_bringer', 'dragon_knight', 'drow_ranger', 'earth_spirit', 'earthshaker',
    'elder_titan', 'ember_spirit', 'enchantress', 'enigma', 'faceless_void', 'furion', 'grimstroke', 'gyrocopter',
    'hoodwink', 'huskar', 'invoker', 'jakiro', 'juggernaut', 'keeper_of_the_light', 'kunkka', 'legion_commander',
    'leshrac', 'lich', 'life_stealer', 'lina', 'lion', 'lone_druid', 'luna', 'lycan', 'magnataur', 'marci', 'mars',
    'medusa', 'meepo', 'mirana', 'monkey_king', 'morphling', 'muerta', 'naga_siren', 'necrolyte', 'nevermore',
    'night_stalker', 'nyx_assassin', 'obsidian_destroyer', 'ogre_magi', 'omniknight', 'oracle', 'pangolier',
    'phantom_assassin', 'phantom_lancer', 'phoenix', 'primal_beast', 'puck', 'pudge', 'pugna', 'queenofpain',
    'rattletrap', 'razor', 'riki', 'rubick', 'sand_king', 'shadow_demon', 'shadow_shaman', 'shredder', 'silencer',
    'skeleton_king', 'skywrath_mage', 'slardar', 'slark', 'snapfire', 'sniper', 'spectre', 'spirit_breaker',
    'storm_spirit', 'sven', 'techies', 'templar_assassin', 'terrorblade', 'tidehunter', 'tinker', 'tiny', 'treant',
    'troll_warlord', 'tusk', 'undying', 'ursa', 'vengefulspirit', 'venomancer', 'viper', 'visage', 'void_spirit',
    'warlock', 'weaver', 'windrunner', 'winter_wyvern', 'wisp', 'witch_doctor', 'zuus' , 'kez' , 'ringmaster'
]


os.makedirs("hero_images", exist_ok=True)

url = "https://cdn.dota2.com/apps/dota2/images/heroes/{}_lg.png"

for name in dota_heroes:
    hero_url = url.format(name)
    response = requests.get(hero_url)
    if response.status_code == 200:
        with open(f"hero_images/{name}_lg.png", "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {name}")
    else:
        print(f"Failed to download: {name} (Status code: {response.status_code})")
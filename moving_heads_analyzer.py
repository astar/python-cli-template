#!/usr/bin/env python3
"""Moving Head timeline generátor používající systematickou strukturu."""

import xml.etree.ElementTree as ET
from pathlib import Path
import configparser
import math
import random

def load_systematic_moving_heads():
    """Načte Moving Head definice ze systematické struktury."""

    import json
    structure_path = Path("generated_scenes_systematic/systematic_structure.json")
    if not structure_path.exists():
        print("❌ Systematic structure not found!")
        return {}

    with open(structure_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Získej Moving Head fixtures
    mh_fixtures = {fid: fixture for fid, fixture in data['fixtures'].items()
                   if fixture['light_type'] == 'moving_head'}

    print(f"🔍 Loaded {len(mh_fixtures)} Moving Head fixtures from systematic structure")

    capabilities = {
        'colors': list(data['colors'].keys()),
        'fixtures': mh_fixtures,
        'effects': list(data['effects'].keys())
    }

    return capabilities

def create_systematic_moving_head_show(capabilities, output_path: str):
    """Vytvoří dynamickou Moving Head show s inteligentními efekty."""

    print(f"\n🎭 Creating Moving Head show...")

    # Vytvoř timeline config
    config = configparser.ConfigParser()

    # Správný Infinit Maximus formát
    config['Params'] = {
        'Version': '0.2',
        'CommentTimeLine': '0',
        'LightTimeLines': '10',
        'MediaTimeLines': '1',
        'ShowWaveForm': '1',
        'MaxTime': '0:30:00',
        'Zoom': '0',
        'TimeLine_1': 'V I D E O   P I C T U R E   T I M E L I N E',
        'TimeLine_2': 'A U D I O   T I M E L I N E',
        'TimeLine_3': 'L I G H T   S C E N E   T I M E L I N E   #   1',
        'TimeLine_4': 'L I G H T   S C E N E   T I M E L I N E   #   2',
        'TimeLine_5': 'L I G H T   S C E N E   T I M E L I N E   #   3',
        'TimeLine_6': 'L I G H T   S C E N E   T I M E L I N E   #   4',
        'TimeLine_7': 'L I G H T   S C E N E   T I M E L I N E   #   5',
        'TimeLine_8': 'L I G H T   S C E N E   T I M E L I N E   #   6',
        'TimeLine_9': 'L I G H T   S C E N E   T I M E L I N E   #   7',
        'TimeLine_10': 'L I G H T   S C E N E   T I M E L I N E   #   8',
        'TimeLine_11': 'L I G H T   S C E N E   T I M E L I N E   #   9',
        'TimeLine_12': 'L I G H T   S C E N E   T I M E L I N E   #   10'
    }

    # Audio track
    config['Event_0'] = {
        'TimeLineIndex': '2',
        'StartTime': '0:00:00.0',
        'Path': 'Music/Kraviny-ze-sauny/Kokoti.mp3',
        'Length': '0:04:13.6'
    }

    # Show parametry
    song_duration = 253.7
    event_counter = 1

    # Dostupné barvy/efekty ze systematické struktury
    available_colors = capabilities['colors']
    available_fixtures = list(capabilities['fixtures'].keys())
    print(f"🎨 Available systematic colors: {available_colors}")
    print(f"🎯 Available Moving Head fixtures: {len(available_fixtures)}")

    if not available_colors or not available_fixtures:
        print("❌ No Moving Head capabilities found!")
        return

    # 1. Pomalé sweep efekty - plynulé otáčení
    print("🌀 Adding sweep effects...")
    for sweep_time in [10, 30, 60, 90, 120, 150, 180, 210]:
        if sweep_time < song_duration - 10:
            color = random.choice(available_colors)
            # Use systematic scene path for Moving Heads
            fixture_id = available_fixtures[0]  # Use first MH for sweep
            fixture = capabilities['fixtures'][fixture_id]
            fixture_key = f"{fixture['light_type']}_{fixture_id[-2:]}"
            scene_path = f"generated_scenes_systematic/individual/{fixture_key}/{color}_fade_in.scex"

            minutes = int(sweep_time // 60)
            seconds = sweep_time % 60

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '4',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': scene_path,
                'Length': '0:00:08.0',  # 8 sekund sweep
                'Speed': '30',  # Pomalé
                'SpeedType': '2'
            }
            event_counter += 1

            # OFF po sweep
            off_time = sweep_time + 8
            off_minutes = int(off_time // 60)
            off_seconds = off_time % 60

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '4',
                'StartTime': f'0:{off_minutes:02d}:{off_seconds:04.1f}',
                'Path': 'OFF'
            }
            event_counter += 1

    # 2. Rychlé chase efekty - střídání barev
    print("⚡ Adding chase effects...")
    beat_interval = 60.0 / 143.6  # BPM 143.6

    for chase_start in [20, 50, 80, 110, 140, 170, 200, 230]:
        if chase_start < song_duration - 15:
            # 4 rychlé změny barev
            for i in range(4):
                chase_time = chase_start + i * beat_interval * 2  # Každé 2 beaty
                color = available_colors[i % len(available_colors)]
                # Cycle through different MH fixtures
                fixture_id = available_fixtures[i % len(available_fixtures)]
                fixture = capabilities['fixtures'][fixture_id]
                fixture_key = f"{fixture['light_type']}_{fixture_id[-2:]}"
                scene_path = f"generated_scenes_systematic/individual/{fixture_key}/{color}_pulse.scex"

                minutes = int(chase_time // 60)
                seconds = chase_time % 60

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '5',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': scene_path,
                    'Length': '0:00:01.5',  # 1.5s každý
                    'Speed': '80',
                    'SpeedType': '2'
                }
                event_counter += 1

    # 3. Bass responsive efekty - na silné beaty
    print("🥁 Adding bass responsive effects...")
    bass_times = [25, 45, 65, 85, 105, 125, 145, 165, 185, 205, 225]

    for bass_time in bass_times:
        if bass_time < song_duration - 5:
            # Náhodný dramatický efekt
            dramatic_colors = [c for c in available_colors if c in ['red', 'blue', 'purple', 'white_cool']]
            if dramatic_colors:
                color = random.choice(dramatic_colors)
                # Use zone-level scene for dramatic effect (all MH together)
                scene_path = f"generated_scenes_systematic/zones/ceiling/{color}_strobe_fast.scex"

                minutes = int(bass_time // 60)
                seconds = bass_time % 60

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '6',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': scene_path,
                    'Length': '0:00:02.0',  # 2s drama
                    'Speed': '100',  # Plná rychlost
                    'SpeedType': '2'
                }
                event_counter += 1

    # 4. Ambient background - jemné barvy na pozadí
    print("🌅 Adding ambient background...")
    for ambient_start in [5, 35, 70, 100, 130, 160, 190, 220]:
        if ambient_start < song_duration - 20:
            # Jemné barvy
            gentle_colors = [c for c in available_colors if c in ['blue', 'green', 'cyan', 'purple']]
            if gentle_colors:
                color = random.choice(gentle_colors)
                # Use individual fixture for ambient
                fixture_id = random.choice(available_fixtures)
                fixture = capabilities['fixtures'][fixture_id]
                fixture_key = f"{fixture['light_type']}_{fixture_id[-2:]}"
                scene_path = f"generated_scenes_systematic/individual/{fixture_key}/{color}_static.scex"

                minutes = int(ambient_start // 60)
                seconds = ambient_start % 60

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '7',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': scene_path,
                    'Length': '0:00:15.0',  # 15s ambient
                    'Speed': '20',  # Velmi pomalé
                    'SpeedType': '2',
                    'FadeIn': '3000',
                    'FadeOut': '3000'
                }
                event_counter += 1

    # Uložit timeline
    with open(output_path, 'w', encoding='utf-8') as f:
        config.write(f)

    # Oprav CamelCase formatting
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = {
        'version =': 'Version =',
        'commenttimeline =': 'CommentTimeLine =',
        'lighttimelines =': 'LightTimeLines =',
        'mediatimelines =': 'MediaTimeLines =',
        'showwaveform =': 'ShowWaveForm =',
        'maxtime =': 'MaxTime =',
        'zoom =': 'Zoom =',
        'timeline_': 'TimeLine_',
        'timelineindex =': 'TimeLineIndex =',
        'starttime =': 'StartTime =',
        'path =': 'Path =',
        'length =': 'Length =',
        'speed =': 'Speed =',
        'speedtype =': 'SpeedType =',
        'fadein =': 'FadeIn =',
        'fadeout =': 'FadeOut ='
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Moving Head show created: {output_path}")
    print(f"   Events: {event_counter}")
    print(f"   Effects: Sweeps, Chases, Bass responses, Ambient")
    print(f"   Colors: {len(available_colors)} variations")

def print_capabilities_summary(capabilities):
    """Vypíše přehled možností Moving Head světel."""

    print(f"\n📊 Moving Head Capabilities Summary:")
    print(f"   Colors/Effects: {len(capabilities['colors'])}")
    print(f"   Parameters: {len(capabilities['parameters'])}")
    print(f"   Total analyzed effects: {len(capabilities['effects'])}")

    print(f"\n🎨 Available Colors/Effects:")
    for color, path in capabilities['colors'].items():
        print(f"   {color}: {path}")

    print(f"\n🎛️  DMX Parameters:")
    for param in sorted(capabilities['parameters']):
        if param in capabilities['ranges']:
            range_info = capabilities['ranges'][param]
            print(f"   {param}: {range_info['min']}-{range_info['max']}")

    print(f"\n🔧 Parameter Analysis:")
    if 'pan' in capabilities['parameters']:
        print("   ✅ Pan (horizontal rotation)")
    if 'tilt' in capabilities['parameters']:
        print("   ✅ Tilt (vertical rotation)")
    if 'color' in capabilities['parameters']:
        print("   ✅ Color mixing")
    if 'gobo' in capabilities['parameters']:
        print("   ✅ Gobo patterns")
    if 'prism' in capabilities['parameters']:
        print("   ✅ Prism effects")
    if 'focus' in capabilities['parameters']:
        print("   ✅ Focus control")
    if 'dimmer' in capabilities['parameters']:
        print("   ✅ Dimmer control")
    if 'shutter' in capabilities['parameters']:
        print("   ✅ Shutter/strobe")

if __name__ == "__main__":
    # Načti systematické Moving Head definice
    capabilities = load_systematic_moving_heads()

    if capabilities and capabilities['colors']:
        # Vytvoř systematickou Moving Head show
        create_systematic_moving_head_show(capabilities, "Kokoti_SYSTEMATIC_MOVING_HEADS.tml")
        print(f"\n🎭 Systematic Moving Head show uses:")
        print(f"   {len(capabilities['fixtures'])} Moving Head fixtures")
        print(f"   {len(capabilities['colors'])} systematic colors")
        print(f"   {len(capabilities['effects'])} systematic effects")
    else:
        print("❌ No systematic Moving Head structure found!")
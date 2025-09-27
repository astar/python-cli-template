#!/usr/bin/env python3
"""Inteligentní beat-responsive timeline používající systematickou strukturu scex souborů."""

import sys
import configparser
import json
from pathlib import Path

def load_systematic_structure():
    """Načte systematickou strukturu scex souborů."""

    structure_path = Path("generated_scenes_systematic/systematic_structure.json")
    if not structure_path.exists():
        print(f"❌ Systematic structure not found: {structure_path}")
        print("   Run systematic_scex_generator.py first!")
        return None

    with open(structure_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📁 Loaded systematic structure:")
    print(f"   Fixtures: {len(data['fixtures'])}")
    print(f"   Colors: {len(data['colors'])}")
    print(f"   Effects: {len(data['effects'])}")

    return data

def get_systematic_scene_path(fixtures, fixture_id, color, effect="static"):
    """Vytvoří cestu k systematickému scex souboru."""

    fixture = fixtures[fixture_id]
    fixture_key = f"{fixture['light_type']}_{fixture_id[-2:]}"

    return f"generated_scenes_systematic/individual/{fixture_key}/{color}_{effect}.scex"

def create_intelligent_beat_timeline(output_path: str):
    """Vytvoří timeline s systematickou strukturou scex souborů."""

    print("🔍 Loading systematic structure...")
    data = load_systematic_structure()
    if not data:
        return

    fixtures = data['fixtures']
    colors = list(data['colors'].keys())

    # Získej LED Wall fixtures
    led_wall_fixtures = [fid for fid, fixture in fixtures.items()
                        if fixture['light_type'] == 'led_wall']

    print(f"\n🎯 Using LED Wall fixtures: {len(led_wall_fixtures)}")
    print(f"🎨 Available colors: {colors[:6]}...")

    # Seřaď fixtures podle pozice pro wave efekt
    led_positions = [(fid, fixtures[fid]['position']) for fid in led_wall_fixtures]
    led_positions.sort(key=lambda x: (x[1][0], x[1][1]))  # sort by x, y

    available_colors = colors[:6]  # Use first 6 systematic colors

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

    # Beat parametry
    beat_interval = 60.0 / 143.6  # BPM 143.6
    song_duration = 253.7

    event_counter = 1
    beat_counter = 0

    print(f"🎵 Creating beat timeline with {beat_interval:.3f}s intervals...")

    for beat_time_raw in [i * beat_interval for i in range(int(song_duration / beat_interval))]:
        if beat_time_raw >= song_duration - 1:
            break

        # Který fixture z dostupných
        fixture_index = beat_counter % len(led_positions)
        fixture_id, position = led_positions[fixture_index]

        # Která barva
        color_index = (beat_counter // len(led_positions)) % len(available_colors)
        color_name = available_colors[color_index]

        # Vytvoř cestu k systematickému scex souboru
        scene_file = get_systematic_scene_path(fixtures, fixture_id, color_name, "static")

        # Formátuj čas
        minutes = int(beat_time_raw // 60)
        seconds = beat_time_raw % 60

        # Light event
        config[f'Event_{event_counter}'] = {
            'TimeLineIndex': '3',
            'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
            'Path': scene_file,
            'Length': '0:00:00.3',
            'Speed': '100',
            'SpeedType': '2'
        }
        event_counter += 1

        # OFF event
        off_time = beat_time_raw + 0.3
        off_minutes = int(off_time // 60)
        off_seconds = off_time % 60

        config[f'Event_{event_counter}'] = {
            'TimeLineIndex': '3',
            'StartTime': f'0:{off_minutes:02d}:{off_seconds:04.1f}',
            'Path': 'OFF'
        }
        event_counter += 1
        beat_counter += 1

        # Progress
        if beat_counter % 50 == 0:
            print(f"  Beat {beat_counter}: Fixture {fixture_id[-4:]}, Color {color_name}")

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
        'speedtype =': 'SpeedType ='
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Systematic beat timeline created: {output_path}")
    print(f"   Events: {event_counter} (light + OFF)")
    print(f"   Fixtures: {len(led_positions)} LED Wall fixtures")
    print(f"   Colors: {len(available_colors)} systematic colors")
    print(f"   Duration: {song_duration}s at {143.6} BPM")
    print(f"   Using systematic structure with precise positioning")

if __name__ == "__main__":
    create_intelligent_beat_timeline("Kokoti_INTELLIGENT_BEAT_SPOTS.tml")
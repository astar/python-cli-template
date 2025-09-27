#!/usr/bin/env python3
"""Systematický enhancer pro timeline - používá systematickou strukturu scex souborů."""

import sys
import configparser
import math
import json
import random
from pathlib import Path

def load_systematic_structure():
    """Načte systematickou strukturu."""
    structure_path = Path("generated_scenes_systematic/systematic_structure.json")
    if not structure_path.exists():
        print("❌ Systematic structure not found!")
        return None

    with open(structure_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_systematic_scene_path(fixtures, fixture_id, color, effect):
    """Vytvoří cestu k systematickému scex souboru."""
    fixture = fixtures[fixture_id]
    fixture_key = f"{fixture['light_type']}_{fixture_id[-2:]}"
    return f"generated_scenes_systematic/individual/{fixture_key}/{color}_{effect}.scex"

def enhance_timeline_systematic(input_path: str, output_path: str):
    """Přidá systematické dynamické efekty do existující timeline."""

    # Načti systematickou strukturu
    data = load_systematic_structure()
    if not data:
        print("❌ Cannot enhance without systematic structure!")
        return

    fixtures = data['fixtures']
    colors = list(data['colors'].keys())

    # Kategorizuj fixtures
    led_walls = [fid for fid, f in fixtures.items() if f['light_type'] == 'led_wall']
    ceiling_spots = [fid for fid, f in fixtures.items() if f['light_type'] == 'ceiling_spot']
    moving_heads = [fid for fid, f in fixtures.items() if f['light_type'] == 'moving_head']

    print(f"📡 Using systematic fixtures:")
    print(f"   LED Walls: {len(led_walls)}")
    print(f"   Ceiling Spots: {len(ceiling_spots)}")
    print(f"   Moving Heads: {len(moving_heads)}")
    print(f"   Colors: {len(colors)}")

    # Načti existující timeline
    config = configparser.ConfigParser()
    config.read(input_path, encoding='utf-8')

    # Počet existujících eventů
    existing_events = len([s for s in config.sections() if s.startswith('Event_')])

    # Přidej systematické dynamické efekty
    event_counter = existing_events

    # BPM 143.6 = beat každých ~0.42 sekund
    beat_interval = 60.0 / 143.6
    song_duration = 253.7  # sekundy

    # 1. Systematic strobe efekty na silné beaty
    for beat in range(0, int(song_duration / beat_interval), 8):  # Every 8th beat
        beat_time = beat * beat_interval
        if beat_time < song_duration - 5:
            minutes = int(beat_time // 60)
            seconds = beat_time % 60

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '3',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': 'generated_scenes_systematic/zones/ceiling/white_warm_strobe_fast.scex',
                'Length': '0:00:00.5',
                'Speed': '100',
                'SpeedType': '2'
            }
            event_counter += 1

    # 2. Systematic wave efekty přes LED walls
    for wave in range(0, int(song_duration), 12):  # Každých 12 sekund
        wave_colors = ['blue', 'cyan', 'purple', 'magenta']
        wave_color = random.choice([c for c in colors if c in wave_colors])

        # Seřaď LED walls podle pozice
        led_positions = [(fid, fixtures[fid]['position']) for fid in led_walls]
        led_positions.sort(key=lambda x: x[1][0])  # Sort by x position

        for i, (fixture_id, position) in enumerate(led_positions):
            wave_time = wave + i * 0.2  # 200ms delay between fixtures
            if wave_time < song_duration - 2:
                minutes = int(wave_time // 60)
                seconds = wave_time % 60

                scene_path = get_systematic_scene_path(fixtures, fixture_id, wave_color, 'fade_in')

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '4',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': scene_path,
                    'Length': '0:00:01.5',
                    'Speed': '70',
                    'SpeedType': '2',
                    'FadeIn': '300',
                    'FadeOut': '500'
                }
                event_counter += 1

    # 3. Systematic ceiling chase - kruhový efekt
    for chase_start in range(20, int(song_duration), 16):  # Každých 16 sekund
        chase_colors = ['red', 'orange', 'yellow']
        chase_color = random.choice([c for c in colors if c in chase_colors])

        # Seřaď ceiling spots v kruhu
        ceiling_positions = [(fid, fixtures[fid]['position']) for fid in ceiling_spots]
        # Calculate angles from center for circular sorting
        center_x, center_y = 4.25, 3.8
        ceiling_circle = []
        for fid, (x, y, z) in ceiling_positions:
            angle = math.atan2(y - center_y, x - center_x)
            ceiling_circle.append((fid, angle))
        ceiling_circle.sort(key=lambda x: x[1])  # Sort by angle

        for i, (fixture_id, angle) in enumerate(ceiling_circle[:8]):  # First 8 spots
            chase_time = chase_start + i * beat_interval / 3  # Third beat intervals
            if chase_time < song_duration - 2:
                minutes = int(chase_time // 60)
                seconds = chase_time % 60

                scene_path = get_systematic_scene_path(fixtures, fixture_id, chase_color, 'pulse')

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '5',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': scene_path,
                    'Length': '0:00:00.8',
                    'Speed': '90',
                    'SpeedType': '2'
                }
                event_counter += 1

    # 4. Systematic bass explosions
    bass_times = [25, 55, 85, 115, 145, 175, 205, 235]  # Strategic bass moments
    for bass_time in bass_times:
        if bass_time < song_duration - 3:
            minutes = int(bass_time // 60)
            seconds = bass_time % 60

            # All walls red flash
            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '6',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': 'generated_scenes_systematic/zones/walls/red_strobe_slow.scex',
                'Length': '0:00:01.5',
                'Speed': '100',
                'SpeedType': '2'
            }
            event_counter += 1

    # 5. Systematic Moving Head choreography
    for mh_start in range(35, int(song_duration), 20):  # Každých 20 sekund
        if mh_start < song_duration - 8 and moving_heads:
            dramatic_colors = [c for c in colors if c in ['red', 'blue', 'purple', 'white_cool']]
            if dramatic_colors:
                mh_color = random.choice(dramatic_colors)
                minutes = int(mh_start // 60)
                seconds = mh_start % 60

                # Zone-level Moving Head effect
                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '7',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': f'generated_scenes_systematic/zones/ceiling/{mh_color}_fade_in.scex',
                    'Length': '0:00:05.0',
                    'Speed': '50',
                    'SpeedType': '2',
                    'FadeIn': '1000',
                    'FadeOut': '1500'
                }
                event_counter += 1

    # 6. Systematic random sparkles - jednotlivé fixtures blikají
    for sparkle_time in [t * beat_interval for t in range(0, int(song_duration / beat_interval), 6)]:
        if sparkle_time < song_duration - 1:
            # Random fixture, random color
            random_fixture = random.choice(led_walls + ceiling_spots[:6])  # Mix of types
            sparkle_colors = ['white_warm', 'yellow', 'cyan', 'magenta']
            sparkle_color = random.choice([c for c in colors if c in sparkle_colors])

            minutes = int(sparkle_time // 60)
            seconds = sparkle_time % 60

            scene_path = get_systematic_scene_path(fixtures, random_fixture, sparkle_color, 'strobe_fast')

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '8',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': scene_path,
                'Length': '0:00:00.3',
                'Speed': '100',
                'SpeedType': '2'
            }
            event_counter += 1

    # Uložit enhanced timeline
    with open(output_path, 'w', encoding='utf-8') as f:
        config.write(f)

    # Fix CamelCase formatting
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = {
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

    print(f"\n✅ Systematically enhanced timeline saved: {output_path}")
    print(f"   Added {event_counter - existing_events} systematic effects!")
    print(f"   Total events: {event_counter}")
    print(f"   Effect types: Strobe, Wave, Chase, Bass, Moving Head, Sparkles")
    print(f"   Using systematic structure with {len(fixtures)} fixtures")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python enhance_timeline_systematic.py <input.tml> <output.tml>")
        print("Note: Uses systematic scex structure!")
        sys.exit(1)

    enhance_timeline_systematic(sys.argv[1], sys.argv[2])
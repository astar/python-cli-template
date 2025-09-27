#!/usr/bin/env python3
"""Beat-responsive spots - správný Infinit Maximus formát."""

import sys
import configparser
import math

def create_infinit_beat_spots_timeline(output_path: str):
    """Vytvoří timeline s beat-responsive bodovkami ve správném Infinit Maximus formátu."""

    # Vytvoř novou timeline s CamelCase formátem
    config = configparser.ConfigParser()

    # Správná [Params] sekce - CamelCase!
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

    # BPM 143.6 = beat každých ~0.42 sekund
    beat_interval = 60.0 / 143.6
    song_duration = 253.7  # sekundy

    # Barvy pro postupné střídání - používáme scene paths z TEST.tml
    colors = [
        ('red', 'SPOT_1_red.scex'),
        ('orange', 'SPOT_1_orange.scex'),
        ('yellow', 'SPOT_walls_2_yellow.scex'),
        ('green', 'SPOT_1_green.scex'),
        ('blue', 'SPOT_1_blue.scex'),
        ('purple', 'SPOT_1_purple.scex')
    ]

    # Přidej audio track jako první event - CamelCase!
    config['Event_0'] = {
        'TimeLineIndex': '2',
        'StartTime': '0:00:00.0',
        'Path': 'Music/Kraviny-ze-sauny/Kokoti.mp3',
        'Length': '0:04:13.6'
    }

    event_counter = 1
    beat_counter = 0

    # Postupné blikání bodovek okolo dokola
    for beat_time_raw in [i * beat_interval for i in range(int(song_duration / beat_interval))]:
        if beat_time_raw >= song_duration - 1:
            break

        # Který spot má blikat (1-12 okolo dokola)
        spot_number = (beat_counter % 12) + 1

        # Která barva (střídá se každých 6 beatů)
        color_index = (beat_counter // 6) % len(colors)
        color_name, scene_file = colors[color_index]

        # Správný formát času - zajisti že seconds < 60
        minutes = int(beat_time_raw // 60)
        seconds = beat_time_raw % 60

        # Light event - CamelCase format!
        config[f'Event_{event_counter}'] = {
            'TimeLineIndex': '3',
            'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
            'Path': f'SPOTS_walls/SPOTS_single/SPOT_{spot_number}/{scene_file}',
            'Length': '0:00:00.3',
            'Speed': '100',
            'SpeedType': '2'
        }
        event_counter += 1

        # OFF event po každém světelném efektu
        off_time = beat_time_raw + 0.3  # 300ms po zapnutí
        off_minutes = int(off_time // 60)
        off_seconds = off_time % 60

        config[f'Event_{event_counter}'] = {
            'TimeLineIndex': '3',
            'StartTime': f'0:{off_minutes:02d}:{off_seconds:04.1f}',
            'Path': 'OFF'
        }
        event_counter += 1
        beat_counter += 1

        # Debug info každých 20 beatů
        if beat_counter % 20 == 0:
            print(f"Beat {beat_counter}: Spot {spot_number}, Color {color_name}, Time {minutes:02d}:{seconds:04.1f}")

    # Uložit timeline
    with open(output_path, 'w', encoding='utf-8') as f:
        config.write(f)

    # Oprav velikost písmen - ConfigParser automaticky převádí na lowercase
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Oprav Params sekci
    content = content.replace('version =', 'Version =')
    content = content.replace('commenttimeline =', 'CommentTimeLine =')
    content = content.replace('lighttimelines =', 'LightTimeLines =')
    content = content.replace('mediatimelines =', 'MediaTimeLines =')
    content = content.replace('showwaveform =', 'ShowWaveForm =')
    content = content.replace('maxtime =', 'MaxTime =')
    content = content.replace('zoom =', 'Zoom =')
    content = content.replace('timeline_', 'TimeLine_')

    # Oprav Events sekci
    content = content.replace('timelineindex =', 'TimeLineIndex =')
    content = content.replace('starttime =', 'StartTime =')
    content = content.replace('path =', 'Path =')
    content = content.replace('length =', 'Length =')
    content = content.replace('speed =', 'Speed =')
    content = content.replace('speedtype =', 'SpeedType =')

    # Uložit opravený obsah
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Infinit Maximus beat spots timeline saved: {output_path}")
    print(f"Created {event_counter} events (light + OFF events)!")
    print(f"Spots: 1-12 rotating, Colors: {len(colors)} rotating")
    print(f"Beat interval: {beat_interval:.3f}s ({143.6} BPM)")

if __name__ == "__main__":
    # Vytvoř beat spots timeline ve správném Infinit Maximus formátu
    create_infinit_beat_spots_timeline("Kokoti_BEAT_SPOTS_INFINIT_FORMAT.tml")
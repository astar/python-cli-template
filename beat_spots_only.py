#!/usr/bin/env python3
"""Beat-responsive spot lights only - postupné blikání bodovek v rytmu."""

import sys
import configparser
import math

def create_beat_spots_timeline(output_path: str):
    """Vytvoří timeline s beat-responsive bodovkami - jedna po druhé okolo dokola."""

    # Vytvoř novou timeline s správným formátem
    config = configparser.ConfigParser()

    # Správná [Params] sekce
    config['Params'] = {
        'version': '0.2',
        'commenttimeline': '0',
        'lighttimelines': '10',
        'mediatimelines': '1',
        'showwaveform': '1',
        'maxtime': '0:30:00',
        'zoom': '0',
        'timeline_1': 'V I D E O   P I C T U R E   T I M E L I N E',
        'timeline_2': 'A U D I O   T I M E L I N E',
        'timeline_3': 'L I G H T   S C E N E   T I M E L I N E   #   1',
        'timeline_4': 'L I G H T   S C E N E   T I M E L I N E   #   2',
        'timeline_5': 'L I G H T   S C E N E   T I M E L I N E   #   3',
        'timeline_6': 'L I G H T   S C E N E   T I M E L I N E   #   4',
        'timeline_7': 'L I G H T   S C E N E   T I M E L I N E   #   5',
        'timeline_8': 'L I G H T   S C E N E   T I M E L I N E   #   6',
        'timeline_9': 'L I G H T   S C E N E   T I M E L I N E   #   7',
        'timeline_10': 'L I G H T   S C E N E   T I M E L I N E   #   8',
        'timeline_11': 'L I G H T   S C E N E   T I M E L I N E   #   9',
        'timeline_12': 'L I G H T   S C E N E   T I M E L I N E   #   10'
    }

    # BPM 143.6 = beat každých ~0.42 sekund
    beat_interval = 60.0 / 143.6
    song_duration = 253.7  # sekundy

    # Barvy pro postupné střídání
    colors = [
        ('red', 'Bodovka_flash_red.scex'),
        ('blue', 'Bodovka_flash_blue.scex'),
        ('yellow', 'Bodovka_flash_yellow.scex'),
        ('green', 'Bodovka_flash_green.scex'),
        ('purple', 'Bodovka_flash_purple.scex'),
        ('white', 'Bodovka_flash_white.scex')
    ]

    event_counter = 0

    # Přidej audio track jako první event
    config['Event_0'] = {
        'timelineindex': '2',
        'starttime': '0:00:00.0',
        'path': 'Music/Kokoti.mp3',
        'length': '0:04:13.6'
    }

    # Postupné blikání bodovek okolo dokola
    beat_counter = 0

    for beat_time_raw in [i * beat_interval for i in range(int(song_duration / beat_interval))]:
        if beat_time_raw >= song_duration - 1:
            break

        # Který spot má blikat (1-12 okolo dokola)
        spot_number = (beat_counter % 12) + 1

        # Která barva (střídá se každých 6 beatů)
        color_index = (beat_counter // 6) % len(colors)
        color_name, scene_file = colors[color_index]

        # Formátuj čas
        minutes = int(beat_time_raw // 60)
        seconds = beat_time_raw % 60

        config[f'Event_{event_counter + 1}'] = {
            'timelineindex': '3',  # Timeline 3 pro světla
            'starttime': f'0:{minutes:02d}:{seconds:04.1f}',
            'path': f'Bodovky/Bodovky_single/Bodovka_{spot_number}/{scene_file}',
            'length': '0:00:00.3',  # Krátký blik 300ms
            'speed': '100',
            'speedtype': '2'
        }
        event_counter += 1
        beat_counter += 1

        # Debug info každých 20 beatů
        if beat_counter % 20 == 0:
            print(f"Beat {beat_counter}: Spot {spot_number}, Color {color_name}, Time {minutes:02d}:{seconds:04.1f}")

    # Uložit timeline
    with open(output_path, 'w', encoding='utf-8') as f:
        config.write(f)

    print(f"Beat spots timeline saved: {output_path}")
    print(f"Created {event_counter} beat-responsive spot events!")
    print(f"Spots: 1-12 rotating, Colors: {len(colors)} rotating")
    print(f"Beat interval: {beat_interval:.3f}s ({143.6} BPM)")

if __name__ == "__main__":
    # Vytvoř beat spots timeline se správným formátem
    create_beat_spots_timeline("Kokoti_BEAT_SPOTS_FIXED.tml")
#!/usr/bin/env python3
"""Rychlý enhancer pro timeline - přidá dynamické efekty."""

import sys
import configparser
import math

def enhance_timeline(input_path: str, output_path: str):
    """Přidá dynamické efekty do existující timeline."""

    # Načti existující timeline
    config = configparser.ConfigParser()
    config.read(input_path, encoding='utf-8')

    # Počet existujících eventů
    existing_events = len([s for s in config.sections() if s.startswith('Event_')])

    # Přidej dynamické efekty
    event_counter = existing_events

    # BPM 143.6 = beat každých ~0.42 sekund
    beat_interval = 60.0 / 143.6
    song_duration = 253.7  # sekundy

    # 1. Strobe efekty každý 4. beat
    for beat in range(0, int(song_duration / beat_interval), 4):
        beat_time = beat * beat_interval
        if beat_time < song_duration - 5:

            minutes = int(beat_time // 60)
            seconds = beat_time % 60

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '3',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': 'Bodovky/Bodovky_all/Bodovka_flash_white.scex',
                'Length': '0:00:00.2',
                'Speed': '100',
                'SpeedType': '2'
            }
            event_counter += 1

    # 2. Rotující bodovky ve vlnách
    for wave in range(0, int(song_duration), 8):  # Každých 8 sekund
        for i in range(8):  # 8 bodovek postupně
            wave_time = wave + i * 0.15
            if wave_time < song_duration - 2:

                minutes = int(wave_time // 60)
                seconds = wave_time % 60

                bodovka_num = (i % 5) + 1  # Bodovky 1-5

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': str(4 + (i % 3)),
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': f'Bodovky/Bodovky_single/Bodovka_{bodovka_num}/Bodovka_{bodovka_num}_red.scex',
                    'Length': '0:00:00.3',
                    'FadeIn': '100',
                    'FadeOut': '200',
                    'Speed': '100',
                    'SpeedType': '2'
                }
                event_counter += 1

    # 3. Bass explosions - všechna světla najednou
    bass_times = [15, 30, 45, 60, 75, 90, 120, 150, 180, 210]  # Silné bass momenty
    for bass_time in bass_times:
        if bass_time < song_duration - 3:

            minutes = int(bass_time // 60)
            seconds = bass_time % 60

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '7',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': 'ALL/All_lights/All_strobe_rainbow.scex',
                'Length': '0:00:01.0',
                'Speed': '100',
                'SpeedType': '2'
            }
            event_counter += 1

    # 4. Moving heads chase
    for chase in range(10, int(song_duration), 12):  # Každých 12 sekund
        for i in range(5):  # 5 moving heads
            chase_time = chase + i * 0.2
            if chase_time < song_duration - 2:

                minutes = int(chase_time // 60)
                seconds = chase_time % 60

                mh_num = i + 1

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': str(8 + (i % 2)),
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': f'Moving_heads/MH_single/MH_{mh_num}/MH_{mh_num}_strobe_white.scex',
                    'Length': '0:00:00.8',
                    'Speed': '100',
                    'SpeedType': '2'
                }
                event_counter += 1

    # 5. Alternující nahore/dole
    for alt in range(5, int(song_duration), 6):  # Každých 6 sekund
        alt_time = alt
        if alt_time < song_duration - 2:

            minutes = int(alt_time // 60)
            seconds = alt_time % 60

            # Střídavě nahore vs dole
            if (alt // 6) % 2 == 0:
                # Nahore - všechny bodovky
                path = 'Bodovky/Bodovky_all/Bodovka_pulse_yellow.scex'
            else:
                # Dole - kamna + spodní lavice
                path = 'LED_kamna/Kamna_all/Kamna_all_red.scex'

            config[f'Event_{event_counter}'] = {
                'TimeLineIndex': '9',
                'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                'Path': path,
                'Length': '0:00:01.5',
                'FadeIn': '300',
                'FadeOut': '500',
                'Speed': '100',
                'SpeedType': '2'
            }
            event_counter += 1

    # Uložit enhanced timeline
    with open(output_path, 'w', encoding='utf-8') as f:
        config.write(f)

    print(f"Enhanced timeline saved: {output_path}")
    print(f"Added {event_counter - existing_events} dynamic effects!")
    print(f"Total events: {event_counter}")

if __name__ == "__main__":
    enhance_timeline("kokoti_original_basic.tml", "Kokoti_ENHANCED_EXPLOSIVE.tml")
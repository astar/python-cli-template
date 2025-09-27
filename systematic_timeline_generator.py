#!/usr/bin/env python3
"""Timeline generátor využívající systematickou strukturu scex souborů."""

import json
import configparser
import random
import math
from pathlib import Path
from typing import Dict, List, Tuple

class SystematicTimelineGenerator:
    """Generátor timeline na základě systematické struktury."""

    def __init__(self, systematic_structure_path: str = "generated_scenes_systematic/systematic_structure.json"):
        """Inicializuje generátor se systematickou strukturou."""

        with open(systematic_structure_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.fixtures = self.data['fixtures']
        self.colors = self.data['colors']
        self.effects = self.data['effects']
        self.structure = self.data['structure']

        print(f"🎵 Systematic Timeline Generator loaded:")
        print(f"   Fixtures: {len(self.fixtures)}")
        print(f"   Colors: {len(self.colors)}")
        print(f"   Effects: {len(self.effects)}")

    def get_fixtures_by_zone(self, zone: str) -> List[str]:
        """Získá fixture ID podle zóny."""
        return [fid for fid, fixture in self.fixtures.items() if fixture['zone'] == zone]

    def get_fixtures_by_type(self, light_type: str) -> List[str]:
        """Získá fixture ID podle typu světla."""
        return [fid for fid, fixture in self.fixtures.items() if fixture['light_type'] == light_type]

    def get_scene_path(self, fixture_ids: List[str], color: str, effect: str) -> str:
        """Vytvoří cestu k scex souboru pro danou kombinaci."""

        if len(fixture_ids) == 1:
            # Individual fixture
            fixture = self.fixtures[fixture_ids[0]]
            fixture_key = f"{fixture['light_type']}_{fixture_ids[0][-2:]}"
            return f"generated_scenes_systematic/individual/{fixture_key}/{color}_{effect}.scex"

        elif len(fixture_ids) == 2:
            # Try to find in groups
            for group_name, group_info in self.structure.get('groups', {}).items():
                if set(fixture_ids) == set(group_info['fixture_ids']):
                    return f"generated_scenes_systematic/groups/{group_name}/{color}_{effect}.scex"

        # Fallback to zone
        zones = set(self.fixtures[fid]['zone'] for fid in fixture_ids)
        if len(zones) == 1:
            zone = zones.pop()
            return f"generated_scenes_systematic/zones/{zone}/{color}_{effect}.scex"

        # Fallback to individual (use first fixture)
        fixture = self.fixtures[fixture_ids[0]]
        fixture_key = f"{fixture['light_type']}_{fixture_ids[0][-2:]}"
        return f"generated_scenes_systematic/individual/{fixture_key}/{color}_{effect}.scex"

    def create_spatial_wave_timeline(self, output_path: str):
        """Vytvoří timeline s prostorovými vlnami napříč saunou."""

        print("🌊 Creating spatial wave timeline...")

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
            'TimeLine_3': 'S P A T I A L   W A V E S',
            'TimeLine_4': 'C E I L I N G   E F F E C T S',
            'TimeLine_5': 'W A L L   C H A S E S',
            'TimeLine_6': 'M O V I N G   H E A D S',
            'TimeLine_7': 'B A S S   R E S P O N S E',
            'TimeLine_8': 'A M B I E N T   L I G H T S',
            'TimeLine_9': 'U V   E F F E C T S',
            'TimeLine_10': 'S Y N C   F L A S H E S',
            'TimeLine_11': 'C L I M A X   E V E N T S',
            'TimeLine_12': 'S I L E N C E   P A D S'
        }

        # Audio track
        config['Event_0'] = {
            'TimeLineIndex': '2',
            'StartTime': '0:00:00.0',
            'Path': 'Music/Kraviny-ze-sauny/Kokoti.mp3',
            'Length': '0:04:13.6'
        }

        event_counter = 1
        song_duration = 253.7
        beat_interval = 60.0 / 143.6  # BPM 143.6

        # 1. Prostorové vlny - postupné rozsvěcování podle pozice
        print("🌊 Adding spatial waves...")
        wall_fixtures = self.get_fixtures_by_type('led_wall')

        # Seřaď fixtures podle pozice (wave pattern)
        wall_positions = []
        for fid in wall_fixtures:
            x, y, z = self.fixtures[fid]['position']
            wall_positions.append((fid, x, y))

        # Seřaď podle x a y pro wave efekt
        wall_positions.sort(key=lambda p: (p[1], p[2]))  # sort by x, then y

        wave_colors = ['blue', 'cyan', 'purple', 'magenta']

        for wave_start in [10, 40, 70, 100, 130, 160, 190, 220]:
            if wave_start < song_duration - 20:
                color = random.choice(wave_colors)

                for i, (fixture_id, x, y) in enumerate(wall_positions):
                    wave_time = wave_start + i * 0.3  # 300ms delay between fixtures

                    minutes = int(wave_time // 60)
                    seconds = wave_time % 60

                    scene_path = self.get_scene_path([fixture_id], color, 'fade_in')

                    config[f'Event_{event_counter}'] = {
                        'TimeLineIndex': '3',
                        'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                        'Path': scene_path,
                        'Length': '0:00:02.0',
                        'Speed': '60',
                        'SpeedType': '2'
                    }
                    event_counter += 1

        # 2. Ceiling chase - kruhový efekt na bodovkách
        print("🔄 Adding ceiling chase effects...")
        ceiling_fixtures = self.get_fixtures_by_type('ceiling_spot')

        # Seřaď bodovky v kruhu (podle angle)
        ceiling_circle = []
        for fid in ceiling_fixtures:
            x, y, z = self.fixtures[fid]['position']
            # Calculate angle from center (4.25, 3.8)
            center_x, center_y = 4.25, 3.8
            angle = math.atan2(y - center_y, x - center_x)
            ceiling_circle.append((fid, angle))

        ceiling_circle.sort(key=lambda p: p[1])  # sort by angle

        chase_colors = ['red', 'orange', 'yellow', 'white_warm']

        for chase_start in [25, 55, 85, 115, 145, 175, 205, 235]:
            if chase_start < song_duration - 15:
                color = random.choice(chase_colors)

                for i, (fixture_id, angle) in enumerate(ceiling_circle):
                    chase_time = chase_start + i * beat_interval / 2  # Half beat intervals

                    minutes = int(chase_time // 60)
                    seconds = chase_time % 60

                    scene_path = self.get_scene_path([fixture_id], color, 'pulse')

                    config[f'Event_{event_counter}'] = {
                        'TimeLineIndex': '4',
                        'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                        'Path': scene_path,
                        'Length': '0:00:01.5',
                        'Speed': '80',
                        'SpeedType': '2'
                    }
                    event_counter += 1

        # 3. Moving Head choreography
        print("💃 Adding Moving Head choreography...")
        moving_heads = self.get_fixtures_by_type('moving_head')
        mh_colors = ['red', 'blue', 'green', 'purple', 'white_cool']

        for mh_start in [15, 50, 90, 125, 165, 200]:
            if mh_start < song_duration - 10:
                # All moving heads synchronous color
                color = random.choice(mh_colors)

                minutes = int(mh_start // 60)
                seconds = mh_start % 60

                # Use zone-level scene (all moving heads together)
                if moving_heads:
                    scene_path = f"generated_scenes_systematic/zones/ceiling/{color}_fade_in.scex"

                    config[f'Event_{event_counter}'] = {
                        'TimeLineIndex': '6',
                        'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                        'Path': scene_path,
                        'Length': '0:00:05.0',
                        'Speed': '40',
                        'SpeedType': '2',
                        'FadeIn': '1000',
                        'FadeOut': '1000'
                    }
                    event_counter += 1

        # 4. Bass response - silné beaty
        print("🥁 Adding bass response...")
        strong_beats = [30, 60, 95, 120, 150, 180, 210, 240]

        for bass_time in strong_beats:
            if bass_time < song_duration - 3:
                # Flash all walls
                minutes = int(bass_time // 60)
                seconds = bass_time % 60

                scene_path = f"generated_scenes_systematic/zones/walls/white_warm_strobe_fast.scex"

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '7',
                    'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                    'Path': scene_path,
                    'Length': '0:00:01.0',
                    'Speed': '100',
                    'SpeedType': '2'
                }
                event_counter += 1

                # OFF after flash
                off_time = bass_time + 1.0
                off_minutes = int(off_time // 60)
                off_seconds = off_time % 60

                config[f'Event_{event_counter}'] = {
                    'TimeLineIndex': '7',
                    'StartTime': f'0:{off_minutes:02d}:{off_seconds:04.1f}',
                    'Path': 'OFF'
                }
                event_counter += 1

        # 5. Ambient pads - jemné pozadí
        print("🌅 Adding ambient lighting...")
        ambient_colors = ['blue', 'purple', 'cyan']

        for ambient_start in [5, 45, 85, 125, 165, 205]:
            if ambient_start < song_duration - 25:
                color = random.choice(ambient_colors)

                minutes = int(ambient_start // 60)
                seconds = ambient_start % 60

                # Individual fixtures for ambient
                for fixture_id in wall_fixtures[::2]:  # Every second wall fixture
                    scene_path = self.get_scene_path([fixture_id], color, 'static')

                    config[f'Event_{event_counter}'] = {
                        'TimeLineIndex': '8',
                        'StartTime': f'0:{minutes:02d}:{seconds:04.1f}',
                        'Path': scene_path,
                        'Length': '0:00:20.0',
                        'Speed': '20',
                        'SpeedType': '2',
                        'FadeIn': '5000',
                        'FadeOut': '5000'
                    }
                    event_counter += 1

        # Save timeline
        with open(output_path, 'w', encoding='utf-8') as f:
            config.write(f)

        # Fix CamelCase formatting
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

        print(f"✅ Systematic timeline created: {output_path}")
        print(f"   Events: {event_counter}")
        print(f"   Features: Spatial waves, Ceiling chase, Moving Head choreography")
        print(f"   Effects: Bass response, Ambient lighting")
        print(f"   Using systematic scene structure with {len(self.fixtures)} fixtures")

def main():
    """Hlavní funkce pro generování systematické timeline."""

    generator = SystematicTimelineGenerator()
    generator.create_spatial_wave_timeline("Kokoti_SYSTEMATIC_SPATIAL_WAVES.tml")

if __name__ == "__main__":
    main()
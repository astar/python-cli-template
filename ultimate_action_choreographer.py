#!/usr/bin/env python3
"""
Ultimate Action Choreographer - ADVANCED VERSION
MAXIMÁLNĚ AKČNÍ světelný systém s HANDMADE choreografiemi!

FILOZOFIE:
- Využívá generated_scenes_advanced s handmade moving heads choreografiemi
- Basy = bass waves postupně zepředu dozadu
- Výšky = treble explosions s all lights
- Moving heads = kontinuální využití potenciálu s symmetry patterns
- Klid = ambient + subtle light scenes
- Total madness = kombinace všech efektů!
- Maximální kreativita s advanced choreography patterns!
"""

import librosa
import numpy as np
from pathlib import Path
import json
import configparser
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import random

class ActionMode(Enum):
    """Pokročilé režimy akce s advanced scenes"""
    BLACKOUT = "blackout"               # Skoro tma
    GENTLE_AMBIENT = "gentle_ambient"   # Jemné pozadí s advanced color schemes
    BASS_WAVES = "bass_waves"          # Bass vlny s systematic individual lights
    TREBLE_EXPLOSION = "treble_explosion"  # Výšky s all lights explosion
    SYMMETRY_DANCE = "symmetry_dance"  # Symmetry movement patterns
    DYNAMIC_FLOW = "dynamic_flow"      # Dynamic movement (water waves, circular flow)
    TOTAL_MADNESS = "total_madness"    # Kombinace všech advanced efektů!
    MUSICAL_STORYTELLING = "musical_storytelling"  # Scene selection podle song section

class AdvancedActionChoreographer:
    """MAXIMÁLNĚ akční choreograf s pokročilými handmade sekvencemi!"""

    def __init__(self, audio_path: str):
        self.audio_path = Path(audio_path)

        # Načti audio pro analýzu
        print(f"🎵 Loading ADVANCED Action Analysis: {self.audio_path}")
        self.y, self.sr = librosa.load(str(self.audio_path), sr=44100)
        self.duration = len(self.y) / self.sr
        print(f"   Duration: {self.duration:.1f}s")

        # ADVANCED SCENE STRUCTURE - používá handmade choreografie!
        self.advanced_scenes = {
            # Symmetry Movement - handmade moving heads patterns
            "symmetry": [
                "generated_scenes_advanced/symmetry_movement/pendulum_synchronized.scex",
                "generated_scenes_advanced/symmetry_movement/mirror_horizontal_gentle.scex",
                "generated_scenes_advanced/symmetry_movement/mirror_horizontal_dynamic.scex",
                "generated_scenes_advanced/symmetry_movement/adjacent_pairs_gentle.scex",
                "generated_scenes_advanced/symmetry_movement/adjacent_pairs_fast.scex",
                "generated_scenes_advanced/symmetry_movement/opposite_pairs_contrast.scex",
                "generated_scenes_advanced/symmetry_movement/pendulum_alternating.scex",
                "generated_scenes_advanced/symmetry_movement/pendulum_cascading.scex",
                "generated_scenes_advanced/symmetry_movement/rotational_symmetry_slow.scex",
                "generated_scenes_advanced/symmetry_movement/rotational_symmetry_fast.scex"
            ],

            # Dynamic Movement - pokročilé pohyby
            "dynamic": [
                "generated_scenes_advanced/dynamic_movement/water_waves_energetic.scex",
                "generated_scenes_advanced/dynamic_movement/circular_flow_fast.scex",
                "generated_scenes_advanced/dynamic_movement/circular_flow_drift.scex",
                "generated_scenes_advanced/dynamic_movement/figure_8_dynamic.scex",
                "generated_scenes_advanced/dynamic_movement/figure_8_hypnotic.scex",
                "generated_scenes_advanced/dynamic_movement/breathing_sync.scex",
                "generated_scenes_advanced/dynamic_movement/breathing_organic.scex",
                "generated_scenes_advanced/dynamic_movement/chase_fast.scex",
                "generated_scenes_advanced/dynamic_movement/chase_complex.scex"
            ],

            # Professional Moving Heads - profesionální efekty
            "professional": [
                "generated_scenes_advanced/professional_moving_heads/zoom_rotation/zoom_in_out_fast.scex",
                "generated_scenes_advanced/professional_moving_heads/gobo_rotation/gobo_spin_fast.scex",
                "generated_scenes_advanced/professional_moving_heads/snake_effects/snake_horizontal.scex",
                "generated_scenes_advanced/professional_moving_heads/oven_single_color/oven_red_intense.scex"
            ],

            # Advanced Moving Heads by Song Section
            "intro": [
                "generated_scenes_advanced/advanced_moving_heads/intro/intro_gentle_fade.scex",
                "generated_scenes_advanced/advanced_moving_heads/intro/intro_mysterious_slow.scex"
            ],
            "verse": [
                "generated_scenes_advanced/advanced_moving_heads/verse/verse_steady_rhythm.scex",
                "generated_scenes_advanced/advanced_moving_heads/verse/verse_subtle_movement.scex"
            ],
            "chorus": [
                "generated_scenes_advanced/advanced_moving_heads/chorus/chorus_explosive_energy.scex",
                "generated_scenes_advanced/advanced_moving_heads/chorus/chorus_full_spectrum.scex"
            ],
            "buildup": [
                "generated_scenes_advanced/advanced_moving_heads/buildup/buildup_ascending_energy.scex",
                "generated_scenes_advanced/advanced_moving_heads/buildup/buildup_tension_crescendo.scex"
            ],
            "breakdown": [
                "generated_scenes_advanced/advanced_moving_heads/breakdown/breakdown_chaos_unleashed.scex"
            ],

            # Color Schemes by Mood
            "ethereal": [
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/ethereal/ethereal_blue_mist.scex",
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/ethereal/ethereal_purple_dream.scex"
            ],
            "high_energy": [
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/high_energy/high_energy_red_burst.scex",
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/high_energy/high_energy_multicolor_strobe.scex"
            ],
            "cool_mysterious": [
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/cool_mysterious/cool_mysterious_deep_blue.scex"
            ],
            "warm_intimate": [
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/warm_intimate/warm_intimate_golden_glow.scex"
            ],
            "romantic": [
                "generated_scenes_advanced/advanced_moving_heads/color_schemes/romantic/romantic_soft_pink.scex"
            ]
        }

        # Bass response zones - stále používáme systematic pro individual control
        self.bass_zones = {
            "front": [
                "generated_scenes_systematic/individual/ceiling_spot_00/",
                "generated_scenes_systematic/individual/ceiling_spot_01/",
                "generated_scenes_systematic/individual/ceiling_spot_02/",
                "generated_scenes_systematic/individual/ceiling_spot_03/"
            ],
            "middle": [
                "generated_scenes_systematic/individual/ceiling_spot_04/",
                "generated_scenes_systematic/individual/ceiling_spot_05/",
                "generated_scenes_systematic/individual/ceiling_spot_06/",
                "generated_scenes_systematic/individual/ceiling_spot_07/"
            ],
            "back": [
                "generated_scenes_systematic/individual/ceiling_spot_08/",
                "generated_scenes_systematic/individual/ceiling_spot_09/",
                "generated_scenes_systematic/individual/ceiling_spot_10/",
                "generated_scenes_systematic/individual/ceiling_spot_11/"
            ]
        }

        # Treble explosion - all lights
        self.treble_explosion_scenes = [
            "generated_scenes_systematic/zones/ceiling/white_warm_strobe_fast.scex",
            "generated_scenes_systematic/zones/walls/white_cool_strobe_fast.scex",
            "generated_scenes_systematic/zones/effects/white_warm_pulse.scex"
        ]

        print("🎭 Advanced Action Choreographer initialized with handmade scenes!")
        print(f"   Symmetry patterns: {len(self.advanced_scenes['symmetry'])}")
        print(f"   Dynamic movements: {len(self.advanced_scenes['dynamic'])} ")
        print(f"   Professional effects: {len(self.advanced_scenes['professional'])}")
        print(f"   Song-based scenes: {len(self.advanced_scenes['intro']) + len(self.advanced_scenes['verse']) + len(self.advanced_scenes['chorus'])}")

    def analyze_audio_advanced(self) -> Dict:
        """Pokročilá analýza pro MAXIMÁLNÍ action detection"""
        print("🔬 Advanced audio analysis for ULTIMATE ACTION...")

        # Základní analýza
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        beat_times = librosa.frames_to_time(beats, sr=self.sr)

        # Spektrální analýza pro bass/treble detection
        stft = librosa.stft(self.y, hop_length=512, n_fft=2048)
        magnitude = np.abs(stft)
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)

        # Frekvenční pásma
        bass_mask = freqs <= 250  # Bass
        treble_mask = freqs >= 4000  # Treble

        bass_energy = np.mean(magnitude[bass_mask], axis=0)
        treble_energy = np.mean(magnitude[treble_mask], axis=0)

        # RMS energie pro obecnou dynamiku
        rms = librosa.feature.rms(y=self.y, hop_length=512)[0]

        # Time stamps
        times = librosa.frames_to_time(range(len(rms)), sr=self.sr, hop_length=512)

        # Detekce ACTION momentů
        action_moments = []
        total_madness_count = 0

        for i, t in enumerate(times):
            if t >= self.duration - 1:
                break

            # Current values
            current_rms = rms[i] if i < len(rms) else 0
            current_bass = bass_energy[i] if i < len(bass_energy) else 0
            current_treble = treble_energy[i] if i < len(treble_energy) else 0

            # Energy thresholds
            high_energy = current_rms > np.percentile(rms, 75)
            very_high_energy = current_rms > np.percentile(rms, 90)
            bass_hit = current_bass > np.percentile(bass_energy, 80)
            treble_hit = current_treble > np.percentile(treble_energy, 80)

            # Detekce ACTION mode
            mode = ActionMode.GENTLE_AMBIENT

            if very_high_energy and bass_hit and treble_hit:
                mode = ActionMode.TOTAL_MADNESS
                total_madness_count += 1
            elif treble_hit and high_energy:
                mode = ActionMode.TREBLE_EXPLOSION
            elif bass_hit:
                mode = ActionMode.BASS_WAVES
            elif high_energy:
                # Střídej mezi symmetry a dynamic movement
                if i % 3 == 0:
                    mode = ActionMode.SYMMETRY_DANCE
                elif i % 3 == 1:
                    mode = ActionMode.DYNAMIC_FLOW
                else:
                    mode = ActionMode.MUSICAL_STORYTELLING
            elif current_rms < np.percentile(rms, 25):
                mode = ActionMode.BLACKOUT

            action_moments.append({
                "time": float(t),
                "mode": mode,
                "energy_level": float(current_rms),
                "bass_energy": float(current_bass),
                "treble_energy": float(current_treble),
                "is_beat": any(abs(bt - t) < 0.1 for bt in beat_times)
            })

        print(f"✅ Analysis complete!")
        print(f"   Total action moments: {len(action_moments)}")
        print(f"   TOTAL MADNESS moments: {total_madness_count}")
        print(f"   Tempo: {float(tempo):.1f} BPM")

        return {
            "tempo": float(tempo),
            "beat_times": beat_times.tolist(),
            "action_moments": action_moments,
            "duration": self.duration,
            "total_madness_count": total_madness_count
        }

    def generate_bass_wave_front_to_back(self, time: float, duration: float = 2.0) -> List[Dict]:
        """Bass wave postupně zepředu dozadu"""
        events = []
        event_counter = 0

        wave_delay = 0.3  # 300ms mezi zónami
        colors = ["red", "orange", "yellow"]

        for zone_idx, (zone_name, zone_paths) in enumerate(self.bass_zones.items()):
            zone_time = time + zone_idx * wave_delay
            if zone_time >= self.duration - 1:
                break

            # Vyber náhodné světlo ze zóny
            light_path = random.choice(zone_paths)
            color = random.choice(colors)
            scene_path = f"{light_path}{color}_pulse.scex"

            minutes = int(zone_time // 60)
            seconds = zone_time % 60

            events.append({
                "timeline": 3,  # Bass Waves Timeline
                "time": zone_time,
                "scene_path": scene_path,
                "duration": duration,
                "speed": 100,
                "comment": f"Bass wave {zone_name} zone"
            })

        return events

    def generate_treble_explosion(self, time: float, duration: float = 1.5) -> List[Dict]:
        """Treble explosion - všechna světla společně"""
        events = []

        # Všechny světla současně
        explosion_scene = random.choice(self.treble_explosion_scenes)

        events.append({
            "timeline": 4,  # Treble Explosions Timeline
            "time": time,
            "scene_path": explosion_scene,
            "duration": duration,
            "speed": 100,
            "comment": "Treble explosion - all lights"
        })

        return events

    def generate_symmetry_dance(self, time: float, duration: float = 3.0) -> List[Dict]:
        """Symmetry dance s handmade moving heads patterns"""
        events = []

        # Vyber symmetry pattern
        symmetry_scene = random.choice(self.advanced_scenes["symmetry"])

        events.append({
            "timeline": 5,  # Moving Heads Symmetry Timeline
            "time": time,
            "scene_path": symmetry_scene,
            "duration": duration,
            "speed": 80,
            "comment": "Handmade symmetry movement"
        })

        return events

    def generate_dynamic_flow(self, time: float, duration: float = 4.0) -> List[Dict]:
        """Dynamic flow s advanced moving heads choreography"""
        events = []

        # Vyber dynamic movement
        dynamic_scene = random.choice(self.advanced_scenes["dynamic"])

        events.append({
            "timeline": 6,  # Dynamic Movement Timeline
            "time": time,
            "scene_path": dynamic_scene,
            "duration": duration,
            "speed": 60,
            "comment": "Advanced dynamic movement"
        })

        return events

    def generate_total_madness(self, time: float, duration: float = 2.0) -> List[Dict]:
        """TOTAL MADNESS - kombinace všech efektů!"""
        events = []

        # 1. Bass wave
        events.extend(self.generate_bass_wave_front_to_back(time, 1.5))

        # 2. Treble explosion 0.5s later
        events.extend(self.generate_treble_explosion(time + 0.5, 1.0))

        # 3. Crazy symmetry movement
        madness_symmetry = random.choice([
            "generated_scenes_advanced/symmetry_movement/rotational_symmetry_fast.scex",
            "generated_scenes_advanced/symmetry_movement/pendulum_cascading.scex",
            "generated_scenes_advanced/advanced_moving_heads/breakdown/breakdown_chaos_unleashed.scex"
        ])

        events.append({
            "timeline": 7,  # Total Madness Timeline
            "time": time,
            "scene_path": madness_symmetry,
            "duration": duration,
            "speed": 120,
            "comment": "TOTAL MADNESS - maximum chaos!"
        })

        return events

    def generate_musical_storytelling(self, time: float, duration: float = 3.0) -> List[Dict]:
        """Musical storytelling based on song section"""
        events = []

        # Detekce části songu podle času
        progress = time / self.duration

        if progress < 0.15:  # Intro (první 15%)
            scene = random.choice(self.advanced_scenes["intro"])
            timeline = 8
            comment = "Intro storytelling"
        elif progress < 0.4:  # Verse (15-40%)
            scene = random.choice(self.advanced_scenes["verse"])
            timeline = 8
            comment = "Verse storytelling"
        elif progress < 0.7:  # Chorus (40-70%)
            scene = random.choice(self.advanced_scenes["chorus"])
            timeline = 8
            comment = "Chorus storytelling"
        elif progress < 0.85:  # Buildup (70-85%)
            scene = random.choice(self.advanced_scenes["buildup"])
            timeline = 8
            comment = "Buildup storytelling"
        else:  # Breakdown/Outro (85%+)
            scene = random.choice(self.advanced_scenes["breakdown"])
            timeline = 8
            comment = "Breakdown storytelling"

        events.append({
            "timeline": timeline,
            "time": time,
            "scene_path": scene,
            "duration": duration,
            "speed": 70,
            "comment": comment
        })

        return events

    def create_ultimate_action_show(self, output_path: str):
        """Vytvoří ULTIMATE ACTION SHOW s advanced choreography!"""
        print("🔥 Creating ULTIMATE ACTION SHOW with ADVANCED choreography...")

        # Analýza audio
        analysis = self.analyze_audio_advanced()

        config = configparser.ConfigParser()

        # Timeline struktura
        config["Params"] = {
            "Version": "0.2",
            "CommentTimeLine": "0",
            "LightTimeLines": "10",
            "MediaTimeLines": "1",
            "ShowWaveForm": "1",
            "MaxTime": f"0:{int(self.duration//60):02d}:{int(self.duration%60):02d}",
            "Zoom": "0",
            "TimeLine_1": "U L T I M A T E   A C T I O N   S H O W   ( A D V A N C E D )",
            "TimeLine_2": "A U D I O   T I M E L I N E",
            "TimeLine_3": "B A S S   W A V E S   ( F R O N T → B A C K )",
            "TimeLine_4": "T R E B L E   E X P L O S I O N S",
            "TimeLine_5": "S Y M M E T R Y   D A N C E",
            "TimeLine_6": "D Y N A M I C   F L O W",
            "TimeLine_7": "T O T A L   M A D N E S S",
            "TimeLine_8": "M U S I C A L   S T O R Y T E L L I N G",
            "TimeLine_9": "A M B I E N T   M O O D S",
            "TimeLine_10": "P R O F E S S I O N A L   E F F E C T S",
            "TimeLine_11": "S P A T I A L   E F F E C T S"
        }

        # Audio track
        song_name = self.audio_path.stem
        config["Event_0"] = {
            "TimeLineIndex": "2",
            "StartTime": "0:00:00.0",
            "Path": f"Music/{song_name}/{self.audio_path.name}",
            "Length": f"0:{int(self.duration//60):02d}:{int(self.duration%60):02d}.0"
        }

        # Generate events z action moments
        all_events = []
        event_counter = 1

        for moment in analysis["action_moments"]:
            time = moment["time"]
            mode = ActionMode(moment["mode"])

            if mode == ActionMode.BASS_WAVES:
                all_events.extend(self.generate_bass_wave_front_to_back(time))
            elif mode == ActionMode.TREBLE_EXPLOSION:
                all_events.extend(self.generate_treble_explosion(time))
            elif mode == ActionMode.SYMMETRY_DANCE:
                all_events.extend(self.generate_symmetry_dance(time))
            elif mode == ActionMode.DYNAMIC_FLOW:
                all_events.extend(self.generate_dynamic_flow(time))
            elif mode == ActionMode.TOTAL_MADNESS:
                all_events.extend(self.generate_total_madness(time))
            elif mode == ActionMode.MUSICAL_STORYTELLING:
                all_events.extend(self.generate_musical_storytelling(time))

        # Sort events by time
        all_events.sort(key=lambda x: x["time"])

        # Add events to config
        for event in all_events:
            if event_counter > 30000:  # GitHub file size limit
                break

            time = event["time"]
            minutes = int(time // 60)
            seconds = time % 60

            config[f"Event_{event_counter}"] = {
                "TimeLineIndex": str(event["timeline"]),
                "StartTime": f"0:{minutes:02d}:{seconds:04.1f}",
                "Path": event["scene_path"],
                "Length": f"0:00:{event['duration']:04.1f}",
                "Speed": str(event["speed"]),
                "SpeedType": "2"
            }
            event_counter += 1

        # Save timeline
        with open(output_path, "w", encoding="utf-8") as f:
            config.write(f)

        # Fix CamelCase formatting
        self._fix_infinit_maximus_format(output_path)

        print(f"🎉 ULTIMATE ACTION SHOW created: {output_path}")
        print(f"   Total events: {event_counter-1}")
        print(f"   TOTAL MADNESS moments: {analysis['total_madness_count']}")
        print(f"   Features: Advanced choreography, Handmade moving heads, Symmetry patterns")
        print(f"   Song duration: {self.duration:.1f}s at {analysis['tempo']:.1f} BPM")
        print("   🎭 Uses generated_scenes_advanced with professional choreography!")

    def _fix_infinit_maximus_format(self, output_path: str):
        """Fix ConfigParser formatting pro Infinit Maximus"""
        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        replacements = {
            "version =": "Version =",
            "commenttimeline =": "CommentTimeLine =",
            "lighttimelines =": "LightTimeLines =",
            "mediatimelines =": "MediaTimeLines =",
            "showwaveform =": "ShowWaveForm =",
            "maxtime =": "MaxTime =",
            "zoom =": "Zoom =",
            "timeline_": "TimeLine_",
            "timelineindex =": "TimeLineIndex =",
            "starttime =": "StartTime =",
            "path =": "Path =",
            "length =": "Length =",
            "speed =": "Speed =",
            "speedtype =": "SpeedType ="
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

def main():
    """Main function for ADVANCED Ultimate Action Show"""
    import sys

    if len(sys.argv) != 3:
        print("Usage: python ultimate_action_choreographer_advanced.py <audio_file> <output_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_file = sys.argv[2]

    choreographer = AdvancedActionChoreographer(audio_file)
    choreographer.create_ultimate_action_show(output_file)

    print("🔥 ULTIMATE ACTION SHOW with ADVANCED choreography complete!")

if __name__ == "__main__":
    main()
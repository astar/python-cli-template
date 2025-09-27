"""Dynamický spektakulární generátor s agresivními efekty navázanými na beaty."""

from __future__ import annotations

import math
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import librosa

from .logging import get_logger
from .models import DMXEvent, DMXTimeline, SpeedType

logger = get_logger(__name__)


class DynamicSpectacularGenerator:
    """Generátor spektakulárních světelných show s dynamickými efekty."""

    def __init__(self):
        """Initialize dynamic spectacular generator."""
        # Mapování typu efektů na světelné skupiny
        self.effect_fixtures = {
            'strobe_ceiling': [
                'Bodovky/Bodovky_single/Bodovka_1/Bodovka_1_strobe_red.scex',
                'Bodovky/Bodovky_single/Bodovka_2/Bodovka_2_strobe_green.scex',
                'Bodovky/Bodovky_single/Bodovka_3/Bodovka_3_strobe_blue.scex',
                'Bodovky/Bodovky_single/Bodovka_4/Bodovka_4_strobe_yellow.scex',
                'Bodovky/Bodovky_single/Bodovka_5/Bodovka_5_strobe_white.scex',
            ],
            'flash_all_ceiling': [
                'Bodovky/Bodovky_all/Bodovka_flash_red.scex',
                'Bodovky/Bodovky_all/Bodovka_flash_white.scex',
                'Bodovky/Bodovky_all/Bodovka_flash_blue.scex',
            ],
            'circular_waves': [
                'Bodovky/Bodovky_single/Bodovka_1/Bodovka_1_red.scex',
                'Bodovky/Bodovky_single/Bodovka_2/Bodovka_2_red.scex',
                'Bodovky/Bodovky_single/Bodovka_3/Bodovka_3_red.scex',
                'Bodovky/Bodovky_single/Bodovka_4/Bodovka_4_red.scex',
                'Bodovky/Bodovky_single/Bodovka_5/Bodovka_5_red.scex',
                'Bodovky/Bodovky_single/Bodovka_6/Bodovka_6_red.scex',
                'Bodovky/Bodovky_single/Bodovka_7/Bodovka_7_red.scex',
                'Bodovky/Bodovky_single/Bodovka_8/Bodovka_8_red.scex',
                'Bodovky/Bodovky_single/Bodovka_9/Bodovka_9_red.scex',
                'Bodovky/Bodovky_single/Bodovka_10/Bodovka_10_red.scex',
                'Bodovky/Bodovky_single/Bodovka_11/Bodovka_11_red.scex',
                'Bodovky/Bodovky_single/Bodovka_12/Bodovka_12_red.scex',
            ],
            'up_down_alternating': {
                'up': [  # Horní část - strop, horní lavice
                    'Bodovky/Bodovky_all/Bodovka_white.scex',
                    'LED_lavice/Lavice_single/Lavice_1/Lavice_1_white.scex',
                    'LED_lavice/Lavice_single/Lavice_2/Lavice_2_white.scex',
                ],
                'down': [  # Dolní část - spodní lavice, kamna
                    'LED_kamna/Kamna_all/Kamna_all_orange.scex',
                    'LED_lavice/Lavice_single/Lavice_10/Lavice_10_white.scex',
                    'LED_lavice/Lavice_single/Lavice_11/Lavice_11_white.scex',
                ]
            },
            'bass_explosions': [
                'ALL/All_lights/All_strobe_rainbow.scex',
                'ALL/All_lights/All_flash_white.scex',
                'ALL/All_lights/All_strobe_red.scex',
            ],
            'moving_chase': [
                'Moving_heads/MH_single/MH_1/MH_1_strobe_red.scex',
                'Moving_heads/MH_single/MH_2/MH_2_strobe_green.scex',
                'Moving_heads/MH_single/MH_3/MH_3_strobe_blue.scex',
                'Moving_heads/MH_single/MH_4/MH_4_strobe_yellow.scex',
                'Moving_heads/MH_single/MH_5/MH_5_strobe_white.scex',
            ],
            'wall_pulse': [
                'LED_Walls/Walls_all/Walls_pulse_red.scex',
                'LED_Walls/Walls_all/Walls_pulse_green.scex',
                'LED_Walls/Walls_all/Walls_pulse_blue.scex',
                'LED_Walls/Walls_all/Walls_pulse_yellow.scex',
            ]
        }

    def generate_spectacular_timeline(self, audio_path: Path, output_path: Path) -> DMXTimeline:
        """Generuje spektakulární timeline s dynamickými efekty."""
        logger.info(f"Generuji dynamickou spektakulární timeline pro: {audio_path}")

        # Načtení a analýza audio
        y, sr = librosa.load(str(audio_path), sr=44100)
        duration = len(y) / sr

        # Pokročilá hudební analýza
        analysis_data = self._analyze_audio_advanced(y, sr)

        # Vytvoření timeline
        timeline = DMXTimeline()
        timeline.audio_length = f"0:{int(duration//60):02d}:{duration%60:05.1f}"
        timeline.light_timelines = 10

        events = []

        # Audio track
        audio_event = DMXEvent(
            timeline_index=2,
            start_time="0:00:00.0",
            path=f"Music/{audio_path.name}",
            length=timeline.audio_length
        )
        events.append(audio_event)

        # Generování dynamických efektů
        events.extend(self._generate_beat_responsive_effects(analysis_data, duration))
        events.extend(self._generate_strobe_effects(analysis_data, duration))
        events.extend(self._generate_circular_waves(analysis_data, duration))
        events.extend(self._generate_alternating_effects(analysis_data, duration))
        events.extend(self._generate_bass_explosions(analysis_data, duration))
        events.extend(self._generate_moving_chase(analysis_data, duration))

        timeline.events = sorted(events, key=lambda e: self._time_to_seconds(e.start_time))

        # Uložení
        timeline.save(output_path)
        logger.info(f"Dynamická timeline uložena: {output_path} ({len(timeline.events)} events)")

        return timeline

    def _analyze_audio_advanced(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Pokročilá analýza audio pro dynamické efekty."""
        logger.info("Analyzing audio for dynamic effects...")

        # Beat tracking s vysokým rozlišením
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=256)
        beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=256)

        # Detekce výrazných beats (onsets)
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=256,
                                                 backtrack=True, units='frames')
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=256)

        # Energy tracking pro bass efekty
        rms = librosa.feature.rms(y=y, hop_length=512)[0]
        rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)

        # Spectral features pro dynamiku
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=512)[0]

        # Bass detection (nízké frekvence)
        stft = librosa.stft(y, hop_length=512)
        bass_freqs = np.abs(stft[:50, :])  # První 50 bins = nízké frekvence
        bass_energy = np.mean(bass_freqs, axis=0)

        # High frequency detection pro stroboskopy
        high_freqs = np.abs(stft[-100:, :])  # Posledních 100 bins = vysoké frekvence
        high_energy = np.mean(high_freqs, axis=0)

        return {
            'tempo': tempo,
            'beat_times': beat_times,
            'onset_times': onset_times,
            'rms': rms,
            'rms_times': rms_times,
            'spectral_centroids': spectral_centroids,
            'spectral_rolloff': spectral_rolloff,
            'bass_energy': bass_energy,
            'high_energy': high_energy,
            'duration': len(y) / sr
        }

    def _generate_beat_responsive_effects(self, analysis: Dict[str, Any], duration: float) -> List[DMXEvent]:
        """Generuje efekty reagující na beaty."""
        events = []
        beat_times = analysis['beat_times']

        timeline_idx = 3

        for i, beat_time in enumerate(beat_times):
            if beat_time >= duration - 1.0:  # Skip beats near end
                continue

            # Skip problematické časy (exact 60 second intervals)
            if beat_time % 60.0 == 0.0 and beat_time > 0:
                beat_time += 0.1

            # Každý 4. beat = výrazný efekt
            if i % 4 == 0:
                # Flash všech bodovek
                effect_path = np.random.choice(self.effect_fixtures['flash_all_ceiling'])
                events.append(DMXEvent(
                    timeline_index=timeline_idx,
                    start_time=self._seconds_to_time(beat_time),
                    path=effect_path,
                    length="0:00:00.2",  # Krátký flash
                    speed=100,  # Maximální rychlost
                    speed_type=SpeedType.PERCENTAGE
                ))

            # Každý 8. beat = strobe efekt
            elif i % 8 == 0:
                strobe_path = np.random.choice(self.effect_fixtures['strobe_ceiling'])
                events.append(DMXEvent(
                    timeline_index=timeline_idx + 1,
                    start_time=self._seconds_to_time(beat_time),
                    path=strobe_path,
                    length="0:00:01.0",
                    speed=100,
                    speed_type=SpeedType.PERCENTAGE
                ))

        return events

    def _generate_strobe_effects(self, analysis: Dict[str, Any], duration: float) -> List[DMXEvent]:
        """Generuje stroboskopické efekty na vysoké frekvence."""
        events = []
        high_energy = analysis['high_energy']
        rms_times = analysis['rms_times']

        # Threshold pro aktivaci strobo efektů
        high_threshold = np.percentile(high_energy, 80)  # Top 20% energie

        timeline_idx = 4
        last_strobe_time = 0.0

        for i, (time, energy) in enumerate(zip(rms_times, high_energy)):
            if energy > high_threshold and time > last_strobe_time + 0.5:  # Min 0.5s mezi stroby
                # Intenzivní strobe na bodovkách
                strobe_count = min(3, int(energy / high_threshold))  # 1-3 stroby

                for j in range(strobe_count):
                    strobe_time = time + j * 0.1
                    if strobe_time < duration - 1.0:
                        events.append(DMXEvent(
                            timeline_index=timeline_idx + j % 3,
                            start_time=self._seconds_to_time(strobe_time),
                            path=self.effect_fixtures['strobe_ceiling'][j % len(self.effect_fixtures['strobe_ceiling'])],
                            length="0:00:00.1",
                            speed=100,  # Maximální rychlost
                            speed_type=SpeedType.PERCENTAGE
                        ))

                last_strobe_time = time

        return events

    def _generate_circular_waves(self, analysis: Dict[str, Any], duration: float) -> List[DMXEvent]:
        """Generuje vlnové efekty po bodovkách."""
        events = []
        beat_times = analysis['beat_times']

        timeline_idx = 5
        wave_fixtures = self.effect_fixtures['circular_waves']

        # Každý 16. beat = kruhová vlna
        for i, beat_time in enumerate(beat_times):
            if i % 16 == 0 and beat_time < duration - 3.0:
                # Postupně rozsvěcuj bodovky v kruhu
                for j, fixture_path in enumerate(wave_fixtures[:8]):  # Prvních 8 bodovek
                    delay = j * 0.1  # 100ms delay mezi bodovkami
                    events.append(DMXEvent(
                        timeline_index=timeline_idx + (j % 3),
                        start_time=self._seconds_to_time(beat_time + delay),
                        path=fixture_path,
                        length="0:00:00.3",
                        fade_in=50,
                        fade_out=100,
                        speed=100,
                        speed_type=SpeedType.PERCENTAGE
                    ))

        return events

    def _generate_alternating_effects(self, analysis: Dict[str, Any], duration: float) -> List[DMXEvent]:
        """Generuje střídavé efekty nahore vs dole."""
        events = []
        beat_times = analysis['beat_times']

        timeline_idx = 6
        up_fixtures = self.effect_fixtures['up_down_alternating']['up']
        down_fixtures = self.effect_fixtures['up_down_alternating']['down']

        for i, beat_time in enumerate(beat_times):
            if i % 8 == 0 and beat_time < duration - 1.0:
                # Střídavě nahore/dole
                if (i // 8) % 2 == 0:
                    # Nahore
                    fixture = np.random.choice(up_fixtures)
                else:
                    # Dole
                    fixture = np.random.choice(down_fixtures)

                events.append(DMXEvent(
                    timeline_index=timeline_idx,
                    start_time=self._seconds_to_time(beat_time),
                    path=fixture,
                    length="0:00:01.0",
                    fade_in=100,
                    fade_out=200,
                    speed=100,
                    speed_type=SpeedType.PERCENTAGE
                ))

        return events

    def _generate_bass_explosions(self, analysis: Dict[str, Any], duration: float) -> List[DMXEvent]:
        """Generuje výbušné efekty na silné basy."""
        events = []
        bass_energy = analysis['bass_energy']
        rms_times = analysis['rms_times']

        # Detekce silných basů
        bass_threshold = np.percentile(bass_energy, 90)  # Top 10% bass energie

        timeline_idx = 7
        last_explosion_time = 0.0

        for time, energy in zip(rms_times, bass_energy):
            if energy > bass_threshold and time > last_explosion_time + 1.5:  # Min 1.5s mezi výbuchy
                # Výbušný efekt všech světel
                explosion_path = np.random.choice(self.effect_fixtures['bass_explosions'])
                events.append(DMXEvent(
                    timeline_index=timeline_idx,
                    start_time=self._seconds_to_time(time),
                    path=explosion_path,
                    length="0:00:00.5",
                    speed=100,  # Maximální rychlost
                    speed_type=SpeedType.PERCENTAGE
                ))

                last_explosion_time = time

        return events

    def _generate_moving_chase(self, analysis: Dict[str, Any], duration: float) -> List[DMXEvent]:
        """Generuje chase efekty na moving heads."""
        events = []
        beat_times = analysis['beat_times']

        timeline_idx = 8
        chase_fixtures = self.effect_fixtures['moving_chase']

        # Každý 12. beat = chase efekt
        for i, beat_time in enumerate(beat_times):
            if i % 12 == 0 and beat_time < duration - 2.0:
                # Postupně rozsvěcuj moving heads
                for j, fixture_path in enumerate(chase_fixtures):
                    delay = j * 0.2  # 200ms delay
                    events.append(DMXEvent(
                        timeline_index=timeline_idx + (j % 2),
                        start_time=self._seconds_to_time(beat_time + delay),
                        path=fixture_path,
                        length="0:00:00.6",
                        speed=100,
                        speed_type=SpeedType.PERCENTAGE
                    ))

        return events

    def _time_to_seconds(self, time_str: str) -> float:
        """Převede čas string na sekundy."""
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        sec_parts = parts[2].split(".")
        seconds = int(sec_parts[0])
        decimal = float("0." + sec_parts[1]) if len(sec_parts) > 1 else 0.0
        return hours * 3600 + minutes * 60 + seconds + decimal

    def _seconds_to_time(self, seconds: float) -> str:
        """Převede sekundy na čas string."""
        # Použij Python timedelta pro správný převod
        from datetime import timedelta

        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds // 60) % 60
        secs = td.seconds % 60 + td.microseconds / 1000000

        return f"{hours}:{minutes:02d}:{secs:04.1f}"


def create_dynamic_spectacular_timeline(audio_path: Path, output_path: Path) -> DMXTimeline:
    """Vytvoří dynamickou spektakulární timeline."""
    generator = DynamicSpectacularGenerator()
    return generator.generate_spectacular_timeline(audio_path, output_path)
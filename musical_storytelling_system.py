#!/usr/bin/env python3
"""
Musical Storytelling System
Pokročilý systém pro vytváření hudebních příběhů pomocí světel

FILOZOFIE:
- Hudba je příběh s emocemi, napětím, uvolněním
- Každá skladba má svou dramaturgii (intro, buildup, drop, outro)
- Světla musí podporovat vnímání této dramatugie
- Vytváříme "visual vocabulary" pro různé hudební elementy

HUDEBNÍ JAZYK:
1. EMOČNÍ STAVY:
   - Calm (klid) → teplé, pomalé barvy
   - Energy (energie) → rychlé, jasné barvy
   - Tension (napětí) → kontrastní barvy, stroboskopy
   - Release (uvolnění) → explozivní efekty
   - Mystery (tajemno) → temné, UV efekty
   - Joy (radost) → barevné, synchronní efekty

2. HUDEBNÍ STRUKTURY:
   - Intro → postupné rozsvěcování
   - Verse → rytmické podkreslení
   - Chorus → velké efekty, všechna světla
   - Bridge → změna barev/tempa
   - Drop → explozivní choreografie
   - Outro → postupné zhasínání

3. INSTRUMENTÁLNÍ MAPOVÁNÍ:
   - Kick Drum → LED Kamna (červené)
   - Snare → Wall Spots (bílé)
   - Hi-Hat → Bodovky (žluté)
   - Bass → LED Lavice (tmavé barvy)
   - Lead → Moving Heads (dynamické)
   - Pad/Strings → všechna světla (ambient)
"""

import librosa
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

class EmotionalState(Enum):
    """Emocionální stavy hudby"""
    CALM = "calm"           # Klid, relaxace
    ENERGY = "energy"       # Vysoká energie
    TENSION = "tension"     # Napětí, suspense
    RELEASE = "release"     # Uvolnění, drop
    MYSTERY = "mystery"     # Tajemno, dark
    JOY = "joy"            # Radost, euphorie
    MELANCHOLY = "melancholy" # Smutek, nostalgie
    AGGRESSIVE = "aggressive" # Agresivita, tvrdost

class SongSection(Enum):
    """Části skladby"""
    INTRO = "intro"
    VERSE = "verse"
    CHORUS = "chorus"
    BRIDGE = "bridge"
    DROP = "drop"
    OUTRO = "outro"
    BREAKDOWN = "breakdown"
    BUILDUP = "buildup"

class MovementPattern(Enum):
    """Vzory pohybu moving heads"""
    STATIC = "static"           # Statické pozice
    SLOW_SWEEP = "slow_sweep"   # Pomalé kývání
    FAST_SWEEP = "fast_sweep"   # Rychlé kývání
    CIRCLE = "circle"           # Kruhový pohyb
    FIGURE_8 = "figure_8"       # Osmička
    RANDOM = "random"           # Náhodný pohyb
    SYNC_ALL = "sync_all"       # Synchronní pohyb všech
    COUNTER = "counter"         # Protisměrný pohyb
    CHASE = "chase"             # Následování

@dataclass
class MusicalMoment:
    """Hudební moment s jeho charakteristikami"""
    start_time: float
    duration: float
    emotion: EmotionalState
    section: SongSection
    energy_level: float  # 0.0 - 1.0
    bass_intensity: float
    treble_intensity: float
    movement_pattern: MovementPattern
    primary_color: str
    secondary_color: Optional[str] = None
    effects: List[str] = None

    # Alias properties pro kompatibilitu
    @property
    def time(self) -> float:
        return self.start_time

    @property
    def energy(self) -> float:
        return self.energy_level

    @property
    def emotional_state(self) -> EmotionalState:
        return self.emotion

    @property
    def tempo(self) -> float:
        # Default tempo, bude přepsáno při analýze
        return 120.0

    def __post_init__(self):
        if self.effects is None:
            self.effects = []

class MusicalStorytellingSystem:
    """Systém pro vytváření hudebních příběhů"""

    def __init__(self, audio_path: str):
        self.audio_path = Path(audio_path)
        self.y, self.sr = librosa.load(str(self.audio_path), sr=44100)
        self.duration = len(self.y) / self.sr

        # Hudební analýza
        self.tempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.beat_times = librosa.beat.beat_track(y=self.y, sr=self.sr, units='time')[1]

        # Emocionální mapování
        self.emotion_color_map = {
            EmotionalState.CALM: ("blue", "white_warm"),
            EmotionalState.ENERGY: ("red", "orange"),
            EmotionalState.TENSION: ("purple", "white_cool"),
            EmotionalState.RELEASE: ("white", "yellow"),
            EmotionalState.MYSTERY: ("purple", "blue"),
            EmotionalState.JOY: ("yellow", "orange"),
            EmotionalState.MELANCHOLY: ("blue", "purple"),
            EmotionalState.AGGRESSIVE: ("red", "white_cool")
        }

        # Moving heads choreografie
        self.movement_sequences = self._create_movement_sequences()

        print(f"🎵 Loaded: {self.audio_path.name}")
        print(f"   Duration: {self.duration:.1f}s, Tempo: {float(self.tempo):.1f} BPM")

    def _create_movement_sequences(self) -> Dict[MovementPattern, Dict]:
        """Vytvoří moving heads choreografie"""
        return {
            MovementPattern.STATIC: {
                "name": "Static Positions",
                "description": "Statické pozice pro ambient momenty",
                "pan_pattern": [128, 128, 128, 128, 128],  # Center
                "tilt_pattern": [128, 128, 128, 128, 128],
                "speed": 1
            },

            MovementPattern.SLOW_SWEEP: {
                "name": "Slow Romantic Sweep",
                "description": "Pomalé kývání pro romantické momenty",
                "pan_pattern": [64, 96, 128, 160, 192],  # Slow left-right
                "tilt_pattern": [112, 120, 128, 136, 144],
                "speed": 2
            },

            MovementPattern.FAST_SWEEP: {
                "name": "Energetic Fast Sweep",
                "description": "Rychlé kývání pro energické části",
                "pan_pattern": [32, 80, 128, 176, 224],  # Fast left-right
                "tilt_pattern": [96, 112, 128, 144, 160],
                "speed": 5
            },

            MovementPattern.CIRCLE: {
                "name": "Mystical Circle",
                "description": "Kruhový pohyb pro mysterické momenty",
                "pan_pattern": [128, 160, 192, 160, 128, 96, 64, 96],  # Circle
                "tilt_pattern": [128, 144, 128, 112, 128, 144, 128, 112],
                "speed": 3
            },

            MovementPattern.FIGURE_8: {
                "name": "Dynamic Figure-8",
                "description": "Osmička pro dynamické buildupy",
                "pan_pattern": [64, 96, 128, 160, 192, 160, 128, 96],
                "tilt_pattern": [112, 128, 144, 128, 112, 128, 144, 128],
                "speed": 4
            },

            MovementPattern.SYNC_ALL: {
                "name": "Synchronized Power",
                "description": "Synchronní pohyb pro power momenty",
                "pan_pattern": [128, 192, 128, 64, 128],  # All same
                "tilt_pattern": [128, 160, 128, 96, 128],
                "speed": 6
            },

            MovementPattern.COUNTER: {
                "name": "Counter Balance",
                "description": "Protisměrný pohyb pro tension",
                "pan_pattern": [64, 128, 192, 128, 64],   # MH1,3,5 one way
                "pan_pattern_alt": [192, 128, 64, 128, 192], # MH2,4 other way
                "tilt_pattern": [96, 128, 160, 128, 96],
                "speed": 4
            },

            MovementPattern.CHASE: {
                "name": "Sequential Chase",
                "description": "Postupné následování pro buildup",
                "sequence_delay": 0.2,  # Delay between heads
                "pan_pattern": [64, 96, 128, 160, 192],
                "tilt_pattern": [112, 120, 128, 136, 144],
                "speed": 3
            }
        }

    def analyze_emotional_journey(self) -> List[MusicalMoment]:
        """Analyzuje emocionální cestu skladby"""
        print("🧠 Analyzing emotional journey...")

        # Rozděl skladbu na segmenty (každé 4 takty)
        beats_per_segment = 16  # 4 takty x 4 beats
        segments = []

        for i in range(0, len(self.beat_times) - beats_per_segment, beats_per_segment):
            start_time = self.beat_times[i]
            end_time = self.beat_times[min(i + beats_per_segment, len(self.beat_times) - 1)]
            duration = end_time - start_time

            # Analyzuj segment
            start_sample = int(start_time * self.sr)
            end_sample = int(end_time * self.sr)
            segment_audio = self.y[start_sample:end_sample]

            # Extrahuj features
            energy = np.mean(librosa.feature.rms(y=segment_audio)[0])
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=segment_audio, sr=self.sr)[0])
            tempo_local = librosa.beat.tempo(y=segment_audio, sr=self.sr)[0]

            # Frekvenční analýza
            stft = librosa.stft(segment_audio)
            magnitude = np.abs(stft)
            freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)

            bass_range = np.where((freqs >= 20) & (freqs <= 250))[0]
            treble_range = np.where((freqs >= 4000) & (freqs <= 20000))[0]

            bass_intensity = np.mean(magnitude[bass_range]) if len(bass_range) > 0 else 0
            treble_intensity = np.mean(magnitude[treble_range]) if len(treble_range) > 0 else 0

            # Mapuj na emocionální stav
            emotion = self._classify_emotion(energy, spectral_centroid, tempo_local, bass_intensity, treble_intensity)
            section = self._classify_section(i, len(self.beat_times) // beats_per_segment, energy, bass_intensity)
            movement = self._select_movement_pattern(emotion, section, energy)

            # Barevné mapování
            primary_color, secondary_color = self.emotion_color_map[emotion]

            moment = MusicalMoment(
                start_time=start_time,
                duration=duration,
                emotion=emotion,
                section=section,
                energy_level=min(energy * 2, 1.0),  # Normalizace
                bass_intensity=bass_intensity,
                treble_intensity=treble_intensity,
                movement_pattern=movement,
                primary_color=primary_color,
                secondary_color=secondary_color,
                effects=self._select_effects(emotion, section, energy)
            )

            segments.append(moment)

        print(f"   Analyzed {len(segments)} musical moments")
        return segments

    def _classify_emotion(self, energy: float, spectral_centroid: float, tempo: float,
                         bass: float, treble: float) -> EmotionalState:
        """Klasifikuje emocionální stav na základě audio features"""

        # Vysoká energie + vysoké frekvence = radost/energie
        if energy > 0.15 and spectral_centroid > 2000:
            if tempo > 120:
                return EmotionalState.JOY
            else:
                return EmotionalState.ENERGY

        # Vysoká energie + nízké frekvence = agresivita
        elif energy > 0.2 and bass > treble:
            return EmotionalState.AGGRESSIVE

        # Střední energie + kontrasty = napětí
        elif 0.08 < energy < 0.15 and abs(bass - treble) > 0.1:
            return EmotionalState.TENSION

        # Nízká energie + vysoké frekvence = tajemno
        elif energy < 0.08 and spectral_centroid > 1500:
            return EmotionalState.MYSTERY

        # Nízká energie + nízké frekvence = smutek
        elif energy < 0.08 and spectral_centroid < 1000:
            return EmotionalState.MELANCHOLY

        # Střední energie = klid
        else:
            return EmotionalState.CALM

    def _classify_section(self, segment_idx: int, total_segments: int,
                         energy: float, bass: float) -> SongSection:
        """Klasifikuje část skladby"""
        progress = segment_idx / total_segments

        # Intro (první 10%)
        if progress < 0.1:
            return SongSection.INTRO

        # Outro (posledních 10%)
        elif progress > 0.9:
            return SongSection.OUTRO

        # Drop (vysoká energie + bass)
        elif energy > 0.18 and bass > 0.15:
            return SongSection.DROP

        # Buildup (rostoucí energie)
        elif energy > 0.12 and progress > 0.3:
            return SongSection.BUILDUP

        # Chorus (střední-vysoká energie)
        elif energy > 0.1:
            return SongSection.CHORUS

        # Bridge (střední část s nižší energií)
        elif 0.3 < progress < 0.7 and energy < 0.1:
            return SongSection.BRIDGE

        # Výchozí verse
        else:
            return SongSection.VERSE

    def _select_movement_pattern(self, emotion: EmotionalState, section: SongSection,
                               energy: float) -> MovementPattern:
        """Vybere vhodný pohybový vzor"""

        # Kombinace emoce a sekce určuje pohyb
        if section == SongSection.INTRO:
            return MovementPattern.SLOW_SWEEP
        elif section == SongSection.DROP:
            return MovementPattern.SYNC_ALL
        elif section == SongSection.BUILDUP:
            return MovementPattern.CHASE
        elif emotion == EmotionalState.TENSION:
            return MovementPattern.COUNTER
        elif emotion == EmotionalState.MYSTERY:
            return MovementPattern.CIRCLE
        elif emotion == EmotionalState.JOY and energy > 0.15:
            return MovementPattern.FAST_SWEEP
        elif emotion == EmotionalState.AGGRESSIVE:
            return MovementPattern.FIGURE_8
        elif emotion == EmotionalState.CALM:
            return MovementPattern.STATIC
        else:
            return MovementPattern.SLOW_SWEEP

    def _select_effects(self, emotion: EmotionalState, section: SongSection,
                       energy: float) -> List[str]:
        """Vybere efekty pro moment"""
        effects = []

        if section == SongSection.DROP:
            effects.extend(["strobe_fast", "all_lights", "intensity_max"])
        elif emotion == EmotionalState.TENSION:
            effects.extend(["strobe_slow", "contrast_colors"])
        elif emotion == EmotionalState.MYSTERY:
            effects.extend(["uv_active", "dim_lighting"])
        elif emotion == EmotionalState.JOY:
            effects.extend(["color_chase", "brightness_high"])
        elif energy > 0.15:
            effects.append("brightness_high")

        return effects

    def generate_advanced_timeline(self, output_path: str = "STORYTELLING_SHOW.tml"):
        """Generuje pokročilý timeline s hudebním příběhem"""
        print("🎭 Generating musical storytelling timeline...")

        # Analyzuj emocionální cestu
        musical_moments = self.analyze_emotional_journey()

        # Generuj timeline
        content = f"""[Params]
version = 0.2
commenttimeline = 0
lighttimelines = 6
mediatimelines = 1
showwaveform = 1
maxtime = 0:30:00
zoom = 0
timeline_1 = V I D E O   P I C T U R E   T I M E L I N E
timeline_2 = A U D I O   T I M E L I N E
timeline_3 = M O V I N G   H E A D S   C H O R E O G R A P H Y
timeline_4 = E M O T I O N A L   L I G H T I N G
timeline_5 = R H Y T H M   E F F E C T S
timeline_6 = A M B I E N T   B A C K G R O U N D

[Event_0]
timelineindex = 2
starttime = 0:00:00.0
path = Music/{self.audio_path.name}
length = {self._format_time(self.duration)}

"""

        event_counter = 1

        for moment in musical_moments:
            # Moving heads choreography (timeline 3)
            choreo_events = self._generate_choreography_events(moment, event_counter)
            for event in choreo_events:
                content += self._format_event(event)
                event_counter += 1

            # Emotional lighting (timeline 4)
            lighting_events = self._generate_emotional_lighting(moment, event_counter)
            for event in lighting_events:
                content += self._format_event(event)
                event_counter += 1

            # Rhythm effects (timeline 5)
            rhythm_events = self._generate_rhythm_effects(moment, event_counter)
            for event in rhythm_events:
                content += self._format_event(event)
                event_counter += 1

        # Ulož soubor
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Musical storytelling timeline created!")
        print(f"   Output: {output_path}")
        print(f"   Total events: {event_counter - 1}")
        print(f"   Musical moments: {len(musical_moments)}")

    def _format_time(self, seconds: float) -> str:
        """Formátuje čas"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)
        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def _format_event(self, event: dict) -> str:
        """Formátuje event do .tml formátu"""
        return f"""[Event_{event['index']}]
timelineindex = {event['timeline']}
starttime = {event['start_time']}
path = {event['path']}
length = {event['length']}
speed = {event.get('speed', 100)}
speedtype = 2

"""

    def _generate_choreography_events(self, moment: MusicalMoment, start_index: int) -> List[dict]:
        """Generuje moving heads choreografii"""
        events = []

        # Mapování choreografií podle emoce a sekce
        choreography_map = {
            (EmotionalState.CALM, SongSection.VERSE): "ambient_static.scex",
            (EmotionalState.CALM, SongSection.INTRO): "romantic_slow_sweep.scex",
            (EmotionalState.ENERGY, SongSection.CHORUS): "energetic_fast_sweep.scex",
            (EmotionalState.ENERGY, SongSection.DROP): "rainbow_explosion.scex",
            (EmotionalState.TENSION, SongSection.BUILDUP): "sequential_chase.scex",
            (EmotionalState.TENSION, SongSection.BRIDGE): "counter_balance.scex",
            (EmotionalState.RELEASE, SongSection.DROP): "synchronized_power.scex",
            (EmotionalState.MYSTERY, SongSection.INTRO): "mystical_circle.scex",
            (EmotionalState.JOY, SongSection.CHORUS): "energetic_fast_sweep.scex",
            (EmotionalState.MELANCHOLY, SongSection.VERSE): "romantic_slow_sweep.scex",
            (EmotionalState.AGGRESSIVE, SongSection.DROP): "strobo_madness.scex",
        }

        # Vyber choreografii
        key = (moment.emotion, moment.section)
        choreography = choreography_map.get(key)

        # Fallback podle energie
        if not choreography:
            if moment.energy_level > 0.7:
                choreography = "energetic_fast_sweep.scex"
            elif moment.energy_level > 0.4:
                choreography = "dynamic_figure_8.scex"
            else:
                choreography = "romantic_slow_sweep.scex"

        # Vytvoř event
        event = {
            "index": start_index,
            "timeline": 3,  # Moving heads timeline
            "start_time": self._format_time(moment.start_time),
            "path": f"generated_scenes_advanced/choreography/{choreography}",
            "length": self._format_time(moment.duration),
            "speed": int(100 * moment.energy_level + 50)  # 50-150 speed
        }
        events.append(event)

        return events

    def _generate_emotional_lighting(self, moment: MusicalMoment, start_index: int) -> List[dict]:
        """Generuje emocionální osvětlení"""
        events = []

        # Mapování barev podle emocí
        fixture_groups = {
            "bodovky": ["ceiling_spot_00", "ceiling_spot_01", "ceiling_spot_02", "ceiling_spot_03",
                       "ceiling_spot_04", "ceiling_spot_05", "ceiling_spot_06", "ceiling_spot_07",
                       "ceiling_spot_08", "ceiling_spot_09", "ceiling_spot_10", "ceiling_spot_11"],
            "walls": ["led_wall_00", "led_wall_01", "led_wall_02", "led_wall_03", "led_wall_04",
                     "led_wall_05", "led_wall_06", "led_wall_07", "led_wall_08", "led_wall_09", "led_wall_99"],
            "lavice": ["led_lavice_01", "led_lavice_02", "led_lavice_03", "led_lavice_04", "led_lavice_05",
                      "led_lavice_06", "led_lavice_07", "led_lavice_08", "led_lavice_09", "led_lavice_10", "led_lavice_11"],
            "kamna": ["led_kamna_41", "led_kamna_42"],
            "uv": ["uv_41", "uv_42"]
        }

        # Efekty podle emocí
        effect_map = {
            EmotionalState.CALM: "static",
            EmotionalState.ENERGY: "strobe_slow",
            EmotionalState.TENSION: "pulse",
            EmotionalState.RELEASE: "strobe_fast",
            EmotionalState.MYSTERY: "fade_in",
            EmotionalState.JOY: "strobe_slow",
            EmotionalState.MELANCHOLY: "fade_in",
            EmotionalState.AGGRESSIVE: "strobe_fast"
        }

        effect = effect_map.get(moment.emotion, "static")

        # Vyber skupiny světel podle sekce
        if moment.section in [SongSection.CHORUS, SongSection.DROP]:
            # Všechna světla
            selected_groups = ["bodovky", "walls", "lavice"]
        elif moment.section == SongSection.VERSE:
            # Jen bodovky a lavice
            selected_groups = ["bodovky", "lavice"]
        elif moment.section == SongSection.BRIDGE:
            # Walls a UV
            selected_groups = ["walls", "uv"]
        elif moment.section == SongSection.INTRO:
            # Postupné rozsvěcování
            selected_groups = ["lavice"]
        else:
            selected_groups = ["bodovky", "walls"]

        # Generuj eventy pro vybrané skupiny
        event_idx = start_index
        for group in selected_groups:
            if group in fixture_groups:
                # Pro každý fixture ve skupině
                for fixture in fixture_groups[group][:3]:  # Omez na 3 fixtures per group
                    scene_path = f"generated_scenes_systematic/individual/{fixture}/{moment.primary_color}_{effect}.scex"

                    # Zkontroluj jestli soubor existuje
                    if Path(scene_path).exists():
                        event = {
                            "index": event_idx,
                            "timeline": 4,  # Emotional lighting timeline
                            "start_time": self._format_time(moment.start_time),
                            "path": scene_path,
                            "length": self._format_time(moment.duration),
                            "speed": 100
                        }
                        events.append(event)
                        event_idx += 1

        return events

    def _generate_rhythm_effects(self, moment: MusicalMoment, start_index: int) -> List[dict]:
        """Generuje rytmické efekty"""
        events = []

        # Rytmické efekty jen pro vysokoenergetické momenty
        if moment.energy_level < 0.5:
            return events

        # Beat-synced efekty
        beat_interval = 60.0 / self.tempo  # Sekundy per beat
        num_beats = int(moment.duration / beat_interval)

        event_idx = start_index
        current_time = moment.start_time

        # Generuj beat events
        for beat in range(min(num_beats, 8)):  # Max 8 beats per moment
            # Bass hits na kamna
            if moment.bass_intensity > 0.1 and beat % 2 == 0:  # Every other beat
                event = {
                    "index": event_idx,
                    "timeline": 5,  # Rhythm effects timeline
                    "start_time": self._format_time(current_time),
                    "path": "generated_scenes_systematic/individual/led_kamna_41/red_pulse.scex",
                    "length": self._format_time(0.1),  # Krátké pulsy
                    "speed": 150
                }
                events.append(event)
                event_idx += 1

            # Treble hits na bodovky
            if moment.treble_intensity > 0.05 and beat % 4 == 1:  # Every 4th beat offset
                event = {
                    "index": event_idx,
                    "timeline": 5,  # Rhythm effects timeline
                    "start_time": self._format_time(current_time),
                    "path": "generated_scenes_systematic/individual/ceiling_spot_00/white_cool_pulse.scex",
                    "length": self._format_time(0.1),
                    "speed": 120
                }
                events.append(event)
                event_idx += 1

            current_time += beat_interval

        return events

    def analyze_song_structure(self) -> List[MusicalMoment]:
        """Analyzuje strukturu skladby a vrátí musical moments"""
        return self.analyze_emotional_journey()

def main():
    """Hlavní funkce"""
    audio_file = "placatá.mp3"

    if not Path(audio_file).exists():
        print(f"❌ Audio soubor {audio_file} nenalezen!")
        return

    print("🎭 Musical Storytelling System")
    print("=" * 50)

    # Vytvoř storytelling systém
    storyteller = MusicalStorytellingSystem(audio_file)

    # Analyzuj a vygeneruj timeline
    storyteller.generate_advanced_timeline()

    print()
    print("🎵 Hudební jazyk vytvořen!")
    print("   - Emocionální mapování")
    print("   - Moving heads choreografie")
    print("   - Inteligentní světelné efekty")
    print("   - Strukturální analýza skladby")

if __name__ == "__main__":
    main()
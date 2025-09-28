"""Spektakulární generátor timeline založený na pokročilé hudební analýze."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .advanced_music_analyzer import analyze_for_lighting
from .logging import get_logger
from .models import DMXEvent
from .models import DMXTimeline
from .models import SpeedType

# Import advanced moving heads choreographer
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from advanced_moving_heads import MovingHeadsChoreographer

logger = get_logger(__name__)


class SpectacularTimelineGenerator:
    """Generátor nádherných světelných show na základě pokročilé analýzy."""

    def __init__(self):
        """Initialize spectacular timeline generator."""
        # Initialize moving heads choreographer
        self.choreographer = MovingHeadsChoreographer()

        # Mapování frekvenčních pásem na typy světel
        self.frequency_to_fixtures = {
            "sub_bass": ["LED_Oven"],  # Hluboké basy -> kamna
            "bass": ["LED_walls", "Bodovky"],  # Basy -> zdi a strop
            "low_mid": ["SPOTS_walls"],  # Spodní středy -> wall spots
            "mid": ["Moving_heads"],  # Středy -> moving heads
            "high_mid": ["LED_lavice"],  # Vysoké středy -> lavice
            "presence": ["UV"],  # Přítomnost -> UV efekty
            "brilliance": ["Moving_heads"],  # Lesk -> moving heads (rychlé)
        }

        # Emocionální mapování barev
        self.emotion_colors = {
            "energetic_happy": ["red", "orange", "yellow"],
            "peaceful_happy": ["yellow", "white - teplá", "green"],
            "aggressive_sad": ["red", "purple", "blue"],
            "melancholic": ["blue", "azure", "white - studená"],
        }

        # Barvy pro různé energie
        self.energy_colors = {
            "explosive": ["red", "orange"],  # Extrémní energie
            "high": ["yellow", "white - teplá"],  # Vysoká energie
            "medium": ["green", "azure"],  # Střední energie
            "low": ["blue", "purple"],  # Nízká energie
            "ambient": ["white - studená"],  # Ambientní
        }

    def generate_spectacular_timeline(
        self, audio_path: Path, output_path: Path | None = None
    ) -> DMXTimeline:
        """Generuje spektakulární timeline ze souboru.

        Args:
            audio_path: Cesta k MP3/WAV souboru
            output_path: Volitelná výstupní cesta

        Returns:
            DMXTimeline s pokročilými efekty
        """
        logger.info(f"Generuji spektakulární timeline pro: {audio_path}")

        # Pokročilá analýza
        analysis = analyze_for_lighting(audio_path)

        # Vytvoř timeline
        timeline = DMXTimeline(
            audio_file=f"Music/{audio_path.name}",
            audio_length=self._format_duration(analysis["duration"]),
        )

        events = []

        # 1. STRUKTURÁLNÍ EFEKTY (intro, verse, chorus, outro)
        events.extend(self._generate_structural_effects(analysis))

        # 2. FREKVENČNÍ PÁSMA EFEKTY
        events.extend(self._generate_frequency_band_effects(analysis))

        # 3. RYTMICKÉ EFEKTY (beaty, synkopace)
        events.extend(self._generate_rhythm_effects(analysis))

        # 4. DYNAMICKÉ EFEKTY (transients, sustain)
        events.extend(self._generate_dynamic_effects(analysis))

        # 5. HARMONICKÉ EFEKTY (změny akordů, klíče)
        events.extend(self._generate_harmonic_effects(analysis))

        # 6. EMOCIONÁLNÍ AMBIENTNÍ OSVĚTLENÍ
        events.extend(self._generate_emotional_ambient(analysis))

        # 7. POKROČILÉ MOVING HEADS CHOREOGRAFIE
        events.extend(self._create_advanced_moving_heads_choreography(analysis, timeline_index=8))

        # Seřaď events podle času
        events.sort(key=lambda e: self._time_to_seconds(e.start_time))

        # Přidej do timeline
        for event in events:
            timeline.add_event(event)

        logger.info(f"Vygenerováno {len(events)} spektakulárních efektů")

        # Uloží pokud je zadána cesta
        if output_path:
            self._save_timeline(timeline, output_path)

        return timeline

    def _generate_structural_effects(self, analysis: dict) -> list[DMXEvent]:
        """Generuje efekty na základě struktury skladby."""
        events = []
        sections = analysis["structure"]["sections"]
        emotion = analysis["emotional_content"]["emotion_category"]

        for section in sections:
            section_type = section["type"]
            start_time = section["start_time"]
            duration = section["duration"]
            energy = section["energy"]

            if section_type == "intro":
                # Intro: postupné rozsvěcování
                events.extend(
                    self._create_intro_sequence(start_time, duration, emotion)
                )

            elif section_type == "verse":
                # Verse: umírněné osvětlení zaměřené na rytmus
                events.extend(
                    self._create_verse_lighting(start_time, duration, energy, emotion)
                )

            elif section_type == "chorus":
                # Chorus: plný efekt, všechna světla
                events.extend(
                    self._create_chorus_explosion(start_time, duration, energy, emotion)
                )

            elif section_type == "outro":
                # Outro: postupné zhasínání
                events.extend(
                    self._create_outro_sequence(start_time, duration, emotion)
                )

        return events

    def _generate_frequency_band_effects(self, analysis: dict) -> list[DMXEvent]:
        """Efekty založené na analýze frekvenčních pásem."""
        events = []
        bands = analysis["frequency_bands"]
        sample_rate = analysis["sample_rate"]
        emotion = analysis["emotional_content"]["emotion_category"]

        # Time axis
        hop_length = 256  # Z analyzátoru
        times = np.linspace(0, analysis["duration"], len(bands.sub_bass))

        # Analyzuj každé frekvenční pásmo
        for band_name, energy_curve in bands._asdict().items():
            if band_name not in self.frequency_to_fixtures:
                continue

            fixture_types = self.frequency_to_fixtures[band_name]

            # Najdi peaks v energii
            peaks = self._find_energy_peaks(energy_curve, prominence=0.3)

            for peak_idx in peaks:
                if peak_idx >= len(times):
                    continue

                peak_time = times[peak_idx]
                peak_energy = energy_curve[peak_idx]

                # Intenzita efektu na základě energie
                if peak_energy > np.percentile(energy_curve, 90):
                    intensity = "explosive"
                elif peak_energy > np.percentile(energy_curve, 75):
                    intensity = "high"
                elif peak_energy > np.percentile(energy_curve, 50):
                    intensity = "medium"
                else:
                    intensity = "low"

                # Vytvoř efekt pro dané pásmo
                events.extend(
                    self._create_frequency_effect(
                        peak_time, band_name, fixture_types, intensity, emotion
                    )
                )

        return events

    def _generate_rhythm_effects(self, analysis: dict) -> list[DMXEvent]:
        """Rytmické efekty na beaty a synkopace."""
        events = []
        rhythm = analysis["rhythm"]
        emotion = analysis["emotional_content"]["emotion_category"]

        # Strong beats (downbeats)
        for i, beat_time in enumerate(rhythm.downbeats):
            if i < len(rhythm.beat_strength):
                strength = rhythm.beat_strength[
                    min(i * 4, len(rhythm.beat_strength) - 1)
                ]
            else:
                strength = 0.5

            # Silné beaty -> Moving heads + wall spots
            if strength > 0.7:  # Velmi silný beat
                events.append(
                    DMXEvent(
                        timeline_index=3,
                        start_time=self._format_time(beat_time),
                        path="Moving_heads/MH_oven_red.scex",
                        length="0:00:00.5",
                        speed=100,
                        speed_type=SpeedType.PERCENTAGE,
                        fade_in=1,
                        fade_out=200,
                    )
                )

                # Přidej wall spots flash
                events.append(
                    DMXEvent(
                        timeline_index=4,
                        start_time=self._format_time(beat_time + 0.1),
                        path="SPOTS_walls/SPOTS_all/SPOTS_orange.scex",
                        length="0:00:00.3",
                        speed=100,
                        speed_type=SpeedType.PERCENTAGE,
                        fade_in=1,
                        fade_out=1,
                    )
                )

        # Syncopation effects
        if len(rhythm.syncopation) > 0:
            avg_syncopation = np.mean(rhythm.syncopation)

            if avg_syncopation > 0.5:  # Vysoká synkopace
                # Vytvoř off-beat efekty
                events.extend(
                    self._create_syncopation_effects(rhythm.beat_times, emotion)
                )

        return events

    def _generate_dynamic_effects(self, analysis: dict) -> list[DMXEvent]:
        """Efekty na základě dynamických změn."""
        events = []
        dynamics = analysis["dynamics"]
        emotion = analysis["emotional_content"]["emotion_category"]

        # Transients -> náhlé blesky
        for transient_time in dynamics.transients:
            # Rychlý flash všemi světly
            events.append(
                DMXEvent(
                    timeline_index=5,
                    start_time=self._format_time(transient_time),
                    path="LED_walls/Walls_all/Walls_white - studená.scex",
                    length="0:00:00.1",
                    speed=100,
                    speed_type=SpeedType.PERCENTAGE,
                    fade_in=1,
                    fade_out=1,
                )
            )

            # UV flash pro extra efekt
            events.append(
                DMXEvent(
                    timeline_index=12,
                    start_time=self._format_time(transient_time + 0.05),
                    path="UV/UV.scex",
                    length="0:00:00.2",
                    speed=100,
                    speed_type=SpeedType.PERCENTAGE,
                )
            )

        # Sustain regions -> plynulé přechody
        hop_length = 256
        times = np.linspace(0, analysis["duration"], len(dynamics.sustain_regions))

        in_sustain = False
        sustain_start = 0

        for i, is_sustain in enumerate(dynamics.sustain_regions):
            if is_sustain and not in_sustain:
                # Začátek sustain regionu
                in_sustain = True
                sustain_start = times[i]

            elif not is_sustain and in_sustain:
                # Konec sustain regionu
                in_sustain = False
                sustain_duration = times[i] - sustain_start

                if sustain_duration > 2.0:  # Minimálně 2 sekundy
                    # Vytvoř plynulý efekt
                    color = self._select_emotion_color(emotion)
                    events.append(
                        DMXEvent(
                            timeline_index=6,
                            start_time=self._format_time(sustain_start),
                            path=f"Bodovky/Bodovky_all/Bodovka_{color}.scex",
                            length=self._format_duration(sustain_duration),
                            speed=30,  # Pomalý, hladký efekt
                            speed_type=SpeedType.PERCENTAGE,
                            fade_in=1000,
                            fade_out=1000,
                        )
                    )

        return events

    def _generate_harmonic_effects(self, analysis: dict) -> list[DMXEvent]:
        """Efekty na harmonické změny."""
        events = []
        harmonic = analysis["harmonic"]
        chroma = harmonic["chroma"]

        # Detekuj změny v harmonickém obsahu
        if chroma.shape[1] > 1:
            # Vypočti harmonickou variabilitu
            chroma_diff = np.diff(chroma, axis=1)
            harmonic_change = np.sum(np.abs(chroma_diff), axis=0)

            # Najdi významné harmonické změny
            change_threshold = np.percentile(harmonic_change, 85)
            change_indices = np.where(harmonic_change > change_threshold)[0]

            hop_length = 256
            times = np.linspace(0, analysis["duration"], len(harmonic_change))

            for idx in change_indices:
                if idx >= len(times):
                    continue

                change_time = times[idx]
                change_magnitude = harmonic_change[idx]

                # Významnější změny -> dramatičtější efekty
                if change_magnitude > np.percentile(harmonic_change, 95):
                    # Velká harmonická změna -> změna barvy všech světel
                    emotion = analysis["emotional_content"]["emotion_category"]
                    new_color = self._select_emotion_color(emotion)

                    events.append(
                        DMXEvent(
                            timeline_index=7,
                            start_time=self._format_time(change_time),
                            path=f"LED_walls/Walls_all/Walls_{new_color}.scex",
                            length="0:00:03.0",
                            speed=50,
                            speed_type=SpeedType.PERCENTAGE,
                            fade_in=500,
                            fade_out=500,
                        )
                    )

        return events

    def _generate_emotional_ambient(self, analysis: dict) -> list[DMXEvent]:
        """Ambientní osvětlení na základě emocí."""
        events = []
        emotion = analysis["emotional_content"]
        duration = analysis["duration"]

        # Základní ambientní barva na celou skladbu
        ambient_color = self._select_emotion_color(emotion["emotion_category"])

        # Kamna - teplá barva pro pozitivní emoce
        if emotion["valence"] > 0.5:
            events.append(
                DMXEvent(
                    timeline_index=8,
                    start_time="0:00:05.0",
                    path=f"LED_Oven/Oven_{ambient_color}.scex",
                    length=self._format_duration(duration - 10.0),
                    speed=20,
                    speed_type=SpeedType.PERCENTAGE,
                    fade_in=3000,
                    fade_out=3000,
                )
            )

        # Lavice - jemné osvětlení
        events.append(
            DMXEvent(
                timeline_index=9,
                start_time="0:00:03.0",
                path=f"LED_lavice/LED_lavice_{ambient_color}.scex",
                length=self._format_duration(duration - 6.0),
                speed=25,
                speed_type=SpeedType.PERCENTAGE,
                fade_in=2000,
                fade_out=2000,
            )
        )

        return events

    def _create_intro_sequence(
        self, start_time: float, duration: float, emotion: str
    ) -> list[DMXEvent]:
        """Vytvoří postupné intro efekty."""
        events = []
        colors = self.emotion_colors[emotion]

        # Postupné rozsvěcování každé skupiny světel
        fixtures = ["Bodovky", "SPOTS_walls", "LED_walls", "LED_Oven"]

        for i, fixture_group in enumerate(fixtures):
            delay = (duration / len(fixtures)) * i
            event_start = start_time + delay

            color = colors[i % len(colors)]

            events.append(
                DMXEvent(
                    timeline_index=3 + i,
                    start_time=self._format_time(event_start),
                    path=f"{fixture_group}/{fixture_group}_all/{fixture_group}_{color}.scex",
                    length=self._format_duration(duration - delay),
                    speed=30,
                    speed_type=SpeedType.PERCENTAGE,
                    fade_in=2000,
                    fade_out=1000,
                )
            )

        return events

    def _create_chorus_explosion(
        self, start_time: float, duration: float, energy: float, emotion: str
    ) -> list[DMXEvent]:
        """Vytvoří explozivní chorus efekty."""
        events = []
        colors = self.emotion_colors[emotion]

        # Všechna světla najednou s vysokou intenzitou
        main_color = colors[0]

        # Moving heads - rychlé pohyby
        events.append(
            DMXEvent(
                timeline_index=3,
                start_time=self._format_time(start_time),
                path=f"Moving_heads/MH_oven_{main_color}.scex",
                length=self._format_duration(duration),
                speed=100,
                speed_type=SpeedType.PERCENTAGE,
                fade_in=100,
                fade_out=300,
            )
        )

        # LED zdi - pulzování
        events.append(
            DMXEvent(
                timeline_index=4,
                start_time=self._format_time(start_time + 0.2),
                path="Special_efects/Walls_flashing_snake/Walls_flashing_snake_red.scex",
                length=self._format_duration(duration - 0.2),
                speed=2,  # Rychlé pulzování
                speed_type=SpeedType.BPM_BASED,
            )
        )

        # UV pro extra drama
        events.append(
            DMXEvent(
                timeline_index=12,
                start_time=self._format_time(start_time + 0.5),
                path="UV/UV.scex",
                length=self._format_duration(duration - 0.5),
                speed=100,
                speed_type=SpeedType.PERCENTAGE,
            )
        )

        return events

    def _create_advanced_moving_heads_choreography(
        self, music_analysis: dict, timeline_index: int = 3
    ) -> list[DMXEvent]:
        """Vytvoří pokročilou choreografii pro moving heads na základě hudební analýzy."""
        events = []

        # Extract music characteristics
        bpm = music_analysis.get("bpm", 120)
        energy = music_analysis.get("energy_mean", 0.5)
        valence = music_analysis.get("valence_mean", 0.5)
        duration = music_analysis.get("duration", 240)

        # Create music analysis dict for choreographer
        choreo_analysis = {
            "bpm": bpm,
            "energy": energy,
            "valence": valence
        }

        # Generate choreography patterns
        choreography = self.choreographer.create_music_reactive_choreography(choreo_analysis)

        if not choreography:
            logger.warning("No choreography patterns generated")
            return events

        pattern = choreography[0]  # Use the first (main) pattern
        logger.info(f"Using choreography pattern: {pattern.name}")

        # Generate timeline events for the pattern
        current_time = 0.0
        pattern_duration_sec = pattern.duration_ms / 1000.0

        # Determine how many times to repeat pattern based on song duration
        repeats = int(duration / pattern_duration_sec) + 1

        for repeat in range(repeats):
            if current_time >= duration:
                break

            # Determine which step in the pattern based on music analysis
            # Use beat synchronization for more precise timing
            beat_duration = 60.0 / bpm  # seconds per beat
            beats_per_pattern = pattern_duration_sec / beat_duration

            for step_idx, position in enumerate(pattern.positions):
                step_start_time = current_time + (step_idx / len(pattern.positions)) * pattern_duration_sec

                if step_start_time >= duration:
                    break

                # Calculate step duration
                step_duration = pattern_duration_sec / len(pattern.positions)

                # Adapt to music energy - higher energy = faster changes
                if energy > 0.7:
                    step_duration *= 0.6  # 40% faster for high energy
                elif energy < 0.3:
                    step_duration *= 1.4  # 40% slower for low energy

                # Create scene path for this choreography step
                scene_path = f"generated_scenes_advanced/advanced_moving_heads/{pattern.name}/step_{step_idx:02d}.scex"

                # Create DMX event
                event = DMXEvent(
                    timeline_index=timeline_index,
                    start_time=self._format_time(step_start_time),
                    path=scene_path,
                    length=self._format_duration(step_duration),
                    speed=int(80 + energy * 40),  # Speed based on energy (80-120%)
                    speed_type=SpeedType.PERCENTAGE,
                    fade_in=int(200 + energy * 300),  # Fade timing based on energy
                    fade_out=int(100 + energy * 200),
                )

                events.append(event)
                logger.debug(f"Added moving heads event at {step_start_time:.2f}s: {scene_path}")

            current_time += pattern_duration_sec

        # Add some variation during high energy sections
        if energy > 0.8:
            # Add extra fast pattern variations
            buildup_pattern = self.choreographer.patterns.get("buildup")
            if buildup_pattern:
                # Use buildup pattern at high energy moments
                high_energy_times = [duration * 0.25, duration * 0.5, duration * 0.75]

                for he_time in high_energy_times:
                    if he_time < duration - 5:  # Leave some buffer at end
                        for step_idx, position in enumerate(buildup_pattern.positions):
                            step_time = he_time + (step_idx / len(buildup_pattern.positions)) * 3.0  # 3 second burst

                            scene_path = f"generated_scenes_advanced/advanced_moving_heads/buildup/step_{step_idx:02d}.scex"

                            event = DMXEvent(
                                timeline_index=timeline_index + 1,  # Use different timeline
                                start_time=self._format_time(step_time),
                                path=scene_path,
                                length="0:00:00.2",  # Very fast changes
                                speed=120,
                                speed_type=SpeedType.PERCENTAGE,
                                fade_in=50,
                                fade_out=50,
                            )

                            events.append(event)

        logger.info(f"Generated {len(events)} advanced moving heads choreography events")
        return events

    def _find_energy_peaks(
        self, energy_curve: np.ndarray, prominence: float = 0.3
    ) -> np.ndarray:
        """Najde vrcholy v energetické křivce."""
        from scipy.signal import find_peaks

        # Normalize
        if np.max(energy_curve) > 0:
            normalized = energy_curve / np.max(energy_curve)
        else:
            normalized = energy_curve

        # Find peaks
        peaks, _ = find_peaks(normalized, prominence=prominence, distance=10)

        return peaks

    def _select_emotion_color(self, emotion: str) -> str:
        """Vybere barvu na základě emoce."""
        if emotion in self.emotion_colors:
            colors = self.emotion_colors[emotion]
            # Vybere první barvu jako hlavní
            return colors[0]
        return "white - studená"  # Default

    def _format_time(self, seconds: float) -> str:
        """Formátuje čas do H:MM:SS.f."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)

        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def _format_duration(self, seconds: float) -> str:
        """Formátuje trvání do H:MM:SS.f."""
        return self._format_time(seconds)

    def _time_to_seconds(self, time_str: str) -> float:
        """Převede čas na sekundy."""
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])

        sec_parts = parts[2].split(".")
        seconds = int(sec_parts[0])
        decimal = int(sec_parts[1]) / 10.0 if len(sec_parts) > 1 else 0.0

        return hours * 3600 + minutes * 60 + seconds + decimal

    def _save_timeline(self, timeline: DMXTimeline, output_path: Path) -> None:
        """Uloží timeline do souboru."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(timeline.to_tml_format())

            logger.info(f"Spektakulární timeline uložen do: {output_path}")

        except Exception as e:
            logger.error(f"Chyba při ukládání timeline: {e}")
            raise


# Convenience functions
def create_spectacular_timeline(
    audio_path: Path, output_path: Path | None = None
) -> DMXTimeline:
    """Vytvoří spektakulární timeline ze souboru."""
    generator = SpectacularTimelineGenerator()
    return generator.generate_spectacular_timeline(audio_path, output_path)

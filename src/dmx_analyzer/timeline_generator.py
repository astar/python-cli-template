"""Timeline generation module for creating DMX lighting sequences from audio analysis."""

from __future__ import annotations

import random
from pathlib import Path

from .logging import get_logger
from .models import AudioAnalysis
from .models import DMXEvent
from .models import DMXFixture
from .models import DMXTimeline
from .models import GenerationConfig
from .models import SpeedType

logger = get_logger(__name__)


class TimelineGenerator:
    """Generates DMX lighting timelines from audio analysis."""

    def __init__(self, config: GenerationConfig | None = None):
        """Initialize timeline generator.

        Args:
            config: Generation configuration
        """
        self.config = config or GenerationConfig()
        self.fixtures: list[DMXFixture] = []

        # Scene mappings based on energy and valence
        self.color_scenes = {
            "red": ["red", "orange"],
            "blue": ["blue", "azure"],
            "green": ["green"],
            "yellow": ["yellow"],
            "purple": ["purple"],
            "white": ["white - studená", "white - teplá"],
        }

        # Energy-based color selection
        self.energy_colors = {
            "low": ["blue", "azure", "purple"],
            "medium": ["green", "white - studená", "white - teplá"],
            "high": ["red", "orange", "yellow"],
        }

    def load_fixtures(self, fixtures_path: Path) -> None:
        """Load DMX fixtures configuration from file.

        Args:
            fixtures_path: Path to fixtures configuration file
        """
        logger.info(f"Loading fixtures from: {fixtures_path}")

        try:
            # Parse fixtures.ini file
            import configparser

            config = configparser.ConfigParser()
            config.read(fixtures_path)

            fixtures = []
            for section in config.sections():
                if section.startswith("Fixture"):
                    fixture_data = dict(config[section])

                    fixture = DMXFixture(
                        id=int(fixture_data.get("id", 0)),
                        name=fixture_data.get("name", ""),
                        address=int(fixture_data.get("address", 1)),
                        model=fixture_data.get("model", ""),
                        group=fixture_data.get("group", ""),
                        channels=4,  # Default RGBW
                    )
                    fixtures.append(fixture)

            self.fixtures = fixtures
            logger.info(f"Loaded {len(fixtures)} fixtures")

        except Exception as e:
            logger.error(f"Failed to load fixtures: {e}")
            raise ValueError(f"Could not load fixtures configuration: {e}") from e

    def generate_timeline(
        self, analysis: AudioAnalysis, output_path: Path | None = None
    ) -> DMXTimeline:
        """Generate DMX timeline from audio analysis.

        Args:
            analysis: Audio analysis results
            output_path: Optional output path for timeline file

        Returns:
            Generated DMX timeline
        """
        logger.info("Generating DMX timeline")

        # Create timeline
        timeline = DMXTimeline(
            audio_file=f"Music/{analysis.file_path.name}",
            audio_length=self._format_duration(analysis.duration),
        )

        # Add fixtures to timeline
        timeline.fixtures = self.fixtures.copy()

        # Generate events based on audio features
        events = self._generate_events(analysis)

        # Add events to timeline
        for event in events:
            timeline.add_event(event)

        logger.info(f"Generated {len(events)} events")

        # Save if output path provided
        if output_path:
            self._save_timeline(timeline, output_path)

        return timeline

    def _generate_events(self, analysis: AudioAnalysis) -> list[DMXEvent]:
        """Generate DMX events from audio analysis.

        Args:
            analysis: Audio analysis results

        Returns:
            List of generated DMX events
        """
        events = []

        # Generate beat-synchronized events
        if self.config.beat_sync and analysis.beats:
            events.extend(self._generate_beat_events(analysis))

        # Generate energy-based events
        events.extend(self._generate_energy_events(analysis))

        # Generate ambient/background lighting
        events.extend(self._generate_ambient_events(analysis))

        # Sort events by start time
        events.sort(key=lambda e: self._time_to_seconds(e.start_time))

        return events

    def _generate_beat_events(self, analysis: AudioAnalysis) -> list[DMXEvent]:
        """Generate events synchronized to beat times.

        Args:
            analysis: Audio analysis results

        Returns:
            Beat-synchronized events
        """
        events = []

        # Select fixtures for beat sync (moving heads work well)
        moving_fixtures = [f for f in self.fixtures if "Intimidator" in f.model]
        wall_spots = [f for f in self.fixtures if "Spot_" in f.name]

        # Generate events on strong beats (every 4th beat for 4/4 time)
        beat_interval = 60.0 / analysis.features.bpm
        strong_beat_interval = beat_interval * 4

        for i, beat_time in enumerate(analysis.beats):
            if i % 4 == 0:  # Strong beat
                # Choose color based on energy at this time
                energy_level = self._get_energy_at_time(analysis, beat_time)
                color = self._select_color_by_energy(energy_level)

                # Moving head event
                if moving_fixtures and random.random() < 0.6:  # 60% chance
                    fixture = random.choice(moving_fixtures)
                    event = DMXEvent(
                        timeline_index=3,  # First light timeline
                        start_time=self._format_time(beat_time),
                        path=f"Moving_heads/MH_oven_{color}.scex",
                        length=self._format_duration(strong_beat_interval * 0.8),
                        speed=100,
                        speed_type=SpeedType.PERCENTAGE,
                    )
                    events.append(event)

                # Wall spots flash
                if wall_spots and random.random() < 0.4:  # 40% chance
                    spot = random.choice(wall_spots)
                    spot_num = spot.name.split("#")[-1] if "#" in spot.name else "1"

                    event = DMXEvent(
                        timeline_index=4,
                        start_time=self._format_time(beat_time),
                        path=f"SPOTS_walls/SPOTS_single/SPOT_{spot_num}/SPOT_{spot_num}_{color}.scex",
                        length=self._format_duration(beat_interval * 0.5),
                        speed=100,
                        speed_type=SpeedType.PERCENTAGE,
                        fade_in=1,
                        fade_out=1,
                    )
                    events.append(event)

        return events

    def _generate_energy_events(self, analysis: AudioAnalysis) -> list[DMXEvent]:
        """Generate events based on energy changes.

        Args:
            analysis: Audio analysis results

        Returns:
            Energy-based events
        """
        events = []

        # Analyze energy over time using onset detection
        high_energy_times = []

        # Find high-energy moments (onset times with high spectral content)
        for onset_time in analysis.onset_times:
            energy = self._get_energy_at_time(analysis, onset_time)
            if energy > self.config.energy_threshold:
                high_energy_times.append(onset_time)

        # Generate events for high-energy moments
        for i, energy_time in enumerate(high_energy_times):
            # Skip if too close to previous event
            if (
                i > 0
                and (energy_time - high_energy_times[i - 1])
                < self.config.min_event_duration
            ):
                continue

            energy_level = self._get_energy_at_time(analysis, energy_time)

            # LED wall effects for high energy
            if energy_level > 0.7:
                color = self._select_color_by_energy(energy_level)

                # All walls flash
                event = DMXEvent(
                    timeline_index=5,
                    start_time=self._format_time(energy_time),
                    path=f"LED_Walls/Walls_all/Walls_{color}.scex",
                    length=self._format_duration(self.config.max_event_duration),
                    speed=100,
                    speed_type=SpeedType.PERCENTAGE,
                    fade_in=200,
                    fade_out=300,
                )
                events.append(event)

            # Individual wall effects for medium energy
            elif energy_level > 0.5:
                color = self._select_color_by_energy(energy_level)
                wall_num = random.randint(1, 11)

                event = DMXEvent(
                    timeline_index=6,
                    start_time=self._format_time(energy_time),
                    path=f"LED_Walls/Walls_single/Walls_{wall_num}/Walls_{wall_num}_{color}.scex",
                    length=self._format_duration(self.config.min_event_duration * 2),
                    speed=100,
                    speed_type=SpeedType.PERCENTAGE,
                )
                events.append(event)

        return events

    def _generate_ambient_events(self, analysis: AudioAnalysis) -> list[DMXEvent]:
        """Generate ambient/background lighting events.

        Args:
            analysis: Audio analysis results

        Returns:
            Ambient lighting events
        """
        events = []

        # Background lighting based on valence and energy
        base_color = "blue" if analysis.features.valence < 0.5 else "yellow"

        # Ceiling spots for ambient lighting
        ambient_start = 10.0  # Start ambient after intro
        ambient_duration = analysis.duration - ambient_start - 10.0  # End before outro

        if ambient_duration > 0:
            event = DMXEvent(
                timeline_index=7,
                start_time=self._format_time(ambient_start),
                path=f"Bodovky/Bodovky_all/Bodovka_{base_color}.scex",
                length=self._format_duration(ambient_duration),
                speed=50,  # Slower, ambient speed
                speed_type=SpeedType.PERCENTAGE,
                fade_in=2000,  # Long fade in
                fade_out=2000,  # Long fade out
            )
            events.append(event)

        # LED stove for warmth
        if analysis.features.valence > 0.6:  # Happy music
            stove_color = "orange" if analysis.features.energy > 0.5 else "red"

            event = DMXEvent(
                timeline_index=8,
                start_time=self._format_time(5.0),
                path=f"LED_Oven/Oven_{stove_color}.scex",
                length=self._format_duration(analysis.duration - 10.0),
                speed=30,
                speed_type=SpeedType.PERCENTAGE,
                fade_in=3000,
                fade_out=3000,
            )
            events.append(event)

        return events

    def _get_energy_at_time(self, analysis: AudioAnalysis, time: float) -> float:
        """Get energy level at specific time.

        Args:
            analysis: Audio analysis results
            time: Time in seconds

        Returns:
            Energy level (0-1)
        """
        # Simple interpolation based on spectral centroids
        if not analysis.spectral_centroids:
            return analysis.features.energy

        # Map time to centroid index
        duration = analysis.duration
        num_centroids = len(analysis.spectral_centroids)

        index = int((time / duration) * num_centroids)
        index = max(0, min(index, num_centroids - 1))

        # Normalize spectral centroid to energy estimate
        centroid = analysis.spectral_centroids[index]
        max_centroid = max(analysis.spectral_centroids)

        return min(1.0, centroid / max_centroid) if max_centroid > 0 else 0.5

    def _select_color_by_energy(self, energy: float) -> str:
        """Select color based on energy level.

        Args:
            energy: Energy level (0-1)

        Returns:
            Color name
        """
        if energy > 0.7:
            return random.choice(self.energy_colors["high"])
        if energy > 0.4:
            return random.choice(self.energy_colors["medium"])
        return random.choice(self.energy_colors["low"])

    def _format_time(self, seconds: float) -> str:
        """Format time in seconds to H:MM:SS.f format.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60

        # Split seconds and milliseconds
        whole_secs = int(secs)
        millisecs = int((secs - whole_secs) * 10)  # Single decimal place

        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{millisecs}"

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to H:MM:SS.f format.

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration string
        """
        return self._format_time(seconds)

    def _time_to_seconds(self, time_str: str) -> float:
        """Convert time string to seconds.

        Args:
            time_str: Time in H:MM:SS.f format

        Returns:
            Time in seconds
        """
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])

        sec_parts = parts[2].split(".")
        seconds = int(sec_parts[0])
        decimal = int(sec_parts[1]) / 10.0 if len(sec_parts) > 1 else 0.0

        return hours * 3600 + minutes * 60 + seconds + decimal

    def _save_timeline(self, timeline: DMXTimeline, output_path: Path) -> None:
        """Save timeline to file.

        Args:
            timeline: DMX timeline to save
            output_path: Output file path
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(timeline.to_tml_format())

            logger.info(f"Timeline saved to: {output_path}")

        except Exception as e:
            logger.error(f"Failed to save timeline: {e}")
            raise


def generate_dmx_timeline(
    analysis: AudioAnalysis,
    fixtures_path: Path | None = None,
    output_path: Path | None = None,
    config: GenerationConfig | None = None,
) -> DMXTimeline:
    """Convenience function to generate a DMX timeline.

    Args:
        analysis: Audio analysis results
        fixtures_path: Path to fixtures configuration
        output_path: Output path for timeline file
        config: Generation configuration

    Returns:
        Generated DMX timeline
    """
    generator = TimelineGenerator(config)

    if fixtures_path:
        generator.load_fixtures(fixtures_path)

    return generator.generate_timeline(analysis, output_path)

#!/usr/bin/env python3
"""
Spectacular Timeline Generator focused on Moving Heads Choreography
"""

from pathlib import Path
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dmx_analyzer.advanced_music_analyzer import analyze_for_lighting
from dmx_analyzer.models import DMXTimeline, DMXEvent, SpeedType
from dmx_analyzer.logging import get_logger

# Import advanced moving heads choreographer
from advanced_moving_heads import MovingHeadsChoreographer

logger = get_logger(__name__)

class MovingHeadsSpectacularGenerator:
    """Spectacular timeline generator focused on moving heads choreography"""

    def __init__(self):
        self.choreographer = MovingHeadsChoreographer()

    def generate_choreography_timeline(self, audio_path: Path, output_path: Path) -> DMXTimeline:
        """Generate timeline focused on moving heads choreography"""

        logger.info(f"Generating moving heads spectacular show for: {audio_path}")

        # Analyze music
        try:
            analysis = analyze_for_lighting(audio_path)
        except Exception as e:
            logger.error(f"Music analysis failed: {e}")
            # Create basic analysis as fallback
            analysis = {
                "bpm": 120,
                "energy_mean": 0.6,
                "valence_mean": 0.7,
                "duration": 180,  # 3 minutes default
            }

        # Create timeline
        timeline = DMXTimeline(
            audio_file=f"Music/{audio_path.name}",
            audio_length=self._format_duration(analysis["duration"]),
        )

        events = []

        # 1. BASIC AMBIENT LIGHTING (walls and ceiling)
        events.extend(self._create_basic_ambient(analysis))

        # 2. ADVANCED MOVING HEADS CHOREOGRAPHY (main attraction)
        events.extend(self._create_moving_heads_choreography(analysis))

        # 3. ACCENT EFFECTS for high energy moments
        events.extend(self._create_accent_effects(analysis))

        # Sort events by time
        events.sort(key=lambda e: self._time_to_seconds(e.start_time))

        # Add to timeline
        for event in events:
            timeline.add_event(event)

        logger.info(f"Generated {len(events)} events with advanced moving heads choreography")

        # Save timeline
        self._save_timeline(timeline, output_path)

        return timeline

    def _create_basic_ambient(self, analysis: dict) -> list[DMXEvent]:
        """Create basic ambient lighting for walls and ceiling"""
        events = []
        duration = analysis["duration"]
        energy = analysis.get("energy_mean", 0.5)

        # Choose ambient color based on energy/valence
        valence = analysis.get("valence_mean", 0.5)

        if energy > 0.7:
            ambient_color = "red" if valence > 0.5 else "blue"
        elif energy > 0.4:
            ambient_color = "yellow" if valence > 0.5 else "green"
        else:
            ambient_color = "white_cool"

        # Wall spots ambient
        events.append(DMXEvent(
            timeline_index=5,  # Wall spots timeline
            start_time="0:00:05.0",
            path=f"generated_scenes_systematic/groups/walls_1&11/{ambient_color}_static.scex",
            length=self._format_duration(duration - 10),
            speed=50,
            speed_type=SpeedType.PERCENTAGE,
            fade_in=3000,
            fade_out=3000,
        ))

        # Ceiling spots ambient
        events.append(DMXEvent(
            timeline_index=6,  # Ceiling spots timeline
            start_time="0:00:10.0",
            path=f"generated_scenes_systematic/individual/ceiling_spot_00/{ambient_color}_static.scex",
            length=self._format_duration(duration - 15),
            speed=30,
            speed_type=SpeedType.PERCENTAGE,
            fade_in=5000,
            fade_out=2000,
        ))

        return events

    def _create_moving_heads_choreography(self, analysis: dict) -> list[DMXEvent]:
        """Create advanced moving heads choreography"""
        events = []

        # Extract music characteristics
        bpm = analysis.get("bpm", 120)
        energy = analysis.get("energy_mean", 0.5)
        valence = analysis.get("valence_mean", 0.5)
        duration = analysis.get("duration", 240)

        logger.info(f"Creating choreography: BPM={bpm}, Energy={energy:.2f}, Valence={valence:.2f}")

        # Create music analysis dict for choreographer
        choreo_analysis = {
            "bpm": bpm,
            "energy": energy,
            "valence": valence
        }

        # Generate choreography patterns
        choreography = self.choreographer.create_music_reactive_choreography(choreo_analysis)

        if not choreography:
            logger.warning("No choreography patterns generated, using default")
            # Use a default pattern
            pattern_name = "buildup" if energy > 0.7 else "intro"
            pattern = self.choreographer.patterns[pattern_name]
        else:
            pattern = choreography[0]

        logger.info(f"Using choreography pattern: {pattern.name}")

        # Generate timeline events
        current_time = 15.0  # Start after ambient lighting
        pattern_duration_sec = pattern.duration_ms / 1000.0

        # Calculate how many full patterns fit in the song
        remaining_duration = duration - current_time - 10  # Leave 10s at end
        repeats = int(remaining_duration / pattern_duration_sec) + 1

        for repeat in range(repeats):
            if current_time >= duration - 10:
                break

            # Create variation based on position in song
            variation = self._get_pattern_variation(repeat, repeats, energy)

            for step_idx, position in enumerate(pattern.positions):
                step_start_time = current_time + (step_idx / len(pattern.positions)) * pattern_duration_sec

                if step_start_time >= duration - 5:
                    break

                # Calculate step duration with variations
                base_step_duration = pattern_duration_sec / len(pattern.positions)

                # Apply variations based on song progress and energy
                step_duration = base_step_duration * variation["duration_multiplier"]
                speed = int(variation["base_speed"] * (1.0 + energy * 0.5))

                # Choose scene path based on pattern and variation
                if variation["use_color_scheme"]:
                    scene_path = f"generated_scenes_advanced/advanced_moving_heads/color_schemes/{variation['color_scheme']}/{pattern.name}_step_{step_idx:02d}.scex"
                else:
                    scene_path = f"generated_scenes_advanced/advanced_moving_heads/{pattern.name}/step_{step_idx:02d}.scex"

                # Create DMX event
                event = DMXEvent(
                    timeline_index=3,  # Moving heads main timeline
                    start_time=self._format_time(step_start_time),
                    path=scene_path,
                    length=self._format_duration(step_duration),
                    speed=speed,
                    speed_type=SpeedType.PERCENTAGE,
                    fade_in=variation["fade_in"],
                    fade_out=variation["fade_out"],
                )

                events.append(event)

            current_time += pattern_duration_sec

        # Add high energy bursts at key moments
        if energy > 0.8:
            events.extend(self._add_energy_bursts(duration, bpm))

        logger.info(f"Generated {len(events)} moving heads choreography events")
        return events

    def _get_pattern_variation(self, repeat: int, total_repeats: int, energy: float) -> dict:
        """Get pattern variation based on position in song"""
        progress = repeat / max(total_repeats - 1, 1)  # 0.0 to 1.0

        if progress < 0.2:  # Intro section
            return {
                "duration_multiplier": 1.4,  # Slower
                "base_speed": 60,
                "fade_in": 800,
                "fade_out": 400,
                "use_color_scheme": True,
                "color_scheme": "cool_mysterious"
            }
        elif progress < 0.4:  # Build up
            return {
                "duration_multiplier": 1.0,
                "base_speed": 80,
                "fade_in": 400,
                "fade_out": 300,
                "use_color_scheme": True,
                "color_scheme": "warm_intimate" if energy < 0.6 else "high_energy"
            }
        elif progress < 0.8:  # Main section
            return {
                "duration_multiplier": 0.8,  # Faster
                "base_speed": 100,
                "fade_in": 200,
                "fade_out": 200,
                "use_color_scheme": True,
                "color_scheme": "high_energy"
            }
        else:  # Outro
            return {
                "duration_multiplier": 1.2,
                "base_speed": 70,
                "fade_in": 600,
                "fade_out": 800,
                "use_color_scheme": True,
                "color_scheme": "ethereal"
            }

    def _add_energy_bursts(self, duration: float, bpm: float) -> list[DMXEvent]:
        """Add high energy burst effects at key moments"""
        events = []

        # Add bursts at quarter, half, and three-quarter points
        burst_times = [duration * 0.25, duration * 0.5, duration * 0.75]
        buildup_pattern = self.choreographer.patterns["buildup"]

        for burst_start in burst_times:
            if burst_start < duration - 10:
                # Quick buildup burst (3 seconds)
                for step_idx in range(min(8, len(buildup_pattern.positions))):  # First 8 steps
                    step_time = burst_start + (step_idx * 0.375)  # 375ms per step

                    scene_path = f"generated_scenes_advanced/advanced_moving_heads/buildup/step_{step_idx:02d}.scex"

                    event = DMXEvent(
                        timeline_index=4,  # Secondary moving heads timeline
                        start_time=self._format_time(step_time),
                        path=scene_path,
                        length="0:00:00.3",  # Fast changes
                        speed=150,  # Very fast
                        speed_type=SpeedType.PERCENTAGE,
                        fade_in=50,
                        fade_out=50,
                    )

                    events.append(event)

        return events

    def _create_accent_effects(self, analysis: dict) -> list[DMXEvent]:
        """Create accent effects for special moments"""
        events = []
        duration = analysis.get("duration", 240)
        energy = analysis.get("energy_mean", 0.5)

        # UV effects during high energy moments
        if energy > 0.6:
            uv_times = [duration * 0.3, duration * 0.7]
            for uv_time in uv_times:
                if uv_time < duration - 20:
                    events.append(DMXEvent(
                        timeline_index=7,  # UV timeline
                        start_time=self._format_time(uv_time),
                        path="generated_scenes_systematic/individual/uv_light_40/white_cool_strobe_fast.scex",
                        length="0:00:05.0",
                        speed=200,
                        speed_type=SpeedType.PERCENTAGE,
                        fade_in=100,
                        fade_out=500,
                    ))

        return events

    def _format_time(self, seconds: float) -> str:
        """Format time to H:MM:SS.f"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)
        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def _format_duration(self, seconds: float) -> str:
        """Format duration to H:MM:SS.f"""
        return self._format_time(seconds)

    def _time_to_seconds(self, time_str: str) -> float:
        """Convert time string to seconds"""
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        sec_parts = parts[2].split(".")
        seconds = int(sec_parts[0])
        decimal = int(sec_parts[1]) / 10.0 if len(sec_parts) > 1 else 0.0
        return hours * 3600 + minutes * 60 + seconds + decimal

    def _save_timeline(self, timeline: DMXTimeline, output_path: Path) -> None:
        """Save timeline to file"""
        content = timeline.to_tml_format()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Timeline saved to: {output_path}")

def main():
    """Generate moving heads spectacular show"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate spectacular moving heads choreography")
    parser.add_argument("audio_file", type=Path, help="Audio file to analyze")
    parser.add_argument("-o", "--output", type=Path, help="Output timeline file")

    args = parser.parse_args()

    if not args.output:
        args.output = args.audio_file.stem + "_moving_heads_spectacular.tml"

    generator = MovingHeadsSpectacularGenerator()
    timeline = generator.generate_choreography_timeline(args.audio_file, args.output)

    print(f"✨ Generated spectacular moving heads show: {args.output}")
    print(f"🎵 Total events: {len(timeline.events)}")

if __name__ == "__main__":
    main()
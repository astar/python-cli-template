#!/usr/bin/env python3
"""
Advanced Moving Heads Choreographer
Creates sophisticated moving head patterns based on music analysis
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import math
import json
from pathlib import Path

@dataclass
class MovingHeadPosition:
    """Position definition for moving head"""
    pan: int          # 0-255 horizontal position
    upan: int         # 0-255 fine horizontal
    tilt: int         # 0-255 vertical position
    utilt: int        # 0-255 fine vertical
    color: int        # 0-255 color wheel
    gobo: int         # 0-255 gobo wheel
    dimmer: int       # 0-255 brightness
    shutter: int      # 0-255 strobe/open
    focus: int        # 0-255 focus
    prism: int        # 0-255 prism effects

@dataclass
class ChoreographyPattern:
    """Movement pattern for choreography"""
    name: str
    description: str
    positions: List[MovingHeadPosition]
    duration_ms: int
    loop: bool = True

class MovingHeadsChoreographer:
    """Creates advanced choreography for moving heads based on music analysis"""

    def __init__(self):
        self.patterns = {}
        self.color_schemes = {}
        self.movement_templates = {}
        self._define_patterns()
        self._define_color_schemes()

    def _define_patterns(self):
        """Define choreography patterns for different music sections"""

        # INTRO PATTERN - Mysterious building
        intro_positions = []
        for i in range(8):  # 8 steps, each 500ms
            angle = (i / 8) * 2 * math.pi
            pan = int(128 + 60 * math.cos(angle))      # Circular motion
            tilt = int(128 + 30 * math.sin(angle))     # Gentle vertical sway

            intro_positions.append(MovingHeadPosition(
                pan=pan, upan=0, tilt=tilt, utilt=0,
                color=11,  # Red start
                gobo=0, dimmer=180, shutter=32, focus=128, prism=0
            ))

        self.patterns["intro"] = ChoreographyPattern(
            name="intro",
            description="Mysterious circular building movement",
            positions=intro_positions,
            duration_ms=4000,
            loop=True
        )

        # VERSE PATTERN - Gentle sweep
        verse_positions = []
        for i in range(6):  # 6 steps, each 800ms
            progress = i / 5  # 0.0 to 1.0
            pan = int(64 + progress * 128)  # Left to right sweep
            tilt = int(128 + 20 * math.sin(progress * math.pi))  # Gentle arc

            verse_positions.append(MovingHeadPosition(
                pan=pan, upan=0, tilt=tilt, utilt=0,
                color=51,  # Blue
                gobo=0, dimmer=220, shutter=32, focus=128, prism=0
            ))

        self.patterns["verse"] = ChoreographyPattern(
            name="verse",
            description="Gentle left-to-right sweep with arc",
            positions=verse_positions,
            duration_ms=4800,
            loop=True
        )

        # CHORUS PATTERN - Energetic zigzag
        chorus_positions = []
        for i in range(12):  # 12 fast steps, each 250ms
            # Zigzag pattern
            if i % 4 < 2:
                pan = 64 if i % 2 == 0 else 192
                tilt = 96 if i % 2 == 0 else 160
            else:
                pan = 192 if i % 2 == 0 else 64
                tilt = 160 if i % 2 == 0 else 96

            # Alternate colors for energy
            color = 11 if i % 2 == 0 else 91  # Red/Blue alternating

            chorus_positions.append(MovingHeadPosition(
                pan=pan, upan=0, tilt=tilt, utilt=0,
                color=color,
                gobo=0, dimmer=255, shutter=32, focus=128, prism=0
            ))

        self.patterns["chorus"] = ChoreographyPattern(
            name="chorus",
            description="Fast energetic zigzag with color changes",
            positions=chorus_positions,
            duration_ms=3000,
            loop=True
        )

        # BREAKDOWN PATTERN - Spotlight convergence
        breakdown_positions = []
        for i in range(4):  # 4 steps focusing to center
            progress = (i + 1) / 4  # 0.25 to 1.0
            # All heads converge to center of dance floor
            pan = int(128 + (128 - 128) * progress)  # Move toward center
            tilt = int(64 + (128 - 64) * progress)   # Tilt down toward floor
            dimmer = int(100 + 155 * progress)       # Build intensity

            breakdown_positions.append(MovingHeadPosition(
                pan=pan, upan=0, tilt=tilt, utilt=0,
                color=0,   # White spotlight
                gobo=16,   # Add gobo for texture
                dimmer=dimmer, shutter=32, focus=200, prism=0
            ))

        self.patterns["breakdown"] = ChoreographyPattern(
            name="breakdown",
            description="Converging spotlight effect with gobo",
            positions=breakdown_positions,
            duration_ms=2000,
            loop=False
        )

        # BUILDUP PATTERN - Spinning energy
        buildup_positions = []
        for i in range(16):  # 16 fast steps, 150ms each
            angle = (i / 16) * 4 * math.pi  # 2 full rotations
            pan = int(128 + 80 * math.cos(angle))
            tilt = int(128 + 40 * math.sin(angle * 2))  # Double frequency vertical

            # Cycle through colors rapidly
            color_cycle = [11, 51, 91, 131, 171, 211]  # Red, Blue, Green, Yellow, Magenta, Cyan
            color = color_cycle[i % len(color_cycle)]

            buildup_positions.append(MovingHeadPosition(
                pan=pan, upan=0, tilt=tilt, utilt=0,
                color=color,
                gobo=0, dimmer=255, shutter=32, focus=128, prism=64
            ))

        self.patterns["buildup"] = ChoreographyPattern(
            name="buildup",
            description="Fast spinning with rapid color changes",
            positions=buildup_positions,
            duration_ms=2400,
            loop=True
        )

    def _define_color_schemes(self):
        """Define color schemes for different moods"""

        self.color_schemes = {
            "warm_intimate": {
                "colors": [11, 31, 71],  # Red, Orange, Yellow
                "description": "Warm intimate atmosphere"
            },
            "cool_mysterious": {
                "colors": [51, 91, 131],  # Blue, Green, Cyan
                "description": "Cool mysterious atmosphere"
            },
            "high_energy": {
                "colors": [11, 91, 171, 211],  # Red, Green, Magenta, White
                "description": "High energy party colors"
            },
            "romantic": {
                "colors": [11, 171, 71],  # Red, Magenta, Yellow
                "description": "Romantic warm colors"
            },
            "ethereal": {
                "colors": [131, 151, 211],  # Cyan, Blue, White
                "description": "Ethereal dreamy colors"
            }
        }

    def create_music_reactive_choreography(self, music_analysis: Dict) -> List[ChoreographyPattern]:
        """Create choreography based on music analysis"""

        choreography = []

        # Analyze music structure
        bpm = music_analysis.get("bpm", 120)
        energy = music_analysis.get("energy", 0.5)
        valence = music_analysis.get("valence", 0.5)

        # Choose patterns based on analysis
        if energy < 0.3:
            base_pattern = "intro"
            color_scheme = "cool_mysterious" if valence < 0.5 else "romantic"
        elif energy < 0.6:
            base_pattern = "verse"
            color_scheme = "warm_intimate" if valence > 0.6 else "cool_mysterious"
        elif energy < 0.8:
            base_pattern = "chorus"
            color_scheme = "high_energy"
        else:
            base_pattern = "buildup"
            color_scheme = "high_energy"

        # Adapt timing to BPM
        pattern = self.patterns[base_pattern]
        adapted_pattern = self._adapt_to_bpm(pattern, bpm)

        # Apply color scheme
        final_pattern = self._apply_color_scheme(adapted_pattern, color_scheme)

        choreography.append(final_pattern)
        return choreography

    def _adapt_to_bpm(self, pattern: ChoreographyPattern, bpm: float) -> ChoreographyPattern:
        """Adapt pattern timing to match BPM"""

        # Calculate beat duration in ms
        beat_duration_ms = (60.0 / bpm) * 1000

        # Adapt pattern duration to musical timing
        beats_per_pattern = round(pattern.duration_ms / beat_duration_ms)
        new_duration = int(beats_per_pattern * beat_duration_ms)

        # Adjust step timing proportionally
        step_duration = new_duration // len(pattern.positions)

        return ChoreographyPattern(
            name=f"{pattern.name}_bpm{int(bpm)}",
            description=f"{pattern.description} (adapted to {bpm} BPM)",
            positions=pattern.positions,
            duration_ms=new_duration,
            loop=pattern.loop
        )

    def _apply_color_scheme(self, pattern: ChoreographyPattern, scheme_name: str) -> ChoreographyPattern:
        """Apply color scheme to pattern"""

        scheme = self.color_schemes[scheme_name]
        colors = scheme["colors"]

        new_positions = []
        for i, pos in enumerate(pattern.positions):
            # Cycle through color scheme
            new_color = colors[i % len(colors)]

            new_pos = MovingHeadPosition(
                pan=pos.pan, upan=pos.upan,
                tilt=pos.tilt, utilt=pos.utilt,
                color=new_color,  # Apply new color
                gobo=pos.gobo, dimmer=pos.dimmer,
                shutter=pos.shutter, focus=pos.focus, prism=pos.prism
            )
            new_positions.append(new_pos)

        return ChoreographyPattern(
            name=f"{pattern.name}_{scheme_name}",
            description=f"{pattern.description} with {scheme['description']}",
            positions=new_positions,
            duration_ms=pattern.duration_ms,
            loop=pattern.loop
        )

    def generate_advanced_scenes(self, output_dir: Path):
        """Generate advanced moving head scene files"""

        output_dir = Path(output_dir) / "advanced_moving_heads"
        output_dir.mkdir(parents=True, exist_ok=True)

        scene_count = 0

        for pattern_name, pattern in self.patterns.items():
            pattern_dir = output_dir / pattern_name
            pattern_dir.mkdir(exist_ok=True)

            # Generate scene for each position in pattern
            for i, position in enumerate(pattern.positions):
                scene_content = self._create_advanced_scene_xml(position, pattern_name, i)

                scene_file = pattern_dir / f"step_{i:02d}.scex"
                with open(scene_file, "w", encoding="utf-8") as f:
                    f.write(scene_content)

                scene_count += 1

        # Generate color scheme variations
        for scheme_name, scheme in self.color_schemes.items():
            scheme_dir = output_dir / f"color_schemes" / scheme_name
            scheme_dir.mkdir(parents=True, exist_ok=True)

            for pattern_name, pattern in self.patterns.items():
                styled_pattern = self._apply_color_scheme(pattern, scheme_name)

                for i, position in enumerate(styled_pattern.positions):
                    scene_content = self._create_advanced_scene_xml(position, styled_pattern.name, i)

                    scene_file = scheme_dir / f"{pattern_name}_step_{i:02d}.scex"
                    with open(scene_file, "w", encoding="utf-8") as f:
                        f.write(scene_content)

                    scene_count += 1

        print(f"✨ Generated {scene_count} advanced moving head scenes!")
        print(f"   Patterns: {len(self.patterns)}")
        print(f"   Color schemes: {len(self.color_schemes)}")
        print(f"   Output: {output_dir}")

    def _create_advanced_scene_xml(self, position: MovingHeadPosition, pattern_name: str, step: int) -> str:
        """Create XML scene content for advanced moving head position"""

        return f'''<?xml version="1.0" encoding="UTF-8"?>

<Scene>
  <Fixtures>
    <Fixture id="1753953037" name="Moving Head #1" model="Intimidator Spot 375Z IRC (15CH)" />
    <Fixture id="1753953038" name="Moving Head #2" model="Intimidator Spot 375Z IRC (15CH)" />
    <Fixture id="1753953039" name="Moving Head #3" model="Intimidator Spot 375Z IRC (15CH)" />
    <Fixture id="1753953040" name="Moving Head #4" model="Intimidator Spot 375Z IRC (15CH)" />
    <Fixture id="1753953041" name="Moving Head #5" model="Intimidator Spot 375Z IRC (15CH)" />
  </Fixtures>
  <Steps>
    <Step length="100">
      <Fixture id="1753953037">
        <Channel index="0" name="pan" value="{position.pan}" />
        <Channel index="1" name="upan" value="{position.upan}" />
        <Channel index="2" name="tilt" value="{position.tilt}" />
        <Channel index="3" name="utilt" value="{position.utilt}" />
        <Channel index="4" name="color" value="{position.color}" />
        <Channel index="5" name="gobo" value="{position.gobo}" />
        <Channel index="6" name="prism" value="{position.prism}" />
        <Channel index="7" name="focus" value="{position.focus}" />
        <Channel index="8" name="dimmer" value="{position.dimmer}" />
        <Channel index="9" name="shutter" value="{position.shutter}" />
      </Fixture>
      <Fixture id="1753953038">
        <Channel index="0" name="pan" value="{position.pan + 20}" />
        <Channel index="1" name="upan" value="{position.upan}" />
        <Channel index="2" name="tilt" value="{position.tilt}" />
        <Channel index="3" name="utilt" value="{position.utilt}" />
        <Channel index="4" name="color" value="{position.color}" />
        <Channel index="5" name="gobo" value="{position.gobo}" />
        <Channel index="6" name="prism" value="{position.prism}" />
        <Channel index="7" name="focus" value="{position.focus}" />
        <Channel index="8" name="dimmer" value="{position.dimmer}" />
        <Channel index="9" name="shutter" value="{position.shutter}" />
      </Fixture>
      <Fixture id="1753953039">
        <Channel index="0" name="pan" value="{position.pan - 20}" />
        <Channel index="1" name="upan" value="{position.upan}" />
        <Channel index="2" name="tilt" value="{position.tilt + 10}" />
        <Channel index="3" name="utilt" value="{position.utilt}" />
        <Channel index="4" name="color" value="{position.color}" />
        <Channel index="5" name="gobo" value="{position.gobo}" />
        <Channel index="6" name="prism" value="{position.prism}" />
        <Channel index="7" name="focus" value="{position.focus}" />
        <Channel index="8" name="dimmer" value="{position.dimmer}" />
        <Channel index="9" name="shutter" value="{position.shutter}" />
      </Fixture>
      <Fixture id="1753953040">
        <Channel index="0" name="pan" value="{position.pan + 40}" />
        <Channel index="1" name="upan" value="{position.upan}" />
        <Channel index="2" name="tilt" value="{position.tilt - 10}" />
        <Channel index="3" name="utilt" value="{position.utilt}" />
        <Channel index="4" name="color" value="{position.color}" />
        <Channel index="5" name="gobo" value="{position.gobo}" />
        <Channel index="6" name="prism" value="{position.prism}" />
        <Channel index="7" name="focus" value="{position.focus}" />
        <Channel index="8" name="dimmer" value="{position.dimmer}" />
        <Channel index="9" name="shutter" value="{position.shutter}" />
      </Fixture>
      <Fixture id="1753953041">
        <Channel index="0" name="pan" value="{position.pan - 40}" />
        <Channel index="1" name="upan" value="{position.upan}" />
        <Channel index="2" name="tilt" value="{position.tilt}" />
        <Channel index="3" name="utilt" value="{position.utilt}" />
        <Channel index="4" name="color" value="{position.color}" />
        <Channel index="5" name="gobo" value="{position.gobo}" />
        <Channel index="6" name="prism" value="{position.prism}" />
        <Channel index="7" name="focus" value="{position.focus}" />
        <Channel index="8" name="dimmer" value="{position.dimmer}" />
        <Channel index="9" name="shutter" value="{position.shutter}" />
      </Fixture>
    </Step>
  </Steps>
</Scene>'''

def main():
    """Generate advanced moving heads choreography"""
    choreographer = MovingHeadsChoreographer()
    choreographer.generate_advanced_scenes("generated_scenes_advanced")

    # Example music analysis integration
    example_music = {
        "bpm": 128,
        "energy": 0.8,
        "valence": 0.7
    }

    choreography = choreographer.create_music_reactive_choreography(example_music)
    print(f"\n🎵 Music-reactive choreography created:")
    for pattern in choreography:
        print(f"   - {pattern.name}: {pattern.description}")

if __name__ == "__main__":
    main()
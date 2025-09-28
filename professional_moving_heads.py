#!/usr/bin/env python3
"""
Professional Moving Heads Scene Generator
Based on analysis of hand_made_scenes - implements professional techniques
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple
import math

class ProfessionalMovingHeadsGenerator:
    """Generate professional moving head scenes based on hand_made_scenes analysis"""

    def __init__(self):
        # Professional channel mapping (from hand_made_scenes analysis)
        self.channel_map = {
            "pan": 0,           # 0-255 horizontal position
            "upan": 1,          # 0-255 fine pan (duplicates pan value)
            "tilt": 2,          # 0-255 vertical position
            "utilt": 3,         # 0-255 fine tilt (duplicates tilt value)
            "color": 5,         # 0-255 color wheel (channel 5, not 4!)
            "gobo": 6,          # 0-255 gobo pattern
            "gobo_rotate": 7,   # 0-255 gobo rotation (160 = rotate)
            "dimmer": 10,       # 0-255 brightness (channel 10, not 8!)
            "shutter": 11,      # 0-255 strobe/shutter (channel 11, not 9!)
            "zoom": 14,         # 0-255 zoom level
        }

        # Professional safe oven positions (from hand_made_scenes analysis)
        # TILT 73-81 ensures lights don't shine into people's eyes
        self.oven_positions = [
            {"name": "MH_1", "pan": 137, "upan": 137, "tilt": 79, "utilt": 79},
            {"name": "MH_2", "pan": 144, "upan": 144, "tilt": 73, "utilt": 73},
            {"name": "MH_3", "pan": 126, "upan": 127, "tilt": 74, "utilt": 75},
            {"name": "MH_4", "pan": 109, "upan": 109, "tilt": 75, "utilt": 75},
            {"name": "MH_5", "pan": 208, "upan": 203, "tilt": 176, "utilt": 176},  # Back wall
        ]

        # Color mapping (professional values from hand_made_scenes)
        self.colors = {
            "red": 11,
            "darkred": 12,
            "blue": 51,
            "darkblue": 52,
            "green": 91,
            "darkgreen": 92,
            "yellow": 131,
            "orange": 132,
            "purple": 171,
            "magenta": 172,
            "white": 211,
            "cyan": 212,
        }

    def generate_professional_scenes(self, output_dir: Path = None):
        """Generate all professional moving head scenes"""
        if output_dir is None:
            output_dir = Path("generated_scenes_advanced/professional_moving_heads")

        output_dir.mkdir(parents=True, exist_ok=True)
        scene_count = 0

        # 1. Generate single-color oven scenes (Jednobarevna kamna)
        scene_count += self._generate_oven_scenes(output_dir)

        # 2. Generate gobo rotation scenes (Rotate gobo na kamnech)
        scene_count += self._generate_gobo_rotation_scenes(output_dir)

        # 3. Generate zoom + rotation scenes (Rotate gobo zoom in and out)
        scene_count += self._generate_zoom_rotation_scenes(output_dir)

        # 4. Generate snake effects for other fixtures
        scene_count += self._generate_snake_effects(output_dir)

        print(f"✨ Generated {scene_count} professional moving head scenes!")
        print(f"   Output: {output_dir}")

        return scene_count

    def _generate_oven_scenes(self, output_dir: Path) -> int:
        """Generate single-color oven-focused scenes"""
        oven_dir = output_dir / "oven_single_color"
        oven_dir.mkdir(exist_ok=True)

        scene_count = 0
        for color_name, color_value in self.colors.items():
            scene_content = self._create_oven_scene_xml(color_name, color_value)

            scene_file = oven_dir / f"MH_all_{color_name}_oven.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)
            scene_count += 1

        print(f"   Generated {scene_count} single-color oven scenes")
        return scene_count

    def _generate_gobo_rotation_scenes(self, output_dir: Path) -> int:
        """Generate gobo rotation scenes"""
        gobo_dir = output_dir / "gobo_rotation"
        gobo_dir.mkdir(exist_ok=True)

        scene_count = 0
        for color_name, color_value in self.colors.items():
            scene_content = self._create_gobo_rotation_xml(color_name, color_value)

            scene_file = gobo_dir / f"Rotate_gobo_{color_name}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)
            scene_count += 1

        print(f"   Generated {scene_count} gobo rotation scenes")
        return scene_count

    def _generate_zoom_rotation_scenes(self, output_dir: Path) -> int:
        """Generate complex zoom + gobo rotation scenes"""
        zoom_dir = output_dir / "zoom_rotation"
        zoom_dir.mkdir(exist_ok=True)

        scene_count = 0
        for color_name, color_value in self.colors.items():
            scene_content = self._create_zoom_rotation_xml(color_name, color_value)

            scene_file = zoom_dir / f"Zoom_{color_name}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)
            scene_count += 1

        print(f"   Generated {scene_count} zoom + rotation scenes")
        return scene_count

    def _generate_snake_effects(self, output_dir: Path) -> int:
        """Generate sequential snake-like effects"""
        snake_dir = output_dir / "snake_effects"
        snake_dir.mkdir(exist_ok=True)

        scene_count = 0
        for color_name, color_value in self.colors.items():
            # Left to right snake
            scene_content = self._create_snake_xml(color_name, color_value, direction="left_right")
            scene_file = snake_dir / f"MH_snake_{color_name}_left_right.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)
            scene_count += 1

            # Right to left snake
            scene_content = self._create_snake_xml(color_name, color_value, direction="right_left")
            scene_file = snake_dir / f"MH_snake_{color_name}_right_left.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)
            scene_count += 1

        print(f"   Generated {scene_count} snake effect scenes")
        return scene_count

    def _create_oven_scene_xml(self, color_name: str, color_value: int) -> str:
        """Create single-color oven scene with professional 3-step structure"""

        fixtures = [
            {"id": "1753951490", "name": "Intimidator Spot 375Z IRC (15CH)"},
            {"id": "1753953036", "name": "Intimidator Spot 375Z IRC (15CH) #2"},
            {"id": "1753953037", "name": "Intimidator Spot 375Z IRC (15CH) #3"},
            {"id": "1753953038", "name": "Intimidator Spot 375Z IRC (15CH) #4"},
            {"id": "1753953039", "name": "Intimidator Spot 375Z IRC (15CH) #5"},
        ]

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n\n<Scene>\n  <Fixtures>\n'

        # Add fixtures
        for fixture in fixtures:
            xml_content += f'    <Fixture id="{fixture["id"]}" name="{fixture["name"]}" model="Intimidator Spot 375Z IRC (15CH)"/>\n'

        xml_content += '  </Fixtures>\n  <Steps>\n'

        # Step 1: Setup/blackout (200ms)
        xml_content += '    <Step length="100">\n'
        for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
            xml_content += f'      <Fixture id="{fixture["id"]}">\n'
            xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
            xml_content += f'        <Channel index="1" name="upan" value="0"/>\n'
            xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
            xml_content += f'        <Channel index="3" name="utilt" value="0"/>\n'
            xml_content += f'        <Channel index="5" name="color" value="{color_value + 1}"/>\n'  # Setup color
            if i == 4:  # Fixture #5 needs gobo_rotate
                xml_content += f'        <Channel index="7" name="gobo_rotate" value="0"/>\n'
            xml_content += f'        <Channel index="10" name="dimmer" value="0"/>\n'
            xml_content += f'        <Channel index="11" name="shutter" value="1"/>\n'
            xml_content += '      </Fixture>\n'
        xml_content += '    </Step>\n'

        # Step 2: Fade-in (100ms with fade attributes)
        xml_content += '    <Step length="100">\n'
        for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
            xml_content += f'      <Fixture id="{fixture["id"]}">\n'
            xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
            xml_content += f'        <Channel index="1" name="upan" value="{pos["upan"]}"/>\n'
            xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
            xml_content += f'        <Channel index="3" name="utilt" value="{pos["utilt"]}"/>\n'
            xml_content += f'        <Channel index="5" name="color" value="{color_value}" fade="1"/>\n'
            if i == 4:  # Fixture #5
                xml_content += f'        <Channel index="7" name="gobo_rotate" value="0"/>\n'
            xml_content += f'        <Channel index="10" name="dimmer" value="60" fade="1"/>\n'
            xml_content += f'        <Channel index="11" name="shutter" value="4" fade="1"/>\n'
            xml_content += '      </Fixture>\n'
        xml_content += '    </Step>\n'

        # Step 3: Main effect (15000ms sustained)
        xml_content += '    <Step length="15000">\n'
        for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
            xml_content += f'      <Fixture id="{fixture["id"]}">\n'
            xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
            xml_content += f'        <Channel index="1" name="upan" value="{pos["upan"]}"/>\n'
            xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
            xml_content += f'        <Channel index="3" name="utilt" value="{pos["utilt"]}"/>\n'
            xml_content += f'        <Channel index="5" name="color" value="{color_value}"/>\n'
            if i == 4:  # Fixture #5
                xml_content += f'        <Channel index="7" name="gobo_rotate" value="0"/>\n'
            xml_content += f'        <Channel index="10" name="dimmer" value="60"/>\n'
            xml_content += f'        <Channel index="11" name="shutter" value="4"/>\n'
            xml_content += '      </Fixture>\n'
        xml_content += '    </Step>\n'

        xml_content += '  </Steps>\n</Scene>\n'
        return xml_content

    def _create_gobo_rotation_xml(self, color_name: str, color_value: int) -> str:
        """Create gobo rotation scene"""

        fixtures = [
            {"id": "1753951490", "name": "Intimidator Spot 375Z IRC (15CH)"},
            {"id": "1753953036", "name": "Intimidator Spot 375Z IRC (15CH) #2"},
            {"id": "1753953037", "name": "Intimidator Spot 375Z IRC (15CH) #3"},
            {"id": "1753953038", "name": "Intimidator Spot 375Z IRC (15CH) #4"},
            {"id": "1753953039", "name": "Intimidator Spot 375Z IRC (15CH) #5"},
        ]

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n\n<Scene>\n  <Fixtures>\n'

        # Add fixtures
        for fixture in fixtures:
            xml_content += f'    <Fixture id="{fixture["id"]}" name="{fixture["name"]}" model="Intimidator Spot 375Z IRC (15CH)"/>\n'

        xml_content += '  </Fixtures>\n  <Steps>\n'

        # Step 1: Setup/blackout (200ms)
        xml_content += '    <Step length="200">\n'
        for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
            xml_content += f'      <Fixture id="{fixture["id"]}">\n'
            xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
            xml_content += f'        <Channel index="1" name="upan" value="{pos["upan"]}"/>\n'
            xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
            xml_content += f'        <Channel index="3" name="utilt" value="{pos["utilt"]}"/>\n'
            xml_content += f'        <Channel index="5" name="color" value="{color_value}"/>\n'
            xml_content += f'        <Channel index="6" name="gobo" value="59"/>\n'  # Gobo pattern
            xml_content += f'        <Channel index="7" name="gobo_rotate" value="160"/>\n'  # Rotating
            xml_content += f'        <Channel index="10" name="dimmer" value="0"/>\n'
            xml_content += f'        <Channel index="11" name="shutter" value="0"/>\n'
            xml_content += f'        <Channel index="14" name="zoom" value="0"/>\n'
            xml_content += '      </Fixture>\n'
        xml_content += '    </Step>\n'

        # Step 2: Main rotating effect (15000ms)
        xml_content += '    <Step length="15000">\n'
        for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
            xml_content += f'      <Fixture id="{fixture["id"]}">\n'
            xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
            xml_content += f'        <Channel index="1" name="upan" value="{pos["upan"]}"/>\n'
            xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
            xml_content += f'        <Channel index="3" name="utilt" value="{pos["utilt"]}"/>\n'
            xml_content += f'        <Channel index="5" name="color" value="{color_value}"/>\n'
            xml_content += f'        <Channel index="6" name="gobo" value="59"/>\n'
            xml_content += f'        <Channel index="7" name="gobo_rotate" value="160"/>\n'  # Continuous rotation
            xml_content += f'        <Channel index="10" name="dimmer" value="60"/>\n'
            xml_content += f'        <Channel index="11" name="shutter" value="4"/>\n'
            xml_content += f'        <Channel index="14" name="zoom" value="0"/>\n'
            xml_content += '      </Fixture>\n'
        xml_content += '    </Step>\n'

        xml_content += '  </Steps>\n</Scene>\n'
        return xml_content

    def _create_zoom_rotation_xml(self, color_name: str, color_value: int) -> str:
        """Create complex zoom + gobo rotation scene with 11+ steps"""

        fixtures = [
            {"id": "1753951490", "name": "Intimidator Spot 375Z IRC (15CH)"},
            {"id": "1753953036", "name": "Intimidator Spot 375Z IRC (15CH) #2"},
            {"id": "1753953037", "name": "Intimidator Spot 375Z IRC (15CH) #3"},
            {"id": "1753953038", "name": "Intimidator Spot 375Z IRC (15CH) #4"},
            {"id": "1753953039", "name": "Intimidator Spot 375Z IRC (15CH) #5"},
        ]

        # Zoom breathing pattern (0→192→0) with 11 steps
        zoom_pattern = [0, 38, 76, 115, 153, 192, 153, 115, 76, 38, 0]

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n\n<Scene>\n  <Fixtures>\n'

        # Add fixtures
        for fixture in fixtures:
            xml_content += f'    <Fixture id="{fixture["id"]}" name="{fixture["name"]}" model="Intimidator Spot 375Z IRC (15CH)"/>\n'

        xml_content += '  </Fixtures>\n  <Steps>\n'

        # Generate 11 steps with zoom breathing effect
        for step_idx, zoom_value in enumerate(zoom_pattern):
            xml_content += '    <Step length="500">\n'  # 500ms per step like hand_made_scenes

            for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
                xml_content += f'      <Fixture id="{fixture["id"]}">\n'
                xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
                xml_content += f'        <Channel index="1" name="upan" value="{pos["upan"]}"/>\n'
                xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
                xml_content += f'        <Channel index="3" name="utilt" value="{pos["utilt"]}"/>\n'
                xml_content += f'        <Channel index="5" name="color" value="{color_value}"/>\n'
                xml_content += f'        <Channel index="6" name="gobo" value="59"/>\n'
                xml_content += f'        <Channel index="7" name="gobo_rotate" value="160"/>\n'  # Continuous rotation
                xml_content += f'        <Channel index="10" name="dimmer" value="60"/>\n'
                xml_content += f'        <Channel index="11" name="shutter" value="4"/>\n'
                xml_content += f'        <Channel index="14" name="zoom" value="{zoom_value}"/>\n'  # Breathing zoom
                xml_content += '      </Fixture>\n'

            xml_content += '    </Step>\n'

        xml_content += '  </Steps>\n</Scene>\n'
        return xml_content

    def _create_snake_xml(self, color_name: str, color_value: int, direction: str = "left_right") -> str:
        """Create snake effect moving across moving heads"""

        fixtures = [
            {"id": "1753951490", "name": "Intimidator Spot 375Z IRC (15CH)"},
            {"id": "1753953036", "name": "Intimidator Spot 375Z IRC (15CH) #2"},
            {"id": "1753953037", "name": "Intimidator Spot 375Z IRC (15CH) #3"},
            {"id": "1753953038", "name": "Intimidator Spot 375Z IRC (15CH) #4"},
            {"id": "1753953039", "name": "Intimidator Spot 375Z IRC (15CH) #5"},
        ]

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n\n<Scene>\n  <Fixtures>\n'

        # Add fixtures
        for fixture in fixtures:
            xml_content += f'    <Fixture id="{fixture["id"]}" name="{fixture["name"]}" model="Intimidator Spot 375Z IRC (15CH)"/>\n'

        xml_content += '  </Fixtures>\n  <Steps>\n'

        # Create 5 steps - one for each fixture activation
        fixture_order = list(range(5))
        if direction == "right_left":
            fixture_order.reverse()

        for active_fixture in fixture_order:
            xml_content += '    <Step length="500">\n'  # 500ms per step

            for i, (fixture, pos) in enumerate(zip(fixtures, self.oven_positions)):
                xml_content += f'      <Fixture id="{fixture["id"]}">\n'
                xml_content += f'        <Channel index="0" name="pan" value="{pos["pan"]}"/>\n'
                xml_content += f'        <Channel index="1" name="upan" value="{pos["upan"]}"/>\n'
                xml_content += f'        <Channel index="2" name="tilt" value="{pos["tilt"]}"/>\n'
                xml_content += f'        <Channel index="3" name="utilt" value="{pos["utilt"]}"/>\n'
                xml_content += f'        <Channel index="5" name="color" value="{color_value}"/>\n'

                # Only the active fixture is lit
                if i == active_fixture:
                    xml_content += f'        <Channel index="10" name="dimmer" value="255"/>\n'  # Full brightness
                    xml_content += f'        <Channel index="11" name="shutter" value="4"/>\n'   # Open
                else:
                    xml_content += f'        <Channel index="10" name="dimmer" value="0"/>\n'    # Dark
                    xml_content += f'        <Channel index="11" name="shutter" value="1"/>\n'   # Closed

                xml_content += '      </Fixture>\n'

            xml_content += '    </Step>\n'

        xml_content += '  </Steps>\n</Scene>\n'
        return xml_content


def main():
    """Generate professional moving head scenes"""
    generator = ProfessionalMovingHeadsGenerator()
    scene_count = generator.generate_professional_scenes()

    print(f"\n🎭 Professional Moving Heads Generator Complete!")
    print(f"   Based on hand_made_scenes analysis")
    print(f"   Safe oven positioning (TILT 73-81°)")
    print(f"   Professional channel mapping")
    print(f"   Multi-step animations with proper timing")
    print(f"   Gobo rotation and zoom effects")
    print(f"   Snake patterns for dynamic sequences")


if __name__ == "__main__":
    main()
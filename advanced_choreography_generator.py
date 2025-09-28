#!/usr/bin/env python3
"""
Advanced Moving Heads Choreography Generator
Generuje pokročilé choreografie pro moving heads s různými vzory pohybu
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json
import math
from typing import Dict, List, Tuple

class AdvancedChoreographyGenerator:
    """Generátor pokročilých choreografií"""

    def __init__(self):
        self.output_dir = Path("generated_scenes_advanced")
        self.choreography_dir = self.output_dir / "choreography"
        self.choreography_dir.mkdir(parents=True, exist_ok=True)

        # Moving heads IDs z maximus konfigurace
        self.moving_head_ids = {
            "moving_head_1": "1753951490",  # Intimidator Spot 375Z IRC (15CH)
            "moving_head_2": "1753953036",  # Intimidator Spot 375Z IRC (15CH) #2
            "moving_head_3": "1753953037",  # Intimidator Spot 375Z IRC (15CH) #3
            "moving_head_4": "1753953038",  # Intimidator Spot 375Z IRC (15CH) #4
            "moving_head_5": "1753953039",  # Intimidator Spot 375Z IRC (15CH) #5
        }

        # Barevný wheel Intimidator Spot 375Z
        self.color_wheel = {
            "white": 0,
            "red": 11,
            "orange": 31,
            "blue": 51,
            "yellow": 71,
            "green": 91,
            "purple": 111,
            "cyan": 131,
            "magenta": 171,
            "warm_white": 211
        }

    def create_choreography_sequence(self, name: str, description: str,
                                   movement_data: Dict, colors: List[str],
                                   duration: int = 10000) -> str:
        """Vytvoří choreografickou sekvenci"""

        # XML struktura
        root = ET.Element("Scene")

        # Fixtures sekce
        fixtures = ET.SubElement(root, "Fixtures")
        for head_name, head_id in self.moving_head_ids.items():
            fixture = ET.SubElement(fixtures, "Fixture")
            fixture.set("id", head_id)
            fixture.set("name", head_name.replace("_", " ").title())
            fixture.set("model", "Intimidator Spot 375Z IRC (15CH)")

        # Steps sekce s pohybovou sekvencí
        steps = ET.SubElement(root, "Steps")

        # Počet kroků v sekvenci
        num_steps = len(movement_data.get("pan_sequence", [128]))
        step_duration = duration // num_steps

        for step_idx in range(num_steps):
            step = ET.SubElement(steps, "Step")
            step.set("length", str(step_duration))

            # Pro každý moving head
            for head_idx, (head_name, head_id) in enumerate(self.moving_head_ids.items()):
                fixture_elem = ET.SubElement(step, "Fixture")
                fixture_elem.set("id", head_id)

                # Pan pozice (s posunem pro každý head)
                base_pan = movement_data["pan_sequence"][step_idx % len(movement_data["pan_sequence"])]
                pan_offset = head_idx * movement_data.get("pan_offset", 0)
                final_pan = (base_pan + pan_offset) % 256

                # Tilt pozice
                base_tilt = movement_data["tilt_sequence"][step_idx % len(movement_data["tilt_sequence"])]
                tilt_offset = head_idx * movement_data.get("tilt_offset", 0)
                final_tilt = max(0, min(255, base_tilt + tilt_offset))

                # Barva (cykluje mezi barvami)
                color_name = colors[head_idx % len(colors)]
                color_value = self.color_wheel.get(color_name, 0)

                # DMX channels
                channels = [
                    ("pan", final_pan),
                    ("tilt", final_tilt),
                    ("color", color_value),
                    ("dimmer", 255),
                    ("shutter", 32),  # Open
                    ("gobo", movement_data.get("gobo", 0)),
                    ("prism", movement_data.get("prism", 0)),
                    ("focus", movement_data.get("focus", 128)),
                ]

                for channel_name, value in channels:
                    channel = ET.SubElement(fixture_elem, "Channel")
                    channel.set("name", channel_name)
                    channel.set("value", str(value))

        # Ulož soubor
        filename = f"{name.lower().replace(' ', '_')}.scex"
        filepath = self.choreography_dir / filename

        # Formátování XML
        self._indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(str(filepath), encoding="UTF-8", xml_declaration=True)

        print(f"   ✅ Created: {filename}")
        return str(filepath)

    def generate_all_choreographies(self):
        """Generuje všechny choreografie"""
        print("🕺 Generating Advanced Moving Heads Choreographies...")

        choreographies = [
            # 1. ROMANTIC SLOW SWEEP
            {
                "name": "Romantic Slow Sweep",
                "description": "Pomalé romantické kývání pro lyrické části",
                "movement": {
                    "pan_sequence": [64, 80, 96, 112, 128, 144, 160, 176, 192, 176, 160, 144, 128, 112, 96, 80],
                    "tilt_sequence": [120, 124, 128, 132, 136, 132, 128, 124, 120, 116, 112, 116, 120, 124, 128, 132],
                    "pan_offset": 10,  # Každý head o trochu posunut
                    "tilt_offset": 5,
                    "gobo": 0,
                    "prism": 0,
                    "focus": 128
                },
                "colors": ["warm_white", "orange", "yellow", "red", "magenta"]
            },

            # 2. ENERGETIC FAST SWEEP
            {
                "name": "Energetic Fast Sweep",
                "description": "Rychlé energické kývání pro taneční části",
                "movement": {
                    "pan_sequence": [32, 64, 96, 128, 160, 192, 224, 192, 160, 128, 96, 64],
                    "tilt_sequence": [96, 112, 128, 144, 160, 144, 128, 112, 96, 112, 128, 144],
                    "pan_offset": 20,
                    "tilt_offset": 8,
                    "gobo": 0,
                    "prism": 0,
                    "focus": 180
                },
                "colors": ["white", "red", "blue", "green", "yellow"]
            },

            # 3. MYSTICAL CIRCLE
            {
                "name": "Mystical Circle",
                "description": "Kruhový pohyb pro tajemné atmosféry",
                "movement": {
                    "pan_sequence": [128, 145, 160, 175, 190, 205, 220, 235, 250, 235, 220, 205, 190, 175, 160, 145],
                    "tilt_sequence": [128, 140, 150, 158, 164, 158, 150, 140, 128, 116, 106, 98, 92, 98, 106, 116],
                    "pan_offset": 51,  # 360/5 = 72 degrees per head ≈ 51 DMX units
                    "tilt_offset": 0,
                    "gobo": 10,  # Používej gobo pattern
                    "prism": 0,
                    "focus": 100
                },
                "colors": ["purple", "blue", "cyan", "magenta", "white"]
            },

            # 4. DYNAMIC FIGURE-8
            {
                "name": "Dynamic Figure 8",
                "description": "Osmička pro dynamické buildupy",
                "movement": {
                    "pan_sequence": [64, 96, 128, 160, 192, 160, 128, 96, 64, 96, 128, 160, 192, 160, 128, 96],
                    "tilt_sequence": [112, 128, 144, 128, 112, 96, 112, 128, 144, 160, 144, 128, 112, 128, 144, 128],
                    "pan_offset": 15,
                    "tilt_offset": 10,
                    "gobo": 0,
                    "prism": 50,  # Prism effect
                    "focus": 200
                },
                "colors": ["red", "orange", "yellow", "green", "blue"]
            },

            # 5. SYNCHRONIZED POWER
            {
                "name": "Synchronized Power",
                "description": "Synchronní pohyb pro power momenty",
                "movement": {
                    "pan_sequence": [128, 192, 128, 64, 128, 192, 128, 64],
                    "tilt_sequence": [128, 160, 128, 96, 128, 160, 128, 96],
                    "pan_offset": 0,  # Všechny stejně
                    "tilt_offset": 0,
                    "gobo": 0,
                    "prism": 0,
                    "focus": 255
                },
                "colors": ["white", "white", "white", "white", "white"]  # Všechny bílé
            },

            # 6. COUNTER BALANCE
            {
                "name": "Counter Balance",
                "description": "Protisměrný pohyb pro vytvoření napětí",
                "movement": {
                    "pan_sequence": [64, 96, 128, 160, 192, 160, 128, 96],
                    "tilt_sequence": [96, 112, 128, 144, 160, 144, 128, 112],
                    "pan_offset": 128,  # Polovina heads opačně
                    "tilt_offset": 0,
                    "gobo": 0,
                    "prism": 0,
                    "focus": 150
                },
                "colors": ["red", "blue", "red", "blue", "red"]  # Střídavé barvy
            },

            # 7. SEQUENTIAL CHASE
            {
                "name": "Sequential Chase",
                "description": "Postupné následování pro buildup",
                "movement": {
                    "pan_sequence": [64, 80, 96, 112, 128, 144, 160, 176, 192],
                    "tilt_sequence": [112, 116, 120, 124, 128, 132, 136, 140, 144],
                    "pan_offset": 25,  # Velký offset pro chase efekt
                    "tilt_offset": 5,
                    "gobo": 0,
                    "prism": 0,
                    "focus": 128
                },
                "colors": ["red", "orange", "yellow", "green", "blue"]
            },

            # 8. RAINBOW EXPLOSION
            {
                "name": "Rainbow Explosion",
                "description": "Explozivní barevný efekt pro drop momenty",
                "movement": {
                    "pan_sequence": [128, 255, 0, 128, 255, 0, 128],
                    "tilt_sequence": [128, 200, 56, 128, 200, 56, 128],
                    "pan_offset": 40,
                    "tilt_offset": 20,
                    "gobo": 20,  # Výrazné gobo
                    "prism": 100,  # Plný prism
                    "focus": 255
                },
                "colors": ["red", "orange", "yellow", "green", "blue"]
            },

            # 9. AMBIENT STATIC
            {
                "name": "Ambient Static",
                "description": "Statické pozice pro ambient pozadí",
                "movement": {
                    "pan_sequence": [128],  # Statické
                    "tilt_sequence": [128],
                    "pan_offset": 30,  # Každý head jinak nasměrován
                    "tilt_offset": 15,
                    "gobo": 0,
                    "prism": 0,
                    "focus": 80
                },
                "colors": ["warm_white", "orange", "blue", "purple", "cyan"]
            },

            # 10. STROBO MADNESS
            {
                "name": "Strobo Madness",
                "description": "Intenzivní stroboskopický efekt",
                "movement": {
                    "pan_sequence": [64, 128, 192, 128, 64, 128, 192, 128],
                    "tilt_sequence": [96, 128, 160, 128, 96, 128, 160, 128],
                    "pan_offset": 50,
                    "tilt_offset": 25,
                    "gobo": 30,
                    "prism": 0,
                    "focus": 255
                },
                "colors": ["white", "red", "white", "blue", "white"]
            }
        ]

        created_files = []
        for choreo in choreographies:
            filepath = self.create_choreography_sequence(
                choreo["name"],
                choreo["description"],
                choreo["movement"],
                choreo["colors"]
            )
            created_files.append(filepath)

        # Vytvoř index soubor
        self._create_choreography_index(choreographies)

        print(f"✅ Generated {len(choreographies)} choreographies")
        return created_files

    def _create_choreography_index(self, choreographies: List[Dict]):
        """Vytvoří index choreografií"""
        index = {
            "choreographies": {},
            "usage_guide": {
                "romantic_moments": ["Romantic Slow Sweep", "Ambient Static"],
                "energetic_parts": ["Energetic Fast Sweep", "Rainbow Explosion"],
                "mysterious_atmospheres": ["Mystical Circle"],
                "buildup_moments": ["Sequential Chase", "Dynamic Figure 8"],
                "power_moments": ["Synchronized Power", "Strobo Madness"],
                "tension_creation": ["Counter Balance"]
            }
        }

        for choreo in choreographies:
            index["choreographies"][choreo["name"]] = {
                "description": choreo["description"],
                "file": f"{choreo['name'].lower().replace(' ', '_')}.scex",
                "colors": choreo["colors"],
                "recommended_for": self._get_recommendations(choreo["name"])
            }

        # Ulož index
        with open(self.choreography_dir / "choreography_index.json", "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def _get_recommendations(self, name: str) -> List[str]:
        """Vrátí doporučení kdy použít choreografii"""
        recommendations = {
            "Romantic Slow Sweep": ["lyrické části", "pomalé verše", "emocionální momenty"],
            "Energetic Fast Sweep": ["rychlé části", "taneční sekce", "vysoká energie"],
            "Mystical Circle": ["intro", "bridge", "tajemné atmosféry"],
            "Dynamic Figure 8": ["buildup", "před dropem", "rostoucí napětí"],
            "Synchronized Power": ["chorus", "drop", "peak momenty"],
            "Counter Balance": ["kontrasty", "napětí", "dramatické momenty"],
            "Sequential Chase": ["buildup", "crescendo", "postupné narůstání"],
            "Rainbow Explosion": ["drop", "explosion", "peak energy"],
            "Ambient Static": ["pozadí", "ambient", "klidné momenty"],
            "Strobo Madness": ["intenzivní momenty", "peak energy", "rave části"]
        }
        return recommendations.get(name, [])

    def _indent_xml(self, elem, level=0):
        """Formátuje XML pro čitelnost"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

def main():
    """Hlavní funkce"""
    print("🕺 Advanced Moving Heads Choreography Generator")
    print("=" * 50)

    generator = AdvancedChoreographyGenerator()
    created_files = generator.generate_all_choreographies()

    print()
    print("🎭 Choreography System Created!")
    print(f"   Files: {len(created_files)}")
    print(f"   Location: {generator.choreography_dir}")
    print()
    print("🎯 Usage Examples:")
    print("   - Romantic moments: romantic_slow_sweep.scex")
    print("   - Energy peaks: energetic_fast_sweep.scex")
    print("   - Buildup: sequential_chase.scex")
    print("   - Drop: rainbow_explosion.scex")
    print("   - Ambient: ambient_static.scex")

if __name__ == "__main__":
    main()
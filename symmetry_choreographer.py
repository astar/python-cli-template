#!/usr/bin/env python3
"""
Symmetry & Movement Choreographer
Systém založený na principech symetrie a asymetrie
- Přilehlé/protilehlé světla
- Moving heads pohyby tam a zpět
- Symetrické a asymetrické formace
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json
import math
import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum

class SymmetryPattern(Enum):
    """Vzory symetrie"""
    MIRROR_HORIZONTAL = "mirror_horizontal"     # Horizontální zrcadlení
    MIRROR_VERTICAL = "mirror_vertical"         # Vertikální zrcadlení
    POINT_SYMMETRY = "point_symmetry"          # Bodová symetrie
    ROTATIONAL = "rotational"                  # Rotační symetrie
    ADJACENT_PAIRS = "adjacent_pairs"          # Přilehlé páry
    OPPOSITE_PAIRS = "opposite_pairs"          # Protilehlé páry
    ALTERNATING = "alternating"                # Střídavé vzory
    CASCADING = "cascading"                    # Kaskádové efekty

class MovementDirection(Enum):
    """Směry pohybu"""
    HORIZONTAL_SWEEP = "horizontal_sweep"       # Horizontální kývání
    VERTICAL_NOD = "vertical_nod"              # Vertikální kývání
    DIAGONAL_CROSS = "diagonal_cross"          # Diagonální křížení
    CIRCULAR_CLOCK = "circular_clock"          # Kruhový ve směru hodin
    CIRCULAR_COUNTER = "circular_counter"      # Kruhový proti hodinám
    PENDULUM_SYNC = "pendulum_sync"            # Synchronní kyvadlo
    PENDULUM_PHASE = "pendulum_phase"          # Fázově posunuté kyvadlo

class SymmetryChoreographer:
    """Generátor choreografií založených na symetrii"""

    def __init__(self):
        self.output_dir = Path("generated_scenes_advanced/symmetry_movement")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Moving heads konfigurace - pozice v saune
        self.moving_head_ids = {
            "moving_head_1": "1753951490",  # Levý zadní
            "moving_head_2": "1753953036",  # Levý přední
            "moving_head_3": "1753953037",  # Střední
            "moving_head_4": "1753953038",  # Pravý přední
            "moving_head_5": "1753953039",  # Pravý zadní
        }

        # Barevný wheel
        self.color_wheel = {
            "white": 0, "red": 11, "orange": 31, "blue": 51,
            "yellow": 71, "green": 91, "purple": 111, "cyan": 131,
            "magenta": 171, "warm_white": 211
        }

        # Symetrické páry moving heads
        self.symmetry_pairs = {
            "horizontal_mirror": [(0, 4), (1, 3)],  # Levý-pravý zrcadlení
            "adjacent_pairs": [(0, 1), (1, 2), (2, 3), (3, 4)],  # Sousední páry
            "opposite_pairs": [(0, 2), (1, 4), (2, 0)],  # Protilehlé páry
            "center_symmetry": [(0, 4), (1, 3), (2,)]  # Symetrie kolem středu
        }

        # Pozice v prostoru pro výpočty
        self.head_positions = {
            0: {"x": -1.0, "y": -0.8, "name": "Levý zadní"},
            1: {"x": -0.5, "y": 0.5, "name": "Levý přední"},
            2: {"x": 0.0, "y": 0.8, "name": "Střední"},
            3: {"x": 0.5, "y": 0.5, "name": "Pravý přední"},
            4: {"x": 1.0, "y": -0.8, "name": "Pravý zadní"},
        }

    def generate_mirror_horizontal_movement(self,
                                          swing_amplitude: float = 40,
                                          swing_frequency: float = 0.06,
                                          sync_offset: float = 0.0,
                                          duration: int = 20000) -> Dict:
        """Horizontální zrcadlení - levé a pravé se pohybují symetricky"""

        steps = 100
        step_duration = duration // steps

        movement_data = {
            "name": "Mirror Horizontal",
            "description": "Symetrické horizontální zrcadlení - levé a pravé světla",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["blue", "cyan", "white", "cyan", "blue"]  # Symetrické barvy
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            pos_x = self.head_positions[head_idx]["x"]

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Symetrický pohyb kolem středu
                swing_phase = time * swing_frequency + sync_offset

                if head_idx in [0, 4]:  # Krajní heads - symetrické
                    # Levý a pravý se pohybují zrcadlově
                    pan_offset = swing_amplitude * math.sin(swing_phase) * abs(pos_x)
                    if pos_x < 0:  # Levý
                        pan = 128 - pan_offset
                    else:  # Pravý
                        pan = 128 + pan_offset

                elif head_idx in [1, 3]:  # Přední heads - menší symetrie
                    pan_offset = swing_amplitude * 0.7 * math.sin(swing_phase + math.pi/4) * abs(pos_x)
                    if pos_x < 0:
                        pan = 128 - pan_offset
                    else:
                        pan = 128 + pan_offset

                else:  # Střední head - jemné kývání
                    pan = 128 + swing_amplitude * 0.3 * math.sin(swing_phase + math.pi/2)

                # Tilt - jemné vertikální pohyby
                tilt = 128 + 15 * math.sin(swing_phase * 1.3 + head_idx * 0.2)

                pan_sequence.append(max(30, min(225, int(pan))))
                tilt_sequence.append(max(70, min(185, int(tilt))))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_adjacent_pairs_movement(self,
                                       chase_speed: float = 0.1,
                                       pair_offset: float = 0.5,
                                       amplitude: float = 35,
                                       duration: int = 18000) -> Dict:
        """Přilehlé páry - sousední lights se pohybují společně"""

        steps = 90
        step_duration = duration // steps

        movement_data = {
            "name": "Adjacent Pairs",
            "description": "Přilehlé páry světel se pohybují synchronně",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["red", "red", "green", "green", "blue"]  # Párové barvy
        }

        # Definice párů: (0,1), (1,2), (2,3), (3,4)
        pair_patterns = [
            {"pair": (0, 1), "phase": 0.0},
            {"pair": (1, 2), "phase": pair_offset},
            {"pair": (2, 3), "phase": pair_offset * 2},
            {"pair": (3, 4), "phase": pair_offset * 3},
        ]

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Najdi k jakému páru patří tento head
            head_pair_phase = 0.0
            for pattern in pair_patterns:
                if head_idx in pattern["pair"]:
                    head_pair_phase = pattern["phase"]
                    break

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Pohyb párů s fázovým posunem
                pair_phase = time * chase_speed + head_pair_phase

                # Pan pohyb - páry se pohybují společně
                pan_movement = amplitude * math.sin(pair_phase)
                pan = 128 + pan_movement

                # Tilt - jemný vertikální pohyb
                tilt_movement = amplitude * 0.4 * math.cos(pair_phase * 0.8)
                tilt = 128 + tilt_movement

                pan_sequence.append(max(35, min(220, int(pan))))
                tilt_sequence.append(max(75, min(180, int(tilt))))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_opposite_pairs_movement(self,
                                       contrast_amplitude: float = 45,
                                       frequency: float = 0.08,
                                       phase_shift: float = math.pi,
                                       duration: int = 16000) -> Dict:
        """Protilehlé páry - protější světla se pohybují opačně"""

        steps = 80
        step_duration = duration // steps

        movement_data = {
            "name": "Opposite Pairs",
            "description": "Protilehlé světla se pohybují v protifázi",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["red", "orange", "white", "orange", "red"]  # Kontrastní symetrie
        }

        # Protilehlé páry: 0-4 (krajní), 1-3 (přední), 2 (střed)
        opposite_pairs = {
            0: 4,   # Levý zadní ↔ Pravý zadní
            1: 3,   # Levý přední ↔ Pravý přední
            2: None,  # Střední - vlastní pohyb
            3: 1,   # Pravý přední ↔ Levý přední
            4: 0    # Pravý zadní ↔ Levý zadní
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            for step in range(steps):
                time = step * (step_duration / 1000)

                base_phase = time * frequency

                if head_idx == 2:  # Střední head - nezávislý pohyb
                    pan = 128 + contrast_amplitude * 0.6 * math.sin(base_phase * 1.5)
                    tilt = 128 + contrast_amplitude * 0.3 * math.cos(base_phase * 1.2)

                else:  # Protilehlé páry
                    opposite_idx = opposite_pairs[head_idx]

                    if head_idx < opposite_idx:  # Hlavní head v páru
                        # Normální pohyb
                        pan = 128 + contrast_amplitude * math.sin(base_phase)
                        tilt = 128 + contrast_amplitude * 0.5 * math.cos(base_phase * 0.9)
                    else:  # Protilehlý head
                        # Opačný pohyb (fázový posun π)
                        pan = 128 + contrast_amplitude * math.sin(base_phase + phase_shift)
                        tilt = 128 + contrast_amplitude * 0.5 * math.cos(base_phase * 0.9 + phase_shift)

                pan_sequence.append(max(25, min(230, int(pan))))
                tilt_sequence.append(max(65, min(190, int(tilt))))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_pendulum_sync_movement(self,
                                      swing_angle: float = 50,
                                      pendulum_frequency: float = 0.05,
                                      sync_type: str = "synchronized",
                                      duration: int = 22000) -> Dict:
        """Kyvadlový pohyb - tam a zpět synchronně nebo fázově"""

        steps = 110
        step_duration = duration // steps

        movement_data = {
            "name": f"Pendulum {sync_type.title()}",
            "description": f"Kyvadlový pohyb tam a zpět - {sync_type}",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["warm_white", "orange", "yellow", "orange", "warm_white"]
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Fázový posun podle typu synchronizace
            if sync_type == "synchronized":
                phase_offset = 0.0  # Všechny synchronně
            elif sync_type == "cascading":
                phase_offset = head_idx * 0.2  # Postupné spuštění
            elif sync_type == "alternating":
                phase_offset = (head_idx % 2) * math.pi  # Střídavě
            else:  # wave
                phase_offset = head_idx * (math.pi / 4)  # Vlnový efekt

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Kyvadlový pohyb (harmonická funkce)
                pendulum_phase = time * pendulum_frequency + phase_offset

                # Pan - hlavní kyvadlový pohyb
                pan_swing = swing_angle * math.sin(pendulum_phase)
                pan = 128 + pan_swing

                # Tilt - jemný vertikální pohyb
                tilt_swing = swing_angle * 0.3 * math.sin(pendulum_phase * 1.1 + math.pi/6)
                tilt = 128 + tilt_swing

                pan_sequence.append(max(20, min(235, int(pan))))
                tilt_sequence.append(max(60, min(195, int(tilt))))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_rotational_symmetry_movement(self,
                                            rotation_speed: float = 0.04,
                                            radius: float = 40,
                                            symmetry_order: int = 5,
                                            duration: int = 25000) -> Dict:
        """Rotační symetrie - všechny heads rotují se zachováním symetrie"""

        steps = 125
        step_duration = duration // steps

        movement_data = {
            "name": "Rotational Symmetry",
            "description": f"Rotační symetrie {symmetry_order}. řádu",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["purple", "blue", "cyan", "green", "yellow"]  # Spektrální postupnost
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Úhel pro symetrické rozmístění
            base_angle = head_idx * (2 * math.pi / 5)  # 72° mezi heads

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Rotace s časem
                rotation_angle = time * rotation_speed + base_angle

                # Kruhová trajektorie se zachováním symetrie
                pan = 128 + radius * math.cos(rotation_angle)
                tilt = 128 + radius * 0.6 * math.sin(rotation_angle)

                # Přidej jemnou modulaci pro organičnost
                modulation = 5 * math.sin(time * 0.02 + head_idx)
                pan += modulation
                tilt += modulation * 0.5

                pan_sequence.append(max(35, min(220, int(pan))))
                tilt_sequence.append(max(70, min(185, int(tilt))))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def create_symmetry_scene(self, movement_data: Dict,
                            gobo: int = 0, prism: int = 0,
                            dimmer: int = 255, shutter: int = 32) -> str:
        """Vytvoří .scex soubor se symetrickým pohybem"""

        # XML struktura
        root = ET.Element("Scene")

        # Fixtures
        fixtures = ET.SubElement(root, "Fixtures")
        for head_name, head_id in self.moving_head_ids.items():
            fixture = ET.SubElement(fixtures, "Fixture")
            fixture.set("id", head_id)
            fixture.set("name", head_name.replace("_", " ").title())
            fixture.set("model", "Intimidator Spot 375Z IRC (15CH)")

        # Steps se symetrickými pohyby
        steps = ET.SubElement(root, "Steps")

        for step_idx in range(movement_data["steps"]):
            step = ET.SubElement(steps, "Step")
            step.set("length", str(movement_data["step_duration"]))

            for head_idx, (head_name, head_id) in enumerate(self.moving_head_ids.items()):
                fixture_elem = ET.SubElement(step, "Fixture")
                fixture_elem.set("id", head_id)

                # Symetrické pozice
                pan = movement_data["pan_sequences"][f"head_{head_idx}"][step_idx]
                tilt = movement_data["tilt_sequences"][f"head_{head_idx}"][step_idx]

                # Symetrické barvy
                color_name = movement_data["colors"][head_idx]
                color_value = self.color_wheel.get(color_name, 0)

                # DMX kanály
                channels = [
                    ("pan", pan),
                    ("tilt", tilt),
                    ("color", color_value),
                    ("dimmer", dimmer),
                    ("shutter", shutter),
                    ("gobo", gobo),
                    ("prism", prism),
                    ("focus", 150),
                ]

                for channel_name, value in channels:
                    channel = ET.SubElement(fixture_elem, "Channel")
                    channel.set("name", channel_name)
                    channel.set("value", str(value))

        # Uložení
        filename = f"{movement_data['name'].lower().replace(' ', '_')}.scex"
        filepath = self.output_dir / filename

        self._indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(str(filepath), encoding="UTF-8", xml_declaration=True)

        print(f"   ✅ Created: {filename}")
        return str(filepath)

    def generate_all_symmetry_movements(self):
        """Generuje všechny symetrické pohyby"""
        print("🔄 Generating Symmetry-Based Choreographies...")

        movements = [
            # Zrcadlení
            {
                "generator": self.generate_mirror_horizontal_movement,
                "params": {"swing_amplitude": 35, "swing_frequency": 0.05},
                "name": "Mirror Horizontal Gentle"
            },
            {
                "generator": self.generate_mirror_horizontal_movement,
                "params": {"swing_amplitude": 45, "swing_frequency": 0.08, "sync_offset": 0.3},
                "name": "Mirror Horizontal Dynamic"
            },

            # Přilehlé páry
            {
                "generator": self.generate_adjacent_pairs_movement,
                "params": {"chase_speed": 0.08, "pair_offset": 0.4, "amplitude": 30},
                "name": "Adjacent Pairs Gentle"
            },
            {
                "generator": self.generate_adjacent_pairs_movement,
                "params": {"chase_speed": 0.15, "pair_offset": 0.6, "amplitude": 40},
                "name": "Adjacent Pairs Fast"
            },

            # Protilehlé páry
            {
                "generator": self.generate_opposite_pairs_movement,
                "params": {"contrast_amplitude": 40, "frequency": 0.06},
                "name": "Opposite Pairs Contrast"
            },
            {
                "generator": self.generate_opposite_pairs_movement,
                "params": {"contrast_amplitude": 50, "frequency": 0.1, "phase_shift": math.pi/2},
                "name": "Opposite Pairs Quarter"
            },

            # Kyvadlové pohyby
            {
                "generator": self.generate_pendulum_sync_movement,
                "params": {"swing_angle": 45, "pendulum_frequency": 0.04, "sync_type": "synchronized"},
                "name": "Pendulum Synchronized"
            },
            {
                "generator": self.generate_pendulum_sync_movement,
                "params": {"swing_angle": 40, "pendulum_frequency": 0.06, "sync_type": "cascading"},
                "name": "Pendulum Cascading"
            },
            {
                "generator": self.generate_pendulum_sync_movement,
                "params": {"swing_angle": 38, "pendulum_frequency": 0.05, "sync_type": "alternating"},
                "name": "Pendulum Alternating"
            },

            # Rotační symetrie
            {
                "generator": self.generate_rotational_symmetry_movement,
                "params": {"rotation_speed": 0.03, "radius": 35, "symmetry_order": 5},
                "name": "Rotational Symmetry Slow"
            },
            {
                "generator": self.generate_rotational_symmetry_movement,
                "params": {"rotation_speed": 0.06, "radius": 45, "symmetry_order": 5},
                "name": "Rotational Symmetry Fast"
            }
        ]

        created_files = []
        for movement_config in movements:
            # Vygeneruj pohybová data
            movement_data = movement_config["generator"](**movement_config["params"])
            movement_data["name"] = movement_config["name"]

            # Vytvoř scénu
            filepath = self.create_symmetry_scene(movement_data)
            created_files.append(filepath)

        # Vytvoř index
        self._create_symmetry_index(movements)

        print(f"✅ Generated {len(movements)} symmetry-based choreographies")
        return created_files

    def _create_symmetry_index(self, movements: List[Dict]):
        """Vytvoří index symetrických pohybů"""
        index = {
            "symmetry_movements": {},
            "principles": {
                "mirror_symmetry": "Zrcadlové odrazy - levé a pravé světla",
                "adjacent_pairs": "Přilehlé páry - sousední světla společně",
                "opposite_pairs": "Protilehlé páry - vzdálená světla v kontrastue",
                "pendulum": "Kyvadlové pohyby - tam a zpět",
                "rotational": "Rotační symetrie - zachování úhlových vztahů"
            },
            "usage_guide": {
                "romantic_moments": ["Mirror Horizontal Gentle", "Pendulum Synchronized"],
                "energetic_sections": ["Adjacent Pairs Fast", "Rotational Symmetry Fast"],
                "dramatic_buildup": ["Opposite Pairs Contrast", "Pendulum Alternating"],
                "hypnotic_parts": ["Rotational Symmetry Slow", "Pendulum Cascading"],
                "rhythmic_emphasis": ["Adjacent Pairs Gentle", "Mirror Horizontal Dynamic"]
            }
        }

        for movement_config in movements:
            name = movement_config["name"]
            index["symmetry_movements"][name] = {
                "file": f"{name.lower().replace(' ', '_')}.scex",
                "description": movement_config["generator"].__doc__.split('\n')[0].strip('"""'),
                "principles": self._identify_movement_principles(name)
            }

        # Ulož index
        with open(self.output_dir / "symmetry_movements_index.json", "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def _identify_movement_principles(self, name: str) -> List[str]:
        """Identifikuje principy pohybu"""
        principles = []
        if "mirror" in name.lower():
            principles.append("zrcadlová_symetrie")
        if "adjacent" in name.lower():
            principles.append("přilehlé_páry")
        if "opposite" in name.lower():
            principles.append("protilehlé_páry")
        if "pendulum" in name.lower():
            principles.append("kyvadlový_pohyb")
        if "rotational" in name.lower():
            principles.append("rotační_symetrie")
        return principles

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
    print("🔄 Symmetry & Movement Choreographer")
    print("=" * 50)

    choreographer = SymmetryChoreographer()
    created_files = choreographer.generate_all_symmetry_movements()

    print()
    print("🎭 Symmetry Movement System Created!")
    print(f"   Files: {len(created_files)}")
    print(f"   Location: {choreographer.output_dir}")
    print()
    print("🔄 Symetrické Principy:")
    print("   🪞 Mirror Symmetry - zrcadlové odrazy")
    print("   👥 Adjacent Pairs - přilehlé páry")
    print("   ⚡ Opposite Pairs - protilehlé kontrasty")
    print("   ⏳ Pendulum Motion - kyvadlové pohyby tam a zpět")
    print("   🌀 Rotational Symmetry - rotační harmonie")
    print()
    print("💡 Každý pohyb založen na matematických principech symetrie!")
    print("   ✅ Přilehlé/protilehlé světla")
    print("   ✅ Pohyby tam a zpět")
    print("   ✅ Symetrické a asymetrické formace")
    print("   ✅ Kontinuální využití moving heads potenciálu")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Dynamic Movement Choreographer
Pokročilý systém pro dynamické pohyby moving heads
Kombinuje kontinuální pohyb s hudební analýzou
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json
import math
import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum

class MovementStyle(Enum):
    """Styly pohybu moving heads"""
    WATER_WAVES = "water_waves"           # Vlnový pohyb jako vodní hladina
    CIRCULAR_FLOW = "circular_flow"       # Plynulý kruhový tok
    PENDULUM_SWING = "pendulum_swing"     # Kyvadlový pohyb
    SPIRAL_ASCENT = "spiral_ascent"       # Spirálový výstup
    FIGURE_8_INFINITY = "figure_8_infinity"  # Nekonečná osmička
    RANDOM_ORGANIC = "random_organic"     # Organický náhodný pohyb
    LASER_PRECISION = "laser_precision"   # Přesné laserové řezy
    BREATHING_EXPAND = "breathing_expand" # Dýchání - rozšiřování/smršťování
    CHASE_SEQUENCE = "chase_sequence"     # Následování v sekvenci
    MIRROR_SYMMETRY = "mirror_symmetry"   # Zrcadlová symetrie

class DynamicMovementChoreographer:
    """Generátor dynamických pohybů pro moving heads"""

    def __init__(self):
        self.output_dir = Path("generated_scenes_advanced/dynamic_movement")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Moving heads konfigurace
        self.moving_head_ids = {
            "moving_head_1": "1753951490",
            "moving_head_2": "1753953036",
            "moving_head_3": "1753953037",
            "moving_head_4": "1753953038",
            "moving_head_5": "1753953039",
        }

        # Barevný wheel
        self.color_wheel = {
            "white": 0, "red": 11, "orange": 31, "blue": 51,
            "yellow": 71, "green": 91, "purple": 111, "cyan": 131,
            "magenta": 171, "warm_white": 211
        }

        # Pozice moving heads v prostoru (pro výpočet pohybů)
        self.head_positions = {
            0: {"x": -1.0, "y": 0.0},   # Levý
            1: {"x": -0.5, "y": 0.8},   # Levý přední
            2: {"x": 0.0, "y": 1.0},    # Střední přední
            3: {"x": 0.5, "y": 0.8},    # Pravý přední
            4: {"x": 1.0, "y": 0.0},    # Pravý
        }

    def generate_water_waves_movement(self,
                                    wave_frequency: float = 0.1,
                                    wave_amplitude: float = 30,
                                    phase_shift: float = 60,
                                    duration: int = 20000) -> Dict:
        """Generuje vlnový pohyb jako vodní hladina"""

        steps = 100  # Počet kroků animace
        step_duration = duration // steps

        movement_data = {
            "name": "Water Waves",
            "description": "Plynulý vlnový pohyb simulující vodní hladinu",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["blue", "cyan", "white", "blue", "cyan"]
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Pozice moving head pro výpočet vlny
            pos_x = self.head_positions[head_idx]["x"]
            pos_y = self.head_positions[head_idx]["y"]

            for step in range(steps):
                # Čas v sekundách
                time = step * (step_duration / 1000)

                # Vlnová funkce s různým phase shiftem pro každý head
                wave_phase = time * wave_frequency + head_idx * (phase_shift * math.pi / 180)

                # Pan: horizontální vlnění
                pan_offset = wave_amplitude * math.sin(wave_phase)
                base_pan = 128 + pan_offset * pos_x  # Pozice v prostoru ovlivňuje amplitudu

                # Tilt: vertikální vlnění s mírným zpožděním
                tilt_wave = wave_amplitude * 0.6 * math.sin(wave_phase + math.pi/4)
                base_tilt = 128 + tilt_wave

                # Přidej jemný náhodný šum pro organičnost
                noise_pan = np.random.normal(0, 2)
                noise_tilt = np.random.normal(0, 1.5)

                final_pan = max(20, min(235, base_pan + noise_pan))
                final_tilt = max(50, min(200, base_tilt + noise_tilt))

                pan_sequence.append(int(final_pan))
                tilt_sequence.append(int(final_tilt))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_circular_flow_movement(self,
                                      radius: float = 40,
                                      rotation_speed: float = 0.05,
                                      center_drift: bool = True,
                                      duration: int = 20000) -> Dict:
        """Generuje plynulý kruhový tok"""

        steps = 120
        step_duration = duration // steps

        movement_data = {
            "name": "Circular Flow",
            "description": "Plynulý kruhový pohyb s postupným driftováním centra",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["purple", "magenta", "blue", "cyan", "white"]
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Každý head má mírně jiný radius a rychlost
            head_radius = radius + head_idx * 5
            head_speed = rotation_speed + head_idx * 0.01

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Základní kruhový pohyb
                angle = time * head_speed + head_idx * (2 * math.pi / 5)  # 72° offset

                # Center drift - centrum kruhu se postupně pohybuje
                if center_drift:
                    center_x = 128 + 20 * math.sin(time * 0.02)
                    center_y = 128 + 15 * math.cos(time * 0.015)
                else:
                    center_x = center_y = 128

                # Výpočet pozice na kruhu
                pan = center_x + head_radius * math.cos(angle)
                tilt = center_y + head_radius * 0.7 * math.sin(angle)  # Tilt má menší rozsah

                # Omezeninl rozsah
                final_pan = max(30, min(225, pan))
                final_tilt = max(60, min(195, tilt))

                pan_sequence.append(int(final_pan))
                tilt_sequence.append(int(final_tilt))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_figure_8_infinity_movement(self,
                                          size: float = 35,
                                          speed: float = 0.08,
                                          vertical_emphasis: float = 0.8,
                                          duration: int = 15000) -> Dict:
        """Generuje nekonečnou osmičku - symbol nekonečna"""

        steps = 80
        step_duration = duration // steps

        movement_data = {
            "name": "Figure 8 Infinity",
            "description": "Hypnotický pohyb ve tvaru nekonečna",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["orange", "yellow", "red", "magenta", "purple"]
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Každý head má různou velikost osmičky
            head_size = size + head_idx * 3
            head_speed = speed + head_idx * 0.005

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Parametrické rovnice pro osmičku (lemniskáta)
                t = time * head_speed + head_idx * 0.4  # Phase offset

                # Lemniskáta of Bernoulli: x = a*cos(t)/(1+sin²(t)), y = a*sin(t)*cos(t)/(1+sin²(t))
                denominator = 1 + math.sin(t)**2

                x = head_size * math.cos(t) / denominator
                y = head_size * math.sin(t) * math.cos(t) / denominator * vertical_emphasis

                # Převod na DMX hodnoty
                pan = 128 + x
                tilt = 128 + y

                # Clamp values
                final_pan = max(40, min(215, pan))
                final_tilt = max(70, min(185, tilt))

                pan_sequence.append(int(final_pan))
                tilt_sequence.append(int(final_tilt))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_breathing_expand_movement(self,
                                         min_radius: float = 10,
                                         max_radius: float = 45,
                                         breath_rate: float = 0.03,
                                         phase_sync: bool = False,
                                         duration: int = 25000) -> Dict:
        """Generuje dýchací pohyb - roztahování a smršťování"""

        steps = 150
        step_duration = duration // steps

        movement_data = {
            "name": "Breathing Expand",
            "description": "Organické dýchání - roztahování a smršťování formace",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["warm_white", "orange", "red", "orange", "warm_white"]
        }

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            # Úhel pro každý head v kruhu
            base_angle = head_idx * (2 * math.pi / 5)

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Breathing function - sinusoida pro radius
                if phase_sync:
                    breath_phase = time * breath_rate
                else:
                    # Každý head dýchá s mírným zpožděním
                    breath_phase = time * breath_rate + head_idx * 0.2

                # Výpočet current radius (dýchání)
                radius_range = max_radius - min_radius
                current_radius = min_radius + radius_range * (0.5 + 0.5 * math.sin(breath_phase))

                # Pozice na kruhu s proměnným radiusem
                pan = 128 + current_radius * math.cos(base_angle)
                tilt = 128 + current_radius * 0.6 * math.sin(base_angle)

                # Přidej jemnou rotaci během dýchání
                rotation = time * 0.01
                pan += 5 * math.sin(rotation + base_angle)
                tilt += 3 * math.cos(rotation + base_angle)

                final_pan = max(35, min(220, pan))
                final_tilt = max(65, min(190, tilt))

                pan_sequence.append(int(final_pan))
                tilt_sequence.append(int(final_tilt))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def generate_chase_sequence_movement(self,
                                       chase_speed: float = 0.15,
                                       trail_length: int = 3,
                                       path_complexity: int = 8,
                                       duration: int = 18000) -> Dict:
        """Generuje chase sekvenci - heads následují jeden druhého"""

        steps = 90
        step_duration = duration // steps

        movement_data = {
            "name": "Chase Sequence",
            "description": "Moving heads následují jeden druhého po komplexní trajektorii",
            "steps": steps,
            "step_duration": step_duration,
            "pan_sequences": {},
            "tilt_sequences": {},
            "colors": ["red", "orange", "yellow", "green", "blue"]
        }

        # Vytvoř komplexní trajektorii
        trajectory_points = []
        for i in range(path_complexity * 4):  # Více bodů pro plynulost
            angle = i * (2 * math.pi / path_complexity)
            # Složitější tvar - kombinace kruhů
            r1 = 35 * math.cos(angle)
            r2 = 25 * math.sin(2 * angle)

            x = 128 + r1 * math.cos(angle) + r2 * math.cos(3 * angle)
            y = 128 + r1 * 0.7 * math.sin(angle) + r2 * 0.5 * math.sin(3 * angle)

            trajectory_points.append((max(40, min(215, x)), max(70, min(185, y))))

        for head_idx in range(5):
            pan_sequence = []
            tilt_sequence = []

            for step in range(steps):
                time = step * (step_duration / 1000)

                # Pozice na trajektorii s různým offsetem pro každý head
                trajectory_position = (time * chase_speed + head_idx * trail_length) % len(trajectory_points)

                # Interpolace mezi body
                point_index = int(trajectory_position)
                next_index = (point_index + 1) % len(trajectory_points)
                interpolation = trajectory_position - point_index

                point1 = trajectory_points[point_index]
                point2 = trajectory_points[next_index]

                # Lineární interpolace
                pan = point1[0] + (point2[0] - point1[0]) * interpolation
                tilt = point1[1] + (point2[1] - point1[1]) * interpolation

                pan_sequence.append(int(pan))
                tilt_sequence.append(int(tilt))

            movement_data["pan_sequences"][f"head_{head_idx}"] = pan_sequence
            movement_data["tilt_sequences"][f"head_{head_idx}"] = tilt_sequence

        return movement_data

    def create_dynamic_scene(self, movement_data: Dict,
                           gobo: int = 0, prism: int = 0,
                           dimmer: int = 255, shutter: int = 32) -> str:
        """Vytvoří .scex soubor s dynamickým pohybem"""

        # XML struktura
        root = ET.Element("Scene")

        # Fixtures
        fixtures = ET.SubElement(root, "Fixtures")
        for head_name, head_id in self.moving_head_ids.items():
            fixture = ET.SubElement(fixtures, "Fixture")
            fixture.set("id", head_id)
            fixture.set("name", head_name.replace("_", " ").title())
            fixture.set("model", "Intimidator Spot 375Z IRC (15CH)")

        # Steps s dynamickým pohybem
        steps = ET.SubElement(root, "Steps")

        for step_idx in range(movement_data["steps"]):
            step = ET.SubElement(steps, "Step")
            step.set("length", str(movement_data["step_duration"]))

            for head_idx, (head_name, head_id) in enumerate(self.moving_head_ids.items()):
                fixture_elem = ET.SubElement(step, "Fixture")
                fixture_elem.set("id", head_id)

                # Dynamické pozice z vygenerovaných sekvencí
                pan = movement_data["pan_sequences"][f"head_{head_idx}"][step_idx]
                tilt = movement_data["tilt_sequences"][f"head_{head_idx}"][step_idx]

                # Barva
                color_name = movement_data["colors"][head_idx]
                color_value = self.color_wheel.get(color_name, 0)

                # Všechny DMX kanály
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

    def generate_all_dynamic_movements(self):
        """Generuje všechny dynamické pohyby"""
        print("🌊 Generating Dynamic Movement Choreographies...")

        movements = [
            # Water Waves - různé rychlosti a amplitudy
            {
                "generator": self.generate_water_waves_movement,
                "params": {"wave_frequency": 0.08, "wave_amplitude": 25, "duration": 20000},
                "name": "Water Waves Gentle"
            },
            {
                "generator": self.generate_water_waves_movement,
                "params": {"wave_frequency": 0.15, "wave_amplitude": 35, "duration": 15000},
                "name": "Water Waves Energetic"
            },

            # Circular Flow
            {
                "generator": self.generate_circular_flow_movement,
                "params": {"radius": 30, "rotation_speed": 0.04, "center_drift": True},
                "name": "Circular Flow Drift"
            },
            {
                "generator": self.generate_circular_flow_movement,
                "params": {"radius": 45, "rotation_speed": 0.08, "center_drift": False},
                "name": "Circular Flow Fast"
            },

            # Figure 8 Infinity
            {
                "generator": self.generate_figure_8_infinity_movement,
                "params": {"size": 30, "speed": 0.06, "vertical_emphasis": 0.9},
                "name": "Figure 8 Hypnotic"
            },
            {
                "generator": self.generate_figure_8_infinity_movement,
                "params": {"size": 40, "speed": 0.12, "vertical_emphasis": 0.6},
                "name": "Figure 8 Dynamic"
            },

            # Breathing Expand
            {
                "generator": self.generate_breathing_expand_movement,
                "params": {"min_radius": 15, "max_radius": 40, "breath_rate": 0.025, "phase_sync": True},
                "name": "Breathing Sync"
            },
            {
                "generator": self.generate_breathing_expand_movement,
                "params": {"min_radius": 8, "max_radius": 50, "breath_rate": 0.04, "phase_sync": False},
                "name": "Breathing Organic"
            },

            # Chase Sequence
            {
                "generator": self.generate_chase_sequence_movement,
                "params": {"chase_speed": 0.1, "trail_length": 4, "path_complexity": 6},
                "name": "Chase Complex"
            },
            {
                "generator": self.generate_chase_sequence_movement,
                "params": {"chase_speed": 0.2, "trail_length": 2, "path_complexity": 8},
                "name": "Chase Fast"
            }
        ]

        created_files = []
        for movement_config in movements:
            # Vygeneruj pohybová data
            movement_data = movement_config["generator"](**movement_config["params"])
            movement_data["name"] = movement_config["name"]

            # Vytvoř scénu
            filepath = self.create_dynamic_scene(movement_data)
            created_files.append(filepath)

        # Vytvoř index
        self._create_movement_index(movements)

        print(f"✅ Generated {len(movements)} dynamic movement choreographies")
        return created_files

    def _create_movement_index(self, movements: List[Dict]):
        """Vytvoří index dynamických pohybů"""
        index = {
            "dynamic_movements": {},
            "usage_guide": {
                "ambient_tracks": ["Water Waves Gentle", "Breathing Sync"],
                "energetic_parts": ["Water Waves Energetic", "Circular Flow Fast"],
                "hypnotic_moments": ["Figure 8 Hypnotic", "Breathing Organic"],
                "buildup_sections": ["Chase Complex", "Figure 8 Dynamic"],
                "dance_tracks": ["Circular Flow Drift", "Chase Fast"]
            },
            "technical_info": {
                "total_movements": len(movements),
                "features": [
                    "Kontinuální pohyb po celou dobu",
                    "Matematicky přesné trajektorie",
                    "Organické variace pro každý moving head",
                    "Plynulé přechody mezi pozicemi",
                    "Barevné mapování podle stylu pohybu"
                ]
            }
        }

        for movement_config in movements:
            name = movement_config["name"]
            params = movement_config["params"]

            index["dynamic_movements"][name] = {
                "file": f"{name.lower().replace(' ', '_')}.scex",
                "description": f"Dynamický pohyb: {name}",
                "parameters": params,
                "recommended_for": self._get_movement_recommendations(name)
            }

        # Ulož index
        with open(self.output_dir / "dynamic_movements_index.json", "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def _get_movement_recommendations(self, name: str) -> List[str]:
        """Doporučení kdy použít daný pohyb"""
        recommendations = {
            "Water Waves Gentle": ["ambient", "relaxační části", "intro/outro"],
            "Water Waves Energetic": ["buildup", "rytmické části", "dance"],
            "Circular Flow Drift": ["hypnotické momenty", "dlouhé buildupy"],
            "Circular Flow Fast": ["vysoká energie", "peak momenty"],
            "Figure 8 Hypnotic": ["meditativní části", "psychedelické momenty"],
            "Figure 8 Dynamic": ["komplexní buildupy", "technické části"],
            "Breathing Sync": ["emocionální momenty", "synchronní efekty"],
            "Breathing Organic": ["organické flow", "progresivní části"],
            "Chase Complex": ["dramatické momenty", "sledování melodie"],
            "Chase Fast": ["rychlé části", "chase efekty"]
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
    print("🌊 Dynamic Movement Choreographer")
    print("=" * 50)

    choreographer = DynamicMovementChoreographer()
    created_files = choreographer.generate_all_dynamic_movements()

    print()
    print("🎭 Dynamic Movement System Created!")
    print(f"   Files: {len(created_files)}")
    print(f"   Location: {choreographer.output_dir}")
    print()
    print("🎯 Featured Movements:")
    print("   🌊 Water Waves - plynulé vlnění jako vodní hladina")
    print("   🔄 Circular Flow - kruhové toky s driftujícím centrem")
    print("   ♾️  Figure 8 Infinity - hypnotické nekonečno")
    print("   🫁 Breathing Expand - organické dýchání formace")
    print("   🏃 Chase Sequence - komplexní následování")
    print()
    print("💡 Každý pohyb využívá plný potenciál moving heads!")
    print("   ✅ Kontinuální animace")
    print("   ✅ Matematicky přesné trajektorie")
    print("   ✅ Organické variace")
    print("   ✅ Plynulé přechody")

if __name__ == "__main__":
    main()
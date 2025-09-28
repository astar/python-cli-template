#!/usr/bin/env python3
"""Systematický generátor scex souborů na základě struktury sauny."""

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FixtureDefinition:
    """Definice fixture s pozicí a vlastnostmi."""

    id: str
    name: str
    model: str
    position: tuple[float, float, float]  # x, y, z
    channels: dict[str, int]  # channel_name -> max_value
    light_type: str
    zone: str  # ceiling, walls, floor, etc.


@dataclass
class ColorDefinition:
    """Definice barvy s RGB hodnotami."""

    name: str
    rgb: tuple[int, int, int]
    channel_values: dict[str, int]  # pro různé typy světel


@dataclass
class EffectDefinition:
    """Definice efektu."""

    name: str
    steps: list[dict]  # seznam kroků s channel hodnotami
    duration: int  # ms


class SystematicScexGenerator:
    """Systematický generátor scex souborů."""

    def __init__(self):
        self.fixtures: dict[str, FixtureDefinition] = {}
        self.colors: dict[str, ColorDefinition] = {}
        self.effects: dict[str, EffectDefinition] = {}
        self.zones: dict[str, list[str]] = {}  # zone -> fixture_ids

    def define_sauna_fixtures(self):
        """Definuje všechny fixtures v sauně systematicky."""
        print("🏗️ Defining systematic sauna fixtures...")

        # LED Wall Spots (1-11) - podle reálné struktury
        led_wall_positions = {
            1: (1.0, 7.6, 1.5),  # wall 1
            2: (3.0, 7.6, 1.5),  # wall 2
            3: (5.0, 7.6, 1.5),  # wall 3
            4: (7.0, 7.6, 1.5),  # wall 4
            5: (8.5, 5.0, 1.5),  # wall 5 (side)
            6: (8.5, 3.0, 1.5),  # wall 6 (side)
            7: (8.5, 1.0, 1.5),  # wall 7 (side)
            8: (7.0, 0.0, 1.5),  # wall 8 (back)
            9: (5.0, 0.0, 1.5),  # wall 9 (back)
            10: (3.0, 0.0, 1.5),  # wall 10 (back)
            11: (1.0, 0.0, 1.5),  # wall 11 (back)
        }

        for spot_id, (x, y, z) in led_wall_positions.items():
            fixture_id = f"175381{7199 + spot_id - 1}"  # Systematic ID
            self.fixtures[fixture_id] = FixtureDefinition(
                id=fixture_id,
                name=f"LED Wall Spot #{spot_id}",
                model="LED_pásky_(lavice)",
                position=(x, y, z),
                channels={"red": 255, "green": 255, "blue": 255, "white": 255},
                light_type="led_wall",
                zone="walls",
            )

        # Ceiling Spots (bodovky) - 12 spotů v kruhu
        ceiling_center = (4.25, 3.8)  # střed sauny
        import math

        for i in range(12):
            angle = (i * 2 * math.pi) / 12
            radius = 2.5
            x = ceiling_center[0] + radius * math.cos(angle)
            y = ceiling_center[1] + radius * math.sin(angle)
            z = 3.1  # výška stropu

            fixture_id = f"175382{1000 + i}"
            self.fixtures[fixture_id] = FixtureDefinition(
                id=fixture_id,
                name=f"Ceiling Spot #{i + 1}",
                model="Bodovka_RGB",
                position=(x, y, z),
                channels={"red": 255, "green": 255, "blue": 255, "dimmer": 255},
                light_type="ceiling_spot",
                zone="ceiling",
            )

        # Moving Heads - 5 kusů strategicky rozmístěných
        moving_head_positions = {
            1: (2.0, 2.0, 3.0),  # levý přední
            2: (6.5, 2.0, 3.0),  # pravý přední
            3: (2.0, 5.6, 3.0),  # levý zadní
            4: (6.5, 5.6, 3.0),  # pravý zadní
            5: (4.25, 3.8, 3.0),  # střed
        }

        for mh_id, (x, y, z) in moving_head_positions.items():
            fixture_id = f"175395{3037 + mh_id - 1}"
            self.fixtures[fixture_id] = FixtureDefinition(
                id=fixture_id,
                name=f"Moving Head #{mh_id}",
                model="Intimidator Spot 375Z IRC (15CH)",
                position=(x, y, z),
                channels={
                    # Professional channel mapping (index -> max_value)
                    # Based on hand_made_scenes analysis
                    0: 255,  # pan
                    1: 255,  # upan (fine pan)
                    2: 255,  # tilt
                    3: 255,  # utilt (fine tilt)
                    5: 255,  # color (channel 5, not 4!)
                    6: 255,  # gobo
                    7: 255,  # gobo_rotate
                    10: 255, # dimmer (channel 10, not 8!)
                    11: 255, # shutter (channel 11, not 9!)
                    14: 255, # zoom
                },
                light_type="moving_head",
                zone="ceiling",
            )

        # UV Lights - 2 kusy v rozích
        uv_positions = {1: (1.0, 1.0, 2.8), 2: (7.5, 6.6, 2.8)}

        for uv_id, (x, y, z) in uv_positions.items():
            fixture_id = f"175384{0000 + uv_id}"
            self.fixtures[fixture_id] = FixtureDefinition(
                id=fixture_id,
                name=f"UV Light #{uv_id}",
                model="UV_Light",
                position=(x, y, z),
                channels={"dimmer": 255},
                light_type="uv",
                zone="effects",
            )

        # Organize by zones
        self.zones = {
            "walls": [fid for fid, f in self.fixtures.items() if f.zone == "walls"],
            "ceiling": [fid for fid, f in self.fixtures.items() if f.zone == "ceiling"],
            "effects": [fid for fid, f in self.fixtures.items() if f.zone == "effects"],
        }

        print(f"   Defined {len(self.fixtures)} fixtures")
        print(
            f"   Zones: {[(zone, len(fixtures)) for zone, fixtures in self.zones.items()]}"
        )

    def define_systematic_colors(self):
        """Definuje systematickou paletu barev."""
        print("🎨 Defining systematic color palette...")

        # Základní barvy s přesnými RGB hodnotami
        base_colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "white_warm": (255, 200, 150),
            "white_cool": (200, 220, 255),
        }

        for color_name, (r, g, b) in base_colors.items():
            # Pro LED Wall spots (RGBW)
            led_channels = {
                "red": int(r * 255 / 255),
                "green": int(g * 255 / 255),
                "blue": int(b * 255 / 255),
                "white": 0 if color_name.startswith("white") else 0,
            }

            # Pro Moving Heads (color wheel hodnoty)
            mh_color_map = {
                "red": 11,
                "green": 19,
                "blue": 51,
                "purple": 59,
                "yellow": 35,
                "orange": 27,
                "cyan": 43,
                "magenta": 47,
                "white_warm": 43,
                "white_cool": 51,
            }

            self.colors[color_name] = ColorDefinition(
                name=color_name,
                rgb=(r, g, b),
                channel_values={
                    "led_wall": led_channels,
                    "ceiling_spot": led_channels,
                    "moving_head": {
                        # Professional channel mapping (channel_index -> value)
                        # Based on hand_made_scenes analysis
                        0: 128,     # pan: center position (0-255)
                        1: 128,     # upan: fine pan (duplicate pan for smooth movement)
                        2: 77,      # tilt: safe oven position (73-81 range)
                        3: 77,      # utilt: fine tilt (duplicate tilt)
                        5: mh_color_map.get(color_name, 11),  # color: professional color values
                        6: 0,       # gobo: no gobo (open)
                        7: 0,       # gobo_rotate: no rotation
                        10: 60,     # dimmer: moderate brightness (not 255!)
                        11: 4,      # shutter: open shutter (not 32!)
                        14: 0,      # zoom: minimum zoom
                    },
                    "uv": {"dimmer": 255},
                },
            )

        print(f"   Defined {len(self.colors)} systematic colors")

    def define_systematic_effects(self):
        """Definuje systematické efekty."""
        print("⚡ Defining systematic effects...")

        # Základní efekty
        self.effects["static"] = EffectDefinition(
            name="static",
            steps=[{"length": 5000}],  # 5s statické světlo
            duration=5000,
        )

        self.effects["fade_in"] = EffectDefinition(
            name="fade_in",
            steps=[
                {"length": 100, "dimmer": 0},  # start dim
                {"length": 2000, "dimmer": 255, "fade": True},  # fade to full
            ],
            duration=2100,
        )

        self.effects["fade_out"] = EffectDefinition(
            name="fade_out",
            steps=[
                {"length": 100, "dimmer": 255},
                {"length": 2000, "dimmer": 0, "fade": True},
            ],
            duration=2100,
        )

        self.effects["strobe_slow"] = EffectDefinition(
            name="strobe_slow",
            steps=[
                {"length": 500, "shutter": 255},  # on
                {"length": 500, "shutter": 0},  # off
            ],
            duration=1000,
        )

        self.effects["strobe_fast"] = EffectDefinition(
            name="strobe_fast",
            steps=[{"length": 100, "shutter": 255}, {"length": 100, "shutter": 0}],
            duration=200,
        )

        self.effects["pulse"] = EffectDefinition(
            name="pulse",
            steps=[
                {"length": 100, "dimmer": 100},
                {"length": 800, "dimmer": 255, "fade": True},
                {"length": 800, "dimmer": 100, "fade": True},
            ],
            duration=1700,
        )

        print(f"   Defined {len(self.effects)} systematic effects")

    def generate_scex_file(
        self, fixture_ids: list[str], color: str, effect: str
    ) -> str:
        """Generuje scex soubor pro zadané fixtures, barvu a efekt."""
        root = ET.Element("Scene")

        # Fixtures sekce
        fixtures_elem = ET.SubElement(root, "Fixtures")
        for fixture_id in fixture_ids:
            if fixture_id in self.fixtures:
                fixture = self.fixtures[fixture_id]
                fixture_elem = ET.SubElement(fixtures_elem, "Fixture")
                fixture_elem.set("id", fixture.id)
                fixture_elem.set("name", fixture.name)
                fixture_elem.set("model", fixture.model)

        # Steps sekce
        steps_elem = ET.SubElement(root, "Steps")

        if effect in self.effects and color in self.colors:
            effect_def = self.effects[effect]
            color_def = self.colors[color]

            for step_data in effect_def.steps:
                step_elem = ET.SubElement(steps_elem, "Step")
                step_elem.set("length", str(step_data["length"]))

                for fixture_id in fixture_ids:
                    if fixture_id in self.fixtures:
                        fixture = self.fixtures[fixture_id]
                        fixture_elem = ET.SubElement(step_elem, "Fixture")
                        fixture_elem.set("id", fixture.id)

                        # Track channels that have been added
                        added_channels = set()

                        # Přidej channel hodnoty
                        light_type = fixture.light_type
                        if light_type in color_def.channel_values:
                            channels = color_def.channel_values[light_type]

                            # Professional moving heads use channel indices directly
                            if light_type == "moving_head":
                                channel_names = {
                                    0: "pan", 1: "upan", 2: "tilt", 3: "utilt",
                                    5: "color", 6: "gobo", 7: "gobo_rotate",
                                    10: "dimmer", 11: "shutter", 14: "zoom"
                                }

                                for channel_index, value in channels.items():
                                    if channel_index in fixture.channels:
                                        channel_elem = ET.SubElement(fixture_elem, "Channel")
                                        channel_elem.set("index", str(channel_index))
                                        channel_elem.set("name", channel_names.get(channel_index, f"ch_{channel_index}"))
                                        channel_elem.set("value", str(value))

                                        if step_data.get("fade", False):
                                            channel_elem.set("fade", "1")

                                        added_channels.add(channel_index)
                            else:
                                # Traditional fixtures use channel names
                                for channel_name, value in channels.items():
                                    if channel_name in fixture.channels:
                                        channel_elem = ET.SubElement(fixture_elem, "Channel")
                                        channel_elem.set(
                                            "index",
                                            str(list(fixture.channels.keys()).index(channel_name))
                                        )
                                        channel_elem.set("name", channel_name)
                                        channel_elem.set("value", str(value))

                                        if step_data.get("fade", False):
                                            channel_elem.set("fade", "1")

                                        added_channels.add(channel_name)

                        # Přidej effect-specific channels (avoid duplicates)
                        for channel_name, value in step_data.items():
                            if (
                                channel_name in fixture.channels
                                and channel_name != "length"
                                and channel_name != "fade"
                                and channel_name not in added_channels
                            ):
                                channel_elem = ET.SubElement(fixture_elem, "Channel")
                                channel_elem.set(
                                    "index",
                                    str(
                                        list(fixture.channels.keys()).index(
                                            channel_name
                                        )
                                    ),
                                )
                                channel_elem.set("name", channel_name)
                                channel_elem.set("value", str(value))

                                added_channels.add(channel_name)

        # Convert to string
        ET.indent(root, space="  ")
        return '<?xml version="1.0" encoding="UTF-8"?>\n\n' + ET.tostring(
            root, encoding="unicode"
        )

    def generate_systematic_structure(self, output_dir: Path):
        """Generuje kompletní systematickou strukturu scex souborů."""
        print(f"🤖 Generating systematic scex structure to {output_dir}...")

        # Vytvoř základní strukturu
        structure = {
            "individual": {},  # jednotlivé fixtures
            "groups": {},  # skupiny fixtures
            "zones": {},  # zóny
            "patterns": {},  # prostorové vzory
        }

        # 1. Jednotlivé fixtures
        for fixture_id, fixture in self.fixtures.items():
            fixture_dir = (
                output_dir / "individual" / f"{fixture.light_type}_{fixture_id[-2:]}"
            )
            fixture_dir.mkdir(parents=True, exist_ok=True)

            for color_name in self.colors.keys():
                for effect_name in self.effects.keys():
                    filename = f"{color_name}_{effect_name}.scex"
                    filepath = fixture_dir / filename

                    scex_content = self.generate_scex_file(
                        [fixture_id], color_name, effect_name
                    )

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(scex_content)

            structure["individual"][f"{fixture.light_type}_{fixture_id[-2:]}"] = {
                "fixture_id": fixture_id,
                "position": fixture.position,
                "files_generated": len(self.colors) * len(self.effects),
            }

        # 2. Skupiny (páry, atd.)
        pairs = [
            ("1&11", ["1753817199", "1753817209"]),  # wall 1 & 11
            ("2&10", ["1753817200", "1753817208"]),  # wall 2 & 10
            ("3&9", ["1753817201", "1753817207"]),  # wall 3 & 9
            ("4&8", ["1753817202", "1753817206"]),  # wall 4 & 8
            ("5&7", ["1753817203", "1753817205"]),  # wall 5 & 7
        ]

        for pair_name, fixture_ids in pairs:
            # Filter existing fixtures
            existing_ids = [fid for fid in fixture_ids if fid in self.fixtures]
            if existing_ids:
                pair_dir = output_dir / "groups" / f"walls_{pair_name}"
                pair_dir.mkdir(parents=True, exist_ok=True)

                for color_name in self.colors.keys():
                    for effect_name in [
                        "static",
                        "fade_in",
                        "strobe_slow",
                    ]:  # Limited effects for groups
                        filename = f"{color_name}_{effect_name}.scex"
                        filepath = pair_dir / filename

                        scex_content = self.generate_scex_file(
                            existing_ids, color_name, effect_name
                        )

                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(scex_content)

                structure["groups"][f"walls_{pair_name}"] = {
                    "fixture_ids": existing_ids,
                    "files_generated": len(self.colors) * 3,
                }

        # 3. Zóny (všechny fixtures v zóně)
        for zone_name, fixture_ids in self.zones.items():
            existing_ids = [fid for fid in fixture_ids if fid in self.fixtures]
            if existing_ids:
                zone_dir = output_dir / "zones" / zone_name
                zone_dir.mkdir(parents=True, exist_ok=True)

                for color_name in self.colors.keys():
                    for effect_name in [
                        "static",
                        "fade_in",
                        "pulse",
                    ]:  # Limited effects for zones
                        filename = f"{color_name}_{effect_name}.scex"
                        filepath = zone_dir / filename

                        scex_content = self.generate_scex_file(
                            existing_ids, color_name, effect_name
                        )

                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(scex_content)

                structure["zones"][zone_name] = {
                    "fixture_ids": existing_ids,
                    "files_generated": len(self.colors) * 3,
                }

        # Uložit metadata
        with open(output_dir / "systematic_structure.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "fixtures": {
                        fid: {
                            "name": f.name,
                            "model": f.model,
                            "position": f.position,
                            "light_type": f.light_type,
                            "zone": f.zone,
                        }
                        for fid, f in self.fixtures.items()
                    },
                    "colors": {
                        name: {"rgb": color.rgb, "channel_values": color.channel_values}
                        for name, color in self.colors.items()
                    },
                    "effects": {
                        name: {"steps": effect.steps, "duration": effect.duration}
                        for name, effect in self.effects.items()
                    },
                    "structure": structure,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        # Report
        total_files = sum(
            info.get("files_generated", 0)
            for category in structure.values()
            for info in category.values()
        )
        print("✅ Systematic generation complete!")
        print(f"   Fixtures: {len(self.fixtures)}")
        print(f"   Colors: {len(self.colors)}")
        print(f"   Effects: {len(self.effects)}")
        print(f"   Total scex files: {total_files}")
        print(f"   Structure saved to: {output_dir / 'systematic_structure.json'}")


def main():
    """Hlavní funkce pro generování systematické struktury."""
    generator = SystematicScexGenerator()

    # Definuj systematickou strukturu
    generator.define_sauna_fixtures()
    generator.define_systematic_colors()
    generator.define_systematic_effects()

    # Generuj scex soubory
    output_dir = Path("generated_scenes_systematic")
    generator.generate_systematic_structure(output_dir)


if __name__ == "__main__":
    main()

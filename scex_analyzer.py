#!/usr/bin/env python3
"""Analyzátor scex souborů pro systematickou restrukturalizaci."""

import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


def analyze_all_scex_files():
    """Analyzuje všechny scex soubory a zjistí fixture ID a jejich vlastnosti."""
    base_path = Path("../auto-dmx/dmx/Infinit Maximus - new admin/scenes")

    fixtures_db = {}
    light_types = {
        "LED_Walls": defaultdict(list),
        "Bodovky": defaultdict(list),
        "Moving_heads": defaultdict(list),
        "UV": defaultdict(list),
        "LED_Oven": defaultdict(list),
        "SPOTS_walls": defaultdict(list),
    }

    print("🔍 Scanning all scex files...")

    # Procházej všechny typy světel
    for light_type in light_types:
        light_path = base_path / light_type
        if not light_path.exists():
            continue

        print(f"\n📁 Analyzing {light_type}...")
        scex_files = list(light_path.rglob("*.scex"))
        print(f"   Found {len(scex_files)} scex files")

        for scex_file in scex_files:
            relative_path = scex_file.relative_to(base_path)
            print(f"   📄 {relative_path}")

            try:
                tree = ET.parse(scex_file)
                root = tree.getroot()

                # Najdi všechny fixtures
                for fixture_elem in root.findall(".//Fixture"):
                    fixture_id = fixture_elem.get("id")
                    fixture_name = fixture_elem.get("name", "Unknown")
                    fixture_model = fixture_elem.get("model", "Unknown")

                    if fixture_id:
                        # Uložit fixture info
                        if fixture_id not in fixtures_db:
                            fixtures_db[fixture_id] = {
                                "name": fixture_name,
                                "model": fixture_model,
                                "files": [],
                                "channels": set(),
                                "light_type": light_type,
                            }

                        fixtures_db[fixture_id]["files"].append(str(relative_path))

                        # Analyzuj channels pro tento fixture
                        for step in root.findall(".//Step"):
                            for fixture_in_step in step.findall(".//Fixture"):
                                if fixture_in_step.get("id") == fixture_id:
                                    for channel in fixture_in_step.findall("Channel"):
                                        channel_name = channel.get("name")
                                        if channel_name:
                                            fixtures_db[fixture_id]["channels"].add(
                                                channel_name
                                            )

                        light_types[light_type][fixture_id].append(str(relative_path))

                        print(f"      Fixture ID: {fixture_id}")
                        print(f"      Name: {fixture_name}")
                        print(f"      Model: {fixture_model}")

            except Exception as e:
                print(f"❌ Error parsing {scex_file}: {e}")

    return fixtures_db, light_types


def analyze_fixture_patterns(fixtures_db):
    """Analyzuje vzory ve fixture ID a pojmenování."""
    print("\n📊 Fixture Database Summary:")
    print(f"   Total fixtures: {len(fixtures_db)}")

    # Grouping by model
    models = defaultdict(list)
    for fixture_id, info in fixtures_db.items():
        models[info["model"]].append(fixture_id)

    print("\n🔧 Models found:")
    for model, fixture_ids in models.items():
        print(f"   {model}: {len(fixture_ids)} fixtures")
        print(f"      IDs: {sorted(fixture_ids)}")

    # Grouping by light type
    print("\n💡 By Light Type:")
    by_type = defaultdict(list)
    for fixture_id, info in fixtures_db.items():
        by_type[info["light_type"]].append(fixture_id)

    for light_type, fixture_ids in by_type.items():
        print(f"   {light_type}: {len(fixture_ids)} fixtures")
        print(f"      IDs: {sorted(fixture_ids)}")

    # Channel analysis
    print("\n🎛️ Channel Analysis:")
    all_channels = set()
    for info in fixtures_db.values():
        all_channels.update(info["channels"])

    print(f"   Unique channels found: {sorted(all_channels)}")

    # Analyze naming patterns
    print("\n📝 Naming Patterns:")
    for fixture_id, info in fixtures_db.items():
        name = info["name"]
        model = info["model"]
        files_count = len(info["files"])
        channels_count = len(info["channels"])

        print(f"   ID {fixture_id}: '{name}' ({model})")
        print(f"      Files: {files_count}, Channels: {channels_count}")
        if info["channels"]:
            print(f"      Channels: {sorted(info['channels'])}")
        print(
            f"      Files: {info['files'][:3]}{'...' if len(info['files']) > 3 else ''}"
        )
        print()


def load_sauna_layout():
    """Načte layout sauny z fixtures.ini."""
    fixtures_ini = Path(
        "../auto-dmx/dmx/Infinit Maximus - new admin/3DView/fixtures.ini"
    )
    other_ini = Path("../auto-dmx/dmx/Infinit Maximus - new admin/3DView/other.ini")

    layout = {}

    print("\n🏗️ Loading sauna layout...")

    # Load fixtures.ini
    if fixtures_ini.exists():
        print(f"   Reading {fixtures_ini}")
        with open(fixtures_ini, encoding="utf-8") as f:
            content = f.read()
            # Parse fixture positions - simplified parsing
            for line in content.split("\n"):
                if "fixture" in line.lower() and "=" in line:
                    parts = line.split("=")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        layout[key] = value

    # Load other.ini
    if other_ini.exists():
        print(f"   Reading {other_ini}")
        with open(other_ini, encoding="utf-8") as f:
            content = f.read()
            for line in content.split("\n"):
                if "=" in line and ("x=" in line or "y=" in line or "z=" in line):
                    parts = line.split("=")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        layout[key] = value

    print(f"   Loaded {len(layout)} layout entries")
    return layout


def propose_systematic_structure(fixtures_db, layout):
    """Navrhne systematickou strukturu založenou na analýze."""
    print("\n🎯 Systematic Structure Proposal:")

    # Analyze current mess
    print("\n❌ Current Problems:")
    print("   • Inconsistent naming (MH_oven_blue vs LED_walls_1_red)")
    print("   • Missing fixtures (only some LED_walls have individual files)")
    print("   • No position-based organization")
    print("   • Manual creation = errors and gaps")

    # Propose solution
    print("\n✅ Proposed Systematic Structure:")
    print("   1. 🏗️  POSITION-BASED: Use 3D coordinates from layout")
    print("   2. 🎨 COLOR-BASED: Systematic color palette")
    print("   3. 🎛️  EFFECT-BASED: Systematic effect types")
    print("   4. 🤖 AUTO-GENERATED: Generate all combinations programmatically")

    print("\n📁 New Directory Structure:")
    print("   scenes/")
    print("   ├── generated/")
    print("   │   ├── single/          # Individual fixtures")
    print("   │   │   ├── led_wall_1/")
    print("   │   │   │   ├── static/  # Static colors")
    print("   │   │   │   │   ├── red.scex")
    print("   │   │   │   │   ├── blue.scex")
    print("   │   │   │   │   └── ...")
    print("   │   │   │   ├── dynamic/ # Dynamic effects")
    print("   │   │   │   │   ├── fade_red.scex")
    print("   │   │   │   │   ├── strobe_white.scex")
    print("   │   │   │   │   └── ...")
    print("   │   │   ├── led_wall_2/")
    print("   │   │   └── ...")
    print("   │   ├── groups/          # Grouped fixtures")
    print("   │   │   ├── walls_left/  # Left side walls")
    print("   │   │   ├── walls_right/")
    print("   │   │   ├── ceiling_center/")
    print("   │   │   └── ...")
    print("   │   └── patterns/        # Spatial patterns")
    print("   │       ├── circular/")
    print("   │       ├── wave/")
    print("   │       └── ...")

    print("\n🎨 Systematic Color Palette:")
    colors = [
        "red",
        "green",
        "blue",
        "yellow",
        "orange",
        "purple",
        "white_warm",
        "white_cool",
        "cyan",
        "magenta",
    ]
    for i, color in enumerate(colors):
        print(f"   {i + 1:2d}. {color}")

    print("\n⚡ Systematic Effect Types:")
    effects = [
        "static",
        "fade_in",
        "fade_out",
        "strobe_slow",
        "strobe_fast",
        "pulse",
        "chase",
        "sweep",
    ]
    for i, effect in enumerate(effects):
        print(f"   {i + 1:2d}. {effect}")


if __name__ == "__main__":
    # Analyze all scex files
    fixtures_db, light_types = analyze_all_scex_files()

    # Analyze patterns
    analyze_fixture_patterns(fixtures_db)

    # Load sauna layout
    layout = load_sauna_layout()

    # Propose systematic structure
    propose_systematic_structure(fixtures_db, layout)

    # Save analysis results
    analysis_results = {
        "fixtures_db": {
            k: {**v, "channels": list(v["channels"])} for k, v in fixtures_db.items()
        },
        "light_types": {k: dict(v) for k, v in light_types.items()},
        "layout": layout,
    }

    with open("scex_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)

    print("\n💾 Analysis saved to scex_analysis.json")

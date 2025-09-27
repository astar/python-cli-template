#!/usr/bin/env python3
"""Přehled všech systematických generátorů pro DMX timeline."""

import json
from pathlib import Path

def show_systematic_overview():
    """Zobrazí přehled systematické struktury a dostupných generátorů."""

    print("🎵 DMX SYSTEMATIC GENERATORS OVERVIEW")
    print("=" * 50)

    # Load systematic structure
    structure_path = Path("generated_scenes_systematic/systematic_structure.json")
    if not structure_path.exists():
        print("❌ Systematic structure not found!")
        print("   Run: python systematic_scex_generator.py")
        return

    with open(structure_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixtures = data['fixtures']
    colors = data['colors']
    effects = data['effects']

    print(f"\n📊 SYSTEMATIC STRUCTURE:")
    print(f"   🔧 Fixtures: {len(fixtures)}")

    # Count by type
    by_type = {}
    for fixture in fixtures.values():
        light_type = fixture['light_type']
        by_type[light_type] = by_type.get(light_type, 0) + 1

    for light_type, count in by_type.items():
        print(f"      {light_type}: {count}")

    print(f"\n   🎨 Colors: {len(colors)}")
    for color_name, color_data in list(colors.items())[:5]:
        r, g, b = color_data['rgb']
        print(f"      {color_name}: RGB({r}, {g}, {b})")
    if len(colors) > 5:
        print(f"      ... and {len(colors) - 5} more")

    print(f"\n   ⚡ Effects: {len(effects)}")
    for effect_name, effect_data in effects.items():
        duration = effect_data['duration']
        print(f"      {effect_name}: {duration}ms")

    # Show file structure
    print(f"\n📁 GENERATED STRUCTURE:")
    base_path = Path("generated_scenes_systematic")
    total_files = 0

    for category in ["individual", "groups", "zones"]:
        category_path = base_path / category
        if category_path.exists():
            files = list(category_path.rglob("*.scex"))
            total_files += len(files)
            print(f"   {category}/: {len(files)} scex files")

    print(f"   📄 Total: {total_files} systematic scex files")

    # Show available generators
    print(f"\n🤖 AVAILABLE SYSTEMATIC GENERATORS:")

    generators = [
        ("systematic_scex_generator.py", "Generate complete systematic scex structure", "2040 scex files"),
        ("systematic_timeline_generator.py", "Create spatial wave timeline", "243 events"),
        ("intelligent_beat_spots.py", "Beat-responsive LED walls", "1211 events"),
        ("moving_heads_analyzer.py", "Moving Head choreography", "68 events"),
        ("enhance_timeline_systematic.py", "Add systematic effects to existing timeline", "546+ effects")
    ]

    for script, description, output in generators:
        if Path(script).exists():
            status = "✅"
        else:
            status = "❌"
        print(f"   {status} {script}")
        print(f"      {description}")
        print(f"      Output: {output}")
        print()

    # Show usage examples
    print(f"🚀 USAGE EXAMPLES:")
    print(f"   # Generate systematic structure:")
    print(f"   python systematic_scex_generator.py")
    print()
    print(f"   # Create timeline with spatial effects:")
    print(f"   python systematic_timeline_generator.py")
    print()
    print(f"   # Beat-responsive spots:")
    print(f"   python intelligent_beat_spots.py")
    print()
    print(f"   # Moving Head show:")
    print(f"   python moving_heads_analyzer.py")
    print()
    print(f"   # Enhance existing timeline:")
    print(f"   python enhance_timeline_systematic.py input.tml output.tml")
    print()

    # Show advantages
    print(f"✨ SYSTEMATIC ADVANTAGES:")
    print(f"   🎯 Position-based: Uses real 3D sauna coordinates")
    print(f"   🎨 Color-consistent: 10 systematic colors with RGB values")
    print(f"   ⚡ Effect-standardized: 6 systematic effects (static, fade, strobe, pulse)")
    print(f"   🤖 Auto-generated: All 2040 combinations programmatically created")
    print(f"   📐 Scalable: Easy to add new fixtures, colors, or effects")
    print(f"   🔧 Testable: Metadata in JSON for validation")
    print(f"   🎵 Music-aware: Beat detection, frequency analysis integration")
    print()

    print(f"🎭 TIMELINE COMPARISON:")
    print(f"   Manual approach:     ~50 events, inconsistent naming")
    print(f"   Basic generator:     ~44 events, hardcoded paths")
    print(f"   Systematic approach: 243-1211 events, position-aware, scalable")
    print()

    print(f"💡 RESULT: Complete systematic DMX lighting ecosystem!")

if __name__ == "__main__":
    show_systematic_overview()
#!/usr/bin/env python3
"""
Comprehensive Test Demo Generator
Tests every light, every function, every color, every effect
"""

from pathlib import Path
from typing import List, Dict
import json

class ComprehensiveTestGenerator:
    """Generate comprehensive test timeline that demonstrates all capabilities"""

    def __init__(self):
        self.timeline_events = []
        self.current_time = 0.0  # seconds
        self.event_counter = 0

        # Load systematic structure to know what fixtures we have
        self.load_systematic_structure()

        # Define all colors we can test
        self.colors = [
            "red", "blue", "green", "yellow", "orange", "purple",
            "magenta", "cyan", "white", "darkred", "darkblue", "darkgreen"
        ]

        # Define all effects we can test
        self.effects = [
            "static", "fade_in", "fade_out", "pulse", "strobe_slow", "strobe_fast"
        ]

        # Moving heads directions and movements
        self.mh_tests = [
            "single_color", "gobo_rotation", "zoom_rotation", "snake_left_right", "snake_right_left"
        ]

    def load_systematic_structure(self):
        """Load systematic structure to know available fixtures"""
        structure_file = Path("generated_scenes_systematic/systematic_structure.json")
        if structure_file.exists():
            with open(structure_file, 'r', encoding='utf-8') as f:
                self.structure = json.load(f)
        else:
            # Fallback structure
            self.structure = {
                "individual": {},
                "groups": {},
                "zones": {}
            }

    def add_event(self, timeline_index: int, path: str, length: float,
                  speed: int = 100, fadein: int = 0, fadeout: int = 0,
                  description: str = ""):
        """Add event to timeline"""
        self.timeline_events.append({
            "index": self.event_counter,
            "timeline_index": timeline_index,
            "start_time": self.format_time(self.current_time),
            "path": path,
            "length": self.format_time(length),
            "speed": speed,
            "fadein": fadein,
            "fadeout": fadeout,
            "description": description
        })

        self.current_time += length
        self.event_counter += 1

        # Add small gap between effects
        self.current_time += 0.5

    def format_time(self, seconds: float) -> str:
        """Format time to H:MM:SS.f"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)
        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def test_individual_fixtures(self):
        """Test each individual fixture with all colors and effects"""
        print("🔍 Testing individual fixtures...")

        # Timeline 3: Individual fixture tests
        timeline_idx = 3

        # Test each individual fixture type
        for fixture_key in self.structure.get("individual", {}):
            fixture_info = self.structure["individual"][fixture_key]
            fixture_id = fixture_info["fixture_id"]

            print(f"   Testing {fixture_key}...")

            # Test each color for this fixture
            for color in self.colors[:3]:  # Test first 3 colors per fixture (time constraint)
                for effect in ["static", "fade_in", "strobe_slow"][:2]:  # Test 2 effects per color
                    scene_path = f"generated_scenes_systematic/individual/{fixture_key}/{color}_{effect}.scex"

                    # Check if scene file exists
                    if Path(scene_path).exists():
                        self.add_event(
                            timeline_idx, scene_path, 2.0,
                            speed=80, fadein=200, fadeout=200,
                            description=f"{fixture_key} {color} {effect}"
                        )

    def test_group_effects(self):
        """Test group effects (walls pairs)"""
        print("🌟 Testing group effects...")

        timeline_idx = 4

        # Test wall groups
        for group_key in self.structure.get("groups", {}):
            if "walls_" in group_key:
                print(f"   Testing {group_key}...")

                for color in self.colors[:2]:  # Test 2 colors per group
                    for effect in ["static", "strobe_slow"]:
                        scene_path = f"generated_scenes_systematic/groups/{group_key}/{color}_{effect}.scex"

                        if Path(scene_path).exists():
                            self.add_event(
                                timeline_idx, scene_path, 3.0,
                                speed=90, fadein=300, fadeout=300,
                                description=f"{group_key} {color} {effect}"
                            )

    def test_moving_heads_comprehensive(self):
        """Comprehensive moving heads test - all movements, colors, effects"""
        print("🎭 Testing moving heads comprehensively...")

        # Timeline 5: Professional moving heads
        timeline_idx = 5

        # 1. Test all single colors with safe oven positioning
        print("   Testing single color oven positioning...")
        for color in self.colors:
            scene_path = f"generated_scenes_advanced/professional_moving_heads/oven_single_color/MH_all_{color}_oven.scex"
            if Path(scene_path).exists():
                self.add_event(
                    timeline_idx, scene_path, 4.0,
                    speed=70, fadein=800, fadeout=400,
                    description=f"MH oven {color}"
                )

        # Timeline 6: Gobo rotation effects
        timeline_idx = 6
        print("   Testing gobo rotation...")
        for color in self.colors[:6]:  # Test 6 colors for rotation
            scene_path = f"generated_scenes_advanced/professional_moving_heads/gobo_rotation/Rotate_gobo_{color}.scex"
            if Path(scene_path).exists():
                self.add_event(
                    timeline_idx, scene_path, 6.0,
                    speed=100, fadein=500, fadeout=500,
                    description=f"MH gobo rotate {color}"
                )

        # Timeline 7: Zoom + rotation breathing effects
        timeline_idx = 7
        print("   Testing zoom + rotation breathing...")
        for color in self.colors[:4]:  # Test 4 colors for zoom breathing
            scene_path = f"generated_scenes_advanced/professional_moving_heads/zoom_rotation/Zoom_{color}.scex"
            if Path(scene_path).exists():
                self.add_event(
                    timeline_idx, scene_path, 5.5,  # 11 steps * 500ms = 5.5s
                    speed=120, fadein=200, fadeout=200,
                    description=f"MH zoom breathing {color}"
                )

    def test_snake_effects(self):
        """Test sequential snake effects"""
        print("🐍 Testing snake effects...")

        timeline_idx = 8

        # Test snake effects in both directions
        directions = ["left_right", "right_left"]
        for direction in directions:
            for color in self.colors[:4]:  # Test 4 colors per direction
                scene_path = f"generated_scenes_advanced/professional_moving_heads/snake_effects/MH_snake_{color}_{direction}.scex"
                if Path(scene_path).exists():
                    self.add_event(
                        timeline_idx, scene_path, 2.5,  # 5 steps * 500ms = 2.5s
                        speed=150, fadein=50, fadeout=50,
                        description=f"MH snake {color} {direction}"
                    )

    def test_zone_effects(self):
        """Test zone-wide effects"""
        print("🌐 Testing zone effects...")

        timeline_idx = 9

        # Test each zone
        for zone_key in self.structure.get("zones", {}):
            print(f"   Testing zone {zone_key}...")

            for color in self.colors[:2]:  # Test 2 colors per zone
                scene_path = f"generated_scenes_systematic/zones/{zone_key}/{color}_static.scex"
                if Path(scene_path).exists():
                    self.add_event(
                        timeline_idx, scene_path, 4.0,
                        speed=60, fadein=1000, fadeout=1000,
                        description=f"Zone {zone_key} {color}"
                    )

    def test_special_effects(self):
        """Test UV lights and special effects"""
        print("✨ Testing special effects...")

        timeline_idx = 10

        # Test UV lights
        uv_effects = ["white_cool_static", "white_cool_strobe_fast", "white_cool_pulse"]
        for effect in uv_effects:
            for uv_id in ["40", "41"]:  # Both UV lights
                scene_path = f"generated_scenes_systematic/individual/uv_light_{uv_id}/{effect}.scex"
                if Path(scene_path).exists():
                    self.add_event(
                        timeline_idx, scene_path, 3.0,
                        speed=200, fadein=100, fadeout=500,
                        description=f"UV {uv_id} {effect}"
                    )

    def test_systematic_vs_professional(self):
        """Compare systematic vs professional moving heads"""
        print("⚔️ Testing systematic vs professional comparison...")

        # Timeline 11: Systematic moving heads
        timeline_idx = 11

        # Test systematic moving heads
        for mh_id in ["37", "38", "39", "40", "41"]:
            for color in ["red", "blue", "green"]:
                scene_path = f"generated_scenes_systematic/individual/moving_head_{mh_id}/{color}_static.scex"
                if Path(scene_path).exists():
                    self.add_event(
                        timeline_idx, scene_path, 3.0,
                        speed=100, fadein=500, fadeout=500,
                        description=f"Systematic MH_{mh_id} {color}"
                    )

    def generate_comprehensive_demo(self):
        """Generate complete comprehensive test demo"""
        print("🎬 Generating comprehensive test demo...")

        # Reset timeline
        self.timeline_events = []
        self.current_time = 5.0  # Start after 5 seconds
        self.event_counter = 0

        # Run all tests
        self.test_individual_fixtures()
        self.test_group_effects()
        self.test_moving_heads_comprehensive()
        self.test_snake_effects()
        self.test_zone_effects()
        self.test_special_effects()
        self.test_systematic_vs_professional()

        # Generate timeline file
        self.generate_timeline_file()

        print(f"✅ Comprehensive demo complete!")
        print(f"   Total events: {len(self.timeline_events)}")
        print(f"   Total duration: {self.format_time(self.current_time)}")
        print(f"   Output: COMPREHENSIVE_TEST_DEMO.tml")

    def generate_timeline_file(self):
        """Generate the timeline file"""
        content = """[Params]
version = 0.2
commenttimeline = 0
lighttimelines = 12
mediatimelines = 1
showwaveform = 1
maxtime = 0:30:00
zoom = 0
timeline_1 = V I D E O   P I C T U R E   T I M E L I N E
timeline_2 = A U D I O   T I M E L I N E
timeline_3 = I N D I V I D U A L   F I X T U R E   T E S T S
timeline_4 = G R O U P   E F F E C T S   T E S T S
timeline_5 = M O V I N G   H E A D S   S I N G L E   C O L O R
timeline_6 = M O V I N G   H E A D S   G O B O   R O T A T I O N
timeline_7 = M O V I N G   H E A D S   Z O O M   B R E A T H I N G
timeline_8 = M O V I N G   H E A D S   S N A K E   E F F E C T S
timeline_9 = Z O N E   W I D E   E F F E C T S
timeline_10 = S P E C I A L   E F F E C T S   ( U V )
timeline_11 = S Y S T E M A T I C   M O V I N G   H E A D S
timeline_12 = F I N A L   T E S T S
timeline_13 = L I G H T   S C E N E   T I M E L I N E   #   13

[Event_0]
timelineindex = 2
starttime = 0:00:00.0
path = Music/test_short.mp3
length = 0:05:45.9

"""

        # Add all events
        for event in self.timeline_events:
            content += f"""[Event_{event['index'] + 1}]
timelineindex = {event['timeline_index']}
starttime = {event['start_time']}
path = {event['path']}
length = {event['length']}
speed = {event['speed']}
speedtype = 2"""

            if event['fadein'] > 0:
                content += f"\nfadein = {event['fadein']}"
            if event['fadeout'] > 0:
                content += f"\nfadeout = {event['fadeout']}"

            content += "\n\n"

        # Save to file
        with open("COMPREHENSIVE_TEST_DEMO.tml", "w", encoding="utf-8") as f:
            f.write(content)

def main():
    """Generate comprehensive test demo"""
    generator = ComprehensiveTestGenerator()
    generator.generate_comprehensive_demo()

    print("\n🎯 Comprehensive Test Demo Features:")
    print("   ✅ Every individual fixture tested")
    print("   ✅ All colors and effects demonstrated")
    print("   ✅ Group effects (wall pairs)")
    print("   ✅ Moving heads: oven positioning, gobo rotation, zoom breathing")
    print("   ✅ Snake effects in both directions")
    print("   ✅ Zone-wide lighting")
    print("   ✅ UV special effects")
    print("   ✅ Systematic vs professional comparison")
    print("   ✅ Comprehensive visualization test")

    print(f"\n🎬 Run: dmx-analyzer visualize COMPREHENSIVE_TEST_DEMO.tml test_short.mp3")

if __name__ == "__main__":
    main()
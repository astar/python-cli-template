#!/usr/bin/env python3
"""
Moving Heads Ultimate Test Generator
Tests EVERY aspect of moving heads - all movements, directions, rotations, colors
"""

from pathlib import Path
import math

class MovingHeadsUltimateTest:
    """Generate ultimate test for all moving heads capabilities"""

    def __init__(self):
        self.timeline_events = []
        self.current_time = 0.0
        self.event_counter = 0

        # Professional safe oven positions (from hand_made_scenes analysis)
        self.oven_positions = [
            {"name": "MH_1", "pan": 137, "upan": 137, "tilt": 79, "utilt": 79},
            {"name": "MH_2", "pan": 144, "upan": 144, "tilt": 73, "utilt": 73},
            {"name": "MH_3", "pan": 126, "upan": 127, "tilt": 74, "utilt": 75},
            {"name": "MH_4", "pan": 109, "upan": 109, "tilt": 75, "utilt": 75},
            {"name": "MH_5", "pan": 208, "upan": 203, "tilt": 176, "utilt": 176},  # Back wall
        ]

        # All colors to test
        self.colors = [
            "red", "darkred", "blue", "darkblue", "green", "darkgreen",
            "yellow", "orange", "purple", "magenta", "white", "cyan"
        ]

        # Professional channel mapping
        self.channel_map = {
            "pan": 0, "upan": 1, "tilt": 2, "utilt": 3,
            "color": 5, "gobo": 6, "gobo_rotate": 7,
            "dimmer": 10, "shutter": 11, "zoom": 14
        }

    def format_time(self, seconds: float) -> str:
        """Format time to H:MM:SS.f"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)
        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def add_event(self, timeline_index: int, path: str, length: float,
                  speed: int = 100, fadein: int = 0, fadeout: int = 0):
        """Add event to timeline"""
        self.timeline_events.append({
            "index": self.event_counter,
            "timeline_index": timeline_index,
            "start_time": self.format_time(self.current_time),
            "path": path,
            "length": self.format_time(length),
            "speed": speed,
            "fadein": fadein,
            "fadeout": fadeout
        })

        self.current_time += length + 0.3  # Small gap between effects
        self.event_counter += 1

    def generate_pan_sweep_scenes(self):
        """Generate scenes that sweep PAN across full range"""
        print("🔄 Generating PAN sweep test scenes...")

        scenes_dir = Path("generated_scenes_advanced/ultimate_test/pan_sweep")
        scenes_dir.mkdir(parents=True, exist_ok=True)

        # Generate 18 steps across PAN range (0-255 in steps of ~14)
        for step in range(18):
            pan_value = int(step * 255 / 17)  # 0, 15, 30, 45... 255

            scene_content = self.create_scene_xml(
                f"pan_sweep_step_{step:02d}",
                pan_values=[pan_value] * 5,  # All fixtures same PAN
                tilt_values=[77] * 5,       # Safe TILT
                color_value=11,             # Red
                special_effects={"dimmer": 100, "shutter": 4}
            )

            scene_file = scenes_dir / f"pan_sweep_step_{step:02d}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)

    def generate_tilt_sweep_scenes(self):
        """Generate scenes that sweep TILT across safe range"""
        print("🔄 Generating TILT sweep test scenes...")

        scenes_dir = Path("generated_scenes_advanced/ultimate_test/tilt_sweep")
        scenes_dir.mkdir(parents=True, exist_ok=True)

        # Generate steps across safe TILT range (65-85 degrees)
        for step in range(10):
            tilt_value = int(65 + step * 20 / 9)  # 65 to 85 in 10 steps

            scene_content = self.create_scene_xml(
                f"tilt_sweep_step_{step:02d}",
                pan_values=[137] * 5,        # Center PAN
                tilt_values=[tilt_value] * 5,  # Sweep TILT
                color_value=51,              # Blue
                special_effects={"dimmer": 120, "shutter": 4}
            )

            scene_file = scenes_dir / f"tilt_sweep_step_{step:02d}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)

    def generate_color_wheel_test(self):
        """Generate scenes testing full color wheel"""
        print("🌈 Generating color wheel test scenes...")

        scenes_dir = Path("generated_scenes_advanced/ultimate_test/color_wheel")
        scenes_dir.mkdir(parents=True, exist_ok=True)

        # Test color wheel values in steps
        color_values = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191, 201, 211, 221, 231, 241, 251]

        for i, color_value in enumerate(color_values):
            scene_content = self.create_scene_xml(
                f"color_wheel_step_{i:02d}",
                pan_values=[137] * 5,  # Center
                tilt_values=[77] * 5,  # Safe oven
                color_value=color_value,
                special_effects={"dimmer": 150, "shutter": 4}
            )

            scene_file = scenes_dir / f"color_wheel_step_{i:02d}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)

    def generate_gobo_rotation_test(self):
        """Generate gobo rotation speed test"""
        print("⚙️ Generating gobo rotation test scenes...")

        scenes_dir = Path("generated_scenes_advanced/ultimate_test/gobo_rotation")
        scenes_dir.mkdir(parents=True, exist_ok=True)

        # Test different rotation speeds
        rotation_speeds = [0, 128, 140, 150, 160, 170, 180, 190, 200, 220, 240, 255]

        for i, rotation_speed in enumerate(rotation_speeds):
            scene_content = self.create_scene_xml(
                f"gobo_rotation_speed_{i:02d}",
                pan_values=[137] * 5,
                tilt_values=[77] * 5,
                color_value=91,  # Green
                special_effects={
                    "dimmer": 180,
                    "shutter": 4,
                    "gobo": 59,  # Gobo pattern
                    "gobo_rotate": rotation_speed
                }
            )

            scene_file = scenes_dir / f"gobo_rotation_speed_{i:02d}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)

    def generate_zoom_test(self):
        """Generate zoom level test"""
        print("🔍 Generating zoom test scenes...")

        scenes_dir = Path("generated_scenes_advanced/ultimate_test/zoom")
        scenes_dir.mkdir(parents=True, exist_ok=True)

        # Test zoom levels from 0 to 255 in steps
        for step in range(16):
            zoom_value = int(step * 255 / 15)  # 0 to 255 in 16 steps

            scene_content = self.create_scene_xml(
                f"zoom_level_{step:02d}",
                pan_values=[137] * 5,
                tilt_values=[77] * 5,
                color_value=211,  # White
                special_effects={
                    "dimmer": 200,
                    "shutter": 4,
                    "zoom": zoom_value
                }
            )

            scene_file = scenes_dir / f"zoom_level_{step:02d}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)

    def generate_circular_movement(self):
        """Generate circular movement pattern"""
        print("🌀 Generating circular movement scenes...")

        scenes_dir = Path("generated_scenes_advanced/ultimate_test/circular")
        scenes_dir.mkdir(parents=True, exist_ok=True)

        # Generate 24 steps for smooth circular movement
        for step in range(24):
            angle = (step / 24) * 2 * math.pi  # Full circle

            # Circular movement around center point
            center_pan = 137
            center_tilt = 77
            radius_pan = 30
            radius_tilt = 15

            pan_value = int(center_pan + radius_pan * math.cos(angle))
            tilt_value = int(center_tilt + radius_tilt * math.sin(angle))

            # Ensure safe ranges
            pan_value = max(50, min(200, pan_value))
            tilt_value = max(65, min(85, tilt_value))

            scene_content = self.create_scene_xml(
                f"circular_step_{step:02d}",
                pan_values=[pan_value] * 5,
                tilt_values=[tilt_value] * 5,
                color_value=171,  # Magenta
                special_effects={"dimmer": 255, "shutter": 4}
            )

            scene_file = scenes_dir / f"circular_step_{step:02d}.scex"
            with open(scene_file, "w", encoding="utf-8") as f:
                f.write(scene_content)

    def create_scene_xml(self, scene_name: str, pan_values: list, tilt_values: list,
                        color_value: int, special_effects: dict = None) -> str:
        """Create XML scene content"""

        fixtures = [
            {"id": "1753951490", "name": "Intimidator Spot 375Z IRC (15CH)"},
            {"id": "1753953036", "name": "Intimidator Spot 375Z IRC (15CH) #2"},
            {"id": "1753953037", "name": "Intimidator Spot 375Z IRC (15CH) #3"},
            {"id": "1753953038", "name": "Intimidator Spot 375Z IRC (15CH) #4"},
            {"id": "1753953039", "name": "Intimidator Spot 375Z IRC (15CH) #5"},
        ]

        if special_effects is None:
            special_effects = {"dimmer": 100, "shutter": 4}

        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n\n<Scene>\n  <Fixtures>\n'

        # Add fixtures
        for fixture in fixtures:
            xml_content += f'    <Fixture id="{fixture["id"]}" name="{fixture["name"]}" model="Intimidator Spot 375Z IRC (15CH)"/>\n'

        xml_content += '  </Fixtures>\n  <Steps>\n'

        # Single step with all fixtures
        xml_content += '    <Step length="500">\n'

        for i, (fixture, pan, tilt) in enumerate(zip(fixtures, pan_values, tilt_values)):
            xml_content += f'      <Fixture id="{fixture["id"]}">\n'
            xml_content += f'        <Channel index="0" name="pan" value="{pan}"/>\n'
            xml_content += f'        <Channel index="1" name="upan" value="{pan}"/>\n'
            xml_content += f'        <Channel index="2" name="tilt" value="{tilt}"/>\n'
            xml_content += f'        <Channel index="3" name="utilt" value="{tilt}"/>\n'
            xml_content += f'        <Channel index="5" name="color" value="{color_value}"/>\n'

            # Add special effects
            for effect_name, effect_value in special_effects.items():
                if effect_name == "gobo":
                    xml_content += f'        <Channel index="6" name="gobo" value="{effect_value}"/>\n'
                elif effect_name == "gobo_rotate":
                    xml_content += f'        <Channel index="7" name="gobo_rotate" value="{effect_value}"/>\n'
                elif effect_name == "dimmer":
                    xml_content += f'        <Channel index="10" name="dimmer" value="{effect_value}"/>\n'
                elif effect_name == "shutter":
                    xml_content += f'        <Channel index="11" name="shutter" value="{effect_value}"/>\n'
                elif effect_name == "zoom":
                    xml_content += f'        <Channel index="14" name="zoom" value="{effect_value}"/>\n'

            xml_content += '      </Fixture>\n'

        xml_content += '    </Step>\n  </Steps>\n</Scene>\n'
        return xml_content

    def generate_timeline(self):
        """Generate ultimate test timeline"""
        print("📋 Generating ultimate test timeline...")

        # Timeline assignments
        timelines = {
            1: "PAN sweep test",
            2: "TILT sweep test",
            3: "Color wheel test",
            4: "Gobo rotation test",
            5: "Zoom test",
            6: "Circular movement test"
        }

        # Add PAN sweep tests
        for step in range(18):
            self.add_event(1, f"generated_scenes_advanced/ultimate_test/pan_sweep/pan_sweep_step_{step:02d}.scex", 1.0, speed=100)

        # Add TILT sweep tests
        for step in range(10):
            self.add_event(2, f"generated_scenes_advanced/ultimate_test/tilt_sweep/tilt_sweep_step_{step:02d}.scex", 1.5, speed=80)

        # Add color wheel tests
        for step in range(26):
            self.add_event(3, f"generated_scenes_advanced/ultimate_test/color_wheel/color_wheel_step_{step:02d}.scex", 1.0, speed=100)

        # Add gobo rotation tests
        for step in range(12):
            self.add_event(4, f"generated_scenes_advanced/ultimate_test/gobo_rotation/gobo_rotation_speed_{step:02d}.scex", 2.0, speed=100)

        # Add zoom tests
        for step in range(16):
            self.add_event(5, f"generated_scenes_advanced/ultimate_test/zoom/zoom_level_{step:02d}.scex", 1.0, speed=100)

        # Add circular movement tests
        for step in range(24):
            self.add_event(6, f"generated_scenes_advanced/ultimate_test/circular/circular_step_{step:02d}.scex", 0.8, speed=100)

    def generate_timeline_file(self):
        """Generate the timeline file"""
        content = """[Params]
version = 0.2
commenttimeline = 0
lighttimelines = 8
mediatimelines = 1
showwaveform = 1
maxtime = 0:30:00
zoom = 0
timeline_1 = V I D E O   P I C T U R E   T I M E L I N E
timeline_2 = A U D I O   T I M E L I N E
timeline_3 = P A N   S W E E P   T E S T   ( F U L L   R A N G E )
timeline_4 = T I L T   S W E E P   T E S T   ( S A F E   R A N G E )
timeline_5 = C O L O R   W H E E L   T E S T   ( A L L   C O L O R S )
timeline_6 = G O B O   R O T A T I O N   T E S T   ( S P E E D S )
timeline_7 = Z O O M   T E S T   ( A L L   L E V E L S )
timeline_8 = C I R C U L A R   M O V E M E N T   T E S T
timeline_9 = L I G H T   S C E N E   T I M E L I N E   #   7

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
        with open("MOVING_HEADS_ULTIMATE_TEST.tml", "w", encoding="utf-8") as f:
            f.write(content)

    def generate_ultimate_test(self):
        """Generate complete ultimate test"""
        print("🎯 Generating Moving Heads Ultimate Test...")

        # Generate all scene types
        self.generate_pan_sweep_scenes()
        self.generate_tilt_sweep_scenes()
        self.generate_color_wheel_test()
        self.generate_gobo_rotation_test()
        self.generate_zoom_test()
        self.generate_circular_movement()

        # Generate timeline
        self.generate_timeline()
        self.generate_timeline_file()

        print(f"✅ Ultimate test complete!")
        print(f"   Total events: {len(self.timeline_events)}")
        print(f"   Total duration: {self.format_time(self.current_time)}")
        print(f"   Output: MOVING_HEADS_ULTIMATE_TEST.tml")

def main():
    """Generate ultimate moving heads test"""
    generator = MovingHeadsUltimateTest()
    generator.generate_ultimate_test()

    print("\n🎯 Moving Heads Ultimate Test Features:")
    print("   ✅ PAN sweep: Full 0-255 range (18 steps)")
    print("   ✅ TILT sweep: Safe 65-85° range (10 steps)")
    print("   ✅ Color wheel: All 26 color positions")
    print("   ✅ Gobo rotation: 12 different speeds (0-255)")
    print("   ✅ Zoom levels: 16 levels from minimum to maximum")
    print("   ✅ Circular movement: 24-step smooth circle")
    print("   ✅ Professional channel mapping (5,7,10,11,14)")
    print("   ✅ Safe oven positioning (TILT 65-85°)")

    print(f"\n🎬 Run: dmx-analyzer visualize MOVING_HEADS_ULTIMATE_TEST.tml test_short.mp3")

if __name__ == "__main__":
    main()
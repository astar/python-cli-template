#!/usr/bin/env python3
"""
Simple Lights Test Generator - Direct Version
Turn on each light for 0.5 seconds, each with different color, one by one
"""

from pathlib import Path

class SimpleLightsTestDirect:
    """Generate simple test - one light at a time, direct folder scan"""

    def __init__(self):
        self.timeline_events = []
        self.current_time = 2.0  # Start after 2 seconds
        self.event_counter = 0

        # Colors to cycle through - each light gets different color
        self.colors = [
            "red", "blue", "green", "yellow", "orange", "purple",
            "magenta", "cyan", "white", "darkred", "darkblue", "darkgreen"
        ]

        self.color_index = 0

    def get_next_color(self):
        """Get next color and advance counter"""
        color = self.colors[self.color_index % len(self.colors)]
        self.color_index += 1
        return color

    def format_time(self, seconds: float) -> str:
        """Format time to H:MM:SS.f"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)
        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def add_event(self, timeline_index: int, path: str, length: float = 0.5, description: str = ""):
        """Add event to timeline"""
        self.timeline_events.append({
            "index": self.event_counter,
            "timeline_index": timeline_index,
            "start_time": self.format_time(self.current_time),
            "path": path,
            "length": self.format_time(length),
            "speed": 100,
            "description": description
        })

        self.current_time += length + 0.2  # 0.5s light + 0.2s gap = 0.7s per light
        self.event_counter += 1

    def scan_all_fixtures(self):
        """Scan individual folder to find all fixtures"""
        individual_dir = Path("generated_scenes_systematic/individual")

        if not individual_dir.exists():
            print("❌ Individual scenes directory not found!")
            return []

        # Get all fixture directories and sort them
        fixtures = []
        for fixture_dir in individual_dir.iterdir():
            if fixture_dir.is_dir():
                fixtures.append(fixture_dir.name)

        fixtures.sort()  # Sort alphabetically
        return fixtures

    def test_all_lights_sequentially(self):
        """Test each light one by one"""
        print("💡 Testing all lights sequentially...")

        fixtures = self.scan_all_fixtures()
        print(f"   Found {len(fixtures)} fixtures")

        timeline_index = 3  # Use timeline 3 for all tests

        for fixture_name in fixtures:
            color = self.get_next_color()

            # Look for a static scene for this fixture and color
            scene_path = f"generated_scenes_systematic/individual/{fixture_name}/{color}_static.scex"

            # Check if file exists
            if Path(scene_path).exists():
                self.add_event(
                    timeline_index,
                    scene_path,
                    0.5,  # 0.5 seconds
                    f"{fixture_name} {color}"
                )
                print(f"   ✅ {fixture_name:20} -> {color}")
            else:
                # Try to find any static scene for this fixture
                fixture_dir = Path(f"generated_scenes_systematic/individual/{fixture_name}")
                static_scenes = list(fixture_dir.glob("*_static.scex"))

                if static_scenes:
                    # Use first available static scene
                    scene_path = str(static_scenes[0])
                    scene_color = static_scenes[0].stem.replace("_static", "")

                    self.add_event(
                        timeline_index,
                        scene_path,
                        0.5,
                        f"{fixture_name} {scene_color}"
                    )
                    print(f"   ✅ {fixture_name:20} -> {scene_color} (fallback)")
                else:
                    print(f"   ❌ No static scene found for: {fixture_name}")

    def generate_timeline_file(self):
        """Generate the timeline file"""
        content = f"""[Params]
version = 0.2
commenttimeline = 0
lighttimelines = 5
mediatimelines = 1
showwaveform = 1
maxtime = 0:30:00
zoom = 0
timeline_1 = V I D E O   P I C T U R E   T I M E L I N E
timeline_2 = A U D I O   T I M E L I N E
timeline_3 = S I M P L E   L I G H T S   T E S T   ( O N E   B Y   O N E )
timeline_4 = L I G H T   S C E N E   T I M E L I N E   #   4
timeline_5 = L I G H T   S C E N E   T I M E L I N E   #   5
timeline_6 = L I G H T   S C E N E   T I M E L I N E   #   6

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
speedtype = 2

"""

        # Save to file
        with open("SIMPLE_LIGHTS_TEST.tml", "w", encoding="utf-8") as f:
            f.write(content)

    def generate_simple_test(self):
        """Generate simple sequential lights test"""
        print("🔍 Generating Simple Lights Test...")
        print("   Each light will turn on for 0.5 seconds with different color")
        print("   0.2 second gap between lights for clear separation")
        print()

        # Test all lights
        self.test_all_lights_sequentially()

        # Generate timeline
        self.generate_timeline_file()

        print()
        print(f"✅ Simple lights test complete!")
        print(f"   Total lights tested: {len(self.timeline_events)}")
        print(f"   Total duration: {self.format_time(self.current_time)}")
        print(f"   Output: SIMPLE_LIGHTS_TEST.tml")
        print()
        print(f"🎬 Run: dmx-analyzer visualize SIMPLE_LIGHTS_TEST.tml test_short.mp3")
        print()
        print("   📝 What you'll see:")
        print("   - Each light turns on for exactly 0.5 seconds")
        print("   - Each light has a different color for easy identification")
        print("   - Lights are tested in alphabetical order")
        print("   - Short pause between each light")
        print("   - Perfect for checking every single light works!")

def main():
    """Generate simple lights test"""
    generator = SimpleLightsTestDirect()
    generator.generate_simple_test()

if __name__ == "__main__":
    main()
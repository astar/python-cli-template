#!/usr/bin/env python3
"""
Simple Lights Test Generator
Turn on each light for 0.5 seconds, each with different color, one by one
"""

import json
from pathlib import Path

class SimpleLightsTest:
    """Generate simple test - one light at a time"""

    def __init__(self):
        self.timeline_events = []
        self.current_time = 2.0  # Start after 2 seconds
        self.event_counter = 0

        # Load systematic structure to know what fixtures we have
        self.load_systematic_structure()

        # Colors to cycle through - each light gets different color
        self.colors = [
            "red", "blue", "green", "yellow", "orange", "purple",
            "magenta", "cyan", "white", "darkred", "darkblue", "darkgreen"
        ]

        # We'll cycle through colors
        self.color_index = 0

    def load_systematic_structure(self):
        """Load systematic structure to know available fixtures"""
        structure_file = Path("generated_scenes_systematic/systematic_structure.json")
        if structure_file.exists():
            with open(structure_file, 'r', encoding='utf-8') as f:
                self.structure = json.load(f)
        else:
            print("❌ Systematic structure not found. Run systematic generator first.")
            self.structure = {"individual": {}}

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

        self.current_time += length + 0.2  # 0.5s light + 0.2s gap
        self.event_counter += 1

    def test_all_lights_sequentially(self):
        """Test each light one by one"""
        print("💡 Testing all lights sequentially...")

        # Get all individual fixtures and sort them for consistent order
        individual_fixtures = list(self.structure.get("individual", {}).items())
        individual_fixtures.sort()  # Sort alphabetically

        timeline_index = 3  # Use timeline 3 for all tests

        for fixture_key, fixture_info in individual_fixtures:
            color = self.get_next_color()

            # Try to find a static scene for this fixture and color
            scene_path = f"generated_scenes_systematic/individual/{fixture_key}/{color}_static.scex"

            # Check if file exists
            if Path(scene_path).exists():
                self.add_event(
                    timeline_index,
                    scene_path,
                    0.5,  # 0.5 seconds
                    f"{fixture_key} {color}"
                )
                print(f"   ✅ {fixture_key} -> {color}")
            else:
                print(f"   ❌ Scene not found: {scene_path}")

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
        print("   Watch as each light turns on one by one!")
        print("   Each light has a different color so you can easily identify it.")

def main():
    """Generate simple lights test"""
    generator = SimpleLightsTest()
    generator.generate_simple_test()

if __name__ == "__main__":
    main()
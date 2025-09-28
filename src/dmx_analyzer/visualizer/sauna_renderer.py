"""2D renderer pro vizualizaci sauny a světel."""

from __future__ import annotations

import math

import pygame

from ..logging import get_logger

logger = get_logger(__name__)


class LightFixture:
    """Reprezentace světelného zařízení."""

    def __init__(
        self, name: str, position: tuple[int, int], fixture_type: str, size: int = 20
    ):
        self.name = name
        self.position = position
        self.fixture_type = fixture_type
        self.size = size

        # Light state
        self.is_on = False
        self.color = (0, 0, 0)  # RGB
        self.intensity = 0.0  # 0.0 - 1.0
        self.effect = None  # strobe, pulse, fade, etc.
        self.effect_progress = 0.0

        # Animation
        self.target_color = (0, 0, 0)
        self.fade_start_time = 0
        self.fade_duration = 0

        # Moving heads specific properties
        self.pan = 128  # 0-255 horizontal position (128 = center)
        self.tilt = 128  # 0-255 vertical position (128 = center)
        self.gobo = 0   # 0-255 gobo pattern
        self.prism = 0  # 0-255 prism effects
        self.focus = 128  # 0-255 focus setting
        self.shutter = 32  # 0-255 shutter/strobe

        # Calculated beam direction for visualization
        self.beam_angle = 0.0  # Horizontal angle in radians
        self.beam_elevation = 0.0  # Vertical angle (affects beam length)

    def set_color(
        self, color: tuple[int, int, int], intensity: float = 1.0, effect: str = None
    ) -> None:
        """Nastaví barvu a efekt světla."""
        self.target_color = color
        self.color = color  # Nastaví okamžitě aktuální barvu
        self.intensity = max(0.0, min(1.0, intensity))
        self.effect = effect
        self.is_on = intensity > 0

    def set_moving_head_position(self, pan: int = None, tilt: int = None, gobo: int = None, prism: int = None, focus: int = None, shutter: int = None) -> None:
        """Set moving head position and parameters."""
        if pan is not None:
            self.pan = max(0, min(255, pan))
        if tilt is not None:
            self.tilt = max(0, min(255, tilt))
        if gobo is not None:
            self.gobo = max(0, min(255, gobo))
        if prism is not None:
            self.prism = max(0, min(255, prism))
        if focus is not None:
            self.focus = max(0, min(255, focus))
        if shutter is not None:
            self.shutter = max(0, min(255, shutter))

        # Calculate beam direction for visualization
        # Pan: 0-255 maps to -180 to +180 degrees
        pan_degrees = ((self.pan - 128) / 128.0) * 180.0
        self.beam_angle = math.radians(pan_degrees)

        # Tilt: 0-255 maps to -90 to +90 degrees (affects beam length/elevation)
        tilt_degrees = ((self.tilt - 128) / 128.0) * 90.0
        self.beam_elevation = math.radians(tilt_degrees)

    def update(self, current_time: float) -> None:
        """Aktualizuje animace světla."""
        # Fade animation
        if self.fade_duration > 0:
            progress = (current_time - self.fade_start_time) / self.fade_duration
            progress = max(0.0, min(1.0, progress))

            # Interpolate color
            start_color = self.color
            target_color = self.target_color

            self.color = (
                int(start_color[0] + (target_color[0] - start_color[0]) * progress),
                int(start_color[1] + (target_color[1] - start_color[1]) * progress),
                int(start_color[2] + (target_color[2] - start_color[2]) * progress),
            )

            if progress >= 1.0:
                self.fade_duration = 0

        # Effect animations
        if self.effect == "strobe" and self.is_on:
            # Strobe effect - rychlé blikání
            strobe_rate = 8  # Hz
            self.effect_progress = (current_time * strobe_rate) % 1.0
            if self.effect_progress < 0.3:
                self.intensity = 1.0
            else:
                self.intensity = 0.1

        elif self.effect == "pulse" and self.is_on:
            # Pulse effect - pomalé pulzování
            pulse_rate = 3  # Hz
            self.effect_progress = (current_time * pulse_rate) % 1.0
            self.intensity = 0.3 + 0.7 * abs(
                math.sin(self.effect_progress * 2 * math.pi)
            )

        elif self.effect == "fade" and self.is_on:
            # Fade effect - pozvolné změny
            fade_rate = 1  # Hz
            self.effect_progress = (current_time * fade_rate) % 1.0
            self.intensity = (
                0.2 + 0.8 * (math.sin(self.effect_progress * 2 * math.pi) + 1) / 2
            )

        # Pro světla bez efektů, ale zapnutá, ujisti se že mají plnou intenzitu
        elif self.is_on and not self.effect:
            self.intensity = 1.0

    def get_render_color(self) -> tuple[int, int, int]:
        """Vrátí barvu pro vykreslení s intenzitou."""
        if not self.is_on or self.intensity <= 0:
            return (10, 10, 10)  # Tmavě šedá když je vypnuto

        return (
            int(self.color[0] * self.intensity),
            int(self.color[1] * self.intensity),
            int(self.color[2] * self.intensity),
        )


class SaunaRenderer:
    """2D renderer sauny se světelnými efekty."""

    def __init__(self, width: int = 1200, height: int = 800):
        """Initialize sauna renderer.

        Args:
            width: Šířka okna
            height: Výška okna
        """
        self.width = width
        self.height = height

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("DMX Sauna Visualizer")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)

        # Colors
        self.bg_color = (20, 20, 25)
        self.sauna_wall_color = (139, 90, 43)  # Hnědé dřevo
        self.sauna_bench_color = (160, 100, 50)
        self.text_color = (255, 255, 255)

        # Sauna layout (proportions)
        self.sauna_rect = pygame.Rect(50, 50, width - 300, height - 100)

        # Initialize fixtures
        self.fixtures: dict[str, LightFixture] = {}
        self._create_sauna_fixtures()

        # Color mapping
        self.color_map = {
            "red": (255, 50, 50),
            "green": (50, 255, 50),
            "blue": (50, 50, 255),
            "yellow": (255, 255, 50),
            "orange": (255, 150, 50),
            "purple": (255, 50, 255),
            "azure": (50, 200, 255),
            "white - studená": (200, 220, 255),
            "white - teplá": (255, 220, 180),
            "white": (255, 255, 255),
        }

    def _create_sauna_fixtures(self) -> None:
        """Vytvoří světelná zařízení podle reálného 3D modelu sauny."""
        # Reálné rozměry sauny: 8.5m x 7.6m x 3.1m
        # 3D souřadnice: X(-4.25 až +4.25), Z(-3.8 až +3.8), Y(0 až 3.1)

        # Scaling pro 2D zobrazení
        scale_x = self.sauna_rect.width / 8.5  # pixels per meter X
        scale_z = self.sauna_rect.height / 7.6  # pixels per meter Z
        center_x = self.sauna_rect.centerx
        center_z = self.sauna_rect.centery

        def real_3d_to_2d(x_3d: float, z_3d: float) -> tuple[int, int]:
            """Převede reálné 3D pozice na 2D obrazovku."""
            x_2d = center_x + (x_3d * scale_x)
            z_2d = center_z - (z_3d * scale_z)  # Inverted Z for screen coordinates
            return (int(x_2d), int(z_2d))

        # Wall Spots (8 kusů) - přesné pozice z 3D modelu
        wall_spots_3d = [
            (-3.21, -2.60),  # Spot_(stěna) #1
            (-3.23, -0.73),  # Spot_(stěna) #2
            (-3.23, 0.80),  # Spot_(stěna) #3
            (-2.58, 3.33),  # Spot_(stěna) #4
            (2.58, 3.33),  # Spot_(stěna) #5
            (3.23, 0.78),  # Spot_(stěna) #6
            (3.23, -0.73),  # Spot_(stěna) #7
            (3.23, -2.60),  # Spot_(stěna) #8
        ]

        for i, (x_3d, z_3d) in enumerate(wall_spots_3d):
            pos = real_3d_to_2d(x_3d, z_3d)
            self.fixtures[f"wall_spot_{i + 1}"] = LightFixture(
                f"Wall Spot {i + 1}", pos, "wall_spot", size=20
            )

        # Bodovky (12 kusů) - přesné pozice z 3D modelu
        bodovky_3d = [
            (-1.07, -3.05),  # Bodovka_(strop) #1
            (-1.07, -1.85),  # Bodovka_(strop) #2
            (-1.07, -0.75),  # Bodovka_(strop) #3
            (-1.07, 0.35),  # Bodovka_(strop) #4
            (-1.07, 1.35),  # Bodovka_(strop) #5
            (0.00, 1.35),  # Bodovka_(strop) #6
            (1.07, 1.35),  # Bodovka_(strop) #7
            (1.07, 0.35),  # Bodovka_(strop) #8
            (1.07, -0.75),  # Bodovka_(strop) #9
            (1.07, -1.85),  # Bodovka_(strop) #10
            (1.07, -2.90),  # Bodovka_(strop) #11
            (0.00, -3.67),  # Bodovka_(strop) #12
        ]

        for i, (x_3d, z_3d) in enumerate(bodovky_3d):
            pos = real_3d_to_2d(x_3d, z_3d)
            self.fixtures[f"bodovka_{i + 1}"] = LightFixture(
                f"Bodovka {i + 1}", pos, "ceiling_spot", size=25
            )

        # LED pásky lavice (11 kusů) - přesné pozice z 3D modelu
        led_lavice_3d = [
            (-2.53, -3.36),  # LED_pásek_(lavice) #1
            (-3.80, -1.64),  # LED_pásek_(lavice) #2
            (-3.80, 0.22),  # LED_pásek_(lavice) #3
            (-3.80, 2.00),  # LED_pásek_(lavice) #4
            (-2.84, 3.66),  # LED_pásek_(lavice) #5
            (0.17, 4.25),  # LED_pásek_(lavice) #6
            (3.03, 3.54),  # LED_pásek_(lavice) #7
            (3.80, 2.00),  # LED_pásek_(lavice) #8
            (3.80, 0.22),  # LED_pásek_(lavice) #9
            (3.80, -1.64),  # LED_pásek_(lavice) #10
            (2.53, -3.33),  # LED_pásek_(lavice) #11
        ]

        for i, (x_3d, z_3d) in enumerate(led_lavice_3d):
            pos = real_3d_to_2d(x_3d, z_3d)
            self.fixtures[f"led_lavice_{i + 1}"] = LightFixture(
                f"LED Lavice {i + 1}", pos, "led_strip", size=30
            )

        # Moving Heads (5 kusů) - přesné pozice z 3D modelu
        moving_heads_3d = [
            (-2.37, -1.65),  # Intimidator Spot 375Z #1
            (-2.37, 0.69),  # Intimidator Spot 375Z #2
            (-0.16, 1.90),  # Intimidator Spot 375Z #3
            (2.21, 0.13),  # Intimidator Spot 375Z #4
            (2.21, -0.54),  # Intimidator Spot 375Z #5
        ]

        for i, (x_3d, z_3d) in enumerate(moving_heads_3d):
            pos = real_3d_to_2d(x_3d, z_3d)
            self.fixtures[f"moving_head_{i + 1}"] = LightFixture(
                f"Moving Head {i + 1}", pos, "moving_head", size=18
            )

        # LED kamna (2 světla) - přesné pozice z 3D modelu
        led_kamna_3d = [
            (-0.68, -1.32),  # LED_pásek_(kamna) #1
            (0.66, -1.28),  # LED_pásek_(kamna) #2
        ]

        for i, (x_3d, z_3d) in enumerate(led_kamna_3d):
            pos = real_3d_to_2d(x_3d, z_3d)
            self.fixtures[f"led_kamna_{i + 1}"] = LightFixture(
                f"LED Kamna {i + 1}", pos, "led_oven", size=25
            )

        # UV světla (1 kus) - přesná pozice z 3D modelu
        uv_3d = (-0.02, -1.58)  # UV_světla
        pos = real_3d_to_2d(uv_3d[0], uv_3d[1])
        self.fixtures["uv_1"] = LightFixture("UV Light 1", pos, "uv_light", size=15)

        logger.info(f"Created {len(self.fixtures)} light fixtures (real 3D layout)")

    def update_lights(self, light_changes: dict, current_time: float) -> None:
        """Aktualizuje světla na základě timeline změn."""
        for timeline_index, change_info in light_changes.items():
            event = change_info["event"]
            action = change_info["action"]
            progress = change_info["progress"]

            # Parse scene path to determine fixture and color
            fixture_group, color = self._parse_scene_path(event.path)

            if action == "start":
                # Check if this is an advanced scene file
                if "generated_scenes_advanced" in event.path:
                    self._activate_advanced_scene(event.path, current_time)
                else:
                    self._activate_fixture_group(fixture_group, color, event, current_time)
            elif action == "end":
                self._deactivate_fixture_group(fixture_group)
            elif action == "update":
                self._update_fixture_group(fixture_group, progress, event)

        # Update all fixture animations
        for fixture in self.fixtures.values():
            fixture.update(current_time)

    def _activate_advanced_scene(self, scene_path: str, current_time: float) -> None:
        """Load and activate advanced scene with full DMX channel control."""
        import xml.etree.ElementTree as ET
        from pathlib import Path
        import os

        # Build full path to scene file
        full_path = Path(scene_path)
        if not full_path.is_absolute():
            # Relative to current working directory
            full_path = Path(os.getcwd()) / scene_path

        logger.debug(f"Loading advanced scene: {full_path}")

        try:
            if not full_path.exists():
                logger.warning(f"Advanced scene file not found: {full_path}")
                return

            # Parse XML scene file
            tree = ET.parse(full_path)
            root = tree.getroot()

            # Find Steps section
            steps = root.find("Steps")
            if steps is None:
                logger.warning(f"No Steps found in scene file: {full_path}")
                return

            # Get first step (for now, we use the first step's values)
            first_step = steps.find("Step")
            if first_step is None:
                logger.warning(f"No Step found in scene file: {full_path}")
                return

            # Process each fixture in the step
            for fixture_elem in first_step.findall("Fixture"):
                fixture_id = fixture_elem.get("id")

                # Map fixture ID to our visualizer fixtures
                viz_fixture_key = self._map_fixture_id_to_key(fixture_id)
                if not viz_fixture_key or viz_fixture_key not in self.fixtures:
                    logger.debug(f"Fixture ID {fixture_id} not found in visualizer")
                    continue

                fixture = self.fixtures[viz_fixture_key]
                logger.debug(f"Processing fixture: {viz_fixture_key}")

                # Extract DMX channel values
                channels = {}
                for channel_elem in fixture_elem.findall("Channel"):
                    channel_name = channel_elem.get("name")
                    channel_value = int(channel_elem.get("value", 0))
                    channels[channel_name] = channel_value

                # Apply channels to fixture
                if fixture.fixture_type == "moving_head":
                    # Set moving head parameters
                    fixture.set_moving_head_position(
                        pan=channels.get("pan"),
                        tilt=channels.get("tilt"),
                        gobo=channels.get("gobo"),
                        prism=channels.get("prism"),
                        focus=channels.get("focus"),
                        shutter=channels.get("shutter")
                    )

                    # Set color and intensity
                    if "color" in channels:
                        color_rgb = self._dmx_color_to_rgb(channels["color"])
                        intensity = channels.get("dimmer", 255) / 255.0
                        fixture.set_color(color_rgb, intensity)
                        logger.debug(f"Set {viz_fixture_key}: PAN={channels.get('pan', 128)}, TILT={channels.get('tilt', 128)}, Color={color_rgb}, Intensity={intensity:.2f}")

        except Exception as e:
            logger.error(f"Error loading advanced scene {scene_path}: {e}")

    def _map_fixture_id_to_key(self, fixture_id: str) -> str | None:
        """Map DMX fixture ID to visualizer fixture key."""
        # Moving heads mapping
        id_to_key = {
            "1753953037": "moving_head_1",
            "1753953038": "moving_head_2",
            "1753953039": "moving_head_3",
            "1753953040": "moving_head_4",
            "1753953041": "moving_head_5",
        }
        return id_to_key.get(fixture_id)

    def _dmx_color_to_rgb(self, dmx_value: int) -> tuple[int, int, int]:
        """Convert DMX color wheel value to RGB."""
        # Basic color wheel mapping (similar to our moving heads generator)
        color_map = {
            0: (255, 255, 255),   # White
            11: (255, 0, 0),      # Red
            31: (255, 128, 0),    # Orange
            51: (0, 0, 255),      # Blue
            71: (255, 255, 0),    # Yellow
            91: (0, 255, 0),      # Green
            111: (128, 0, 255),   # Purple
            131: (0, 255, 255),   # Cyan
            171: (255, 0, 255),   # Magenta
            211: (255, 255, 255), # White
        }

        # Find closest color
        closest_dmx = min(color_map.keys(), key=lambda x: abs(x - dmx_value))
        return color_map[closest_dmx]

    def _parse_scene_path(self, path: str) -> tuple[str, str]:
        """Parsuje scene path pro určení skupiny světel a barvy."""
        if path == "OFF":
            return "all", "off"

        # Extract fixture group and color from path
        # Systematic paths: "generated_scenes_systematic/individual/ceiling_spot_00/red_static.scex"
        #                  "generated_scenes_systematic/individual/led_wall_00/blue_static.scex"

        parts = path.split("/")
        if len(parts) >= 2:
            # For systematic individual scenes
            if "individual" in parts and len(parts) >= 4:
                fixture_name = parts[-2]  # e.g., "ceiling_spot_00", "led_wall_00"
                filename = parts[-1]      # e.g., "red_static.scex"

                # Map systematic names to renderer fixture keys
                fixture_key = self._map_systematic_name_to_fixture_key(fixture_name)

                # Extract color from filename
                color = self._extract_color_from_filename(filename)

                return fixture_key, color

            # Legacy paths: "LED_walls/Walls_all/Walls_red.scex"
            group = parts[0].lower()

            # Rozpoznej jestli je to single nebo all
            if len(parts) >= 3:
                if "single" in parts[1].lower():
                    # Pro single light - použij specifický název
                    if len(parts) >= 4:
                        group = parts[2].lower()  # např. "Walls_11"
                    else:
                        group = parts[1].lower()
                elif "all" in parts[1].lower():
                    # Pro all lights - použij základní skupinu
                    group = parts[0].lower()
                else:
                    group = parts[1].lower()

            filename = parts[-1] if len(parts) > 2 else parts[1]
            color = self._extract_color_from_filename(filename)

            return group, color

        return "unknown", "white"

    def _map_systematic_name_to_fixture_key(self, systematic_name: str) -> str:
        """Map systematic fixture name to renderer fixture key."""
        # ceiling_spot_00 -> bodovka_1
        if systematic_name.startswith("ceiling_spot_"):
            num = int(systematic_name.split("_")[-1])
            return f"bodovka_{num + 1}"  # 0-based to 1-based

        # led_wall_00 -> wall_spot_1
        elif systematic_name.startswith("led_wall_"):
            num_str = systematic_name.split("_")[-1]
            if num_str == "99":  # Special case for led_wall_99
                num = 10  # Map to wall_spot_11 (but we only have 8, so it will map to existing)
            else:
                num = int(num_str)
            return f"wall_spot_{num + 1}"  # 0-based to 1-based

        # moving_head_37 -> moving_head_1
        elif systematic_name.startswith("moving_head_"):
            num_str = systematic_name.split("_")[-1]
            # Map moving head IDs to 1-5 range
            if num_str == "37":
                return "moving_head_1"
            elif num_str == "38":
                return "moving_head_2"
            elif num_str == "39":
                return "moving_head_3"
            elif num_str == "40":
                return "moving_head_4"
            elif num_str == "41":
                return "moving_head_5"
            else:
                return "moving_head_1"  # Default fallback

        # uv_41, uv_42 -> uv_1
        elif systematic_name.startswith("uv_"):
            return "uv_1"

        # For other types, return as-is and let the group mapping handle it
        return systematic_name

    def _extract_color_from_filename(self, filename: str) -> str:
        """Extract color from filename."""
        filename_lower = filename.lower()

        if "red" in filename_lower or "červen" in filename_lower:
            return "red"
        elif "blue" in filename_lower or "modr" in filename_lower:
            return "blue"
        elif "green" in filename_lower or "zelen" in filename_lower:
            return "green"
        elif "yellow" in filename_lower or "žlut" in filename_lower:
            return "yellow"
        elif "orange" in filename_lower or "oranžov" in filename_lower:
            return "orange"
        elif "purple" in filename_lower or "fialov" in filename_lower:
            return "purple"
        elif "magenta" in filename_lower:
            return "purple"  # Map magenta to purple
        elif "cyan" in filename_lower:
            return "azure"   # Map cyan to azure
        elif "azure" in filename_lower or "azurov" in filename_lower:
            return "azure"
        elif "white" in filename_lower and "cool" in filename_lower:
            return "white - studená"
        elif "white" in filename_lower and "warm" in filename_lower:
            return "white - teplá"
        elif "white" in filename_lower or "bil" in filename_lower:
            return "white"

        return "white"  # Default

    def _activate_fixture_group(
        self, group: str, color: str, event, current_time: float
    ) -> None:
        """Aktivuje skupinu světel."""
        rgb_color = self.color_map.get(color, (255, 255, 255))
        intensity = 1.0
        effect = None

        # Determine effect based on scene path or event properties
        if "strobe" in event.path.lower() or "flash" in event.path.lower():
            effect = "strobe"
        elif "pulse" in event.path.lower():
            effect = "pulse"
        elif "single" in event.path.lower():
            # Pro single světla použij pulse efekt
            effect = "pulse"
        elif "fade" in event.path.lower() or (
            event.length and ("0:00:01" in event.length or "0:00:02" in event.length)
        ):
            effect = "fade"

        # Map groups to fixtures
        fixture_keys = self._get_fixtures_for_group(group)

        logger.debug(
            f"Activating group '{group}' with color '{color}' -> {len(fixture_keys)} fixtures: {fixture_keys}"
        )

        for key in fixture_keys:
            if key in self.fixtures:
                self.fixtures[key].set_color(rgb_color, intensity, effect)
                logger.info(
                    f"🔴 Activated fixture {key} with color {rgb_color}, intensity {intensity}, effect {effect}"
                )
                logger.info(
                    f"🔴 Fixture {key} is_on: {self.fixtures[key].is_on}, color: {self.fixtures[key].color}"
                )

    def _deactivate_fixture_group(self, group: str) -> None:
        """Deaktivuje skupinu světel."""
        fixture_keys = self._get_fixtures_for_group(group)

        for key in fixture_keys:
            if key in self.fixtures:
                self.fixtures[key].set_color((0, 0, 0), 0.0)

    def _update_fixture_group(self, group: str, progress: float, event) -> None:
        """Aktualizuje skupinu světel s progresem."""
        # Pro fade efekty můžeme měnit intenzitu podle progresu
        fixture_keys = self._get_fixtures_for_group(group)

        for key in fixture_keys:
            if key in self.fixtures:
                fixture = self.fixtures[key]
                if event.fade_out and progress > 0.8:
                    # Fade out effect
                    fade_progress = (progress - 0.8) / 0.2
                    fixture.intensity = 1.0 - fade_progress

    def _get_fixtures_for_group(self, group: str) -> list[str]:
        """Vrátí klíče světel pro danou skupinu."""
        group_lower = group.lower()

        # Check if this is a direct fixture key first
        if group in self.fixtures:
            return [group]

        # Základní skupiny
        if group_lower in ["bodovky", "bodovka", "ceiling"]:
            return [k for k in self.fixtures.keys() if k.startswith("bodovka_")]
        if group_lower in ["led_walls", "walls", "led_wall"]:
            return [k for k in self.fixtures.keys() if k.startswith("wall_spot_")]
        if group_lower in ["led_lavice", "lavice", "bench"]:
            return [k for k in self.fixtures.keys() if k.startswith("led_lavice_")]
        if group_lower in ["led_kamna", "led_oven", "oven", "kamna"]:
            return [k for k in self.fixtures.keys() if k.startswith("led_kamna_")]
        if group_lower in ["moving_heads", "moving"]:
            return [k for k in self.fixtures.keys() if k.startswith("moving_head_")]
        if group_lower in ["uv", "uv_lights"]:
            return [k for k in self.fixtures.keys() if k.startswith("uv_")]
        if group_lower == "all":
            return list(self.fixtures.keys())

        # Jednotlivé světla
        if "walls_" in group_lower:
            # Parse wall number - mapuj na dostupné wall spoty (1-8)
            try:
                wall_num = int(group_lower.split("_")[-1])
                # Mapuj wall čísla na dostupné spoty (máme jen 8 wall spotů)
                mapped_num = ((wall_num - 1) % 8) + 1
                fixture_key = f"wall_spot_{mapped_num}"
                if fixture_key in self.fixtures:
                    return [fixture_key]
                return [k for k in self.fixtures.keys() if k.startswith("wall_spot_")]
            except:
                return [k for k in self.fixtures.keys() if k.startswith("wall_spot_")]

        elif "bodovka_" in group_lower:
            # Parse bodovka number (máme 1-12)
            try:
                bodovka_num = int(group_lower.split("_")[-1])
                if 1 <= bodovka_num <= 12:
                    fixture_key = f"bodovka_{bodovka_num}"
                    if fixture_key in self.fixtures:
                        return [fixture_key]
                return [k for k in self.fixtures.keys() if k.startswith("bodovka_")]
            except:
                return [k for k in self.fixtures.keys() if k.startswith("bodovka_")]

        elif "moving_head_" in group_lower:
            # Moving heads - direct mapping
            if group_lower in self.fixtures:
                return [group_lower]
            # Try parsing number
            try:
                mh_num = int(group_lower.split("_")[-1])
                if 1 <= mh_num <= 5:
                    fixture_key = f"moving_head_{mh_num}"
                    if fixture_key in self.fixtures:
                        return [fixture_key]
                return [k for k in self.fixtures.keys() if k.startswith("moving_head_")]
            except:
                return [k for k in self.fixtures.keys() if k.startswith("moving_head_")]

        elif "wall_spot_" in group_lower:
            # Wall spots - direct mapping
            if group_lower in self.fixtures:
                return [group_lower]
            return []

        elif "uv_" in group_lower:
            # UV lights - direct mapping
            if group_lower in self.fixtures:
                return [group_lower]
            return [k for k in self.fixtures.keys() if k.startswith("uv_")]

        elif "lavice_" in group_lower:
            # LED lavice
            try:
                lavice_num = int(group_lower.split("_")[-1])
                if 1 <= lavice_num <= 11:
                    fixture_key = f"led_lavice_{lavice_num}"
                    if fixture_key in self.fixtures:
                        return [fixture_key]
                return [k for k in self.fixtures.keys() if k.startswith("led_lavice_")]
            except:
                return [k for k in self.fixtures.keys() if k.startswith("led_lavice_")]

        return []

    def render(
        self, current_time: float, duration: float, active_events: list = None
    ) -> None:
        """Vykreslí celou scénu."""
        # Clear screen
        self.screen.fill(self.bg_color)

        # Draw sauna structure
        self._draw_sauna_structure()

        # Draw light fixtures
        self._draw_light_fixtures()

        # Draw UI panel
        self._draw_ui_panel(current_time, duration, active_events)

        # Update display
        pygame.display.flip()

    def _draw_sauna_structure(self) -> None:
        """Vykreslí realistickou strukturu sauny podle 3D modelu."""
        # Sauna walls - reálné rozměry 8.5m x 7.6m
        pygame.draw.rect(self.screen, self.sauna_wall_color, self.sauna_rect, 4)

        # Scaling pro 2D zobrazení (stejný jako v _create_sauna_fixtures)
        scale_x = self.sauna_rect.width / 8.5
        scale_z = self.sauna_rect.height / 7.6
        center_x = self.sauna_rect.centerx
        center_z = self.sauna_rect.centery

        def real_3d_to_2d_structure(x_3d: float, z_3d: float) -> tuple[int, int]:
            """Převede reálné 3D pozice na 2D obrazovku."""
            x_2d = center_x + (x_3d * scale_x)
            z_2d = center_z - (z_3d * scale_z)
            return (int(x_2d), int(z_2d))

        # Vykreslení hlavních lavic podle reálných pozic
        bench_color = (160, 82, 45)
        main_benches = [
            # Levá strana
            (-2.48, -0.63, 120, 40),
            (-2.48, 2.00, 80, 30),
            # Pravá strana
            (2.48, -0.64, 120, 40),
            (2.48, 2.00, 80, 30),
            # Zadní strana
            (0.00, 2.94, 140, 35),
        ]

        for x_3d, z_3d, width, height in main_benches:
            pos = real_3d_to_2d_structure(x_3d, z_3d)
            bench_rect = pygame.Rect(
                pos[0] - width // 2, pos[1] - height // 2, width, height
            )
            pygame.draw.rect(self.screen, bench_color, bench_rect)

        # Kamna oblast (podle reálné pozice)
        stove_pos = real_3d_to_2d_structure(0.0, -1.25)
        stove_rect = pygame.Rect(stove_pos[0] - 50, stove_pos[1] - 40, 100, 80)
        pygame.draw.rect(self.screen, (100, 50, 50), stove_rect)

        # Plasma screen (podle reálné pozice)
        screen_pos = real_3d_to_2d_structure(0.00, -4.22)
        screen_rect = pygame.Rect(screen_pos[0] - 40, screen_pos[1] - 15, 80, 30)
        pygame.draw.rect(self.screen, (32, 32, 32), screen_rect)

        # Labels s reálnými rozměry
        title_text = self.font_medium.render(
            "REÁLNÁ SAUNA (8.5m × 7.6m)", True, self.text_color
        )
        self.screen.blit(title_text, (self.sauna_rect.x, self.sauna_rect.y - 25))

        # Kamna label
        stove_text = self.font_small.render("KAMNA", True, self.text_color)
        self.screen.blit(stove_text, (stove_rect.x + 30, stove_rect.y + 35))

        # Screen label
        screen_text = self.font_small.render("TV", True, self.text_color)
        self.screen.blit(screen_text, (screen_rect.x + 30, screen_rect.y + 8))

        # Orientace kompas
        compass_x = self.sauna_rect.right - 80
        compass_y = self.sauna_rect.top + 15
        compass_text = self.font_small.render("N↑", True, (150, 150, 150))
        self.screen.blit(compass_text, (compass_x, compass_y))

    def _draw_light_fixtures(self) -> None:
        """Vykreslí světelná zařízení."""
        active_count = 0
        for fixture in self.fixtures.values():
            color = fixture.get_render_color()
            pos = fixture.position
            size = fixture.size

            # Debug: počítej aktivní světla
            if fixture.is_on and fixture.intensity > 0.1:
                active_count += 1

            # Draw light fixture
            if fixture.fixture_type == "ceiling_spot":
                # Kruh pro bodovky
                pygame.draw.circle(self.screen, color, pos, size // 2)
                pygame.draw.circle(self.screen, (100, 100, 100), pos, size // 2, 2)

            elif fixture.fixture_type == "wall_spot":
                # Čtverec pro wall spoty
                rect = pygame.Rect(pos[0] - size // 2, pos[1] - size // 2, size, size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)

            elif fixture.fixture_type == "led_strip":
                # Obdélník pro LED pásky
                rect = pygame.Rect(pos[0] - size // 2, pos[1] - 10, size, 20)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

            elif fixture.fixture_type == "led_oven":
                # Kruh pro LED kamna
                pygame.draw.circle(self.screen, color, pos, size // 2)
                pygame.draw.circle(self.screen, (150, 100, 100), pos, size // 2, 2)

            elif fixture.fixture_type == "moving_head":
                # Advanced moving head visualization with beam direction

                # Draw main fixture body (diamond)
                points = [
                    (pos[0], pos[1] - size // 2),
                    (pos[0] + size // 2, pos[1]),
                    (pos[0], pos[1] + size // 2),
                    (pos[0] - size // 2, pos[1]),
                ]
                pygame.draw.polygon(self.screen, color, points)
                pygame.draw.polygon(self.screen, (100, 100, 100), points, 2)

                # Draw beam direction if light is on
                if fixture.intensity > 0.1:
                    # Calculate beam length based on tilt (elevation)
                    # Higher tilt = shorter beam (pointing down), lower tilt = longer beam
                    base_beam_length = 120
                    elevation_factor = math.cos(fixture.beam_elevation)
                    beam_length = int(base_beam_length * elevation_factor * fixture.intensity)

                    if beam_length > 10:  # Only draw if beam is long enough to see
                        # Calculate beam end point based on pan angle
                        beam_end_x = pos[0] + beam_length * math.cos(fixture.beam_angle)
                        beam_end_y = pos[1] + beam_length * math.sin(fixture.beam_angle)

                        # Draw beam cone (triangle)
                        beam_width = 15 + int(5 * fixture.intensity)

                        # Calculate perpendicular vector for beam width
                        perp_x = -math.sin(fixture.beam_angle) * beam_width
                        perp_y = math.cos(fixture.beam_angle) * beam_width

                        beam_points = [
                            pos,  # Start at fixture
                            (beam_end_x + perp_x, beam_end_y + perp_y),  # Left side
                            (beam_end_x - perp_x, beam_end_y - perp_y),  # Right side
                        ]

                        # Semi-transparent beam color
                        beam_color = (*color, 40)
                        beam_surf = pygame.Surface((abs(int(beam_end_x - pos[0])) + beam_width * 2,
                                                  abs(int(beam_end_y - pos[1])) + beam_width * 2), pygame.SRCALPHA)

                        # Offset for beam surface
                        surf_offset_x = min(pos[0], beam_end_x + perp_x, beam_end_x - perp_x) - beam_width
                        surf_offset_y = min(pos[1], beam_end_y + perp_y, beam_end_y - perp_y) - beam_width

                        # Adjust beam points for surface coordinates
                        beam_points_surf = [
                            (pos[0] - surf_offset_x, pos[1] - surf_offset_y),
                            (beam_end_x + perp_x - surf_offset_x, beam_end_y + perp_y - surf_offset_y),
                            (beam_end_x - perp_x - surf_offset_x, beam_end_y - perp_y - surf_offset_y),
                        ]

                        pygame.draw.polygon(beam_surf, beam_color, beam_points_surf)
                        self.screen.blit(beam_surf, (surf_offset_x, surf_offset_y), special_flags=pygame.BLEND_ALPHA_SDL2)

                        # Draw beam center line
                        beam_line_color = tuple(min(255, c + 50) for c in color)
                        pygame.draw.line(self.screen, beam_line_color, pos, (beam_end_x, beam_end_y), 2)

                        # Draw beam target spot
                        target_radius = max(3, int(8 * fixture.intensity))
                        pygame.draw.circle(self.screen, color, (int(beam_end_x), int(beam_end_y)), target_radius)

                        # Add gobo/prism effects
                        if fixture.gobo > 0:
                            # Simple gobo pattern visualization
                            gobo_points = []
                            for i in range(6):
                                angle = i * math.pi / 3
                                gobo_x = beam_end_x + 8 * math.cos(angle)
                                gobo_y = beam_end_y + 8 * math.sin(angle)
                                gobo_points.append((gobo_x, gobo_y))
                            pygame.draw.polygon(self.screen, beam_line_color, gobo_points, 1)

                        if fixture.prism > 0:
                            # Prism rainbow effect
                            prism_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
                            for i, prism_color in enumerate(prism_colors):
                                offset_angle = fixture.beam_angle + (i - 3) * 0.2
                                prism_x = pos[0] + beam_length * 0.8 * math.cos(offset_angle)
                                prism_y = pos[1] + beam_length * 0.8 * math.sin(offset_angle)
                                pygame.draw.circle(self.screen, prism_color, (int(prism_x), int(prism_y)), 2)

            elif fixture.fixture_type == "uv":
                # Hvězda pro UV
                star_points = []
                for i in range(8):
                    angle = i * math.pi / 4
                    radius = size // 2 if i % 2 == 0 else size // 4
                    x = pos[0] + radius * math.cos(angle)
                    y = pos[1] + radius * math.sin(angle)
                    star_points.append((x, y))
                pygame.draw.polygon(self.screen, color, star_points)
                pygame.draw.polygon(self.screen, (150, 0, 255), star_points, 1)

            # Draw light glow effect if intensity > 0
            if fixture.intensity > 0.3:
                glow_radius = int(size * 1.5 * fixture.intensity)
                glow_color = (*color, int(30 * fixture.intensity))

                # Create glow surface with alpha
                glow_surf = pygame.Surface(
                    (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
                )
                glow_center = (glow_radius, glow_radius)

                for r in range(glow_radius, 0, -2):
                    alpha = int(
                        20 * fixture.intensity * (glow_radius - r) / glow_radius
                    )
                    glow_color_alpha = (*color, alpha)
                    pygame.draw.circle(glow_surf, glow_color_alpha, glow_center, r)

                glow_pos = (pos[0] - glow_radius, pos[1] - glow_radius)
                self.screen.blit(glow_surf, glow_pos, special_flags=pygame.BLEND_ADD)

        # Debug log each few frames
        if hasattr(self, "_frame_count"):
            self._frame_count += 1
        else:
            self._frame_count = 0

        if self._frame_count % 60 == 0 and active_count > 0:  # Every second
            logger.info(f"🎨 Rendering {active_count} active lights")

    def _draw_ui_panel(
        self, current_time: float, duration: float, active_events: list = None
    ) -> None:
        """Vykreslí UI panel s informacemi."""
        panel_x = self.width - 280
        panel_y = 20
        panel_width = 260
        panel_height = self.height - 40

        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (40, 40, 50), panel_rect)
        pygame.draw.rect(self.screen, (80, 80, 90), panel_rect, 2)

        y_offset = panel_y + 20

        # Title
        title = self.font_large.render("DMX Visualizer", True, self.text_color)
        self.screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 50

        # Time info
        time_text = f"Time: {current_time:.1f}s / {duration:.1f}s"
        time_surface = self.font_medium.render(time_text, True, self.text_color)
        self.screen.blit(time_surface, (panel_x + 10, y_offset))
        y_offset += 30

        # Progress bar
        progress = current_time / duration if duration > 0 else 0
        progress_rect = pygame.Rect(panel_x + 10, y_offset, panel_width - 20, 20)
        pygame.draw.rect(self.screen, (100, 100, 100), progress_rect)

        progress_fill = pygame.Rect(
            panel_x + 10, y_offset, int((panel_width - 20) * progress), 20
        )
        pygame.draw.rect(self.screen, (50, 150, 255), progress_fill)
        y_offset += 40

        # Active events
        events_title = self.font_medium.render("Active Events:", True, self.text_color)
        self.screen.blit(events_title, (panel_x + 10, y_offset))
        y_offset += 30

        if active_events:
            for i, event in enumerate(active_events[:10]):  # Max 10 events
                event_text = (
                    f"TL{event.timeline_index}: {event.path.split('/')[-1][:20]}"
                )
                event_surface = self.font_small.render(
                    event_text, True, (200, 200, 200)
                )
                self.screen.blit(event_surface, (panel_x + 15, y_offset))
                y_offset += 20
        else:
            no_events = self.font_small.render(
                "No active events", True, (150, 150, 150)
            )
            self.screen.blit(no_events, (panel_x + 15, y_offset))

        y_offset += 40

        # Light fixtures status
        fixtures_title = self.font_medium.render("Light Status:", True, self.text_color)
        self.screen.blit(fixtures_title, (panel_x + 10, y_offset))
        y_offset += 30

        # Count active lights by type
        active_counts = {}
        for key, fixture in self.fixtures.items():
            fixture_type = fixture.fixture_type
            if fixture_type not in active_counts:
                active_counts[fixture_type] = [0, 0]  # [active, total]

            active_counts[fixture_type][1] += 1
            if fixture.is_on and fixture.intensity > 0.1:
                active_counts[fixture_type][0] += 1

        for fixture_type, (active, total) in active_counts.items():
            status_text = f"{fixture_type}: {active}/{total}"
            color = (100, 255, 100) if active > 0 else (150, 150, 150)
            status_surface = self.font_small.render(status_text, True, color)
            self.screen.blit(status_surface, (panel_x + 15, y_offset))
            y_offset += 20

    def handle_events(self) -> bool:
        """Zpracuje pygame eventy. Vrátí False pokud má aplikace skončit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Další eventy můžeme přidat později (klávesy, myš, etc.)

        return True

    def cleanup(self) -> None:
        """Uklidí pygame resources."""
        pygame.quit()

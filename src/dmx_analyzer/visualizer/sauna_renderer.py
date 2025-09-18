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

    def set_color(
        self, color: tuple[int, int, int], intensity: float = 1.0, effect: str = None
    ) -> None:
        """Nastaví barvu a efekt světla."""
        self.target_color = color
        self.color = color  # Nastaví okamžitě aktuální barvu
        self.intensity = max(0.0, min(1.0, intensity))
        self.effect = effect
        self.is_on = intensity > 0

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
            self.intensity = 0.3 + 0.7 * abs(math.sin(self.effect_progress * 2 * math.pi))

        elif self.effect == "fade" and self.is_on:
            # Fade effect - pozvolné změny
            fade_rate = 1  # Hz
            self.effect_progress = (current_time * fade_rate) % 1.0
            self.intensity = 0.2 + 0.8 * (math.sin(self.effect_progress * 2 * math.pi) + 1) / 2

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
        """Vytvoří světelná zařízení podle layoutu sauny."""
        # Ceiling spots (Bodovky) - 12 světel ve stropě
        ceiling_y = self.sauna_rect.top + 30
        ceiling_spacing = self.sauna_rect.width // 4
        for i in range(12):
            row = i // 4
            col = i % 4
            x = self.sauna_rect.left + ceiling_spacing // 2 + col * ceiling_spacing
            y = ceiling_y + row * 40

            self.fixtures[f"bodovka_{i + 1}"] = LightFixture(
                f"Bodovka {i + 1}", (x, y), "ceiling_spot", size=25
            )

        # Wall spots (8 světel na stěnách)
        wall_spots_positions = [
            # Levá stěna
            (self.sauna_rect.left + 20, self.sauna_rect.top + 100),
            (self.sauna_rect.left + 20, self.sauna_rect.top + 200),
            # Pravá stěna
            (self.sauna_rect.right - 20, self.sauna_rect.top + 100),
            (self.sauna_rect.right - 20, self.sauna_rect.top + 200),
            # Zadní stěna
            (self.sauna_rect.left + 100, self.sauna_rect.top + 20),
            (self.sauna_rect.left + 200, self.sauna_rect.top + 20),
            (self.sauna_rect.left + 300, self.sauna_rect.top + 20),
            (self.sauna_rect.left + 400, self.sauna_rect.top + 20),
        ]

        for i, pos in enumerate(wall_spots_positions):
            self.fixtures[f"wall_spot_{i + 1}"] = LightFixture(
                f"Wall Spot {i + 1}", pos, "wall_spot", size=20
            )

        # LED strips na lavicích (11 segmentů)
        bench_y = self.sauna_rect.bottom - 80
        bench_spacing = self.sauna_rect.width // 11
        for i in range(11):
            x = self.sauna_rect.left + bench_spacing // 2 + i * bench_spacing
            self.fixtures[f"led_lavice_{i + 1}"] = LightFixture(
                f"LED Lavice {i + 1}", (x, bench_y), "led_strip", size=30
            )

        # LED kamna (2 světla u kamen)
        stove_x = self.sauna_rect.right - 100
        stove_y = self.sauna_rect.bottom - 120
        for i in range(2):
            self.fixtures[f"led_kamna_{i + 1}"] = LightFixture(
                f"LED Kamna {i + 1}", (stove_x + i * 30, stove_y), "led_oven", size=25
            )

        # Moving heads (5 světel)
        moving_positions = [
            (self.sauna_rect.centerx - 100, self.sauna_rect.top + 60),
            (self.sauna_rect.centerx + 100, self.sauna_rect.top + 60),
            (self.sauna_rect.centerx, self.sauna_rect.top + 80),
            (self.sauna_rect.left + 80, self.sauna_rect.centery),
            (self.sauna_rect.right - 80, self.sauna_rect.centery),
        ]

        for i, pos in enumerate(moving_positions):
            self.fixtures[f"moving_head_{i + 1}"] = LightFixture(
                f"Moving Head {i + 1}", pos, "moving_head", size=18
            )

        # UV světla (2 světla)
        uv_positions = [
            (self.sauna_rect.left + 50, self.sauna_rect.bottom - 50),
            (self.sauna_rect.right - 50, self.sauna_rect.bottom - 50),
        ]

        for i, pos in enumerate(uv_positions):
            self.fixtures[f"uv_{i + 1}"] = LightFixture(
                f"UV {i + 1}", pos, "uv", size=15
            )

        logger.info(f"Created {len(self.fixtures)} light fixtures")

    def update_lights(self, light_changes: dict, current_time: float) -> None:
        """Aktualizuje světla na základě timeline změn."""
        for timeline_index, change_info in light_changes.items():
            event = change_info["event"]
            action = change_info["action"]
            progress = change_info["progress"]

            # Parse scene path to determine fixture and color
            fixture_group, color = self._parse_scene_path(event.path)

            if action == "start":
                self._activate_fixture_group(fixture_group, color, event, current_time)
            elif action == "end":
                self._deactivate_fixture_group(fixture_group)
            elif action == "update":
                self._update_fixture_group(fixture_group, progress, event)

        # Update all fixture animations
        for fixture in self.fixtures.values():
            fixture.update(current_time)

    def _parse_scene_path(self, path: str) -> tuple[str, str]:
        """Parsuje scene path pro určení skupiny světel a barvy."""
        if path == "OFF":
            return "all", "off"

        # Extract fixture group and color from path
        # Examples: "LED_walls/Walls_all/Walls_red.scex"
        #          "Bodovky/Bodovky_all/Bodovka_blue.scex"
        #          "LED_Walls/Walls_single/Walls_11/Walls_11_white - studená.scex"

        parts = path.split("/")
        if len(parts) >= 2:
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

            # Extract color from filename - zlepšené rozpoznávání
            color = "white"
            filename_lower = filename.lower()

            # Rozpoznání barev v různých formátech
            if "red" in filename_lower or "červen" in filename_lower:
                color = "red"
            elif "blue" in filename_lower or "modr" in filename_lower:
                color = "blue"
            elif "green" in filename_lower or "zelen" in filename_lower:
                color = "green"
            elif "yellow" in filename_lower or "žlut" in filename_lower:
                color = "yellow"
            elif "orange" in filename_lower or "oranžov" in filename_lower:
                color = "orange"
            elif "purple" in filename_lower or "fialov" in filename_lower:
                color = "purple"
            elif "azure" in filename_lower or "azurov" in filename_lower:
                color = "azure"
            elif "white - studená" in filename_lower or "studena" in filename_lower:
                color = "white - studená"
            elif "white - teplá" in filename_lower or "tepla" in filename_lower:
                color = "white - teplá"
            elif "white" in filename_lower or "bil" in filename_lower:
                color = "white"

            return group, color

        return "unknown", "white"

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
        elif "fade" in event.path.lower():
            effect = "fade"
        else:
            # Pro krátké události (< 2s) použij fade efekt
            if event.length and ("0:00:01" in event.length or "0:00:02" in event.length):
                effect = "fade"

        # Map groups to fixtures
        fixture_keys = self._get_fixtures_for_group(group)

        logger.debug(f"Activating group '{group}' with color '{color}' -> {len(fixture_keys)} fixtures: {fixture_keys}")

        for key in fixture_keys:
            if key in self.fixtures:
                self.fixtures[key].set_color(rgb_color, intensity, effect)
                logger.info(f"🔴 Activated fixture {key} with color {rgb_color}, intensity {intensity}, effect {effect}")
                logger.info(f"🔴 Fixture {key} is_on: {self.fixtures[key].is_on}, color: {self.fixtures[key].color}")


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

        # Základní skupiny
        if group_lower in ["bodovky", "bodovka", "ceiling"]:
            return [k for k in self.fixtures.keys() if k.startswith("bodovka_")]
        elif group_lower in ["led_walls", "walls", "led_wall"]:
            return [k for k in self.fixtures.keys() if k.startswith("wall_spot_")]
        elif group_lower in ["led_lavice", "lavice", "bench"]:
            return [k for k in self.fixtures.keys() if k.startswith("led_lavice_")]
        elif group_lower in ["led_kamna", "led_oven", "oven", "kamna"]:
            return [k for k in self.fixtures.keys() if k.startswith("led_kamna_")]
        elif group_lower in ["moving_heads", "moving"]:
            return [k for k in self.fixtures.keys() if k.startswith("moving_head_")]
        elif group_lower in ["uv", "uv_lights"]:
            return [k for k in self.fixtures.keys() if k.startswith("uv_")]
        elif group_lower == "all":
            return list(self.fixtures.keys())

        # Jednotlivé světla
        elif "walls_" in group_lower:
            # Parse wall number - mapuj na dostupné wall spoty (1-8)
            try:
                wall_num = int(group_lower.split("_")[-1])
                # Mapuj wall čísla na dostupné spoty (máme jen 8 wall spotů)
                mapped_num = ((wall_num - 1) % 8) + 1
                fixture_key = f"wall_spot_{mapped_num}"
                if fixture_key in self.fixtures:
                    return [fixture_key]
                else:
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

        elif "mh_" in group_lower:
            # Moving heads
            try:
                mh_num = int(group_lower.split("_")[-1])
                if 1 <= mh_num <= 5:
                    fixture_key = f"moving_head_{mh_num}"
                    if fixture_key in self.fixtures:
                        return [fixture_key]
                return [k for k in self.fixtures.keys() if k.startswith("moving_head_")]
            except:
                return [k for k in self.fixtures.keys() if k.startswith("moving_head_")]

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
        """Vykreslí strukturu sauny."""
        # Sauna walls
        pygame.draw.rect(self.screen, self.sauna_wall_color, self.sauna_rect, 3)

        # Benches
        bench_rect = pygame.Rect(
            self.sauna_rect.left + 20,
            self.sauna_rect.bottom - 100,
            self.sauna_rect.width - 40,
            20,
        )
        pygame.draw.rect(self.screen, self.sauna_bench_color, bench_rect)

        # Stove area
        stove_rect = pygame.Rect(
            self.sauna_rect.right - 120, self.sauna_rect.bottom - 140, 80, 60
        )
        pygame.draw.rect(self.screen, (100, 50, 50), stove_rect)

        # Labels
        stove_text = self.font_small.render("KAMNA", True, self.text_color)
        self.screen.blit(stove_text, (stove_rect.x + 20, stove_rect.y + 25))

        bench_text = self.font_small.render("LAVICE", True, self.text_color)
        self.screen.blit(bench_text, (bench_rect.x + 10, bench_rect.y - 25))

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
                # Diamant pro moving heads
                points = [
                    (pos[0], pos[1] - size // 2),
                    (pos[0] + size // 2, pos[1]),
                    (pos[0], pos[1] + size // 2),
                    (pos[0] - size // 2, pos[1]),
                ]
                pygame.draw.polygon(self.screen, color, points)
                pygame.draw.polygon(self.screen, (100, 100, 100), points, 2)

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
        if hasattr(self, '_frame_count'):
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

"""Hlavní aplikace pro real-time vizualizaci DMX timeline."""

from __future__ import annotations

import sys
from pathlib import Path

import pygame

from ..logging import get_logger
from .sauna_renderer import SaunaRenderer
from .timeline_player import TimelinePlayer

logger = get_logger(__name__)


class VisualizerApp:
    """Hlavní aplikace vizualizátoru."""

    def __init__(self, timeline_path: Path, audio_path: Path):
        """Initialize visualizer app.

        Args:
            timeline_path: Cesta k .tml timeline souboru
            audio_path: Cesta k audio souboru
        """
        self.timeline_path = timeline_path
        self.audio_path = audio_path

        # Components
        self.player: TimelinePlayer | None = None
        self.renderer: SaunaRenderer | None = None

        # State
        self.running = False
        self.last_key_time = {}  # Track last key press times

        self._initialize()

    def _initialize(self) -> None:
        """Inicializuje komponenty."""
        try:
            # Create renderer
            self.renderer = SaunaRenderer(width=1400, height=900)

            # Create timeline player
            self.player = TimelinePlayer(self.timeline_path, self.audio_path)

            # Set up callbacks
            self.player.on_light_change = self._on_light_change
            self.player.on_time_update = self._on_time_update

            logger.info("Visualizer initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize visualizer: {e}")
            raise

    def _on_light_change(self, light_changes: dict) -> None:
        """Callback pro změny světel."""
        if self.renderer:
            current_time = self.player.current_time if self.player else 0
            self.renderer.update_lights(light_changes, current_time)

    def _on_time_update(self, current_time: float, duration: float) -> None:
        """Callback pro aktualizaci času."""
        # Můžeme zde přidat další logiku pro čas

    def run(self) -> None:
        """Spustí hlavní smyčku aplikace."""
        if not self.player or not self.renderer:
            logger.error("Visualizer not properly initialized")
            return

        self.running = True

        try:
            logger.info("Starting visualizer application")

            # Start playback
            self.player.play()

            # Main loop
            while self.running:
                # Handle pygame events
                if not self.renderer.handle_events():
                    self.running = False
                    break

                # Handle keyboard input
                self._handle_keyboard()

                # Get current state
                state = self.player.get_playback_state()

                # Render frame
                self.renderer.render(
                    current_time=state["current_time"],
                    duration=state["duration"],
                    active_events=state["active_events"],
                )

                # Control framerate
                self.renderer.clock.tick(60)  # 60 FPS

        except KeyboardInterrupt:
            logger.info("Visualizer interrupted by user")
        except Exception as e:
            logger.error(f"Visualizer error: {e}")
        finally:
            self._cleanup()

    def _handle_keyboard(self) -> None:
        """Zpracuje klávesové vstupy."""
        import time
        current_time = time.time()
        keys = pygame.key.get_pressed()

        # Spacebar: play/pause (single press)
        if keys[pygame.K_SPACE] and current_time - self.last_key_time.get('space', 0) > 0.3:
            if self.player.is_playing:
                self.player.pause()
            else:
                self.player.resume()
            self.last_key_time['space'] = current_time

        # Escape: quit
        if keys[pygame.K_ESCAPE]:
            self.running = False

        # R: restart (single press)
        if keys[pygame.K_r] and current_time - self.last_key_time.get('r', 0) > 0.3:
            self.player.seek(0.0)
            if not self.player.is_playing:
                self.player.resume()
            self.last_key_time['r'] = current_time

        # Left arrow: seek backward (rate limited)
        if keys[pygame.K_LEFT] and current_time - self.last_key_time.get('left', 0) > 0.1:
            new_time = max(0, self.player.current_time - 5.0)
            self.player.seek(new_time)
            self.last_key_time['left'] = current_time

        # Right arrow: seek forward (rate limited)
        if keys[pygame.K_RIGHT] and current_time - self.last_key_time.get('right', 0) > 0.1:
            new_time = min(self.player.duration, self.player.current_time + 5.0)
            self.player.seek(new_time)
            self.last_key_time['right'] = current_time

    def _cleanup(self) -> None:
        """Uklidí resources."""
        logger.info("Cleaning up visualizer")

        if self.player:
            self.player.stop()

        if self.renderer:
            self.renderer.cleanup()

    def stop(self) -> None:
        """Zastaví aplikaci."""
        self.running = False


def run_visualizer(timeline_path: Path, audio_path: Path) -> None:
    """Spustí vizualizátor.

    Args:
        timeline_path: Cesta k .tml souboru
        audio_path: Cesta k audio souboru
    """
    # Check if files exist
    if not timeline_path.exists():
        print(f"❌ Timeline file not found: {timeline_path}")
        return

    if not audio_path.exists():
        print(f"❌ Audio file not found: {audio_path}")
        return

    print(f"🎵 Loading timeline: {timeline_path.name}")
    print(f"🎼 Loading audio: {audio_path.name}")
    print("\n🎮 Controls:")
    print("   SPACE     - Play/Pause")
    print("   R         - Restart")
    print("   ←/→       - Seek backward/forward (5s)")
    print("   ESC       - Quit")
    print("\n🚀 Starting visualizer...")

    try:
        app = VisualizerApp(timeline_path, audio_path)
        app.run()

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Visualizer failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DMX Timeline Visualizer")
    parser.add_argument("timeline", type=Path, help="Path to .tml timeline file")
    parser.add_argument("audio", type=Path, help="Path to audio file")

    args = parser.parse_args()

    run_visualizer(args.timeline, args.audio)

"""Application settings and configuration management."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from .path_converter import PathConfig


class DMXSettings(BaseSettings):
    """Global DMX analyzer settings."""

    # Application settings
    app_name: str = Field(default="DMX Music Analyzer", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Audio analysis settings
    audio_sample_rate: int = Field(default=22050, description="Audio sample rate for analysis")
    hop_length: int = Field(default=512, description="Hop length for audio analysis")
    frame_length: int = Field(default=2048, description="Frame length for audio analysis")

    # Timeline generation settings
    min_event_duration: float = Field(default=0.5, description="Minimum event duration in seconds")
    max_event_duration: float = Field(default=5.0, description="Maximum event duration in seconds")
    default_light_timelines: int = Field(default=10, description="Default number of light timelines")

    # Path conversion settings
    export_platform: str = Field(default="windows", description="Target platform for export")
    path_config: PathConfig = Field(default_factory=PathConfig, description="Path conversion configuration")

    # Visualization settings
    visualization_fps: int = Field(default=60, description="Visualization frame rate")
    window_width: int = Field(default=1200, description="Visualization window width")
    window_height: int = Field(default=800, description="Visualization window height")

    # Fixture mapping
    fixture_groups: Dict[str, list[str]] = Field(
        default_factory=lambda: {
            "ceiling_spots": ["ceiling_spot_00", "ceiling_spot_01", "ceiling_spot_02", "ceiling_spot_03", "ceiling_spot_04", "ceiling_spot_05"],
            "wall_spots": ["wall_spot_00", "wall_spot_01", "wall_spot_02", "wall_spot_03", "wall_spot_04", "wall_spot_05", "wall_spot_06", "wall_spot_07"],
            "bench_leds": ["bench_led_00", "bench_led_01", "bench_led_02", "bench_led_03", "bench_led_04", "bench_led_05", "bench_led_06", "bench_led_07", "bench_led_08", "bench_led_09", "bench_led_10"],
            "stove_leds": ["stove_led_00", "stove_led_01"],
            "moving_heads": ["moving_head_00", "moving_head_01", "moving_head_02", "moving_head_03", "moving_head_04"],
            "uv_lights": ["uv_00", "uv_01"]
        },
        description="DMX fixture group mappings"
    )

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


class ExportConfig(BaseModel):
    """Configuration for timeline export."""

    target_platform: str = Field(default="windows", description="Target platform (windows/unix)")
    include_audio_reference: bool = Field(default=True, description="Include audio file reference in timeline")
    validate_scene_paths: bool = Field(default=True, description="Validate scene paths exist")
    convert_encoding: bool = Field(default=True, description="Convert text encoding for target platform")

    # Windows-specific settings
    windows_scene_base: str = Field(
        default=r"C:\Users\itbrn\TheLightingController\LightShows\Infinit Maximus - Jarda Vazny\generated_scenes_systematic",
        description="Windows base path for scene files"
    )
    windows_audio_base: str = Field(
        default=r"C:\Users\itbrn\TheLightingController\LightShows\Infinit Maximus - Jarda Vazny\audio",
        description="Windows base path for audio files"
    )

    # Development settings
    dev_scene_base: str = Field(
        default="generated_scenes_systematic",
        description="Development base path for scene files"
    )
    dev_audio_base: str = Field(
        default="audio",
        description="Development base path for audio files"
    )


# Global settings instance
_global_settings: Optional[DMXSettings] = None


def get_settings() -> DMXSettings:
    """Get global settings instance.

    Returns:
        DMXSettings instance
    """
    global _global_settings

    if _global_settings is None:
        _global_settings = DMXSettings()

    return _global_settings


def update_settings(**kwargs) -> DMXSettings:
    """Update global settings.

    Args:
        **kwargs: Settings to update

    Returns:
        Updated DMXSettings instance
    """
    global _global_settings

    current_settings = get_settings()
    updated_data = current_settings.model_dump()
    updated_data.update(kwargs)

    _global_settings = DMXSettings(**updated_data)
    return _global_settings
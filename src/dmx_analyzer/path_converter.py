"""Path converter for cross-platform timeline export.

Handles conversion between Unix paths (development) and Windows paths (target system).
Also handles CP1250 encoding for Czech characters.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field

from .logging import get_logger

logger = get_logger(__name__)


class PathConfig(BaseModel):
    """Configuration for path conversion."""

    # Base paths
    unix_base_path: str = Field(
        default="generated_scenes_systematic",
        description="Unix development base path"
    )
    windows_base_path: str = Field(
        default=r"C:\Users\itbrn\TheLightingController\LightShows\Infinit Maximus - Jarda Vazny\generated_scenes_systematic",
        description="Windows target system base path"
    )

    # Ceremonial structure settings
    ceremonial_name: Optional[str] = Field(
        default=None,
        description="Name of the ceremonial (e.g., 'Kokoti', 'Placata')"
    )
    windows_music_base: str = Field(
        default=r"C:\Users\itbrn\TheLightingController\LightShows\Infinit Maximus - Jarda Vazny\Music",
        description="Windows base path for music files"
    )
    unix_music_base: str = Field(
        default="music",
        description="Unix development base path for music files"
    )

    # Encoding settings
    source_encoding: str = Field(default="utf-8", description="Source encoding")
    target_encoding: str = Field(default="cp1250", description="Target encoding for Windows")

    # Path separator conversion
    convert_separators: bool = Field(default=True, description="Convert path separators")

    # Character replacement map for problematic chars
    char_replacements: Dict[str, str] = Field(
        default_factory=lambda: {
            "ý": "y",
            "ž": "z",
            "š": "s",
            "č": "c",
            "ř": "r",
            "ě": "e",
            "á": "a",
            "í": "i",
            "é": "e",
            "ó": "o",
            "ú": "u",
            "ů": "u",
            "ň": "n",
            "ť": "t",
            "ď": "d",
        },
        description="Character replacements for Windows compatibility"
    )


class PathConverter:
    """Converts paths between development (Unix) and target (Windows) systems."""

    def __init__(self, config: Optional[PathConfig] = None):
        """Initialize path converter.

        Args:
            config: Path conversion configuration
        """
        self.config = config or PathConfig()
        logger.debug("Initialized PathConverter with config: %s", self.config)

    def to_windows_path(self, unix_path: str) -> str:
        """Convert Unix development path to Windows target path.

        Args:
            unix_path: Unix-style path from development system

        Returns:
            Windows-compatible path for target system
        """
        # Start with the original path
        windows_path = unix_path

        # Replace base path if it matches
        if windows_path.startswith(self.config.unix_base_path):
            windows_path = windows_path.replace(
                self.config.unix_base_path,
                self.config.windows_base_path,
                1
            )

        # Convert forward slashes to backslashes
        if self.config.convert_separators:
            windows_path = windows_path.replace("/", "\\")

        # Handle Czech characters for CP1250 compatibility
        windows_path = self._replace_czech_chars(windows_path)

        logger.debug("Converted path: '%s' -> '%s'", unix_path, windows_path)
        return windows_path

    def to_unix_path(self, windows_path: str) -> str:
        """Convert Windows target path to Unix development path.

        Args:
            windows_path: Windows-style path from target system

        Returns:
            Unix-compatible path for development system
        """
        # Start with the original path
        unix_path = windows_path

        # Replace base path if it matches
        if unix_path.startswith(self.config.windows_base_path):
            unix_path = unix_path.replace(
                self.config.windows_base_path,
                self.config.unix_base_path,
                1
            )

        # Convert backslashes to forward slashes
        if self.config.convert_separators:
            unix_path = unix_path.replace("\\", "/")

        logger.debug("Converted path: '%s' -> '%s'", windows_path, unix_path)
        return unix_path

    def _replace_czech_chars(self, text: str) -> str:
        """Replace Czech characters with ASCII equivalents for Windows compatibility.

        Args:
            text: Text containing Czech characters

        Returns:
            Text with Czech characters replaced
        """
        result = text
        for czech_char, replacement in self.config.char_replacements.items():
            result = result.replace(czech_char, replacement)
            result = result.replace(czech_char.upper(), replacement.upper())

        return result

    def convert_scene_path(self, scene_path: str, target_platform: str = "windows") -> str:
        """Convert scene path for target platform.

        Args:
            scene_path: Original scene path
            target_platform: Target platform ("windows" or "unix")

        Returns:
            Converted scene path
        """
        if target_platform.lower() == "windows":
            return self.to_windows_path(scene_path)
        elif target_platform.lower() == "unix":
            return self.to_unix_path(scene_path)
        else:
            logger.warning("Unknown target platform: %s", target_platform)
            return scene_path

    def convert_audio_path(self, audio_path: str, target_platform: str = "windows") -> str:
        """Convert audio path for target platform with ceremonial support.

        Args:
            audio_path: Original audio path
            target_platform: Target platform ("windows" or "unix")

        Returns:
            Converted audio path with ceremonial directory structure
        """
        if target_platform.lower() == "windows":
            # Convert to Windows ceremonial structure
            windows_path = audio_path

            # Handle relative paths starting with "Music\"
            if windows_path.startswith("Music\\") or windows_path.startswith("Music/"):
                # This is already a relative path from the project base
                # Convert to full Windows path with ceremonial structure
                relative_part = windows_path[6:]  # Remove "Music\" or "Music/"

                if self.config.ceremonial_name:
                    safe_ceremonial_name = self.get_safe_filename(self.config.ceremonial_name)
                    windows_path = f"{self.config.windows_music_base}\\{safe_ceremonial_name}\\{relative_part}"
                else:
                    windows_path = f"{self.config.windows_music_base}\\{relative_part}"

            # Handle absolute Unix paths
            elif windows_path.startswith(self.config.unix_music_base):
                windows_path = windows_path.replace(
                    self.config.unix_music_base,
                    self.config.windows_music_base,
                    1
                )

                # Add ceremonial directory if specified
                if self.config.ceremonial_name:
                    safe_ceremonial_name = self.get_safe_filename(self.config.ceremonial_name)
                    music_base_with_sep = self.config.windows_music_base
                    if not music_base_with_sep.endswith("\\"):
                        music_base_with_sep += "\\"

                    ceremonial_path = f"{music_base_with_sep}{safe_ceremonial_name}\\"

                    if windows_path.startswith(self.config.windows_music_base):
                        remaining_path = windows_path[len(self.config.windows_music_base):].lstrip("\\")
                        windows_path = ceremonial_path + remaining_path

            # Convert separators and handle Czech chars
            if self.config.convert_separators:
                windows_path = windows_path.replace("/", "\\")

            windows_path = self._replace_czech_chars(windows_path)

            return windows_path

        elif target_platform.lower() == "unix":
            # Convert back to Unix
            unix_path = audio_path

            # Remove ceremonial directory structure for development
            if self.config.ceremonial_name and self.config.windows_music_base in unix_path:
                safe_ceremonial_name = self.get_safe_filename(self.config.ceremonial_name)
                ceremonial_pattern = f"\\{safe_ceremonial_name}\\"
                unix_path = unix_path.replace(ceremonial_pattern, "\\")

            # Replace base path
            if unix_path.startswith(self.config.windows_music_base):
                unix_path = unix_path.replace(
                    self.config.windows_music_base,
                    self.config.unix_music_base,
                    1
                )

            # Convert separators
            if self.config.convert_separators:
                unix_path = unix_path.replace("\\", "/")

            return unix_path
        else:
            logger.warning("Unknown target platform: %s", target_platform)
            return audio_path

    def validate_windows_encoding(self, path: str) -> tuple[bool, str]:
        """Validate that path can be encoded in CP1250.

        Args:
            path: Path to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            path.encode(self.config.target_encoding)
            return True, ""
        except UnicodeEncodeError as e:
            error_msg = f"Path contains characters not encodable in {self.config.target_encoding}: {e}"
            return False, error_msg

    def get_safe_filename(self, filename: str) -> str:
        """Get Windows-safe filename by replacing problematic characters.

        Args:
            filename: Original filename

        Returns:
            Windows-safe filename
        """
        # First handle Czech characters
        safe_name = self._replace_czech_chars(filename)

        # Replace other problematic characters for Windows
        problematic_chars = '<>:"|?*'
        for char in problematic_chars:
            safe_name = safe_name.replace(char, "_")

        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip(" .")

        return safe_name


# Global converter instance
_global_converter: Optional[PathConverter] = None


def get_path_converter(config: Optional[PathConfig] = None) -> PathConverter:
    """Get global path converter instance.

    Args:
        config: Optional configuration for new instance

    Returns:
        PathConverter instance
    """
    global _global_converter

    if _global_converter is None or config is not None:
        _global_converter = PathConverter(config)

    return _global_converter


def convert_path_for_export(path: str, target_platform: str = "windows") -> str:
    """Convenience function to convert path for export.

    Args:
        path: Path to convert
        target_platform: Target platform

    Returns:
        Converted path
    """
    converter = get_path_converter()
    return converter.convert_scene_path(path, target_platform)
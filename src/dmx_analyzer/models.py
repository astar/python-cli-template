"""Data models for DMX music analysis and timeline generation."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class SpeedType(Enum):
    """DMX timeline speed types."""

    BPM_BASED = 1
    PERCENTAGE = 2


class AudioFeatures(BaseModel):
    """Extracted audio features for analysis."""

    bpm: float = Field(..., description="Beats per minute")
    key: str | None = Field(None, description="Musical key")
    energy: float = Field(..., ge=0, le=1, description="Energy level (0-1)")
    valence: float = Field(..., ge=0, le=1, description="Valence/positivity (0-1)")
    loudness: float = Field(..., description="Average loudness in dB")
    tempo_stability: float = Field(..., ge=0, le=1, description="Tempo stability (0-1)")


class AudioAnalysis(BaseModel):
    """Complete audio analysis results."""

    file_path: Path
    duration: float = Field(..., gt=0, description="Duration in seconds")
    features: AudioFeatures
    beats: list[float] = Field(..., description="Beat times in seconds")
    spectral_centroids: list[float] = Field(
        ..., description="Spectral centroids over time"
    )
    onset_times: list[float] = Field(..., description="Note onset times")


class DMXFixture(BaseModel):
    """DMX fixture configuration."""

    id: int = Field(..., description="Fixture ID")
    name: str = Field(..., description="Fixture name")
    address: int = Field(..., ge=1, le=512, description="DMX address")
    model: str = Field(..., description="Fixture model")
    group: str = Field(..., description="Fixture group")
    channels: int = Field(..., gt=0, description="Number of DMX channels")


class DMXEvent(BaseModel):
    """Individual DMX timeline event."""

    timeline_index: int = Field(..., description="Timeline track number")
    start_time: str = Field(..., description="Start time (H:MM:SS.f format)")
    path: str = Field(..., description="Scene file path or command")
    length: str | None = Field(None, description="Event duration")
    speed: int = Field(100, ge=1, le=100, description="Effect speed percentage")
    speed_type: SpeedType = Field(
        SpeedType.PERCENTAGE, description="Speed calculation method"
    )
    fade_in: int | None = Field(None, description="Fade in time in milliseconds")
    fade_out: int | None = Field(None, description="Fade out time in milliseconds")
    bpm: int | None = Field(None, description="BPM for beat-synced events")
    volume: int | None = Field(None, description="Volume level")

    @validator("start_time")
    def validate_start_time(cls, v: str) -> str:
        """Validate time format."""
        try:
            # Parse H:MM:SS.f format
            parts = v.split(":")
            if len(parts) != 3:
                raise ValueError("Invalid time format")

            hours = int(parts[0])
            minutes = int(parts[1])

            # Handle seconds with milliseconds
            sec_parts = parts[2].split(".")
            seconds = int(sec_parts[0])

            if len(sec_parts) == 2:
                milliseconds = int(sec_parts[1])
            else:
                milliseconds = 0

            if not (
                0 <= hours <= 23
                and 0 <= minutes <= 59
                and 0 <= seconds <= 59
                and 0 <= milliseconds <= 999
            ):
                raise ValueError("Time values out of range")

            return v
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid time format: {v}") from e


class DMXTimeline(BaseModel):
    """Complete DMX timeline configuration."""

    version: str = Field("0.2", description="Timeline format version")
    max_time: str = Field("0:30:00", description="Maximum timeline duration")
    light_timelines: int = Field(10, description="Number of light timeline tracks")
    media_timelines: int = Field(1, description="Number of media timeline tracks")
    show_waveform: bool = Field(True, description="Show audio waveform")

    audio_file: str | None = Field(None, description="Audio file path")
    audio_length: str | None = Field(None, description="Audio file duration")

    events: list[DMXEvent] = Field(default_factory=list, description="Timeline events")
    fixtures: list[DMXFixture] = Field(default_factory=list, description="DMX fixtures")

    def add_event(self, event: DMXEvent) -> None:
        """Add an event to the timeline."""
        self.events.append(event)

    def get_events_at_time(self, time_str: str) -> list[DMXEvent]:
        """Get all events starting at a specific time."""
        return [event for event in self.events if event.start_time == time_str]

    def to_tml_format(self) -> str:
        """Convert timeline to .tml file format."""
        lines = []

        # Header section
        lines.append("[Params]")
        lines.append(f"Version = {self.version}")
        lines.append("CommentTimeLine = 0")
        lines.append(f"LightTimeLines = {self.light_timelines}")
        lines.append(f"MediaTimeLines = {self.media_timelines}")
        lines.append(f"ShowWaveForm = {1 if self.show_waveform else 0}")
        lines.append(f"MaxTime = {self.max_time}")
        lines.append("Zoom = 0")

        # Timeline labels
        lines.append("TimeLine_1 = V I D E O   P I C T U R E   T I M E L I N E")
        lines.append("TimeLine_2 = A U D I O   T I M E L I N E")
        for i in range(self.light_timelines):
            lines.append(
                f"TimeLine_{i + 3} = L I G H T   S C E N E   T I M E L I N E   #   {i + 1}"
            )

        # Audio event (if present)
        if self.audio_file and self.audio_length:
            lines.append("[Event_0]")
            lines.append("TimeLineIndex = 2")
            lines.append("StartTime = 0:00:00.0")
            lines.append(f"Path = {self.audio_file}")
            lines.append(f"Length = {self.audio_length}")

        # DMX events
        for i, event in enumerate(self.events, 1):
            lines.append(f"[Event_{i}]")
            lines.append(f"TimeLineIndex = {event.timeline_index}")
            lines.append(f"StartTime = {event.start_time}")
            lines.append(f"Path = {event.path}")

            if event.length:
                lines.append(f"Length = {event.length}")
            if event.fade_in:
                lines.append(f"FadeIn = {event.fade_in}")
            if event.fade_out:
                lines.append(f"FadeOut = {event.fade_out}")
            if event.bpm:
                lines.append(f"BPM = {event.bpm}")
            if event.volume is not None:
                lines.append(f"Volume = {event.volume}")

            lines.append(f"Speed = {event.speed}")
            lines.append(f"SpeedType = {event.speed_type.value}")

        return "\n".join(lines)


class GenerationConfig(BaseModel):
    """Configuration for timeline generation."""

    min_event_duration: float = Field(
        0.5, gt=0, description="Minimum event duration in seconds"
    )
    max_event_duration: float = Field(
        5.0, gt=0, description="Maximum event duration in seconds"
    )
    energy_threshold: float = Field(
        0.5, ge=0, le=1, description="Energy threshold for triggering events"
    )
    beat_sync: bool = Field(True, description="Sync events to beat times")
    color_intensity_mapping: bool = Field(
        True, description="Map audio features to light colors/intensity"
    )
    fixture_groups: dict[str, list[str]] = Field(
        default_factory=lambda: {
            "ceiling": ["Bodovka"],
            "walls": ["Spot_st\x1bna", "LED_walls"],
            "bench": ["LED_lavice"],
            "stove": ["LED_kamna"],
            "moving": ["Intimidator"],
            "effects": ["UV"],
        },
        description="Fixture group mappings",
    )

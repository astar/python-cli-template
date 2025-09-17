"""Music analysis module for extracting audio features and timing information."""

from __future__ import annotations

import warnings
from pathlib import Path

import librosa
import numpy as np
from mutagen import File as MutagenFile

from .logging import get_logger
from .models import AudioAnalysis
from .models import AudioFeatures

logger = get_logger(__name__)

# Suppress librosa warnings
warnings.filterwarnings("ignore", category=UserWarning, module="librosa")


class MusicAnalyzer:
    """Analyzes audio files to extract musical features and timing information."""

    def __init__(self, sample_rate: int = 22050):
        """Initialize the music analyzer.

        Args:
            sample_rate: Target sample rate for audio analysis
        """
        self.sample_rate = sample_rate

    def analyze_file(
        self, audio_path: Path, override_bpm: float | None = None
    ) -> AudioAnalysis:
        """Analyze an audio file and extract all relevant features.

        Args:
            audio_path: Path to the audio file
            override_bpm: If provided, use this BPM instead of detecting it

        Returns:
            Complete audio analysis results

        Raises:
            ValueError: If audio file cannot be loaded
            FileNotFoundError: If audio file doesn't exist
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info(f"Starting analysis of: {audio_path}")

        try:
            # Load audio file
            y, sr = librosa.load(str(audio_path), sr=self.sample_rate)
            duration = len(y) / sr

            logger.debug(f"Loaded audio: {duration:.2f}s at {sr}Hz")

            # Extract features
            features = self._extract_features(y, sr, override_bpm)

            # Extract timing information
            beats = self._extract_beats(y, sr, features.bpm)
            onset_times = self._extract_onsets(y, sr)
            spectral_centroids = self._extract_spectral_centroids(y, sr)

            analysis = AudioAnalysis(
                file_path=audio_path,
                duration=duration,
                features=features,
                beats=beats,
                onset_times=onset_times,
                spectral_centroids=spectral_centroids,
            )

            logger.info(
                f"Analysis complete - BPM: {features.bpm:.1f}, Duration: {duration:.1f}s"
            )
            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze audio file: {e}")
            raise ValueError(f"Could not analyze audio file: {e}") from e

    def _extract_features(
        self, y: np.ndarray, sr: int, override_bpm: float | None
    ) -> AudioFeatures:
        """Extract musical features from audio signal.

        Args:
            y: Audio time series
            sr: Sample rate
            override_bpm: Override detected BPM if provided

        Returns:
            Extracted audio features
        """
        # BPM detection
        if override_bpm:
            bpm = override_bpm
            tempo_stability = 1.0  # Assume perfect stability for override
            logger.debug(f"Using override BPM: {bpm}")
        else:
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            bpm = float(tempo)

            # Calculate tempo stability
            beat_intervals = np.diff(beats) * (60.0 / sr)
            if len(beat_intervals) > 1:
                tempo_stability = 1.0 - (
                    np.std(beat_intervals) / np.mean(beat_intervals)
                )
                tempo_stability = max(0.0, min(1.0, tempo_stability))
            else:
                tempo_stability = 0.5

            logger.debug(f"Detected BPM: {bpm:.1f}, stability: {tempo_stability:.2f}")

        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]

        # Energy (RMS)
        rms = librosa.feature.rms(y=y)[0]
        energy = float(np.mean(rms))

        # Loudness (approximate)
        loudness = float(librosa.amplitude_to_db(rms).mean())

        # Valence estimation (simplified)
        # Higher spectral centroid and energy generally correlate with positive valence
        centroid_normalized = np.mean(spectral_centroids) / (sr / 2)
        valence = (centroid_normalized + energy) / 2
        valence = max(0.0, min(1.0, valence))

        # Musical key detection (simplified)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key = self._estimate_key(chroma)

        return AudioFeatures(
            bpm=bpm,
            key=key,
            energy=energy,
            valence=valence,
            loudness=loudness,
            tempo_stability=tempo_stability,
        )

    def _extract_beats(self, y: np.ndarray, sr: int, bpm: float) -> list[float]:
        """Extract beat times from audio.

        Args:
            y: Audio time series
            sr: Sample rate
            bpm: Beats per minute

        Returns:
            List of beat times in seconds
        """
        _, beats = librosa.beat.beat_track(y=y, sr=sr, bpm=bpm)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        return beat_times.tolist()

    def _extract_onsets(self, y: np.ndarray, sr: int) -> list[float]:
        """Extract note onset times from audio.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            List of onset times in seconds
        """
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units="time")
        return onset_frames.tolist()

    def _extract_spectral_centroids(self, y: np.ndarray, sr: int) -> list[float]:
        """Extract spectral centroids over time.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            List of spectral centroids
        """
        centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        return centroids.tolist()

    def _estimate_key(self, chroma: np.ndarray) -> str | None:
        """Estimate musical key from chroma features.

        Args:
            chroma: Chroma feature matrix

        Returns:
            Estimated key or None if cannot determine
        """
        # Simplified key estimation using chroma profile matching
        key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        # Average chroma over time
        chroma_mean = np.mean(chroma, axis=1)

        # Find the most prominent chroma class
        max_chroma = np.argmax(chroma_mean)

        # Simple heuristic: if the max value is significantly higher than others, use it
        if chroma_mean[max_chroma] > np.mean(chroma_mean) + np.std(chroma_mean):
            return key_names[max_chroma]

        return None

    def get_audio_metadata(self, audio_path: Path) -> dict:
        """Extract metadata from audio file.

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with metadata
        """
        try:
            audio_file = MutagenFile(str(audio_path))
            if audio_file is None:
                return {}

            metadata = {}
            if hasattr(audio_file, "info"):
                metadata["duration"] = getattr(audio_file.info, "length", 0)
                metadata["bitrate"] = getattr(audio_file.info, "bitrate", 0)
                metadata["sample_rate"] = getattr(audio_file.info, "sample_rate", 0)

            # Extract common tags
            for key in ["title", "artist", "album", "date"]:
                if key in audio_file:
                    metadata[key] = str(audio_file[key][0]) if audio_file[key] else None

            return metadata

        except Exception as e:
            logger.warning(f"Could not extract metadata: {e}")
            return {}


def analyze_audio_file(
    audio_path: Path, override_bpm: float | None = None, sample_rate: int = 22050
) -> AudioAnalysis:
    """Convenience function to analyze an audio file.

    Args:
        audio_path: Path to the audio file
        override_bpm: Optional BPM override
        sample_rate: Target sample rate

    Returns:
        Complete audio analysis
    """
    analyzer = MusicAnalyzer(sample_rate=sample_rate)
    return analyzer.analyze_file(audio_path, override_bpm)

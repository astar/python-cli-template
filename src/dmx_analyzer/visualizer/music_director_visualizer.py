"""Advanced Music Director Visualizer - Inteligentní dirigent pro světelné show."""

from __future__ import annotations

import math
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
import pygame
import librosa
from dataclasses import dataclass

from ..logging import get_logger

logger = get_logger(__name__)


@dataclass
class LightingZone:
    """Definuje světelnou zónu v sauně."""
    name: str
    fixtures: List[str]
    frequency_range: Tuple[float, float]  # Hz
    physical_position: str  # 'floor', 'benches', 'walls', 'ceiling'
    priority: int  # 1-10, vyšší = důležitější
    color_profile: str  # 'warm', 'cool', 'dynamic'


@dataclass
class MusicFeature:
    """Hudební prvek s časovou stopou."""
    name: str
    values: np.ndarray  # Hodnoty v čase
    times: np.ndarray   # Časové značky
    threshold: float    # Práh pro aktivaci
    smoothing: float    # Vyhlazení 0-1


class MusicDirectorVisualizer:
    """Pokročilý vizualizátor s inteligentním řízením světel podle hudby."""

    def __init__(self, width: int = 1600, height: int = 1000):
        """Initialize music director visualizer."""
        self.width = width
        self.height = height

        # Pygame setup
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Advanced Music Director - DMX Visualizer")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # Colors
        self.bg_color = (20, 20, 25)
        self.text_color = (220, 220, 220)
        self.accent_color = (100, 200, 255)
        self.bass_color = (255, 100, 100)
        self.mid_color = (100, 255, 100)
        self.high_color = (100, 100, 255)

        # Layout areas
        self._setup_layout()

        # Music analysis
        self.audio_data: Optional[np.ndarray] = None
        self.sample_rate: int = 44100
        self.music_features: Dict[str, MusicFeature] = {}
        self.spectrogram: Optional[np.ndarray] = None
        self.freqs: Optional[np.ndarray] = None
        self.times: Optional[np.ndarray] = None

        # Lighting zones - Reálná mapa sauny
        self.lighting_zones = self._create_lighting_zones()

        # Configurable rules system
        self.mapping_rules = self._create_default_mapping_rules()

        # Current state
        self.current_time = 0.0
        self.duration = 0.0
        self.is_playing = False
        self.start_time = 0.0
        self.last_key_time = {}  # Track last key press times for rate limiting

        logger.info("Music Director Visualizer initialized")

    def _setup_layout(self) -> None:
        """Nastaví layout vizualizátoru."""
        # Hlavní oblasti
        self.spectrogram_rect = pygame.Rect(50, 50, 600, 300)      # Spektrogram
        self.sauna_3d_rect = pygame.Rect(700, 50, 500, 400)        # 3D sauna pohled
        self.waveforms_rect = pygame.Rect(50, 400, 600, 200)       # Průběhy frekvencí
        self.zones_control_rect = pygame.Rect(700, 500, 500, 200)  # Zóny ovládání
        self.timeline_rect = pygame.Rect(50, 650, 1150, 100)      # Timeline
        self.controls_rect = pygame.Rect(50, 800, 1150, 150)      # Ovládání a info

    def _create_lighting_zones(self) -> Dict[str, LightingZone]:
        """Vytvoří inteligentní mapování světelných zón."""
        zones = {
            'FLOOR_BASS': LightingZone(
                name="Podlaha - Basy",
                fixtures=['led_kamna_1', 'led_kamna_2'],
                frequency_range=(20, 120),
                physical_position='floor',
                priority=9,
                color_profile='warm'
            ),
            'BENCHES_RHYTHM': LightingZone(
                name="Lavice - Rytmus",
                fixtures=[f'led_lavice_{i}' for i in range(1, 12)],
                frequency_range=(60, 350),
                physical_position='benches',
                priority=8,
                color_profile='dynamic'
            ),
            'WALLS_LOW_MID': LightingZone(
                name="Stěny Dolní - Mid",
                fixtures=['wall_spot_1', 'wall_spot_2', 'wall_spot_7', 'wall_spot_8'],
                frequency_range=(250, 800),
                physical_position='walls_low',
                priority=6,
                color_profile='cool'
            ),
            'WALLS_HIGH_MID': LightingZone(
                name="Stěny Horní - Vokály",
                fixtures=['wall_spot_3', 'wall_spot_4', 'wall_spot_5', 'wall_spot_6'],
                frequency_range=(800, 3000),
                physical_position='walls_high',
                priority=7,
                color_profile='warm'
            ),
            'CEILING_HARMONY': LightingZone(
                name="Strop - Harmonie",
                fixtures=[f'bodovka_{i}' for i in [1, 2, 3, 4, 5, 9, 10, 11, 12]],
                frequency_range=(1000, 5000),
                physical_position='ceiling_outer',
                priority=5,
                color_profile='dynamic'
            ),
            'CEILING_BRILLIANCE': LightingZone(
                name="Strop Střed - Výšky",
                fixtures=['bodovka_6', 'bodovka_7', 'bodovka_8'],
                frequency_range=(4000, 15000),
                physical_position='ceiling_inner',
                priority=6,
                color_profile='cool'
            ),
            'MOVING_DYNAMICS': LightingZone(
                name="Moving - Dynamika",
                fixtures=[f'moving_head_{i}' for i in range(1, 6)],
                frequency_range=(100, 8000),  # Celé spektrum
                physical_position='moving',
                priority=10,
                color_profile='dynamic'
            ),
            'UV_SPECIAL': LightingZone(
                name="UV - Speciální",
                fixtures=['uv_1'],
                frequency_range=(50, 200),  # Jen silné basy
                physical_position='center',
                priority=4,
                color_profile='special'
            )
        }

        logger.info(f"Created {len(zones)} intelligent lighting zones")
        return zones

    def _create_default_mapping_rules(self) -> Dict:
        """Vytvoří výchozí konfigurovatená pravidla pro mapování."""
        rules = {
            'frequency_bands': {
                'sub_bass': (20, 60),
                'bass': (60, 250),
                'low_mid': (250, 500),
                'mid': (500, 2000),
                'high_mid': (2000, 4000),
                'presence': (4000, 6000),
                'brilliance': (6000, 20000)
            },
            'zone_assignments': {
                'FLOOR_BASS': ['sub_bass', 'bass'],
                'BENCHES_RHYTHM': ['bass', 'low_mid'],
                'WALLS_LOW_MID': ['low_mid', 'mid'],
                'WALLS_HIGH_MID': ['mid', 'high_mid'],
                'CEILING_HARMONY': ['mid', 'high_mid', 'presence'],
                'CEILING_BRILLIANCE': ['presence', 'brilliance'],
                'MOVING_DYNAMICS': ['bass', 'mid', 'high_mid'],  # Full spectrum
                'UV_SPECIAL': ['sub_bass']  # Only deep bass
            },
            'activation_thresholds': {
                'FLOOR_BASS': 0.3,
                'BENCHES_RHYTHM': 0.25,
                'WALLS_LOW_MID': 0.2,
                'WALLS_HIGH_MID': 0.2,
                'CEILING_HARMONY': 0.15,
                'CEILING_BRILLIANCE': 0.4,
                'MOVING_DYNAMICS': 0.3,
                'UV_SPECIAL': 0.5
            },
            'color_mappings': {
                'sub_bass': (255, 0, 0),      # Deep red
                'bass': (255, 100, 0),        # Orange
                'low_mid': (255, 255, 0),     # Yellow
                'mid': (0, 255, 0),           # Green
                'high_mid': (0, 255, 255),    # Cyan
                'presence': (0, 100, 255),    # Blue
                'brilliance': (255, 0, 255)  # Magenta
            },
            'effects_settings': {
                'bass_waves_enabled': True,
                'rhythm_pulses_enabled': True,
                'brilliance_sparkles_enabled': True,
                'moving_beams_enabled': True,
                'effect_intensity_multiplier': 1.0
            }
        }

        logger.info("Created configurable mapping rules")
        return rules

    def update_mapping_rules(self, new_rules: Dict) -> None:
        """Aktualizuje mapování pravidla za běhu."""
        # Deep merge new rules with existing ones
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value

        deep_update(self.mapping_rules, new_rules)
        logger.info(f"Updated mapping rules: {list(new_rules.keys())}")

    def load_audio(self, audio_path: Path) -> None:
        """Načte a analyzuje audio soubor."""
        logger.info(f"Loading and analyzing audio: {audio_path}")

        # Load audio
        self.audio_data, self.sample_rate = librosa.load(str(audio_path), sr=44100)
        self.duration = len(self.audio_data) / self.sample_rate

        # Vypočti spektrogram s vysokým rozlišením
        hop_length = 512
        n_fft = 2048

        self.spectrogram = np.abs(librosa.stft(
            self.audio_data,
            hop_length=hop_length,
            n_fft=n_fft
        ))

        self.freqs = librosa.fft_frequencies(sr=self.sample_rate, n_fft=n_fft)
        self.times = librosa.frames_to_time(
            np.arange(self.spectrogram.shape[1]),
            sr=self.sample_rate,
            hop_length=hop_length
        )

        # Analyzuj hudební prvky
        self._analyze_music_features()

        logger.info(f"Audio analyzed: {self.duration:.1f}s, {len(self.music_features)} features")

    def _analyze_music_features(self) -> None:
        """Analyzuje pokročilé hudební prvky."""
        hop_length = 512

        # RMS energie pro celkovou hlasitost
        rms = librosa.feature.rms(y=self.audio_data, hop_length=hop_length)[0]
        rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=self.sample_rate, hop_length=hop_length)

        self.music_features['energy'] = MusicFeature(
            name="Celková Energie",
            values=rms,
            times=rms_times,
            threshold=np.percentile(rms, 70),
            smoothing=0.1
        )

        # Spektrální centroid (jas zvuku)
        centroid = librosa.feature.spectral_centroid(y=self.audio_data, sr=self.sample_rate, hop_length=hop_length)[0]
        centroid_times = librosa.frames_to_time(np.arange(len(centroid)), sr=self.sample_rate, hop_length=hop_length)

        self.music_features['brightness'] = MusicFeature(
            name="Jas Zvuku",
            values=centroid,
            times=centroid_times,
            threshold=np.percentile(centroid, 60),
            smoothing=0.2
        )

        # Beat tracking
        tempo, beats = librosa.beat.beat_track(y=self.audio_data, sr=self.sample_rate, hop_length=hop_length)
        beat_times = librosa.frames_to_time(beats, sr=self.sample_rate, hop_length=hop_length)

        # Vytvoř beat strength signal
        beat_signal = np.zeros(len(rms_times))
        for beat_time in beat_times:
            # Najdi nejbližší time index
            idx = np.argmin(np.abs(rms_times - beat_time))
            if idx < len(beat_signal):
                beat_signal[idx] = 1.0

        self.music_features['beats'] = MusicFeature(
            name="Beaty",
            values=beat_signal,
            times=rms_times,
            threshold=0.5,
            smoothing=0.0
        )

        # Frekvenční pásma pro zóny
        for zone_name, zone in self.lighting_zones.items():
            freq_band = self._extract_frequency_band(zone.frequency_range)
            self.music_features[f'zone_{zone_name.lower()}'] = MusicFeature(
                name=f"Zóna {zone.name}",
                values=freq_band,
                times=self.times,
                threshold=np.percentile(freq_band, 65),
                smoothing=0.15
            )

    def _extract_frequency_band(self, freq_range: Tuple[float, float]) -> np.ndarray:
        """Extrahuje energii z konkrétního frekvenčního pásma."""
        if self.spectrogram is None or self.freqs is None:
            return np.array([])

        # Najdi indexy pro dané frekvenční pásmo
        freq_mask = (self.freqs >= freq_range[0]) & (self.freqs <= freq_range[1])

        # Průměrná energie v pásmu
        band_energy = np.mean(self.spectrogram[freq_mask, :], axis=0)

        # Vyhlazení - fallback if scipy not available
        try:
            from scipy.ndimage import gaussian_filter1d
            band_energy = gaussian_filter1d(band_energy, sigma=2.0)
        except ImportError:
            # Simple moving average as fallback
            window_size = 5
            padded = np.pad(band_energy, window_size//2, mode='edge')
            band_energy = np.convolve(padded, np.ones(window_size)/window_size, mode='valid')

        return band_energy

    def get_current_activation(self, current_time: float) -> Dict[str, float]:
        """Vrací aktuální aktivaci všech zón v daném čase podle konfigurovatelnách pravidel."""
        activations = {}

        # Get frequency band energies for current time
        band_energies = self._get_frequency_band_energies(current_time)

        for zone_name, zone in self.lighting_zones.items():
            # Get assigned frequency bands for this zone
            assigned_bands = self.mapping_rules['zone_assignments'].get(zone_name, [])
            threshold = self.mapping_rules['activation_thresholds'].get(zone_name, 0.3)

            # Calculate combined activation from assigned bands
            total_activation = 0.0
            for band_name in assigned_bands:
                if band_name in band_energies:
                    band_energy = band_energies[band_name]
                    # Normalize against threshold
                    band_activation = max(0.0, (band_energy - threshold) / threshold)
                    total_activation += band_activation

            # Average activation across assigned bands
            if assigned_bands:
                activation = min(1.0, total_activation / len(assigned_bands))
            else:
                # Fallback to original method
                feature_key = f'zone_{zone_name.lower()}'
                if feature_key in self.music_features:
                    feature = self.music_features[feature_key]
                    time_idx = np.argmin(np.abs(feature.times - current_time))
                    if time_idx < len(feature.values):
                        value = feature.values[time_idx]
                        activation = max(0.0, (value - feature.threshold) / feature.threshold)
                        activation = min(1.0, activation)
                    else:
                        activation = 0.0
                else:
                    activation = 0.0

            # Apply effect intensity multiplier
            activation *= self.mapping_rules['effects_settings']['effect_intensity_multiplier']
            activations[zone_name] = min(1.0, activation)

        return activations

    def _get_frequency_band_energies(self, current_time: float) -> Dict[str, float]:
        """Vrací energie jednotlivých frekvenčních pásem pro aktuální čas."""
        band_energies = {}

        if self.spectrogram is None or self.times is None:
            return band_energies

        # Find closest time index
        time_idx = np.argmin(np.abs(self.times - current_time))
        if time_idx >= self.spectrogram.shape[1]:
            return band_energies

        # Calculate energy for each frequency band
        for band_name, (low_freq, high_freq) in self.mapping_rules['frequency_bands'].items():
            # Find frequency indices
            freq_mask = (self.freqs >= low_freq) & (self.freqs <= high_freq)

            if np.any(freq_mask):
                # Average energy in this frequency band at current time
                band_energy = np.mean(self.spectrogram[freq_mask, time_idx])
                band_energies[band_name] = float(band_energy)
            else:
                band_energies[band_name] = 0.0

        return band_energies

    def run(self, audio_path: Path) -> None:
        """Spustí vizualizátor."""
        # Load and analyze audio
        self.load_audio(audio_path)

        # Load audio for playback
        pygame.mixer.music.load(str(audio_path))

        running = True
        self.start_time = time.time()

        logger.info("Starting Music Director Visualizer")

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.is_playing:
                            pygame.mixer.music.pause()
                            self.is_playing = False
                        else:
                            if pygame.mixer.music.get_busy():
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.play()
                            self.is_playing = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play()
                        self.current_time = 0.0
                        self.start_time = time.time()
                        self.is_playing = True

            # Handle continuous keyboard input (arrows for seeking)
            self._handle_keyboard()

            # Update time
            if self.is_playing:
                self.current_time = time.time() - self.start_time

            # Clamp time
            self.current_time = max(0, min(self.current_time, self.duration))

            # Render
            self._render_frame()

            # Control frame rate
            self.clock.tick(60)

        pygame.quit()
        logger.info("Music Director Visualizer closed")

    def _handle_keyboard(self) -> None:
        """Zpracuje klávesové vstupy pro posun v čase."""
        current_time = time.time()
        keys = pygame.key.get_pressed()

        # Left arrow: seek backward (rate limited)
        if (
            keys[pygame.K_LEFT]
            and current_time - self.last_key_time.get("left", 0) > 0.1
        ):
            new_time = max(0, self.current_time - 5.0)
            self.seek(new_time)
            self.last_key_time["left"] = current_time

        # Right arrow: seek forward (rate limited)
        if (
            keys[pygame.K_RIGHT]
            and current_time - self.last_key_time.get("right", 0) > 0.1
        ):
            new_time = min(self.duration, self.current_time + 5.0)
            self.seek(new_time)
            self.last_key_time["right"] = current_time

    def seek(self, time_seconds: float) -> None:
        """Přejde na specifický čas."""
        # Nastaví nový čas bez rušení audio přehrávání (jako u původního vizualizátoru)
        self.current_time = max(0, min(time_seconds, self.duration))

        # Aktualizuj start_time pro správnou synchronizaci
        self.start_time = time.time() - self.current_time

        logger.info(f"Seeked to {time_seconds:.1f}s (audio continues playing)")

    def _render_frame(self) -> None:
        """Vykreslí jeden frame."""
        # Clear screen
        self.screen.fill(self.bg_color)

        # Draw all components
        self._draw_spectrogram()
        self._draw_sauna_3d()
        self._draw_waveforms()
        self._draw_zone_controls()
        self._draw_timeline()
        self._draw_controls_info()

        # Update display
        pygame.display.flip()

    def _draw_spectrogram(self) -> None:
        """Vykreslí spektrogram."""
        # Title
        title = self.font_medium.render("SPEKTROGRAM - Real-time Analýza", True, self.text_color)
        self.screen.blit(title, (self.spectrogram_rect.x, self.spectrogram_rect.y - 25))

        # Draw border
        pygame.draw.rect(self.screen, self.accent_color, self.spectrogram_rect, 2)

        if self.spectrogram is not None and self.times is not None:
            # Time window pro zobrazení (±30 sekund od current_time)
            time_window = 30.0
            time_start = max(0, self.current_time - time_window)
            time_end = min(self.duration, self.current_time + time_window)

            # Najdi časové indexy
            start_idx = np.argmin(np.abs(self.times - time_start))
            end_idx = np.argmin(np.abs(self.times - time_end))

            if end_idx > start_idx:
                # Vezmi část spektrogramu
                spec_slice = self.spectrogram[:, start_idx:end_idx]

                # Frequency range pro zobrazení (do 8kHz)
                max_freq_idx = np.argmin(np.abs(self.freqs - 8000))
                spec_display = spec_slice[:max_freq_idx, :]

                # Normalizace pro vizualizaci
                spec_display = np.log1p(spec_display)  # Log scale
                spec_display = spec_display / np.max(spec_display) if np.max(spec_display) > 0 else spec_display

                # Vykreslení jako barevná mapa
                for y in range(0, spec_display.shape[0], 4):  # Skip every 4th frequency bin
                    for x in range(spec_display.shape[1]):
                        intensity = spec_display[y, x]

                        # Barva podle frekvence
                        freq_ratio = y / spec_display.shape[0]
                        if freq_ratio < 0.3:  # Bass
                            color = (int(255 * intensity), 0, 0)
                        elif freq_ratio < 0.7:  # Mid
                            color = (0, int(255 * intensity), 0)
                        else:  # High
                            color = (0, 0, int(255 * intensity))

                        # Pozice na obrazovce
                        screen_x = self.spectrogram_rect.x + (x * self.spectrogram_rect.width // spec_display.shape[1])
                        screen_y = self.spectrogram_rect.bottom - (y * self.spectrogram_rect.height // spec_display.shape[0])

                        pygame.draw.rect(self.screen, color, (screen_x, screen_y, 3, 3))

        # Current time marker
        if self.duration > 0:
            time_pos = (self.current_time - max(0, self.current_time - 30)) / 60  # Normalize to window
            marker_x = self.spectrogram_rect.x + int(time_pos * self.spectrogram_rect.width)
            pygame.draw.line(self.screen, (255, 255, 255),
                           (marker_x, self.spectrogram_rect.y),
                           (marker_x, self.spectrogram_rect.bottom), 2)

    def _draw_sauna_3d(self) -> None:
        """Vykreslí 3D pohled na saunu s aktivními zónami a geografickými efekty."""
        # Title
        title = self.font_medium.render("SAUNA - Zóny Aktivace & Fyzické Efekty", True, self.text_color)
        self.screen.blit(title, (self.sauna_3d_rect.x, self.sauna_3d_rect.y - 25))

        # Draw border
        pygame.draw.rect(self.screen, self.accent_color, self.sauna_3d_rect, 2)

        # Získej aktuální aktivace
        activations = self.get_current_activation(self.current_time)

        # Draw background sauna structure first
        self._draw_sauna_background()

        # Draw geographical effects
        self._draw_geographical_effects(activations)

        # Definice zón pro vykreslení
        zone_rects = {
            'FLOOR_BASS': pygame.Rect(self.sauna_3d_rect.x + 220, self.sauna_3d_rect.y + 320, 60, 30),
            'BENCHES_RHYTHM': [
                pygame.Rect(self.sauna_3d_rect.x + 50, self.sauna_3d_rect.y + 280, 400, 20),   # Bottom bench
                pygame.Rect(self.sauna_3d_rect.x + 80, self.sauna_3d_rect.y + 250, 340, 20),   # Mid bench
                pygame.Rect(self.sauna_3d_rect.x + 110, self.sauna_3d_rect.y + 220, 280, 20)   # Top bench
            ],
            'WALLS_LOW_MID': [
                pygame.Rect(self.sauna_3d_rect.x + 20, self.sauna_3d_rect.y + 150, 15, 100),   # Left wall
                pygame.Rect(self.sauna_3d_rect.x + 465, self.sauna_3d_rect.y + 150, 15, 100)   # Right wall
            ],
            'WALLS_HIGH_MID': [
                pygame.Rect(self.sauna_3d_rect.x + 80, self.sauna_3d_rect.y + 40, 340, 15),    # Top wall
                pygame.Rect(self.sauna_3d_rect.x + 80, self.sauna_3d_rect.y + 360, 340, 15)    # Bottom wall
            ],
            'CEILING_HARMONY': pygame.Rect(self.sauna_3d_rect.x + 80, self.sauna_3d_rect.y + 80, 340, 120),
            'CEILING_BRILLIANCE': pygame.Rect(self.sauna_3d_rect.x + 180, self.sauna_3d_rect.y + 130, 140, 60),
            'MOVING_DYNAMICS': [
                pygame.Rect(self.sauna_3d_rect.x + 150, self.sauna_3d_rect.y + 100, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 330, self.sauna_3d_rect.y + 100, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 240, self.sauna_3d_rect.y + 120, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 200, self.sauna_3d_rect.y + 180, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 280, self.sauna_3d_rect.y + 180, 20, 20)
            ],
            'UV_SPECIAL': pygame.Rect(self.sauna_3d_rect.x + 240, self.sauna_3d_rect.y + 160, 20, 20)
        }

        # Vykreslení zón s aktivací
        for zone_name, activation in activations.items():
            if zone_name in zone_rects:
                # Barva podle aktivace
                intensity = int(255 * activation)
                zone = self.lighting_zones[zone_name]

                if zone.color_profile == 'warm':
                    color = (intensity, intensity // 2, 0)
                elif zone.color_profile == 'cool':
                    color = (0, intensity // 2, intensity)
                elif zone.color_profile == 'special':
                    color = (intensity, 0, intensity)
                else:  # dynamic
                    color = (intensity, intensity, intensity // 2)

                rects = zone_rects[zone_name]
                if isinstance(rects, list):
                    for rect in rects:
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
                else:
                    pygame.draw.rect(self.screen, color, rects)
                    pygame.draw.rect(self.screen, (100, 100, 100), rects, 1)

    def _draw_sauna_background(self) -> None:
        """Vykreslí základní strukturu sauny podle reálných rozměrů."""
        # Reálné rozměry sauny: 8.5m × 7.6m
        # Scale factor pro zobrazení
        scale = 40  # pixels per meter
        offset_x = self.sauna_3d_rect.x + 50
        offset_y = self.sauna_3d_rect.y + 50

        # Transformace 3D koordinátů do 2D (kopíruje z původního vizualizátoru)
        def real_3d_to_2d(x_3d, z_3d):
            # Škálování a posunutí pro zobrazení
            screen_x = offset_x + int((x_3d + 4.25) * scale)  # Center na 4.25m
            screen_y = offset_y + int((z_3d + 3.8) * scale)   # Center na 3.8m
            return (screen_x, screen_y)

        # Sauna outline (walls) - reálný tvar
        wall_points = [
            real_3d_to_2d(-4.25, -3.8),  # Bottom left
            real_3d_to_2d(4.25, -3.8),   # Bottom right
            real_3d_to_2d(4.25, 3.8),    # Top right
            real_3d_to_2d(-4.25, 3.8),   # Top left
        ]
        pygame.draw.polygon(self.screen, (80, 60, 40), wall_points, 3)  # Wood color

        # Lavice (benches) podle reálných pozic
        bench_positions = [
            # Bottom bench
            [real_3d_to_2d(-3.8, -3.6), real_3d_to_2d(3.8, -3.6),
             real_3d_to_2d(3.8, -3.0), real_3d_to_2d(-3.8, -3.0)],
            # Mid bench
            [real_3d_to_2d(-3.5, -2.5), real_3d_to_2d(3.5, -2.5),
             real_3d_to_2d(3.5, -1.9), real_3d_to_2d(-3.5, -1.9)],
            # Top bench
            [real_3d_to_2d(-3.2, -1.4), real_3d_to_2d(3.2, -1.4),
             real_3d_to_2d(3.2, -0.8), real_3d_to_2d(-3.2, -0.8)],
        ]

        for bench_points in bench_positions:
            pygame.draw.polygon(self.screen, (100, 80, 60), bench_points, 1)

        # Kamna (stove) area - reálná pozice
        stove_center = real_3d_to_2d(0, -2.5)  # Střed kamen
        stove_rect = pygame.Rect(stove_center[0] - 30, stove_center[1] - 15, 60, 30)
        pygame.draw.rect(self.screen, (60, 60, 60), stove_rect, 2)

        # Vykreslí pozice všech světel jako malé tečky pro orientaci
        self._draw_fixture_positions(real_3d_to_2d)

    def _draw_fixture_positions(self, transform_func) -> None:
        """Vykreslí pozice všech světelných zařízení podle reálných koordinátů."""
        # Wall Spots (8 kusů) - čtvercové
        wall_spots_3d = [
            (-3.21, 2.55), (-2.02, 2.55), (2.02, 2.55), (3.21, 2.55),  # Horní stěna
            (-3.21, -2.60), (-2.02, -2.60), (2.02, -2.60), (3.21, -2.60)  # Dolní stěna
        ]
        for i, (x, z) in enumerate(wall_spots_3d):
            pos = transform_func(x, z)
            pygame.draw.rect(self.screen, (100, 100, 100),
                           (pos[0] - 8, pos[1] - 8, 16, 16), 1)

        # Bodovky (12 kusů) - kruhové
        bodovky_3d = [
            (-1.07, -2.90), (-1.07, -1.85), (-1.07, -0.75), (-1.07, 0.35), (-1.07, 1.35),
            (0.00, 1.35), (1.07, 1.35), (1.07, 0.35), (1.07, -0.75), (1.07, -1.85),
            (1.07, -2.90), (0.00, -3.67)
        ]
        for i, (x, z) in enumerate(bodovky_3d):
            pos = transform_func(x, z)
            pygame.draw.circle(self.screen, (100, 100, 100), pos, 10, 1)

        # Moving Heads (5 kusů) - diamantové
        moving_heads_3d = [
            (-2.37, -1.65), (-2.37, 0.69), (-0.16, 1.90), (2.21, 0.13), (2.21, -0.54)
        ]
        for i, (x, z) in enumerate(moving_heads_3d):
            pos = transform_func(x, z)
            diamond_points = [
                (pos[0], pos[1] - 8), (pos[0] + 8, pos[1]),
                (pos[0], pos[1] + 8), (pos[0] - 8, pos[1])
            ]
            pygame.draw.polygon(self.screen, (100, 100, 100), diamond_points, 1)

    def _draw_geographical_effects(self, activations: Dict[str, float]) -> None:
        """Vykreslí geografické efekty - kruhy, vlny, zóny."""
        center_x = self.sauna_3d_rect.centerx
        center_y = self.sauna_3d_rect.centery

        # Bass waves from floor/stove - expanding circles (if enabled)
        bass_activation = activations.get('FLOOR_BASS', 0.0)
        if (bass_activation > 0.3 and
            self.mapping_rules['effects_settings']['bass_waves_enabled']):
            for i in range(3):
                radius = int(50 + bass_activation * 100 + i * 30)
                alpha = max(0, int(255 * bass_activation - i * 80))
                if alpha > 0:
                    # Create surface for alpha blending
                    wave_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    color_with_alpha = (*self.bass_color[:3], alpha//3)
                    pygame.draw.circle(wave_surface, color_with_alpha, (radius, radius), radius, 3)
                    self.screen.blit(wave_surface, (center_x - radius, center_y - radius))

        # Rhythm pulses from benches - horizontal waves (if enabled)
        rhythm_activation = activations.get('BENCHES_RHYTHM', 0.0)
        if (rhythm_activation > 0.2 and
            self.mapping_rules['effects_settings']['rhythm_pulses_enabled']):
            wave_height = int(rhythm_activation * 50)
            for y_offset in [-40, 0, 40]:  # Three bench levels
                wave_y = center_y + y_offset
                # Draw wave across the width
                points = []
                for x in range(self.sauna_3d_rect.left + 80, self.sauna_3d_rect.right - 80, 5):
                    wave_offset = int(wave_height * math.sin((x - self.sauna_3d_rect.left) * 0.02 + self.current_time * 5))
                    points.append((x, wave_y + wave_offset))

                if len(points) > 1:
                    alpha = int(255 * rhythm_activation)
                    wave_surface = pygame.Surface(self.sauna_3d_rect.size, pygame.SRCALPHA)
                    color_with_alpha = (*self.mid_color[:3], alpha//2)
                    pygame.draw.lines(wave_surface, color_with_alpha, False, points, 3)
                    self.screen.blit(wave_surface, self.sauna_3d_rect.topleft)

        # High frequency sparkles from ceiling (if enabled)
        brilliance_activation = activations.get('CEILING_BRILLIANCE', 0.0)
        if (brilliance_activation > 0.4 and
            self.mapping_rules['effects_settings']['brilliance_sparkles_enabled']):
            import random
            random.seed(int(self.current_time * 10))  # Deterministic sparkles

            num_sparkles = int(brilliance_activation * 20)
            for _ in range(num_sparkles):
                spark_x = random.randint(self.sauna_3d_rect.x + 100, self.sauna_3d_rect.right - 100)
                spark_y = random.randint(self.sauna_3d_rect.y + 80, self.sauna_3d_rect.y + 200)
                spark_size = random.randint(2, 6)

                alpha = int(255 * brilliance_activation * random.uniform(0.5, 1.0))
                spark_surface = pygame.Surface((spark_size*2, spark_size*2), pygame.SRCALPHA)
                color_with_alpha = (*self.high_color[:3], alpha)
                pygame.draw.circle(spark_surface, color_with_alpha, (spark_size, spark_size), spark_size)
                self.screen.blit(spark_surface, (spark_x - spark_size, spark_y - spark_size))

        # Moving heads - rotating beams (if enabled)
        moving_activation = activations.get('MOVING_DYNAMICS', 0.0)
        if (moving_activation > 0.3 and
            self.mapping_rules['effects_settings']['moving_beams_enabled']):
            beam_length = int(moving_activation * 80)
            beam_angle = self.current_time * 2 * math.pi  # Rotate over time

            # Five moving heads positions
            mh_positions = [
                (self.sauna_3d_rect.x + 160, self.sauna_3d_rect.y + 110),
                (self.sauna_3d_rect.x + 340, self.sauna_3d_rect.y + 110),
                (self.sauna_3d_rect.x + 250, self.sauna_3d_rect.y + 130),
                (self.sauna_3d_rect.x + 210, self.sauna_3d_rect.y + 190),
                (self.sauna_3d_rect.x + 290, self.sauna_3d_rect.y + 190)
            ]

            for i, (mh_x, mh_y) in enumerate(mh_positions):
                angle = beam_angle + i * math.pi / 3  # Offset each head
                end_x = mh_x + int(beam_length * math.cos(angle))
                end_y = mh_y + int(beam_length * math.sin(angle))

                alpha = int(255 * moving_activation)
                beam_surface = pygame.Surface(self.sauna_3d_rect.size, pygame.SRCALPHA)
                color_with_alpha = (255, 255, 100, alpha//2)
                pygame.draw.line(beam_surface, color_with_alpha, (mh_x, mh_y), (end_x, end_y), 4)
                self.screen.blit(beam_surface, self.sauna_3d_rect.topleft)

        # Zone activation indicators with smooth transitions
        self._draw_zone_indicators(activations)

    def _draw_zone_indicators(self, activations: Dict[str, float]) -> None:
        """Vykreslí indikátory aktivace zón s plynulými přechody."""
        # Definice zón pro vykreslení
        zone_rects = {
            'FLOOR_BASS': pygame.Rect(self.sauna_3d_rect.x + 220, self.sauna_3d_rect.y + 320, 60, 30),
            'BENCHES_RHYTHM': [
                pygame.Rect(self.sauna_3d_rect.x + 70, self.sauna_3d_rect.y + 280, 360, 15),   # Bottom bench
                pygame.Rect(self.sauna_3d_rect.x + 90, self.sauna_3d_rect.y + 250, 320, 15),   # Mid bench
                pygame.Rect(self.sauna_3d_rect.x + 110, self.sauna_3d_rect.y + 220, 280, 15)   # Top bench
            ],
            'WALLS_LOW_MID': [
                pygame.Rect(self.sauna_3d_rect.x + 50, self.sauna_3d_rect.y + 150, 15, 100),   # Left wall
                pygame.Rect(self.sauna_3d_rect.x + 435, self.sauna_3d_rect.y + 150, 15, 100)   # Right wall
            ],
            'WALLS_HIGH_MID': [
                pygame.Rect(self.sauna_3d_rect.x + 70, self.sauna_3d_rect.y + 50, 360, 15),    # Top wall
                pygame.Rect(self.sauna_3d_rect.x + 70, self.sauna_3d_rect.y + 335, 360, 15)    # Bottom wall
            ],
            'CEILING_HARMONY': pygame.Rect(self.sauna_3d_rect.x + 100, self.sauna_3d_rect.y + 80, 300, 120),
            'CEILING_BRILLIANCE': pygame.Rect(self.sauna_3d_rect.x + 180, self.sauna_3d_rect.y + 130, 140, 60),
            'MOVING_DYNAMICS': [
                pygame.Rect(self.sauna_3d_rect.x + 150, self.sauna_3d_rect.y + 100, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 330, self.sauna_3d_rect.y + 100, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 240, self.sauna_3d_rect.y + 120, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 200, self.sauna_3d_rect.y + 180, 20, 20),
                pygame.Rect(self.sauna_3d_rect.x + 280, self.sauna_3d_rect.y + 180, 20, 20)
            ],
            'UV_SPECIAL': pygame.Rect(self.sauna_3d_rect.x + 240, self.sauna_3d_rect.y + 160, 20, 20)
        }

        # Vykreslení zón s aktivací
        for zone_name, activation in activations.items():
            if zone_name in zone_rects and activation > 0.1:
                # Barva podle aktivace a typu zóny
                intensity = int(255 * activation)
                zone = self.lighting_zones[zone_name]

                if zone.color_profile == 'warm':
                    color = (intensity, intensity // 2, 0)
                elif zone.color_profile == 'cool':
                    color = (0, intensity // 2, intensity)
                elif zone.color_profile == 'special':
                    color = (intensity, 0, intensity)
                else:  # dynamic
                    color = (intensity, intensity, intensity // 2)

                rects = zone_rects[zone_name]
                if isinstance(rects, list):
                    for rect in rects:
                        # Create surface for alpha blending
                        zone_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
                        color_with_alpha = (*color, int(255 * activation * 0.7))
                        zone_surface.fill(color_with_alpha)
                        self.screen.blit(zone_surface, rect.topleft)
                        pygame.draw.rect(self.screen, color, rect, 2)
                else:
                    zone_surface = pygame.Surface(rects.size, pygame.SRCALPHA)
                    color_with_alpha = (*color, int(255 * activation * 0.7))
                    zone_surface.fill(color_with_alpha)
                    self.screen.blit(zone_surface, rects.topleft)
                    pygame.draw.rect(self.screen, color, rects, 2)

    def _draw_waveforms(self) -> None:
        """Vykreslí průběhy jednotlivých frekvenčních pásem."""
        # Title
        title = self.font_medium.render("FREKVENČNÍ PÁSMA - Live Monitoring", True, self.text_color)
        self.screen.blit(title, (self.waveforms_rect.x, self.waveforms_rect.y - 25))

        # Draw border
        pygame.draw.rect(self.screen, self.accent_color, self.waveforms_rect, 2)

        # Průběhy pro důležité features
        features_to_show = ['energy', 'zone_floor_bass', 'zone_benches_rhythm', 'zone_ceiling_brilliance']
        colors = [(255, 255, 100), (255, 100, 100), (100, 255, 100), (100, 100, 255)]

        if self.music_features:
            # Time window
            time_window = 30.0
            time_start = max(0, self.current_time - time_window)
            time_end = min(self.duration, self.current_time + time_window)

            for i, (feature_name, color) in enumerate(zip(features_to_show, colors)):
                if feature_name in self.music_features:
                    feature = self.music_features[feature_name]

                    # Najdi časové indexy
                    start_idx = np.argmin(np.abs(feature.times - time_start))
                    end_idx = np.argmin(np.abs(feature.times - time_end))

                    if end_idx > start_idx:
                        values_slice = feature.values[start_idx:end_idx]
                        times_slice = feature.times[start_idx:end_idx]

                        # Normalizace pro zobrazení
                        if len(values_slice) > 0:
                            values_norm = (values_slice - np.min(values_slice))
                            if np.max(values_norm) > 0:
                                values_norm = values_norm / np.max(values_norm)

                            # Vykreslení křivky
                            y_offset = self.waveforms_rect.y + (i + 1) * (self.waveforms_rect.height // 5)
                            wave_height = self.waveforms_rect.height // 6

                            points = []
                            for j, (t, v) in enumerate(zip(times_slice, values_norm)):
                                x = self.waveforms_rect.x + int((t - time_start) / (time_end - time_start) * self.waveforms_rect.width)
                                y = y_offset - int(v * wave_height)
                                points.append((x, y))

                            if len(points) > 1:
                                pygame.draw.lines(self.screen, color, False, points, 2)

                            # Label
                            label = self.font_small.render(feature.name, True, color)
                            self.screen.blit(label, (self.waveforms_rect.x + 5, y_offset - wave_height - 15))

        # Current time marker
        if self.duration > 0:
            time_pos = (self.current_time - time_start) / (time_end - time_start)
            marker_x = self.waveforms_rect.x + int(time_pos * self.waveforms_rect.width)
            pygame.draw.line(self.screen, (255, 255, 255),
                           (marker_x, self.waveforms_rect.y),
                           (marker_x, self.waveforms_rect.bottom), 2)

    def _draw_zone_controls(self) -> None:
        """Vykreslí ovládání a stav zón."""
        # Title
        title = self.font_medium.render("ZÓNY - Aktuální Stav", True, self.text_color)
        self.screen.blit(title, (self.zones_control_rect.x, self.zones_control_rect.y - 25))

        # Draw border
        pygame.draw.rect(self.screen, self.accent_color, self.zones_control_rect, 2)

        # Získej aktivace
        activations = self.get_current_activation(self.current_time)

        # Zobraz stav každé zóny
        y_offset = self.zones_control_rect.y + 10
        for i, (zone_name, zone) in enumerate(self.lighting_zones.items()):
            activation = activations.get(zone_name, 0.0)

            # Zone name
            zone_text = self.font_small.render(f"{zone.name[:20]}", True, self.text_color)
            self.screen.blit(zone_text, (self.zones_control_rect.x + 10, y_offset))

            # Activation bar
            bar_rect = pygame.Rect(
                self.zones_control_rect.x + 200, y_offset,
                200, 15
            )
            pygame.draw.rect(self.screen, (60, 60, 60), bar_rect)

            # Fill bar
            fill_width = int(bar_rect.width * activation)
            if fill_width > 0:
                fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_width, bar_rect.height)

                # Barva podle typu zóny
                if 'BASS' in zone_name:
                    color = (255, 100, 100)
                elif 'RHYTHM' in zone_name:
                    color = (255, 255, 100)
                elif 'MID' in zone_name:
                    color = (100, 255, 100)
                elif 'BRILLIANCE' in zone_name:
                    color = (100, 100, 255)
                else:
                    color = (150, 150, 255)

                pygame.draw.rect(self.screen, color, fill_rect)

            pygame.draw.rect(self.screen, (100, 100, 100), bar_rect, 1)

            # Activation percentage
            perc_text = self.font_small.render(f"{activation:.1%}", True, self.text_color)
            self.screen.blit(perc_text, (bar_rect.right + 10, y_offset))

            y_offset += 22

    def _draw_timeline(self) -> None:
        """Vykreslí timeline s beats a důležitými momenty."""
        # Title
        title = self.font_medium.render("TIMELINE - Hudební Struktura", True, self.text_color)
        self.screen.blit(title, (self.timeline_rect.x, self.timeline_rect.y - 25))

        # Draw border
        pygame.draw.rect(self.screen, self.accent_color, self.timeline_rect, 2)

        if self.duration > 0:
            # Time markers
            for t in np.arange(0, self.duration, 30):  # Every 30 seconds
                x_pos = self.timeline_rect.x + int((t / self.duration) * self.timeline_rect.width)
                pygame.draw.line(self.screen, (100, 100, 100),
                               (x_pos, self.timeline_rect.y),
                               (x_pos, self.timeline_rect.bottom), 1)

                # Time label
                time_text = self.font_small.render(f"{int(t//60)}:{int(t%60):02d}", True, (150, 150, 150))
                self.screen.blit(time_text, (x_pos + 2, self.timeline_rect.bottom - 15))

            # Beat markers
            if 'beats' in self.music_features:
                beats_feature = self.music_features['beats']
                for i, (beat_time, beat_strength) in enumerate(zip(beats_feature.times, beats_feature.values)):
                    if beat_strength > 0.5:  # Only strong beats
                        x_pos = self.timeline_rect.x + int((beat_time / self.duration) * self.timeline_rect.width)
                        beat_height = int(beat_strength * 30)
                        pygame.draw.line(self.screen, (255, 200, 100),
                                       (x_pos, self.timeline_rect.bottom - beat_height),
                                       (x_pos, self.timeline_rect.bottom), 2)

            # Current time marker
            current_x = self.timeline_rect.x + int((self.current_time / self.duration) * self.timeline_rect.width)
            pygame.draw.line(self.screen, (255, 255, 255),
                           (current_x, self.timeline_rect.y),
                           (current_x, self.timeline_rect.bottom), 3)

    def _draw_controls_info(self) -> None:
        """Vykreslí ovládání a informace."""
        # Controls
        controls_text = [
            "OVLÁDÁNÍ: SPACE = Play/Pause | R = Restart | ←/→ = Seek (-5s/+5s) | ESC = Quit",
            f"ČAS: {int(self.current_time//60):02d}:{int(self.current_time%60):02d} / {int(self.duration//60):02d}:{int(self.duration%60):02d}",
            f"STATUS: {'▶️ PLAYING' if self.is_playing else '⏸️ PAUSED'}"
        ]

        y_offset = self.controls_rect.y + 10
        for text in controls_text:
            rendered_text = self.font_medium.render(text, True, self.text_color)
            self.screen.blit(rendered_text, (self.controls_rect.x + 10, y_offset))
            y_offset += 30

        # Music features info
        if self.music_features:
            features_info = f"ANALYZOVÁNO: {len(self.music_features)} hudebních prvků | {len(self.lighting_zones)} světelných zón"
            info_text = self.font_small.render(features_info, True, (150, 150, 150))
            self.screen.blit(info_text, (self.controls_rect.x + 10, y_offset + 10))

            # Configuration info
            effects_count = sum(1 for setting, enabled in self.mapping_rules['effects_settings'].items()
                              if setting.endswith('_enabled') and enabled)
            config_info = f"KONFIGURACE: {effects_count}/4 efektů aktivních | Intenzita: {self.mapping_rules['effects_settings']['effect_intensity_multiplier']:.1f}x"
            config_text = self.font_small.render(config_info, True, (150, 150, 150))
            self.screen.blit(config_text, (self.controls_rect.x + 10, y_offset + 30))

    def save_configuration(self, config_path: Path) -> None:
        """Uloží aktuální konfiguraci do souboru."""
        import json
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.mapping_rules, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def load_configuration(self, config_path: Path) -> None:
        """Načte konfiguraci ze souboru."""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_rules = json.load(f)
                self.update_mapping_rules(loaded_rules)
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")


def run_music_director(audio_path: Path) -> None:
    """Spustí Music Director Visualizer."""
    if not audio_path.exists():
        print(f"❌ Audio file not found: {audio_path}")
        return

    print(f"🎼 Starting Music Director Visualizer...")
    print(f"🎵 Audio: {audio_path.name}")
    print("🎹 Analyzing music and creating intelligent light mapping...")

    try:
        visualizer = MusicDirectorVisualizer()
        visualizer.run(audio_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Music Director failed: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python music_director_visualizer.py <audio_file>")
        sys.exit(1)

    audio_file = Path(sys.argv[1])
    run_music_director(audio_file)
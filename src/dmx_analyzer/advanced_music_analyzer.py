"""Advanced music analysis for spectacular lighting effects."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple

import librosa
import numpy as np
from scipy import signal
from scipy.ndimage import gaussian_filter1d

from .logging import get_logger

logger = get_logger(__name__)

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="librosa")


class FrequencyBands(NamedTuple):
    """Frequency band analysis results."""
    sub_bass: np.ndarray      # 20-60 Hz - hluboké basy pro masivní efekty
    bass: np.ndarray          # 60-250 Hz - kick drum, bass guitar
    low_mid: np.ndarray       # 250-500 Hz - spodní středy
    mid: np.ndarray           # 500-2000 Hz - vokály, hlavní melodie
    high_mid: np.ndarray      # 2000-4000 Hz - jasnost, detail
    presence: np.ndarray      # 4000-6000 Hz - přítomnost, čitelnost
    brilliance: np.ndarray    # 6000+ Hz - lesk, výšky


class SpectralFeatures(NamedTuple):
    """Advanced spectral analysis features."""
    spectral_centroid: np.ndarray      # Jas/tmavost zvuku
    spectral_bandwidth: np.ndarray     # Šířka zvuku
    spectral_contrast: np.ndarray      # Kontrast mezi peaky a valleys
    spectral_rolloff: np.ndarray       # Kde se koncentruje energie
    zero_crossing_rate: np.ndarray     # Hrubost/hladkost zvuku
    mfcc: np.ndarray                   # Timbre charakteristiky
    chroma: np.ndarray                 # Harmonický obsah
    tonnetz: np.ndarray                # Harmonické vztahy


class RhythmAnalysis(NamedTuple):
    """Rhythm and beat analysis results."""
    beat_times: np.ndarray             # Přesné časy beatů
    beat_strength: np.ndarray          # Síla jednotlivých beatů
    downbeats: np.ndarray              # Hlavní doby (1, 3 v 4/4)
    tempo_curve: np.ndarray            # Změny tempa v čase
    rhythm_pattern: np.ndarray         # Rytmický vzor
    syncopation: np.ndarray            # Míra synkopace


class DynamicsAnalysis(NamedTuple):
    """Dynamic range and energy analysis."""
    rms_energy: np.ndarray             # RMS energie
    peak_energy: np.ndarray            # Peak energie
    dynamic_range: float               # Celkový dynamický rozsah
    transients: np.ndarray             # Náhlé změny (údery, ataky)
    sustain_regions: np.ndarray        # Sustain oblasti
    silence_regions: np.ndarray        # Tiché oblasti


class AdvancedMusicAnalyzer:
    """Pokročilý analyzátor hudby pro spektakulární světelné efekty."""
    
    def __init__(self, sample_rate: int = 44100, hop_length: int = 512):
        """Initialize advanced analyzer.
        
        Args:
            sample_rate: Vyšší sample rate pro lepší kvalitu
            hop_length: Menší hop pro vyšší časové rozlišení
        """
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.frame_length = hop_length * 4
        
        # Frekvenční pásma pro spektrální analýzu
        self.frequency_bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250), 
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 6000),
            'brilliance': (6000, 22050)
        }
    
    def analyze_comprehensive(self, audio_path: Path) -> Dict:
        """Kompletní analýza pro maximální efekt.
        
        Args:
            audio_path: Cesta k audio souboru (MP3/WAV)
            
        Returns:
            Slovník s kompletní analýzou
        """
        logger.info(f"Spouštím pokročilou analýzu: {audio_path}")
        
        # Load audio with high quality
        y, sr = librosa.load(str(audio_path), sr=self.sample_rate, mono=True)
        
        logger.debug(f"Loaded: {len(y)/sr:.2f}s at {sr}Hz")
        
        analysis = {
            'duration': len(y) / sr,
            'sample_rate': sr,
            'frequency_bands': self._analyze_frequency_bands(y, sr),
            'spectral_features': self._extract_spectral_features(y, sr),
            'rhythm': self._analyze_rhythm(y, sr),
            'dynamics': self._analyze_dynamics(y, sr),
            'harmonic': self._analyze_harmonic_content(y, sr),
            'structure': self._detect_musical_structure(y, sr),
            'emotional_content': self._analyze_emotional_content(y, sr)
        }
        
        logger.info("Pokročilá analýza dokončena")
        return analysis
    
    def _analyze_frequency_bands(self, y: np.ndarray, sr: int) -> FrequencyBands:
        """Analýza frekvenčních pásem pro cílené světelné efekty."""
        
        # Výpočet spectrogramu s vysokým rozlišením
        S = np.abs(librosa.stft(y, hop_length=self.hop_length, 
                               n_fft=4096))  # Vyšší FFT pro lepší frekvenční rozlišení
        
        freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)
        times = librosa.frames_to_time(np.arange(S.shape[1]), 
                                      sr=sr, hop_length=self.hop_length)
        
        bands = {}
        for band_name, (low_freq, high_freq) in self.frequency_bands.items():
            # Najdi indexy pro dané frekvenční pásmo
            freq_mask = (freqs >= low_freq) & (freqs <= high_freq)
            
            # Průměrná energie v pásmu
            band_energy = np.mean(S[freq_mask, :], axis=0)
            
            # Vyhlazení pro plynulejší přechody
            band_energy = gaussian_filter1d(band_energy, sigma=1.0)
            
            bands[band_name] = band_energy
        
        return FrequencyBands(**bands)
    
    def _extract_spectral_features(self, y: np.ndarray, sr: int) -> SpectralFeatures:
        """Extrakce pokročilých spektrálních charakteristik."""
        
        # Spektrální centroid (jas zvuku)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr, 
                                                    hop_length=self.hop_length)[0]
        
        # Spektrální bandwidth (šířka zvuku)
        bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr,
                                                      hop_length=self.hop_length)[0]
        
        # Spektrální kontrast (peak vs valley)
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr,
                                                    hop_length=self.hop_length)
        
        # Spektrální rolloff (kde je 85% energie)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr,
                                                  hop_length=self.hop_length)[0]
        
        # Zero crossing rate (hrubost zvuku)
        zcr = librosa.feature.zero_crossing_rate(y=y, 
                                                hop_length=self.hop_length)[0]
        
        # MFCC pro timbre
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13,
                                   hop_length=self.hop_length)
        
        # Chroma pro harmonický obsah
        chroma = librosa.feature.chroma_stft(y=y, sr=sr,
                                           hop_length=self.hop_length)
        
        # Tonnetz pro harmonické vztahy
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        
        return SpectralFeatures(
            spectral_centroid=centroid,
            spectral_bandwidth=bandwidth,
            spectral_contrast=contrast,
            spectral_rolloff=rolloff,
            zero_crossing_rate=zcr,
            mfcc=mfcc,
            chroma=chroma,
            tonnetz=tonnetz
        )
    
    def _analyze_rhythm(self, y: np.ndarray, sr: int) -> RhythmAnalysis:
        """Pokročilá rytmická analýza."""
        
        # Beat tracking s vysokou přesností
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, 
                                             hop_length=self.hop_length,
                                             trim=False)
        
        beat_times = librosa.frames_to_time(beats, sr=sr, 
                                          hop_length=self.hop_length)
        
        # Síla beatů
        onset_envelope = librosa.onset.onset_strength(y=y, sr=sr,
                                                     hop_length=self.hop_length)
        beat_strength = onset_envelope[beats] if len(beats) > 0 else np.array([])
        
        # Detekce downbeatů (hlavní doby)
        try:
            _, downbeats = librosa.beat.beat_track(y=y, sr=sr, 
                                                 hop_length=self.hop_length,
                                                 trim=False)
            downbeat_times = librosa.frames_to_time(downbeats, sr=sr,
                                                  hop_length=self.hop_length)
        except:
            downbeat_times = beat_times[::4] if len(beat_times) > 0 else np.array([])
        
        # Tempo curve (změny tempa)
        tempo_curve = self._estimate_tempo_curve(y, sr)
        
        # Rytmický vzor
        rhythm_pattern = self._extract_rhythm_pattern(onset_envelope, beats)
        
        # Synkopace
        syncopation = self._measure_syncopation(beat_times, onset_envelope, sr)
        
        return RhythmAnalysis(
            beat_times=beat_times,
            beat_strength=beat_strength,
            downbeats=downbeat_times,
            tempo_curve=tempo_curve,
            rhythm_pattern=rhythm_pattern,
            syncopation=syncopation
        )
    
    def _analyze_dynamics(self, y: np.ndarray, sr: int) -> DynamicsAnalysis:
        """Analýza dynamiky a energie."""
        
        # RMS energie
        rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
        
        # Peak energie (lokální maxima)
        peak_energy = np.maximum(rms, np.roll(rms, 1))
        peak_energy = np.maximum(peak_energy, np.roll(peak_energy, -1))
        
        # Dynamický rozsah
        dynamic_range = np.max(rms) - np.min(rms[rms > 0]) if np.any(rms > 0) else 0
        
        # Transients (náhlé změny)
        transients = self._detect_transients(y, sr)
        
        # Sustain regiony (stabilní oblasti)
        sustain_regions = self._detect_sustain_regions(rms)
        
        # Tiché oblasti
        silence_threshold = np.percentile(rms[rms > 0], 10) if np.any(rms > 0) else 0
        silence_regions = rms < silence_threshold
        
        return DynamicsAnalysis(
            rms_energy=rms,
            peak_energy=peak_energy,
            dynamic_range=dynamic_range,
            transients=transients,
            sustain_regions=sustain_regions,
            silence_regions=silence_regions
        )
    
    def _analyze_harmonic_content(self, y: np.ndarray, sr: int) -> Dict:
        """Analýza harmonického obsahu."""
        
        # Harmonic vs percussive separation
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        
        # Chroma features pro harmonický obsah
        chroma = librosa.feature.chroma_stft(y=y_harmonic, sr=sr,
                                           hop_length=self.hop_length)
        
        # Key detection
        key_profile = np.mean(chroma, axis=1)
        key_correlations = []
        
        # Major and minor key templates (simplified)
        major_template = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
        minor_template = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        
        for shift in range(12):
            major_corr = np.corrcoef(key_profile, np.roll(major_template, shift))[0, 1]
            minor_corr = np.corrcoef(key_profile, np.roll(minor_template, shift))[0, 1]
            key_correlations.append((shift, 'major', major_corr))
            key_correlations.append((shift, 'minor', minor_corr))
        
        # Best key match
        best_key = max(key_correlations, key=lambda x: x[2] if not np.isnan(x[2]) else -1)
        
        return {
            'harmonic_component': y_harmonic,
            'percussive_component': y_percussive,
            'chroma': chroma,
            'key_profile': key_profile,
            'estimated_key': best_key,
            'harmonic_strength': np.mean(np.abs(y_harmonic)) / np.mean(np.abs(y)),
            'percussive_strength': np.mean(np.abs(y_percussive)) / np.mean(np.abs(y))
        }
    
    def _detect_musical_structure(self, y: np.ndarray, sr: int) -> Dict:
        """Detekce struktury skladby (intro, verse, chorus, outro)."""
        
        # Self-similarity matrix
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=self.hop_length)
        
        # Compute self-similarity
        similarity_matrix = np.dot(chroma.T, chroma)
        similarity_matrix = (similarity_matrix + similarity_matrix.T) / 2
        
        # Detect segments using Laplacian segmentation
        try:
            boundaries = librosa.segment.agglomerative(similarity_matrix, k=8)
            boundary_times = librosa.frames_to_time(boundaries, sr=sr,
                                                  hop_length=self.hop_length)
        except:
            # Fallback: divide into equal segments
            duration = len(y) / sr
            boundary_times = np.linspace(0, duration, 5)
        
        # Estimate section types based on energy and spectral characteristics
        sections = self._classify_sections(y, sr, boundary_times)
        
        return {
            'boundaries': boundary_times,
            'sections': sections,
            'similarity_matrix': similarity_matrix
        }
    
    def _analyze_emotional_content(self, y: np.ndarray, sr: int) -> Dict:
        """Analýza emocionálního obsahu hudby."""
        
        # Valence (pozitivita/negativita)
        # Vyšší centroid + vyšší energia = pozitivnější
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        rms = librosa.feature.rms(y=y)[0]
        
        valence = (np.mean(centroid) / (sr/2) + np.mean(rms)) / 2
        valence = np.clip(valence, 0, 1)
        
        # Arousal (vzrušení/klid)
        # Vyšší tempo + vyšší energie = vyšší arousal
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        arousal = (tempo / 200 + np.mean(rms)) / 2
        arousal = np.clip(arousal, 0, 1)
        
        # Emocionální kategorization
        if valence > 0.5 and arousal > 0.5:
            emotion = "energetic_happy"  # Červené/oranžové světla
        elif valence > 0.5 and arousal <= 0.5:
            emotion = "peaceful_happy"   # Žluté/teplé bílé světla
        elif valence <= 0.5 and arousal > 0.5:
            emotion = "aggressive_sad"   # Červené/fialové světla
        else:
            emotion = "melancholic"      # Modré/studené světla
        
        return {
            'valence': valence,
            'arousal': arousal,
            'emotion_category': emotion,
            'tempo': float(tempo)
        }
    
    def _estimate_tempo_curve(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Odhad změn tempa v čase."""
        
        # Sliding window tempo analysis
        window_length = sr * 4  # 4 second windows
        hop_length = sr * 1     # 1 second hop
        
        tempo_curve = []
        for start in range(0, len(y) - window_length, hop_length):
            window = y[start:start + window_length]
            try:
                tempo, _ = librosa.beat.beat_track(y=window, sr=sr)
                tempo_curve.append(float(tempo))
            except:
                tempo_curve.append(120.0)  # Default tempo
        
        return np.array(tempo_curve)
    
    def _extract_rhythm_pattern(self, onset_envelope: np.ndarray, 
                               beats: np.ndarray) -> np.ndarray:
        """Extrakce rytmického vzoru."""
        
        if len(beats) < 2:
            return np.array([])
        
        # Average beat interval
        beat_interval = np.mean(np.diff(beats))
        
        # Pattern length (one measure)
        pattern_length = int(beat_interval * 4)
        
        # Extract pattern around strong beats
        patterns = []
        for beat in beats[::4]:  # Every 4th beat (downbeat)
            if beat + pattern_length < len(onset_envelope):
                pattern = onset_envelope[beat:beat + pattern_length]
                patterns.append(pattern)
        
        if patterns:
            return np.mean(patterns, axis=0)
        else:
            return np.array([])
    
    def _measure_syncopation(self, beat_times: np.ndarray, 
                           onset_envelope: np.ndarray, sr: int) -> np.ndarray:
        """Měření synkopace (off-beat akcenty)."""
        
        if len(beat_times) < 2:
            return np.array([])
        
        # Convert beat times to frames
        beat_frames = librosa.time_to_frames(beat_times, sr=sr, 
                                           hop_length=self.hop_length)
        
        syncopation = []
        for i in range(len(beat_frames) - 1):
            start_frame = beat_frames[i]
            end_frame = beat_frames[i + 1]
            
            # Find off-beat positions
            mid_frame = (start_frame + end_frame) // 2
            quarter_frame = (start_frame + mid_frame) // 2
            three_quarter_frame = (mid_frame + end_frame) // 2
            
            # Measure energy at off-beat positions
            off_beat_energy = 0
            for frame in [quarter_frame, mid_frame, three_quarter_frame]:
                if 0 <= frame < len(onset_envelope):
                    off_beat_energy += onset_envelope[frame]
            
            # Compare to on-beat energy
            on_beat_energy = onset_envelope[start_frame] if start_frame < len(onset_envelope) else 0
            
            # Syncopation ratio
            if on_beat_energy > 0:
                sync_ratio = off_beat_energy / (3 * on_beat_energy)
            else:
                sync_ratio = 0
            
            syncopation.append(sync_ratio)
        
        return np.array(syncopation)
    
    def _detect_transients(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Detekce transientů (náhlých změn)."""
        
        # Onset detection s vysokou citlivostí
        onsets = librosa.onset.onset_detect(y=y, sr=sr, 
                                          hop_length=self.hop_length,
                                          delta=0.1, wait=1)
        
        return librosa.frames_to_time(onsets, sr=sr, hop_length=self.hop_length)
    
    def _detect_sustain_regions(self, rms: np.ndarray) -> np.ndarray:
        """Detekce sustain regionů."""
        
        # Smooth RMS
        smooth_rms = gaussian_filter1d(rms, sigma=3.0)
        
        # Find regions with stable energy
        energy_diff = np.abs(np.diff(smooth_rms))
        stable_threshold = np.percentile(energy_diff, 25)
        
        sustain_mask = np.zeros_like(rms, dtype=bool)
        sustain_mask[1:] = energy_diff < stable_threshold
        
        return sustain_mask
    
    def _classify_sections(self, y: np.ndarray, sr: int, 
                          boundary_times: np.ndarray) -> List[Dict]:
        """Klasifikace hudebních sekcí."""
        
        sections = []
        
        for i in range(len(boundary_times) - 1):
            start_time = boundary_times[i]
            end_time = boundary_times[i + 1]
            
            # Extract segment
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment = y[start_sample:end_sample]
            
            if len(segment) == 0:
                continue
            
            # Analyze segment characteristics
            rms_energy = np.mean(librosa.feature.rms(y=segment))
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=segment, sr=sr))
            
            # Classify based on energy and spectral characteristics
            if i == 0:
                section_type = "intro"
            elif i == len(boundary_times) - 2:
                section_type = "outro" 
            elif rms_energy > np.percentile([np.mean(librosa.feature.rms(y=y))], 75):
                section_type = "chorus"
            else:
                section_type = "verse"
            
            sections.append({
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time,
                'type': section_type,
                'energy': float(rms_energy),
                'brightness': float(spectral_centroid)
            })
        
        return sections


def analyze_for_lighting(audio_path: Path) -> Dict:
    """Hlavní funkce pro analýzu hudby pro světelné efekty.
    
    Args:
        audio_path: Cesta k MP3 nebo WAV souboru
        
    Returns:
        Kompletní analýza optimalizovaná pro světelné efekty
    """
    analyzer = AdvancedMusicAnalyzer(sample_rate=44100, hop_length=256)
    return analyzer.analyze_comprehensive(audio_path)
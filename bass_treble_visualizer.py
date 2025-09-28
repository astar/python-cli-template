#!/usr/bin/env python3
"""
Bass & Treble Reactive Visualizer
Vytvoří jednoduchý timeline kde:
- Basy (nízké frekvence) = červené světla (LED Kamna, LED Lavice)
- Výšky (vysoké frekvence) = modré světla (Bodovky)
"""

import librosa
import numpy as np
from pathlib import Path
import json
from typing import List, Tuple

class BassTrableVisualizer:
    """Generátor bass/treble reaktivní vizualizace"""

    def __init__(self, audio_path: str):
        self.audio_path = Path(audio_path)
        self.timeline_events = []
        self.event_counter = 0

        # Načteme audio
        print(f"🎵 Načítám audio: {self.audio_path}")
        self.y, self.sr = librosa.load(str(self.audio_path), sr=44100)
        self.duration = len(self.y) / self.sr
        print(f"   Délka: {self.duration:.1f} sekund")

        # Systematická struktura (podle našich generovaných scene)
        self.load_systematic_structure()

    def load_systematic_structure(self):
        """Načte systematickou strukturu světel"""
        structure_file = Path("generated_scenes_systematic/systematic_structure.json")
        if structure_file.exists():
            with open(structure_file, 'r', encoding='utf-8') as f:
                self.structure = json.load(f)
        else:
            print("❌ Systematic structure not found. Creating basic structure.")
            self.structure = {"individual": {}}

    def analyze_audio_frequencies(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Analyzuje basy a výšky v audio"""
        print("🔍 Analyzujem frekvence...")

        # STFT pro frekvenční analýzu
        hop_length = 512
        stft = librosa.stft(self.y, hop_length=hop_length)
        magnitude = np.abs(stft)

        # Frekvenční rozsahy
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)

        # Bass: 20-250 Hz (nízké frekvence)
        bass_indices = np.where((freqs >= 20) & (freqs <= 250))[0]
        bass_energy = np.mean(magnitude[bass_indices], axis=0)

        # Treble: 4000-20000 Hz (vysoké frekvence)
        treble_indices = np.where((freqs >= 4000) & (freqs <= 20000))[0]
        treble_energy = np.mean(magnitude[treble_indices], axis=0)

        # Čas pro každý frame
        times = librosa.frames_to_time(np.arange(len(bass_energy)),
                                      sr=self.sr, hop_length=hop_length)

        print(f"   Bass energie: max={bass_energy.max():.2f}, mean={bass_energy.mean():.2f}")
        print(f"   Treble energie: max={treble_energy.max():.2f}, mean={treble_energy.mean():.2f}")

        return times, bass_energy, treble_energy

    def detect_peaks(self, energy: np.ndarray, threshold_factor: float = 1.5) -> np.ndarray:
        """Detekuje vrcholy v energii"""
        try:
            from scipy.signal import find_peaks
            # Dynamický threshold
            threshold = np.mean(energy) * threshold_factor
            peaks, _ = find_peaks(energy, height=threshold, distance=10)
            return peaks
        except ImportError:
            # Fallback - jednoduchá peak detection bez scipy
            threshold = np.mean(energy) * threshold_factor
            peaks = []
            for i in range(1, len(energy) - 1):
                if (energy[i] > energy[i-1] and
                    energy[i] > energy[i+1] and
                    energy[i] > threshold):
                    peaks.append(i)
            return np.array(peaks)

    def get_bass_fixtures(self) -> List[str]:
        """Vrátí fixture paths pro bass (červené světla)"""
        bass_fixtures = []

        # LED Kamna - pro hluboké basy (známe že máme led_kamna_41, led_kamna_42)
        kamna_ids = ["41", "42"]
        for kamna_id in kamna_ids:
            scene_path = f"generated_scenes_systematic/individual/led_kamna_{kamna_id}/red_static.scex"
            if Path(scene_path).exists():
                bass_fixtures.append(scene_path)

        # LED Walls - pro střední basy (0-10)
        for wall_id in range(10):  # 0-9
            scene_path = f"generated_scenes_systematic/individual/led_wall_{wall_id:02d}/red_static.scex"
            if Path(scene_path).exists():
                bass_fixtures.append(scene_path)

        # LED Wall 99 - speciální případ
        scene_path = "generated_scenes_systematic/individual/led_wall_99/red_static.scex"
        if Path(scene_path).exists():
            bass_fixtures.append(scene_path)

        return bass_fixtures

    def get_treble_fixtures(self) -> List[str]:
        """Vrátí fixture paths pro treble (modré světla)"""
        treble_fixtures = []

        # Bodovky - pro vysoké frekvence (ceiling_spot_00 až ceiling_spot_11)
        for spot_id in range(12):  # 0-11
            scene_path = f"generated_scenes_systematic/individual/ceiling_spot_{spot_id:02d}/blue_static.scex"
            if Path(scene_path).exists():
                treble_fixtures.append(scene_path)

        return treble_fixtures

    def format_time(self, seconds: float) -> str:
        """Formátuje čas na H:MM:SS.f"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        whole_secs = int(secs)
        decimal = int((secs - whole_secs) * 10)
        return f"{hours}:{minutes:02d}:{whole_secs:02d}.{decimal}"

    def add_event(self, timeline_index: int, path: str, start_time: float,
                  length: float = 0.2, description: str = ""):
        """Přidá event do timeline"""
        self.timeline_events.append({
            "index": self.event_counter,
            "timeline_index": timeline_index,
            "start_time": self.format_time(start_time),
            "path": path,
            "length": self.format_time(length),
            "speed": 100,
            "description": description
        })
        self.event_counter += 1

    def generate_bass_treble_timeline(self):
        """Generuje bass/treble reaktivní timeline"""
        print("🎛️ Generujem bass/treble timeline...")

        # Analyzuj frekvence
        times, bass_energy, treble_energy = self.analyze_audio_frequencies()

        # Detekuj vrcholy
        bass_peaks = self.detect_peaks(bass_energy, threshold_factor=1.8)
        treble_peaks = self.detect_peaks(treble_energy, threshold_factor=1.6)

        print(f"   Nalezeno {len(bass_peaks)} bass peaks")
        print(f"   Nalezeno {len(treble_peaks)} treble peaks")

        # Získej fixture paths
        bass_fixtures = self.get_bass_fixtures()
        treble_fixtures = self.get_treble_fixtures()

        print(f"   Bass fixtures: {len(bass_fixtures)}")
        print(f"   Treble fixtures: {len(treble_fixtures)}")

        # Generuj bass eventy (timeline 3 - červené)
        bass_fixture_idx = 0
        for peak_idx in bass_peaks:
            if peak_idx < len(times):
                time = times[peak_idx]

                # Rotuj mezi bass fixtures
                if bass_fixtures:
                    fixture_path = bass_fixtures[bass_fixture_idx % len(bass_fixtures)]
                    self.add_event(3, fixture_path, time, 0.3, "Bass Hit")
                    bass_fixture_idx += 1

        # Generuj treble eventy (timeline 4 - modré)
        treble_fixture_idx = 0
        for peak_idx in treble_peaks:
            if peak_idx < len(times):
                time = times[peak_idx]

                # Rotuj mezi treble fixtures
                if treble_fixtures:
                    fixture_path = treble_fixtures[treble_fixture_idx % len(treble_fixtures)]
                    self.add_event(4, fixture_path, time, 0.2, "Treble Hit")
                    treble_fixture_idx += 1

    def generate_timeline_file(self, output_path: str = "BASS_TREBLE_SHOW.tml"):
        """Generuje .tml soubor"""
        print(f"💾 Generujem timeline: {output_path}")

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
timeline_3 = B A S S   R E A C T I V E   ( R E D )
timeline_4 = T R E B L E   R E A C T I V E   ( B L U E )
timeline_5 = L I G H T   S C E N E   T I M E L I N E   #   5
timeline_6 = L I G H T   S C E N E   T I M E L I N E   #   6

[Event_0]
timelineindex = 2
starttime = 0:00:00.0
path = Music/{self.audio_path.name}
length = {self.format_time(self.duration)}

"""

        # Přidej všechny eventy
        for event in self.timeline_events:
            content += f"""[Event_{event['index'] + 1}]
timelineindex = {event['timeline_index']}
starttime = {event['start_time']}
path = {event['path']}
length = {event['length']}
speed = {event['speed']}
speedtype = 2

"""

        # Ulož soubor
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Timeline vytvořen!")
        print(f"   Celkem eventů: {len(self.timeline_events)}")
        print(f"   Délka show: {self.format_time(self.duration)}")
        print(f"   Soubor: {output_path}")

def main():
    """Hlavní funkce"""
    audio_file = "placatá.mp3"

    if not Path(audio_file).exists():
        print(f"❌ Audio soubor {audio_file} nenalezen!")
        return

    print("🎵 Bass & Treble Reactive Visualizer")
    print("=" * 50)

    # Vytvoř visualizer
    visualizer = BassTrableVisualizer(audio_file)

    # Generuj timeline
    visualizer.generate_bass_treble_timeline()
    visualizer.generate_timeline_file()

    print()
    print("🎬 Spusť vizualizaci:")
    print("   dmx-analyzer visualize BASS_TREBLE_SHOW.tml placatá.mp3")
    print()
    print("🎯 Co uvidíš:")
    print("   - Červená světla blikají na basy (LED Kamna, LED Walls)")
    print("   - Modrá světla blikají na výšky (Bodovky)")
    print("   - Každý peak je synchronizovaný s hudbou!")

if __name__ == "__main__":
    main()
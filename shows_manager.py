#!/usr/bin/env python3
"""
Shows Manager
Organizovaný systém pro tvorbu a správu světelných show
- Windows formát cest (C:\...)
- CP1250 kódování
- Organizace do adresářů podle songů
"""

import os
import shutil
from pathlib import Path
import json
from typing import Dict, List
import librosa

# Import našich systémů - ADVANCED VERSION
from ultimate_action_choreographer import AdvancedActionChoreographer

class ShowsManager:
    """Manažer pro organizaci a vytváření show"""

    def __init__(self):
        self.shows_dir = Path("shows")
        self.shows_dir.mkdir(exist_ok=True)

        # Windows cesta pro cílový server
        self.windows_base_path = "C:\\Users\\itbrn\\TheLightingController\\LightShows\\Infinit Maximus - Jarda Vazny"

        # Dostupné audio soubory
        self.available_songs = self._find_audio_files()

    def _find_audio_files(self) -> List[str]:
        """Najde všechny audio soubory"""
        audio_extensions = ['.mp3', '.wav', '.flac', '.m4a']
        audio_files = []

        for ext in audio_extensions:
            audio_files.extend(Path('.').glob(f'*{ext}'))

        return [str(f) for f in audio_files if f.exists()]

    def create_song_directory(self, song_path: str) -> Path:
        """Vytvoří adresář pro song"""
        song_file = Path(song_path)
        song_name = song_file.stem

        # Překlad českých znaků pro Windows kompatibilitu
        song_name_clean = self._clean_filename(song_name)

        song_dir = self.shows_dir / song_name_clean
        song_dir.mkdir(exist_ok=True)

        # Vytvoř podadresáře
        (song_dir / "timelines").mkdir(exist_ok=True)
        (song_dir / "music").mkdir(exist_ok=True)
        (song_dir / "reports").mkdir(exist_ok=True)

        # Zkopíruj audio soubor
        shutil.copy2(song_path, song_dir / "music" / song_file.name)

        return song_dir

    def _clean_filename(self, filename: str) -> str:
        """Vyčistí název souboru pro Windows kompatibilitu"""
        # České znaky
        replacements = {
            'ž': 'z', 'š': 's', 'č': 'c', 'ř': 'r', 'ě': 'e',
            'ý': 'y', 'á': 'a', 'í': 'i', 'é': 'e', 'ó': 'o', 'ú': 'u',
            'ů': 'u', 'ň': 'n', 'ť': 't', 'ď': 'd',
            'Ž': 'Z', 'Š': 'S', 'Č': 'C', 'Ř': 'R', 'Ě': 'E',
            'Ý': 'Y', 'Á': 'A', 'Í': 'I', 'É': 'E', 'Ó': 'O', 'Ú': 'U',
            'Ů': 'U', 'Ň': 'N', 'Ť': 'T', 'Ď': 'D'
        }

        result = filename
        for czech, ascii_char in replacements.items():
            result = result.replace(czech, ascii_char)

        # Odstraň problematické znaky pro Windows
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            result = result.replace(char, '_')

        return result.strip()

    def convert_to_windows_format(self, timeline_content: str, song_name: str) -> str:
        """Převede timeline na Windows formát s Windows cestami"""

        # Převod cest na Windows formát
        song_name_clean = self._clean_filename(song_name)

        # Nahradí Unix cesty za Windows cesty
        windows_content = timeline_content.replace(
            f"Music/{Path(song_name).name}",
            f"{self.windows_base_path}\\Music\\{song_name_clean}\\{Path(song_name).name}"
        )

        # Převod scene cest
        windows_content = windows_content.replace(
            "generated_scenes_systematic/",
            f"{self.windows_base_path}\\generated_scenes_systematic\\"
        )

        windows_content = windows_content.replace(
            "generated_scenes_advanced/",
            f"{self.windows_base_path}\\generated_scenes_advanced\\"
        )

        # Převod lomítek na zpětná lomítka
        windows_content = windows_content.replace("/", "\\")

        return windows_content

    def save_timeline_with_encoding(self, content: str, filepath: str):
        """Uloží timeline s CP1250 kódováním"""
        try:
            with open(filepath, 'w', encoding='cp1250') as f:
                f.write(content)
        except UnicodeEncodeError:
            # Fallback na utf-8 pokud cp1250 selže
            print(f"⚠️  CP1250 encoding failed for {filepath}, using UTF-8")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    def create_ultimate_action_show(self, song_path: str) -> Dict:
        """Vytvoří Ultimate Action show pro song"""
        song_dir = self.create_song_directory(song_path)
        song_file = Path(song_path)
        song_name = song_file.stem

        print(f"🔥 Creating Ultimate Action Show for: {song_name}")

        # Vytvoř Ultimate Action Choreographer
        choreographer = AdvancedActionChoreographer(song_path)

        # Generuj timeline
        temp_timeline = song_dir / "timelines" / "temp_ultimate_action.tml"
        choreographer.create_ultimate_action_show(str(temp_timeline))

        # Načti a převeď na Windows formát
        with open(temp_timeline, 'r', encoding='utf-8') as f:
            content = f.read()

        windows_content = self.convert_to_windows_format(content, song_name)

        # Ulož s Windows formátem a CP1250
        final_timeline = song_dir / "timelines" / "Ultimate_Action_Show.tml"
        self.save_timeline_with_encoding(windows_content, str(final_timeline))

        # Smaž temp soubor
        temp_timeline.unlink()

        return {
            "type": "Ultimate Action Show",
            "timeline": str(final_timeline),
            "description": "Maximálně akční show s bass vlnami a treble explozemi"
        }

    def create_intelligent_shows(self, song_path: str) -> List[Dict]:
        """Vytvoří inteligentní storytelling shows - TEMPORARILY DISABLED"""
        print("🧠 Intelligent Shows temporarily disabled - focus on Advanced Action Show")
        return []

        # TODO: Implement advanced storytelling with generated_scenes_advanced
        """
        song_dir = self.create_song_directory(song_path)
        song_file = Path(song_path)
        song_name = song_file.stem

        print(f"🧠 Creating Intelligent Shows for: {song_name}")

        # Vytvoř storyteller - NEEDS REWRITE FOR ADVANCED SCENES
        storyteller = CompleteMusicalStoryteller()

        # Různé story arcs
        configs = [
            ("Classic_Buildup", StorytellingConfig(story_arc=StoryArc.CLASSIC_BUILDUP)),
            ("Emotional_Journey", StorytellingConfig(story_arc=StoryArc.EMOTIONAL_JOURNEY)),
            ("Party_Energy", StorytellingConfig(story_arc=StoryArc.PARTY_ENERGY))
        ]

        shows = []

        for name, config in configs:
            temp_timeline = song_dir / "timelines" / f"temp_{name}.tml"

            # Generuj timeline
            storyteller.analyze_and_create_show(
                song_path, config, str(temp_timeline)
            )

            # Načti a převeď na Windows formát
            with open(temp_timeline, 'r', encoding='utf-8') as f:
                content = f.read()

            windows_content = self.convert_to_windows_format(content, song_name)

            # Ulož s Windows formátem
            final_timeline = song_dir / "timelines" / f"Intelligent_{name}.tml"
            self.save_timeline_with_encoding(windows_content, str(final_timeline))

            # Smaž temp soubor
            temp_timeline.unlink()

            shows.append({
                "type": f"Intelligent {name}",
                "timeline": str(final_timeline),
                "description": f"AI řízená show s {name} story arc"
            })

        return shows

    def create_all_shows_for_song(self, song_path: str) -> Dict:
        """Vytvoří všechny typy show pro jeden song"""
        song_file = Path(song_path)
        song_name = song_file.stem

        print(f"\n🎵 Creating ALL SHOWS for: {song_name}")
        print("=" * 50)

        shows = {}

        # Ultimate Action Show
        try:
            shows["ultimate_action"] = self.create_ultimate_action_show(song_path)
        except Exception as e:
            print(f"❌ Failed to create Ultimate Action Show: {e}")

        # Intelligent Shows
        try:
            shows["intelligent"] = self.create_intelligent_shows(song_path)
        except Exception as e:
            print(f"❌ Failed to create Intelligent Shows: {e}")

        # Vytvoř summary report
        song_dir = self.shows_dir / self._clean_filename(song_name)
        self._create_show_summary(song_dir, song_name, shows)

        return shows

    def _create_show_summary(self, song_dir: Path, song_name: str, shows: Dict):
        """Vytvoří summary report pro song"""

        # Základní info o songu
        audio_file = list((song_dir / "music").glob("*"))[0]
        y, sr = librosa.load(str(audio_file), sr=22050)
        duration = len(y) / sr
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        summary = {
            "song_name": song_name,
            "duration": float(duration),
            "tempo": float(tempo),
            "created_shows": {},
            "windows_paths": {
                "music_directory": f"{self.windows_base_path}\\Music\\{self._clean_filename(song_name)}",
                "timelines_directory": f"{self.windows_base_path}\\Timelines\\{self._clean_filename(song_name)}"
            }
        }

        # Přidej info o shows
        for show_type, show_data in shows.items():
            if isinstance(show_data, list):
                summary["created_shows"][show_type] = [
                    {
                        "name": show["type"],
                        "file": Path(show["timeline"]).name,
                        "description": show["description"]
                    }
                    for show in show_data
                ]
            else:
                summary["created_shows"][show_type] = {
                    "name": show_data["type"],
                    "file": Path(show_data["timeline"]).name,
                    "description": show_data["description"]
                }

        # Ulož summary
        summary_file = song_dir / "reports" / "show_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"📊 Summary saved: {summary_file}")

    def create_all_shows(self):
        """Vytvoří všechny show pro všechny dostupné songy"""
        print("🎭 SHOWS MANAGER - Creating All Shows")
        print("=" * 50)

        if not self.available_songs:
            print("❌ No audio files found!")
            return

        print(f"📁 Found {len(self.available_songs)} audio files:")
        for song in self.available_songs:
            print(f"   - {song}")

        print()

        all_shows = {}

        for song_path in self.available_songs:
            try:
                shows = self.create_all_shows_for_song(song_path)
                all_shows[song_path] = shows
                print(f"✅ Completed shows for: {Path(song_path).stem}")
            except Exception as e:
                print(f"❌ Failed to create shows for {song_path}: {e}")

        # Master summary
        self._create_master_summary(all_shows)

        print()
        print("🌟 ALL SHOWS CREATED!")
        print(f"   Location: {self.shows_dir}")
        print("   Windows format with CP1250 encoding")
        print("   Ready for deployment to target server")

    def _create_master_summary(self, all_shows: Dict):
        """Vytvoří master summary všech show"""
        master_summary = {
            "total_songs": len(all_shows),
            "shows_directory": str(self.shows_dir),
            "windows_base_path": self.windows_base_path,
            "encoding": "CP1250",
            "songs": {}
        }

        for song_path, shows in all_shows.items():
            song_name = Path(song_path).stem
            master_summary["songs"][song_name] = {
                "audio_file": song_path,
                "show_types": list(shows.keys()),
                "total_timelines": sum(
                    len(show_data) if isinstance(show_data, list) else 1
                    for show_data in shows.values()
                )
            }

        # Ulož master summary
        master_file = self.shows_dir / "master_summary.json"
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(master_summary, f, indent=2, ensure_ascii=False)

        print(f"📋 Master summary: {master_file}")

def main():
    """Hlavní funkce"""
    manager = ShowsManager()
    manager.create_all_shows()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Intelligent Scene Selector
Systém pro inteligentní výběr scén na základě hudební analýzy
"""

from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MoodCategory(Enum):
    """Nálady pro kategorización scén"""
    ROMANTIC = "romantic"           # Romantické momenty
    ENERGETIC = "energetic"         # Vysoká energie
    MYSTERIOUS = "mysterious"       # Tajemné atmosféry
    AGGRESSIVE = "aggressive"       # Tvrdé, agresivní
    PEACEFUL = "peaceful"           # Klidné, mírové
    DRAMATIC = "dramatic"           # Dramatické, napínavé
    JOYFUL = "joyful"              # Radostné, veselé
    MELANCHOLIC = "melancholic"     # Smutné, nostalgické

class IntensityLevel(Enum):
    """Úrovně intenzity"""
    LOW = "low"           # 0-25%
    MEDIUM = "medium"     # 25-60%
    HIGH = "high"         # 60-85%
    EXTREME = "extreme"   # 85-100%

@dataclass
class SceneDescriptor:
    """Popis scény pro inteligentní výběr"""
    name: str
    file_path: str
    mood: MoodCategory
    intensity: IntensityLevel
    tempo_range: Tuple[int, int]  # BPM range
    best_for_sections: List[str]  # intro, verse, chorus, drop, etc.
    color_palette: List[str]
    fixture_types: List[str]      # moving_heads, bodovky, walls, etc.
    effects: List[str]            # strobe, pulse, static, etc.
    emotional_weight: float       # 0.0-1.0 jak moc emocionálně působí
    energy_requirement: float     # 0.0-1.0 kolik energie vyžaduje

class IntelligentSceneSelector:
    """Inteligentní systém pro výběr scén"""

    def __init__(self):
        self.scene_database: Dict[str, SceneDescriptor] = {}
        self.load_scene_database()

    def load_scene_database(self):
        """Načte databázi scén"""
        print("🧠 Loading intelligent scene database...")

        # Choreography scenes
        choreography_scenes = [
            SceneDescriptor(
                name="Romantic Slow Sweep",
                file_path="generated_scenes_advanced/choreography/romantic_slow_sweep.scex",
                mood=MoodCategory.ROMANTIC,
                intensity=IntensityLevel.LOW,
                tempo_range=(60, 100),
                best_for_sections=["intro", "verse", "bridge"],
                color_palette=["warm_white", "orange", "yellow"],
                fixture_types=["moving_heads"],
                effects=["slow_movement", "warm_colors"],
                emotional_weight=0.8,
                energy_requirement=0.2
            ),

            SceneDescriptor(
                name="Energetic Fast Sweep",
                file_path="generated_scenes_advanced/choreography/energetic_fast_sweep.scex",
                mood=MoodCategory.ENERGETIC,
                intensity=IntensityLevel.HIGH,
                tempo_range=(120, 180),
                best_for_sections=["chorus", "drop"],
                color_palette=["white", "red", "blue", "green"],
                fixture_types=["moving_heads"],
                effects=["fast_movement", "bright_colors"],
                emotional_weight=0.6,
                energy_requirement=0.8
            ),

            SceneDescriptor(
                name="Mystical Circle",
                file_path="generated_scenes_advanced/choreography/mystical_circle.scex",
                mood=MoodCategory.MYSTERIOUS,
                intensity=IntensityLevel.MEDIUM,
                tempo_range=(80, 120),
                best_for_sections=["intro", "bridge", "breakdown"],
                color_palette=["purple", "blue", "cyan"],
                fixture_types=["moving_heads"],
                effects=["circular_movement", "gobo_patterns"],
                emotional_weight=0.9,
                energy_requirement=0.4
            ),

            SceneDescriptor(
                name="Rainbow Explosion",
                file_path="generated_scenes_advanced/choreography/rainbow_explosion.scex",
                mood=MoodCategory.JOYFUL,
                intensity=IntensityLevel.EXTREME,
                tempo_range=(130, 200),
                best_for_sections=["drop", "chorus"],
                color_palette=["red", "orange", "yellow", "green", "blue"],
                fixture_types=["moving_heads"],
                effects=["explosive_movement", "prism_effects", "gobo_patterns"],
                emotional_weight=0.9,
                energy_requirement=0.95
            ),

            SceneDescriptor(
                name="Synchronized Power",
                file_path="generated_scenes_advanced/choreography/synchronized_power.scex",
                mood=MoodCategory.DRAMATIC,
                intensity=IntensityLevel.EXTREME,
                tempo_range=(110, 150),
                best_for_sections=["drop", "climax"],
                color_palette=["white"],
                fixture_types=["moving_heads"],
                effects=["synchronized_movement", "intense_white"],
                emotional_weight=0.7,
                energy_requirement=0.9
            ),

            SceneDescriptor(
                name="Strobo Madness",
                file_path="generated_scenes_advanced/choreography/strobo_madness.scex",
                mood=MoodCategory.AGGRESSIVE,
                intensity=IntensityLevel.EXTREME,
                tempo_range=(140, 200),
                best_for_sections=["drop", "breakdown"],
                color_palette=["white", "red"],
                fixture_types=["moving_heads"],
                effects=["strobe", "aggressive_movement"],
                emotional_weight=0.5,
                energy_requirement=1.0
            )
        ]

        # Add to database
        for scene in choreography_scenes:
            self.scene_database[scene.name] = scene

        # Add systematic scenes
        self._add_systematic_scenes()

        print(f"   Loaded {len(self.scene_database)} scenes")

    def _add_systematic_scenes(self):
        """Přidá systematické scény do databáze"""

        # Color-mood mapping
        color_moods = {
            "red": (MoodCategory.AGGRESSIVE, 0.8, ["drop", "climax"]),
            "blue": (MoodCategory.PEACEFUL, 0.6, ["verse", "bridge"]),
            "green": (MoodCategory.PEACEFUL, 0.5, ["verse", "ambient"]),
            "yellow": (MoodCategory.JOYFUL, 0.7, ["chorus", "uplifting"]),
            "orange": (MoodCategory.ENERGETIC, 0.7, ["chorus", "dance"]),
            "purple": (MoodCategory.MYSTERIOUS, 0.8, ["intro", "bridge"]),
            "white_warm": (MoodCategory.ROMANTIC, 0.9, ["intro", "verse"]),
            "white_cool": (MoodCategory.DRAMATIC, 0.6, ["drop", "tension"])
        }

        # Effect-intensity mapping
        effect_intensities = {
            "static": (IntensityLevel.LOW, 0.1),
            "fade_in": (IntensityLevel.LOW, 0.3),
            "fade_out": (IntensityLevel.LOW, 0.2),
            "pulse": (IntensityLevel.MEDIUM, 0.5),
            "strobe_slow": (IntensityLevel.HIGH, 0.7),
            "strobe_fast": (IntensityLevel.EXTREME, 0.9)
        }

        # Generate systematic scene descriptors
        fixture_types = ["ceiling_spot", "led_wall", "led_lavice", "led_kamna", "uv"]

        for fixture_type in fixture_types:
            for color, (mood, emotional_weight, sections) in color_moods.items():
                for effect, (intensity, energy_req) in effect_intensities.items():

                    # Tempo based on intensity
                    tempo_ranges = {
                        IntensityLevel.LOW: (60, 100),
                        IntensityLevel.MEDIUM: (90, 130),
                        IntensityLevel.HIGH: (120, 160),
                        IntensityLevel.EXTREME: (140, 200)
                    }

                    scene_name = f"{fixture_type}_{color}_{effect}"
                    scene_path = f"generated_scenes_systematic/individual/{fixture_type}_00/{color}_{effect}.scex"

                    # Check if file exists
                    if Path(scene_path).exists():
                        descriptor = SceneDescriptor(
                            name=scene_name,
                            file_path=scene_path,
                            mood=mood,
                            intensity=intensity,
                            tempo_range=tempo_ranges[intensity],
                            best_for_sections=sections,
                            color_palette=[color],
                            fixture_types=[fixture_type],
                            effects=[effect],
                            emotional_weight=emotional_weight,
                            energy_requirement=energy_req
                        )

                        self.scene_database[scene_name] = descriptor

    def select_scene_for_moment(self,
                               tempo: float,
                               energy_level: float,
                               emotion: str,
                               section: str,
                               preferred_fixtures: List[str] = None) -> Optional[SceneDescriptor]:
        """Vybere nejlepší scénu pro daný moment"""

        # Score každé scény
        best_scene = None
        best_score = -1

        for scene in self.scene_database.values():
            score = self._calculate_scene_score(scene, tempo, energy_level, emotion, section, preferred_fixtures)

            if score > best_score:
                best_score = score
                best_scene = scene

        return best_scene

    def _calculate_scene_score(self,
                              scene: SceneDescriptor,
                              tempo: float,
                              energy_level: float,
                              emotion: str,
                              section: str,
                              preferred_fixtures: List[str] = None) -> float:
        """Vypočítá skóre scény pro daný moment"""

        score = 0.0

        # Tempo matching (25% váha)
        tempo_min, tempo_max = scene.tempo_range
        if tempo_min <= tempo <= tempo_max:
            score += 25
        else:
            # Penalty za tempo mismatch
            tempo_diff = min(abs(tempo - tempo_min), abs(tempo - tempo_max))
            score += max(0, 25 - tempo_diff * 0.2)

        # Energy matching (30% váha)
        energy_diff = abs(energy_level - scene.energy_requirement)
        score += max(0, 30 - energy_diff * 30)

        # Section matching (20% váha)
        if section in scene.best_for_sections:
            score += 20
        elif section in ["chorus", "drop"] and "climax" in scene.best_for_sections:
            score += 15
        elif section in ["verse", "bridge"] and "ambient" in scene.best_for_sections:
            score += 15

        # Emotion/mood matching (15% váha)
        emotion_mood_map = {
            "calm": MoodCategory.PEACEFUL,
            "energy": MoodCategory.ENERGETIC,
            "tension": MoodCategory.DRAMATIC,
            "release": MoodCategory.JOYFUL,
            "mystery": MoodCategory.MYSTERIOUS,
            "joy": MoodCategory.JOYFUL,
            "melancholy": MoodCategory.MELANCHOLIC,
            "aggressive": MoodCategory.AGGRESSIVE
        }

        if emotion in emotion_mood_map and emotion_mood_map[emotion] == scene.mood:
            score += 15

        # Fixture preference (10% váha)
        if preferred_fixtures:
            fixture_match = any(fixture in scene.fixture_types for fixture in preferred_fixtures)
            if fixture_match:
                score += 10

        return score

    def create_intelligent_playlist(self, musical_moments: List[Dict]) -> List[Tuple[Dict, SceneDescriptor]]:
        """Vytvoří inteligentní playlist scén pro hudební momenty"""

        playlist = []

        for moment in musical_moments:
            # Extract parameters from moment
            tempo = moment.get("tempo", 120)
            energy = moment.get("energy_level", 0.5)
            emotion = moment.get("emotion", "calm")
            section = moment.get("section", "verse")

            # Select best scene
            scene = self.select_scene_for_moment(
                tempo=tempo,
                energy_level=energy,
                emotion=emotion,
                section=section
            )

            if scene:
                playlist.append((moment, scene))

        return playlist

    def export_scene_recommendations(self, output_path: str = "scene_recommendations.json"):
        """Exportuje doporučení scén"""

        recommendations = {
            "by_mood": {},
            "by_intensity": {},
            "by_section": {},
            "usage_guide": {
                "romantic_moments": [],
                "high_energy": [],
                "mysterious_intro": [],
                "explosive_drop": [],
                "peaceful_verse": [],
                "dramatic_bridge": []
            }
        }

        # Group by categories
        for scene in self.scene_database.values():
            # By mood
            mood_key = scene.mood.value
            if mood_key not in recommendations["by_mood"]:
                recommendations["by_mood"][mood_key] = []
            recommendations["by_mood"][mood_key].append({
                "name": scene.name,
                "file": scene.file_path,
                "intensity": scene.intensity.value,
                "emotional_weight": scene.emotional_weight
            })

            # By intensity
            intensity_key = scene.intensity.value
            if intensity_key not in recommendations["by_intensity"]:
                recommendations["by_intensity"][intensity_key] = []
            recommendations["by_intensity"][intensity_key].append({
                "name": scene.name,
                "mood": scene.mood.value,
                "energy_requirement": scene.energy_requirement
            })

            # Usage guide
            if scene.mood == MoodCategory.ROMANTIC and scene.intensity == IntensityLevel.LOW:
                recommendations["usage_guide"]["romantic_moments"].append(scene.name)
            elif scene.intensity == IntensityLevel.EXTREME:
                recommendations["usage_guide"]["high_energy"].append(scene.name)
            elif scene.mood == MoodCategory.MYSTERIOUS:
                recommendations["usage_guide"]["mysterious_intro"].append(scene.name)

        # Save recommendations
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(recommendations, f, indent=2, ensure_ascii=False)

        print(f"✅ Scene recommendations exported to {output_path}")

def main():
    """Hlavní funkce"""
    print("🧠 Intelligent Scene Selector")
    print("=" * 50)

    selector = IntelligentSceneSelector()

    # Export recommendations
    selector.export_scene_recommendations()

    # Demo: výběr scény pro konkrétní moment
    print("\n🎯 Demo: Scene Selection")

    test_moments = [
        {"tempo": 128, "energy_level": 0.8, "emotion": "energy", "section": "chorus"},
        {"tempo": 85, "energy_level": 0.3, "emotion": "calm", "section": "verse"},
        {"tempo": 140, "energy_level": 0.95, "emotion": "aggressive", "section": "drop"},
        {"tempo": 95, "energy_level": 0.4, "emotion": "mystery", "section": "intro"}
    ]

    for i, moment in enumerate(test_moments, 1):
        scene = selector.select_scene_for_moment(**moment)
        if scene:
            print(f"   {i}. {moment} -> {scene.name}")
            print(f"      File: {scene.file_path}")
            print(f"      Mood: {scene.mood.value}, Intensity: {scene.intensity.value}")
        else:
            print(f"   {i}. {moment} -> No suitable scene found")

    print(f"\n✅ Intelligent Scene Selector Ready!")
    print(f"   Database: {len(selector.scene_database)} scenes")
    print(f"   Categories: {len(set(s.mood for s in selector.scene_database.values()))} moods")

if __name__ == "__main__":
    main()
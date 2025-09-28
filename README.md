# 🎭 DMX Music Analyzer - Ultimate Sauna Lighting System

> **Inteligentní systém pro řízení DMX světel s analýzou hudby a real-time vizualizací**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pokročilý systém, který analyzuje hudbu a automaticky vytváří spektakulární světelné show synchronizované s hudbou pro saunu. Obsahuje AI-řízené choreografie, real-time vizualizátor a kompletní produkční systém.

## 🌟 Klíčové Funkce

### 🎵 **Hudební Analýza a AI Choreografie**
- **7 frekvenčních pásem**: Sub-bass → Brilliance pro precizní mapování světel
- **Emocionální mapování**: Calm, Energy, Tension, Release, Mystery, Joy, Melancholy, Aggressive
- **Strukturální analýza**: Intro, Verse, Chorus, Bridge, Drop, Outro, Breakdown, Buildup
- **AI choreograf**: Inteligentní výběr scén na základě hudební analýzy

### 💡 **Pokročilé Světelné Systémy**
- **Ultimate Action Choreographer**: Maximálně akční show s bass vlnami a treble explozemi
- **Intelligent Storytelling**: AI-řízené příběhové oblouky (Classic Buildup, Emotional Journey, Party Energy)
- **Symmetry Movement**: Matematicky precizní symetrické a asymetrické pohyby
- **Dynamic Choreographies**: 10+ typů pohybových choreografií (Water Waves, Circular Flow, Figure-8)

### 🎮 **Real-time Vizualizátor**
- **2D reprezentace sauny**: Všech 47 světelných zařízení v real-time
- **Audio synchronizace**: <50ms latence pro perfektní synchronizaci
- **Interaktivní ovládání**: Play/Pause, Seek, Restart pomocí klávesnice
- **60 FPS rendering**: Plynulé animace a efekty

### 🏗️ **Produkční Systém**
- **Organizované adresáře**: Automatická struktura shows/[song_name]/
- **Windows kompatibilita**: C:\ cesty a CP1250 kódování pro cílový server
- **Batch zpracování**: Vytvoření show pro všechny dostupné songy najednou
- **JSON reporty**: Detailní analýzy a shrnutí každé show

## 🎯 Architektura Systému

```
Audio File → Music Analysis → AI Choreographer → Timeline Generator → Real-time Visualizer
   (.mp3)         ↓               ↓                    (.tml)              ↓
              BPM, Energy    Scene Selection      Windows Format      Live Preview
             7 Freq Bands   Story Arcs          CP1250 Encoding     47 Fixtures
            Emotional Map   Movement Patterns   Spatial Mapping     60 FPS
```

## 🚀 Rychlý Start

### Instalace

```bash
# Klonování repository
git clone https://github.com/your-username/dmx-music-analyzer.git
cd dmx-music-analyzer

# Instalace závislostí
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# nebo .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Základní Použití

```bash
# 🎭 VYTVOŘENÍ KOMPLETNÍCH SHOW PRO VŠECHNY SONGY
python shows_manager.py

# 🎮 REAL-TIME VIZUALIZACE
python -m src.dmx_analyzer.visualizer.visualizer_app timeline.tml song.mp3

# 🔥 ULTIMATE ACTION SHOW
python ultimate_action_choreographer.py song.mp3

# 🧠 INTELLIGENT STORYTELLING
python complete_musical_storyteller.py song.mp3

# 🔄 SYMMETRY CHOREOGRAPHIES
python symmetry_choreographer.py song.mp3
```

## 🎪 Typy Světelných Show

### 1. **Ultimate Action Show** 🔥
```python
# Maximálně akční show s:
- Bass vlny postupně zepředu dozadu
- Treble exploze s všemi světly
- Spatial efekty através prostorových zón
- TOTAL MADNESS momenty při vrcholech
- 29,795+ action momentů pro 5min track
```

### 2. **Intelligent Storytelling** 🧠
```python
# AI-řízené příběhové show:
- Classic Buildup: Postupné gradování napětí
- Emotional Journey: Emocionální cesta skladbou
- Party Energy: Energická taneční atmosféra
- Cinematic: Filmová dramaturgie
- Ambient Flow: Plynulé ambientní světlo
```

### 3. **Symmetry Movement** 🪞
```python
# Matematicky precizní pohyby:
- Mirror Horizontal: Zrcadlové horizontální pohyby
- Adjacent Pairs: Přilehlé páry světel
- Opposite Pairs: Protilehlé světla
- Pendulum Motion: Kyvadlové pohyby tam a zpět
- Rotational Symmetry: Rotační symetrie
```

### 4. **Dynamic Choreographies** 🌊
```python
# Organické pohybové vzory:
- Water Waves: Vlnové pohyby napříč prostorem
- Circular Flow: Kruhové toky energie
- Figure-8 Infinity: Nekonečné osmičky
- Breathing Expand: Dýchání prostoru
- Chase Sequences: Honičkové sekvence
```

## 🎮 Real-time Vizualizátor

### Ovládání Klávesnicí
```
SPACE  → Play/Pause přehrávání
R      → Restart od začátku
←/→    → Seek 5s zpět/vpřed
ESC    → Ukončit aplikaci
```

### Vizuální Reprezentace
- **Kruhová světla**: 12x Ceiling Spots (Bodovky)
- **Čtvercová světla**: 8x Wall Spots
- **Obdélníková světla**: 11x LED Bench Strips
- **Diamantová světla**: 5x Moving Heads s reálnými pohyby pan/tilt
- **Hvězdicová světla**: 2x UV Lights
- **LED pásky**: 2x LED Stove u kamen

## 🎵 Hudební Analýza

### Frekvenční Pásma → Světelné Mapování
```python
Sub-bass (20-60Hz)    → LED Kamna (hluboký bass)
Bass (60-250Hz)       → LED Walls + Bodovky
Low-mid (250-500Hz)   → Moving Heads základní
Mid (500-2kHz)        → Moving Heads rychlejší
High-mid (2-4kHz)     → Bodovky jasné efekty
Presence (4-6kHz)     → Wall Spots ostré efekty
Brilliance (6-20kHz)  → Moving Heads velmi rychlé
```

### Emocionální Mapování
```python
Calm        → Modré, teplé barvy, pomalé fades
Energy      → Červené, žluté, rychlé efekty
Tension     → Ostré, kontrastní barvy
Release     → Výbušné, všechny světla najednou
Mystery     → Fialové, temné, tajemné efekty
Joy         → Žluté, oranžové, živé barvy
Melancholy  → Modré, chladné, pomalé změny
Aggressive  → Červené, rychlé stroby, chaos
```

## 🏗️ Struktura Projektu

### Organizace Show
```
shows/
├── [song_name]/
│   ├── music/
│   │   └── song.mp3
│   ├── timelines/
│   │   ├── Ultimate_Action_Show.tml
│   │   ├── Intelligent_Classic_Buildup.tml
│   │   ├── Intelligent_Emotional_Journey.tml
│   │   └── Intelligent_Party_Energy.tml
│   └── reports/
│       └── show_summary.json
└── master_summary.json
```

### Technické Soubory
```
src/dmx_analyzer/
├── visualizer/                    # Real-time vizualizátor
│   ├── visualizer_app.py         # Hlavní aplikace
│   ├── sauna_renderer.py         # 2D rendering sauny
│   └── audio_player.py           # Audio přehrávač
├── music_analyzer.py             # Hudební analýza
├── timeline_generator.py         # Generování timeline
└── models.py                     # Datové modely

generated_scenes_systematic/       # 3000+ scén
├── individual/                   # Jednotlivá světla
├── groups/                       # Skupiny světel
└── zones/                        # Prostorové zóny

choreography_systems/
├── ultimate_action_choreographer.py
├── complete_musical_storyteller.py
├── symmetry_choreographer.py
└── dynamic_movement_choreographer.py
```

## 🎛️ Pokročilé Funkce

### Prostorové Mapování
```python
# Spatial zones pro progresivní efekty
zones = {
    'front': ['ceiling_spot_00', 'ceiling_spot_01', 'ceiling_spot_02'],
    'middle': ['ceiling_spot_03', 'ceiling_spot_04', 'ceiling_spot_05'],
    'back': ['ceiling_spot_06', 'ceiling_spot_07', 'ceiling_spot_08']
}

# Bass wave front-to-back
for zone in ['front', 'middle', 'back']:
    trigger_zone_effect(zone, 'red_pulse', duration=0.5)
```

### Moving Heads Choreografie
```python
# Real Intimidator Spot 375Z DMX channels
pan_channel = 1        # 0-540° rotation
tilt_channel = 3       # 0-270° tilt
color_wheel = 5        # 8 colors + white
gobo_wheel = 7         # 7 gobos + open
dimmer = 11            # 0-100% brightness

# Smooth pan/tilt movements with mathematical precision
def water_wave_movement(head_id, time_offset):
    pan = 127 + 100 * math.sin(time * 0.5 + time_offset)
    tilt = 127 + 50 * math.cos(time * 0.3 + time_offset)
    return create_movement(head_id, pan, tilt)
```

### Windows Server Deployment
```python
# Automatická konverze cest pro cílový Windows server
unix_path = "generated_scenes_systematic/individual/ceiling_spot_00/red_pulse.scex"
windows_path = "C:\\Users\\itbrn\\TheLightingController\\LightShows\\Infinit Maximus - Jarda Vazny\\generated_scenes_systematic\\individual\\ceiling_spot_00\\red_pulse.scex"

# CP1250 encoding pro české znaky
with open(timeline_path, 'w', encoding='cp1250') as f:
    f.write(timeline_content)
```

## 📊 Výkonnostní Charakteristiky

- **Audio Latence**: <50ms synchronizace
- **Frame Rate**: 60 FPS rendering
- **Memory Usage**: ~50MB pro typickou show
- **CPU Usage**: ~10-15% na moderním CPU
- **Scén v databázi**: 3000+ systematických scén
- **Action momentů**: 29,795 pro 5min track
- **Podporované formáty**: .mp3, .wav, .flac

## 🔧 Produkční Deployment

### Generování Show
```bash
# Vytvoření kompletních show pro všechny songy
python shows_manager.py

# Output:
📁 Found 2 audio files:
   - test_short.mp3
   - placatá.mp3

🎵 Creating ALL SHOWS for: test_short
✅ Ultimate Action Show: 4,568 bass waves + 3,837 treble explosions
✅ Intelligent Classic Buildup: 32 intelligent moments
✅ Intelligent Emotional Journey: emocionální gradace
✅ Intelligent Party Energy: energická atmosféra

🌟 Shows ready for Windows server deployment!
```

### Real-time Visualization
```bash
# Vizualizace Ultimate Action Show
python -m src.dmx_analyzer.visualizer.visualizer_app \
    shows/placata/timelines/Ultimate_Action_Show.tml \
    placatá.mp3

# Output:
🔥 Starting ULTIMATE ACTION SHOW!
   💥 MAXIMÁLNĚ AKČNÍ světelná show!
   🎯 Basy postupně zepředu dozadu
   🎆 Výšky = explozivní všechna světla
   🔥 1,998 TOTAL MADNESS momentů!
```

## 🎨 Customizace a Rozšíření

### Vlastní Choreografie
```python
from complete_musical_storyteller import CompleteMusicalStoryteller

storyteller = CompleteMusicalStoryteller()

# Custom story arc
config = StorytellingConfig(
    story_arc=StoryArc.CUSTOM,
    energy_buildup_rate=1.5,
    color_palette=['red', 'orange', 'yellow'],
    movement_intensity='high'
)

storyteller.analyze_and_create_show('song.mp3', config, 'custom_show.tml')
```

### Nové Scény
```python
from systematic_scex_generator import SystematicScexGenerator

generator = SystematicScexGenerator()

# Vytvoření nových scén
generator.generate_individual_scenes(['ceiling_spot_00'], ['purple_fade_in'])
generator.generate_group_scenes(['walls_1&11'], ['rainbow_pulse'])
generator.generate_zone_scenes(['ceiling'], ['breathing_effect'])
```

## 🎯 Příklady Použití

### 1. Rychlé Demo
```bash
# Vytvoření a vizualizace v jednom kroku
python bass_treble_visualizer.py && \
python -m src.dmx_analyzer.visualizer.visualizer_app BASS_TREBLE_SHOW.tml placatá.mp3
```

### 2. Produkční Workflow
```bash
# 1. Vytvoření všech show
python shows_manager.py

# 2. Preview nejlepší show
python -m src.dmx_analyzer.visualizer.visualizer_app \
    shows/song/timelines/Ultimate_Action_Show.tml song.mp3

# 3. Export na Windows server
# Soubory jsou již ve Windows formátu s CP1250 encoding
```

### 3. Custom Scene Development
```bash
# Generování vlastních scén
python systematic_scex_generator.py

# Testování nových choreografií
python symmetry_choreographer.py test_song.mp3
python dynamic_movement_choreographer.py test_song.mp3
```

## 🛠️ Development a Debugging

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Detailní výstup analýzy
analyzer = AdvancedMusicAnalyzer()
analysis = analyzer.analyze('song.mp3')
print(f"Detected {len(analysis.beats)} beats")
print(f"Energy peaks: {len(analysis.energy_peaks)}")
print(f"Emotional moments: {len(analysis.emotional_moments)}")
```

### Performance Monitoring
```python
import time
start_time = time.time()

# Analýza a generování
shows = shows_manager.create_all_shows_for_song('song.mp3')

end_time = time.time()
print(f"Total processing time: {end_time - start_time:.2f}s")
```

## 🌟 Budoucí Rozšíření

### Plánované Funkce
- **Web Interface**: Browser-based ovládání a preview
- **MIDI Control**: Kontrola přes MIDI kontrolery
- **Video Export**: Render show do MP4 souboru
- **Cloud Sync**: Sdílení show přes cloud
- **VR Preview**: Virtual reality náhled sauny

### Možná Rozšíření
- **Multi-room Support**: Podpora více saun současně
- **Live Performance**: Real-time ovládání během party
- **DJ Integration**: Integrace s DJ software
- **Mobile App**: Mobilní aplikace pro ovládání

## 📋 Troubleshooting

### Časté Problémy
```bash
# Audio codec issues
pip install ffmpeg-python

# Memory issues s velkými soubory
export PYTHONPATH=.:$PYTHONPATH
python -X dev your_script.py

# Visualization performance
# Snižte rozlišení v sauna_renderer.py:
width, height = 800, 600  # místo 1200, 900
```

### Debug Commands
```bash
# Test audio loading
python -c "import librosa; print(librosa.load('song.mp3')[1])"

# Test timeline generation
python -c "from timeline_generator import *; print('Timeline generator OK')"

# Test visualization
python -c "import pygame; pygame.init(); print('Pygame OK')"
```

## 🤝 Contributing

Projekt je otevřený pro příspěvky! Zejména vítáme:

- **Nové choreografie**: Vlastní pohybové vzory
- **Hudební analýza**: Lepší detekce hudebních prvků
- **Vizualizace**: Nové efekty a animace
- **Optimalizace**: Vylepšení výkonu
- **Dokumentace**: Rozšíření dokumentace

### Workflow
1. Fork repository
2. Vytvoř feature branch (`git checkout -b feature/nova-choreografie`)
3. Implementuj změny s testy
4. Spusť `make check` pro kontrolu kvality
5. Vytvoř Pull Request

## 📝 License

MIT License - plná svoboda použití pro komerční i nekomerční účely.

## 🏆 Acknowledgments

- **Librosa**: Pokročilá audio analýza
- **Pygame**: Real-time vizualizace
- **Infinit Maximus**: Target lighting controller
- **Intimidator Spot 375Z**: Moving heads reference

---

**🎵💡 Vytvořte nezapomenutelnou hudební a světelnou atmosféru ve vaší saune! 🔥🎭**

*Systém obsahuje kompletní AI-řízené choreografie, real-time vizualizaci a produkční tools pro profesionální deployment. Od základní analýzy po spektakulární Ultimate Action Show - vše připraveno k okamžitému použití!*
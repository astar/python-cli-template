# DMX Music Analyzer - Claude Project Memory

## 🎯 Projekt Přehled

Systém pro řízení DMX světel v saune na základě analýzy hudby. Projekt vytváří timeline soubory (.tml) kompatibilní s Infinit Maximus lighting controllerem a poskytuje real-time vizualizaci.

**⚡ NOVÉ FUNKCE V TÉTO VERZI:**
- ✅ **Windows Export System** - Automatická konverze cest pro cílový Windows systém
- ✅ **Ceremonial Structure** - Organizace projektů podle ceremoniálů
- ✅ **CP1250 Encoding** - Podpora pro české znaky na Windows
- ✅ **Path Converter** - Inteligentní konverze mezi Unix/Windows cestami

## 🏗️ Architektura Systému

### Hlavní Komponenty

1. **Music Analysis Engine** (`music_analyzer.py`, `advanced_music_analyzer.py`)
   - Základní analýza: BPM, energy, valence, spektrální vlastnosti
   - Pokročilá analýza: 7 frekvenčních pásem, rytmus, harmonie, struktura

2. **Timeline Generation** (`timeline_generator.py`, `spectacular_timeline_generator.py`)
   - Standardní generátor pro základní světelné efekty
   - Spektakulární generátor s pokročilou analýzou hudby

3. **Real-time Visualizer** (`visualizer/`)
   - 2D reprezentace sauny se všemi 47 světelnými zařízeními
   - Audio synchronizace a real-time efekty
   - Interaktivní ovládání (play/pause, seek, restart)

### Struktura Světel v Saune

- **12x Bodovky (Ceiling Spots)**: Kruhové světla ve stropě
- **8x Wall Spots**: Čtvercová světla na stěnách
- **11x LED Lavice**: LED pásky na lavicích
- **2x LED Kamna**: Světla u kamen
- **5x Moving Heads**: Pohyblivá světla (diamantový tvar)
- **2x UV Lights**: UV světla (hvězdicový tvar)

## 🎵 Pokročilá Hudební Analýza

### Frekvenční Pásma → Světelné Skupiny
```
Sub-bass (20-60Hz)    → LED Kamna (hluboký bass)
Bass (60-250Hz)       → LED Walls + Bodovky
Low-mid (250-500Hz)   → Moving Heads
Mid (500-2kHz)        → Moving Heads (rychlejší)
High-mid (2-4kHz)     → Bodovky (jasné)
Presence (4-6kHz)     → Wall Spots
Brilliance (6-20kHz)  → Moving Heads (velmi rychlé)
```

### Typy Analýzy
- **Rytmická**: Beat detection, downbeats, syncopation, tempo curves
- **Dynamická**: RMS energie, transienty, sustain regiony
- **Harmonická**: Chroma features, detekce tóniny, změny akordů
- **Strukturální**: Detekce intro/verse/chorus/outro
- **Emocionální**: Valence-arousal model pro mapování barev

## 🎮 CLI Příkazy

```bash
# Základní analýza
dmx-analyzer analyze song.wav -o basic_show.tml

# Spektakulární show s pokročilou analýzou
dmx-analyzer spectacular song.wav -o amazing_show.tml

# Real-time vizualizace
dmx-analyzer visualize amazing_show.tml song.wav

# 🆕 NOVÉ PŘÍKAZY:

# Vytvoření ceremoniální struktury
dmx-analyzer create-ceremonial "Kokoti"

# Export pro Windows s ceremoniální strukturou
dmx-analyzer export timeline.tml --target windows --ceremonial "Kokoti"

# Export s vlastním kódováním
dmx-analyzer export timeline.tml --target windows --encoding cp1250

# Pokročilé spektrální řízení
dmx-analyzer music-director song.wav

# Dynamické explozivní efekty
dmx-analyzer dynamic song.wav -o explosive_show.tml
```

## 🎨 Vizualizátor Ovládání

- **SPACE**: Play/Pause přehrávání
- **R**: Restart od začátku
- **←/→**: Seek 5s zpět/vpřed
- **ESC**: Ukončit aplikaci

## 🔧 Technické Detaily

### Dependencies
```toml
librosa>=0.10.0      # Audio analýza
pygame>=2.5.0        # Real-time vizualizace
numpy>=1.24.0        # Numerické výpočty
scipy>=1.10.0        # Vědecké výpočty
pydantic>=2.11.4     # Data validace
click>=8.2.0         # CLI framework
```

### Výkonnost
- **Frame Rate**: 60 FPS pro plynulé animace
- **Audio Latence**: <50ms synchronizace
- **Memory Usage**: ~50MB pro typickou show
- **CPU Usage**: ~10-15% na moderním CPU

### Formáty Souborů
- **Timeline**: .tml (Infinit Maximus format)
- **Audio**: .wav (nejlepší), .mp3 (podporováno)

## 🚀 Development Workflow

### Typický Proces
1. **Analyze** → Vytvoř basic timeline
2. **Spectacular** → Vylepši pokročilou analýzou
3. **Visualize** → Zkontroluj výsledek v real-time
4. **Edit** → Uprav problematické části
5. **Deploy** → Nahraj do lighting controlleru

### Testing Commands
```bash
# Rychlý test
dmx-analyzer spectacular test.wav -o test.tml
dmx-analyzer visualize test.tml test.wav

# Batch processing
for song in *.wav; do
    dmx-analyzer spectacular "$song" -o "${song%.wav}.tml"
done
```

## 📊 Scene Path Mapování

### Příklady Scene Paths
```
LED_walls/Walls_all/Walls_red.scex     → Všechny wall spoty červené
Bodovky/Bodovky_all/Bodovka_blue.scex  → Všechny bodovky modré
Moving_heads/MH_oven_yellow.scex       → Moving heads žluté
UV/UV.scex                             → UV světla aktivní
Special_efects/Walls_flashing_snake/   → Speciální efekty
```

### Barevné Mapování
```python
{
    'red': (255, 50, 50),      # Vysoká energie
    'blue': (50, 50, 255),     # Nízká energie
    'yellow': (255, 255, 50),  # Pozitivní nálada
    'green': (50, 255, 50),    # Střední části
    'purple': (255, 50, 255),  # Emocionální momenty
    'white': (255, 255, 255),  # Transients
}
```

## 🌐 Windows Export System

### Ceremonial Structure
```
C:\Users\itbrn\TheLightingController\LightShows\Infinit Maximus - Jarda Vazny\
├── Music\
│   ├── Kokoti\           # Ceremonial directory
│   │   ├── song1.mp3
│   │   └── song2.wav
│   └── Placata\          # Another ceremonial
│       └── track.mp3
└── generated_scenes_systematic\
    ├── individual\
    ├── groups\
    └── zones\
```

### Export Workflow
```bash
# 1. Vytvoř ceremonial strukturu
dmx-analyzer create-ceremonial "Kokoti"

# 2. Zkopíruj hudbu do ceremonial/music/
cp song.wav Kokoti/music/

# 3. Generuj timeline
dmx-analyzer spectacular Kokoti/music/song.wav -o Kokoti/timelines/song.tml

# 4. Export pro Windows
dmx-analyzer export Kokoti/timelines/song.tml -o Kokoti/exports/song_windows.tml --ceremonial "Kokoti"
```

### Path Conversion Features
- **Automatická konverze**: Unix ↔ Windows cesty
- **České znaky**: ž→z, š→s, č→c, ř→r, ě→e
- **CP1250 encoding**: Kompatibilita s Windows
- **Ceremonial paths**: Organizace podle ceremoniálů

## 🐛 Známé Omezení

### Pygame Mixer
- Seek operace vyžadují restart audio
- Budoucí verze: migrace na ffmpeg-python

### Performance
- Pro pomalší systémy: snížit rozlišení okna
- Editovat `sauna_renderer.py`: width=800, height=600

### Windows Export
- Testováno jen s CP1250 encoding
- Dlouhé názvy souborů (>260 znaků) mohou způsobit problémy

## 🔮 Budoucí Rozšíření

### Plánované Funkce
- **Video Export**: Render do MP4 souboru
- **Live Control**: Real-time editace během přehrávání
- **Remote Control**: Ovládání přes webové rozhraní
- **BPM Visualization**: Real-time zobrazení BPM
- **Audio Waveform**: Zobrazení audio waveform

### Možná Rozšíření
- **Web Interface**: Browser-based vizualizátor
- **VR Support**: Virtual Reality pro saunu
- **Multi-room**: Podpora více sauny najednou

## 💡 Best Practices

### Optimalizace Show
- Testuj nejdřív krátké úseky (30s)
- Iterativní approach - postupně vylepšuj
- Backup originals - zachovej originální timeline
- Performance testing na cílové hardware

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
PYTHONPATH=. python -m dmx_analyzer.visualizer.visualizer_app timeline.tml song.wav
```

## 🎉 Výsledek

Kompletní systém pro tvorbu spektakulárních světelných show v saune s:
- ✅ Pokročilou hudební analýzou
- ✅ Real-time vizualizací
- ✅ Intuitivním ovládáním
- ✅ Professional výstupem pro lighting controller

Projekt umožňuje vytvářet "magnificientni svetelnou show" s perfektní synchronizací hudby a světel! 🎵💡✨

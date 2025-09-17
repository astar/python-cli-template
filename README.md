# DMX Music Analyzer

> Intelligent DMX lighting control system with music analysis for sauna environments

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced tool that analyzes music tracks and automatically generates synchronized DMX lighting timelines for sauna lighting systems. Creates immersive lighting experiences that respond to musical features like beats, energy, and mood.

## 🎵 Features

- **Audio Analysis**: Extract beats, tempo, energy, and musical features from audio files
- **DMX Timeline Generation**: Automatically create .tml timeline files compatible with lighting controllers
- **Sauna-Optimized**: Designed for sauna environments with appropriate fixture mappings
- **Music Synchronization**: Beat-aligned lighting effects that respond to music
- **Energy-Based Lighting**: Color and intensity changes based on musical energy
- **Configurable Fixtures**: Support for various DMX fixture types (RGBW spots, LED strips, moving heads)
- **Professional Output**: Generates timeline files in standard DMX controller format

## 🏗 System Architecture

The system works with your existing sauna DMX lighting setup:

```
Audio File → Music Analysis → Feature Extraction → DMX Timeline → Lighting Controller
   (.wav)         ↓               ↓                  (.tml)           ↓
                 BPM         Energy/Valence                    Synchronized
                Beats        Color Mapping                    Light Show
               Onsets        Effect Timing
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/jarda/dmx-music-analyzer.git
cd dmx-music-analyzer

# Install dependencies
uv install

# Or using pip
pip install -e .
```

### Basic Usage

```bash
# Analyze a music file and generate DMX timeline
dmx-analyzer analyze path/to/music.wav

# Specify output location
dmx-analyzer analyze music.wav -o custom_timeline.tml

# Use custom DMX fixtures configuration
dmx-analyzer analyze music.wav --dmx-config fixtures.ini

# Override BPM detection
dmx-analyzer analyze music.wav --bpm 128.0

# Dry run to preview what would be generated
dmx-analyzer analyze music.wav --dry-run
```

## 📁 Supported Fixture Types

Based on your sauna DMX setup:

- **Ceiling Spots (Bodovky)**: 12x RGBW ceiling-mounted spots
- **Wall Spots (Spot_stěna)**: 8x RGBW wall-mounted spots
- **LED Bench Strips (LED_lavice)**: 11x LED strips along benches
- **LED Stove (LED_kamna)**: 2x LED strips by the stove
- **Moving Heads**: 5x Intimidator Spot 375Z IRC with pan/tilt/color/gobo
- **UV Lights**: UV effect fixtures
- **DMX Outlets**: 7x DMX-controlled power outlets

## 🎛 Timeline Generation Features

### Beat Synchronization
- Automatic BPM detection from audio
- Strong beat emphasis (every 4th beat)
- Moving head choreography on beats
- Flash effects synchronized to rhythm

### Energy-Based Effects
- High energy moments trigger wall LED flashes
- Medium energy creates individual fixture effects
- Low energy maintains ambient lighting
- Color selection based on musical intensity

### Ambient Lighting
- Background lighting based on mood (valence)
- Gentle fades for atmosphere
- Stove lighting for warmth in happy songs
- Ceiling spots for general illumination

### Smart Color Mapping
- **High Energy**: Red, Orange, Yellow
- **Medium Energy**: Green, Cool White, Warm White
- **Low Energy**: Blue, Azure, Purple
- Musical key influences color selection

## 🔧 Configuration

### DMX Fixtures Configuration

The system reads your existing `fixtures.ini` file:

```ini
[Fixture1]
address = 1
name = Spot_(stěna)
model = Spot_RGBW (stěna)
group = b

[Fixture2]
address = 33
name = Bodovka_(strop)
model = Bodovka_RGBW_(strop)
group = a
```

### Generation Configuration

Customize timeline generation behavior:

```python
from dmx_analyzer.models import GenerationConfig

config = GenerationConfig(
    min_event_duration=0.5,      # Minimum effect duration
    max_event_duration=5.0,      # Maximum effect duration
    energy_threshold=0.5,        # Energy level for triggering effects
    beat_sync=True,              # Sync to detected beats
    color_intensity_mapping=True  # Map audio features to colors
)
```

## 🎯 Example Output

Generated timeline files are compatible with your lighting controller:

```ini
[Params]
Version = 0.2
LightTimeLines = 10
MediaTimeLines = 1
ShowWaveForm = 1
MaxTime = 0:30:00

[Event_0]
TimeLineIndex = 2
StartTime = 0:00:00.0
Path = Music/your_song.wav
Length = 0:04:32.5

[Event_1]
TimeLineIndex = 3
StartTime = 0:00:02.7
Path = LED_walls/Walls_single/Walls_1/Walls_1_yellow.scex
Length = 0:00:05.0
Speed = 100
SpeedType = 2
```

## 📊 Audio Analysis

The system extracts comprehensive musical features:

- **BPM**: Beats per minute and tempo stability
- **Energy**: Musical intensity and dynamics
- **Valence**: Mood/positivity of the track
- **Spectral Features**: Brightness and tone characteristics
- **Beat Times**: Precise timing of musical beats
- **Onset Detection**: Note attack times for sharp effects
- **Key Detection**: Musical key estimation

## 🛠 Development

### Project Structure

```
dmx-music-analyzer/
├── src/dmx_analyzer/
│   ├── __init__.py
│   ├── __main__.py           # CLI interface
│   ├── models.py             # Data models
│   ├── music_analyzer.py     # Audio analysis
│   ├── timeline_generator.py # Timeline creation
│   └── logging.py           # Logging utilities
├── tests/                   # Test suite
├── data/                   # Sample data
└── pyproject.toml          # Dependencies
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific tests
pytest tests/test_music_analyzer.py
```

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# All quality checks
make check
```

## 🎨 Advanced Usage

### Custom Scene Mapping

Map audio features to specific lighting scenes:

```python
from dmx_analyzer import MusicAnalyzer, TimelineGenerator

analyzer = MusicAnalyzer()
analysis = analyzer.analyze_file("song.wav")

generator = TimelineGenerator()
generator.load_fixtures("path/to/fixtures.ini")

# Customize color mappings
generator.energy_colors['high'] = ['red', 'orange', 'yellow']
generator.energy_colors['low'] = ['blue', 'purple']

timeline = generator.generate_timeline(analysis)
```

### Integration with Lighting Controllers

The generated `.tml` files work directly with:
- **Infinit Maximus** lighting controllers
- **TheeLightingController** software
- Most DMX timeline-based systems

## 🔗 Related Projects

- [Audio Analysis with librosa](https://librosa.org/)
- [DMX Protocol Documentation](https://en.wikipedia.org/wiki/DMX512)
- [Lighting Controller Integration](docs/controller_integration.md)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`make check`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Create a Pull Request

## 🆘 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/jarda/dmx-music-analyzer/issues)
- 💬 [Discussions](https://github.com/jarda/dmx-music-analyzer/discussions)

---

*Transform your sauna into an immersive musical lighting experience!* 🎵💡

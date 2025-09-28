"""Main CLI entry point."""

import sys
from pathlib import Path

import click

from dmx_analyzer import __version__
from dmx_analyzer.logging import get_logger

# Get logger for this module - will be created only once
logger = get_logger(__name__)


@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Configuration file path",
)
@click.pass_context
def cli(ctx: click.Context, *, verbose: bool, config: Path | None) -> None:
    """DMX lighting control system with music analysis for sauna environments."""
    ctx.ensure_object(dict)

    # Set up logging based on verbosity
    if verbose:
        # Create a new logger with DEBUG level for verbose mode
        debug_logger = get_logger(__name__, level="DEBUG")
        debug_logger.debug("Verbose logging enabled")

    if config:
        logger.info("Using config file: %s", config)
        # Load custom config here


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output timeline file path"
)
@click.option(
    "--dmx-config",
    type=click.Path(exists=True, path_type=Path),
    help="DMX fixtures configuration file",
)
@click.option("--bpm", type=float, help="Override detected BPM")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def analyze(
    audio_file: Path,
    output: Path | None,
    dmx_config: Path | None,
    bpm: float | None,
    *,
    dry_run: bool,
) -> None:
    """Analyze audio file and generate DMX timeline."""
    if dry_run:
        click.echo(f"Would analyze {audio_file} -> {output or 'auto-generated'}")
        logger.info("Dry run mode: analyzing %s", audio_file)
        return

    # Standard analysis
    from .music_analyzer import MusicAnalyzer
    from .timeline_generator import TimelineGenerator

    try:
        click.echo(f"🎵 Analyzing audio file: {audio_file}...")

        # Create analyzer
        analyzer = MusicAnalyzer()
        analysis = analyzer.analyze_file(audio_file, bpm)

        click.echo(f"✓ BPM detected: {analysis.features.bpm:.1f}")
        click.echo(f"✓ Duration: {analysis.duration:.1f}s")
        click.echo(f"✓ Energy: {analysis.features.energy:.2f}")
        click.echo(f"✓ Valence: {analysis.features.valence:.2f}")

        # Generate timeline
        generator = TimelineGenerator()
        if dmx_config:
            generator.load_fixtures(dmx_config)

        timeline = generator.generate_timeline(analysis, output)

        click.echo(f"✓ Generated timeline with {len(timeline.events)} events")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        logger.error("Analysis failed: %s", e)
        sys.exit(1)


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output timeline file path"
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def spectacular(
    audio_file: Path,
    output: Path | None,
    *,
    dry_run: bool,
) -> None:
    """Generate spectacular lighting show with advanced analysis."""
    if dry_run:
        click.echo(
            f"Would create spectacular show for {audio_file} -> {output or 'auto-generated'}"
        )
        return

    from .spectacular_timeline_generator import create_spectacular_timeline

    try:
        click.echo(f"🎼 Creating spectacular lighting show for: {audio_file}...")
        click.echo("🔬 Running advanced music analysis...")

        # Generate output path if not provided
        if not output:
            output = audio_file.with_suffix(".tml")

        # Create spectacular timeline
        timeline = create_spectacular_timeline(audio_file, output)

        click.echo(
            f"✨ Spectacular timeline created with {len(timeline.events)} effects!"
        )
        click.echo(f"💾 Saved to: {output}")

        # Show analysis summary
        click.echo("\n🎯 Analysis Summary:")
        click.echo(f"   Duration: {timeline.audio_length}")
        click.echo(f"   Events: {len(timeline.events)}")
        click.echo(f"   Timelines: {timeline.light_timelines}")

    except Exception as e:
        click.echo(f"❌ Error creating spectacular show: {e}", err=True)
        logger.error("Spectacular generation failed: %s", e)
        sys.exit(1)


@cli.command()
@click.argument("timeline_file", type=click.Path(exists=True, path_type=Path))
@click.argument("audio_file", type=click.Path(exists=True, path_type=Path))
def visualize(timeline_file: Path, audio_file: Path) -> None:
    """Real-time visualization of DMX timeline with audio playback."""
    try:
        from .visualizer.visualizer_app import run_visualizer

        click.echo("🎥 Starting real-time visualizer...")
        click.echo(f"   Timeline: {timeline_file}")
        click.echo(f"   Audio: {audio_file}")

        run_visualizer(timeline_file, audio_file)

    except ImportError as e:
        click.echo("❌ Visualization requires pygame: pip install pygame", err=True)
        click.echo(f"   Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Visualization error: {e}", err=True)
        logger.error("Visualization failed: %s", e)
        sys.exit(1)


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True, path_type=Path))
def music_director(audio_file: Path) -> None:
    """Advanced Music Director Visualizer with intelligent zone mapping."""
    try:
        from .visualizer.music_director_visualizer import run_music_director

        click.echo("🎼 Starting Music Director Visualizer...")
        click.echo("🎹 Advanced spectral analysis and intelligent light mapping")
        click.echo(f"   Audio: {audio_file}")

        run_music_director(audio_file)

    except ImportError as e:
        click.echo(
            "❌ Music Director requires pygame and librosa: pip install pygame librosa",
            err=True,
        )
        click.echo(f"   Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Music Director error: {e}", err=True)
        logger.error("Music Director failed: %s", e)
        sys.exit(1)


@cli.command()
@click.argument("timeline_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output timeline file path"
)
@click.option(
    "--target",
    type=click.Choice(["windows", "unix"]),
    default="windows",
    help="Target platform for export"
)
@click.option(
    "--encoding",
    type=str,
    default="cp1250",
    help="Target encoding (default: cp1250 for Windows)"
)
@click.option(
    "--ceremonial",
    type=str,
    help="Ceremonial name for directory structure (e.g., 'Kokoti', 'Placata')"
)
def export(
    timeline_file: Path,
    output: Path | None,
    target: str,
    encoding: str,
    ceremonial: str | None,
) -> None:
    """Export timeline with Windows-compatible paths and encoding."""
    from .settings import ExportConfig
    from .models import DMXTimeline
    import configparser

    try:
        click.echo(f"📤 Exporting timeline for {target} platform...")
        click.echo(f"   Source: {timeline_file}")
        click.echo(f"   Target encoding: {encoding}")
        if ceremonial:
            click.echo(f"   Ceremonial: {ceremonial}")

        # Generate output path if not provided
        if not output:
            suffix = "_windows" if target == "windows" else "_unix"
            output = timeline_file.with_stem(f"{timeline_file.stem}{suffix}")

        # Read existing timeline file - try UTF-8 first, then CP1250
        config = configparser.ConfigParser(interpolation=None)
        try:
            config.read(timeline_file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                config.read(timeline_file, encoding='cp1250')
                click.echo("   ℹ️  Read file using CP1250 encoding")
            except UnicodeDecodeError:
                config.read(timeline_file, encoding='latin-1')
                click.echo("   ℹ️  Read file using Latin-1 encoding")

        # Create DMXTimeline from config
        timeline = DMXTimeline()

        # Parse params section
        if 'Params' in config:
            params = config['Params']
            timeline.version = params.get('Version', '0.2')
            timeline.light_timelines = int(params.get('LightTimeLines', '10'))
            timeline.media_timelines = int(params.get('MediaTimeLines', '1'))
            timeline.show_waveform = bool(int(params.get('ShowWaveForm', '1')))
            timeline.max_time = params.get('MaxTime', '0:30:00')

        # Parse events
        from .models import DMXEvent, SpeedType

        for section_name in config.sections():
            if section_name.startswith('Event_'):
                event_data = dict(config[section_name])

                # Skip audio event (Event_0)
                if section_name == 'Event_0':
                    timeline.audio_file = event_data.get('path', event_data.get('Path', ''))
                    timeline.audio_length = event_data.get('length', event_data.get('Length', ''))
                    continue

                event = DMXEvent(
                    timeline_index=int(event_data.get('timelineindex', event_data.get('TimeLineIndex', '3'))),
                    start_time=event_data.get('starttime', event_data.get('StartTime', '0:00:00.0')),
                    path=event_data.get('path', event_data.get('Path', '')),
                    length=event_data.get('length', event_data.get('Length')),
                    speed=int(event_data.get('speed', event_data.get('Speed', '100'))),
                    speed_type=SpeedType(int(event_data.get('speedtype', event_data.get('SpeedType', '2')))),
                    fade_in=int(event_data.get('fadein', event_data.get('FadeIn', '0'))) if event_data.get('fadein') or event_data.get('FadeIn') else None,
                    fade_out=int(event_data.get('fadeout', event_data.get('FadeOut', '0'))) if event_data.get('fadeout') or event_data.get('FadeOut') else None,
                    bpm=int(event_data.get('bpm', event_data.get('BPM', '0'))) if event_data.get('bpm') or event_data.get('BPM') else None,
                    volume=int(event_data.get('volume', event_data.get('Volume', '0'))) if event_data.get('volume') or event_data.get('Volume') else None,
                )
                timeline.add_event(event)

        # Configure export settings
        export_config = ExportConfig(
            target_platform=target,
            convert_encoding=True
        )

        # Update path converter encoding and ceremonial settings
        from .path_converter import get_path_converter, PathConfig
        path_config = PathConfig(
            target_encoding=encoding,
            ceremonial_name=ceremonial
        )
        converter = get_path_converter(path_config)

        # Export timeline
        exported_content = timeline.to_tml_format(export_config)

        # Write to file with appropriate encoding
        output_encoding = encoding if target == "windows" else "utf-8"
        with open(output, 'w', encoding=output_encoding) as f:
            f.write(exported_content)

        click.echo(f"✅ Timeline exported successfully!")
        click.echo(f"   Output: {output}")
        click.echo(f"   Platform: {target}")
        click.echo(f"   Encoding: {output_encoding}")
        click.echo(f"   Events: {len(timeline.events)}")

        # Show sample path conversion
        if timeline.events:
            sample_event = timeline.events[0]
            click.echo(f"\n📝 Sample path conversion:")
            click.echo(f"   Original: {sample_event.path}")

            from .path_converter import get_path_converter
            converter = get_path_converter()
            converted_path = converter.convert_scene_path(sample_event.path, target)
            click.echo(f"   Converted: {converted_path}")

    except Exception as e:
        click.echo(f"❌ Export failed: {e}", err=True)
        logger.error("Export failed: %s", e)
        sys.exit(1)


@cli.command()
@click.argument("ceremonial_name", type=str)
@click.option(
    "--base-dir",
    type=click.Path(path_type=Path),
    default=Path.cwd(),
    help="Base directory for ceremonial structure"
)
def create_ceremonial(ceremonial_name: str, base_dir: Path) -> None:
    """Create ceremonial directory structure for organized timeline management."""
    from .path_converter import PathConverter, PathConfig

    try:
        click.echo(f"🎭 Creating ceremonial structure for: {ceremonial_name}")

        # Create safe directory name
        converter = PathConverter()
        safe_name = converter.get_safe_filename(ceremonial_name)

        # Create directory structure
        ceremonial_dir = base_dir / safe_name
        music_dir = ceremonial_dir / "music"
        timelines_dir = ceremonial_dir / "timelines"
        exports_dir = ceremonial_dir / "exports"

        # Create directories
        music_dir.mkdir(parents=True, exist_ok=True)
        timelines_dir.mkdir(parents=True, exist_ok=True)
        exports_dir.mkdir(parents=True, exist_ok=True)

        # Create README with structure explanation
        readme_content = f"""# {ceremonial_name} - DMX Light Show Project

## Directory Structure

- `music/` - Audio files for this ceremonial
- `timelines/` - Generated .tml timeline files
- `exports/` - Windows-compatible exports for target system

## Usage

### 1. Add Music
Copy your audio files to the `music/` directory.

### 2. Generate Timeline
```bash
dmx-analyzer spectacular music/your_song.wav -o timelines/your_song.tml
```

### 3. Export for Windows
```bash
dmx-analyzer export timelines/your_song.tml -o exports/your_song_windows.tml --target windows --ceremonial "{ceremonial_name}"
```

### 4. Windows Target Paths
- Music: `C:\\Users\\itbrn\\TheLightingController\\LightShows\\Infinit Maximus - Jarda Vazny\\Music\\{safe_name}\\`
- Scenes: `C:\\Users\\itbrn\\TheLightingController\\LightShows\\Infinit Maximus - Jarda Vazny\\generated_scenes_systematic\\`

## Created with DMX Music Analyzer
"""

        readme_path = ceremonial_dir / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")

        click.echo(f"✅ Ceremonial structure created:")
        click.echo(f"   📁 {ceremonial_dir}")
        click.echo(f"   📁 {music_dir}")
        click.echo(f"   📁 {timelines_dir}")
        click.echo(f"   📁 {exports_dir}")
        click.echo(f"   📄 {readme_path}")

        click.echo(f"\n🎵 Next steps:")
        click.echo(f"1. Copy audio files to: {music_dir}")
        click.echo(f"2. Generate timeline: dmx-analyzer spectacular music/song.wav -o timelines/song.tml")
        click.echo(f"3. Export for Windows: dmx-analyzer export timelines/song.tml --ceremonial \"{ceremonial_name}\"")

    except Exception as e:
        click.echo(f"❌ Failed to create ceremonial structure: {e}", err=True)
        logger.error("Ceremonial creation failed: %s", e)
        sys.exit(1)


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output timeline file path"
)
def dynamic(
    audio_file: Path,
    output: Path | None,
) -> None:
    """Generate EXPLOSIVE dynamic timeline with beat-responsive effects."""
    from .dynamic_spectacular_generator import create_dynamic_spectacular_timeline

    try:
        click.echo("💥 Creating DYNAMIC explosive lighting show...")
        click.echo(
            "🎯 Beat detection + Strobe effects + Circular waves + Bass explosions"
        )
        click.echo(f"🎵 Audio: {audio_file}")

        # Generate output path if not provided
        if not output:
            output = audio_file.with_stem(f"{audio_file.stem}_DYNAMIC").with_suffix(
                ".tml"
            )

        # Create dynamic spectacular timeline
        timeline = create_dynamic_spectacular_timeline(audio_file, output)

        click.echo(
            f"💥 EXPLOSIVE timeline created with {len(timeline.events)} dynamic effects!"
        )
        click.echo(f"💾 Saved to: {output}")

        # Show effects summary
        click.echo("\n🎪 Dynamic Effects Applied:")
        click.echo("   ⚡ Beat-responsive flashes every 4th beat")
        click.echo("   🌪️  Stroboscopic effects on high frequencies")
        click.echo("   🌊 Circular waves across ceiling")
        click.echo("   🎭 Alternating up/down effects")
        click.echo("   💥 Bass explosions on strong low frequencies")
        click.echo("   🏃 Moving head chase sequences")

    except Exception as e:
        click.echo(f"❌ Error creating dynamic show: {e}", err=True)
        logger.error("Dynamic generation failed: %s", e)
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled.", err=True)
        logger.warning("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        logger.exception("Unexpected error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()

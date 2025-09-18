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

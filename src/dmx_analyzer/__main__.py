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

    # Implementation here
    click.echo(f"Analyzing audio file: {audio_file}...")
    logger.info("Starting music analysis: %s", audio_file)


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

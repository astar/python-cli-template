"""Main CLI entry point."""

import sys
from pathlib import Path

import click

from your_package import __version__
from your_package.logging import get_logger

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
    """Your CLI tool description."""
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
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output file path"
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["json", "yaml", "csv"]),
    default="json",
    help="Output format",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def process(
    input_file: Path,
    output: Path | None,
    output_format: str,
    *,
    dry_run: bool,
) -> None:
    """Process input file and generate output."""
    if dry_run:
        click.echo(f"Would process {input_file} -> {output} ({output_format})")
        logger.info("Dry run mode: %s -> %s", input_file, output)
        return

    # Implementation here
    click.echo(f"Processing {input_file}...")
    logger.info("Processing file: %s", input_file)


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

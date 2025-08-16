"""Logging utilities with singleton pattern to prevent duplicate loggers."""

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler

# Keep track of configured loggers to prevent duplicates
_configured_loggers = set()


def get_logger(
    name: str,
    level: str = "INFO",
    log_file: Path | None = None,
    *,
    rich_console: bool = True,
) -> logging.Logger:
    """Get a logger instance - configured only once per name.

    This prevents duplicate log messages that occur when loggers are configured
    multiple times.

    Args:
        name: Logger name (use __name__ or module path)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for file logging
        rich_console: Whether to use Rich formatting for console output

    Returns:
        Configured logger instance

    Example:
        ```python
        from your_package.logging import get_logger

        logger = get_logger(__name__)
        logger.info("This will only appear once!")

        # Multiple calls return the same configured logger
        logger2 = get_logger(__name__)  # Same instance as logger
        ```
    """
    logger = logging.getLogger(name)

    # Create unique key for this configuration
    config_key = f"{name}:{level}:{log_file}:{rich_console}"

    # Only configure if not already configured with same parameters
    if config_key not in _configured_loggers:
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        logger.setLevel(getattr(logging, level.upper()))

        handlers = []

        # Console handler with Rich formatting
        if rich_console:
            handlers.append(
                RichHandler(rich_tracebacks=True, show_path=False, show_time=True)
            )
        else:
            console_handler = logging.StreamHandler(sys.stdout)
            handlers.append(console_handler)

        # Optional file handler
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            handlers.append(file_handler)

        # Set formatter for all handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Prevent propagation to avoid duplicate messages
        logger.propagate = False

        # Mark as configured
        _configured_loggers.add(config_key)

    return logger


def setup_logging(
    level: str = "INFO", log_file: Path | None = None, *, rich_console: bool = True
) -> logging.Logger:
    """Set up root logger configuration.

    This is a convenience function that configures the root logger.
    For module-specific loggers, use get_logger(__name__) instead.

    Args:
        level: Logging level
        log_file: Optional file path for file logging
        rich_console: Whether to use Rich formatting

    Returns:
        Configured root logger
    """
    return get_logger("root", level, log_file, rich_console=rich_console)


def clear_logger_cache() -> None:
    """Clear the logger cache - useful for testing."""
    _configured_loggers.clear()

    # Also remove all handlers from all loggers
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

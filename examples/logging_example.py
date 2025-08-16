#!/usr/bin/env python3
"""Example demonstrating the singleton logging pattern.

This shows how to use the logging utilities to prevent duplicate log messages.
"""

from your_package.logging import get_logger

# Module-level logger - will be created only once
logger = get_logger(__name__)


def function_with_logging() -> None:
    """Function that logs messages."""
    # This logger will be the same instance as the module-level logger
    local_logger = get_logger(__name__)

    local_logger.info(
        "This message appears only once, even though called multiple times"
    )
    local_logger.debug("Debug message (won't show unless debug enabled)")


def demonstrate_singleton_pattern() -> None:
    """Demonstrate that multiple calls return same logger."""
    logger1 = get_logger("example.module")
    logger2 = get_logger("example.module")
    logger3 = get_logger("example.module")

    print(f"logger1 id: {id(logger1)}")
    print(f"logger2 id: {id(logger2)}")
    print(f"logger3 id: {id(logger3)}")
    print(f"All same instance: {logger1 is logger2 is logger3}")

    # Only one log message despite multiple loggers
    logger1.info("Message from logger1")
    logger2.info("Message from logger2")
    logger3.info("Message from logger3")


def demonstrate_different_levels() -> None:
    """Show different logging levels."""
    debug_logger = get_logger("debug.example", level="DEBUG")
    info_logger = get_logger("info.example", level="INFO")
    warning_logger = get_logger("warning.example", level="WARNING")

    # Debug logger shows all levels
    debug_logger.debug("Debug message (visible)")
    debug_logger.info("Info message")
    debug_logger.warning("Warning message")

    # Info logger only shows INFO and above
    info_logger.debug("Debug message (hidden)")
    info_logger.info("Info message")
    info_logger.warning("Warning message")

    # Warning logger only shows WARNING and above
    warning_logger.debug("Debug message (hidden)")
    warning_logger.info("Info message (hidden)")
    warning_logger.warning("Warning message")


if __name__ == "__main__":
    print("=== Singleton Pattern Demo ===")
    demonstrate_singleton_pattern()

    print("\n=== Function Logging Demo ===")
    # Call function multiple times - should only configure logger once
    for _ in range(3):
        function_with_logging()

    print("\n=== Different Levels Demo ===")
    demonstrate_different_levels()

    print("\n=== No Duplicate Messages ===")
    # Even with repeated logger creation, no duplicates
    for i in range(5):
        temp_logger = get_logger("temp.example")
        temp_logger.info(
            "Iteration %d - this should appear only once per iteration", i + 1
        )

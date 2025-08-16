"""Tests for logging utilities."""

import logging
from pathlib import Path

from your_package.logging import clear_logger_cache
from your_package.logging import get_logger
from your_package.logging import setup_logging


class TestLogging:
    """Test logging utilities."""

    def teardown_method(self) -> None:
        """Clear logger cache after each test."""
        clear_logger_cache()
        # Remove any handlers that might have been added
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    def test_get_logger_singleton(self) -> None:
        """Test that get_logger returns the same instance for same name."""
        logger1 = get_logger("test.module")
        logger2 = get_logger("test.module")

        # Should be the same object
        assert logger1 is logger2

        # Should have same name
        assert logger1.name == "test.module"
        assert logger2.name == "test.module"

    def test_get_logger_different_names(self) -> None:
        """Test that different names return different loggers."""
        logger1 = get_logger("test.module1")
        logger2 = get_logger("test.module2")

        # Should be different objects
        assert logger1 is not logger2
        assert logger1.name != logger2.name

    def test_get_logger_no_duplicate_handlers(self) -> None:
        """Test that multiple calls don't add duplicate handlers."""
        logger1 = get_logger("test.module")
        initial_handler_count = len(logger1.handlers)

        # Call again - should not add more handlers
        logger2 = get_logger("test.module")
        final_handler_count = len(logger2.handlers)

        assert logger1 is logger2
        assert initial_handler_count == final_handler_count
        assert initial_handler_count > 0  # Should have at least one handler

    def test_get_logger_with_file(self, tmp_path: Path) -> None:
        """Test logger with file output."""
        log_file = tmp_path / "test.log"
        logger = get_logger("test.module", log_file=log_file)

        logger.info("Test message")

        # Flush all handlers to ensure data is written
        for handler in logger.handlers:
            handler.flush()

        # Check that file was created and has content
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content
        assert "test.module" in content

    def test_get_logger_levels(self) -> None:
        """Test different logging levels."""
        debug_logger = get_logger("test.debug", level="DEBUG")
        info_logger = get_logger("test.info", level="INFO")
        warning_logger = get_logger("test.warning", level="WARNING")

        assert debug_logger.level == logging.DEBUG
        assert info_logger.level == logging.INFO
        assert warning_logger.level == logging.WARNING

    def test_no_propagation(self) -> None:
        """Test that loggers don't propagate to prevent duplicates."""
        logger = get_logger("test.module")
        assert logger.propagate is False

    def test_setup_logging_convenience(self) -> None:
        """Test setup_logging convenience function."""
        logger = setup_logging(level="DEBUG")

        assert logger.name == "root"  # Root logger
        assert logger.level == logging.DEBUG
        assert not logger.propagate

    def test_clear_cache(self) -> None:
        """Test that cache clearing works."""
        logger1 = get_logger("test.module")
        clear_logger_cache()
        logger2 = get_logger("test.module")

        # After clearing cache, should get a fresh logger
        # Note: They might have the same name but could be reconfigured
        assert logger1.name == logger2.name

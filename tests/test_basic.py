import pytest
from app.utils.logger import setup_logger
from config.settings import BASE_DIR
import logging

def test_project_structure():
    """Test that the basic project structure exists."""
    assert BASE_DIR.exists(), "Base directory should exist"
    assert (BASE_DIR / "app").exists(), "App directory should exist"
    assert (BASE_DIR / "backend").exists(), "Backend directory should exist"
    assert (BASE_DIR / "data").exists(), "Data directory should exist"
    assert (BASE_DIR / "tests").exists(), "Tests directory should exist"

def test_logger_setup():
    """Test that the logger can be set up correctly."""
    logger = setup_logger("test_logger")
    assert logger is not None, "Logger should be created"
    assert logger.name == "test_logger", "Logger should have correct name"
    assert logger.level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL], \
        "Logger should have valid level" 
"""
Pytest configuration and fixtures for Biryani Maker tests.
"""

import sys
import pytest
from pathlib import Path
from typing import Generator

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
#                           GPIO MOCKING
# =============================================================================

@pytest.fixture(autouse=True)
def mock_gpio_module():
    """Automatically mock GPIO module for all tests."""
    from tests.mock.mock_gpio import MockGPIO

    # Create mock RPi module structure
    class MockRPi:
        GPIO = MockGPIO

    # Inject mock modules
    sys.modules['RPi'] = MockRPi
    sys.modules['RPi.GPIO'] = MockGPIO

    yield MockGPIO

    # Clean up
    MockGPIO.reset()
    if 'RPi' in sys.modules:
        del sys.modules['RPi']
    if 'RPi.GPIO' in sys.modules:
        del sys.modules['RPi.GPIO']


@pytest.fixture(autouse=True)
def mock_spidev_module():
    """Automatically mock spidev module for all tests."""
    from tests.mock.mock_sensors import MockSpiDev

    # Create mock spidev module
    class MockSpiDevModule:
        SpiDev = MockSpiDev

    sys.modules['spidev'] = MockSpiDevModule

    yield MockSpiDevModule

    if 'spidev' in sys.modules:
        del sys.modules['spidev']


# =============================================================================
#                           HARDWARE FIXTURES
# =============================================================================

@pytest.fixture
def mock_hardware():
    """Provide mock hardware manager for tests."""
    from tests.mock.mock_hardware import get_mock_hardware, reset_mock_hardware

    hardware = get_mock_hardware()
    hardware.reset()

    yield hardware

    reset_mock_hardware()


@pytest.fixture
def mock_temp_sensor(mock_hardware):
    """Provide mock temperature sensor."""
    return mock_hardware.temp_sensor


@pytest.fixture
def mock_weight_sensor(mock_hardware):
    """Provide mock weight sensor."""
    return mock_hardware.weight_sensor


# =============================================================================
#                           DATABASE FIXTURES
# =============================================================================

@pytest.fixture
def test_database(tmp_path):
    """Provide a temporary test database."""
    from config.database import DatabaseConnection

    db_path = tmp_path / "test_biryani.db"
    db = DatabaseConnection(db_path)

    yield db

    db.close()


@pytest.fixture
def initialized_database(test_database):
    """Provide an initialized test database with schema."""
    conn = test_database.get_connection()

    # Create minimal schema for testing
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS cooking_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            status TEXT CHECK(status IN ('running', 'completed', 'error', 'stopped'))
        );

        CREATE TABLE IF NOT EXISTS cooking_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER REFERENCES cooking_sessions(id),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            level TEXT CHECK(level IN ('info', 'warning', 'error', 'debug')),
            source TEXT,
            message TEXT
        );

        CREATE TABLE IF NOT EXISTS temperature_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER REFERENCES cooking_sessions(id),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature_celsius REAL
        );

        CREATE TABLE IF NOT EXISTS system_settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            steps_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_default BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()

    yield test_database


# =============================================================================
#                           CONFIG FIXTURES
# =============================================================================

@pytest.fixture
def gpio_config():
    """Provide GPIO configuration."""
    from config import gpio_config as cfg
    return cfg


@pytest.fixture
def timing_config():
    """Provide timing configuration."""
    from config import timing_config as cfg
    return cfg


# =============================================================================
#                           SERVICE FIXTURES
# =============================================================================

@pytest.fixture
def gpio_controller(mock_gpio_module, gpio_config):
    """Provide initialized GPIO controller."""
    from backend.hardware.gpio_controller import GPIOController

    controller = GPIOController()
    controller.initialize()

    yield controller

    controller.cleanup()


# =============================================================================
#                           UTILITY FIXTURES
# =============================================================================

@pytest.fixture
def event_log(mock_gpio_module):
    """Provide access to GPIO event log."""
    yield mock_gpio_module.get_event_log

    mock_gpio_module.clear_event_log()


@pytest.fixture
def capture_logs(caplog):
    """Capture log messages during test."""
    import logging

    caplog.set_level(logging.DEBUG)
    yield caplog


# =============================================================================
#                           MARKERS
# =============================================================================

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "hardware: marks tests requiring hardware simulation"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: marks integration tests"
    )

"""GPIO controller with Raspberry Pi / mock fallback."""

from __future__ import annotations

import sys
from pathlib import Path

from config import gpio_config as gpio_cfg
from config.logging_config import get_logger

logger = get_logger("biryani.hardware.gpio")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _load_gpio_module():
    try:
        import RPi.GPIO as GPIO  # type: ignore

        logger.info("Using real RPi.GPIO")
        return GPIO, False
    except (ImportError, RuntimeError):
        from tests.mock.mock_gpio import MockGPIO

        logger.info("Using MOCK GPIO (development mode)")
        return MockGPIO, True


GPIO, IS_MOCK = _load_gpio_module()

RELAY_ON = GPIO.LOW if gpio_cfg.ACTIVE_LOW else GPIO.HIGH
RELAY_OFF = GPIO.HIGH if gpio_cfg.ACTIVE_LOW else GPIO.LOW


class GPIOController:
    """Central GPIO initialization and relay control."""

    def __init__(self) -> None:
        self._initialized = False
        self.is_mock = IS_MOCK

    def initialize(self) -> None:
        if self._initialized:
            return

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in gpio_cfg.ALL_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, RELAY_OFF)

        self._initialized = True
        logger.info("GPIO initialized (%d pins)", len(gpio_cfg.ALL_PINS))

    def cleanup(self) -> None:
        if not self._initialized:
            return

        for pin in gpio_cfg.ALL_PINS:
            GPIO.output(pin, RELAY_OFF)

        GPIO.cleanup()
        self._initialized = False
        logger.info("GPIO cleaned up")

    def turn_on(self, pin: int) -> None:
        GPIO.output(pin, RELAY_ON)

    def turn_off(self, pin: int) -> None:
        GPIO.output(pin, RELAY_OFF)

    def all_off(self) -> None:
        for pin in gpio_cfg.ALL_PINS:
            GPIO.output(pin, RELAY_OFF)

"""Mixer motor control."""

from __future__ import annotations

from backend.hardware.gpio_controller import GPIOController
from config import gpio_config as gpio_cfg
from config.logging_config import get_logger

logger = get_logger("biryani.hardware.stirrer")


class MixerMotor:
    """Single-direction mixer motor relay."""

    def __init__(self, gpio: GPIOController) -> None:
        self._gpio = gpio
        self._pin = gpio_cfg.M1_PIN

    def on(self) -> None:
        self._gpio.turn_on(self._pin)
        logger.info("Mixer Motor ON")

    def off(self) -> None:
        self._gpio.turn_off(self._pin)
        logger.info("Mixer Motor OFF")

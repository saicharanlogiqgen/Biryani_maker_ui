"""Position motor control (180-degree timed rotation)."""

from __future__ import annotations

import time

from backend.hardware.gpio_controller import GPIOController
from config import gpio_config as gpio_cfg
from config import timing_config as timing
from config.logging_config import get_logger

logger = get_logger("biryani.hardware.stepper")


class PositionMotor:
    """Bidirectional position motor with timed 180-degree rotation."""

    def __init__(self, gpio: GPIOController) -> None:
        self._gpio = gpio
        self._pin_f = gpio_cfg.M2_F
        self._pin_b = gpio_cfg.M2_B

    def stop(self) -> None:
        self._gpio.turn_off(self._pin_f)
        self._gpio.turn_off(self._pin_b)
        logger.info("Position Motor STOP")

    def forward(self) -> None:
        self.stop()
        self._gpio.turn_on(self._pin_f)
        logger.info("Position Motor FORWARD 180 DEGREE")
        time.sleep(timing.POSITION_180_TIME)
        self.stop()

    def backward(self) -> None:
        self.stop()
        self._gpio.turn_on(self._pin_b)
        logger.info("Position Motor BACKWARD 180 DEGREE")
        time.sleep(timing.POSITION_180_TIME)
        self.stop()

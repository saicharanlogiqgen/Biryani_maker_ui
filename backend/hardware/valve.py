"""Bidirectional hydraulic valve control (rice bowl, mixer)."""

from __future__ import annotations

import time

from backend.hardware.gpio_controller import GPIOController
from config import timing_config as timing
from config.logging_config import get_logger

logger = get_logger("biryani.hardware.valve")


class HydraulicValve:
    """Controls a bidirectional hydraulic actuator via two relay pins."""

    def __init__(
        self,
        gpio: GPIOController,
        pin_forward: int,
        pin_backward: int,
        name: str,
    ) -> None:
        self._gpio = gpio
        self._pin_f = pin_forward
        self._pin_b = pin_backward
        self.name = name

    def _safe_stop(self) -> None:
        self._gpio.turn_off(self._pin_f)
        self._gpio.turn_off(self._pin_b)
        time.sleep(timing.SAFE_STOP_DELAY)

    def down(self) -> None:
        self._safe_stop()
        self._gpio.turn_on(self._pin_f)
        logger.info("%s DOWN", self.name)

    def up(self) -> None:
        self._safe_stop()
        self._gpio.turn_on(self._pin_b)
        logger.info("%s UP", self.name)

    def stop(self) -> None:
        self._safe_stop()
        logger.info("%s STOP", self.name)


class ElectronicValve:
    """Controls open/close electronic valve via two relay pins."""

    def __init__(
        self,
        gpio: GPIOController,
        pin_open: int,
        pin_close: int,
    ) -> None:
        self._gpio = gpio
        self._pin_open = pin_open
        self._pin_close = pin_close

    def stop(self) -> None:
        self._gpio.turn_off(self._pin_open)
        self._gpio.turn_off(self._pin_close)
        logger.info("Electronic Valve STOP")

    def open(self) -> None:
        self.stop()
        self._gpio.turn_on(self._pin_open)
        logger.info("Electronic Valve OPEN")

    def close(self) -> None:
        self.stop()
        self._gpio.turn_on(self._pin_close)
        logger.info("Electronic Valve CLOSE")

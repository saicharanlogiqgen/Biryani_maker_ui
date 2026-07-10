"""Unified machine hardware interface."""

from __future__ import annotations

from backend.hardware.gpio_controller import GPIOController
from backend.hardware.stirrer import MixerMotor
from backend.hardware.stepper import PositionMotor
from backend.hardware.valve import ElectronicValve, HydraulicValve
from config import gpio_config as gpio_cfg
from config.logging_config import get_logger

logger = get_logger("biryani.hardware.machine")


class MachineController:
    """Aggregates all machine devices from the industrial control script."""

    def __init__(self, gpio: GPIOController) -> None:
        self.gpio = gpio
        self.rice_bowl = HydraulicValve(gpio, gpio_cfg.V1_F, gpio_cfg.V1_B, "Rice Bowl")
        self.mixer_hydraulic = HydraulicValve(gpio, gpio_cfg.V2_F, gpio_cfg.V2_B, "Mixer")
        self.mixer_motor = MixerMotor(gpio)
        self.position_motor = PositionMotor(gpio)
        self.electronic_valve = ElectronicValve(gpio, gpio_cfg.EV_OPEN, gpio_cfg.EV_CLOSE)

    def stop_main_devices(self) -> None:
        self.mixer_motor.off()
        self.position_motor.stop()
        self.rice_bowl.stop()
        self.mixer_hydraulic.stop()

    def stop_everything(self) -> None:
        self.stop_main_devices()
        self.electronic_valve.stop()
        logger.info("ALL DEVICES STOPPED")

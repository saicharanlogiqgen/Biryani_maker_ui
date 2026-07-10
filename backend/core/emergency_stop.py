"""Emergency stop controller."""

from __future__ import annotations

from backend.hardware.machine import MachineController
from config.logging_config import get_logger

logger = get_logger("biryani.core.emergency_stop")


class EmergencyStopController:
    def __init__(self, machine: MachineController) -> None:
        self._machine = machine

    def stop_main_devices(self) -> None:
        self._machine.stop_main_devices()
        logger.warning("Emergency: main devices stopped")

    def stop_everything(self) -> None:
        self._machine.stop_everything()
        logger.warning("EMERGENCY STOP — all devices stopped")

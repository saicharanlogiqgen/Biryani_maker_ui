"""
Mock hardware wrapper for testing.
Provides a unified interface to mock all hardware components.
"""

from typing import Dict, List, Optional, Callable
from datetime import datetime
import threading

from .mock_gpio import MockGPIO
from .mock_sensors import MockMAX6675, MockWeightSensor, MockSpiDev


class MockHardwareManager:
    """Manages all mock hardware components for testing."""

    def __init__(self):
        self._gpio = MockGPIO
        self._temp_sensor = MockMAX6675()
        self._weight_sensor = MockWeightSensor()
        self._spi = MockSpiDev()

        # Hardware state tracking
        self._motor_states: Dict[str, bool] = {
            "mixer": False,
            "position_fwd": False,
            "position_bwd": False,
        }

        self._valve_states: Dict[str, str] = {
            "valve1": "stopped",  # stopped, up, down
            "valve2": "stopped",
            "valve3": "off",  # on, off
        }

        self._stepper_state = {
            "enabled": False,
            "running": False,
            "direction": None,
            "steps": 0,
        }

        self._action_log: List[Dict] = []
        self._lock = threading.Lock()

    @property
    def gpio(self) -> type:
        """Get the mock GPIO class."""
        return self._gpio

    @property
    def temp_sensor(self) -> MockMAX6675:
        """Get the mock temperature sensor."""
        return self._temp_sensor

    @property
    def weight_sensor(self) -> MockWeightSensor:
        """Get the mock weight sensor."""
        return self._weight_sensor

    @property
    def spi(self) -> MockSpiDev:
        """Get the mock SPI device."""
        return self._spi

    # ==========================================================================
    #                           STATE SIMULATION
    # ==========================================================================

    def set_motor_state(self, motor: str, running: bool) -> None:
        """Set motor running state.

        Args:
            motor: Motor name (mixer, position_fwd, position_bwd).
            running: True if motor is running.
        """
        with self._lock:
            if motor in self._motor_states:
                self._motor_states[motor] = running
                self._log_action("motor", {"motor": motor, "running": running})

    def get_motor_state(self, motor: str) -> Optional[bool]:
        """Get motor running state.

        Args:
            motor: Motor name.

        Returns:
            True if running, False if stopped, None if unknown motor.
        """
        return self._motor_states.get(motor)

    def set_valve_state(self, valve: str, state: str) -> None:
        """Set valve state.

        Args:
            valve: Valve name (valve1, valve2, valve3).
            state: Valve state (stopped, up, down, on, off).
        """
        with self._lock:
            if valve in self._valve_states:
                self._valve_states[valve] = state
                self._log_action("valve", {"valve": valve, "state": state})

    def get_valve_state(self, valve: str) -> Optional[str]:
        """Get valve state.

        Args:
            valve: Valve name.

        Returns:
            Valve state string, or None if unknown valve.
        """
        return self._valve_states.get(valve)

    def set_stepper_state(
        self,
        enabled: Optional[bool] = None,
        running: Optional[bool] = None,
        direction: Optional[str] = None,
        steps: Optional[int] = None
    ) -> None:
        """Set stepper motor state.

        Args:
            enabled: Driver enabled state.
            running: Motor running state.
            direction: Direction (forward, backward).
            steps: Steps completed.
        """
        with self._lock:
            if enabled is not None:
                self._stepper_state["enabled"] = enabled
            if running is not None:
                self._stepper_state["running"] = running
            if direction is not None:
                self._stepper_state["direction"] = direction
            if steps is not None:
                self._stepper_state["steps"] = steps
            self._log_action("stepper", self._stepper_state.copy())

    def get_stepper_state(self) -> Dict:
        """Get stepper motor state.

        Returns:
            Dictionary with stepper state.
        """
        return self._stepper_state.copy()

    # ==========================================================================
    #                           LOGGING
    # ==========================================================================

    def _log_action(self, component: str, details: Dict) -> None:
        """Log a hardware action.

        Args:
            component: Hardware component name.
            details: Action details.
        """
        self._action_log.append({
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "details": details
        })

    def get_action_log(self) -> List[Dict]:
        """Get the action log.

        Returns:
            List of logged actions.
        """
        return self._action_log.copy()

    def clear_action_log(self) -> None:
        """Clear the action log."""
        self._action_log.clear()

    # ==========================================================================
    #                           RESET
    # ==========================================================================

    def reset(self) -> None:
        """Reset all hardware state."""
        with self._lock:
            # Reset GPIO
            self._gpio.reset()

            # Reset motors
            for motor in self._motor_states:
                self._motor_states[motor] = False

            # Reset valves
            self._valve_states = {
                "valve1": "stopped",
                "valve2": "stopped",
                "valve3": "off",
            }

            # Reset stepper
            self._stepper_state = {
                "enabled": False,
                "running": False,
                "direction": None,
                "steps": 0,
            }

            # Reset sensors
            self._temp_sensor.set_temperature(25.0)
            self._temp_sensor.set_fault(False)
            self._weight_sensor.set_weight(0.0)
            self._weight_sensor.set_fault(False)

            # Clear logs
            self._action_log.clear()

    # ==========================================================================
    #                           SCENARIO SIMULATION
    # ==========================================================================

    def simulate_cooking_scenario(
        self,
        start_temp: float = 25.0,
        target_temp: float = 100.0,
        duration_seconds: int = 120
    ) -> None:
        """Simulate a cooking temperature profile.

        Args:
            start_temp: Starting temperature.
            target_temp: Target cooking temperature.
            duration_seconds: Simulation duration.
        """
        import time

        temp_step = (target_temp - start_temp) / duration_seconds

        for i in range(duration_seconds):
            current_temp = start_temp + (temp_step * i)
            self._temp_sensor.set_temperature(current_temp)
            time.sleep(1)

    def simulate_sensor_fault(self, sensor: str, duration_seconds: int = 5) -> None:
        """Simulate a sensor fault.

        Args:
            sensor: Sensor name (temp, weight).
            duration_seconds: Fault duration.
        """
        import time

        if sensor == "temp":
            self._temp_sensor.set_fault(True)
            time.sleep(duration_seconds)
            self._temp_sensor.set_fault(False)
        elif sensor == "weight":
            self._weight_sensor.set_fault(True)
            time.sleep(duration_seconds)
            self._weight_sensor.set_fault(False)


# Global mock hardware instance
_mock_hardware: Optional[MockHardwareManager] = None


def get_mock_hardware() -> MockHardwareManager:
    """Get the global mock hardware manager.

    Returns:
        MockHardwareManager instance.
    """
    global _mock_hardware
    if _mock_hardware is None:
        _mock_hardware = MockHardwareManager()
    return _mock_hardware


def reset_mock_hardware() -> None:
    """Reset the global mock hardware manager."""
    global _mock_hardware
    if _mock_hardware is not None:
        _mock_hardware.reset()

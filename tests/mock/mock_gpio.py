"""
Mock GPIO module for testing on non-Raspberry Pi systems.
Mimics the RPi.GPIO interface for development on Windows/Mac.
"""

import threading
from typing import Dict, Optional, Callable, List
from datetime import datetime


class MockGPIO:
    """Mock implementation of RPi.GPIO module."""

    # Constants matching RPi.GPIO
    BCM = 11
    BOARD = 10
    OUT = 1
    IN = 0
    HIGH = 1
    LOW = 0
    PUD_UP = 22
    PUD_DOWN = 21
    PUD_OFF = 20
    RISING = 31
    FALLING = 32
    BOTH = 33

    # Internal state
    _mode: Optional[int] = None
    _pin_modes: Dict[int, int] = {}
    _pin_states: Dict[int, bool] = {}
    _pin_callbacks: Dict[int, List[Callable]] = {}
    _warnings: bool = True
    _lock = threading.Lock()

    # Event log for testing
    _event_log: List[Dict] = []
    _log_enabled: bool = True

    @classmethod
    def setmode(cls, mode: int) -> None:
        """Set the GPIO pin numbering mode.

        Args:
            mode: BCM or BOARD numbering scheme.
        """
        with cls._lock:
            cls._mode = mode
            cls._log_event("setmode", {"mode": "BCM" if mode == cls.BCM else "BOARD"})

    @classmethod
    def getmode(cls) -> Optional[int]:
        """Get the current GPIO pin numbering mode.

        Returns:
            Current mode (BCM or BOARD) or None if not set.
        """
        return cls._mode

    @classmethod
    def setwarnings(cls, flag: bool) -> None:
        """Enable or disable GPIO warnings.

        Args:
            flag: True to enable warnings, False to disable.
        """
        cls._warnings = flag

    @classmethod
    def setup(cls, pin: int, mode: int, initial: Optional[int] = None,
              pull_up_down: Optional[int] = None) -> None:
        """Configure a GPIO pin.

        Args:
            pin: GPIO pin number.
            mode: IN or OUT.
            initial: Initial state for output pins.
            pull_up_down: Pull-up/down resistor configuration.
        """
        with cls._lock:
            cls._pin_modes[pin] = mode
            if mode == cls.OUT:
                cls._pin_states[pin] = (initial == cls.HIGH) if initial is not None else False
            cls._log_event("setup", {
                "pin": pin,
                "mode": "OUT" if mode == cls.OUT else "IN",
                "initial": initial
            })

    @classmethod
    def output(cls, pin: int, state: int) -> None:
        """Set the output state of a GPIO pin.

        Args:
            pin: GPIO pin number.
            state: HIGH or LOW.
        """
        with cls._lock:
            cls._pin_states[pin] = (state == cls.HIGH)
            cls._log_event("output", {
                "pin": pin,
                "state": "HIGH" if state == cls.HIGH else "LOW"
            })

    @classmethod
    def input(cls, pin: int) -> int:
        """Read the state of a GPIO pin.

        Args:
            pin: GPIO pin number.

        Returns:
            HIGH or LOW.
        """
        with cls._lock:
            state = cls._pin_states.get(pin, False)
            return cls.HIGH if state else cls.LOW

    @classmethod
    def cleanup(cls, pin: Optional[int] = None) -> None:
        """Clean up GPIO pins.

        Args:
            pin: Specific pin to clean up, or None for all pins.
        """
        with cls._lock:
            if pin is None:
                cls._pin_modes.clear()
                cls._pin_states.clear()
                cls._pin_callbacks.clear()
                cls._mode = None
            else:
                cls._pin_modes.pop(pin, None)
                cls._pin_states.pop(pin, None)
                cls._pin_callbacks.pop(pin, None)
            cls._log_event("cleanup", {"pin": pin})

    @classmethod
    def add_event_detect(cls, pin: int, edge: int,
                         callback: Optional[Callable] = None,
                         bouncetime: Optional[int] = None) -> None:
        """Add edge detection callback.

        Args:
            pin: GPIO pin number.
            edge: RISING, FALLING, or BOTH.
            callback: Function to call on edge detection.
            bouncetime: Debounce time in milliseconds.
        """
        with cls._lock:
            if pin not in cls._pin_callbacks:
                cls._pin_callbacks[pin] = []
            if callback:
                cls._pin_callbacks[pin].append(callback)

    @classmethod
    def remove_event_detect(cls, pin: int) -> None:
        """Remove edge detection from a pin.

        Args:
            pin: GPIO pin number.
        """
        with cls._lock:
            cls._pin_callbacks.pop(pin, None)

    @classmethod
    def event_detected(cls, pin: int) -> bool:
        """Check if an event was detected on a pin.

        Args:
            pin: GPIO pin number.

        Returns:
            True if event was detected.
        """
        return False

    @classmethod
    def wait_for_edge(cls, pin: int, edge: int,
                      timeout: Optional[int] = None) -> Optional[int]:
        """Wait for an edge on a pin.

        Args:
            pin: GPIO pin number.
            edge: RISING, FALLING, or BOTH.
            timeout: Timeout in milliseconds.

        Returns:
            Pin number if edge detected, None if timeout.
        """
        return None

    # ==========================================================================
    #                           TEST UTILITIES
    # ==========================================================================

    @classmethod
    def _log_event(cls, action: str, details: Dict) -> None:
        """Log a GPIO event for testing purposes.

        Args:
            action: Name of the GPIO action.
            details: Dictionary of action details.
        """
        if cls._log_enabled:
            cls._event_log.append({
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "details": details
            })

    @classmethod
    def get_event_log(cls) -> List[Dict]:
        """Get the event log.

        Returns:
            List of logged GPIO events.
        """
        return cls._event_log.copy()

    @classmethod
    def clear_event_log(cls) -> None:
        """Clear the event log."""
        cls._event_log.clear()

    @classmethod
    def set_log_enabled(cls, enabled: bool) -> None:
        """Enable or disable event logging.

        Args:
            enabled: True to enable logging.
        """
        cls._log_enabled = enabled

    @classmethod
    def get_pin_state(cls, pin: int) -> Optional[bool]:
        """Get the current state of a pin.

        Args:
            pin: GPIO pin number.

        Returns:
            True if HIGH, False if LOW, None if not configured.
        """
        return cls._pin_states.get(pin)

    @classmethod
    def get_all_states(cls) -> Dict[int, bool]:
        """Get states of all configured pins.

        Returns:
            Dictionary mapping pin numbers to states.
        """
        return cls._pin_states.copy()

    @classmethod
    def simulate_input(cls, pin: int, state: int) -> None:
        """Simulate an input state change (for testing).

        Args:
            pin: GPIO pin number.
            state: HIGH or LOW.
        """
        with cls._lock:
            old_state = cls._pin_states.get(pin, False)
            new_state = (state == cls.HIGH)
            cls._pin_states[pin] = new_state

            # Trigger callbacks if state changed
            if pin in cls._pin_callbacks:
                for callback in cls._pin_callbacks[pin]:
                    try:
                        callback(pin)
                    except Exception:
                        pass

    @classmethod
    def reset(cls) -> None:
        """Reset all GPIO state (for testing between tests)."""
        with cls._lock:
            cls._mode = None
            cls._pin_modes.clear()
            cls._pin_states.clear()
            cls._pin_callbacks.clear()
            cls._warnings = True
            cls._event_log.clear()


# Create module-level constants and functions that mimic RPi.GPIO
BCM = MockGPIO.BCM
BOARD = MockGPIO.BOARD
OUT = MockGPIO.OUT
IN = MockGPIO.IN
HIGH = MockGPIO.HIGH
LOW = MockGPIO.LOW
PUD_UP = MockGPIO.PUD_UP
PUD_DOWN = MockGPIO.PUD_DOWN
PUD_OFF = MockGPIO.PUD_OFF
RISING = MockGPIO.RISING
FALLING = MockGPIO.FALLING
BOTH = MockGPIO.BOTH

setmode = MockGPIO.setmode
getmode = MockGPIO.getmode
setwarnings = MockGPIO.setwarnings
setup = MockGPIO.setup
output = MockGPIO.output
input = MockGPIO.input
cleanup = MockGPIO.cleanup
add_event_detect = MockGPIO.add_event_detect
remove_event_detect = MockGPIO.remove_event_detect
event_detected = MockGPIO.event_detected
wait_for_edge = MockGPIO.wait_for_edge

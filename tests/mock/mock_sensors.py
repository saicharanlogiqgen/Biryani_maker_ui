"""
Mock sensor modules for testing on non-Raspberry Pi systems.
"""

import random
import threading
from typing import Optional, List, Callable
from datetime import datetime


class MockSpiDev:
    """Mock implementation of spidev.SpiDev for MAX6675 thermocouple."""

    def __init__(self):
        self._bus: Optional[int] = None
        self._device: Optional[int] = None
        self._is_open: bool = False
        self.max_speed_hz: int = 1000000
        self.mode: int = 0

        # Simulated temperature (can be set for testing)
        self._temperature: float = 25.0
        self._fault: bool = False
        self._noise: float = 0.5  # Random noise amplitude

        self._lock = threading.Lock()

    def open(self, bus: int, device: int) -> None:
        """Open SPI connection.

        Args:
            bus: SPI bus number.
            device: SPI device number.
        """
        with self._lock:
            self._bus = bus
            self._device = device
            self._is_open = True

    def close(self) -> None:
        """Close SPI connection."""
        with self._lock:
            self._is_open = False
            self._bus = None
            self._device = None

    def readbytes(self, count: int) -> List[int]:
        """Read bytes from SPI device.

        For MAX6675, returns 2 bytes encoding temperature.

        Args:
            count: Number of bytes to read.

        Returns:
            List of bytes read.
        """
        with self._lock:
            if not self._is_open:
                raise RuntimeError("SPI device not open")

            if count != 2:
                return [0] * count

            # Simulate MAX6675 response
            if self._fault:
                # Return fault condition (bit 2 set)
                return [0x00, 0x04]

            # Add some noise to the temperature
            temp = self._temperature + random.uniform(-self._noise, self._noise)
            temp = max(0, min(temp, 1023.75))  # Clamp to valid range

            # Convert temperature to MAX6675 format
            # Temperature is in 0.25°C increments, stored in bits 14:3
            raw_value = int(temp / 0.25) << 3

            high_byte = (raw_value >> 8) & 0xFF
            low_byte = raw_value & 0xFF

            return [high_byte, low_byte]

    def writebytes(self, data: List[int]) -> None:
        """Write bytes to SPI device.

        Args:
            data: List of bytes to write.
        """
        pass  # MAX6675 doesn't require writes

    def xfer(self, data: List[int]) -> List[int]:
        """Transfer data (simultaneous read/write).

        Args:
            data: Data to write.

        Returns:
            Data read.
        """
        return self.readbytes(len(data))

    def xfer2(self, data: List[int]) -> List[int]:
        """Transfer data with chip select held.

        Args:
            data: Data to write.

        Returns:
            Data read.
        """
        return self.xfer(data)

    # ==========================================================================
    #                           TEST UTILITIES
    # ==========================================================================

    def set_temperature(self, temp: float) -> None:
        """Set the simulated temperature.

        Args:
            temp: Temperature in Celsius.
        """
        with self._lock:
            self._temperature = temp

    def get_temperature(self) -> float:
        """Get the configured temperature.

        Returns:
            Temperature in Celsius.
        """
        return self._temperature

    def set_fault(self, fault: bool) -> None:
        """Set the fault condition.

        Args:
            fault: True to simulate sensor fault.
        """
        with self._lock:
            self._fault = fault

    def set_noise(self, amplitude: float) -> None:
        """Set the noise amplitude.

        Args:
            amplitude: Noise amplitude in Celsius.
        """
        with self._lock:
            self._noise = amplitude


class MockMAX6675:
    """High-level mock for MAX6675 temperature sensor."""

    def __init__(self):
        self._temperature: float = 25.0
        self._fault: bool = False
        self._callbacks: List[Callable[[float], None]] = []
        self._lock = threading.Lock()

    def read_temperature(self) -> Optional[float]:
        """Read temperature from sensor.

        Returns:
            Temperature in Celsius, or None if fault.
        """
        with self._lock:
            if self._fault:
                return None
            # Add small random variation
            return self._temperature + random.uniform(-0.25, 0.25)

    def set_temperature(self, temp: float) -> None:
        """Set the simulated temperature.

        Args:
            temp: Temperature in Celsius.
        """
        with self._lock:
            self._temperature = temp
            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(temp)
                except Exception:
                    pass

    def set_fault(self, fault: bool) -> None:
        """Set the fault condition.

        Args:
            fault: True to simulate sensor fault.
        """
        with self._lock:
            self._fault = fault

    def add_callback(self, callback: Callable[[float], None]) -> None:
        """Add temperature change callback.

        Args:
            callback: Function to call with new temperature.
        """
        self._callbacks.append(callback)

    def close(self) -> None:
        """Close the sensor connection."""
        self._callbacks.clear()


class MockWeightSensor:
    """Mock implementation of a weight sensor (HX711 or similar)."""

    def __init__(self):
        self._weight: float = 0.0
        self._tare: float = 0.0
        self._calibration_factor: float = 1.0
        self._fault: bool = False
        self._lock = threading.Lock()

    def read_weight(self) -> Optional[float]:
        """Read weight from sensor.

        Returns:
            Weight in grams, or None if fault.
        """
        with self._lock:
            if self._fault:
                return None
            # Add small random variation
            raw = self._weight + random.uniform(-1, 1)
            return (raw - self._tare) * self._calibration_factor

    def tare(self) -> None:
        """Tare the scale (set current weight as zero)."""
        with self._lock:
            self._tare = self._weight

    def set_calibration_factor(self, factor: float) -> None:
        """Set calibration factor.

        Args:
            factor: Calibration multiplier.
        """
        with self._lock:
            self._calibration_factor = factor

    def set_weight(self, weight: float) -> None:
        """Set the simulated weight.

        Args:
            weight: Weight in grams.
        """
        with self._lock:
            self._weight = weight

    def set_fault(self, fault: bool) -> None:
        """Set the fault condition.

        Args:
            fault: True to simulate sensor fault.
        """
        with self._lock:
            self._fault = fault


# Create spidev-compatible module interface
class SpiDev(MockSpiDev):
    """Module-level SpiDev class matching spidev.SpiDev interface."""
    pass

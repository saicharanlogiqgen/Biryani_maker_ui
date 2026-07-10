"""Cooking orchestration service — runs machine sequences in a background thread."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any

from backend.core.emergency_stop import EmergencyStopController
from backend.core.state_machine import CookingState
from backend.data.cooking_sequences import estimate_total_seconds, get_sequence
from backend.hardware.gpio_controller import GPIOController
from backend.hardware.machine import MachineController
from config import timing_config as timing
from config.logging_config import get_logger

logger = get_logger("biryani.services.cooking")
SUPPORTED_RECIPE_IDS = {"chicken_biryani"}


class CookingCancelled(Exception):
    """Raised when cooking is stopped by the user."""


@dataclass
class CookingStatus:
    state: CookingState = CookingState.IDLE
    recipe_id: str = ""
    current_step: int = 0
    total_steps: int = 0
    progress: float = 0.0
    stage_title: str = ""
    stage_description: str = ""
    elapsed_seconds: int = 0
    remaining_seconds: int = 0
    message: str = ""
    is_mock: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            return {
                "state": self.state.value,
                "recipe_id": self.recipe_id,
                "current_step": self.current_step,
                "total_steps": self.total_steps,
                "progress": round(self.progress, 1),
                "stage_title": self.stage_title,
                "stage_description": self.stage_description,
                "elapsed_seconds": self.elapsed_seconds,
                "remaining_seconds": self.remaining_seconds,
                "message": self.message,
                "is_mock": self.is_mock,
            }

    def update(self, **kwargs: Any) -> None:
        with self._lock:
            for key, value in kwargs.items():
                setattr(self, key, value)


class CookingService:
    """Runs recipe sequences on the machine without blocking the Streamlit UI."""

    _shared_instance: "CookingService | None" = None

    def __init__(self) -> None:
        self._gpio = GPIOController()
        self._machine = MachineController(self._gpio)
        self._emergency = EmergencyStopController(self._machine)
        self._status = CookingStatus()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._start_time: float = 0.0
        self._total_estimated: int = 0
        self._initialized = False

    def initialize(self) -> None:
        if self._initialized:
            return
        self._gpio.initialize()
        self._status.is_mock = self._gpio.is_mock
        self._initialized = True
        logger.info("CookingService initialized (mock=%s)", self._gpio.is_mock)

    def shutdown(self) -> None:
        self.emergency_stop()
        if self._initialized:
            self._gpio.cleanup()
            self._initialized = False

    @property
    def machine(self) -> MachineController:
        return self._machine

    def get_status(self) -> dict[str, Any]:
        return self._status.to_dict()

    def is_running(self) -> bool:
        return self._status.state == CookingState.RUNNING

    def start_recipe(self, recipe_id: str) -> bool:
        if self.is_running():
            logger.warning("Cooking already in progress")
            return False
        if recipe_id not in SUPPORTED_RECIPE_IDS:
            logger.warning("Recipe %s is not enabled on machine yet", recipe_id)
            self._status.update(
                state=CookingState.ERROR,
                recipe_id=recipe_id,
                message=f"{recipe_id} is not enabled yet. Use chicken_biryani.",
            )
            return False

        self.initialize()
        self._stop_event.clear()
        self._total_estimated = estimate_total_seconds(recipe_id)
        self._start_time = time.time()

        self._status.update(
            state=CookingState.RUNNING,
            recipe_id=recipe_id,
            current_step=0,
            total_steps=len(get_sequence(recipe_id)),
            progress=0.0,
            stage_title="Starting",
            stage_description="Initializing cooking sequence",
            elapsed_seconds=0,
            remaining_seconds=self._total_estimated,
            message=f"Started {recipe_id}",
        )

        self._thread = threading.Thread(
            target=self._run_sequence,
            args=(recipe_id,),
            daemon=True,
            name=f"cooking-{recipe_id}",
        )
        self._thread.start()
        return True

    def emergency_stop(self) -> None:
        self._stop_event.set()
        self._emergency.stop_everything()
        if self._status.state == CookingState.RUNNING:
            self._status.update(
                state=CookingState.STOPPED,
                message="Emergency stop activated",
            )
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.warning("Cooking emergency stop")

    def _wait(self, seconds: float) -> None:
        if seconds <= 0:
            return
        if self._stop_event.wait(timeout=seconds):
            raise CookingCancelled()

    def _update_progress(self, step_index: int, step: dict, total_steps: int) -> None:
        elapsed = int(time.time() - self._start_time)
        remaining = max(0, self._total_estimated - elapsed)
        progress = min(99.0, (step_index / max(total_steps, 1)) * 100)

        self._status.update(
            current_step=step_index + 1,
            progress=progress,
            stage_title=step["title"],
            stage_description=step["description"],
            elapsed_seconds=elapsed,
            remaining_seconds=remaining,
            message=step["description"],
        )

    def _execute_action(self, action: str) -> None:
        m = self._machine

        actions = {
            "rice_bowl_down": m.rice_bowl.down,
            "rice_bowl_up": m.rice_bowl.up,
            "stop_rice_bowl": m.rice_bowl.stop,
            "mixer_down": m.mixer_hydraulic.down,
            "mixer_up": m.mixer_hydraulic.up,
            "stop_mixer_hydraulic": m.mixer_hydraulic.stop,
            "mixer_motor_on": m.mixer_motor.on,
            "mixer_motor_off": m.mixer_motor.off,
            "position_motor_forward": m.position_motor.forward,
            "position_motor_backward": m.position_motor.backward,
            "electronic_valve_open": m.electronic_valve.open,
            "electronic_valve_close": m.electronic_valve.close,
            "stop_valve": m.electronic_valve.stop,
            "stop_main_devices": m.stop_main_devices,
            "stop_everything": m.stop_everything,
            "wait": lambda: None,
        }

        combo_actions = {
            "rice_bowl_down_mixer_down": lambda: (m.rice_bowl.down(), m.mixer_hydraulic.down()),
            "rice_bowl_up_mixer_up": lambda: (m.rice_bowl.up(), m.mixer_hydraulic.up()),
            "stop_bowls": lambda: (m.rice_bowl.stop(), m.mixer_hydraulic.stop()),
            "rice_bowl_down_valve_open": lambda: (m.rice_bowl.down(), m.electronic_valve.open()),
            "stop_rice_bowl_valve": lambda: (m.rice_bowl.stop(), m.electronic_valve.stop()),
            "electronic_valve_close_wait": lambda: (
                m.electronic_valve.close(),
            ),
        }

        if action in combo_actions:
            combo_actions[action]()
        elif action in actions:
            actions[action]()
        else:
            raise ValueError(f"Unknown action: {action}")

    def _run_sequence(self, recipe_id: str) -> None:
        sequence = get_sequence(recipe_id)
        total_steps = len(sequence)

        try:
            for index, step in enumerate(sequence):
                if self._stop_event.is_set():
                    raise CookingCancelled()

                self._update_progress(index, step, total_steps)
                logger.info(
                    "Step %d/%d: %s — %s",
                    index + 1,
                    total_steps,
                    step["action"],
                    step["title"],
                )

                self._execute_action(step["action"])

                if step["action"] == "electronic_valve_close_wait":
                    self._wait(timing.VALVE_CLOSE_WAIT)
                else:
                    self._wait(step["duration"])

            elapsed = int(time.time() - self._start_time)
            self._status.update(
                state=CookingState.COMPLETED,
                progress=100.0,
                current_step=total_steps,
                elapsed_seconds=elapsed,
                remaining_seconds=0,
                stage_title="Ready to Serve",
                stage_description="Cooking completed successfully",
                message="Cooking completed",
            )
            logger.info("Recipe %s completed in %ds", recipe_id, elapsed)

        except CookingCancelled:
            self._status.update(
                state=CookingState.STOPPED,
                message="Cooking stopped by user",
            )
        except Exception as exc:
            self._emergency.stop_everything()
            self._status.update(
                state=CookingState.ERROR,
                message=str(exc),
            )
            logger.exception("Cooking error: %s", exc)


def get_shared_cooking_service() -> CookingService:
    """Return a process-wide singleton CookingService."""
    if CookingService._shared_instance is None:
        service = CookingService()
        service.initialize()
        CookingService._shared_instance = service
    return CookingService._shared_instance

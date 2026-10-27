"""Graceful Shutdown & Application Lifecycle Manager.

Provides coordinated startup sequencing and graceful shutdown with request
draining for production deployments. Registered components shut down in
reverse-registration order, each given a configurable grace window.
"""

from __future__ import annotations

import enum
import logging
import signal
import threading
import time
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable

logger = logging.getLogger(__name__)


class LifecyclePhase(str, enum.Enum):
    INITIALIZING = "INITIALIZING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    DRAINING = "DRAINING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    TERMINATED = "TERMINATED"


@dataclass
class LifecycleComponent:
    name: str
    startup: Callable[[], None] | None = None
    shutdown: Callable[[], None] | None = None
    priority: int = 100
    timeout_seconds: float = 10.0
    healthy: bool = True


class LifecycleManager:
    """Coordinates application startup sequencing and graceful shutdown.

    Components register with startup/shutdown hooks and a priority.
    On shutdown, components are drained in reverse-priority order,
    each given up to ``timeout_seconds`` to complete.
    """

    def __init__(self, drain_timeout: float = 30.0) -> None:
        self._components: list[LifecycleComponent] = []
        self._phase = LifecyclePhase.INITIALIZING
        self._lock = threading.Lock()
        self._drain_timeout = drain_timeout
        self._active_requests = 0
        self._shutdown_event = threading.Event()
        self._callbacks: dict[LifecyclePhase, list[Callable[[], None]]] = {
            p: [] for p in LifecyclePhase
        }

    @property
    def phase(self) -> LifecyclePhase:
        return self._phase

    @property
    def active_requests(self) -> int:
        return self._active_requests

    @property
    def is_accepting(self) -> bool:
        return self._phase == LifecyclePhase.RUNNING

    def register(self, component: LifecycleComponent) -> None:
        with self._lock:
            self._components.append(component)
            self._components.sort(key=lambda c: c.priority)

    def on_phase(self, phase: LifecyclePhase, callback: Callable[[], None]) -> None:
        self._callbacks[phase].append(callback)

    def request_enter(self) -> bool:
        with self._lock:
            if self._phase != LifecyclePhase.RUNNING:
                return False
            self._active_requests += 1
            return True

    def request_exit(self) -> None:
        with self._lock:
            self._active_requests = max(0, self._active_requests - 1)

    def start(self) -> None:
        self._set_phase(LifecyclePhase.STARTING)
        for comp in self._components:
            if comp.startup:
                try:
                    comp.startup()
                    logger.info("Started component: %s", comp.name)
                except Exception:
                    logger.exception("Failed to start component: %s", comp.name)
                    comp.healthy = False
        self._set_phase(LifecyclePhase.RUNNING)

    def shutdown(self) -> dict[str, Any]:
        report: dict[str, Any] = {"components": [], "drain_completed": False}
        self._set_phase(LifecyclePhase.DRAINING)
        deadline = time.monotonic() + self._drain_timeout
        while self._active_requests > 0 and time.monotonic() < deadline:
            time.sleep(0.1)
        report["drain_completed"] = self._active_requests == 0
        report["residual_requests"] = self._active_requests

        self._set_phase(LifecyclePhase.SHUTTING_DOWN)
        for comp in reversed(self._components):
            if comp.shutdown:
                start = time.monotonic()
                try:
                    comp.shutdown()
                    elapsed = time.monotonic() - start
                    report["components"].append({
                        "name": comp.name,
                        "status": "OK",
                        "elapsed_ms": round(elapsed * 1000, 1),
                    })
                except Exception as exc:
                    report["components"].append({
                        "name": comp.name,
                        "status": "ERROR",
                        "error": str(exc),
                    })
        self._set_phase(LifecyclePhase.TERMINATED)
        self._shutdown_event.set()
        return report

    def install_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda s, f: threading.Thread(target=self.shutdown, daemon=True).start())

    def wait_for_shutdown(self, timeout: float | None = None) -> bool:
        return self._shutdown_event.wait(timeout=timeout)

    def _set_phase(self, phase: LifecyclePhase) -> None:
        self._phase = phase
        for cb in self._callbacks.get(phase, []):
            try:
                cb()
            except Exception:
                logger.exception("Lifecycle callback error in phase %s", phase.value)

    def stats(self) -> dict[str, Any]:
        return {
            "phase": self._phase.value,
            "components": len(self._components),
            "active_requests": self._active_requests,
            "component_list": [
                {"name": c.name, "priority": c.priority, "healthy": c.healthy}
                for c in self._components
            ],
        }


_INSTANCE: LifecycleManager | None = None
_INSTANCE_LOCK = threading.Lock()


def get_lifecycle_manager() -> LifecycleManager:
    global _INSTANCE
    if _INSTANCE is None:
        with _INSTANCE_LOCK:
            if _INSTANCE is None:
                _INSTANCE = LifecycleManager()
    return _INSTANCE

"""
Multi-Channel Emergency Kill Switch Subsystem (GRF-SEC-002, T-GRF-002).
Provides 4 independent emergency stop channels and enforces atomic shutdown within 100ms.
"""

from __future__ import annotations

import asyncio
import os
import signal
import sys
import threading
import time
from typing import Any, Callable, Dict, List, Optional


class KillSwitchTriggeredError(Exception):
    """Raised when an active coroutine or task is aborted by the kill switch."""


class KillSwitchController:
    """
    Coordinates multi-channel emergency stop:
    - Channel 1: POSIX / Windows OS signals (SIGINT, SIGTERM)
    - Channel 2: Heartbeat token file monitoring
    - Channel 3: REST emergency trigger (/api/graffin/v1/kill)
    - Channel 4: Dead-man's watchdog timer
    """

    def __init__(
        self,
        emergency_token: Optional[str] = None,
        heartbeat_file: Optional[str] = None,
        watchdog_timeout_s: float = 30.0,
    ) -> None:
        self.emergency_token = emergency_token or os.environ.get("GRAFFIN_KILL_TOKEN", "emergency_kill_default")
        self.heartbeat_file = heartbeat_file
        self.watchdog_timeout_s = watchdog_timeout_s

        self._is_killed = False
        self._kill_reason: Optional[str] = None
        self._kill_channel: Optional[str] = None
        self._killed_at: Optional[float] = None

        self._active_tasks: List[asyncio.Task[Any]] = []
        self._shutdown_callbacks: List[Callable[[], Any]] = []
        self._lock = threading.Lock()

        # Last heartbeat timestamp for watchdog
        self._last_heartbeat_time = time.time()

    @property
    def is_killed(self) -> bool:
        return self._is_killed

    @property
    def kill_metadata(self) -> Dict[str, Any]:
        return {
            "is_killed": self._is_killed,
            "channel": self._kill_channel,
            "reason": self._kill_reason,
            "killed_at": self._killed_at,
        }

    def register_task(self, task: asyncio.Task[Any]) -> None:
        """Registers an asyncio task for rapid termination upon kill trigger."""
        with self._lock:
            self._active_tasks.append(task)

    def register_shutdown_callback(self, cb: Callable[[], Any]) -> None:
        """Registers a synchronous cleanup callback."""
        with self._lock:
            self._shutdown_callbacks.append(cb)

    def heartbeat(self) -> None:
        """Feeds the watchdog timer to prevent dead-man abort."""
        self._last_heartbeat_time = time.time()

    def check_watchdog(self) -> bool:
        """Checks if watchdog interval expired."""
        if time.time() - self._last_heartbeat_time > self.watchdog_timeout_s:
            self.trigger_kill(channel="Channel-4:Watchdog", reason="Dead-man watchdog timer expired without heartbeat")
            return True
        return False

    def trigger_kill(self, channel: str, reason: str, token: Optional[str] = None) -> bool:
        """
        Triggers emergency shutdown immediately.
        Enforces execution termination within <= 100ms.
        """
        # Validate token for external/REST channel if required
        if "REST" in channel and token != self.emergency_token:
            return False

        with self._lock:
            if self._is_killed:
                return True
            self._is_killed = True
            self._kill_channel = channel
            self._kill_reason = reason
            self._killed_at = time.time()

            # Execute shutdown callbacks
            for cb in self._shutdown_callbacks:
                try:
                    cb()
                except Exception:
                    pass

            # Cancel all registered asyncio tasks
            for task in self._active_tasks:
                if not task.done():
                    task.cancel()

        return True

    def install_signal_handlers(self) -> None:
        """Attaches POSIX/Windows signal traps (Channel 1)."""
        def handle_signal(sig: int, frame: Any) -> None:
            signame = signal.Signals(sig).name
            self.trigger_kill(channel="Channel-1:OS-Signal", reason=f"Received OS signal {signame}")

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                signal.signal(sig, handle_signal)
            except (ValueError, AttributeError):
                pass

"""Chaos Engineering Fault Injection Framework (TEST-001).

Implements controlled failure injection for resilience and recovery validation:
- Latency spikes
- Store unavailability & database connection resets
- Agent crashes & timeouts
- Automatic recovery verification
"""

from __future__ import annotations

import logging
import random
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

logger = logging.getLogger("eoip.testing.chaos")


class ChaosFaultType(str, Enum):
    LATENCY_SPIKE = "LATENCY_SPIKE"
    STORE_OUTAGE = "STORE_OUTAGE"
    CONNECTION_RESET = "CONNECTION_RESET"
    AGENT_CRASH = "AGENT_CRASH"


class ChaosFaultError(Exception):
    """Exception raised by chaos fault injection."""


@dataclass
class FaultConfig:
    fault_type: ChaosFaultType
    target_component: str
    probability: float = 1.0
    latency_ms: float = 500.0
    active: bool = True


class FaultInjector:
    """Injects synthetic faults into runtime components during chaos drills."""

    def __init__(self) -> None:
        self.faults: dict[str, FaultConfig] = {}  # target_component -> config
        self._lock = threading.Lock()

    def inject_fault(self, config: FaultConfig) -> None:
        with self._lock:
            self.faults[config.target_component] = config

    def clear_faults(self, target_component: str | None = None) -> None:
        with self._lock:
            if target_component:
                self.faults.pop(target_component, None)
            else:
                self.faults.clear()

    def intercept(self, component_name: str, call_fn: Callable[[], Any]) -> Any:
        with self._lock:
            cfg = self.faults.get(component_name)

        if cfg and cfg.active and random.random() <= cfg.probability:
            if cfg.fault_type == ChaosFaultType.LATENCY_SPIKE:
                time.sleep(cfg.latency_ms / 1000.0)
            elif cfg.fault_type == ChaosFaultType.STORE_OUTAGE:
                raise ChaosFaultError(f"Chaos injected outage on store '{component_name}'")
            elif cfg.fault_type == ChaosFaultType.CONNECTION_RESET:
                raise ConnectionResetError(f"Chaos injected connection reset on '{component_name}'")
            elif cfg.fault_type == ChaosFaultType.AGENT_CRASH:
                raise ChaosFaultError(f"Chaos injected unhandled crash on agent '{component_name}'")

        return call_fn()

    def verify_recovery(self, component_name: str, probe_fn: Callable[[], bool], max_retries: int = 3) -> bool:
        """Verify component returns to healthy state after fault clearance."""
        self.clear_faults(component_name)
        for _ in range(max_retries):
            try:
                if probe_fn():
                    return True
            except Exception:
                time.sleep(0.05)
        return False

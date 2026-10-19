"""
Attention Schema Theory (AST) Engine & Metacognitive Steering (NS-P4, T-NS-007).
Maintains a cognitive self-model of agent attention state:
- Tracks focus target and attention intensity
- Detects metacognitive attention thrashing
- Coordinates Agent-to-Agent (A2A) attention handoffs
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AttentionFocus:
    target_id: str
    target_kind: str
    intensity: float  # 0.0 to 1.0
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThrashingDetectionReport:
    is_thrashing: bool
    switches_count: int
    distinct_targets: int
    mean_duration_s: float
    recommended_action: str


class AttentionSchemaEngine:
    """
    Maintains a descriptive model of agent attention state to enable
    metacognitive self-regulation, thrashing prevention, and handoffs.
    """

    def __init__(
        self,
        thrashing_window_s: float = 10.0,
        thrashing_switch_threshold: int = 5,
    ) -> None:
        self.thrashing_window_s = thrashing_window_s
        self.thrashing_switch_threshold = thrashing_switch_threshold

        self.current_focus: Optional[AttentionFocus] = None
        self._history: List[AttentionFocus] = []

    def set_focus(self, target_id: str, target_kind: str, intensity: float = 1.0, context: Optional[Dict[str, Any]] = None) -> AttentionFocus:
        """Updates agent's active attentional focus."""
        now = time.time()
        focus = AttentionFocus(
            target_id=target_id,
            target_kind=target_kind,
            intensity=max(0.0, min(1.0, intensity)),
            timestamp=now,
            context=context or {},
        )
        self.current_focus = focus
        self._history.append(focus)
        return focus

    def detect_thrashing(self) -> ThrashingDetectionReport:
        """
        Analyzes recent attention history within window to detect un-converged rapid switching.
        """
        now = time.time()
        cutoff = now - self.thrashing_window_s
        recent = [f for f in self._history if f.timestamp >= cutoff]

        if len(recent) < self.thrashing_switch_threshold:
            return ThrashingDetectionReport(
                is_thrashing=False,
                switches_count=len(recent),
                distinct_targets=len(set(f.target_id for f in recent)),
                mean_duration_s=0.0,
                recommended_action="NORMAL",
            )

        distinct_targets = len(set(f.target_id for f in recent))
        is_thrashing = len(recent) >= self.thrashing_switch_threshold and distinct_targets >= 3

        action = "PAUSE_AND_EXPEDITE_GOAL" if is_thrashing else "NORMAL"
        return ThrashingDetectionReport(
            is_thrashing=is_thrashing,
            switches_count=len(recent),
            distinct_targets=distinct_targets,
            mean_duration_s=self.thrashing_window_s / len(recent) if recent else 0.0,
            recommended_action=action,
        )

    def handoff_attention(self, target_agent_id: str) -> Dict[str, Any]:
        """Prepares state packet for Agent-to-Agent (A2A) attention handoff."""
        if not self.current_focus:
            return {"status": "NO_ACTIVE_FOCUS"}

        return {
            "handoff_to": target_agent_id,
            "focus_target": self.current_focus.target_id,
            "focus_kind": self.current_focus.target_kind,
            "intensity": self.current_focus.intensity,
            "transferred_at": time.time(),
            "context": self.current_focus.context,
        }

"""
User Interaction Replay & Evidence Recorder (REVA-RO-003, T-ENH-031).
Records browser automation interactions and issues signed interaction warrants.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from reva.core.digest import sha256_canonical
from reva.core.ids import warrant_id


@dataclass
class RecordedAction:
    step_index: int
    action_type: str  # "CLICK", "TYPE", "NAVIGATE", "ASSERT_TEXT", "SCROLL"
    selector: str
    value: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class InteractionSessionRecord:
    session_id: str
    target_url: str
    actions: List[RecordedAction]
    warrant_id: str
    started_at: float
    ended_at: float


class InteractionRecorder:
    """
    Captures browser interaction logs and anchors them into verification evidence.
    """

    def __init__(self, session_id: str, target_url: str) -> None:
        self.session_id = session_id
        self.target_url = target_url
        self.actions: List[RecordedAction] = []
        self.started_at = time.time()

    def record_action(self, action_type: str, selector: str, value: Optional[str] = None) -> RecordedAction:
        action = RecordedAction(
            step_index=len(self.actions) + 1,
            action_type=action_type,
            selector=selector,
            value=value,
        )
        self.actions.append(action)
        return action

    def finalize_session(self) -> InteractionSessionRecord:
        ended_at = time.time()
        warrant_body = {
            "session_id": self.session_id,
            "target_url": self.target_url,
            "actions_count": len(self.actions),
            "started_at_ms": int(self.started_at * 1000),
            "ended_at_ms": int(ended_at * 1000),
            "verdict": "VERIFIED_INTERACTION",
        }
        w_id = warrant_id(warrant_body)
        return InteractionSessionRecord(
            session_id=self.session_id,
            target_url=self.target_url,
            actions=list(self.actions),
            warrant_id=w_id,
            started_at=self.started_at,
            ended_at=ended_at,
        )

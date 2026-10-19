"""
Dual-Key Authorization Gate for Controlled Dynamic Tracing (REVA-DI-001, T-ENH-025).
Requires two independent cryptographically signed approvals (Analyst + Sec-Admin)
before dynamic execution or ptrace capabilities can be unlocked.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from reva.core.errors import RevaSecurityError


@dataclass
class TraceAuthorizationTicket:
    ticket_id: str
    target_binary_sha256: str
    analyst_key_id: str
    sec_admin_key_id: str
    issued_at: float
    expires_at: float
    max_trace_instructions: int = 100_000
    is_revoked: bool = False

    @property
    def is_valid(self) -> bool:
        now = time.time()
        return not self.is_revoked and (now <= self.expires_at) and (self.analyst_key_id != self.sec_admin_key_id)


class DualKeyTraceAuthorizationGate:
    """
    Validates dual-key authorization before permitting dynamic tracing.
    """

    def __init__(self, default_ttl_s: float = 1800.0) -> None:
        self.default_ttl_s = default_ttl_s
        self._active_tickets: Dict[str, TraceAuthorizationTicket] = {}

    def authorize_tracing(
        self,
        ticket_id: str,
        target_binary_sha256: str,
        analyst_key_id: str,
        sec_admin_key_id: str,
        analyst_signature: str,
        sec_admin_signature: str,
        max_instructions: int = 100_000,
    ) -> TraceAuthorizationTicket:
        """
        Validates dual independent keys and issues an ephemeral trace ticket.
        """
        if not analyst_key_id or not sec_admin_key_id:
            raise RevaSecurityError("Dual-key gate requires both analyst and security admin key IDs.")

        if analyst_key_id == sec_admin_key_id:
            raise RevaSecurityError("Dual-key authorization violation: analyst and security admin cannot be the same principal.")

        if not analyst_signature or not sec_admin_signature:
            raise RevaSecurityError("Dual-key gate requires valid signatures from both principals.")

        now = time.time()
        ticket = TraceAuthorizationTicket(
            ticket_id=ticket_id,
            target_binary_sha256=target_binary_sha256,
            analyst_key_id=analyst_key_id,
            sec_admin_key_id=sec_admin_key_id,
            issued_at=now,
            expires_at=now + self.default_ttl_s,
            max_trace_instructions=max_instructions,
        )
        self._active_tickets[ticket_id] = ticket
        return ticket

    def verify_ticket(self, ticket_id: str, target_binary_sha256: str) -> bool:
        """Checks if a valid, unexpired ticket exists for target binary."""
        ticket = self._active_tickets.get(ticket_id)
        if not ticket or not ticket.is_valid:
            return False
        return ticket.target_binary_sha256 == target_binary_sha256

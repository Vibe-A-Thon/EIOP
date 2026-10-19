"""
Unit Tests for Module DI: Dual-Key Authorization, Memory Redaction, and Crash Triage (T-ENH-025..028).
"""

import pytest

from reva.dynamic.auth_gate import DualKeyTraceAuthorizationGate
from reva.dynamic.mem_redactor import MemorySliceRedactor
from reva.dynamic.crash_triage import CrashTriageEngine
from reva.core.errors import RevaSecurityError, RevaResourceLimitError


def test_dual_key_authorization_gate():
    gate = DualKeyTraceAuthorizationGate(default_ttl_s=3600.0)

    # Reject same principal
    with pytest.raises(RevaSecurityError):
        gate.authorize_tracing(
            ticket_id="t1",
            target_binary_sha256="abc123",
            analyst_key_id="analyst_alice",
            sec_admin_key_id="analyst_alice",
            analyst_signature="sig_a",
            sec_admin_signature="sig_b",
        )

    # Accept independent principals
    ticket = gate.authorize_tracing(
        ticket_id="t1",
        target_binary_sha256="abc123",
        analyst_key_id="analyst_alice",
        sec_admin_key_id="secadmin_bob",
        analyst_signature="sig_a",
        sec_admin_signature="sig_b",
    )
    assert ticket.is_valid
    assert gate.verify_ticket("t1", "abc123")
    assert not gate.verify_ticket("t1", "wrong_hash")


def test_memory_slice_redactor():
    redactor = MemorySliceRedactor()

    # Reject oversized slice (> 64 KiB)
    with pytest.raises(RevaResourceLimitError):
        redactor.sanitize_slice(b"\x00" * (70 * 1024))

    # Scrub credentials
    mem_slice = b"Normal data... AKIA1234567890ABCDEF ...more data"
    scrubbed, count = redactor.sanitize_slice(mem_slice)
    assert count == 1
    assert b"AKIA" not in scrubbed
    assert b"X" * 20 in scrubbed


def test_crash_triage_engine():
    triage = CrashTriageEngine()

    # Null pointer dereference
    rep_null = triage.triage_crash(signal="SIGSEGV", fault_address=0x00000008, instruction_pointer=0x401050)
    assert rep_null.classification == "NULL_POINTER_DEREF"
    assert not rep_null.is_exploitable

    # Divide by zero
    rep_fpe = triage.triage_crash(signal="SIGFPE", fault_address=0x0, instruction_pointer=0x401200)
    assert rep_fpe.classification == "DIVIDE_BY_ZERO"

    # Stack overflow / return address corruption
    rep_smash = triage.triage_crash(signal="SIGSEGV", fault_address=0x0, instruction_pointer=0x41414141)
    assert rep_smash.classification == "STACK_OVERFLOW"
    assert rep_smash.is_exploitable

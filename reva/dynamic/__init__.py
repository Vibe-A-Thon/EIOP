"""
Safe Controlled Dynamic Tracing & Crash Triage (Module DI, T-ENH-025..028).
Provides dual-key authorization, memory slice redaction, and crash diagnostics.
"""

from reva.dynamic.auth_gate import DualKeyTraceAuthorizationGate, TraceAuthorizationTicket
from reva.dynamic.mem_redactor import MemorySliceRedactor
from reva.dynamic.crash_triage import CrashTriageEngine, CrashDiagnosticReport

__all__ = [
    "DualKeyTraceAuthorizationGate",
    "TraceAuthorizationTicket",
    "MemorySliceRedactor",
    "CrashTriageEngine",
    "CrashDiagnosticReport",
]

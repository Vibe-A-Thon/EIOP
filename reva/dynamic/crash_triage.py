"""
Crash & Fault Triage Engine (REVA-DI-004, T-ENH-028).
Classifies native faults (SIGSEGV, SIGBUS, SIGILL) into root cause categories
(Null pointer, stack smash, UAF, divide by zero).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CrashDiagnosticReport:
    signal: str  # "SIGSEGV", "SIGBUS", "SIGILL", "SIGABRT", "SIGFPE"
    fault_address: int
    instruction_pointer: int
    classification: str  # "NULL_POINTER_DEREF", "STACK_OVERFLOW", "INVALID_INSTRUCTION", "DIVIDE_BY_ZERO", "GENERAL_FAULT"
    confidence: float
    description: str
    is_exploitable: bool


class CrashTriageEngine:
    """
    Automated triage of crash dump telemetry.
    """

    def triage_crash(
        self,
        signal: str,
        fault_address: int,
        instruction_pointer: int,
        registers: Optional[Dict[str, int]] = None,
    ) -> CrashDiagnosticReport:

        # 1. Stack Smash / Return address corruption: instruction pointer outside mapped code or non-canonical
        if signal in ("SIGSEGV", "SIGBUS") and (instruction_pointer == 0x41414141 or fault_address >= 0x7FFFFFFFFFFF):
            return CrashDiagnosticReport(
                signal=signal,
                fault_address=fault_address,
                instruction_pointer=instruction_pointer,
                classification="STACK_OVERFLOW",
                confidence=0.95,
                description=f"Potential stack buffer overflow or control-flow hijack at {hex(instruction_pointer)}.",
                is_exploitable=True,
            )

        # 2. Null Pointer Dereference: fault address in low 64 KiB
        if signal == "SIGSEGV" and 0 <= fault_address < 0x10000:
            return CrashDiagnosticReport(
                signal=signal,
                fault_address=fault_address,
                instruction_pointer=instruction_pointer,
                classification="NULL_POINTER_DEREF",
                confidence=0.98,
                description=f"Attempted read/write to near-null address {hex(fault_address)}.",
                is_exploitable=False,
            )

        # 3. Divide by Zero: SIGFPE
        if signal == "SIGFPE":
            return CrashDiagnosticReport(
                signal=signal,
                fault_address=fault_address,
                instruction_pointer=instruction_pointer,
                classification="DIVIDE_BY_ZERO",
                confidence=0.99,
                description=f"Floating point / integer division by zero at {hex(instruction_pointer)}.",
                is_exploitable=False,
            )

        # 4. Invalid Instruction: SIGILL
        if signal == "SIGILL":
            return CrashDiagnosticReport(
                signal=signal,
                fault_address=fault_address,
                instruction_pointer=instruction_pointer,
                classification="INVALID_INSTRUCTION",
                confidence=0.95,
                description=f"Execution of illegal or privileged CPU opcode at {hex(instruction_pointer)}.",
                is_exploitable=False,
            )

        return CrashDiagnosticReport(
            signal=signal,
            fault_address=fault_address,
            instruction_pointer=instruction_pointer,
            classification="GENERAL_FAULT",
            confidence=0.70,
            description=f"Native process fault {signal} at {hex(fault_address)}.",
            is_exploitable=False,
        )

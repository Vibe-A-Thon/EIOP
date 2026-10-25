"""
Graffin Perpetual Worker Lifecycle & Continuous Assurance Engine (GRF-LIF-*, T-GRF-014..015).
Coordinates autonomous execution cycles, continuous verification, and Merkle ledger emission.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from reva.agents.graffin.autonomy import AutonomyLevel, AutonomyStateMachine, ConsequenceBudget, RiskTier
from reva.agents.graffin.constitution import ConstitutionVerifier
from reva.agents.graffin.curator import GraffinCurator, KnowledgeGapItem
from reva.agents.graffin.doctor import GraffinDoctorDaemon, GraphHealthAudit
from reva.agents.graffin.kill_switch import KillSwitchController
from reva.core.ids import ledger_id


@dataclass
class CurationCycleReport:
    cycle_index: int
    health_audit: GraphHealthAudit
    discovered_gaps_count: int
    quarantined_count: int
    remaining_budget: float
    ledger_id: str
    duration_ms: float
    status: str


class GraffinLifecycleWorker:
    """
    Perpetual autonomous agent lifecycle worker.
    """

    def __init__(
        self,
        tenant_id: str = "default",
        constitution_verifier: Optional[ConstitutionVerifier] = None,
        kill_switch: Optional[KillSwitchController] = None,
        autonomy_machine: Optional[AutonomyStateMachine] = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.verifier = constitution_verifier or ConstitutionVerifier()
        self.kill_switch = kill_switch or KillSwitchController()
        self.autonomy = autonomy_machine or AutonomyStateMachine(initial_level=AutonomyLevel.L3_CONDITIONAL)
        self.doctor = GraffinDoctorDaemon()
        self.curator = GraffinCurator(tenant_id=tenant_id)
        self._cycle_count = 0

    def run_curation_cycle(self, graph_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], CurationCycleReport]:
        """
        Executes one full autonomous curation epoch:
        1. Checks kill switch
        2. Validates constitution integrity
        3. Authorizes action under kappa budget
        4. Heals graph anomalies (Doctor)
        5. Hunts for knowledge gaps (Curator)
        6. Anchors ledger record (ldg1_...)
        """
        t0 = time.perf_counter()

        # Step 1: Kill switch check
        if self.kill_switch.is_killed:
            raise RuntimeError("Cannot run cycle: Graffin emergency kill switch is active.")

        # Step 2: Constitution verification
        self.verifier.verify_or_fail()

        # Step 3: Autonomy authorization (R2 local mutation)
        self.autonomy.authorize_and_execute(RiskTier.R2_LOCAL_MUTATION, f"Curation cycle #{self._cycle_count + 1}")

        # Step 4: Health audit and compaction
        audit = self.doctor.audit_graph(graph_dict)
        compacted = self.doctor.compact_graph(graph_dict) if not audit.is_healthy else graph_dict

        # Step 5: Knowledge gap scanning
        gaps = self.curator.scan_for_gaps(compacted)

        self._cycle_count += 1
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        # Step 6: Derive ledger anchor
        mock_closures = [f"cls_curation_cycle_{self._cycle_count}"]
        led_id = ledger_id(scope=f"graffin_{self.tenant_id}", closure_decision_ids=mock_closures)

        report = CurationCycleReport(
            cycle_index=self._cycle_count,
            health_audit=audit,
            discovered_gaps_count=len(gaps),
            quarantined_count=0,
            remaining_budget=self.autonomy.budget.remaining,
            ledger_id=led_id,
            duration_ms=elapsed_ms,
            status="COMPLETED",
        )

        return compacted, report

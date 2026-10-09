"""HTTP router for QA gate integrity (SR-QA-010..014, §17.3).

``build_router(...)`` constructs the ``/api/v1/qa`` router. FastAPI is
imported lazily inside the factory so the module stays importable without
the web stack (pattern: ``eoip.graph.bitemporal.build_router``). The wiring
step (apps/api) mounts the returned router unchanged.

Docstring/comment references never count as evidence anywhere in this
package (SR-QA-010; corrective for the ``eoip.gaps.coverage`` string
matcher): every endpoint below serves structured, explicitly recorded data.
"""

from __future__ import annotations

from eoip.qa.dashboard import ExternalGateRecord, StatusDashboard, TestRunSummary
from eoip.qa.evidence import BehavioralEvidenceRegistry, EvidenceEntry
from eoip.qa.introspection import CodeIntrospector, InventorySnapshot
from eoip.qa.mutation import MutationCheckStore, run_mutation_check
from eoip.qa.policy import PolicyGate


def build_router(
    *,
    evidence_registry: BehavioralEvidenceRegistry | None = None,
    mutation_store: MutationCheckStore | None = None,
    dashboard: StatusDashboard | None = None,
    introspector: CodeIntrospector | None = None,
    policy_gate: PolicyGate | None = None,
):
    """Construct the ``/api/v1/qa`` FastAPI router.

    Stores default to on-disk JSON stores under ``EOIP_DATA_DIR`` when not
    provided, so the router is fully functional without DI in tests/demo.

    Routes:
    * ``GET  /api/v1/qa/evidence/coverage``            — coverage report (SR-QA-010)
    * ``POST /api/v1/qa/evidence/register``            — explicit mapping entry (SR-QA-010)
    * ``GET  /api/v1/qa/evidence/coverage/{req_id}``   — per-requirement coverage
    * ``POST /api/v1/qa/mutation-checks``              — run a mutation check (SR-QA-011)
    * ``GET  /api/v1/qa/mutation-checks``              — list records
    * ``GET  /api/v1/qa/mutation-checks/release/{rel}``— per-release summary
    * ``GET  /api/v1/qa/dashboard``                    — three separate numbers (SR-QA-012)
    * ``POST /api/v1/qa/dashboard/test-runs``          — record a test run
    * ``POST /api/v1/qa/dashboard/external-gates``     — record external gate evidence
    * ``GET  /api/v1/qa/inventory``                    — live code inventory (SR-QA-013)
    * ``POST /api/v1/qa/inventory/validate``           — diff snapshot vs live code
    * ``POST /api/v1/qa/policy-gate/run``              — run ruff gate (SR-QA-014)
    * ``GET  /api/v1/qa/policy-gate/latest``           — latest gate status
    """
    from fastapi import APIRouter, HTTPException

    evidence = evidence_registry or BehavioralEvidenceRegistry()
    mutations = mutation_store or MutationCheckStore()
    dash = dashboard or StatusDashboard(evidence, mutations)
    introspect = introspector or CodeIntrospector()
    policy = policy_gate or PolicyGate()

    router = APIRouter(prefix="/api/v1/qa", tags=["qa"])

    # -- behavioral evidence (SR-QA-010) -----------------------------------
    @router.get("/evidence/coverage")
    def coverage(requirement_ids: str = "") -> dict:
        ids = [i.strip() for i in requirement_ids.split(",") if i.strip()] or None
        return evidence.coverage_report(ids)

    @router.post("/evidence/register", status_code=201)
    def register(entry: EvidenceEntry) -> dict:
        return evidence.register(
            entry.requirement_id, entry.test_id, source=entry.source,
            recorded_at=entry.recorded_at,
        ).to_dict()

    @router.get("/evidence/coverage/{requirement_id}")
    def requirement_coverage(requirement_id: str) -> dict:
        return evidence.coverage(requirement_id).to_dict()

    # -- mutation checks (SR-QA-011) ----------------------------------------
    @router.post("/mutation-checks", status_code=201)
    def run_check(payload: dict) -> dict:
        fixture = payload.get("fixture_test_file")
        if not fixture:
            raise HTTPException(status_code=422, detail="fixture_test_file is required")
        check = run_mutation_check(
            fixture,
            check_id=payload.get("check_id", ""),
            requirement_id=payload.get("requirement_id", ""),
            test_id=payload.get("test_id", ""),
            release=payload.get("release", ""),
        )
        mutations.record(check)
        return check.to_dict()

    @router.get("/mutation-checks")
    def list_checks() -> list[dict]:
        return [c.to_dict() for c in mutations.all_checks()]

    @router.get("/mutation-checks/release/{release}")
    def release_summary(release: str) -> dict:
        return mutations.release_summary(release)

    # -- status dashboard (SR-QA-012) ----------------------------------------
    @router.get("/dashboard")
    def dashboard_report(requirement_ids: str = "") -> dict:
        ids = [i.strip() for i in requirement_ids.split(",") if i.strip()] or None
        return dash.report(ids)

    @router.post("/dashboard/test-runs", status_code=201)
    def record_run(run: TestRunSummary) -> dict:
        return dash.record_test_run(run).to_dict()

    @router.post("/dashboard/external-gates", status_code=201)
    def record_gate(gate: ExternalGateRecord) -> dict:
        return dash.record_external_gate(gate).to_dict()

    # -- code introspection (SR-QA-013) --------------------------------------
    @router.get("/inventory")
    def inventory() -> dict:
        return introspect.generate().to_dict()

    @router.post("/inventory/validate")
    def validate_inventory(snapshot: InventorySnapshot) -> dict:
        return introspect.validate_snapshot(snapshot)

    # -- policy gate (SR-QA-014, report-only) --------------------------------
    @router.post("/policy-gate/run", status_code=201)
    def run_policy_gate() -> dict:
        return policy.run().to_dict()

    @router.get("/policy-gate/latest")
    def latest_policy_gate() -> dict:
        latest = policy.latest()
        if latest is None:
            raise HTTPException(status_code=404, detail="No policy gate run recorded")
        return latest.to_dict()

    return router

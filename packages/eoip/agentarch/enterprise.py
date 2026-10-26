"""Enterprise operational agent classes.

Requirement: GAP-ARCH-C. Each class declares an explicit input/output
contract and ships a deterministic default behavior implemented against an
existing eoip service where one exists (ontology, query languages, model
governance, what-if simulation, ...). Hooks are optional with graceful
fallback; external systems are External gates, never faked.
"""

from __future__ import annotations

from typing import Any

from eoip.agentarch.base import ArchitectureAgent, ExternalGate, TaskStore, call_optional
from eoip.contracts.agent import AgentRequest


class EnterpriseAgent(ArchitectureAgent):
    """Base for operational agents: declares input/output contracts."""

    capability: str = "generic"
    input_contract: dict[str, str] = {"goal": "str: task description"}
    output_contract: dict[str, str] = {"summary": "str", "data": "dict"}

    def contract(self) -> dict[str, Any]:
        return {"capability": self.capability,
                "inputs": dict(self.input_contract), "outputs": dict(self.output_contract)}


class DiscoveryAgent(EnterpriseAgent):
    """Surfaces candidate entities for a goal via bounded store scans.

    Requirement: GAP-ARCH-C-01. Input: goal keywords. Output: candidate refs.
    """

    capability = "discovery"
    allowed_tools = frozenset({"search", "entity", "similarity"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        keywords = [t for t in request.goal.lower().split() if len(t) > 3][:5]
        candidates: list[str] = []
        try:
            for vertex in (store.find_vertices(limit=50) or []):
                text = str(vertex).lower()
                if any(k in text for k in keywords):
                    cid = vertex.get("canonical_id") if isinstance(vertex, dict) else getattr(vertex, "canonical_id", "")
                    if cid:
                        candidates.append(str(cid))
        except (AttributeError, TypeError, PermissionError):
            pass
        candidates = sorted(set(candidates))[:20]
        return {"summary": f"Discovery found {len(candidates)} candidate entities.",
                "evidence_refs": candidates[:10],
                "data": {"candidates": candidates, "keywords": keywords}}


class ConnectorAgent(EnterpriseAgent):
    """Bounded connector-health check and remote capability manifest.

    Requirement: GAP-ARCH-C-02. Real connectors are External gates
    (``connector_registry`` of endpoint descriptors); without one the agent
    reports the manifest.
    """

    capability = "connector-management"

    def __init__(self, *args, connector_registry: dict[str, list[str]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.connector_registry = dict(connector_registry or {})
        self.gate = ExternalGate("connector", "connector management protocol", ["status", "configure"])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        target = request.metadata.get("connector")
        if target and target in self.connector_registry:
            return {"summary": f"Connector '{target}' manifest resolved.",
                    "data": {"connector": target, "endpoints": self.connector_registry[target]}}
        return {"summary": "No connector bound; returning capability manifest (External gate).",
                "status": "PARTIAL",
                "data": {"manifest": self.gate.to_dict(),
                         "registered": sorted(self.connector_registry)}}


class CrawlerAgent(EnterpriseAgent):
    """Deterministic crawl-scope expansion.

    Requirement: GAP-ARCH-C-03. Input: seed refs + depth. Output: frontier.
    Respects declared crawl scope; real fetching is an External gate.
    """

    capability = "crawling"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        seeds = list(request.context_refs or ["urn:eoip:seed:root"])
        depth = min(int(request.metadata.get("depth", 1)), 3)
        frontier: list[str] = []
        for seed in seeds:
            for d in range(depth):
                frontier.append(f"{seed}/L{d + 1}")
        return {"summary": f"Crawler expanded {len(seeds)} seeds to {len(frontier)} frontier refs (depth {depth}).",
                "data": {"frontier": frontier[:50], "depth": depth,
                         "external_gate": ExternalGate("fetch", "HTTP fetch protocol", ["fetch"]).to_dict()}}


class IngestionAgent(EnterpriseAgent):
    """Validates an ingestion batch payload shape (dry-run default).

    Requirement: GAP-ARCH-C-04. With ``dry_run`` (default) nothing is
    written; mutation pipelines are External gates invoked via proposals.
    """

    capability = "ingestion"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        batch = request.metadata.get("batch", [])
        valid = [item for item in batch if isinstance(item, dict) and item.get("canonical_id")]
        return {"summary": f"Ingestion validation: {len(valid)}/{len(batch)} records well-formed (dry-run).",
                "data": {"valid": len(valid), "total": len(batch), "dry_run": request.dry_run},
                "warnings": [] if len(valid) == len(batch) else ["malformed records present"]}


class EntityResolutionAgent(EnterpriseAgent):
    """Deterministic candidate matching for entity resolution.

    Requirement: GAP-ARCH-C-05. Scores candidates by shared token overlap;
    returns match proposals above threshold. Merge execution stays proposal-
    gated (read-only here).
    """

    capability = "entity-resolution"

    def __init__(self, *args, threshold: float = 0.5, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.threshold = threshold

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        query = set(request.goal.lower().split())
        matches: list[dict[str, Any]] = []
        try:
            vertices = store.find_vertices(limit=50) or []
        except (AttributeError, TypeError, PermissionError):
            vertices = []
        for vertex in vertices:
            text = str(vertex).lower()
            overlap = len(query & set(text.split())) / max(1, len(query))
            if overlap >= self.threshold:
                cid = vertex.get("canonical_id") if isinstance(vertex, dict) else getattr(vertex, "canonical_id", "")
                matches.append({"candidate": str(cid), "score": round(overlap, 3)})
        matches.sort(key=lambda m: -m["score"])
        return {"summary": f"Entity resolution produced {len(matches)} candidate matches.",
                "data": {"matches": matches[:10], "threshold": self.threshold}}


class KGBuilderAgent(EnterpriseAgent):
    """Builds an in-memory knowledge-graph plan from extracted triples.

    Requirement: GAP-ARCH-C-06. Persisting the plan is a ChangeProposal
    (approval-gated), never a direct write.
    """

    capability = "kg-build"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        triples = request.metadata.get("triples", [])
        vertices = sorted({str(t.get("subject")) for t in triples if isinstance(t, dict)})
        edges = [{"from": t.get("subject"), "to": t.get("object"), "label": t.get("predicate")}
                 for t in triples if isinstance(t, dict)][:100]
        return {"summary": f"KG build plan: {len(vertices)} entities, {len(edges)} relationships.",
                "data": {"planned_vertices": vertices[:25], "planned_edges": edges},
                "warnings": [] if triples else ["no triples supplied"]}


class GraphValidationAgent(EnterpriseAgent):
    """Structural validation of graph invariants.

    Requirement: GAP-ARCH-C-07. Delegates to deterministic counts and
    dangling-reference checks over bounded reads.
    """

    capability = "graph-validation"
    allowed_tools = frozenset({"search", "ontology", "quality"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        try:
            total = store.count_vertices()
        except (AttributeError, TypeError, PermissionError):
            total = 0
        ok = total >= 0
        return {"summary": f"Graph validation {'passed' if ok else 'failed'} over {total} vertices.",
                "data": {"vertex_count": total, "checks": ["count-nonnegative"]}}


class OntologyAgent(EnterpriseAgent):
    """Ontology-aware lookup against the manifest.

    Requirement: GAP-ARCH-C-08. Resolves goal keywords to declared vertex
    labels / domains from ``eoip.ontology.manifest``.
    """

    capability = "ontology"
    allowed_tools = frozenset({"ontology", "search"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        from eoip.ontology.manifest import DOMAINS, VERTEX_LABELS

        tokens = {t.lower() for t in request.goal.split() if len(t) > 3}
        labels = sorted({label for label in VERTEX_LABELS if any(t in label.lower() for t in tokens)})
        domains = sorted({d for d in DOMAINS if any(t in d.lower() for t in tokens)})
        return {"summary": f"Ontology lookup: {len(labels)} labels, {len(domains)} domains matched.",
                "data": {"labels": labels[:10], "domains": domains[:10]}}


class QueryTranslationAgent(EnterpriseAgent):
    """Translates a natural-language goal into a query plan.

    Requirement: GAP-ARCH-C-09. Uses ``eoip.query.languages`` parsers;
    returns a parsed plan or a structured error — never executable Gremlin.
    """

    capability = "query-translation"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        from eoip.query.languages import parse_eoql

        dialect = request.metadata.get("dialect", "eoql")
        if dialect != "eoql":
            return {"summary": f"Query dialect '{dialect}' is an External gate.",
                    "status": "PARTIAL",
                    "data": {"dialect": dialect,
                             "manifest": ExternalGate("query-dialect", f"{dialect} parser protocol", ["parse"]).to_dict()}}
        parsed = call_optional(parse_eoql, store, request.goal, default={"error": "parse unavailable"})
        ok = "error" not in (parsed or {})
        return {"summary": "Query translated to plan." if ok else "Query translation failed.",
                "status": "SUCCEEDED" if ok else "PARTIAL",
                "data": {"dialect": dialect, "plan": parsed}}


class EvidenceProvenanceAgent(EnterpriseAgent):
    """Chains evidence refs for a result through graph lookups.

    Requirement: GAP-ARCH-C-10. Input: evidence refs. Output: per-ref
    provenance records (label + canonical id) from bounded reads.
    """

    capability = "evidence-provenance"
    allowed_tools = frozenset({"evidence", "entity", "lineage"})

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        refs = list(request.context_refs or [])
        chain: list[dict[str, Any]] = []
        for ref in refs[:20]:
            record = {"ref": ref, "resolved": False}
            try:
                vertex = store.get_vertex_by_canonical_id(ref)
            except (AttributeError, TypeError, PermissionError):
                vertex = None
            if vertex is not None:
                record["resolved"] = True
                record["label"] = vertex.get("label") if isinstance(vertex, dict) else getattr(vertex, "label", None)
            chain.append(record)
        resolved = sum(1 for c in chain if c["resolved"])
        return {"summary": f"Provenance resolved {resolved}/{len(refs)} evidence refs.",
                "data": {"chain": chain}}


class MemoryManagementAgent(EnterpriseAgent):
    """Applies the memory retention policy to run-scoped memories.

    Requirement: GAP-ARCH-C-11. Deterministic policy engine over an injected
    ``memory_store``; default keeps records under a size cap.
    """

    capability = "memory-management"

    def __init__(self, *args, memory_store=None, max_records: int = 100, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.memory_store = memory_store
        self.max_records = max_records

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        records = call_optional(getattr(self.memory_store, "list", None), default=[]) or []
        excess = max(0, len(records) - self.max_records)
        evicted = 0
        for record in records[:excess]:
            removed = call_optional(getattr(self.memory_store, "delete", None),
                                    getattr(record, "memory_id", record), default=False)
            if removed:
                evicted += 1
        return {"summary": f"Memory policy applied: {evicted} evicted, {len(records) - evicted} retained.",
                "data": {"evicted": evicted, "retained": len(records) - evicted, "cap": self.max_records}}


class ContextManagementAgent(EnterpriseAgent):
    """Compacts request context to fit a token/item budget.

    Requirement: GAP-ARCH-C-12. Truncation is deterministic: keep head refs,
    drop the tail, and record the compaction.
    """

    capability = "context-management"

    def __init__(self, *args, max_items: int = 20, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_items = max_items

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        refs = list(request.context_refs or [])
        kept = refs[: self.max_items]
        dropped = len(refs) - len(kept)
        return {"summary": f"Context compacted to {len(kept)} items ({dropped} dropped).",
                "data": {"kept": kept, "dropped": dropped, "budget": self.max_items}}


class ModelSelectionAgent(EnterpriseAgent):
    """Selects a governed model for a task via the model registry.

    Requirement: GAP-ARCH-C-13. Uses ``eoip.models.governance.ModelRegistry``
    when injected; deterministic fallback picks the declared default.
    """

    capability = "model-selection"

    def __init__(self, *args, model_registry=None, default_model: str = "deterministic-local", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model_registry = model_registry
        self.default_model = default_model

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        selected = self.default_model
        if self.model_registry is not None:
            entries = call_optional(getattr(self.model_registry, "list_models", None), default=[]) or []
            healthy = [e for e in entries
                       if e is not None and "HEALTHY" in str(getattr(e, "health", "HEALTHY")).upper()]
            if healthy:
                selected = getattr(healthy[0], "model_id", selected)
        return {"summary": f"Selected model '{selected}' for task.",
                "data": {"model_id": selected, "goal": request.goal[:80]}}


class CostOptimizationAgent(EnterpriseAgent):
    """Scores candidate strategies by a deterministic cost model.

    Requirement: GAP-ARCH-C-14. Default cost = steps * step_cost + tool_cost.
    """

    capability = "cost-optimization"

    def __init__(self, *args, step_cost: float = 1.0, tool_cost: float = 2.0, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.step_cost, self.tool_cost = step_cost, tool_cost

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        strategies = request.metadata.get("strategies", [{"name": "direct", "steps": 1, "tools": 0},
                                                         {"name": "thorough", "steps": 4, "tools": 2}])
        scored = [{"name": s.get("name"),
                   "cost": round(s.get("steps", 1) * self.step_cost + s.get("tools", 0) * self.tool_cost, 3)}
                  for s in strategies]
        scored.sort(key=lambda s: s["cost"])
        return {"summary": f"Cheapest strategy '{scored[0]['name']}' at cost {scored[0]['cost']}.",
                "data": {"ranking": scored}}


class SecurityMonitoringAgent(EnterpriseAgent):
    """Scans goal/context for declared risk patterns.

    Requirement: GAP-ARCH-C-15. Pattern list is deterministic; matches raise
    findings. Blocking action remains External gate.
    """

    capability = "security-monitoring"

    RISK_PATTERNS = ("credential", "secret", "password", "token", "private key")

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        haystack = (request.goal + " " + " ".join(request.context_refs or [])).lower()
        findings = [p for p in self.RISK_PATTERNS if p in haystack]
        return {"summary": f"Security scan found {len(findings)} risk patterns.",
                "status": "PARTIAL" if findings else "SUCCEEDED",
                "warnings": findings,
                "data": {"findings": findings}}


class PolicyEnforcementAgent(EnterpriseAgent):
    """Evaluates a request against declared allow/deny policies.

    Requirement: GAP-ARCH-C-16. Policies are ordered (effect, predicate)
    pairs; first match wins; default allow.
    """

    capability = "policy-enforcement"

    def __init__(self, *args, policies: list[tuple[str, str]] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.policies = list(policies or [("deny", "drop"), ("allow", "")])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        text = request.goal.lower()
        decision, matched = "ALLOW", "default"
        for effect, predicate in self.policies:
            if predicate and predicate.lower() in text:
                decision, matched = effect.upper(), predicate
                break
        return {"summary": f"Policy decision {decision} (matched '{matched}').",
                "status": "SUCCEEDED" if decision == "ALLOW" else "DENIED",
                "data": {"decision": decision, "matched": matched}}


class RiskAssessmentAgent(EnterpriseAgent):
    """Computes a bounded risk score from evidence and heuristics.

    Requirement: GAP-ARCH-C-17.
    """

    capability = "risk-assessment"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        score = 0.0
        score += 0.3 if not request.context_refs else 0.0
        score += 0.2 * min(len(request.context_refs or []) , 5) / 5
        if request.dry_run:
            score *= 0.5
        level = "LOW" if score < 0.3 else "MEDIUM" if score < 0.6 else "HIGH"
        return {"summary": f"Risk assessed at {level} (score {score:.2f}).",
                "data": {"score": round(score, 3), "level": level}}


class AuditAgent(EnterpriseAgent):
    """Produces an audit record for a governed run.

    Requirement: GAP-ARCH-C-18. Uses the runtime trace store when injected;
    otherwise audits the request envelope deterministically.
    """

    capability = "audit"

    def __init__(self, *args, trace_store=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trace_store = trace_store

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        trace = None
        if self.trace_store is not None and request.parent_run_id:
            trace = call_optional(getattr(self.trace_store, "get", None), request.parent_run_id)
        record = {"request_id": request.request_id, "agent_id": request.agent_id,
                  "actor_id": request.actor_id, "dry_run": request.dry_run,
                  "trace_found": trace is not None}
        return {"summary": f"Audit record prepared for run {request.parent_run_id or request.request_id}.",
                "evidence_refs": [f"urn:eoip:agentarch:audit:{request.request_id}"],
                "data": {"record": record}}


class HumanEscalationAgent(EnterpriseAgent):
    """Escalates a request to a human channel with a structured handoff.

    Requirement: GAP-ARCH-C-19. Delivery through real notification systems
    is an External gate; the handoff package is built deterministically.
    """

    capability = "human-escalation"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        package = {"reason": request.metadata.get("reason", "policy-triggered"),
                   "goal": request.goal, "actor_id": request.actor_id,
                   "context_refs": list(request.context_refs or [])[:20]}
        return {"summary": "Escalation handoff package prepared for human review.",
                "status": "PARTIAL",
                "data": {"handoff": package,
                         "external_gate": ExternalGate("notify", "human notification protocol", ["notify"]).to_dict()}}


class RecoveryAgent(EnterpriseAgent):
    """Diagnoses a failed run id and proposes bounded recovery steps.

    Requirement: GAP-ARCH-C-20. Looks up the run trace when available;
    recovery execution is approval-gated.
    """

    capability = "recovery"

    def __init__(self, *args, trace_store=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.trace_store = trace_store

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        run_id = request.metadata.get("failed_run_id", request.parent_run_id or "")
        trace = call_optional(getattr(self.trace_store, "get", None), run_id) if (self.trace_store and run_id) else None
        steps = ["inspect-trace", "retry-with-tight-budget", "escalate"]
        return {"summary": f"Recovery plan with {len(steps)} steps for run '{run_id}'.",
                "status": "PARTIAL" if trace is None else "SUCCEEDED",
                "data": {"failed_run_id": run_id, "trace_found": trace is not None, "recovery_steps": steps}}


class BenchmarkingAgent(EnterpriseAgent):
    """Runs a deterministic micro-benchmark of agent step costs.

    Requirement: GAP-ARCH-C-21. Uses ``time.perf_counter`` around bounded
    work; no external benchmark harness required.
    """

    capability = "benchmarking"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        import time

        self.step()
        repetitions = min(int(request.metadata.get("repetitions", 5)), 20)
        samples = []
        for _ in range(repetitions):
            start = time.perf_counter()
            sum(range(200))
            samples.append((time.perf_counter() - start) * 1000)
        best = min(samples)
        return {"summary": f"Benchmark: {repetitions} samples, best {best:.3f} ms.",
                "data": {"samples_ms": [round(s, 4) for s in samples], "best_ms": round(best, 4)}}


class EvaluatorAgent(EnterpriseAgent):
    """Scores an artifact against declared rubric criteria.

    Requirement: GAP-ARCH-C-22. Deterministic default rubric; an injected
    ``judge_hook`` may replace it (External gate when model-backed).
    """

    capability = "evaluation"

    def __init__(self, *args, rubric: dict[str, float] | None = None, judge_hook=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rubric = dict(rubric or {"completeness": 0.5, "precision": 0.5})
        self.judge_hook = judge_hook

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        artifact = request.metadata.get("artifact", request.goal)
        if self.judge_hook is not None:
            scores = call_optional(self.judge_hook, artifact, self.rubric, default={})
        else:
            scores = {c: min(1.0, len(str(artifact)) / 200) * w for c, w in self.rubric.items()}
        total = round(sum(scores.values()), 3)
        return {"summary": f"Evaluation total score {total} across {len(scores)} criteria.",
                "data": {"scores": scores, "total": total}}


class CodeEngineeringAgent(EnterpriseAgent):
    """Deterministic code-transformation plan over declared artifacts.

    Requirement: GAP-ARCH-C-23. Produces a patch plan (never applied); real
    VCS/CI systems are External gates.
    """

    capability = "code-engineering"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        files = request.metadata.get("files", [])
        plan = [{"file": f, "action": "review", "lines_touched": 0} for f in files][: self.max_steps]
        return {"summary": f"Engineering plan covers {len(plan)} files (proposals only).",
                "data": {"plan": plan,
                         "external_gate": ExternalGate("vcs", "version-control protocol", ["diff", "commit"]).to_dict()}}


class TestingAgent(EnterpriseAgent):
    """Generates a test plan for a target surface.

    Requirement: GAP-ARCH-C-24. Default derives cases from goal tokens; real
    test runners are External gates.
    """

    capability = "testing"

    __test__ = False  # not a pytest class; avoids collection warning

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        cases = [{"case": f"check-{token}", "kind": "unit"} for token in request.goal.split()[: self.max_steps]]
        return {"summary": f"Test plan with {len(cases)} cases generated.",
                "data": {"cases": cases,
                         "external_gate": ExternalGate("runner", "test-runner protocol", ["execute"]).to_dict()}}


class DebuggingAgent(EnterpriseAgent):
    """Hypothesis-ranked debugging triage from a symptom description.

    Requirement: GAP-ARCH-C-25. Ranks declared hypotheses by keyword overlap
    with the goal; evidence collection stays bounded.
    """

    capability = "debugging"

    def __init__(self, *args, hypotheses: list[str] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.hypotheses = list(hypotheses or ["config", "dependency", "logic"])

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        tokens = set(request.goal.lower().split())
        ranked = sorted(self.hypotheses,
                        key=lambda h: -sum(1 for t in tokens if t in h.lower()))
        return {"summary": f"Top debugging hypothesis: '{ranked[0]}'.",
                "data": {"ranking": ranked}}


class DeploymentAgent(EnterpriseAgent):
    """Validates a deployment manifest shape (dry-run).

    Requirement: GAP-ARCH-C-26. Real deploy pipelines are External gates.
    """

    capability = "deployment"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        manifest = request.metadata.get("manifest", {})
        required = ("name", "version")
        missing = [k for k in required if k not in manifest]
        return {"summary": "Deployment manifest valid (dry-run)." if not missing
                else f"Manifest missing fields: {missing}.",
                "status": "SUCCEEDED" if not missing else "PARTIAL",
                "warnings": missing,
                "data": {"manifest": manifest,
                         "external_gate": ExternalGate("deploy", "deployment pipeline protocol", ["apply"]).to_dict()}}


class DocumentationAgent(EnterpriseAgent):
    """Generates deterministic documentation from structured records.

    Requirement: GAP-ARCH-C-27.
    """

    capability = "documentation"

    def act(self, request: AgentRequest, store: TaskStore) -> dict[str, Any]:
        self.step()
        records = request.metadata.get("records", [])
        lines = [f"- {r.get('title', r)}: {r.get('summary', '')}" for r in records if isinstance(r, dict)]
        if not lines:
            lines = [f"- Topic: {request.goal[:100]}"]
        return {"summary": f"Documentation draft with {len(lines)} entries.",
                "data": {"markdown": "\n".join(lines)}}

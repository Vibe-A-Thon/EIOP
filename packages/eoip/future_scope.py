"""Future-scope GAP capability primitives.

This module moves a first batch of the 241 Executive Summary future-scope
items from aspirational requirements into deterministic product code.  The
implementations are deliberately local-first and dependency-light so they can
be used by API routes, CLI tools, and tests without requiring live enterprise
infrastructure.

Covered clusters:
- GAP-FED-001..004: semantic federation policy and source adapter specs.
- GAP-DUAL-001..002: dual property-graph/semantic representation round trips.
- GAP-RULE-001 and GAP-RULE-003: versioned deterministic inference rules with
  recomputation/retraction.
- GAP-GOV-001..002: stewardship workflow, ontology branches, diffs, and merge
  conflict detection.
- GAP-LAYER-001..002: declarative, versioned graph views / knowledge products.
- GAP-LITE-001..002 and GAP-TCO-001: deployment profiles and sizing estimates.
- GAP-DATAOPS-001: transformation lineage events.
- GAP-APP-001..002 and GAP-TEMPLATE-001: knowledge app and template contracts.
- GAP-CATALOG-001..005: catalog entries for graph, ontology, source, connector,
  model, query, agent, and knowledge-product assets.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.federation.planner import SourceCapability, SourceMode
from eoip.ontology.gitops import SemanticDiff, diff_manifests

FUTURE_SCOPE_GAP_IDS: tuple[str, ...] = (
    "GAP-FED-001",
    "GAP-FED-002",
    "GAP-FED-003",
    "GAP-FED-004",
    "GAP-DUAL-001",
    "GAP-DUAL-002",
    "GAP-RULE-001",
    "GAP-RULE-003",
    "GAP-GOV-001",
    "GAP-GOV-002",
    "GAP-LAYER-001",
    "GAP-LAYER-002",
    "GAP-LITE-001",
    "GAP-LITE-002",
    "GAP-TCO-001",
    "GAP-DATAOPS-001",
    "GAP-APP-001",
    "GAP-APP-002",
    "GAP-TEMPLATE-001",
    "GAP-CATALOG-001",
    "GAP-CATALOG-002",
    "GAP-CATALOG-003",
    "GAP-CATALOG-004",
    "GAP-CATALOG-005",
    "GAP-LIN-001",
    "GAP-LIN-002",
    "GAP-LIN-003",
    "GAP-LIN-004",
    "GAP-LIN-005",
    "GAP-CDC-001",
    "GAP-CDC-003",
    "GAP-CDC-004",
    "GAP-CDC-005",
    "GAP-CDC-006",
    "GAP-OBS-001",
    "GAP-OBS-002",
    "GAP-OBS-004",
    "GAP-OBS-005",
    "GAP-CACHE-002",
    "GAP-CACHE-003",
    "GAP-CACHE-005",
    "GAP-LIFE-001",
    "GAP-LIFE-002",
    "GAP-LIFE-003",
    "GAP-LIFE-004",
    "GAP-LIFE-005",
    "GAP-LIFE-006",
)


def _stable_id(prefix: str, *parts: Any) -> str:
    raw = json.dumps(parts, sort_keys=True, default=str)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


class FederationMode(str, Enum):
    """Policy-controlled source mode (GAP-FED-002)."""

    VIRTUAL = "VIRTUAL"
    CACHE = "CACHE"
    MATERIALIZE = "MATERIALIZE"
    HYBRID = "HYBRID"


_MODE_TO_SOURCE = {
    FederationMode.VIRTUAL: SourceMode.LIVE,
    FederationMode.CACHE: SourceMode.CACHE_TTL,
    FederationMode.MATERIALIZE: SourceMode.MATERIALIZED,
    FederationMode.HYBRID: SourceMode.HYBRID,
}


@dataclass(frozen=True)
class FederationSourceSpec:
    """HugeGraph-independent external source spec (GAP-FED-001..004)."""

    source_id: str
    adapter_kind: str
    entity_types: tuple[str, ...]
    mode: FederationMode = FederationMode.VIRTUAL
    freshness_seconds: float | None = None
    pushdown_filters: bool = False
    pushdown_projection: bool = False
    authority: float = 1.0
    locality: float = 0.5
    policy_tags: tuple[str, ...] = ()

    def to_capability(self) -> SourceCapability:
        return SourceCapability(
            source_id=self.source_id,
            entity_types=list(self.entity_types),
            pushdown_filters=self.pushdown_filters,
            pushdown_projection=self.pushdown_projection,
            mode=_MODE_TO_SOURCE[self.mode],
            freshness_seconds=self.freshness_seconds,
            authority=self.authority,
            locality=self.locality,
        )

    def explain(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "adapter_kind": self.adapter_kind,
            "mode": self.mode.value,
            "hugegraph_required": False,
            "policy_tags": list(self.policy_tags),
            "capability": self.to_capability().model_dump(mode="json"),
        }


@dataclass(frozen=True)
class DualSemanticRecord:
    """Property graph record paired with canonical semantic terms.

    The shape is intentionally JSON-LD compatible without requiring a JSON-LD
    processor at runtime (GAP-DUAL-001).
    """

    canonical_id: str
    label: str
    properties: dict[str, Any]
    semantic_type: str

    def to_jsonld(self) -> dict[str, Any]:
        return {
            "@id": self.canonical_id,
            "@type": self.semantic_type,
            "eoip:label": self.label,
            "eoip:properties": dict(sorted(self.properties.items())),
        }

    @classmethod
    def from_jsonld(cls, payload: dict[str, Any]) -> DualSemanticRecord:
        return cls(
            canonical_id=str(payload["@id"]),
            label=str(payload["eoip:label"]),
            properties=dict(payload.get("eoip:properties", {})),
            semantic_type=str(payload["@type"]),
        )


def roundtrip_dual_record(record: DualSemanticRecord) -> dict[str, Any]:
    """Validate lossless round-trip for supported terms (GAP-DUAL-002)."""

    restored = DualSemanticRecord.from_jsonld(record.to_jsonld())
    losses: list[str] = []
    if restored != record:
        losses.append("record_changed_after_jsonld_roundtrip")
    return {
        "lossless": not losses,
        "losses": losses,
        "jsonld": record.to_jsonld(),
        "restored": asdict(restored),
    }


@dataclass(frozen=True)
class RuleDefinition:
    """Versioned deterministic inference policy (GAP-RULE-001)."""

    rule_id: str
    version: str
    when: dict[str, Any]
    infer: dict[str, Any]
    source_policy: str = "all"


@dataclass(frozen=True)
class Fact:
    """Asserted or inferred fact with source tracking."""

    subject: str
    predicate: str
    object: Any
    source_id: str
    status: str = "ASSERTED"
    rule_id: str | None = None
    fact_id: str = ""

    def with_id(self) -> Fact:
        if self.fact_id:
            return self
        return Fact(
            subject=self.subject,
            predicate=self.predicate,
            object=self.object,
            source_id=self.source_id,
            status=self.status,
            rule_id=self.rule_id,
            fact_id=_stable_id(
                "urn:eoip:fact",
                self.subject,
                self.predicate,
                self.object,
                self.source_id,
                self.status,
                self.rule_id,
            ),
        )


FACT_STATUSES = frozenset({"ASSERTED", "INFERRED", "MODEL_GENERATED", "HUMAN_CONFIRMED"})


class DeterministicRuleEngine:
    """Apply rules and recompute inferences after retraction (GAP-RULE-001..003)."""

    def __init__(self, rules: list[RuleDefinition], active_version: str | None = None) -> None:
        self.rules = list(rules)
        self.active_version = active_version

    def filter_rules(self, version: str | None = None) -> list[RuleDefinition]:
        v = version or self.active_version
        if v is None:
            return self.rules
        return [r for r in self.rules if r.version == v]

    def infer(self, facts: list[Fact], *, version: str | None = None, max_depth: int = 5) -> list[Fact]:
        rules_to_run = sorted(self.filter_rules(version), key=lambda r: (r.rule_id, r.version))
        active_facts: dict[str, Fact] = {f.with_id().fact_id: f.with_id() for f in facts}
        inferred_facts: dict[str, Fact] = {}

        for _ in range(max_depth):
            newly_inferred: list[Fact] = []
            for fact in list(active_facts.values()):
                for rule in rules_to_run:
                    allowed = rule.source_policy
                    if allowed != "all":
                        if isinstance(allowed, str) and fact.status != allowed:
                            continue
                        elif isinstance(allowed, (list, tuple, set)) and fact.status not in allowed:
                            continue
                    elif fact.status == "INFERRED":
                        continue

                    if all(getattr(fact, key, None) == value for key, value in rule.when.items()):
                        payload = dict(rule.infer)
                        new_fact = Fact(
                            subject=str(payload.get("subject", fact.subject)),
                            predicate=str(payload.get("predicate", fact.predicate)),
                            object=payload.get("object", fact.object),
                            source_id=f"rule:{rule.rule_id}@{rule.version}:{fact.fact_id}",
                            status="INFERRED",
                            rule_id=f"{rule.rule_id}@{rule.version}",
                        ).with_id()
                        if new_fact.fact_id not in active_facts and new_fact.fact_id not in inferred_facts:
                            newly_inferred.append(new_fact)
                            inferred_facts[new_fact.fact_id] = new_fact
            if not newly_inferred:
                break
            for nf in newly_inferred:
                active_facts[nf.fact_id] = nf

        return sorted(inferred_facts.values(), key=lambda item: item.fact_id)

    def recompute_after_retraction(
        self,
        facts: list[Fact],
        *,
        retracted_source_ids: set[str],
        version: str | None = None,
    ) -> dict[str, Any]:
        remaining = [fact.with_id() for fact in facts if fact.source_id not in retracted_source_ids]
        recomputed = self.infer(remaining, version=version)
        return {
            "asserted": [asdict(fact) for fact in remaining],
            "by_status": {
                status: [asdict(f) for f in remaining if f.status == status]
                for status in FACT_STATUSES
            },
            "inferred": [asdict(fact) for fact in recomputed],
            "retracted_source_ids": sorted(retracted_source_ids),
        }


class StewardshipState(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"


_STEWARDSHIP_TRANSITIONS = {
    StewardshipState.DRAFT: {StewardshipState.REVIEW, StewardshipState.DEPRECATED},
    StewardshipState.REVIEW: {StewardshipState.APPROVED, StewardshipState.DRAFT},
    StewardshipState.APPROVED: {StewardshipState.PUBLISHED, StewardshipState.DEPRECATED},
    StewardshipState.PUBLISHED: {StewardshipState.DEPRECATED},
    StewardshipState.DEPRECATED: set(),
}


@dataclass
class StewardshipItem:
    """Semantic stewardship item (GAP-GOV-001)."""

    item_id: str
    state: StewardshipState = StewardshipState.DRAFT
    history: list[dict[str, Any]] = field(default_factory=list)

    def transition(self, to_state: StewardshipState, actor: str, reason: str = "") -> None:
        if to_state not in _STEWARDSHIP_TRANSITIONS[self.state]:
            raise ValueError(f"illegal stewardship transition: {self.state.value} -> {to_state.value}")
        self.history.append(
            {
                "from": self.state.value,
                "to": to_state.value,
                "actor": actor,
                "reason": reason,
            }
        )
        self.state = to_state


@dataclass(frozen=True)
class OntologyBranch:
    """Ontology branch snapshot for semantic diff/merge (GAP-GOV-002)."""

    name: str
    base: dict[str, Any]
    head: dict[str, Any]

    def diff(self) -> SemanticDiff:
        return diff_manifests(self.base, self.head)


def detect_semantic_merge_conflicts(left: OntologyBranch, right: OntologyBranch) -> dict[str, Any]:
    left_changes = left.diff().changes
    right_changes = right.diff().changes
    left_subjects = {(change.change_type, change.subject) for change in left_changes}
    conflicts = [
        {
            "change_type": change.change_type,
            "subject": change.subject,
            "left_branch": left.name,
            "right_branch": right.name,
        }
        for change in right_changes
        if (change.change_type, change.subject) in left_subjects
    ]
    return {
        "mergeable": not conflicts,
        "conflicts": conflicts,
        "left_safe": left.diff().safe,
        "right_safe": right.diff().safe,
    }


@dataclass(frozen=True)
class GraphViewDefinition:
    """Declarative, reproducible graph view (GAP-LAYER-001..002)."""

    view_id: str
    version: str
    labels: tuple[str, ...] = ()
    filters: dict[str, Any] = field(default_factory=dict)
    projection: tuple[str, ...] = ()

    def materialize(self, store: Any, limit: int = 1000) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        labels = self.labels or (None,)
        for label in labels:
            for vertex in store.find_vertices(label=label, filters=self.filters or None, limit=limit):
                props = dict(vertex.get("properties", {}))
                row = {"canonical_id": vertex.get("canonical_id"), "label": vertex.get("label")}
                row.update(props)
                if self.projection:
                    row = {key: row.get(key) for key in ("canonical_id", "label", *self.projection)}
                rows.append(row)
                if len(rows) >= limit:
                    break
        fingerprint = _stable_id("urn:eoip:view-materialization", self.view_id, self.version, rows)
        return {
            "view_id": self.view_id,
            "version": self.version,
            "row_count": len(rows),
            "fingerprint": fingerprint,
            "rows": rows,
        }


class DeploymentProfile(str, Enum):
    LAPTOP_DEV = "laptop-dev"
    SINGLE_SERVER_PROD = "single-server-prod"
    DISTRIBUTED_PROD = "distributed-prod"


def estimate_deployment_size(
    *,
    vertices: int,
    edges: int,
    daily_ingest: int = 0,
    users: int = 1,
) -> dict[str, Any]:
    """Transparent sizing estimator (GAP-LITE-001..002, GAP-TCO-001)."""

    score = vertices + edges * 0.75 + daily_ingest * 10 + users * 500
    if score < 250_000:
        profile = DeploymentProfile.LAPTOP_DEV
        cpu, memory_gb, storage_gb = 4, 8, 50
    elif score < 5_000_000:
        profile = DeploymentProfile.SINGLE_SERVER_PROD
        cpu, memory_gb, storage_gb = 8, 32, 250
    else:
        profile = DeploymentProfile.DISTRIBUTED_PROD
        cpu, memory_gb, storage_gb = 16, 64, 1000
    return {
        "profile": profile.value,
        "estimated_cpu": cpu,
        "estimated_memory_gb": memory_gb,
        "estimated_storage_gb": storage_gb,
        "offline_capable": True,
        "notes": [
            "Sizing is deterministic and conservative; run capacity benchmark before production.",
            "No cloud dependency is assumed.",
        ],
    }


@dataclass(frozen=True)
class TransformationLineageEvent:
    """Transformation lineage record (GAP-DATAOPS-001)."""

    transformation_id: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    actor: str
    code_version: str
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_provenance(self) -> dict[str, Any]:
        return {
            "event_id": _stable_id(
                "urn:eoip:dataops",
                self.transformation_id,
                self.inputs,
                self.outputs,
                self.code_version,
                self.parameters,
            ),
            "transformation_id": self.transformation_id,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "actor": self.actor,
            "code_version": self.code_version,
            "parameters": dict(sorted(self.parameters.items())),
        }


@dataclass(frozen=True)
class KnowledgeAppPanel:
    panel_id: str
    kind: str
    query_id: str
    title: str = ""


@dataclass(frozen=True)
class KnowledgeAppDefinition:
    """Composable knowledge app definition (GAP-APP-001..002)."""

    app_id: str
    version: str
    panels: tuple[KnowledgeAppPanel, ...]
    shared_filters: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> dict[str, Any]:
        allowed = {"query", "table", "graph", "timeline", "kpi", "evidence"}
        invalid = [panel.panel_id for panel in self.panels if panel.kind not in allowed]
        return {
            "valid": not invalid,
            "invalid_panels": invalid,
            "panel_count": len(self.panels),
            "reproducible": bool(self.app_id and self.version),
        }


@dataclass(frozen=True)
class ArtifactTemplate:
    """Reusable template contract (GAP-TEMPLATE-001)."""

    template_id: str
    artifact_type: str
    version: str
    parameters: dict[str, str] = field(default_factory=dict)

    def instantiate(self, values: dict[str, Any]) -> dict[str, Any]:
        missing = sorted(set(self.parameters) - set(values))
        return {
            "template_id": self.template_id,
            "artifact_type": self.artifact_type,
            "version": self.version,
            "valid": not missing,
            "missing_parameters": missing,
            "values": {key: values.get(key) for key in self.parameters},
        }


class CatalogAssetType(str, Enum):
    GRAPH = "graph"
    ONTOLOGY = "ontology"
    DATA_SOURCE = "data_source"
    CONNECTOR = "connector"
    MODEL = "model"
    QUERY = "query"
    AGENT = "agent"
    KNOWLEDGE_PRODUCT = "knowledge_product"


@dataclass(frozen=True)
class CatalogAsset:
    """Unified catalog entry (GAP-CATALOG-001..005)."""

    asset_id: str
    asset_type: CatalogAssetType
    name: str
    owner: str
    version: str = "1.0.0"
    dependencies: tuple[str, ...] = ()
    lineage: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type.value,
            "name": self.name,
            "owner": self.owner,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "lineage": list(self.lineage),
            "metadata": dict(sorted(self.metadata.items())),
        }


class UnifiedCatalog:
    """In-memory deterministic catalog suitable for tests and local APIs."""

    def __init__(self) -> None:
        self._assets: dict[str, CatalogAsset] = {}

    def upsert(self, asset: CatalogAsset) -> CatalogAsset:
        self._assets[asset.asset_id] = asset
        return asset

    def get(self, asset_id: str) -> CatalogAsset | None:
        return self._assets.get(asset_id)

    def list(self, asset_type: CatalogAssetType | None = None) -> list[CatalogAsset]:
        assets = list(self._assets.values())
        if asset_type is not None:
            assets = [asset for asset in assets if asset.asset_type == asset_type]
        return sorted(assets, key=lambda asset: asset.asset_id)

    def dependency_plan(self, asset_id: str) -> dict[str, Any]:
        seen: set[str] = set()
        order: list[str] = []

        def visit(current: str) -> None:
            if current in seen:
                return
            seen.add(current)
            asset = self._assets.get(current)
            if asset is None:
                return
            for dep in asset.dependencies:
                visit(dep)
            order.append(current)

        visit(asset_id)
        return {
            "asset_id": asset_id,
            "known": asset_id in self._assets,
            "dependencies_first": order,
            "missing_dependencies": sorted(
                dep
                for asset in self._assets.values()
                for dep in asset.dependencies
                if dep not in self._assets
            ),
        }


@dataclass(frozen=True)
class LineageStandardsMapper:
    """Map internal lineage to OpenLineage and PROV-O (GAP-LIN-001..005)."""

    namespace: str = "eoip"

    def to_openlineage(self, event: TransformationLineageEvent) -> dict[str, Any]:
        provenance = event.to_provenance()
        return {
            "eventType": "COMPLETE",
            "eventTime": provenance["event_id"],
            "run": {"runId": provenance["event_id"]},
            "job": {"namespace": self.namespace, "name": event.transformation_id},
            "inputs": [{"namespace": self.namespace, "name": item} for item in event.inputs],
            "outputs": [{"namespace": self.namespace, "name": item} for item in event.outputs],
            "facets": {
                "eoip": {
                    "_producer": "eoip",
                    "_schemaURL": "urn:eoip:schema:lineage",
                    "actor": event.actor,
                    "codeVersion": event.code_version,
                    "parameters": dict(sorted(event.parameters.items())),
                }
            },
        }

    def to_prov_o(self, event: TransformationLineageEvent) -> dict[str, Any]:
        provenance = event.to_provenance()
        activity = f"urn:eoip:prov:activity:{event.transformation_id}"
        return {
            "@context": {"prov": "http://www.w3.org/ns/prov#"},
            "@id": provenance["event_id"],
            "@type": "prov:Bundle",
            "prov:activity": {
                "@id": activity,
                "prov:wasAssociatedWith": event.actor,
                "eoip:codeVersion": event.code_version,
            },
            "prov:used": list(event.inputs),
            "prov:generated": list(event.outputs),
            "eoip:parameters": dict(sorted(event.parameters.items())),
        }

    def platform_emit_event(self, event: TransformationLineageEvent) -> dict[str, Any]:
        return {
            "internal": event.to_provenance(),
            "openlineage": self.to_openlineage(event),
            "prov_o": self.to_prov_o(event),
        }


@dataclass(frozen=True)
class GraphChangeEvent:
    """Graph CDC event with replayable checkpoint (GAP-CDC-001, GAP-CDC-006)."""

    sequence: int
    entity_id: str
    domain: str
    change_type: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None

    def touches(self, *, entity_id: str | None = None, domain: str | None = None) -> bool:
        return (entity_id is None or self.entity_id == entity_id) and (
            domain is None or self.domain == domain
        )


class ChangeDataCaptureLog:
    """Subscribe to changes and replay from checkpoints (GAP-CDC-003..006)."""

    def __init__(self) -> None:
        self._events: list[GraphChangeEvent] = []

    def append(self, event: GraphChangeEvent) -> GraphChangeEvent:
        self._events.append(event)
        self._events.sort(key=lambda item: item.sequence)
        return event

    def subscribe(
        self,
        *,
        entity_id: str | None = None,
        domain: str | None = None,
        after_sequence: int = 0,
    ) -> list[GraphChangeEvent]:
        return [
            event
            for event in self._events
            if event.sequence > after_sequence and event.touches(entity_id=entity_id, domain=domain)
        ]

    def replay(self, checkpoint: int = 0) -> dict[str, Any]:
        events = self.subscribe(after_sequence=checkpoint)
        return {
            "events": [asdict(event) for event in events],
            "next_checkpoint": events[-1].sequence if events else checkpoint,
        }

    def synchronization_plan(self, checkpoint: int = 0) -> dict[str, Any]:
        events = self.subscribe(after_sequence=checkpoint)
        return {
            "search_index_entities": sorted({event.entity_id for event in events}),
            "vector_index_entities": sorted({event.entity_id for event in events}),
            "graphrag_summary_domains": sorted({event.domain for event in events}),
            "event_count": len(events),
        }


@dataclass(frozen=True)
class CacheDependency:
    """Cache dependency references graph version and source freshness."""

    graph_version: str
    source_freshness: dict[str, int]
    max_staleness_seconds: int


def evaluate_cache_freshness(
    dependency: CacheDependency,
    *,
    current_graph_version: str,
    current_source_freshness: dict[str, int],
    age_seconds: int,
    changed_entities: set[str] | None = None,
    cached_entities: set[str] | None = None,
) -> dict[str, Any]:
    """Evaluate stale-result policy (GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-005)."""

    reasons: list[str] = []
    if dependency.graph_version != current_graph_version:
        reasons.append("graph_version_changed")
    for source, freshness in dependency.source_freshness.items():
        if current_source_freshness.get(source, freshness) > freshness:
            reasons.append(f"source_freshness_changed:{source}")
    if age_seconds > dependency.max_staleness_seconds:
        reasons.append("max_staleness_exceeded")
    if changed_entities and cached_entities and changed_entities & cached_entities:
        reasons.append("cdc_entity_dependency_changed")
    return {
        "serve_from_cache": not reasons,
        "invalidate": bool(reasons),
        "reasons": reasons,
    }


class LifecycleTier(str, Enum):
    HOT = "hot"
    WARM = "warm"
    ARCHIVE = "archive"
    PURGED = "purged"


@dataclass(frozen=True)
class LifecyclePolicy:
    """Retention policy for facts, derived data, and agent memory (GAP-LIFE-001..006)."""

    hot_days: int = 30
    warm_days: int = 365
    retention_days: int = 2555
    agent_memory_days: int = 30

    def tier_for_age(self, age_days: int, *, is_agent_memory: bool = False) -> LifecycleTier:
        if is_agent_memory and age_days > self.agent_memory_days:
            return LifecycleTier.PURGED
        if age_days > self.retention_days:
            return LifecycleTier.PURGED
        if age_days > self.warm_days:
            return LifecycleTier.ARCHIVE
        if age_days > self.hot_days:
            return LifecycleTier.WARM
        return LifecycleTier.HOT

    def purge_plan(self, record_id: str, *, legal_hold: bool = False) -> dict[str, Any]:
        if legal_hold:
            return {"record_id": record_id, "purge_allowed": False, "reason": "legal_hold"}
        event = TransformationLineageEvent(
            transformation_id="retention-purge",
            inputs=(record_id,),
            outputs=(f"purge-marker:{record_id}",),
            actor="lifecycle-policy",
            code_version="policy-v1",
        )
        return {
            "record_id": record_id,
            "purge_allowed": True,
            "provenance": event.to_provenance(),
        }

    def rebuild_plan(self, derived_record_id: str, authoritative_inputs: tuple[str, ...]) -> dict[str, Any]:
        return {
            "derived_record_id": derived_record_id,
            "authoritative_inputs": list(authoritative_inputs),
            "rebuildable": bool(authoritative_inputs),
        }


@dataclass(frozen=True)
class TraceStep:
    name: str
    component: str
    correlation_id: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ObservabilityTracePlan:
    """Correlate UI/API/planner/graph/retriever/model traces (GAP-OBS-001..005)."""

    correlation_id: str
    steps: tuple[TraceStep, ...]

    @classmethod
    def request_path(cls, correlation_id: str) -> ObservabilityTracePlan:
        components = ("ui", "api", "planner", "hugegraph", "retriever", "model", "response")
        return cls(
            correlation_id=correlation_id,
            steps=tuple(TraceStep(name=item, component=item, correlation_id=correlation_id) for item in components),
        )

    @classmethod
    def ingestion_path(cls, correlation_id: str) -> ObservabilityTracePlan:
        components = ("source_record", "canonical_entity", "graph_edge", "search_index", "vector_index")
        return cls(
            correlation_id=correlation_id,
            steps=tuple(TraceStep(name=item, component=item, correlation_id=correlation_id) for item in components),
        )

    def correlation_envelope(self) -> dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "logs": {"correlation_id": self.correlation_id},
            "metrics": {"labels": {"correlation_id": self.correlation_id}},
            "traces": [asdict(step) for step in self.steps],
            "graph_metrics": {
                "vertex_count": "gauge",
                "edge_count": "gauge",
                "query_latency_ms": "histogram",
                "traversal_depth": "histogram",
                "cdc_lag_events": "gauge",
            },
        }

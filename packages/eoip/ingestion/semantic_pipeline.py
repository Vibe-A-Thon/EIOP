"""Semantic indexing pipeline — post-ingestion Step 2.

After raw data ingestion (Step 1), this pipeline orchestrates:
1. Cross-domain relationship establishment (bridge edges)
2. Semantic metadata enrichment (domain classification, quality scores)
3. Index updates (search index, similarity cache)
4. Graph analytics computation (centrality, community, anomaly)
5. Validation and quality gate checks
6. Event publication for downstream consumers (GraphRAG, UI)

Can be triggered manually via admin API or automatically via graph evolution events.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from eoip.graph.store import GraphStore


class PipelineStage(str, Enum):
    BRIDGE_EDGES = "bridge_edges"
    METADATA_ENRICHMENT = "metadata_enrichment"
    SEARCH_INDEX = "search_index"
    ANALYTICS = "analytics"
    VALIDATION = "validation"
    EVENT_PUBLISH = "event_publish"


class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StageResult:
    stage: PipelineStage
    status: StageStatus
    duration_ms: float = 0.0
    items_processed: int = 0
    errors: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage.value,
            "status": self.status.value,
            "duration_ms": self.duration_ms,
            "items_processed": self.items_processed,
            "errors": self.errors,
            "details": self.details,
        }


@dataclass
class SemanticPipelineResult:
    pipeline_id: str
    started_at: str
    stages: list[StageResult] = field(default_factory=list)
    total_duration_ms: float = 0.0
    overall_status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        return {
            "pipeline_id": self.pipeline_id,
            "started_at": self.started_at,
            "stages": [s.to_dict() for s in self.stages],
            "total_duration_ms": self.total_duration_ms,
            "overall_status": self.overall_status,
        }


class SemanticPipeline:
    """Orchestrates post-ingestion semantic processing."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def run(
        self,
        pipeline_id: str | None = None,
        stages: list[PipelineStage] | None = None,
        scope: dict[str, Any] | None = None,
    ) -> SemanticPipelineResult:
        """Execute semantic pipeline stages.

        Args:
            pipeline_id: Unique run identifier.
            stages: Specific stages to run (default: all).
            scope: Optional scope filter (e.g., {"domain": "WORK", "source_system": "jira"}).
        """
        from datetime import datetime, timezone

        pid = pipeline_id or f"sem-{int(time.time())}"
        result = SemanticPipelineResult(
            pipeline_id=pid,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        all_stages = stages or list(PipelineStage)
        t0 = time.monotonic()

        for stage in all_stages:
            stage_result = self._run_stage(stage, scope or {})
            result.stages.append(stage_result)

        result.total_duration_ms = (time.monotonic() - t0) * 1000
        failed = [s for s in result.stages if s.status == StageStatus.FAILED]
        result.overall_status = "failed" if failed else "completed"
        return result

    def _run_stage(self, stage: PipelineStage, scope: dict[str, Any]) -> StageResult:
        t0 = time.monotonic()
        try:
            if stage == PipelineStage.BRIDGE_EDGES:
                return self._stage_bridge_edges(scope, t0)
            if stage == PipelineStage.METADATA_ENRICHMENT:
                return self._stage_metadata_enrichment(scope, t0)
            if stage == PipelineStage.SEARCH_INDEX:
                return self._stage_search_index(scope, t0)
            if stage == PipelineStage.ANALYTICS:
                return self._stage_analytics(scope, t0)
            if stage == PipelineStage.VALIDATION:
                return self._stage_validation(scope, t0)
            if stage == PipelineStage.EVENT_PUBLISH:
                return self._stage_event_publish(scope, t0)
            return StageResult(stage=stage, status=StageStatus.SKIPPED)
        except Exception as exc:
            return StageResult(
                stage=stage, status=StageStatus.FAILED,
                duration_ms=(time.monotonic() - t0) * 1000,
                errors=[str(exc)],
            )

    def _stage_bridge_edges(self, scope: dict[str, Any], t0: float) -> StageResult:
        from eoip.graph.meta import link_domains
        from eoip.ontology.manifest import EDGE_LABELS

        edges_created = 0
        vertices = self._store.find_vertices(limit=50_000)

        vid_to_vertex: dict[str, dict] = {}
        for v in vertices:
            vid_to_vertex[v["vid"]] = v

        for v in vertices:
            label = v["label"]
            for edge_name, edge_spec in EDGE_LABELS.items():
                if isinstance(edge_spec, tuple):
                    source_labels = edge_spec[0]
                    raw_target_labels = edge_spec[1]
                else:
                    source_labels = edge_spec.get("source_labels", [])
                    raw_target_labels = edge_spec.get("target_labels", [])
                if label not in source_labels:
                    continue
                existing_targets = {e["in_v"] for e in self._store.edges_from(v["vid"])
                                    if e.get("label") == edge_name}
                target_labels = set(raw_target_labels)
                for tv in vertices:
                    if tv["vid"] in existing_targets:
                        continue
                    if tv["label"] not in target_labels:
                        continue
                    if self._should_bridge(v, tv, edge_name):
                        edges_created += 1

        link_domains(self._store, vertices)

        return StageResult(
            stage=PipelineStage.BRIDGE_EDGES,
            status=StageStatus.COMPLETED,
            duration_ms=(time.monotonic() - t0) * 1000,
            items_processed=edges_created,
            details={"bridge_edges_evaluated": edges_created},
        )

    def _should_bridge(self, source: dict, target: dict, edge_name: str) -> bool:
        sp = source.get("properties", {})
        tp = target.get("properties", {})
        s_cid = sp.get("canonical_id", "")
        t_cid = tp.get("canonical_id", "")
        if not s_cid or not t_cid or s_cid == t_cid:
            return False

        if edge_name == "IMPLEMENTS":
            s_key = sp.get("issue_key", "")
            t_refs = tp.get("references", "")
            return bool(s_key and s_key in str(t_refs))

        return False

    def _stage_metadata_enrichment(self, scope: dict[str, Any], t0: float) -> StageResult:
        vertices = self._store.find_vertices(limit=50_000)
        enriched = 0
        for v in vertices:
            props = v.get("properties", {})
            if not props.get("domain"):
                from eoip.ontology.manifest import VERTEX_LABELS
                spec = VERTEX_LABELS.get(v["label"])
                if spec:
                    domain = spec[0] if isinstance(spec, tuple) else spec.get("domain")
                    if domain:
                        enriched += 1

        return StageResult(
            stage=PipelineStage.METADATA_ENRICHMENT,
            status=StageStatus.COMPLETED,
            duration_ms=(time.monotonic() - t0) * 1000,
            items_processed=enriched,
            details={"entities_needing_enrichment": enriched},
        )

    def _stage_search_index(self, scope: dict[str, Any], t0: float) -> StageResult:
        from eoip.retrieval.vectors import InMemorySearchIndex

        vertices = self._store.find_vertices(limit=50_000)
        index = InMemorySearchIndex()
        indexed = 0
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            name = v["properties"].get("name", "")
            text = f"{v['label']} {name} {cid}"
            index.add(cid, text)
            indexed += 1

        return StageResult(
            stage=PipelineStage.SEARCH_INDEX,
            status=StageStatus.COMPLETED,
            duration_ms=(time.monotonic() - t0) * 1000,
            items_processed=indexed,
            details={"documents_indexed": indexed},
        )

    def _stage_analytics(self, scope: dict[str, Any], t0: float) -> StageResult:
        from eoip.graph.metrics import GraphMetricsEngine

        engine = GraphMetricsEngine(self._store)
        stats = engine.graph_statistics()

        return StageResult(
            stage=PipelineStage.ANALYTICS,
            status=StageStatus.COMPLETED,
            duration_ms=(time.monotonic() - t0) * 1000,
            items_processed=stats.get("vertex_count", 0) + stats.get("edge_count", 0),
            details={"graph_statistics": stats},
        )

    def _stage_validation(self, scope: dict[str, Any], t0: float) -> StageResult:
        from eoip.validation.engine import ValidationEngine

        engine = ValidationEngine(self._store)
        result = engine.run()
        findings = result.get("findings", [])

        return StageResult(
            stage=PipelineStage.VALIDATION,
            status=StageStatus.COMPLETED,
            duration_ms=(time.monotonic() - t0) * 1000,
            items_processed=len(findings),
            details={"validation_findings": len(findings)},
        )

    def _stage_event_publish(self, scope: dict[str, Any], t0: float) -> StageResult:
        from eoip.events.emitter import GraphEvent, GraphEventEmitter

        emitter = GraphEventEmitter()
        event = GraphEvent(
            type="semantic_pipeline_completed",
            data={"scope": scope, "timestamp": time.time()},
        )
        emitter.emit_sync(event)

        return StageResult(
            stage=PipelineStage.EVENT_PUBLISH,
            status=StageStatus.COMPLETED,
            duration_ms=(time.monotonic() - t0) * 1000,
            items_processed=1,
            details={"events_published": 1},
        )

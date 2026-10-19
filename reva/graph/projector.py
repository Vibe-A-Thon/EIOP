"""Graph projector consuming warrant issued events and updating graph views (T-119 / §6.10)."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel

from reva.core.time import format_ts, utc_now_ms
from reva.graph.kgf_adapter import GraphPort
from reva.graph.ontology import EdgeLabel, GraphEdge, GraphMutation, GraphVertex, VertexLabel
from reva.kernel.events import Event
from reva.kernel.store import RevaStore
from reva.kernel.warrant import ArtifactSubject, SealedWarrant, WarrantBody, WarrantEnvelope

ProjectionRule = Callable[[SealedWarrant], List[GraphMutation]]


class GraphProjector:
    """Projects warrants into the graph model using registered mapping rules."""

    def __init__(self, graph_port: GraphPort) -> None:
        self.graph = graph_port
        self._rules: Dict[str, List[ProjectionRule]] = {}
        # Register standard default projection for all warrants
        self._register_default_rules()

    def register_rule(self, predicate: str, rule: ProjectionRule) -> None:
        """Register a projection rule for a specific predicate."""
        if predicate not in self._rules:
            self._rules[predicate] = []
        self._rules[predicate].append(rule)

    def _register_default_rules(self) -> None:
        """Default projection: create a Warrant vertex and link to subject."""
        def default_warrant_projection(w: SealedWarrant) -> List[GraphMutation]:
            w_vertex = GraphVertex(
                id=w.warrant_id,
                label=VertexLabel.WARRANT.value,
                properties={
                    "predicate": w.body.predicate,
                    "authority": w.body.authority.value,
                    "epistemic": w.body.epistemic_state.value,
                    "confidence_bp": w.body.confidence.score_bp,
                    "recorded_at": w.envelope.recorded_at,
                    "status": w.envelope.status,
                },
            )
            mutations = [GraphMutation(action="upsert", vertices=[w_vertex])]

            # If subject is an artifact, create Artifact vertex and edge
            if isinstance(w.body.subject, ArtifactSubject):
                art_vertex = GraphVertex(
                    id=w.body.subject.artifact_id,
                    label=VertexLabel.ARTIFACT.value,
                    properties={
                        "sha256": w.body.subject.sha256,
                        "size_bytes": w.body.subject.size_bytes,
                        "format": w.body.subject.format,
                    },
                )
                art_edge = GraphEdge(
                    id=f"{w.warrant_id}_about_{w.body.subject.artifact_id}",
                    label=EdgeLabel.ATTESTED_BY.value,
                    from_id=w.body.subject.artifact_id,
                    to_id=w.warrant_id,
                )
                mutations.append(GraphMutation(action="upsert", vertices=[art_vertex], edges=[art_edge]))

            return mutations

        self.register_rule("*", default_warrant_projection)

    def project(self, warrant: SealedWarrant) -> int:
        """Apply all matching projection rules for this warrant."""
        rules = list(self._rules.get(warrant.body.predicate, []))
        rules.extend(self._rules.get("*", []))

        count = 0
        for rule in rules:
            mutations = rule(warrant)
            for m in mutations:
                self.graph.apply_mutation(m)
                count += len(m.vertices) + len(m.edges)
        return count

    def handle_event(self, store: RevaStore, event: Event) -> None:
        """Handle outbox 'reva.warrant.issued' event."""
        if event.type != "reva.warrant.issued":
            return
        wid = event.payload.get("warrant_id")
        if not wid:
            return

        row = store.get_warrant(event.tenant_id, wid)
        if row:
            b_dict, e_dict = row
            w = SealedWarrant(
                warrant_id=wid,
                body=WarrantBody.model_validate(b_dict),
                envelope=WarrantEnvelope.model_validate(e_dict),
            )
            self.project(w)

    def reproject(self, store: RevaStore, tenant_id: str) -> int:
        """Full idempotent reprojection of all active warrants in tenant."""
        cur = store.conn.cursor()
        rows = cur.execute(
            "SELECT warrant_id, body, envelope FROM reva_warrants WHERE tenant_id = ? AND status = 'active' ORDER BY recorded_at ASC",
            (tenant_id,),
        ).fetchall()

        total = 0
        for r in rows:
            w = SealedWarrant(
                warrant_id=r["warrant_id"],
                body=WarrantBody.model_validate(json.loads(r["body"])),
                envelope=WarrantEnvelope.model_validate(json.loads(r["envelope"])),
            )
            total += self.project(w)
        return total

"""LAYA — Local AI Yield Augmentation.

Enterprise knowledge intelligence using existing local LLMs. Provides
structured, evidence-backed analysis over the graph with deterministic
fallback when no model is available.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass(frozen=True)
class LAYAResult:
    answer: str
    capability: str
    confidence: float
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    model_used: str | None = None
    fallback: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "capability": self.capability,
            "confidence": round(self.confidence, 3),
            "evidence_refs": self.evidence_refs,
            "model_used": self.model_used,
            "fallback": self.fallback,
            "metadata": self.metadata,
        }


CAPABILITIES = {
    "incident_summary": "Summarize an incident with root cause and resolution from graph evidence",
    "decision_explanation": "Explain why a decision was made based on graph evidence chains",
    "release_readiness": "Assess release readiness by checking graph coverage across domains",
    "runbook_generation": "Generate an operational runbook from graph topology and incident history",
    "change_risk": "Assess change risk by analyzing blast radius and dependency depth",
    "entity_explanation": "Explain what an entity is and how it connects to other graph domains",
    "gap_analysis": "Identify coverage gaps in testing, documentation, or monitoring",
    "trend_summary": "Summarize trends from temporal graph data and change history",
}


class LAYAEngine:
    """Local AI Yield Augmentation engine.

    Uses a local LLM when available, otherwise falls back to structured
    graph analysis with deterministic summaries.
    """

    def __init__(self, store: GraphStore, model_provider: Any = None) -> None:
        self._store = store
        self._model = model_provider

    @property
    def capabilities(self) -> dict[str, str]:
        return dict(CAPABILITIES)

    def analyze(
        self,
        question: str,
        capability: str = "entity_explanation",
        context_ids: list[str] | None = None,
    ) -> LAYAResult:
        if capability not in CAPABILITIES:
            return LAYAResult(
                answer=f"Unknown capability: {capability}",
                capability=capability,
                confidence=0.0,
            )

        context = self._gather_context(context_ids or [])

        if self._model and getattr(self._model, "available", False):
            return self._llm_analyze(question, capability, context)
        return self._fallback_analyze(question, capability, context)

    def _gather_context(self, canonical_ids: list[str]) -> list[dict]:
        context = []
        for cid in canonical_ids:
            vertex = self._store.get_vertex_by_canonical_id(cid)
            if vertex:
                neighbors = []
                seen_neighbor_ids: set[str] = set()
                for edges, endpoint in (
                    (self._store.edges_from(vertex["vid"], limit=20), "in_v"),
                    (self._store.edges_to(vertex["vid"], limit=20), "out_v"),
                ):
                    for edge in edges:
                        neighbor_id = edge.get(endpoint)
                        if (
                            not isinstance(neighbor_id, str)
                            or neighbor_id == vertex["vid"]
                            or neighbor_id in seen_neighbor_ids
                        ):
                            continue
                        neighbor = self._store.get_vertex(neighbor_id)
                        if neighbor is None:
                            continue
                        seen_neighbor_ids.add(neighbor_id)
                        neighbors.append(neighbor)
                        if len(neighbors) == 20:
                            break
                    if len(neighbors) == 20:
                        break
                context.append({
                    "entity": vertex,
                    "neighbors": neighbors,
                })
        return context

    def _llm_analyze(
        self, question: str, capability: str, context: list[dict]
    ) -> LAYAResult:
        context_text = self._format_context(context)
        system_prompt = (
            f"You are an enterprise knowledge analyst. Capability: {CAPABILITIES[capability]}. "
            "Provide a structured, evidence-backed answer. Cite entity canonical_ids as evidence. "
            "If the context is insufficient, say so rather than speculating."
        )
        user_prompt = f"Question: {question}\n\nGraph context:\n{context_text}"

        try:
            response = self._model.generate(
                system_prompt, user_prompt, temperature=0, max_tokens=1024
            )
            evidence_refs = [
                e["entity"]["canonical_id"]
                for e in context
                if "canonical_id" in e.get("entity", {})
            ]
            base_conf = 0.7
            if evidence_refs:
                base_conf = min(0.95, 0.7 + 0.05 * len(evidence_refs))
            return LAYAResult(
                answer=response.content,
                capability=capability,
                confidence=round(base_conf, 3),
                evidence_refs=evidence_refs,
                model_used=response.model,
                fallback=False,
            )
        except Exception:  # noqa: BLE001 - resilient fallback must not fail the caller
            return self._fallback_analyze(question, capability, context)

    def _fallback_analyze(
        self, question: str, capability: str, context: list[dict]
    ) -> LAYAResult:
        if not context:
            return LAYAResult(
                answer=f"No graph context available to analyze: {question}",
                capability=capability,
                confidence=0.1,
                fallback=True,
            )

        summary_parts = []
        evidence_refs = []
        for entry in context:
            entity = entry["entity"]
            label = entity.get("label", "Unknown")
            name = entity.get("name", entity.get("summary", entity.get("canonical_id", "")))
            cid = entity.get("canonical_id", "")
            evidence_refs.append(cid)
            neighbor_labels = {}
            for n in entry.get("neighbors", []):
                nl = n.get("label", "Unknown")
                neighbor_labels[nl] = neighbor_labels.get(nl, 0) + 1
            neighbor_summary = ", ".join(
                f"{count} {lab}" for lab, count in sorted(neighbor_labels.items())
            )
            summary_parts.append(
                f"{label} '{name}' ({cid}): connected to {neighbor_summary or 'no neighbors'}"
            )

        answer = (
            f"Structured analysis ({CAPABILITIES[capability]}):\n\n"
            + "\n".join(f"- {part}" for part in summary_parts)
        )

        neighbor_count = sum(len(e.get("neighbors", [])) for e in context)
        conf = min(0.75, 0.3 + 0.1 * len(context) + 0.02 * neighbor_count)
        return LAYAResult(
            answer=answer,
            capability=capability,
            confidence=round(conf, 3),
            evidence_refs=evidence_refs,
            fallback=True,
            metadata={"entities_analyzed": len(context)},
        )

    def _format_context(self, context: list[dict]) -> str:
        parts = []
        for entry in context:
            entity = entry["entity"]
            parts.append(
                f"[{entity.get('label', '?')}] {entity.get('canonical_id', '?')}: "
                f"{entity.get('name', entity.get('summary', ''))}"
            )
            for n in entry.get("neighbors", [])[:5]:
                parts.append(f"  -> [{n.get('label', '?')}] {n.get('canonical_id', '?')}")
        return "\n".join(parts)

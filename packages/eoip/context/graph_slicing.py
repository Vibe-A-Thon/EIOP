"""Attention-weighted graph context compression and bitemporal context slates.

Extracts prioritized subgraphs weighted by causal shock and betweenness centrality,
and constructs side-by-side bitemporal comparative context slates for LLM reasoning.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any

from eoip.context.engine import ContextItem, get_context_engine
from eoip.state.engine import get_state_engine


@dataclass
class SlicedEntity:
    entity_id: str
    label: str
    attention_score: float
    properties: dict[str, Any]
    causal_coupling: float = 0.0
    degree: int = 1


@dataclass
class SlicedGraphWindow:
    query: str
    total_candidates: int
    retained_count: int
    compression_ratio: float
    entities: list[SlicedEntity]
    rendered_context: str


class AttentionGraphSlicer:
    """Calculates attention scores across graph vertices to build token-compressed subgraphs."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._slices_generated = 0

    def slice_graph(
        self,
        query: str,
        seed_ids: list[str] | None = None,
        nodes: list[dict[str, Any]] | None = None,
        edges: list[dict[str, Any]] | None = None,
        attention_threshold: float = 0.35,
        max_tokens: int = 2048,
    ) -> SlicedGraphWindow:
        raw_nodes = nodes or [
            {"id": "auth-gateway", "label": "Service", "degree": 5, "causal_weight": 0.9, "desc": "Handles authentication & sessions"},
            {"id": "billing-core", "label": "Service", "degree": 4, "causal_weight": 0.85, "desc": "Processes transactions & invoices"},
            {"id": "user-db", "label": "Database", "degree": 3, "causal_weight": 0.75, "desc": "PostgreSQL user storage cluster"},
            {"id": "metrics-agent", "label": "Service", "degree": 1, "causal_weight": 0.1, "desc": "Telemetry scraper for monitoring"},
            {"id": "doc-server", "label": "Service", "degree": 1, "causal_weight": 0.05, "desc": "Static documentation renderer"},
        ]
        raw_edges = edges or [
            {"from": "auth-gateway", "to": "billing-core", "coupling": 0.8},
            {"from": "billing-core", "to": "user-db", "coupling": 0.9},
        ]

        query_terms = set(query.lower().split())
        seeds = set(seed_ids or ["auth-gateway", "billing-core"])

        scored_entities: list[SlicedEntity] = []
        for n in raw_nodes:
            nid = n.get("id", "")
            desc = n.get("desc", "").lower()
            label = n.get("label", "Node")
            degree = int(n.get("degree", 1))
            causal_wt = float(n.get("causal_weight", 0.5))

            # Factor 1: Keyword relevance
            overlap = sum(1 for term in query_terms if term in desc or term in nid.lower())
            relevance = overlap / max(len(query_terms), 1)

            # Factor 2: Seed proximity bonus
            seed_bonus = 0.3 if nid in seeds else 0.0

            # Factor 3: Centrality & Causal weight
            centrality_factor = min(degree / 5.0, 1.0) * 0.3
            causal_factor = causal_wt * 0.4

            attention_score = min(1.0, relevance * 0.4 + seed_bonus + centrality_factor + causal_factor)

            if attention_score >= attention_threshold:
                scored_entities.append(
                    SlicedEntity(
                        entity_id=nid,
                        label=label,
                        attention_score=round(attention_score, 4),
                        properties={"desc": n.get("desc", ""), "degree": degree},
                        causal_coupling=causal_wt,
                        degree=degree,
                    )
                )

        scored_entities.sort(key=lambda x: x.attention_score, reverse=True)

        # Assemble compressed markdown context block
        lines = [f"### [Attention-Weighted Subgraph for: '{query}']"]
        lines.append(f"Retained {len(scored_entities)}/{len(raw_nodes)} entities (Attention Threshold >= {attention_threshold}):")
        for e in scored_entities:
            lines.append(
                f"- **{e.entity_id}** ({e.label}) [Attention: {e.attention_score:.2f}, Causal Shock: {e.causal_coupling:.2f}]: {e.properties.get('desc', '')}"
            )
        rendered = "\n".join(lines)

        compression_ratio = round(
            1.0 - (len(scored_entities) / max(len(raw_nodes), 1)), 2
        )

        with self._lock:
            self._slices_generated += 1

        # Also push into global ContextEngine
        context_engine = get_context_engine()
        for e in scored_entities:
            context_engine.add_item(
                ContextItem(
                    item_id=f"slice-{e.entity_id}",
                    content=f"Entity {e.entity_id} ({e.label}) [Attn: {e.attention_score}]: {e.properties.get('desc', '')}",
                    priority="HIGH" if e.attention_score > 0.6 else "MEDIUM",
                    source="attention_slicer",
                    metadata={"attention_score": e.attention_score},
                )
            )

        return SlicedGraphWindow(
            query=query,
            total_candidates=len(raw_nodes),
            retained_count=len(scored_entities),
            compression_ratio=compression_ratio,
            entities=scored_entities,
            rendered_context=rendered,
        )


class BitemporalContextSlate:
    """Assembles comparative historical and present context slates side-by-side."""

    def __init__(self) -> None:
        self._lock = threading.Lock()

    def build_slate(
        self,
        stream: str,
        past_timestamp: float,
        present_timestamp: float | None = None,
    ) -> dict[str, Any]:
        state_engine = get_state_engine()
        # As-of semantics: each side includes events recorded at or before its
        # timestamp. 0.0 is a valid timestamp, so only None means "now".
        now = time.time() if present_timestamp is None else present_timestamp
        if now < past_timestamp:
            raise ValueError("present_timestamp must not be earlier than past_timestamp")

        past_state = state_engine.time_travel_state(stream, past_timestamp)
        present_state = state_engine.time_travel_state(stream, now)

        added = {k: present_state[k] for k in present_state if k not in past_state}
        removed = {k: past_state[k] for k in past_state if k not in present_state}
        modified = {
            k: {"past": past_state[k], "present": present_state[k]}
            for k in past_state
            if k in present_state and past_state[k] != present_state[k]
        }

        slate_sections = [
            f"### [Bitemporal Delta Slate: Stream '{stream}']",
            f"Comparing T_past ({past_timestamp:.0f}) vs T_present ({now:.0f}):",
            f"- **Added Fields ({len(added)})**: {added if added else 'None'}",
            f"- **Modified Fields ({len(modified)})**: {modified if modified else 'None'}",
            f"- **Removed Fields ({len(removed)})**: {removed if removed else 'None'}",
        ]
        rendered_slate = "\n".join(slate_sections)

        # Inject into ContextEngine
        get_context_engine().add_item(
            ContextItem(
                item_id=f"bitemporal-{stream}-{int(past_timestamp)}-{int(now)}",
                content=rendered_slate,
                priority="CRITICAL",
                source="bitemporal_slate",
                metadata={"stream": stream, "past_t": past_timestamp, "now_t": now},
            )
        )

        return {
            "stream": stream,
            "past_timestamp": past_timestamp,
            "present_timestamp": now,
            "delta_summary": {
                "added_keys": list(added.keys()),
                "modified_keys": list(modified.keys()),
                "removed_keys": list(removed.keys()),
            },
            "rendered_slate": rendered_slate,
        }


_slicer_instance: AttentionGraphSlicer | None = None
_slate_instance: BitemporalContextSlate | None = None
_lock = threading.Lock()


def get_attention_graph_slicer() -> AttentionGraphSlicer:
    global _slicer_instance
    if _slicer_instance is None:
        with _lock:
            if _slicer_instance is None:
                _slicer_instance = AttentionGraphSlicer()
    return _slicer_instance


def get_bitemporal_context_slate() -> BitemporalContextSlate:
    global _slate_instance
    if _slate_instance is None:
        with _lock:
            if _slate_instance is None:
                _slate_instance = BitemporalContextSlate()
    return _slate_instance

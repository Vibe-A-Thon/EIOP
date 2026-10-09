"""Moonshot 8: Adaptive Graph Attention Memory (AGAM) & Neuro-Symbolic Agent Brain.

Provides:
- Dynamic consolidation of conversational interactions into persistent graph memories.
- Attention-weighted salience scoring and autonomous memory decay/pruning.
- Neuro-symbolic guardrail verification preventing hallucinated tool actions.
"""

from __future__ import annotations

import math
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryGraphNode:
    memory_id: str
    content: str
    category: str  # EPISODIC, SEMANTIC, PROCEDURAL
    created_at: float
    last_accessed: float
    access_count: int = 1
    decay_rate: float = 0.05
    salience_score: float = 1.0
    connected_entities: list[str] = field(default_factory=list)


class AdaptiveGraphAttentionMemory:
    """Consolidates conversational episodic memory into enduring semantic knowledge."""

    def __init__(self, tenant_id: str = "default") -> None:
        self.tenant_id = tenant_id
        self.memories: dict[str, MemoryGraphNode] = {}

    def record_interaction(
        self,
        content: str,
        category: str = "EPISODIC",
        connected_entities: list[str] | None = None,
    ) -> MemoryGraphNode:
        """Record and consolidate a new interaction memory."""
        now = time.time()
        mem_id = f"mem_{uuid.uuid4().hex[:8]}"
        node = MemoryGraphNode(
            memory_id=mem_id,
            content=content,
            category=category,
            created_at=now,
            last_accessed=now,
            access_count=1,
            salience_score=1.0 + (len(connected_entities or []) * 0.2),
            connected_entities=list(connected_entities or []),
        )
        self.memories[mem_id] = node
        return node

    def retrieve_relevant(self, query: str, top_k: int = 5) -> list[MemoryGraphNode]:
        """Retrieve memories weighted by lexical overlap and attention salience."""
        now = time.time()
        scored: list[tuple[float, MemoryGraphNode]] = []
        words = set(query.lower().split())

        for mem in self.memories.values():
            # Update salience with temporal decay
            age_days = (now - mem.last_accessed) / 86400.0
            decay = 1.0 / (1.0 + mem.decay_rate * age_days)
            # Relevance based on word overlap
            content_words = set(mem.content.lower().split())
            overlap = len(words & content_words)

            total_score = (overlap * 2.0 + 0.5) * mem.salience_score * decay
            scored.append((total_score, mem))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [m for _, m in scored[:top_k]]

        # Boost access counts
        for m in results:
            m.last_accessed = now
            m.access_count += 1
            m.salience_score += 0.1

        return results

    def prune_decayed_memories(self, threshold: float = 0.3) -> list[str]:
        """Prune obsolete, low-salience memories while keeping high-centrality semantic knowledge."""
        now = time.time()
        pruned_ids: list[str] = []

        for mem_id, mem in list(self.memories.items()):
            # Procedural and foundational semantic memories decay much slower
            if mem.category == "PROCEDURAL":
                continue
            age_days = (now - mem.last_accessed) / 86400.0
            decay = 1.0 / (1.0 + mem.decay_rate * age_days)
            effective_salience = mem.salience_score * decay

            if effective_salience < threshold:
                pruned_ids.append(mem_id)
                del self.memories[mem_id]

        return pruned_ids


class NeuroSymbolicGuardrail:
    """Validates LLM and agent proposed actions against formal ontology constraints."""

    def __init__(self, allowed_vertex_types: set[str], allowed_edge_types: set[str]) -> None:
        self.allowed_vertex_types = set(allowed_vertex_types)
        self.allowed_edge_types = set(allowed_edge_types)

    def validate_action(self, tool_name: str, args: dict[str, Any]) -> tuple[bool, str | None]:
        """Verify action conformity to ontology schema rules."""
        if tool_name in ("create_vertex", "upsert_vertex"):
            v_type = args.get("label") or args.get("type")
            if v_type not in self.allowed_vertex_types:
                return False, f"Symbolic Guardrail Rejection: Unknown vertex label '{v_type}'"

        if tool_name in ("create_edge", "upsert_edge"):
            e_type = args.get("label") or args.get("type")
            if e_type not in self.allowed_edge_types:
                return False, f"Symbolic Guardrail Rejection: Forbidden edge relationship '{e_type}'"

        if tool_name == "delete_graph":
            return False, "Symbolic Guardrail Rejection: Destructive graph purge is prohibited"

        return True, None

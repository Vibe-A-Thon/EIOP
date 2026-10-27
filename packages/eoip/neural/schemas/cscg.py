"""
Clone-Structured Cognitive Graphs (CSCG) & Relational Schemas (NS-P2, T-NS-005).
Implements polysemous clone state splitting and relational transition graphs
for zero-shot schema rebinding and structural abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class CSCGCloneState:
    clone_id: str
    base_symbol: str
    context_tag: str
    emission_prob: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CSCGNode:
    symbol: str
    clones: List[CSCGCloneState] = field(default_factory=list)

    def add_clone(self, context_tag: str, emission_prob: float = 1.0, properties: Optional[Dict[str, Any]] = None) -> CSCGCloneState:
        clone_id = f"{self.symbol}::clone_{len(self.clones) + 1}_{context_tag}"
        clone = CSCGCloneState(
            clone_id=clone_id,
            base_symbol=self.symbol,
            context_tag=context_tag,
            emission_prob=emission_prob,
            properties=properties or {},
        )
        self.clones.append(clone)
        return clone


class CSCGGraph:
    """
    Clone-Structured Cognitive Graph representing high-order relational schemas.
    Allows disambiguating identical observation tokens occurring in different relational contexts.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, CSCGNode] = {}
        self.transitions: Dict[Tuple[str, str], float] = {}  # (from_clone_id, to_clone_id) -> probability

    def get_or_create_node(self, symbol: str) -> CSCGNode:
        if symbol not in self.nodes:
            self.nodes[symbol] = CSCGNode(symbol=symbol)
        return self.nodes[symbol]

    def split_clone(self, symbol: str, context_tag: str, properties: Optional[Dict[str, Any]] = None) -> CSCGCloneState:
        """Splits an observation node into a context-specialized clone state."""
        node = self.get_or_create_node(symbol)
        return node.add_clone(context_tag=context_tag, properties=properties)

    def set_transition(self, from_clone_id: str, to_clone_id: str, probability: float) -> None:
        self.transitions[(from_clone_id, to_clone_id)] = max(0.0, min(1.0, probability))

    def rebind_schema(self, source_context: str, target_context: str, symbol_mapping: Dict[str, str]) -> CSCGGraph:
        """
        Executes zero-shot relational schema rebinding:
        Maps structural transition topology from source_context to target_context.
        """
        rebound = CSCGGraph()
        for (u_clone, v_clone), prob in self.transitions.items():
            u_base = u_clone.split("::")[0]
            v_base = v_clone.split("::")[0]

            new_u_symbol = symbol_mapping.get(u_base, u_base)
            new_v_symbol = symbol_mapping.get(v_base, v_base)

            new_u_clone = rebound.split_clone(new_u_symbol, context_tag=target_context)
            new_v_clone = rebound.split_clone(new_v_symbol, context_tag=target_context)

            rebound.set_transition(new_u_clone.clone_id, new_v_clone.clone_id, prob)

        return rebound

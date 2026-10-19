"""
Control Flow Graph (CFG) & Cyclomatic Complexity Builder (REVA-NB-003, T-ENH-010).
Constructs basic-block graph topology and computes McCabe cyclomatic complexity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from reva.extract.native.disasm import BasicBlock


@dataclass
class CFGEdge:
    source_addr: int
    target_addr: int
    edge_type: str  # "FALLTHROUGH", "CONDITIONAL_BRANCH", "UNCONDITIONAL_JUMP", "CALL"


@dataclass
class ControlFlowGraph:
    entry_address: int
    blocks: Dict[int, BasicBlock] = field(default_factory=dict)
    edges: List[CFGEdge] = field(default_factory=list)
    cyclomatic_complexity: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_address": hex(self.entry_address),
            "blocks_count": len(self.blocks),
            "edges_count": len(self.edges),
            "cyclomatic_complexity": self.cyclomatic_complexity,
            "blocks": [
                {
                    "start": hex(b.start_address),
                    "end": hex(b.end_address),
                    "instructions_count": b.instruction_count,
                    "terminator": b.terminator_type,
                    "successors": [hex(s) for s in b.successors],
                }
                for b in self.blocks.values()
            ],
            "edges": [
                {
                    "source": hex(e.source_addr),
                    "target": hex(e.target_addr),
                    "type": e.edge_type,
                }
                for e in self.edges
            ],
        }


class CFGBuilder:
    """
    Builds Control Flow Graphs from basic blocks and computes topological metrics.
    """

    def build_cfg(self, blocks: List[BasicBlock], entry_address: Optional[int] = None) -> ControlFlowGraph:
        if not blocks:
            return ControlFlowGraph(entry_address=0)

        entry = entry_address if entry_address is not None else blocks[0].start_address
        block_map = {b.start_address: b for b in blocks}
        edges: List[CFGEdge] = []

        for b in blocks:
            for succ in b.successors:
                edge_type = "FALLTHROUGH"
                if b.terminator_type == "jcc":
                    edge_type = "CONDITIONAL_BRANCH"
                elif b.terminator_type == "jmp":
                    edge_type = "UNCONDITIONAL_JUMP"
                elif b.terminator_type == "call":
                    edge_type = "CALL"

                edges.append(CFGEdge(
                    source_addr=b.start_address,
                    target_addr=succ,
                    edge_type=edge_type,
                ))

        # McCabe's Cyclomatic Complexity: M = E - N + 2P
        n_vertices = len(blocks)
        n_edges = len(edges)
        p_components = 1
        complexity = max(1, n_edges - n_vertices + 2 * p_components)

        return ControlFlowGraph(
            entry_address=entry,
            blocks=block_map,
            edges=edges,
            cyclomatic_complexity=complexity,
        )

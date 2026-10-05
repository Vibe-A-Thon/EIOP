"""What-if simulation engine: simulate entity removal/isolation without mutation.

Extended (G2-T0910..0912) with structured mutation plans, user-confirmation
summaries, and affected-entity categorisation.
"""

from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.simulation import Mutation, SimulationWorkspace
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS


@dataclass
class WhatIfResult:
    canonical_id: str
    action: str
    broken_edges: int = 0
    affected_neighbors: int = 0
    orphaned_entities: int = 0
    broken_paths: int = 0
    centrality_changes: list[dict[str, Any]] = field(default_factory=list)
    component_split: bool = False
    new_components: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "action": self.action,
            "broken_edges": self.broken_edges,
            "affected_neighbors": self.affected_neighbors,
            "orphaned_entities": self.orphaned_entities,
            "broken_paths": self.broken_paths,
            "centrality_changes": self.centrality_changes,
            "component_split": self.component_split,
            "new_components": self.new_components,
        }


class WhatIfEngine:
    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def simulate_removal(self, canonical_id: str) -> WhatIfResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return WhatIfResult(canonical_id=canonical_id, action="remove")

        out_edges = self._store.edges_from(root["vid"])
        in_edges = self._store.edges_to(root["vid"])
        broken_edges = len(out_edges) + len(in_edges)

        neighbors: set[str] = set()
        neighbor_vids: set[str] = set()
        for edge in out_edges:
            v = self._store.get_vertex(edge["in_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
                neighbor_vids.add(edge["in_v"])
        for edge in in_edges:
            v = self._store.get_vertex(edge["out_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
                neighbor_vids.add(edge["out_v"])

        orphaned = 0
        for vid in neighbor_vids:
            other_out = [e for e in self._store.edges_from(vid) if e["in_v"] != root["vid"]]
            other_in = [e for e in self._store.edges_to(vid) if e["out_v"] != root["vid"]]
            if not other_out and not other_in:
                orphaned += 1

        # Partition once instead of repeating remote BFS for every neighbor pair.
        components = self._neighbor_components(root["vid"], neighbor_vids)
        neighbor_count = sum(components)
        broken_paths = (neighbor_count ** 2 - sum(size ** 2 for size in components)) // 2
        component_split = len(components) > 1
        new_components = len(components) if component_split else 0

        centrality_changes = self._compute_centrality_changes(
            canonical_id, neighbors
        )

        return WhatIfResult(
            canonical_id=canonical_id,
            action="remove",
            broken_edges=broken_edges,
            affected_neighbors=len(neighbors),
            orphaned_entities=orphaned,
            broken_paths=broken_paths,
            centrality_changes=centrality_changes,
            component_split=component_split,
            new_components=new_components,
        )

    def simulate_isolation(self, canonical_id: str) -> WhatIfResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return WhatIfResult(canonical_id=canonical_id, action="isolate")

        out_edges = self._store.edges_from(root["vid"])
        in_edges = self._store.edges_to(root["vid"])

        neighbors: set[str] = set()
        for edge in out_edges:
            v = self._store.get_vertex(edge["in_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])
        for edge in in_edges:
            v = self._store.get_vertex(edge["out_v"])
            if v:
                neighbors.add(v["properties"]["canonical_id"])

        return WhatIfResult(
            canonical_id=canonical_id,
            action="isolate",
            broken_edges=len(out_edges) + len(in_edges),
            affected_neighbors=len(neighbors),
            orphaned_entities=0,
            broken_paths=0,
            component_split=False,
            new_components=0,
        )

    def _neighbor_components(self, removed_vid: str, neighbor_vids: set[str]) -> list[int]:
        """Count root neighbors in each remaining weakly connected component."""
        remaining = neighbor_vids - {removed_vid}
        visited = {removed_vid}
        components: list[int] = []
        while remaining:
            if len(remaining) == 1:
                components.append(1)
                break
            start = next(iter(remaining))
            visited.add(start)
            queue = deque([start])
            size = 0
            while queue and remaining:
                vid = queue.popleft()
                if vid in remaining:
                    remaining.remove(vid)
                    size += 1
                for edge in self._store.edges_from(vid):
                    nxt = edge["in_v"]
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
                for edge in self._store.edges_to(vid):
                    nxt = edge["out_v"]
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
            components.append(size)
        return components

    def _compute_centrality_changes(
        self, removed_cid: str, neighbors: set[str]
    ) -> list[dict[str, Any]]:
        if not neighbors:
            return []
        from eoip.graph.metrics import GraphMetricsEngine
        engine = GraphMetricsEngine(self._store)
        before = engine.centrality(list(neighbors))
        changes = []
        for cid, metrics in before.items():
            changes.append({
                "canonical_id": cid,
                "degree_before": metrics.degree,
                "degree_after": max(0, metrics.degree - 1),
            })
        return changes


# ---------------------------------------------------------------------------
# G2-T0910..0912: Structured what-if mutation plans
# ---------------------------------------------------------------------------

@dataclass
class MutationPlan:
    intent: str
    mutations: list[Mutation] = field(default_factory=list)
    description: str = ""
    confirmed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "description": self.description,
            "mutations": [m.to_dict() for m in self.mutations],
            "mutation_count": len(self.mutations),
            "confirmed": self.confirmed,
        }


_INTENT_PATTERNS: list[tuple[str, str, str]] = [
    (r"remove\s+(\w+)\s+(.+)", "remove_vertex", "Remove {label} {target}"),
    (r"delete\s+(\w+)\s+(.+)", "remove_vertex", "Delete {label} {target}"),
    (r"add\s+(\w+)\s+named\s+(.+)", "add_vertex", "Add {label} named {target}"),
    (r"connect\s+(.+?)\s+to\s+(.+?)\s+via\s+(\w+)", "add_edge", "Connect {src} to {tgt} via {edge}"),
    (r"disconnect\s+(.+?)\s+from\s+(.+)", "remove_edge_between", "Disconnect {src} from {tgt}"),
    (r"modify\s+(.+?)\s+set\s+(.+)", "modify_vertex", "Modify {target} properties"),
]


def parse_whatif_intent(intent: str) -> MutationPlan:
    """Parse a structured or semi-natural-language intent into a mutation plan."""
    plan = MutationPlan(intent=intent)
    text = intent.strip()

    for pattern, kind, desc_tpl in _INTENT_PATTERNS:
        m = re.match(pattern, text, re.IGNORECASE)
        if not m:
            continue
        groups = m.groups()

        if kind == "remove_vertex":
            label, target = groups[0], groups[1]
            plan.mutations.append(Mutation(kind="remove_vertex", label=label, target_id=target.strip()))
            plan.description = desc_tpl.format(label=label, target=target.strip())
        elif kind == "add_vertex":
            label, name = groups[0], groups[1]
            plan.mutations.append(Mutation(
                kind="add_vertex", label=label,
                properties={"canonical_id": f"urn:sim:{name.strip().replace(' ', '-').lower()}", "name": name.strip()},
            ))
            plan.description = desc_tpl.format(label=label, target=name.strip())
        elif kind == "add_edge":
            src, tgt, edge = groups[0].strip(), groups[1].strip(), groups[2].strip()
            plan.mutations.append(Mutation(kind="add_edge", label=edge, out_v=src, in_v=tgt))
            plan.description = desc_tpl.format(src=src, tgt=tgt, edge=edge)
        elif kind == "remove_edge_between":
            src, tgt = groups[0].strip(), groups[1].strip()
            plan.mutations.append(Mutation(kind="remove_edge_between", out_v=src, in_v=tgt))
            plan.description = desc_tpl.format(src=src, tgt=tgt)
        elif kind == "modify_vertex":
            target, props_str = groups[0].strip(), groups[1].strip()
            props: dict[str, Any] = {}
            for pair in props_str.split(","):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    props[k.strip()] = v.strip()
            plan.mutations.append(Mutation(kind="modify_vertex", target_id=target, properties=props))
            plan.description = desc_tpl.format(target=target)
        break

    if not plan.mutations:
        plan.description = f"Unrecognised intent: {text}"

    return plan


def confirm_scenario(plan: MutationPlan) -> dict[str, Any]:
    """Return a confirmation summary requiring user approval before execution."""
    summary: dict[str, Any] = {
        "intent": plan.intent,
        "description": plan.description,
        "mutations": [m.to_dict() for m in plan.mutations],
        "mutation_count": len(plan.mutations),
        "requires_confirmation": True,
    }
    adds = sum(1 for m in plan.mutations if m.kind.startswith("add"))
    removes = sum(1 for m in plan.mutations if m.kind.startswith("remove"))
    modifies = sum(1 for m in plan.mutations if m.kind == "modify_vertex")
    summary["breakdown"] = {"additions": adds, "removals": removes, "modifications": modifies}
    return summary


def execute_scenario(store: GraphStore, plan: MutationPlan) -> dict[str, Any]:
    """Execute a confirmed mutation plan against a simulation workspace.

    Returns affected entities grouped by category and graph path.
    """
    workspace = SimulationWorkspace(store)
    sim_id = workspace.create(description=plan.intent)

    results = []
    for mut in plan.mutations:
        if mut.kind == "remove_edge_between":
            overlay = workspace.get_overlay(sim_id)
            if overlay:
                edges = overlay.find_edges(limit=10_000)
                for e in edges:
                    src = overlay.get_vertex(e["out_v"])
                    tgt = overlay.get_vertex(e["in_v"])
                    if (
                        src
                        and tgt
                        and src["canonical_id"] == mut.out_v
                        and tgt["canonical_id"] == mut.in_v
                    ):
                        results.append(workspace.apply_mutation(sim_id, Mutation(
                            kind="remove_edge", target_id=e["eid"],
                        )))
        else:
            results.append(workspace.apply_mutation(sim_id, mut))

    analysis = workspace.run_analysis(sim_id, "impact")

    overlay = workspace.get_overlay(sim_id)
    affected_by_category: dict[str, list[str]] = {}
    if overlay:
        for cid in analysis.get("affected_entities", []):
            v = overlay.get_vertex_by_canonical_id(cid)
            if v:
                domain = VERTEX_LABELS.get(v["label"], ("UNKNOWN",))[0]
                affected_by_category.setdefault(domain, []).append(cid)

    return {
        "simulation_id": sim_id,
        "intent": plan.intent,
        "mutation_results": results,
        "analysis": analysis,
        "affected_by_category": affected_by_category,
        "manifest": workspace.get_manifest(sim_id),
    }

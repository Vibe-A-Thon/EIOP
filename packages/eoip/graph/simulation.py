"""Simulation workspace for counterfactual twin analysis (G2-T0901..0906).

Provides an overlay-based simulation engine: hypothetical mutations are applied
on top of an immutable base graph snapshot, and existing analysis functions
(conformance, knowledge debt, impact) can run against the combined view.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from eoip.graph.store import GraphStore


@dataclass
class Mutation:
    kind: str  # add_vertex, remove_vertex, add_edge, remove_edge, modify_vertex
    label: str = ""
    target_id: str = ""
    properties: dict[str, Any] = field(default_factory=dict)
    out_v: str = ""
    in_v: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind, "label": self.label, "target_id": self.target_id,
            "properties": self.properties, "out_v": self.out_v, "in_v": self.in_v,
        }


@dataclass
class SimulationManifest:
    simulation_id: str
    created_at: str
    base_snapshot: str
    mutations: list[dict[str, Any]]
    results: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "created_at": self.created_at,
            "base_snapshot": self.base_snapshot,
            "mutations": self.mutations,
            "results": self.results,
        }


class SimulationOverlay:
    """Overlay on a base GraphStore — provides combined query without mutating the base."""

    def __init__(self, base: GraphStore) -> None:
        self._base = base
        self._added_vertices: dict[str, dict] = {}
        self._removed_vertex_vids: set[str] = set()
        self._added_edges: dict[str, dict] = {}
        self._removed_edge_eids: set[str] = set()
        self._modified_props: dict[str, dict[str, Any]] = {}

    def add_vertex(self, label: str, properties: dict[str, Any]) -> dict:
        cid = properties.get("canonical_id", f"sim:{uuid4().hex[:12]}")
        vid = f"sim-v-{uuid4().hex[:12]}"
        record = {
            "vid": vid, "label": label, "canonical_id": cid,
            "properties": {**properties, "canonical_id": cid},
        }
        self._added_vertices[vid] = record
        return record

    def remove_vertex(self, canonical_id: str) -> bool:
        v = self.get_vertex_by_canonical_id(canonical_id)
        if not v:
            return False
        self._removed_vertex_vids.add(v["vid"])
        return True

    def add_edge(self, label: str, out_cid: str, in_cid: str,
                 properties: dict[str, Any] | None = None) -> dict | None:
        out_v = self.get_vertex_by_canonical_id(out_cid)
        in_v = self.get_vertex_by_canonical_id(in_cid)
        if not out_v or not in_v:
            return None
        props = properties or {}
        eid = f"sim-e-{uuid4().hex[:12]}"
        record = {
            "eid": eid, "label": label,
            "out_v": out_v["vid"], "in_v": in_v["vid"],
            "out_cid": out_cid, "in_cid": in_cid,
            "properties": {**props, "edge_key": eid},
        }
        self._added_edges[eid] = record
        return record

    def remove_edge_by_eid(self, eid: str) -> bool:
        if eid in self._added_edges:
            self._removed_edge_eids.add(eid)
            return True
        e = self._base.get_edge(eid)
        if e:
            self._removed_edge_eids.add(eid)
            return True
        return False

    def modify_vertex(self, canonical_id: str, properties: dict[str, Any]) -> bool:
        v = self.get_vertex_by_canonical_id(canonical_id)
        if not v:
            return False
        self._modified_props.setdefault(v["vid"], {}).update(properties)
        return True

    def _apply_mods(self, record: dict) -> dict:
        mods = self._modified_props.get(record["vid"])
        if mods:
            record = copy.deepcopy(record)
            record["properties"].update(mods)
        return record

    # --- Read interface (duck-typed GraphStore) ---

    def get_vertex_by_canonical_id(self, cid: str) -> dict | None:
        for v in self._added_vertices.values():
            if v["canonical_id"] == cid and v["vid"] not in self._removed_vertex_vids:
                return self._apply_mods(copy.deepcopy(v))
        base_v = self._base.get_vertex_by_canonical_id(cid)
        if base_v and base_v["vid"] not in self._removed_vertex_vids:
            return self._apply_mods(copy.deepcopy(base_v))
        return None

    def get_vertex(self, vid: str) -> dict | None:
        if vid in self._removed_vertex_vids:
            return None
        if vid in self._added_vertices:
            return self._apply_mods(copy.deepcopy(self._added_vertices[vid]))
        base_v = self._base.get_vertex(vid)
        if base_v:
            return self._apply_mods(copy.deepcopy(base_v))
        return None

    def find_vertices(self, label: str | None = None, limit: int = 10_000,
                      **_kw: Any) -> list[dict]:
        results: list[dict] = []
        seen: set[str] = set()
        for v in self._added_vertices.values():
            if v["vid"] in self._removed_vertex_vids:
                continue
            if label and v["label"] != label:
                continue
            results.append(self._apply_mods(copy.deepcopy(v)))
            seen.add(v["vid"])
            if len(results) >= limit:
                return results
        for v in self._base.find_vertices(label=label, limit=limit * 2):
            if v["vid"] in self._removed_vertex_vids or v["vid"] in seen:
                continue
            results.append(self._apply_mods(copy.deepcopy(v)))
            if len(results) >= limit:
                break
        return results

    def find_edges(self, out_v: str | None = None, in_v: str | None = None,
                   label: str | None = None, limit: int = 1000,
                   **_kw: Any) -> list[dict]:
        results: list[dict] = []
        seen: set[str] = set()
        for e in self._added_edges.values():
            if not self._edge_visible(e, out_v, in_v, label):
                continue
            results.append(e)
            seen.add(e["eid"])
            if len(results) >= limit:
                return results
        for e in self._base.find_edges(out_v=out_v, in_v=in_v, label=label, limit=limit * 2):
            if e["eid"] in self._removed_edge_eids or e["eid"] in seen:
                continue
            if e["out_v"] in self._removed_vertex_vids or e["in_v"] in self._removed_vertex_vids:
                continue
            results.append(e)
            if len(results) >= limit:
                break
        return results

    def edges_from(self, vid: str, labels: list[str] | None = None,
                   limit: int = 500, **_kw: Any) -> list[dict]:
        results: list[dict] = []
        for e in self._added_edges.values():
            if e["eid"] in self._removed_edge_eids:
                continue
            if e["out_v"] != vid:
                continue
            if e["in_v"] in self._removed_vertex_vids:
                continue
            if labels and e["label"] not in labels:
                continue
            results.append(e)
        for e in self._base.edges_from(vid, labels=labels, limit=limit * 2):
            if e["eid"] in self._removed_edge_eids:
                continue
            if e["in_v"] in self._removed_vertex_vids:
                continue
            results.append(e)
            if len(results) >= limit:
                break
        return results

    def edges_to(self, vid: str, labels: list[str] | None = None,
                 limit: int = 500, **_kw: Any) -> list[dict]:
        results: list[dict] = []
        for e in self._added_edges.values():
            if e["eid"] in self._removed_edge_eids:
                continue
            if e["in_v"] != vid:
                continue
            if e["out_v"] in self._removed_vertex_vids:
                continue
            if labels and e["label"] not in labels:
                continue
            results.append(e)
        for e in self._base.edges_to(vid, labels=labels, limit=limit * 2):
            if e["eid"] in self._removed_edge_eids:
                continue
            if e["out_v"] in self._removed_vertex_vids:
                continue
            results.append(e)
            if len(results) >= limit:
                break
        return results

    def _edge_visible(self, e: dict, out_v: str | None, in_v: str | None,
                      label: str | None) -> bool:
        if e["eid"] in self._removed_edge_eids:
            return False
        if e["out_v"] in self._removed_vertex_vids or e["in_v"] in self._removed_vertex_vids:
            return False
        if out_v and e["out_v"] != out_v:
            return False
        if in_v and e["in_v"] != in_v:
            return False
        return not (label and e["label"] != label)

    @property
    def mutation_count(self) -> int:
        return (
            len(self._added_vertices)
            + len(self._removed_vertex_vids)
            + len(self._added_edges)
            + len(self._removed_edge_eids)
            + len(self._modified_props)
        )


class SimulationWorkspace:
    """Manages named simulation sessions on a base graph (G2-SIM-001..007)."""

    def __init__(self, base_store: GraphStore) -> None:
        self._base = base_store
        self._simulations: dict[str, SimulationOverlay] = {}
        self._manifests: dict[str, SimulationManifest] = {}

    def create(self, description: str = "") -> str:
        sim_id = f"sim-{uuid4().hex[:8]}"
        self._simulations[sim_id] = SimulationOverlay(self._base)
        vertex_count = self._base.count_vertices()
        self._manifests[sim_id] = SimulationManifest(
            simulation_id=sim_id,
            created_at=datetime.now(UTC).isoformat(),
            base_snapshot=f"{description or 'snapshot'} ({vertex_count} vertices)",
            mutations=[],
        )
        return sim_id

    def get_overlay(self, sim_id: str) -> SimulationOverlay | None:
        return self._simulations.get(sim_id)

    def apply_mutation(self, sim_id: str, mutation: Mutation) -> dict[str, Any]:
        overlay = self._simulations.get(sim_id)
        if not overlay:
            return {"error": f"Simulation {sim_id} not found"}
        result: dict[str, Any] = {"kind": mutation.kind, "success": False}

        if mutation.kind == "add_vertex":
            v = overlay.add_vertex(mutation.label, mutation.properties)
            result.update(success=True, vertex={"vid": v["vid"], "canonical_id": v["canonical_id"]})
        elif mutation.kind == "remove_vertex":
            result["success"] = overlay.remove_vertex(mutation.target_id)
        elif mutation.kind == "add_edge":
            e = overlay.add_edge(mutation.label, mutation.out_v, mutation.in_v, mutation.properties)
            result["success"] = e is not None
            if e:
                result["edge"] = {"eid": e["eid"]}
        elif mutation.kind == "remove_edge":
            result["success"] = overlay.remove_edge_by_eid(mutation.target_id)
        elif mutation.kind == "modify_vertex":
            result["success"] = overlay.modify_vertex(mutation.target_id, mutation.properties)

        self._manifests[sim_id].mutations.append(mutation.to_dict())
        return result

    def apply_mutations(self, sim_id: str, mutations: list[Mutation]) -> list[dict[str, Any]]:
        return [self.apply_mutation(sim_id, m) for m in mutations]

    def run_analysis(self, sim_id: str, analysis_type: str = "impact") -> dict[str, Any]:
        overlay = self._simulations.get(sim_id)
        if not overlay:
            return {"error": f"Simulation {sim_id} not found"}

        base_v = self._base.count_vertices()
        base_e = self._base.count_edges()
        sim_vertices = overlay.find_vertices(limit=100_000)
        sim_edges = overlay.find_edges(limit=100_000)

        result: dict[str, Any] = {
            "simulation_id": sim_id, "analysis_type": analysis_type,
            "base": {"vertices": base_v, "edges": base_e},
            "simulated": {"vertices": len(sim_vertices), "edges": len(sim_edges)},
            "delta": {"vertices": len(sim_vertices) - base_v, "edges": len(sim_edges) - base_e},
            "mutations_applied": overlay.mutation_count,
        }

        if analysis_type == "impact":
            removed_cids: set[str] = set()
            for vid in overlay._removed_vertex_vids:
                v = self._base.get_vertex(vid)
                if v:
                    removed_cids.add(v["canonical_id"])
            affected: set[str] = set()
            for vid in overlay._removed_vertex_vids:
                for e in self._base.edges_from(vid, limit=500):
                    t = self._base.get_vertex(e["in_v"])
                    if t:
                        affected.add(t["canonical_id"])
                for e in self._base.edges_to(vid, limit=500):
                    s = self._base.get_vertex(e["out_v"])
                    if s:
                        affected.add(s["canonical_id"])
            affected -= removed_cids
            result["removed_entities"] = sorted(removed_cids)
            result["affected_entities"] = sorted(affected)

        self._manifests[sim_id].results[analysis_type] = result
        return result

    def compare(self, sim_id: str) -> dict[str, Any]:
        overlay = self._simulations.get(sim_id)
        if not overlay:
            return {"error": f"Simulation {sim_id} not found"}
        return {
            "simulation_id": sim_id,
            "added_vertices": len(overlay._added_vertices),
            "removed_vertices": len(overlay._removed_vertex_vids),
            "added_edges": len(overlay._added_edges),
            "removed_edges": len(overlay._removed_edge_eids),
            "modified_vertices": len(overlay._modified_props),
            "total_mutations": overlay.mutation_count,
        }

    def get_manifest(self, sim_id: str) -> dict[str, Any] | None:
        m = self._manifests.get(sim_id)
        return m.to_dict() if m else None

    def list_simulations(self) -> list[dict[str, Any]]:
        return [
            {"simulation_id": sid, "created_at": self._manifests[sid].created_at,
             "mutations": len(self._manifests[sid].mutations)}
            for sid in self._simulations
        ]

"""Hierarchy induction over flat entity sets.

Three deterministic strategies, all producing ``CHILD_OF`` edge proposals:

* ``parent_pointer`` — records carry an explicit parent reference field.
* ``path_string`` — records carry delimited path strings (``a/b/c``).
* ``lexical_clustering`` — names share case-insensitive token prefixes;
  clusters get a synthetic parent whose name is the shared prefix.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import GraphDelta, ProposedEdge


class HierarchyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: str = Field(default="parent_pointer")  # parent_pointer | path_string | lexical_clustering
    parent_field: str = "parent_id"
    path_field: str = "path"
    name_field: str = "name"
    id_field: str = "id"
    delimiter: str = "/"
    min_cluster_size: int = Field(default=2, ge=2)
    min_prefix_tokens: int = Field(default=1, ge=1)


def induce_hierarchy(
    records: Iterable[dict[str, Any]],
    config: HierarchyConfig | None = None,
) -> GraphDelta:
    """Induce a hierarchy over ``records`` using the configured strategy."""
    cfg = config or HierarchyConfig()
    records = list(records)
    if cfg.method == "parent_pointer":
        edges = _parent_pointer(records, cfg)
    elif cfg.method == "path_string":
        edges = _path_string(records, cfg)
    elif cfg.method == "lexical_clustering":
        edges = _lexical_clustering(records, cfg)
    else:
        raise ValueError(f"Unknown hierarchy method: {cfg.method}")
    return GraphDelta.make("hierarchy", repr((cfg.model_dump(), sorted(r.get(cfg.id_field) for r in records))), edges=edges, notes=[f"method={cfg.method}"])


def _parent_pointer(records: list[dict[str, Any]], cfg: HierarchyConfig) -> list[ProposedEdge]:
    edges = []
    ids = {r.get(cfg.id_field) for r in records}
    for record in records:
        child = record.get(cfg.id_field)
        parent = record.get(cfg.parent_field)
        if not child or parent in {None, ""} or parent not in ids or parent == child:
            continue
        edges.append(ProposedEdge.make("CHILD_OF", str(child), str(parent), 1.0, "hierarchy:parent-pointer"))
    return edges


def _path_string(records: list[dict[str, Any]], cfg: HierarchyConfig) -> list[ProposedEdge]:
    edges = []
    by_path = {str(r.get(cfg.path_field, "")): r.get(cfg.id_field) for r in records}
    seen: set[tuple[str, str]] = set()
    for record in records:
        child = record.get(cfg.id_field)
        path = str(record.get(cfg.path_field, ""))
        parts = [p for p in path.split(cfg.delimiter) if p]
        if len(parts) < 2 or not child:
            continue
        parent_path = cfg.delimiter.join(parts[:-1])
        parent = by_path.get(parent_path)
        if parent and parent != child and (str(child), str(parent)) not in seen:
            seen.add((str(child), str(parent)))
            edges.append(
                ProposedEdge.make(
                    "CHILD_OF",
                    str(child),
                    str(parent),
                    1.0,
                    "hierarchy:path-string",
                    parent_path=parent_path,
                )
            )
    return edges


def _lexical_clustering(records: list[dict[str, Any]], cfg: HierarchyConfig) -> list[ProposedEdge]:
    clusters: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    for record in records:
        name = str(record.get(cfg.name_field, ""))
        tokens = [t for t in re.split(r"[^A-Za-z0-9]+", name) if t]
        if not tokens:
            continue
        key = tuple(t.casefold() for t in tokens[: cfg.min_prefix_tokens])
        clusters.setdefault(key, []).append(record)

    edges: list[ProposedEdge] = []
    for key in sorted(clusters):
        members = clusters[key]
        if len(members) < cfg.min_cluster_size:
            continue
        parent_name = " ".join(key).title()
        parent_id = f"synthetic:{parent_name}"
        for member in members:
            child = member.get(cfg.id_field)
            if not child or str(child) == parent_id:
                continue
            edges.append(
                ProposedEdge.make(
                    "CHILD_OF",
                    str(child),
                    parent_id,
                    1.0,
                    "hierarchy:lexical-clustering",
                    cluster=parent_name,
                )
            )
    return edges

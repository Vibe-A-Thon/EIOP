"""KGR-G-003: Obsidian Vault & Interactive Knowledge Generator.

Exports the knowledge graph into an Obsidian-compatible vault of
interlinked Markdown files.  Each entity becomes a note with YAML
frontmatter, and each edge becomes an [[internal link]].  Supports
incremental sync, Dataview-compatible metadata, and Mermaid diagram
generation for subgraph visualization.
"""

from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eoip.graph.store import Edge, GraphStore, Vertex

log = logging.getLogger("eoip.exporters.obsidian_vault")


@dataclass
class VaultConfig:
    vault_root: Path
    include_labels: set[str] | None = None
    exclude_labels: set[str] | None = None
    max_depth: int = 3
    generate_mermaid: bool = True
    generate_index: bool = True
    generate_moc: bool = True
    frontmatter_keys: list[str] | None = None
    folder_by_label: bool = True
    timestamp_format: str = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class ExportStats:
    notes_created: int = 0
    notes_updated: int = 0
    notes_skipped: int = 0
    links_created: int = 0
    mermaid_diagrams: int = 0
    errors: list[str] = field(default_factory=list)


def _sanitize_filename(name: str) -> str:
    """Remove characters forbidden in Obsidian filenames."""
    cleaned = re.sub(r'[<>:"/\\|?*#^[\]{}]', "_", name)
    cleaned = cleaned.strip(". ")
    return cleaned[:200] or "untitled"


def _vertex_display_name(v: Vertex) -> str:
    props = dict(v)
    return str(
        props.get("name")
        or props.get("title")
        or props.get("canonical_id")
        or props.get("vid", "unknown")
    )


def _vertex_canonical(v: Vertex) -> str:
    return str(v.get("canonical_id") or v.get("vid", ""))


class ObsidianNoteBuilder:
    """Builds a single Obsidian Markdown note from a graph vertex and its edges."""

    def __init__(self, config: VaultConfig) -> None:
        self.config = config

    def build(self, vertex: Vertex, outgoing: list[Edge], incoming: list[Edge], neighbors: dict[str, Vertex]) -> str:
        sections: list[str] = []
        sections.append(self._frontmatter(vertex))
        sections.append(self._header(vertex))
        sections.append(self._properties_section(vertex))

        if outgoing or incoming:
            sections.append(self._relationships_section(outgoing, incoming, neighbors))

        if self.config.generate_mermaid and (outgoing or incoming):
            sections.append(self._mermaid_section(vertex, outgoing, incoming, neighbors))

        return "\n\n".join(sections) + "\n"

    def _frontmatter(self, vertex: Vertex) -> str:
        props = dict(vertex)
        meta: dict[str, Any] = {
            "canonical_id": _vertex_canonical(vertex),
            "label": props.get("label", "Entity"),
            "created": datetime.now(timezone.utc).strftime(self.config.timestamp_format),
            "tags": [f"eoip/{props.get('label', 'entity')}"],
        }
        allowed = self.config.frontmatter_keys
        for k, v in props.items():
            if k in ("vid", "properties"):
                continue
            if allowed is not None and k not in allowed:
                continue
            if isinstance(v, (str, int, float, bool)):
                meta[k] = v
        lines = ["---"]
        for k, v in meta.items():
            if isinstance(v, list):
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{k}: {json.dumps(v) if isinstance(v, (bool, dict)) else v}")
        lines.append("---")
        return "\n".join(lines)

    def _header(self, vertex: Vertex) -> str:
        name = _vertex_display_name(vertex)
        label = vertex.get("label", "Entity")
        return f"# {name}\n\n**Type:** `{label}`"

    def _properties_section(self, vertex: Vertex) -> str:
        props = dict(vertex)
        skip = {"vid", "canonical_id", "label", "name", "title", "properties", "_deleted"}
        items = {k: v for k, v in props.items() if k not in skip and v is not None}
        if not items:
            return ""
        lines = ["## Properties", ""]
        for k, v in sorted(items.items()):
            lines.append(f"- **{k}:** {v}")
        return "\n".join(lines)

    def _relationships_section(
        self, outgoing: list[Edge], incoming: list[Edge], neighbors: dict[str, Vertex]
    ) -> str:
        lines = ["## Relationships", ""]
        if outgoing:
            lines.append("### Outgoing")
            for edge in outgoing:
                target_vid = str(edge.get("in_v") or edge.get("in_cid", ""))
                target = neighbors.get(target_vid)
                target_name = _vertex_display_name(target) if target else target_vid
                safe_name = _sanitize_filename(target_name)
                edge_label = edge.get("label", "RELATED_TO")
                lines.append(f"- **{edge_label}** → [[{safe_name}]]")

        if incoming:
            lines.append("")
            lines.append("### Incoming")
            for edge in incoming:
                source_vid = str(edge.get("out_v") or edge.get("out_cid", ""))
                source = neighbors.get(source_vid)
                source_name = _vertex_display_name(source) if source else source_vid
                safe_name = _sanitize_filename(source_name)
                edge_label = edge.get("label", "RELATED_TO")
                lines.append(f"- **{edge_label}** ← [[{safe_name}]]")

        return "\n".join(lines)

    def _mermaid_section(
        self, vertex: Vertex, outgoing: list[Edge], incoming: list[Edge], neighbors: dict[str, Vertex]
    ) -> str:
        vid = _vertex_canonical(vertex)
        name = _vertex_display_name(vertex)
        lines = [
            "## Graph Neighborhood",
            "",
            "```mermaid",
            "graph LR",
            f'    {_mermaid_id(vid)}["{name}"]',
        ]
        for edge in outgoing:
            target_vid = str(edge.get("in_v") or edge.get("in_cid", ""))
            target = neighbors.get(target_vid)
            target_name = _vertex_display_name(target) if target else target_vid
            edge_label = edge.get("label", "")
            lines.append(
                f'    {_mermaid_id(vid)} -->|{edge_label}| {_mermaid_id(target_vid)}["{target_name}"]'
            )
        for edge in incoming:
            source_vid = str(edge.get("out_v") or edge.get("out_cid", ""))
            source = neighbors.get(source_vid)
            source_name = _vertex_display_name(source) if source else source_vid
            edge_label = edge.get("label", "")
            lines.append(
                f'    {_mermaid_id(source_vid)}["{source_name}"] -->|{edge_label}| {_mermaid_id(vid)}'
            )
        lines.append("```")
        return "\n".join(lines)


def _mermaid_id(cid: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", cid)[:40]


class ObsidianVaultExporter:
    """Exports the knowledge graph into an Obsidian vault structure."""

    def __init__(self, store: GraphStore, config: VaultConfig) -> None:
        self.store = store
        self.config = config
        self._note_builder = ObsidianNoteBuilder(config)

    def export(self) -> ExportStats:
        stats = ExportStats()
        self.config.vault_root.mkdir(parents=True, exist_ok=True)

        vertices = self._fetch_vertices()
        for vertex in vertices:
            try:
                self._export_vertex(vertex, stats)
            except Exception as exc:
                stats.errors.append(f"{_vertex_canonical(vertex)}: {exc}")

        if self.config.generate_index:
            self._generate_index(vertices, stats)

        if self.config.generate_moc:
            self._generate_moc(vertices, stats)

        return stats

    def export_subgraph(self, root_vid: str, *, depth: int | None = None) -> ExportStats:
        stats = ExportStats()
        max_depth = depth or self.config.max_depth
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(root_vid, 0)]

        while queue:
            vid, d = queue.pop(0)
            if vid in visited or d > max_depth:
                continue
            visited.add(vid)
            vertex = self.store.get_vertex(vid)
            if vertex is None:
                vertex = self.store.get_vertex_by_canonical_id(vid)
            if vertex is None:
                continue
            self._export_vertex(vertex, stats)
            if d < max_depth:
                for edge in self.store.edges_from(vid):
                    target = str(edge.get("in_v") or edge.get("in_cid", ""))
                    queue.append((target, d + 1))
                for edge in self.store.edges_to(vid):
                    source = str(edge.get("out_v") or edge.get("out_cid", ""))
                    queue.append((source, d + 1))

        return stats

    def _fetch_vertices(self) -> list[Vertex]:
        vertices = self.store.find_vertices(limit=100_000)
        if self.config.include_labels:
            vertices = [v for v in vertices if v.get("label") in self.config.include_labels]
        if self.config.exclude_labels:
            vertices = [v for v in vertices if v.get("label") not in self.config.exclude_labels]
        return vertices

    def _export_vertex(self, vertex: Vertex, stats: ExportStats) -> None:
        vid = _vertex_canonical(vertex)
        name = _vertex_display_name(vertex)
        safe = _sanitize_filename(name)

        if self.config.folder_by_label:
            label = vertex.get("label", "Entity")
            folder = self.config.vault_root / _sanitize_filename(str(label))
        else:
            folder = self.config.vault_root

        folder.mkdir(parents=True, exist_ok=True)
        note_path = folder / f"{safe}.md"

        outgoing = self.store.edges_from(vid)
        incoming = self.store.edges_to(vid)

        neighbors: dict[str, Vertex] = {}
        for edge in outgoing:
            nv = str(edge.get("in_v") or edge.get("in_cid", ""))
            v = self.store.get_vertex(nv) or self.store.get_vertex_by_canonical_id(nv)
            if v:
                neighbors[nv] = v
        for edge in incoming:
            nv = str(edge.get("out_v") or edge.get("out_cid", ""))
            v = self.store.get_vertex(nv) or self.store.get_vertex_by_canonical_id(nv)
            if v:
                neighbors[nv] = v

        content = self._note_builder.build(vertex, outgoing, incoming, neighbors)
        stats.links_created += len(outgoing) + len(incoming)
        if self.config.generate_mermaid and (outgoing or incoming):
            stats.mermaid_diagrams += 1

        if note_path.exists():
            existing = note_path.read_text(encoding="utf-8")
            if existing == content:
                stats.notes_skipped += 1
                return
            stats.notes_updated += 1
        else:
            stats.notes_created += 1

        note_path.write_text(content, encoding="utf-8")

    def _generate_index(self, vertices: list[Vertex], stats: ExportStats) -> None:
        lines = [
            "---",
            "tags: [eoip/index]",
            "---",
            "# Knowledge Graph Index",
            "",
            f"**Total entities:** {len(vertices)}",
            "",
        ]
        by_label: dict[str, list[Vertex]] = {}
        for v in vertices:
            label = str(v.get("label", "Entity"))
            by_label.setdefault(label, []).append(v)

        for label in sorted(by_label):
            items = by_label[label]
            lines.append(f"## {label} ({len(items)})")
            lines.append("")
            for v in sorted(items, key=lambda x: _vertex_display_name(x).lower()):
                name = _vertex_display_name(v)
                safe = _sanitize_filename(name)
                lines.append(f"- [[{safe}]]")
            lines.append("")

        index_path = self.config.vault_root / "Index.md"
        index_path.write_text("\n".join(lines), encoding="utf-8")
        stats.notes_created += 1

    def _generate_moc(self, vertices: list[Vertex], stats: ExportStats) -> None:
        """Generate a Map of Content (MOC) per entity label."""
        by_label: dict[str, list[Vertex]] = {}
        for v in vertices:
            label = str(v.get("label", "Entity"))
            by_label.setdefault(label, []).append(v)

        for label, items in by_label.items():
            lines = [
                "---",
                f"tags: [eoip/moc, eoip/{label.lower()}]",
                "---",
                f"# {label} — Map of Content",
                "",
                f"**Count:** {len(items)}",
                "",
            ]
            for v in sorted(items, key=lambda x: _vertex_display_name(x).lower()):
                name = _vertex_display_name(v)
                safe = _sanitize_filename(name)
                lines.append(f"- [[{safe}]]")
            lines.append("")

            moc_path = self.config.vault_root / f"MOC-{_sanitize_filename(label)}.md"
            moc_path.write_text("\n".join(lines), encoding="utf-8")
            stats.notes_created += 1

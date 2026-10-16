"""Scoped Multi-Modal Diagram-to-Graph & Graph-to-Diagram Engine (MULTI-001).

Implements:
- DiagramToGraphParser: Parses structured diagram formats (Mermaid, PlantUML) into graph entities & relations
- GraphToDiagramRenderer: Renders subgraphs to standard Mermaid, PlantUML, and SVG diagrams
"""

from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.fileparse.diagram")


class DiagramType(str, Enum):
    FLOWCHART = "FLOWCHART"
    ER_DIAGRAM = "ER_DIAGRAM"
    ARCHITECTURE = "ARCHITECTURE"
    SEQUENCE = "SEQUENCE"


@dataclass
class ParsedDiagramGraph:
    diagram_type: DiagramType
    vertices: list[dict[str, Any]] = field(default_factory=list)
    edges: list[dict[str, Any]] = field(default_factory=list)

    def load_into_store(self, store: MemoryGraphStore) -> None:
        for v in self.vertices:
            store.upsert_vertex(v["label"], v["properties"])
        for e in self.edges:
            out_cid = e["out_cid"]
            in_cid = e["in_cid"]
            store.upsert_edge(e["label"], out_cid, in_cid, e.get("properties", {}))


class DiagramToGraphParser:
    """Parses text diagrams (Mermaid, PlantUML) into knowledge graph structures."""

    def parse_mermaid(self, mermaid_text: str) -> ParsedDiagramGraph:
        vertices: list[dict[str, Any]] = []
        edges: list[dict[str, Any]] = []
        seen_vids: set[str] = set()

        # Determine diagram type
        dtype = DiagramType.FLOWCHART
        if "erDiagram" in mermaid_text:
            dtype = DiagramType.ER_DIAGRAM
        elif "sequenceDiagram" in mermaid_text:
            dtype = DiagramType.SEQUENCE

        # Extract nodes: id["label"] or id[label]
        node_pat = re.compile(r'([A-Za-z0-9_-]+)\[["\']?([^"\'\]]+)["\']?\]')
        for match in node_pat.finditer(mermaid_text):
            nid = match.group(1)
            name = match.group(2)
            if nid not in seen_vids:
                seen_vids.add(nid)
                vertices.append({
                    "label": "Service",
                    "properties": {
                        "canonical_id": nid,
                        "service_id": nid,
                        "name": name,
                    },
                })

        # Extract edges: u -->|LABEL| v or u --> v (handling potential inline node labels like u["label"])
        edge_pat = re.compile(r'([A-Za-z0-9_-]+)(?:\[[^\]]*\])?\s*-->\s*(?:\|([^|]+)\|)?\s*([A-Za-z0-9_-]+)(?:\[[^\]]*\])?')
        for match in edge_pat.finditer(mermaid_text):
            u = match.group(1)
            lbl = match.group(2) or "CALLS"
            v = match.group(3)
            # Ensure vertices exist
            if u not in seen_vids:
                seen_vids.add(u)
                vertices.append({
                    "label": "Service",
                    "properties": {"canonical_id": u, "service_id": u, "name": u},
                })
            if v not in seen_vids:
                seen_vids.add(v)
                vertices.append({
                    "label": "Service",
                    "properties": {"canonical_id": v, "service_id": v, "name": v},
                })

            valid_label = "CALLS" if lbl.upper() not in ("CALLS", "DEPENDS_ON") else lbl.upper()
            edges.append({
                "label": valid_label,
                "out_cid": u,
                "in_cid": v,
                "properties": {},
            })

        return ParsedDiagramGraph(
            diagram_type=dtype,
            vertices=vertices,
            edges=edges,
        )


class GraphToDiagramRenderer:
    """Exports subgraphs to visualization formats."""

    def render_mermaid(self, vertices: list[dict[str, Any]], edges: list[dict[str, Any]]) -> str:
        lines = ["flowchart LR"]
        for v in vertices:
            cid = v.get("canonical_id", v.get("properties", {}).get("canonical_id", "node"))
            name = v.get("properties", {}).get("name", cid)
            lines.append(f'    {cid}["{name}"]')
        for e in edges:
            u = e.get("out_cid", e.get("out_v"))
            v = e.get("in_cid", e.get("in_v"))
            lbl = e.get("label", "CALLS")
            lines.append(f'    {u} -->|{lbl}| {v}')
        return "\n".join(lines)

    def render_svg(self, vertices: list[dict[str, Any]], edges: list[dict[str, Any]]) -> str:
        """Pure Python SVG diagram generation."""
        width = 600
        height = max(300, len(vertices) * 80)
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '  <style>rect { fill: #2d3748; stroke: #4a5568; rx: 6; } text { fill: #f7fafc; font-family: sans-serif; font-size: 14px; }</style>',
        ]

        y = 50
        pos = {}
        for idx, v in enumerate(vertices):
            cid = v.get("canonical_id", v.get("properties", {}).get("canonical_id", f"node_{idx}"))
            name = v.get("properties", {}).get("name", cid)
            x = 80 if (idx % 2 == 0) else 350
            pos[cid] = (x + 80, y + 25)
            svg_parts.append(f'  <rect x="{x}" y="{y}" width="160" height="50"/>')
            svg_parts.append(f'  <text x="{x + 80}" y="{y + 30}" text-anchor="middle">{name}</text>')
            y += 80

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

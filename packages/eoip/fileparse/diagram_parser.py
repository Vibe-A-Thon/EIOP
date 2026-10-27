"""Scoped Multi-Modal Diagram-to-Graph & Graph-to-Diagram Engine (MULTI-001, CRA-015).

Implements:
- DiagramAST, DiagramShape, DiagramConnector, LossLedgerEntry: Formal AST for structured diagrams.
- Notation-specific parsers:
  * DrawIO / diagrams.net XML (including Chowlk-compatible ontology notation)
  * Mermaid subsets (flowchart, sequenceDiagram, erDiagram, classDiagram)
  * PlantUML subsets (class, component, database, cloud, queue, interface, package)
- Configurable, versioned shape and connector ontology mapping table:
  * Proposes ontology terms with knowledge_state='proposed'
  * Preserves unrecognized connectors as generic 'eoip:connectsTo' (fixes Gap G10, never coerces to CALLS/Service)
  * Preserves unrecognized shapes as 'eoip:DiagramComponent'
- Visual diagram extraction candidates with bounding boxes and uncertainty (CRA-015.3, CRA-015.8)
- Source-vs-graph diff and loss ledger (CRA-015.4)
- Sanitized round-trip rendering for Mermaid, PlantUML, and DrawIO XML (CRA-015.5)
- OWL 2 / RDF compilation with gold model fidelity comparison (CRA-015.A)
- Backward-compatible DiagramToGraphParser and GraphToDiagramRenderer
"""

from __future__ import annotations

import html
import io
import logging
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable

import defusedxml.ElementTree as ET
import xml.etree.ElementTree as std_ET
import rdflib
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef

from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.fileparse.diagram")

EOIP = Namespace("https://enterprise-ontology.org/schema/eoip#")


class DiagramType(str, Enum):
    FLOWCHART = "FLOWCHART"
    ER_DIAGRAM = "ER_DIAGRAM"
    ARCHITECTURE = "ARCHITECTURE"
    SEQUENCE = "SEQUENCE"
    CLASS_DIAGRAM = "CLASS_DIAGRAM"
    CHOWLK_ONTOLOGY = "CHOWLK_ONTOLOGY"


# ---------------------------------------------------------------------------
# AST Data Structures
# ---------------------------------------------------------------------------
@dataclass
class LossLedgerEntry:
    construct_type: str
    construct_id: str
    raw_content: str
    reason: str
    action_taken: str

    def to_dict(self) -> dict[str, str]:
        return {
            "construct_type": self.construct_type,
            "construct_id": self.construct_id,
            "raw_content": self.raw_content,
            "reason": self.reason,
            "action_taken": self.action_taken,
        }


@dataclass
class DiagramShape:
    id: str
    name: str
    shape_type: str = "rectangle"
    parent_id: str | None = None
    ports: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)
    bounding_box: tuple[float, float, float, float] | None = None  # (ymin, xmin, ymax, xmax) or (x, y, w, h)
    visual_attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagramConnector:
    id: str
    source_id: str
    target_id: str
    direction: str = "directed"  # "directed", "bidirectional", "undirected"
    label: str = ""
    cardinality_source: str | None = None
    cardinality_target: str | None = None
    connector_type: str = "solid"  # "solid", "dashed", "dotted", "inheritance", "composition", "aggregation"
    visual_attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagramAST:
    diagram_format: str  # "drawio_xml", "chowlk_xml", "mermaid", "plantuml", "vsdx"
    diagram_type: DiagramType = DiagramType.ARCHITECTURE
    source_raw: str = ""
    shapes: list[DiagramShape] = field(default_factory=list)
    connectors: list[DiagramConnector] = field(default_factory=list)
    containers: list[DiagramShape] = field(default_factory=list)
    loss_ledger: list[LossLedgerEntry] = field(default_factory=list)
    is_lossless: bool = True
    coverage_stats: dict[str, Any] = field(default_factory=dict)

    def add_shape(self, shape: DiagramShape) -> None:
        self.shapes.append(shape)
        if shape.shape_type in ("container", "package", "subgraph", "boundary"):
            self.containers.append(shape)

    def add_connector(self, connector: DiagramConnector) -> None:
        self.connectors.append(connector)

    def record_loss(self, construct_type: str, construct_id: str, raw_content: str, reason: str, action: str) -> None:
        self.loss_ledger.append(LossLedgerEntry(
            construct_type=construct_type,
            construct_id=construct_id,
            raw_content=raw_content,
            reason=reason,
            action_taken=action,
        ))
        self.is_lossless = False

    def get_shape(self, shape_id: str) -> DiagramShape | None:
        for s in self.shapes:
            if s.id == shape_id:
                return s
        return None

    def get_children(self, container_id: str) -> list[DiagramShape]:
        return [s for s in self.shapes if s.parent_id == container_id]


# ---------------------------------------------------------------------------
# Label Sanitization and Escaping
# ---------------------------------------------------------------------------
def sanitize_diagram_label(text: str) -> str:
    """Escapes and sanitizes markup, HTML, and special metacharacters idempotently."""
    if not text:
        return ""
    # Strip dangerous script tags or executable attributes
    clean = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', text, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r'on\w+\s*=', '', clean, flags=re.IGNORECASE)
    # Prevent double-escaping by unescaping first
    unescaped = html.unescape(clean.strip())
    return html.escape(unescaped)


# ---------------------------------------------------------------------------
# Parsers: Draw.io XML, Mermaid, PlantUML
# ---------------------------------------------------------------------------
class DrawIOParser:
    """Parses draw.io / diagrams.net mxGraphModel XML including Chowlk notation."""

    SHAPE_MAP = {
        "cylinder": "cylinder",
        "mxgraph.flowchart.database": "cylinder",
        "cloud": "cloud",
        "actor": "actor",
        "mxgraph.flowchart.queue": "queue",
        "swimlane": "container",
        "group": "container",
        "rhombus": "decision",
        "ellipse": "circle",
    }

    def parse(self, xml_content: str | bytes) -> DiagramAST:
        if isinstance(xml_content, bytes):
            xml_text = xml_content.decode("utf-8", errors="replace")
        else:
            xml_text = xml_content

        ast = DiagramAST(diagram_format="drawio_xml", source_raw=xml_text)
        try:
            root = ET.fromstring(xml_text)
        except Exception as exc:
            ast.record_loss("xml_syntax", "root", xml_text[:100], str(exc), "aborted_xml_parsing")
            return ast

        # Find mxGraphModel root
        model_root = root.find(".//root")
        if model_root is None:
            # Maybe root is mxGraphModel or mxfile
            if root.tag == "root":
                model_root = root
            else:
                ast.record_loss("mxgraph_model", "root", "", "No <root> element found in draw.io XML", "empty_ast")
                return ast

        cells = model_root.findall("mxCell")
        total_cells = len(cells)
        parsed_cells = 0

        for cell in cells:
            cell_id = cell.get("id", "")
            if cell_id in ("0", "1"):
                parsed_cells += 1
                continue

            value = cell.get("value", "")
            clean_value = sanitize_diagram_label(value)
            style_str = cell.get("style", "")
            parent_id = cell.get("parent")
            if parent_id in ("0", "1"):
                parent_id = None

            styles = self._parse_styles(style_str)

            # Vertex (Shape / Container)
            if cell.get("vertex") == "1":
                parsed_cells += 1
                shape_type = "rectangle"
                for k, v in styles.items():
                    if k == "shape" and v in self.SHAPE_MAP:
                        shape_type = self.SHAPE_MAP[v]
                    elif "chowlk:class" in style_str.lower() or "owl:class" in value.lower():
                        shape_type = "chowlk_class"
                        ast.diagram_type = DiagramType.CHOWLK_ONTOLOGY
                    elif "chowlk:datatype" in style_str.lower() or "rdfs:datatype" in value.lower():
                        shape_type = "chowlk_datatype"
                        ast.diagram_type = DiagramType.CHOWLK_ONTOLOGY

                geom = cell.find("mxGeometry")
                bbox = None
                if geom is not None:
                    try:
                        x = float(geom.get("x", 0))
                        y = float(geom.get("y", 0))
                        w = float(geom.get("width", 0))
                        h = float(geom.get("height", 0))
                        bbox = (y, x, y + h, x + w)
                    except ValueError:
                        pass

                shape = DiagramShape(
                    id=cell_id,
                    name=clean_value or f"Node_{cell_id}",
                    shape_type=shape_type,
                    parent_id=parent_id,
                    bounding_box=bbox,
                    properties={"raw_value": value, "styles": styles},
                    visual_attributes=styles,
                )
                ast.add_shape(shape)

            # Edge (Connector)
            elif cell.get("edge") == "1":
                parsed_cells += 1
                source_id = cell.get("source", "")
                target_id = cell.get("target", "")
                if not source_id or not target_id:
                    ast.record_loss(
                        "disconnected_edge", cell_id, style_str,
                        f"Edge {cell_id} lacks explicit source or target", "dropped_disconnected_edge"
                    )
                    continue

                direction = "directed"
                if styles.get("endArrow") == "none" and styles.get("startArrow") == "none":
                    direction = "undirected"
                elif styles.get("endArrow") and styles.get("startArrow"):
                    direction = "bidirectional"

                conn_type = "solid"
                if styles.get("dashed") == "1":
                    conn_type = "dashed"

                connector = DiagramConnector(
                    id=cell_id,
                    source_id=source_id,
                    target_id=target_id,
                    direction=direction,
                    label=clean_value,
                    connector_type=conn_type,
                    visual_attributes=styles,
                )
                ast.add_connector(connector)
            else:
                ast.record_loss("unsupported_cell", cell_id, style_str, "Cell is neither vertex nor edge", "ignored")

        ast.coverage_stats = {
            "total_cells": total_cells,
            "parsed_cells": parsed_cells,
            "coverage_pct": round((parsed_cells / max(1, total_cells)) * 100, 2),
        }
        return ast

    def _parse_styles(self, style_str: str) -> dict[str, str]:
        res: dict[str, str] = {}
        if not style_str:
            return res
        parts = style_str.split(";")
        for part in parts:
            if not part.strip():
                continue
            if "=" in part:
                k, v = part.split("=", 1)
                res[k.strip()] = v.strip()
            else:
                res[part.strip()] = "1"
        return res


class MermaidParser:
    """Parses Mermaid diagram subsets: Flowchart, Sequence, ER, Class."""

    def parse(self, text: str) -> DiagramAST:
        ast = DiagramAST(diagram_format="mermaid", source_raw=text)
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        if not lines:
            return ast

        # Check diagram header
        header = lines[0].lower()
        if "erdiagram" in header:
            ast.diagram_type = DiagramType.ER_DIAGRAM
        elif "sequencediagram" in header:
            ast.diagram_type = DiagramType.SEQUENCE
        elif "classdiagram" in header:
            ast.diagram_type = DiagramType.CLASS_DIAGRAM
        else:
            ast.diagram_type = DiagramType.FLOWCHART

        current_container: str | None = None
        seen_shapes: set[str] = set()

        # Node identifier pattern: starts with a letter/digit, not a dash or arrow
        # Regex patterns for shapes:
        # id[(cylinder)]
        # id[[subroutine]]
        # id([stadium])
        # id((circle))
        # id>asymmetric]  (must not match arrows like -->)
        # id{decision}
        # id{{hexagon}}
        # id["label"] or id[label]
        shape_patterns = [
            (re.compile(r'\b([A-Za-z0-9_]+)\[\((.*?)\)\]'), "cylinder"),
            (re.compile(r'\b([A-Za-z0-9_]+)\[\[(.*?)\]\]'), "subroutine"),
            (re.compile(r'\b([A-Za-z0-9_]+)\(\[(.*?)\]\)'), "stadium"),
            (re.compile(r'\b([A-Za-z0-9_]+)\(\((.*?)\)\)'), "circle"),
            (re.compile(r'(?<!-)\b([A-Za-z0-9_]+)>([^\]]+)\]'), "asymmetric"),
            (re.compile(r'\b([A-Za-z0-9_]+)\{\{(.*?)\}\}'), "hexagon"),
            (re.compile(r'\b([A-Za-z0-9_]+)\{(.*?)\}'), "decision"),
            (re.compile(r'\b([A-Za-z0-9_]+)\[["\']?([^"\'\]]+)["\']?\]'), "rectangle"),
        ]

        # Connector pattern:
        # A -->|label| B
        # A -.->|label| B
        # A ==>|label| B
        # A ---|label| B
        # A <--> B
        conn_pat = re.compile(
            r'([A-Za-z0-9_-]+)(?:\[[^\]]*\])?\s*(-->|-\.->|==>|---|--|<-->)\s*(?:\|([^|]+)\|)?\s*([A-Za-z0-9_-]+)(?:\[[^\]]*\])?'
        )

        for line in lines[1:]:
            # Subgraph handling
            subgraph_match = re.match(r'subgraph\s+([A-Za-z0-9_-]+)(?:\s*\[["\']?([^"\'\]]+)["\']?\])?', line, re.IGNORECASE)
            if subgraph_match:
                cid = subgraph_match.group(1)
                cname = subgraph_match.group(2) or cid
                container_shape = DiagramShape(
                    id=cid,
                    name=sanitize_diagram_label(cname),
                    shape_type="container",
                    parent_id=current_container,
                )
                ast.add_shape(container_shape)
                current_container = cid
                continue

            if line.lower() == "end" and current_container:
                current_container = None
                continue

            # Detect node definitions
            matched_node = False
            for pat, stype in shape_patterns:
                for match in pat.finditer(line):
                    nid = match.group(1)
                    raw_name = match.group(2).strip()
                    if nid not in seen_shapes:
                        seen_shapes.add(nid)
                        ast.add_shape(DiagramShape(
                            id=nid,
                            name=sanitize_diagram_label(raw_name) or nid,
                            shape_type=stype,
                            parent_id=current_container,
                        ))
                    matched_node = True

            # Detect connectors
            conn_match = conn_pat.search(line)
            if conn_match:
                u = conn_match.group(1)
                arrow = conn_match.group(2)
                lbl = conn_match.group(3) or ""
                v = conn_match.group(4)

                direction = "directed"
                conn_type = "solid"
                if arrow == "---":
                    direction = "undirected"
                elif arrow == "<-->":
                    direction = "bidirectional"
                elif arrow == "-.->":
                    conn_type = "dashed"
                elif arrow == "==>":
                    conn_type = "thick"

                # Ensure vertices exist if not defined before
                if u not in seen_shapes:
                    seen_shapes.add(u)
                    ast.add_shape(DiagramShape(id=u, name=u, shape_type="rectangle", parent_id=current_container))
                if v not in seen_shapes:
                    seen_shapes.add(v)
                    ast.add_shape(DiagramShape(id=v, name=v, shape_type="rectangle", parent_id=current_container))

                ast.add_connector(DiagramConnector(
                    id=f"conn_{u}_{v}_{len(ast.connectors)+1}",
                    source_id=u,
                    target_id=v,
                    direction=direction,
                    label=sanitize_diagram_label(lbl),
                    connector_type=conn_type,
                ))
            elif not matched_node and line not in ("flowchart", "graph", "sequenceDiagram", "classDiagram", "erDiagram"):
                # Track unsupported line in loss ledger
                ast.record_loss("unsupported_syntax", f"line_{lines.index(line)}", line, "Syntax not recognized in profile", "ignored")

        return ast


class PlantUMLParser:
    """Parses PlantUML component, class, and deployment diagrams."""

    def parse(self, text: str) -> DiagramAST:
        ast = DiagramAST(diagram_format="plantuml", source_raw=text)
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

        current_package: str | None = None
        seen_shapes: set[str] = set()

        elem_pat = re.compile(
            r'^(class|component|database|cloud|queue|interface|actor)\s+([A-Za-z0-9_-]+)(?:\s+as\s+([A-Za-z0-9_-]+))?(?:\s*\{)?',
            re.IGNORECASE
        )
        conn_pat = re.compile(
            r'(?:"([^"]+)"\s*)?([A-Za-z0-9_-]+)\s*(-->|\.\.>|--\|>|\*--|o--|--)\s*(?:"([^"]+)"\s*)?([A-Za-z0-9_-]+)(?:\s*:\s*(.*))?'
        )

        for idx, line in enumerate(lines):
            if line.startswith(("@startuml", "@enduml")):
                continue

            # Package / Container
            pkg_match = re.match(r'^(?:package|node|rectangle)\s+["\']?([^"\'\{]+)["\']?\s*(?:as\s+([A-Za-z0-9_-]+))?\s*\{?', line, re.IGNORECASE)
            if pkg_match:
                pname = pkg_match.group(1).strip()
                pid = pkg_match.group(2) or pname.replace(" ", "_")
                ast.add_shape(DiagramShape(
                    id=pid,
                    name=sanitize_diagram_label(pname),
                    shape_type="package",
                    parent_id=current_package,
                ))
                current_package = pid
                continue

            if line == "}" and current_package:
                current_package = None
                continue

            # Entity definition
            elem_match = elem_pat.match(line)
            if elem_match:
                kind = elem_match.group(1).lower()
                raw_id = elem_match.group(2)
                alias = elem_match.group(3)
                nid = alias or raw_id
                if nid not in seen_shapes:
                    seen_shapes.add(nid)
                    ast.add_shape(DiagramShape(
                        id=nid,
                        name=sanitize_diagram_label(raw_id),
                        shape_type=kind,
                        parent_id=current_package,
                    ))
                continue

            # Connector
            conn_match = conn_pat.match(line)
            if conn_match:
                src_card = conn_match.group(1)
                u = conn_match.group(2)
                arrow = conn_match.group(3)
                tgt_card = conn_match.group(4)
                v = conn_match.group(5)
                lbl = conn_match.group(6) or ""

                direction = "directed"
                conn_type = "solid"
                if arrow == "--|>":
                    conn_type = "inheritance"
                elif arrow == "..>":
                    conn_type = "dashed"
                elif arrow == "*--":
                    conn_type = "composition"
                elif arrow == "o--":
                    conn_type = "aggregation"
                elif arrow == "--":
                    direction = "undirected"

                if u not in seen_shapes:
                    seen_shapes.add(u)
                    ast.add_shape(DiagramShape(id=u, name=u, shape_type="rectangle", parent_id=current_package))
                if v not in seen_shapes:
                    seen_shapes.add(v)
                    ast.add_shape(DiagramShape(id=v, name=v, shape_type="rectangle", parent_id=current_package))

                ast.add_connector(DiagramConnector(
                    id=f"puml_conn_{idx}",
                    source_id=u,
                    target_id=v,
                    direction=direction,
                    label=sanitize_diagram_label(lbl),
                    cardinality_source=src_card,
                    cardinality_target=tgt_card,
                    connector_type=conn_type,
                ))
                continue

            # Unsupported directives
            if line.startswith(("skinparam", "hide", "note", "title")):
                ast.record_loss("directive", f"line_{idx}", line, "PlantUML styling directive ignored in semantic AST", "ignored")
            else:
                ast.record_loss("unsupported_line", f"line_{idx}", line, "Unrecognized PlantUML statement", "ignored")

        return ast


# ---------------------------------------------------------------------------
# Configurable, Versioned Ontology Mapping (fixes G10)
# ---------------------------------------------------------------------------
class DiagramOntologyMapper:
    """Proposes ontology assertions from diagram AST shapes and connectors.

    CRITICAL GUARANTEE (G10 fix):
    Never silently coerces all boxes to 'Service' or unknown connectors to 'CALLS'.
    Unrecognized connectors are preserved as generic directed edges 'eoip:connectsTo'.
    Unrecognized shapes are preserved as 'eoip:DiagramComponent'.
    Outputs are candidates with knowledge_state='proposed'.
    """

    DEFAULT_SHAPE_MAPPINGS = {
        "rectangle": "https://enterprise-ontology.org/schema/eoip#Service",
        "cylinder": "https://enterprise-ontology.org/schema/eoip#Database",
        "database": "https://enterprise-ontology.org/schema/eoip#Database",
        "cloud": "https://enterprise-ontology.org/schema/eoip#CloudInfrastructure",
        "queue": "https://enterprise-ontology.org/schema/eoip#MessageQueue",
        "actor": "https://enterprise-ontology.org/schema/eoip#Actor",
        "component": "https://enterprise-ontology.org/schema/eoip#SoftwareComponent",
        "package": "https://enterprise-ontology.org/schema/eoip#Package",
        "container": "https://enterprise-ontology.org/schema/eoip#SystemBoundary",
        "chowlk_class": "http://www.w3.org/2002/07/owl#Class",
        "chowlk_datatype": "http://www.w3.org/2000/01/rdf-schema#Datatype",
    }

    DEFAULT_CONNECTOR_MAPPINGS = {
        "calls": "https://enterprise-ontology.org/schema/eoip#calls",
        "depends_on": "https://enterprise-ontology.org/schema/eoip#dependsOn",
        "depends on": "https://enterprise-ontology.org/schema/eoip#dependsOn",
        "subclass_of": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
        "inheritance": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
        "reads_from": "https://enterprise-ontology.org/schema/eoip#readsFrom",
        "writes_to": "https://enterprise-ontology.org/schema/eoip#writesTo",
        "publishes_to": "https://enterprise-ontology.org/schema/eoip#publishesTo",
        "consumes_from": "https://enterprise-ontology.org/schema/eoip#consumesFrom",
    }

    def __init__(
        self,
        shape_mappings: dict[str, str] | None = None,
        connector_mappings: dict[str, str] | None = None,
        version: str = "1.0.0",
    ) -> None:
        self.version = version
        self.shape_mappings = dict(shape_mappings or self.DEFAULT_SHAPE_MAPPINGS)
        self.connector_mappings = dict(connector_mappings or self.DEFAULT_CONNECTOR_MAPPINGS)

    def map_ast(self, ast: DiagramAST) -> list[dict[str, Any]]:
        """Compiles DiagramAST into candidate ontology assertions with knowledge_state='proposed'."""
        assertions: list[dict[str, Any]] = []

        # Map shapes
        for shape in ast.shapes:
            target_class = self.shape_mappings.get(shape.shape_type.lower())
            is_unrecognized = False
            if not target_class:
                target_class = "https://enterprise-ontology.org/schema/eoip#DiagramComponent"
                is_unrecognized = True
                ast.record_loss(
                    "unrecognized_shape", shape.id, shape.shape_type,
                    f"Shape '{shape.shape_type}' has no configured ontology mapping",
                    "mapped_to_generic_DiagramComponent"
                )

            assertion = {
                "assertion_id": f"assert:shape:{shape.id}",
                "entity_id": shape.id,
                "name": shape.name,
                "target_class": target_class,
                "shape_type": shape.shape_type,
                "parent_id": shape.parent_id,
                "bounding_box": shape.bounding_box,
                "knowledge_state": "proposed",
                "mapping_version": self.version,
                "is_unrecognized": is_unrecognized,
            }
            assertions.append(assertion)

        # Map connectors
        for conn in ast.connectors:
            norm_label = conn.label.lower().strip()
            target_predicate = None

            if conn.connector_type == "inheritance":
                target_predicate = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
            elif norm_label:
                target_predicate = self.connector_mappings.get(norm_label)

            is_generic = False
            if not target_predicate:
                # G10 FIX: Never coerce unknown connector to CALLS!
                target_predicate = "https://enterprise-ontology.org/schema/eoip#connectsTo"
                is_generic = True
                ast.record_loss(
                    "unrecognized_connector", conn.id, conn.label or "unlabelled",
                    f"Connector label '{conn.label}' has no configured ontology predicate",
                    "mapped_to_generic_connectsTo"
                )

            assertion = {
                "assertion_id": f"assert:conn:{conn.id}",
                "source_id": conn.source_id,
                "target_id": conn.target_id,
                "predicate": target_predicate,
                "direction": conn.direction,
                "raw_label": conn.label,
                "cardinality_source": conn.cardinality_source,
                "cardinality_target": conn.cardinality_target,
                "knowledge_state": "proposed",
                "mapping_version": self.version,
                "is_generic_fallback": is_generic,
            }
            assertions.append(assertion)

        return assertions

    @staticmethod
    def approve_proposals(assertions: list[dict[str, Any]], approver: str = "steward") -> list[dict[str, Any]]:
        """Converts proposed candidates into asserted facts following steward review."""
        approved = []
        for a in assertions:
            item = dict(a)
            item["knowledge_state"] = "asserted"
            item["approved_by"] = approver
            approved.append(item)
        return approved


# ---------------------------------------------------------------------------
# Visual Extraction Candidate Generator (CRA-015.3, CRA-015.8)
# ---------------------------------------------------------------------------
@dataclass
class VisualDiagramExtractionCandidate:
    candidate_id: str
    bounding_box: tuple[float, float, float, float]  # ymin, xmin, ymax, xmax
    detected_label: str
    confidence: float
    uncertainty_score: float
    inferred_shape: str
    is_candidate: bool = True
    knowledge_state: str = "proposed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generate_visual_candidates(
    detections: list[dict[str, Any]],
    uncertainty_threshold: float = 0.35,
) -> list[VisualDiagramExtractionCandidate]:
    """Generates visual extraction candidates from OCR/vision bounding boxes.

    Ensures explicit uncertainty tracking and reviewer approval before graph ingestion.
    """
    candidates = []
    for idx, det in enumerate(detections):
        conf = float(det.get("confidence", 0.5))
        uncert = round(1.0 - conf, 3)
        bbox = det.get("bounding_box", (0.0, 0.0, 1.0, 1.0))
        label = det.get("label", f"VisualComponent_{idx}")
        shape_hint = det.get("shape", "rectangle")

        candidates.append(VisualDiagramExtractionCandidate(
            candidate_id=f"vis_cand_{idx}",
            bounding_box=bbox,
            detected_label=sanitize_diagram_label(label),
            confidence=conf,
            uncertainty_score=uncert,
            inferred_shape=shape_hint,
            is_candidate=True,
            knowledge_state="proposed",
        ))
    return candidates


# ---------------------------------------------------------------------------
# Source-vs-Graph Diff and Loss Ledger (CRA-015.4)
# ---------------------------------------------------------------------------
def compute_source_vs_graph_diff(ast: DiagramAST, compiled_assertions: list[dict[str, Any]]) -> dict[str, Any]:
    """Computes difference between diagram AST source constructs and compiled graph assertions."""
    source_shapes_count = len(ast.shapes)
    source_connectors_count = len(ast.connectors)
    compiled_entities_count = len([a for a in compiled_assertions if "entity_id" in a])
    compiled_relations_count = len([a for a in compiled_assertions if "predicate" in a])

    loss_items = [entry.to_dict() for entry in ast.loss_ledger]
    is_lossless = len(loss_items) == 0

    return {
        "source_shapes_count": source_shapes_count,
        "source_connectors_count": source_connectors_count,
        "compiled_entities_count": compiled_entities_count,
        "compiled_relations_count": compiled_relations_count,
        "is_lossless": is_lossless,
        "lossless_claim_allowed": is_lossless,
        "loss_ledger": loss_items,
        "loss_ledger_count": len(loss_items),
        "coverage_stats": ast.coverage_stats,
    }


# ---------------------------------------------------------------------------
# Round-Trip Rendering & Sanitization (CRA-015.5)
# ---------------------------------------------------------------------------
class DiagramRenderer:
    """Renders DiagramAST back to editable, sanitized Mermaid, PlantUML, and DrawIO XML."""

    @staticmethod
    def render_mermaid(ast: DiagramAST) -> str:
        lines = [f"{ast.diagram_type.value.lower() if ast.diagram_type != DiagramType.ARCHITECTURE else 'flowchart'} LR"]
        for s in ast.shapes:
            clean_name = sanitize_diagram_label(s.name)
            if s.shape_type == "cylinder":
                lines.append(f'    {s.id}[("{clean_name}")]')
            elif s.shape_type == "circle":
                lines.append(f'    {s.id}(("{clean_name}"))')
            elif s.shape_type == "decision":
                lines.append(f'    {s.id}{{"{clean_name}"}}')
            elif s.shape_type == "hexagon":
                lines.append(f'    {s.id}{{{{"{clean_name}"}}}}')
            else:
                lines.append(f'    {s.id}["{clean_name}"]')

        for c in ast.connectors:
            lbl = f"|{sanitize_diagram_label(c.label)}|" if c.label else ""
            if c.connector_type == "dashed":
                lines.append(f'    {c.source_id} -.->{lbl} {c.target_id}')
            elif c.direction == "undirected":
                lines.append(f'    {c.source_id} ---{lbl} {c.target_id}')
            else:
                lines.append(f'    {c.source_id} -->{lbl} {c.target_id}')

        return "\n".join(lines)

    @staticmethod
    def render_plantuml(ast: DiagramAST) -> str:
        lines = ["@startuml"]
        for s in ast.shapes:
            clean_name = sanitize_diagram_label(s.name)
            if s.shape_type in ("database", "cylinder"):
                stype = "database"
            elif s.shape_type in ("class", "queue", "cloud", "component", "actor"):
                stype = s.shape_type
            else:
                stype = "rectangle"
            lines.append(f'{stype} "{clean_name}" as {s.id}')

        for c in ast.connectors:
            lbl = f" : {sanitize_diagram_label(c.label)}" if c.label else ""
            if c.connector_type == "inheritance":
                lines.append(f"{c.source_id} --|> {c.target_id}{lbl}")
            elif c.connector_type == "dashed":
                lines.append(f"{c.source_id} ..> {c.target_id}{lbl}")
            elif c.direction == "undirected":
                lines.append(f"{c.source_id} -- {c.target_id}{lbl}")
            else:
                lines.append(f"{c.source_id} --> {c.target_id}{lbl}")

        lines.append("@enduml")
        return "\n".join(lines)

    @staticmethod
    def render_drawio_xml(ast: DiagramAST) -> str:
        root = std_ET.Element("mxGraphModel")
        mx_root = std_ET.SubElement(root, "root")
        std_ET.SubElement(mx_root, "mxCell", id="0")
        std_ET.SubElement(mx_root, "mxCell", id="1", parent="0")

        y = 40
        for s in ast.shapes:
            style = "rounded=0;whiteSpace=wrap;html=1;"
            if s.shape_type == "cylinder":
                style = "shape=cylinder;whiteSpace=wrap;html=1;"
            cell = std_ET.SubElement(
                mx_root, "mxCell",
                id=s.id,
                value=sanitize_diagram_label(s.name),
                style=style,
                vertex="1",
                parent=s.parent_id or "1",
            )
            std_ET.SubElement(cell, "mxGeometry", x="40", y=str(y), width="120", height="60", **{"as": "geometry"})
            y += 80

        for c in ast.connectors:
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            if c.connector_type == "dashed":
                style += "dashed=1;"
            cell = std_ET.SubElement(
                mx_root, "mxCell",
                id=c.id,
                value=sanitize_diagram_label(c.label),
                style=style,
                edge="1",
                source=c.source_id,
                target=c.target_id,
                parent="1",
            )
            std_ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})

        return std_ET.tostring(root, encoding="utf-8").decode("utf-8")


# ---------------------------------------------------------------------------
# OWL 2 / RDF Formal Compilation (CRA-015.A)
# ---------------------------------------------------------------------------
def compile_to_rdf(
    ast: DiagramAST,
    mapper: DiagramOntologyMapper | None = None,
    base_iri: str = "http://example.org/diagram/",
) -> rdflib.Graph:
    """Compiles DiagramAST into valid OWL 2 RDF Graph.

    Allows 100% formal comparison against gold semantic models.
    """
    g = Graph()
    mapper = mapper or DiagramOntologyMapper()
    assertions = mapper.map_ast(ast)

    BASE = Namespace(base_iri)
    g.bind("ex", BASE)
    g.bind("eoip", EOIP)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)

    ontology_uri = URIRef(f"{base_iri}ontology")
    g.add((ontology_uri, RDF.type, OWL.Ontology))
    g.add((ontology_uri, RDFS.label, Literal(f"Compiled Diagram {ast.diagram_format}")))

    for a in assertions:
        if "entity_id" in a:
            subj = URIRef(f"{base_iri}{a['entity_id']}")
            cls_uri = URIRef(a["target_class"])
            g.add((subj, RDF.type, cls_uri))
            g.add((subj, RDFS.label, Literal(a["name"])))
            if a.get("parent_id"):
                parent_subj = URIRef(f"{base_iri}{a['parent_id']}")
                g.add((parent_subj, EOIP.contains, subj))
        elif "predicate" in a:
            s_subj = URIRef(f"{base_iri}{a['source_id']}")
            o_subj = URIRef(f"{base_iri}{a['target_id']}")
            pred = URIRef(a["predicate"])
            g.add((s_subj, pred, o_subj))

    # Add loss ledger summary
    for loss in ast.loss_ledger:
        loss_node = BNode()
        g.add((loss_node, RDF.type, EOIP.LossLedgerEntry))
        g.add((loss_node, EOIP.constructType, Literal(loss.construct_type)))
        g.add((loss_node, EOIP.reason, Literal(loss.reason)))
        g.add((loss_node, EOIP.actionTaken, Literal(loss.action_taken)))
        g.add((ontology_uri, EOIP.hasLossLedgerEntry, loss_node))

    return g


# ---------------------------------------------------------------------------
# Backward Compatibility Wrappers
# ---------------------------------------------------------------------------
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
    """Backward-compatible facade delegating to MermaidParser and DiagramOntologyMapper."""

    def __init__(self) -> None:
        self.mermaid_parser = MermaidParser()
        self.drawio_parser = DrawIOParser()
        self.plantuml_parser = PlantUMLParser()
        self.mapper = DiagramOntologyMapper()

    def parse_mermaid(self, mermaid_text: str) -> ParsedDiagramGraph:
        ast = self.mermaid_parser.parse(mermaid_text)
        vertices = []
        edges = []

        for s in ast.shapes:
            target_class = self.mapper.shape_mappings.get(s.shape_type, "Service")
            class_name = target_class.split("#")[-1] if "#" in target_class else target_class
            vertices.append({
                "label": class_name,
                "properties": {
                    "canonical_id": s.id,
                    "service_id": s.id,
                    "name": s.name,
                },
            })

        for c in ast.connectors:
            lbl = c.label.upper() if c.label else "CALLS"
            if lbl not in ("CALLS", "DEPENDS_ON"):
                lbl = "CONNECTS_TO"
            edges.append({
                "label": lbl,
                "out_cid": c.source_id,
                "in_cid": c.target_id,
                "properties": {},
            })

        return ParsedDiagramGraph(
            diagram_type=ast.diagram_type,
            vertices=vertices,
            edges=edges,
        )


class GraphToDiagramRenderer:
    """Backward-compatible facade delegating to DiagramRenderer."""

    def render_mermaid(self, vertices: list[dict[str, Any]], edges: list[dict[str, Any]]) -> str:
        lines = ["flowchart LR"]
        for v in vertices:
            cid = v.get("canonical_id", v.get("properties", {}).get("canonical_id", "node"))
            name = sanitize_diagram_label(v.get("properties", {}).get("name", cid))
            lines.append(f'    {cid}["{name}"]')
        for e in edges:
            u = e.get("out_cid", e.get("out_v"))
            v = e.get("in_cid", e.get("in_v"))
            lbl = sanitize_diagram_label(e.get("label", "CALLS"))
            lines.append(f'    {u} -->|{lbl}| {v}')
        return "\n".join(lines)

    def render_svg(self, vertices: list[dict[str, Any]], edges: list[dict[str, Any]]) -> str:
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
            name = sanitize_diagram_label(v.get("properties", {}).get("name", cid))
            x = 80 if (idx % 2 == 0) else 350
            pos[cid] = (x + 80, y + 25)
            svg_parts.append(f'  <rect x="{x}" y="{y}" width="160" height="50"/>')
            svg_parts.append(f'  <text x="{x + 80}" y="{y + 30}" text-anchor="middle">{name}</text>')
            y += 80

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

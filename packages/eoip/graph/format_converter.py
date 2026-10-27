"""Graph format converter: JSON to RDF, RDFS, OWL, Gremlin, Cypher, GQL, SPARQL,
OpenCypher, SHACL, PGQL.

Converts EOIP graph data (vertices + edges) into industry-standard
graph serialization formats for interoperability and export.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET

from eoip.graph.store import GraphStore

EOIP_NS = "urn:eoip:ontology:"
EOIP_DATA_NS = "urn:eoip:data:"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NS = "http://www.w3.org/2000/01/rdf-schema#"
OWL_NS = "http://www.w3.org/2002/07/owl#"
XSD_NS = "http://www.w3.org/2001/XMLSchema#"


def _escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _escape_sparql(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


_PGQL_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _pgql_identifier(name: str) -> str:
    if not _PGQL_IDENT.fullmatch(name):
        raise ValueError(f"unsafe PGQL identifier: {name!r}")
    return name


def _pgql_literal(value: object) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _safe_uri(value: str) -> str:
    return value.replace(" ", "_").replace("/", "_").replace(":", "_")


class FormatConverter:
    """Converts EOIP graph data to multiple output formats."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    def _load_graph(self, limit: int = 50_000) -> tuple[list[dict], list[dict]]:
        vertices = self._store.find_vertices(limit=limit)
        edges = []
        vid_to_cid: dict[str, str] = {}
        for v in vertices:
            vid_to_cid[v["vid"]] = v["properties"].get("canonical_id", v["vid"])
        for v in vertices:
            for e in self._store.edges_from(v["vid"]):
                edges.append({
                    "label": e.get("label", "RELATED_TO"),
                    "from_cid": vid_to_cid.get(e["out_v"], e["out_v"]),
                    "to_cid": vid_to_cid.get(e["in_v"], e["in_v"]),
                    "properties": e.get("properties", {}),
                })
        return vertices, edges

    def to_rdf_turtle(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        lines = [
            f"@prefix eoip: <{EOIP_NS}> .",
            f"@prefix data: <{EOIP_DATA_NS}> .",
            f"@prefix rdf: <{RDF_NS}> .",
            f"@prefix rdfs: <{RDFS_NS}> .",
            f"@prefix xsd: <{XSD_NS}> .",
            "",
        ]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            uri = f"data:{_safe_uri(cid)}"
            lines.append(f'{uri} rdf:type eoip:{v["label"]} ;')
            lines.append(f'    rdfs:label "{_escape_sparql(v["properties"].get("name", cid))}" ;')
            props = v.get("properties", {})
            for k, val in props.items():
                if k in ("canonical_id",):
                    continue
                if isinstance(val, (int, float)):
                    lines.append(f'    eoip:{k} {val} ;')
                elif isinstance(val, str):
                    lines.append(f'    eoip:{k} "{_escape_sparql(val)}" ;')
            if lines[-1].endswith(" ;"):
                lines[-1] = lines[-1][:-2] + " ."
            lines.append("")

        for e in edges:
            src = f"data:{_safe_uri(e['from_cid'])}"
            tgt = f"data:{_safe_uri(e['to_cid'])}"
            lines.append(f"{src} eoip:{e['label']} {tgt} .")

        return "\n".join(lines)

    def to_rdf_xml(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        root = ET.Element("rdf:RDF")
        root.set("xmlns:rdf", RDF_NS)
        root.set("xmlns:rdfs", RDFS_NS)
        root.set("xmlns:eoip", EOIP_NS)

        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            desc = ET.SubElement(root, "rdf:Description")
            desc.set("rdf:about", f"{EOIP_DATA_NS}{_safe_uri(cid)}")
            rtype = ET.SubElement(desc, "rdf:type")
            rtype.set("rdf:resource", f"{EOIP_NS}{v['label']}")
            label_el = ET.SubElement(desc, "rdfs:label")
            label_el.text = v["properties"].get("name", cid)
            for k, val in v.get("properties", {}).items():
                if k == "canonical_id":
                    continue
                prop_el = ET.SubElement(desc, f"eoip:{k}")
                prop_el.text = str(val)

        for e in edges:
            desc = ET.SubElement(root, "rdf:Description")
            desc.set("rdf:about", f"{EOIP_DATA_NS}{_safe_uri(e['from_cid'])}")
            rel = ET.SubElement(desc, f"eoip:{e['label']}")
            rel.set("rdf:resource", f"{EOIP_DATA_NS}{_safe_uri(e['to_cid'])}")

        return ET.tostring(root, encoding="unicode", xml_declaration=True)

    def to_rdfs(self, limit: int = 50_000) -> str:
        vertices, _ = self._load_graph(limit)
        labels = set()
        edge_labels = set()
        for v in vertices:
            labels.add(v["label"])
            for e in self._store.edges_from(v["vid"]):
                edge_labels.add(e.get("label", "RELATED_TO"))

        lines = [
            f"@prefix rdfs: <{RDFS_NS}> .",
            f"@prefix rdf: <{RDF_NS}> .",
            f"@prefix eoip: <{EOIP_NS}> .",
            "",
            "# RDFS Class definitions",
        ]
        for label in sorted(labels):
            lines.append(f"eoip:{label} rdf:type rdfs:Class ;")
            lines.append(f'    rdfs:label "{label}" .')
            lines.append("")

        lines.append("# RDFS Property definitions")
        for el in sorted(edge_labels):
            lines.append(f"eoip:{el} rdf:type rdf:Property ;")
            lines.append(f'    rdfs:label "{el}" .')
            lines.append("")

        return "\n".join(lines)

    def to_owl(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        labels = set()
        edge_labels = set()
        for v in vertices:
            labels.add(v["label"])
        for e in edges:
            edge_labels.add(e["label"])

        lines = [
            f"@prefix owl: <{OWL_NS}> .",
            f"@prefix rdf: <{RDF_NS}> .",
            f"@prefix rdfs: <{RDFS_NS}> .",
            f"@prefix eoip: <{EOIP_NS}> .",
            "",
            f"<{EOIP_NS}> rdf:type owl:Ontology ;",
            '    rdfs:label "EOIP Enterprise Ontology" .',
            "",
        ]
        for label in sorted(labels):
            lines.append(f"eoip:{label} rdf:type owl:Class ;")
            lines.append(f'    rdfs:label "{label}" .')
            lines.append("")

        for el in sorted(edge_labels):
            lines.append(f"eoip:{el} rdf:type owl:ObjectProperty ;")
            lines.append(f'    rdfs:label "{el}" .')
            lines.append("")

        return "\n".join(lines)

    def to_gremlin(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        lines = ["// Gremlin traversal script generated by EOIP", ""]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            props_str = ""
            for k, val in v.get("properties", {}).items():
                if isinstance(val, str):
                    props_str += f".property('{k}', '{_escape_sparql(val)}')"
                elif isinstance(val, (int, float)):
                    props_str += f".property('{k}', {val})"
            lines.append(
                f"g.addV('{v['label']}').property('canonical_id', '{_safe_uri(cid)}'){props_str}"
            )

        lines.append("")
        for e in edges:
            src = _safe_uri(e["from_cid"])
            tgt = _safe_uri(e["to_cid"])
            lines.append(
                f"g.V().has('canonical_id', '{src}').addE('{e['label']}').to(g.V().has('canonical_id', '{tgt}'))"
            )

        return "\n".join(lines)

    def to_cypher(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        lines = ["// Cypher script generated by EOIP", ""]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            props = {**v.get("properties", {}), "canonical_id": cid}
            props_str = ", ".join(
                f'{k}: {json.dumps(val)}' for k, val in props.items()
                if isinstance(val, (str, int, float, bool))
            )
            lines.append(
                f'MERGE (n:{v["label"]} {{canonical_id: {json.dumps(cid)}}}) SET n += {{{props_str}}};'
            )

        lines.append("")
        for e in edges:
            lines.append(
                f'MATCH (a {{canonical_id: {json.dumps(e["from_cid"])}}}), '
                f'(b {{canonical_id: {json.dumps(e["to_cid"])}}}) '
                f'MERGE (a)-[:{e["label"]}]->(b);'
            )

        return "\n".join(lines)

    def to_gql(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        lines = ["-- GQL (ISO/IEC 39075) script generated by EOIP", ""]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            props = {**v.get("properties", {}), "canonical_id": cid}
            props_str = ", ".join(
                f'{k}: {json.dumps(val)}' for k, val in props.items()
                if isinstance(val, (str, int, float, bool))
            )
            lines.append(
                f'INSERT (:"{v["label"]}" {{{props_str}}});'
            )

        lines.append("")
        for e in edges:
            lines.append(
                f'MATCH (a {{canonical_id: {json.dumps(e["from_cid"])}}}), '
                f'(b {{canonical_id: {json.dumps(e["to_cid"])}}}) '
                f'INSERT (a)-[:"{e["label"]}"]->(b);'
            )

        return "\n".join(lines)

    def to_sparql_insert(self, limit: int = 50_000) -> str:
        vertices, edges = self._load_graph(limit)
        lines = [
            f"PREFIX eoip: <{EOIP_NS}>",
            f"PREFIX data: <{EOIP_DATA_NS}>",
            f"PREFIX rdf: <{RDF_NS}>",
            f"PREFIX rdfs: <{RDFS_NS}>",
            "",
            "INSERT DATA {",
        ]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            uri = f"data:{_safe_uri(cid)}"
            lines.append(f"  {uri} rdf:type eoip:{v['label']} .")
            name = v["properties"].get("name", cid)
            lines.append(f'  {uri} rdfs:label "{_escape_sparql(name)}" .')
            for k, val in v.get("properties", {}).items():
                if k == "canonical_id":
                    continue
                if isinstance(val, (int, float)):
                    lines.append(f"  {uri} eoip:{k} {val} .")
                elif isinstance(val, str):
                    lines.append(f'  {uri} eoip:{k} "{_escape_sparql(val)}" .')

        for e in edges:
            src = f"data:{_safe_uri(e['from_cid'])}"
            tgt = f"data:{_safe_uri(e['to_cid'])}"
            lines.append(f"  {src} eoip:{e['label']} {tgt} .")

        lines.append("}")
        return "\n".join(lines)

    def to_opencypher(self, limit: int = 50_000) -> str:
        """OpenCypher (ISO standardized Cypher) export."""
        vertices, edges = self._load_graph(limit)
        lines = ["// OpenCypher script generated by EOIP", ""]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            props = {**v.get("properties", {}), "canonical_id": cid}
            props_str = ", ".join(
                f'{k}: {json.dumps(val)}' for k, val in props.items()
                if isinstance(val, (str, int, float, bool))
            )
            lines.append(
                f'MERGE (n:{v["label"]} {{canonical_id: {json.dumps(cid)}}}) '
                f'SET n = {{{props_str}}}'
            )

        lines.append("")
        for e in edges:
            lines.append(
                f'MATCH (a {{canonical_id: {json.dumps(e["from_cid"])}}}), '
                f'(b {{canonical_id: {json.dumps(e["to_cid"])}}}) '
                f'MERGE (a)-[:{e["label"]}]->(b)'
            )

        return "\n".join(lines)

    def to_shacl(self, limit: int = 50_000) -> str:
        """Generate SHACL shapes from the ontology schema."""
        vertices, edges = self._load_graph(limit)
        labels = set()
        edge_labels = set()
        label_props: dict[str, set[str]] = {}
        for v in vertices:
            lbl = v["label"]
            labels.add(lbl)
            if lbl not in label_props:
                label_props[lbl] = set()
            for k in v.get("properties", {}):
                if k != "canonical_id":
                    label_props[lbl].add(k)
        for e in edges:
            edge_labels.add(e["label"])

        SHACL_NS = "http://www.w3.org/ns/shacl#"
        lines = [
            f"@prefix sh: <{SHACL_NS}> .",
            f"@prefix eoip: <{EOIP_NS}> .",
            f"@prefix rdf: <{RDF_NS}> .",
            f"@prefix rdfs: <{RDFS_NS}> .",
            f"@prefix xsd: <{XSD_NS}> .",
            "",
        ]
        for lbl in sorted(labels):
            shape_uri = f"eoip:{lbl}Shape"
            lines.append(f"{shape_uri} a sh:NodeShape ;")
            lines.append(f"    sh:targetClass eoip:{lbl} ;")
            lines.append(f'    rdfs:label "{lbl} shape" ;')
            lines.append("    sh:property [")
            lines.append("        sh:path eoip:canonical_id ;")
            lines.append("        sh:datatype xsd:string ;")
            lines.append("        sh:minCount 1 ;")
            lines.append("        sh:maxCount 1 ;")
            lines.append("    ] ;")
            for prop in sorted(label_props.get(lbl, set())):
                lines.append("    sh:property [")
                lines.append(f"        sh:path eoip:{prop} ;")
                lines.append("        sh:datatype xsd:string ;")
                lines.append("    ] ;")
            lines[-1] = lines[-1].rstrip(" ;") + " ."
            lines.append("")

        return "\n".join(lines)

    def to_pgql(self, limit: int = 50_000) -> str:
        """PGQL (Property Graph Query Language) export — Oracle-style INSERT statements."""
        vertices, edges = self._load_graph(limit)
        lines = ["-- PGQL (Oracle) script generated by EOIP", ""]
        for v in vertices:
            cid = v["properties"].get("canonical_id", v["vid"])
            props = {**v.get("properties", {}), "canonical_id": cid}
            assignments = ", ".join(
                f'n.{_pgql_identifier(str(k))} = {_pgql_literal(val)}' for k, val in props.items()
                if isinstance(val, (str, int, float, bool))
            )
            lines.append(
                f"INSERT INTO graph VERTEX n LABELS ({_pgql_identifier(str(v['label']))}) "
                f"PROPERTIES ({assignments})"
            )

        lines.append("")
        for e in edges:
            lines.append(
                f"INSERT INTO graph EDGE e BETWEEN "  # nosec B608 - identifiers whitelist-validated, values escaped as SQL literals
                f"(SELECT n FROM graph MATCH (n) WHERE n.canonical_id = {_pgql_literal(e['from_cid'])}) AND "
                f"(SELECT n FROM graph MATCH (n) WHERE n.canonical_id = {_pgql_literal(e['to_cid'])}) "
                f"LABELS ({_pgql_identifier(str(e['label']))})"
            )

        return "\n".join(lines)

    def convert(self, format_id: str, limit: int = 50_000) -> str:
        converters = {
            "rdf": self.to_rdf_turtle,
            "rdf_xml": self.to_rdf_xml,
            "rdfs": self.to_rdfs,
            "owl": self.to_owl,
            "gremlin": self.to_gremlin,
            "cypher": self.to_cypher,
            "opencypher": self.to_opencypher,
            "gql": self.to_gql,
            "sparql": self.to_sparql_insert,
            "shacl": self.to_shacl,
            "pgql": self.to_pgql,
        }
        fn = converters.get(format_id)
        if fn is None:
            raise ValueError(f"Unknown format: {format_id}. Available: {list(converters.keys())}")
        return fn(limit=limit)

    @staticmethod
    def available_formats() -> list[dict[str, str]]:
        return [
            {"id": "rdf", "label": "RDF (Turtle)", "ext": ".ttl", "desc": "W3C RDF in Turtle syntax"},
            {"id": "rdf_xml", "label": "RDF/XML", "ext": ".rdf", "desc": "W3C RDF in XML syntax"},
            {"id": "rdfs", "label": "RDFS Schema", "ext": ".ttl", "desc": "RDFS class and property definitions"},
            {"id": "owl", "label": "OWL Ontology", "ext": ".owl", "desc": "OWL ontology with classes and object properties"},
            {"id": "gremlin", "label": "Gremlin Script", "ext": ".groovy", "desc": "Apache TinkerPop Gremlin traversal"},
            {"id": "cypher", "label": "Cypher Script", "ext": ".cypher", "desc": "Neo4j Cypher MERGE statements"},
            {"id": "opencypher", "label": "OpenCypher Script", "ext": ".cypher", "desc": "Vendor-neutral OpenCypher statements"},
            {"id": "gql", "label": "GQL Script", "ext": ".gql", "desc": "ISO GQL INSERT statements"},
            {"id": "sparql", "label": "SPARQL INSERT", "ext": ".sparql", "desc": "SPARQL INSERT DATA for RDF stores"},
            {"id": "shacl", "label": "SHACL Shapes", "ext": ".ttl", "desc": "W3C SHACL node shapes"},
            {"id": "pgql", "label": "PGQL Script", "ext": ".pgql", "desc": "Property Graph Query Language export"},
        ]

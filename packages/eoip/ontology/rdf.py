"""Dual RDF/OWL/SHACL mapping for EOIP's controlled graph vocabulary."""

from __future__ import annotations

from collections import Counter
from typing import Any
from urllib.parse import quote, unquote

from eoip.ontology.manifest import (
    EDGE_LABELS,
    ONTOLOGY_VERSION,
    PROPERTY_KEYS,
    VERTEX_LABELS,
    edge_endpoints_valid,
)

EOIP_NAMESPACE = "urn:eoip:ontology:"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
OWL_NAMESPACE = "http://www.w3.org/2002/07/owl#"
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"
SHACL_NAMESPACE = "http://www.w3.org/ns/shacl#"


def _property_term(name: str) -> str:
    return f"property_{quote(name, safe='')}"


def _property_name(term: str) -> str | None:
    if not term.startswith("property_"):
        return None
    return unquote(term.removeprefix("property_"))


def _property_type(value: object) -> str | None:
    if isinstance(value, (dict, list)):
        return "@json"
    return None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _entity_label(types: Any) -> str | None:
    for item in _as_list(types):
        if isinstance(item, str) and item.startswith("eoip:entity/"):
            return unquote(item.removeprefix("eoip:entity/"))
    return None


def _relation_label(predicate: Any) -> str | None:
    if not isinstance(predicate, str) or not predicate.startswith("eoip:relation/"):
        return None
    return unquote(predicate.removeprefix("eoip:relation/"))


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _decode_property_terms(item: dict[str, Any], losses: Counter[tuple[str, str]]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    for term, value in item.items():
        name = _property_name(term)
        if name is None:
            continue
        if name not in PROPERTY_KEYS:
            losses[("unsupported_property", name)] += 1
            continue
        properties[name] = value
    return properties


def export_jsonld(store, limit: int = 5000) -> dict:
    """Export ontology and graph records as JSON-LD, bounded by ``limit`` per kind."""
    if not 1 <= limit <= 10_000:
        raise ValueError("JSON-LD export limit must be between 1 and 10000")

    vertices = store.find_vertices(limit=limit + 1)
    edges = store.find_edges(limit=limit + 1)
    partial_vertices = len(vertices) > limit
    partial_edges = len(edges) > limit
    vertices = vertices[:limit]
    edges = edges[:limit]
    included_vertex_ids = {vertex["canonical_id"] for vertex in vertices}

    property_names = set(PROPERTY_KEYS)
    property_values: dict[str, list[object]] = {}
    for record in [*vertices, *edges]:
        for name, value in record["properties"].items():
            property_names.add(name)
            property_values.setdefault(name, []).append(value)

    context = {
        "eoip": EOIP_NAMESPACE,
        "rdf": RDF_NAMESPACE,
        "rdfs": RDFS_NAMESPACE,
        "owl": OWL_NAMESPACE,
        "xsd": XSD_NAMESPACE,
        "canonical_id": "eoip:canonicalId",
        "ontologyVersion": "eoip:ontologyVersion",
        "graphDomain": "eoip:graphDomain",
        "requiredProperty": "eoip:requiredProperty",
        "optionalProperty": "eoip:optionalProperty",
        "allowedEndpointPairs": {"@id": "eoip:allowedEndpointPairs", "@type": "@json"},
        "usedByEntityLabel": "eoip:usedByEntityLabel",
        "export": {"@id": "eoip:exportMetadata", "@type": "@json"},
        "rdfs:label": "rdfs:label",
        "rdfs:range": {"@id": "rdfs:range", "@type": "@id"},
        "rdf:subject": {"@id": "rdf:subject", "@type": "@id"},
        "rdf:predicate": {"@id": "rdf:predicate", "@type": "@id"},
        "rdf:object": {"@id": "rdf:object", "@type": "@id"},
    }
    for name in sorted(property_names):
        term = _property_term(name)
        definition = {"@id": f"eoip:property/{quote(name, safe='')}"}
        if any(_property_type(value) == "@json" for value in property_values.get(name, [])):
            definition["@type"] = "@json"
        context[term] = definition

    ontology_graph: list[dict] = [
        {
            "@id": "urn:eoip:ontology",
            "@type": "owl:Ontology",
            "ontologyVersion": ONTOLOGY_VERSION,
        },
        {"@id": "eoip:Entity", "@type": "owl:Class", "rdfs:label": "Entity"},
        {
            "@id": "eoip:exportMetadata",
            "@type": "owl:DatatypeProperty",
            "rdfs:label": "export metadata",
            "rdfs:range": "rdf:JSON",
        },
    ]
    for label, (domain, required, optional) in sorted(VERTEX_LABELS.items()):
        ontology_graph.append(
            {
                "@id": f"eoip:entity/{label}",
                "@type": "owl:Class",
                "rdfs:label": label,
                "graphDomain": domain,
                "requiredProperty": required,
                "optionalProperty": optional,
            }
        )
    for label, (out_labels, in_labels, _) in sorted(EDGE_LABELS.items()):
        ontology_graph.append(
            {
                "@id": f"eoip:relation/{label}",
                "@type": "owl:ObjectProperty",
                "rdfs:label": label,
                "allowedEndpointPairs": [
                    [out_label, in_label] for out_label in out_labels for in_label in in_labels
                ],
            }
        )
    for name, data_type in sorted(PROPERTY_KEYS.items()):
        used_by = [
            label
            for label, (_, required, optional) in VERTEX_LABELS.items()
            if name in required or name in optional
        ]
        datatype = {
            "TEXT": "xsd:string",
            "DATE": "xsd:string",
            "INT": "xsd:integer",
            "LONG": "xsd:integer",
            "DOUBLE": "xsd:double",
            "BOOLEAN": "xsd:boolean",
        }[data_type]
        ontology_graph.append(
            {
                "@id": f"eoip:property/{quote(name, safe='')}",
                "@type": "owl:DatatypeProperty",
                "rdfs:label": name,
                "rdfs:range": datatype,
                "usedByEntityLabel": used_by,
            }
        )

    losses: Counter[tuple[str, str]] = Counter()
    data_graph: list[dict] = []
    vertices_by_cid = {vertex["canonical_id"]: vertex for vertex in vertices}
    data_nodes_by_cid: dict[str, dict] = {}
    for vertex in vertices:
        label = vertex["label"]
        if label not in VERTEX_LABELS:
            losses[("unsupported_vertex_label", label)] += 1
            rdf_type = "eoip:Entity"
        else:
            rdf_type = f"eoip:entity/{label}"
        for name in vertex["properties"]:
            if name not in PROPERTY_KEYS:
                losses[("unsupported_property", name)] += 1
        item = {
            "@id": vertex["canonical_id"],
            "@type": ["owl:NamedIndividual", rdf_type],
            "canonical_id": vertex["canonical_id"],
        }
        item.update({_property_term(name): value for name, value in vertex["properties"].items()})
        data_graph.append(item)
        data_nodes_by_cid[vertex["canonical_id"]] = item

    for edge in edges:
        label = edge["label"]
        relation = f"eoip:relation/{quote(label, safe='')}"
        if label not in EDGE_LABELS:
            losses[("unsupported_edge_label", label)] += 1
        for name in edge["properties"]:
            if name not in PROPERTY_KEYS:
                losses[("unsupported_property", name)] += 1
        if edge["out_cid"] not in included_vertex_ids or edge["in_cid"] not in included_vertex_ids:
            losses[("edge_endpoint_not_in_export", label)] += 1
        if edge["out_cid"] in vertices_by_cid:
            source_node = data_nodes_by_cid[edge["out_cid"]]
            relation_term = f"relation_{quote(label, safe='')}"
            context[relation_term] = {"@id": relation, "@type": "@id"}
            source_node.setdefault(relation_term, []).append({"@id": edge["in_cid"]})

        edge_id = edge["properties"].get("edge_key") or edge["eid"]
        assertion = {
            "@id": f"urn:eoip:edge:{quote(str(edge_id), safe='')}",
            "@type": "eoip:RelationshipAssertion",
            "rdf:subject": edge["out_cid"],
            "rdf:predicate": relation,
            "rdf:object": edge["in_cid"],
        }
        assertion.update({_property_term(name): value for name, value in edge["properties"].items()})
        data_graph.append(assertion)

    return {
        "@context": context,
        "@graph": [*ontology_graph, *data_graph],
        "export": {
            "format": "JSON-LD 1.1",
            "ontology_version": ONTOLOGY_VERSION,
            "limit_per_kind": limit,
            "vertices_included": len(vertices),
            "edges_included": len(edges),
            "partial": partial_vertices or partial_edges,
            "truncated_vertices": partial_vertices,
            "truncated_edges": partial_edges,
            "mapping_losses": [
                {"kind": kind, "label": label, "count": count}
                for (kind, label), count in sorted(losses.items())
            ],
        },
    }


def jsonld_to_property_graph(document: dict[str, Any]) -> dict[str, Any]:
    """Map supported EOIP JSON-LD records back into property-graph records.

    The importer deliberately ignores ontology declaration nodes and direct
    relation triples; relationship assertions are the lossless carrier because
    they preserve edge attributes.
    """
    graph = document.get("@graph")
    if not isinstance(graph, list):
        raise TypeError("JSON-LD document must contain an @graph list")

    losses: Counter[tuple[str, str]] = Counter()
    vertices: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    vertex_ids: set[str] = set()

    for item in graph:
        if not isinstance(item, dict):
            losses[("unsupported_jsonld_item", type(item).__name__)] += 1
            continue
        types = _as_list(item.get("@type"))
        if "eoip:RelationshipAssertion" in types:
            continue
        if "owl:NamedIndividual" not in types:
            continue

        label = _entity_label(types)
        canonical_id = item.get("canonical_id") or item.get("@id")
        if label not in VERTEX_LABELS:
            losses[("unsupported_vertex_label", str(label or ""))] += 1
            continue
        if _is_missing(canonical_id):
            losses[("missing_canonical_id", label)] += 1
            continue

        properties = _decode_property_terms(item, losses)
        properties["canonical_id"] = canonical_id
        vertices.append(
            {
                "label": label,
                "canonical_id": canonical_id,
                "properties": properties,
            }
        )
        vertex_ids.add(canonical_id)

    for item in graph:
        if not isinstance(item, dict) or "eoip:RelationshipAssertion" not in _as_list(item.get("@type")):
            continue

        label = _relation_label(item.get("rdf:predicate"))
        out_cid = item.get("rdf:subject")
        in_cid = item.get("rdf:object")
        if label not in EDGE_LABELS:
            losses[("unsupported_edge_label", str(label or ""))] += 1
            continue
        if _is_missing(out_cid) or _is_missing(in_cid):
            losses[("missing_edge_endpoint", label)] += 1
            continue
        if out_cid not in vertex_ids or in_cid not in vertex_ids:
            losses[("edge_endpoint_not_in_document", label)] += 1
            continue

        properties = _decode_property_terms(item, losses)
        edges.append(
            {
                "label": label,
                "out_cid": out_cid,
                "in_cid": in_cid,
                "properties": properties,
            }
        )

    return {
        "vertices": vertices,
        "edges": edges,
        "mapping_losses": [
            {"kind": kind, "label": label, "count": count}
            for (kind, label), count in sorted(losses.items())
        ],
    }


def import_jsonld(document: dict[str, Any], store, *, clear: bool = False) -> dict[str, Any]:
    """Import supported EOIP JSON-LD records into a property-graph store."""
    mapped = jsonld_to_property_graph(document)
    if clear:
        if not hasattr(store, "clear"):
            raise RuntimeError("target graph store does not support clearing before JSON-LD import")
        store.clear()

    vertices_by_cid: dict[str, dict] = {}
    for vertex in mapped["vertices"]:
        created = store.upsert_vertex(vertex["label"], vertex["properties"])
        vertices_by_cid[vertex["canonical_id"]] = created

    imported_edges = 0
    skipped_edges = 0
    for edge in mapped["edges"]:
        out_vertex = vertices_by_cid.get(edge["out_cid"]) or store.get_vertex_by_canonical_id(edge["out_cid"])
        in_vertex = vertices_by_cid.get(edge["in_cid"]) or store.get_vertex_by_canonical_id(edge["in_cid"])
        if out_vertex is None or in_vertex is None:
            skipped_edges += 1
            continue
        store.upsert_edge(edge["label"], out_vertex["vid"], in_vertex["vid"], edge["properties"])
        imported_edges += 1

    return {
        "vertices": len(vertices_by_cid),
        "edges": imported_edges,
        "skipped_edges": skipped_edges,
        "mapping_losses": mapped["mapping_losses"],
    }


def export_shacl_shapes() -> dict[str, Any]:
    """Export manifest-derived SHACL node and relationship shapes as JSON-LD."""
    graph: list[dict[str, Any]] = [
        {
            "@id": "urn:eoip:shacl",
            "@type": "owl:Ontology",
            "ontologyVersion": ONTOLOGY_VERSION,
        }
    ]
    for label, (_domain, required, optional) in sorted(VERTEX_LABELS.items()):
        graph.append(
            {
                "@id": f"eoip:shape/{label}",
                "@type": "sh:NodeShape",
                "sh:targetClass": f"eoip:entity/{label}",
                "sh:property": [
                    {
                        "sh:path": f"eoip:property/{quote(name, safe='')}",
                        "sh:minCount": 1,
                    }
                    for name in required
                ],
                "optionalProperty": optional,
            }
        )
    for label, (out_labels, in_labels, properties) in sorted(EDGE_LABELS.items()):
        graph.append(
            {
                "@id": f"eoip:shape/relation/{label}",
                "@type": "eoip:RelationshipShape",
                "sh:path": f"eoip:relation/{quote(label, safe='')}",
                "allowedEndpointPairs": [
                    [out_label, in_label] for out_label in out_labels for in_label in in_labels
                ],
                "sh:property": [
                    {
                        "sh:path": f"eoip:property/{quote(name, safe='')}",
                        "sh:minCount": 1,
                    }
                    for name in properties
                ],
            }
        )
    return {
        "@context": {
            "eoip": EOIP_NAMESPACE,
            "owl": OWL_NAMESPACE,
            "sh": SHACL_NAMESPACE,
            "ontologyVersion": "eoip:ontologyVersion",
            "allowedEndpointPairs": {"@id": "eoip:allowedEndpointPairs", "@type": "@json"},
            "optionalProperty": {"@id": "eoip:optionalProperty", "@type": "@json"},
        },
        "@graph": graph,
    }


def validate_shacl(store, limit: int = 5000) -> dict[str, Any]:
    """Validate graph records against the manifest-derived SHACL contract."""
    if not 1 <= limit <= 10_000:
        raise ValueError("SHACL validation limit must be between 1 and 10000")

    vertices = store.find_vertices(limit=limit + 1, include_deleted=True)
    edges = store.find_edges(limit=limit + 1, include_historical=True)
    partial_vertices = len(vertices) > limit
    partial_edges = len(edges) > limit
    vertices = vertices[:limit]
    edges = edges[:limit]
    vertices_by_vid = {vertex["vid"]: vertex for vertex in vertices}
    results: list[dict[str, Any]] = []

    for vertex in vertices:
        label = vertex["label"]
        spec = VERTEX_LABELS.get(label)
        if spec is None:
            results.append(
                {
                    "focusNode": vertex.get("canonical_id"),
                    "sourceShape": "eoip:shape/Entity",
                    "resultPath": "rdf:type",
                    "severity": "Violation",
                    "message": f"Unsupported vertex label {label}",
                }
            )
            continue
        for name in spec[1]:
            if _is_missing(vertex["properties"].get(name)):
                results.append(
                    {
                        "focusNode": vertex["canonical_id"],
                        "sourceShape": f"eoip:shape/{label}",
                        "resultPath": f"eoip:property/{quote(name, safe='')}",
                        "severity": "Violation",
                        "message": f"{label} requires property {name}",
                    }
                )

    for edge in edges:
        label = edge["label"]
        spec = EDGE_LABELS.get(label)
        out_vertex = vertices_by_vid.get(edge["out_v"]) or store.get_vertex(edge["out_v"])
        in_vertex = vertices_by_vid.get(edge["in_v"]) or store.get_vertex(edge["in_v"])
        focus_node = edge["properties"].get("edge_key") or edge.get("eid")
        if spec is None:
            results.append(
                {
                    "focusNode": focus_node,
                    "sourceShape": "eoip:shape/relation",
                    "resultPath": "rdf:predicate",
                    "severity": "Violation",
                    "message": f"Unsupported edge label {label}",
                }
            )
            continue
        if out_vertex is None or in_vertex is None:
            results.append(
                {
                    "focusNode": focus_node,
                    "sourceShape": f"eoip:shape/relation/{label}",
                    "resultPath": "rdf:subject/rdf:object",
                    "severity": "Violation",
                    "message": f"{label} references an endpoint outside the validation set",
                }
            )
            continue
        if not edge_endpoints_valid(label, out_vertex["label"], in_vertex["label"]):
            results.append(
                {
                    "focusNode": focus_node,
                    "sourceShape": f"eoip:shape/relation/{label}",
                    "resultPath": "rdf:subject/rdf:object",
                    "severity": "Violation",
                    "message": f"{label} does not allow {out_vertex['label']} -> {in_vertex['label']}",
                }
            )
        for name in spec[2]:
            if _is_missing(edge["properties"].get(name)):
                results.append(
                    {
                        "focusNode": focus_node,
                        "sourceShape": f"eoip:shape/relation/{label}",
                        "resultPath": f"eoip:property/{quote(name, safe='')}",
                        "severity": "Violation",
                        "message": f"{label} requires property {name}",
                    }
                )

    return {
        "conforms": not results,
        "ontology_version": ONTOLOGY_VERSION,
        "checked": {
            "vertices": len(vertices),
            "edges": len(edges),
            "partial": partial_vertices or partial_edges,
            "truncated_vertices": partial_vertices,
            "truncated_edges": partial_edges,
        },
        "results": results,
    }


def validate_jsonld_round_trip(store, limit: int = 5000) -> dict[str, Any]:
    """Verify that supported property-graph constructs survive JSON-LD round trip."""
    from eoip.graph.memory import MemoryGraphStore

    document = export_jsonld(store, limit=limit)
    restored = MemoryGraphStore()
    import_report = import_jsonld(document, restored)

    def vertex_snapshot(source) -> dict[str, dict[str, Any]]:
        snapshot: dict[str, dict[str, Any]] = {}
        for vertex in source.find_vertices(limit=limit, include_deleted=True):
            snapshot[vertex["canonical_id"]] = {
                "label": vertex["label"],
                "properties": {
                    key: value
                    for key, value in vertex["properties"].items()
                    if key in PROPERTY_KEYS
                },
            }
        return snapshot

    def edge_snapshot(source) -> set[tuple[str, str, str, tuple[tuple[str, Any], ...]]]:
        snapshot: set[tuple[str, str, str, tuple[tuple[str, Any], ...]]] = set()
        for edge in source.find_edges(limit=limit, include_historical=True):
            props = tuple(
                sorted(
                    (key, repr(value))
                    for key, value in edge["properties"].items()
                    if key in PROPERTY_KEYS
                )
            )
            snapshot.add((edge["label"], edge["out_cid"], edge["in_cid"], props))
        return snapshot

    original_vertices = vertex_snapshot(store)
    restored_vertices = vertex_snapshot(restored)
    original_edges = edge_snapshot(store)
    restored_edges = edge_snapshot(restored)
    missing_vertices = sorted(set(original_vertices) - set(restored_vertices))
    changed_vertices = sorted(
        cid
        for cid in set(original_vertices) & set(restored_vertices)
        if original_vertices[cid] != restored_vertices[cid]
    )
    missing_edges = sorted(original_edges - restored_edges, key=repr)

    issues = []
    issues.extend({"kind": "missing_vertex", "id": cid} for cid in missing_vertices)
    issues.extend({"kind": "changed_vertex", "id": cid} for cid in changed_vertices)
    issues.extend({"kind": "missing_edge", "edge": edge} for edge in missing_edges)
    issues.extend(
        {"kind": "mapping_loss", **loss}
        for loss in import_report["mapping_losses"]
        if loss["count"] > 0
    )

    return {
        "conforms": not issues,
        "export": document["export"],
        "import": import_report,
        "original": {"vertices": len(original_vertices), "edges": len(original_edges)},
        "restored": {"vertices": len(restored_vertices), "edges": len(restored_edges)},
        "issues": issues,
    }


# ── OWL Reasoner (GRAPH-006) ─────────────────────────────────────────


class OWLReasoner:
    """Runtime OWL DL classification, subsumption, and property chain reasoning."""

    def __init__(self) -> None:
        self.subclasses: dict[str, set[str]] = {}
        self.disjoint_classes: dict[str, set[str]] = {}
        self.property_chains: list[tuple[str, str, str]] = []
        self._bootstrap_core_axioms()

    def _bootstrap_core_axioms(self) -> None:
        # Example enterprise class hierarchy
        self.add_subclass("Microservice", "Service")
        self.add_subclass("DatabaseService", "Service")
        self.add_subclass("RelationalDatabase", "DatabaseService")
        self.add_subclass("GraphDatabase", "DatabaseService")
        self.add_subclass("Engineer", "Person")
        self.add_subclass("Manager", "Person")

        # Disjointness
        self.add_disjoint("Service", "Person")
        self.add_disjoint("RelationalDatabase", "GraphDatabase")

        # Property chains: PART_OF o PART_OF -> PART_OF (transitivity)
        self.add_property_chain("PART_OF", "PART_OF", "PART_OF")
        self.add_property_chain("DEPENDS_ON", "DEPENDS_ON", "DEPENDS_ON")

    def add_subclass(self, child: str, parent: str) -> None:
        self.subclasses.setdefault(child.lower(), set()).add(parent.lower())

    def add_disjoint(self, class_a: str, class_b: str) -> None:
        ca, cb = class_a.lower(), class_b.lower()
        self.disjoint_classes.setdefault(ca, set()).add(cb)
        self.disjoint_classes.setdefault(cb, set()).add(ca)

    def add_property_chain(self, p1: str, p2: str, implied: str) -> None:
        self.property_chains.append((p1.upper(), p2.upper(), implied.upper()))

    def is_subclass_of(self, child: str, parent: str) -> bool:
        """Transitive subsumption check."""
        c = child.lower()
        p = parent.lower()
        if c == p:
            return True
        visited = set()
        queue = [c]
        while queue:
            curr = queue.pop(0)
            if curr == p:
                return True
            visited.add(curr)
            for par in self.subclasses.get(curr, set()):
                if par not in visited:
                    queue.append(par)
        return False

    def are_disjoint(self, class_a: str, class_b: str) -> bool:
        ca = class_a.lower()
        cb = class_b.lower()
        # Direct disjointness
        if cb in self.disjoint_classes.get(ca, set()):
            return True
        # Inherited disjointness
        for super_a in self._all_superclasses(ca):
            for super_b in self._all_superclasses(cb):
                if super_b in self.disjoint_classes.get(super_a, set()):
                    return True
        return False

    def _all_superclasses(self, cls_name: str) -> set[str]:
        supers = set()
        queue = [cls_name]
        while queue:
            curr = queue.pop(0)
            for p in self.subclasses.get(curr, set()):
                if p not in supers:
                    supers.add(p)
                    queue.append(p)
        return supers

    def infer_triples(self, store: Any) -> list[dict[str, Any]]:
        """Infer transitive property chain edges across existing graph store."""
        inferred = []
        edges = store.find_edges() if hasattr(store, "find_edges") else []
        edge_map: dict[str, list[dict[str, Any]]] = {}
        for e in edges:
            edge_map.setdefault(e["out_v"], []).append(e)

        for p1, p2, implied in self.property_chains:
            for e1 in edges:
                if e1["label"].upper() == p1:
                    mid_node = e1["in_v"]
                    for e2 in edge_map.get(mid_node, []):
                        if e2["label"].upper() == p2:
                            u = e1["out_v"]
                            w = e2["in_v"]
                            inferred.append({
                                "out_v": u,
                                "in_v": w,
                                "label": implied,
                                "inferred_by": f"Chain({p1} o {p2})",
                            })
        return inferred


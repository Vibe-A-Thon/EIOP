"""Bounded JSON-LD export for EOIP's controlled graph vocabulary."""

from __future__ import annotations

from collections import Counter
from urllib.parse import quote

from eoip.ontology.manifest import EDGE_LABELS, ONTOLOGY_VERSION, PROPERTY_KEYS, VERTEX_LABELS

EOIP_NAMESPACE = "urn:eoip:ontology:"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
OWL_NAMESPACE = "http://www.w3.org/2002/07/owl#"
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"


def _property_term(name: str) -> str:
    return f"property_{quote(name, safe='')}"


def _property_type(value: object) -> str | None:
    if isinstance(value, (dict, list)):
        return "@json"
    return None


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

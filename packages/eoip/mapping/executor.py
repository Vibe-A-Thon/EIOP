"""Mapping execution engine: LPG <-> RDF projection and PROV-O provenance (CRA-017.8, CRA-017.9).

Executes MappingIR against raw records, producing:
1. Vertices and RDF triples conforming to the LPG <-> RDF projection scheme:
   - vertex IRI: eoip:entity/{Label}/{id} (id percent-encoded).
   - rdf:type eoip:class/{Label}.
   - vertex property: eoip:property/{name}.
   - edge without properties -> direct triple.
   - edge with properties -> named graph per edge assertion urn:eoip:assertion:{id}.
2. W3C PROV-O triples:
   - prov:wasDerivedFrom source resource revision.
   - prov:wasGeneratedBy mapping-run activity.
   - prov:wasAttributedTo connector agent.
3. PII field redaction on export per governance settings.
"""

from __future__ import annotations

import hashlib
import uuid
from typing import Any
from urllib.parse import quote

from eoip.mapping.cml import safe_apply_template
from eoip.mapping.ir import MappingIR


def execute_mapping(
    mapping_ir: MappingIR,
    records: list[dict[str, Any]],
    tenant_id: str,
    run_id: str = "run_001",
    redact_pii: bool = False,
) -> dict[str, Any]:
    """Execute mapping over records producing LPG graph structures and RDF quads."""
    vertices: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    triples: list[dict[str, str]] = []  # {graph, subject, predicate, object, datatype}

    tenant_graph = f"urn:eoip:tenant:{tenant_id}"
    activity_iri = mapping_ir.provenance.mapping_activity_iri_template.replace("{run_id}", run_id)
    agent_iri = mapping_ir.provenance.connector_agent_iri

    for rec in records:
        # 1. Subject Resolution
        subject_iri = safe_apply_template(mapping_ir.subject_map.template, rec)
        target_class = mapping_ir.subject_map.target_class_iri

        # Add vertex and type triple
        vertex_props: dict[str, Any] = {}
        triples.append({
            "graph": tenant_graph,
            "subject": subject_iri,
            "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "object": target_class,
            "datatype": "IRI",
        })

        # 2. Properties
        for pm in mapping_ir.property_maps:
            if pm.source_path not in rec:
                continue
            raw_val = rec[pm.source_path]
            if raw_val is None:
                continue

            # PII redaction check
            if redact_pii and pm.is_pii:
                continue

            val_str = str(raw_val)
            vertex_props[pm.source_path] = val_str

            triples.append({
                "graph": tenant_graph,
                "subject": subject_iri,
                "predicate": pm.predicate_iri,
                "object": val_str,
                "datatype": pm.datatype_iri,
            })

        vertices.append({
            "vid": subject_iri,
            "label": target_class.split("/")[-1],
            "properties": vertex_props,
        })

        # 3. Relations / Edges
        for rm in mapping_ir.relation_maps:
            if rm.source_path not in rec:
                continue
            val = rec[rm.source_path]
            if not val:
                continue

            obj_iri = safe_apply_template(rm.object_template, rec)
            edge_id = f"urn:eoip:assertion:{uuid.uuid4().hex[:12]}"

            edge_props = {}
            for ep_key, ep_path in rm.edge_properties.items():
                if ep_path in rec:
                    edge_props[ep_key] = str(rec[ep_path])

            edges.append({
                "eid": edge_id,
                "label": rm.predicate_iri.split("/")[-1],
                "out_v": subject_iri,
                "in_v": obj_iri,
                "properties": edge_props,
            })

            if edge_props:
                # CRA-017.8: Edge with properties placed in assertion named graph
                assertion_graph = edge_id
                triples.append({
                    "graph": assertion_graph,
                    "subject": subject_iri,
                    "predicate": rm.predicate_iri,
                    "object": obj_iri,
                    "datatype": "IRI",
                })
                for prop_name, prop_val in edge_props.items():
                    triples.append({
                        "graph": assertion_graph,
                        "subject": edge_id,
                        "predicate": f"eoip:property/{prop_name}",
                        "object": prop_val,
                        "datatype": "http://www.w3.org/2001/XMLSchema#string",
                    })
            else:
                # Direct triple in tenant graph
                triples.append({
                    "graph": tenant_graph,
                    "subject": subject_iri,
                    "predicate": rm.predicate_iri,
                    "object": obj_iri,
                    "datatype": "IRI",
                })

        # 4. PROV-O Provenance Triples (CRA-017.9)
        if mapping_ir.provenance.emit_prov_o:
            source_res_iri = f"urn:eoip:source:{mapping_ir.source_type}:{rec.get('id', 'unknown')}"
            triples.append({
                "graph": tenant_graph,
                "subject": subject_iri,
                "predicate": "http://www.w3.org/ns/prov#wasDerivedFrom",
                "object": source_res_iri,
                "datatype": "IRI",
            })
            triples.append({
                "graph": tenant_graph,
                "subject": subject_iri,
                "predicate": "http://www.w3.org/ns/prov#wasGeneratedBy",
                "object": activity_iri,
                "datatype": "IRI",
            })
            triples.append({
                "graph": tenant_graph,
                "subject": activity_iri,
                "predicate": "http://www.w3.org/ns/prov#wasAttributedTo",
                "object": agent_iri,
                "datatype": "IRI",
            })

    return {
        "vertices": vertices,
        "edges": edges,
        "triples": triples,
        "total_records_processed": len(records),
        "total_triples": len(triples),
    }

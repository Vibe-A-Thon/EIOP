"""Engine-neutral Mapping Intermediate Representation (IR) for CRA-017.1.

Defines the normalized, versioned structure for translating source records
into property graphs and RDF graphs with stable identity, datatypes,
null handling, and provenance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TermType(str, Enum):
    IRI = "IRI"
    LITERAL = "LITERAL"
    BLANK_NODE = "BLANK_NODE"


@dataclass(frozen=True)
class SubjectMapIR:
    template: str
    target_class_iri: str
    graph_iri_template: Optional[str] = None


@dataclass(frozen=True)
class PropertyMapIR:
    source_path: str
    predicate_iri: str
    datatype_iri: str = "http://www.w3.org/2001/XMLSchema#string"
    required: bool = False
    language: Optional[str] = None
    is_pii: bool = False
    classification: str = "INTERNAL"


@dataclass(frozen=True)
class RelationMapIR:
    source_path: str
    predicate_iri: str
    object_template: str
    object_class_iri: str
    edge_properties: dict[str, str] = field(default_factory=dict)  # prop_name -> source_path
    graph_iri_template: Optional[str] = None


@dataclass(frozen=True)
class ProvenanceConfigIR:
    emit_prov_o: bool = True
    connector_agent_iri: str = "urn:eoip:agent:connector"
    mapping_activity_iri_template: str = "urn:eoip:activity:mapping_run:{run_id}"
    confidence_default: float = 1.0


@dataclass
class MappingIR:
    mapping_id: str
    version: str
    source_type: str
    subject_map: SubjectMapIR
    property_maps: list[PropertyMapIR] = field(default_factory=list)
    relation_maps: list[RelationMapIR] = field(default_factory=list)
    provenance: ProvenanceConfigIR = field(default_factory=ProvenanceConfigIR)
    classification: str = "INTERNAL"
    pii_fields: list[str] = field(default_factory=list)

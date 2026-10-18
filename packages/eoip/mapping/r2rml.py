"""R2RML and RML adapter for Mapping IR (CRA-017.2, CRA-017.3, CRA-017.7).

Translates R2RML / RML mapping definitions into engine-neutral MappingIR.
Tracks unsupported constructs and lossy coercions, blocking lossless claims
when any loss exists (CRA-017.3).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from eoip.mapping.ir import (
    MappingIR,
    PropertyMapIR,
    ProvenanceConfigIR,
    RelationMapIR,
    SubjectMapIR,
)


@dataclass
class UnsupportedConstruct:
    construct_type: str
    identifier: str
    detail: str


@dataclass
class LossReport:
    unsupported_constructs: list[UnsupportedConstruct] = field(default_factory=list)
    lossy_coercions: list[str] = field(default_factory=list)

    @property
    def is_lossless(self) -> bool:
        """Blocks lossless claims when any loss exists (CRA-017.3)."""
        return len(self.unsupported_constructs) == 0 and len(self.lossy_coercions) == 0


class R2RMLAdapter:
    """R2RML / RML mapping import adapter producing MappingIR."""

    def __init__(self, allowed_functions: Optional[set[str]] = None) -> None:
        self.allowed_functions = allowed_functions or {
            "lower", "upper", "trim", "concat", "split", "date_parse", "iri_safe"
        }

    def import_r2rml_dict(self, r2rml_def: dict[str, Any]) -> tuple[MappingIR, LossReport]:
        """Convert an R2RML definition dictionary into MappingIR and a LossReport."""
        report = LossReport()

        mapping_id = r2rml_def.get("id", "r2rml_imported")
        version = r2rml_def.get("version", "1.0.0")
        source_type = r2rml_def.get("source_type", "relational")

        # Logical table / source validation
        logical_table = r2rml_def.get("logicalTable", {})
        if "sqlQuery" in logical_table:
            query = logical_table["sqlQuery"]
            # Detect unapproved UDFs or complex procedural SQL
            if any(forbidden in query.lower() for forbidden in ["procedure", "exec", "call", "sleep"]):
                report.unsupported_constructs.append(
                    UnsupportedConstruct(
                        construct_type="sqlQuery_procedural",
                        identifier=mapping_id,
                        detail="Stored procedures or unsafe calls in logicalTable are unsupported",
                    )
                )

        # Subject Map
        sub_def = r2rml_def.get("subjectMap", {})
        sub_template = sub_def.get("template", "")
        target_class = sub_def.get("class", "http://www.w3.org/2002/07/owl#Thing")
        term_type = sub_def.get("termType", "IRI")
        if term_type == "BlankNode":
            report.lossy_coercions.append("BlankNode subject mapped to local anonymous IRI prefix")

        # Validate subject template syntax
        if "{" not in sub_template and sub_template:
            report.lossy_coercions.append("Constant subject IRI without template variable")

        subject_map = SubjectMapIR(
            template=sub_template,
            target_class_iri=target_class,
            graph_iri_template=sub_def.get("graph"),
        )

        # Predicate-Object Maps
        property_maps: list[PropertyMapIR] = []
        relation_maps: list[RelationMapIR] = []
        pii_fields: list[str] = []

        for pom in r2rml_def.get("predicateObjectMaps", []):
            predicate = pom.get("predicate", "")
            object_map = pom.get("objectMap", {})

            # Check if this is a parent-triples-map / join (Relation)
            if "parentTriplesMap" in pom or "objectTemplate" in object_map:
                obj_template = object_map.get("template", object_map.get("objectTemplate", ""))
                obj_class = object_map.get("class", "http://www.w3.org/2002/07/owl#Thing")
                join_col = pom.get("joinCondition", {}).get("child", object_map.get("column", ""))
                
                edge_props = pom.get("edgeProperties", {})
                relation_maps.append(
                    RelationMapIR(
                        source_path=join_col,
                        predicate_iri=predicate,
                        object_template=obj_template,
                        object_class_iri=obj_class,
                        edge_properties=edge_props,
                    )
                )
            else:
                # Regular column property map
                col = object_map.get("column") or pom.get("column", "")
                datatype = object_map.get("datatype", "http://www.w3.org/2001/XMLSchema#string")
                language = object_map.get("language")
                is_pii = bool(pom.get("pii", False))
                if is_pii and col:
                    pii_fields.append(col)

                # Check unsupported custom transformations
                custom_fn = object_map.get("function")
                if custom_fn and custom_fn not in self.allowed_functions:
                    report.unsupported_constructs.append(
                        UnsupportedConstruct(
                            construct_type="custom_function",
                            identifier=custom_fn,
                            detail=f"Function {custom_fn} not in authorized whitelist {self.allowed_functions}",
                        )
                    )

                if not datatype:
                    report.lossy_coercions.append(f"Missing datatype on column {col}, coerced to xsd:string")
                    datatype = "http://www.w3.org/2001/XMLSchema#string"

                property_maps.append(
                    PropertyMapIR(
                        source_path=col,
                        predicate_iri=predicate,
                        datatype_iri=datatype,
                        required=bool(pom.get("required", False)),
                        language=language,
                        is_pii=is_pii,
                    )
                )

        mapping_ir = MappingIR(
            mapping_id=mapping_id,
            version=version,
            source_type=source_type,
            subject_map=subject_map,
            property_maps=property_maps,
            relation_maps=relation_maps,
            provenance=ProvenanceConfigIR(
                emit_prov_o=True,
                connector_agent_iri=r2rml_def.get("agent", "urn:eoip:agent:r2rml_adapter"),
            ),
            pii_fields=pii_fields,
        )

        return mapping_ir, report

"""Schema induction: class/property proposals from profiled datasets.

Reuses ``eoip.ingest.profile.SchemaProfiler``/``ProfileReport`` (SR-ING-010)
so induced classes/properties are grounded in deterministic field profiles,
not heuristics over raw records alone.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import ProposedClass, ProposedProperty, _urn
from eoip.ingest.profile import ProfileReport

_SCALAR_RANGE = {
    "string": "xsd:string",
    "integer": "xsd:integer",
    "number": "xsd:double",
    "boolean": "xsd:boolean",
}


class InducedSchema(BaseModel):
    """Deterministic class + property proposal from one dataset profile."""

    model_config = ConfigDict(extra="forbid")

    schema_id: str
    dataset: str
    classes: list[ProposedClass] = Field(default_factory=list)
    properties: list[ProposedProperty] = Field(default_factory=list)


def induce_schema(report: ProfileReport, *, root_class: str | None = None, dataset: str | None = None) -> InducedSchema:
    """Induce one class per object-level field path plus its scalar properties.

    Each ``object`` field path becomes a proposed class; scalar leaf paths
    nested under an object become properties of that class. Top-level scalars
    attach to the root class.
    """
    dataset = dataset or report.profile_id.rsplit(":", 1)[-1] or "dataset"
    classes: dict[str, ProposedClass] = {}
    properties: list[ProposedProperty] = []

    root_name = root_class or _classify(dataset)
    root = ProposedClass(
        class_id=_urn("class", f"{dataset}:{root_name}"),
        name=root_name,
        source="schema-induction:root",
        member_count=report.record_count,
        evidence={"profile_id": report.profile_id, "record_count": report.record_count},
    )
    classes[root_name] = root

    for field in report.fields:
        if field.kind == "object" and field.path not in {"$", ""}:
            name = _classify(field.path.rsplit(".", 1)[-1].rstrip("[]"))
            cls = classes.get(name) or ProposedClass(
                class_id=_urn("class", f"{dataset}:{name}"),
                name=name,
                source="schema-induction:object-path",
                evidence={"path": field.path},
            )
            cls.member_count += field.total_count
            cls.evidence.setdefault("paths", []).append(field.path)
            classes[name] = cls

    for field in report.fields:
        if field.kind != "scalar":
            continue
        parent_path, _, leaf = field.path.rpartition(".")
        if parent_path:
            domain = _classify(parent_path.rsplit(".", 1)[-1].rstrip("[]"))
        else:
            domain = root_name
        if not leaf:
            leaf = field.path
        observed = [t for t in field.observed_types if t != "null"]
        range_ = _SCALAR_RANGE.get(observed[0] if observed else "", "xsd:string")
        properties.append(
            ProposedProperty(
                property_id=_urn("property", f"{dataset}:{domain}:{leaf}"),
                name=leaf.rstrip("[]"),
                domain=domain,
                range=range_,
                functional=field.unique_ratio >= 0.99 and field.cardinality > 0,
                required=field.null_count == 0 and field.total_count > 0,
                evidence={
                    "path": field.path,
                    "observed_types": field.observed_types,
                    "unique_ratio": field.unique_ratio,
                    "formats": field.formats,
                    "enum_candidate": field.enum_candidate,
                },
            )
        )

    return InducedSchema(
        schema_id=_urn("schema", report.profile_id),
        dataset=dataset,
        classes=[classes[name] for name in sorted(classes)],
        properties=sorted(properties, key=lambda p: (p.domain, p.name)),
    )


def _classify(raw: str) -> str:
    parts = [p for p in raw.replace("[]", "").replace("_", " ").replace("-", " ").split() if p]
    if not parts:
        return "Record"
    name = "".join(p[:1].upper() + p[1:] for p in parts)
    return name if name[0].isalpha() else "Record" + name

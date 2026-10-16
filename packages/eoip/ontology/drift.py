"""Ontology drift detection and evolution proposals (G2-OEVO-001..006).

Detects recurring unmapped graph vocabulary (vertex labels, edge labels,
property keys) that connectors or mappings produced without a matching
ontology declaration, and turns repeated patterns into reviewable ontology
evolution proposals. Detection is read-only; proposals enter the existing
governed proposal store and require human approval — nothing is applied to the
manifest automatically.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS


@dataclass
class DriftFinding:
    kind: str  # "vertex_label" | "edge_label" | "property_key"
    value: str
    occurrences: int
    examples: list[str] = field(default_factory=list)
    classification: str = "additive"  # additive | potentially_breaking


@dataclass
class OntologyDriftReport:
    findings: list[DriftFinding]

    @property
    def has_drift(self) -> bool:
        return bool(self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "has_drift": self.has_drift,
            "findings": [
                {
                    "kind": finding.kind,
                    "value": finding.value,
                    "occurrences": finding.occurrences,
                    "examples": finding.examples,
                    "classification": finding.classification,
                }
                for finding in self.findings
            ],
        }


_PROPERTY_SAMPLE = 5_000


def detect_ontology_drift(store, *, sample_limit: int = _PROPERTY_SAMPLE) -> OntologyDriftReport:
    """Scan the graph for vocabulary not declared in the ontology manifest.

    Read-only. Vertex/edge labels are counted across the graph; property keys
    are sampled up to ``sample_limit`` vertices/edges for bounded cost.
    """
    findings: list[DriftFinding] = []

    label_counts: Counter[str] = Counter()
    label_examples: dict[str, list[str]] = {}
    for vertex in store.find_vertices(limit=200_000):
        label = vertex["label"]
        label_counts[label] += 1
        if len(label_examples.setdefault(label, [])) < 3:
            label_examples[label].append(vertex["canonical_id"])
    for label, count in label_counts.items():
        if label not in VERTEX_LABELS:
            findings.append(
                DriftFinding(
                    kind="vertex_label",
                    value=label,
                    occurrences=count,
                    examples=label_examples[label],
                    classification="potentially_breaking",
                )
            )

    edge_counts: Counter[str] = Counter()
    edge_examples: dict[str, list[str]] = {}
    for edge in store.find_edges(limit=200_000, include_historical=True):
        label = edge["label"]
        edge_counts[label] += 1
        example = edge.get("out_cid") or edge["eid"]
        if len(edge_examples.setdefault(label, [])) < 3:
            edge_examples[label].append(example)
    for label, count in edge_counts.items():
        if label not in EDGE_LABELS:
            findings.append(
                DriftFinding(
                    kind="edge_label",
                    value=label,
                    occurrences=count,
                    examples=edge_examples[label],
                    classification="potentially_breaking",
                )
            )

    key_counts: Counter[str] = Counter()
    for scanned, vertex in enumerate(store.find_vertices(limit=sample_limit), start=1):
        for key in vertex["properties"]:
            key_counts[key] += 1
        if scanned >= sample_limit:
            break
    for key, count in key_counts.items():
        if key not in PROPERTY_KEYS:
            findings.append(
                DriftFinding(
                    kind="property_key",
                    value=key,
                    occurrences=count,
                    classification="additive",
                )
            )

    findings.sort(key=lambda item: (-item.occurrences, item.kind, item.value))
    return OntologyDriftReport(findings=findings)


def build_evolution_proposal(finding: DriftFinding) -> dict[str, Any]:
    """Map a drift finding to a governed ontology-evolution proposal payload."""
    if finding.kind == "vertex_label":
        summary = f"Declare unmapped vertex label '{finding.value}' in the ontology"
        proposal_type = "ONTOLOGY_VERTEX_LABEL"
    elif finding.kind == "edge_label":
        summary = f"Declare unmapped edge label '{finding.value}' with domain/range"
        proposal_type = "ONTOLOGY_EDGE_LABEL"
    else:
        summary = f"Declare unmapped property key '{finding.value}'"
        proposal_type = "ONTOLOGY_PROPERTY_KEY"
    return {
        "proposal_type": proposal_type,
        "summary": summary,
        "evidence": {
            "kind": finding.kind,
            "value": finding.value,
            "occurrences": finding.occurrences,
            "examples": finding.examples,
            "classification": finding.classification,
        },
        "impact_analysis": (
            f"{finding.occurrences} existing graph fact(s) reference this vocabulary; "
            "declaring it is additive and requires no migration."
            if finding.classification == "additive"
            else f"{finding.occurrences} existing graph fact(s) reference this vocabulary; "
            "review domain/range before publishing."
        ),
    }

"""Construction modes: ontology-first, data-first, and hybrid planning.

A *construction plan* orders the builders: which schema source wins, which
discovery steps run, and how induced classes are reconciled against an
existing ontology manifest.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import _urn
from eoip.graphbuild.schema import InducedSchema

ConstructionMode = Literal["ontology-first", "data-first", "hybrid"]


class ConstructionPlan(BaseModel):
    """Ordered, deterministic plan for building one knowledge graph."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    mode: ConstructionMode
    dataset: str
    steps: list[str] = Field(default_factory=list)
    reconciliation: dict[str, str] = Field(default_factory=dict)
    """How induced classes/properties map onto existing ontology entities."""


def plan_construction(
    mode: ConstructionMode,
    dataset: str,
    induced: InducedSchema | None = None,
    ontology_classes: list[str] | None = None,
) -> ConstructionPlan:
    """Build the step order and reconciliation map for one mode.

    * ``ontology-first``: existing ontology manifest is authoritative; data
      induction only proposes *extensions* (new classes/properties), never
      renames, and validation gates run before any write.
    * ``data-first``: induction is authoritative; ontology entities are
      matched by name afterward and unmatched induced classes are added.
    * ``hybrid``: ontology anchors core classes; induction fills in
      properties and leaf classes; conflicts go to the review queue.
    """
    ontology = set(ontology_classes or [])
    reconciliation: dict[str, str] = {}
    if induced is not None:
        for cls in induced.classes:
            if cls.name in ontology:
                reconciliation[cls.name] = "match:existing"
            elif mode == "ontology-first":
                reconciliation[cls.name] = "propose:extension"
            elif mode == "data-first":
                reconciliation[cls.name] = "add:induced"
            else:
                reconciliation[cls.name] = "review:conflict"
        for prop in induced.properties:
            key = f"{prop.domain}.{prop.name}"
            reconciliation[key] = "match:existing" if prop.name in ontology else "propose:extension"

    if mode == "ontology-first":
        steps = [
            "validate-ontology-manifest",
            "profile-dataset",
            "induce-schema",
            "reconcile-extensions",
            "review-queue",
            "validated-write",
        ]
    elif mode == "data-first":
        steps = [
            "profile-dataset",
            "induce-schema",
            "match-ontology",
            "add-unmatched",
            "validated-write",
        ]
    else:
        steps = [
            "validate-ontology-manifest",
            "profile-dataset",
            "induce-schema",
            "anchor-core-classes",
            "reconcile-conflicts-to-review",
            "validated-write",
        ]

    return ConstructionPlan(
        plan_id=_urn("plan", f"{mode}:{dataset}"),
        mode=mode,
        dataset=dataset,
        steps=steps,
        reconciliation=dict(sorted(reconciliation.items())),
    )

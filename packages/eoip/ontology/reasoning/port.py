"""Reasoning Port and Semantic Run types (CRA-019.1, CRA-019.2, CRA-019.3, CRA-019.7).

Defines ReasonerPort Protocol:
- classify(), is_consistent(), unsatisfiable_classes(), realize(), entails(), explain()
- Typed SemanticRun results with engine, version, profile, status, revision bindings
- InconsistentOntologyException with minimal conflicting axiom set
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class ReasonerStatus(str, Enum):
    OK = "OK"
    INCONSISTENT = "INCONSISTENT"
    UNSUPPORTED = "UNSUPPORTED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"


class OWLProfile(str, Enum):
    RDFS = "RDFS"
    OWL2_RL = "OWL 2 RL"
    OWL2_EL = "OWL 2 EL"
    OWL2_QL = "OWL 2 QL"
    OWL2_DL = "OWL 2 DL"
    NATIVE_RDFS_SUBSET = "eoip-native-rdfs-subset"


@dataclass
class SemanticRun:
    """Detailed result of a semantic reasoning operation (CRA-019.3)."""

    engine: str
    engine_version: str
    profile: str
    status: ReasonerStatus
    revision: str
    asserted_count: int = 0
    inferred_count: int = 0
    inferred_statements: list[dict[str, Any]] = field(default_factory=list)
    explanations: dict[str, list[str]] = field(default_factory=dict)  # conclusion -> supporting axiom IDs
    execution_time_ms: float = 0.0
    is_degraded: bool = False
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine": self.engine,
            "engine_version": self.engine_version,
            "profile": self.profile,
            "status": self.status.value,
            "revision": self.revision,
            "asserted_count": self.asserted_count,
            "inferred_count": self.inferred_count,
            "inferred_statements": self.inferred_statements,
            "explanations": self.explanations,
            "execution_time_ms": self.execution_time_ms,
            "is_degraded": self.is_degraded,
            "error_message": self.error_message,
        }


class InconsistentOntologyException(Exception):
    """Raised when an ontology is logically inconsistent during reasoning (CRA-019.12)."""

    def __init__(
        self,
        message: str = "Ontology is inconsistent",
        minimal_conflicting_axioms: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.minimal_conflicting_axioms: list[str] = minimal_conflicting_axioms or []


@runtime_checkable
class ReasonerPort(Protocol):
    """Abstract port for standards-conformant OWL/RDFS reasoners (CRA-019.7)."""

    def classify(
        self,
        ontology_graph: Any,
        *,
        revision: str = "v1",
        timeout_seconds: float = 60.0,
    ) -> SemanticRun:
        """Compute the complete subclass and equivalence hierarchy."""
        ...

    def is_consistent(
        self,
        ontology_graph: Any,
        *,
        revision: str = "v1",
        timeout_seconds: float = 60.0,
    ) -> tuple[bool, SemanticRun]:
        """Check whether the ontology has at least one valid model."""
        ...

    def unsatisfiable_classes(
        self,
        ontology_graph: Any,
        *,
        revision: str = "v1",
        timeout_seconds: float = 60.0,
    ) -> tuple[list[str], SemanticRun]:
        """Identify classes that cannot have instances (subsumed by owl:Nothing)."""
        ...

    def realize(
        self,
        data_graph: Any,
        ontology_graph: Any,
        *,
        revision: str = "v1",
        timeout_seconds: float = 60.0,
    ) -> SemanticRun:
        """Compute the most specific classes for all individuals."""
        ...

    def entails(
        self,
        ontology_graph: Any,
        axiom: str | tuple[str, str, str],
        *,
        revision: str = "v1",
        timeout_seconds: float = 60.0,
    ) -> tuple[bool, SemanticRun]:
        """Test whether an axiom logically follows from the ontology."""
        ...

    def explain(
        self,
        ontology_graph: Any,
        axiom: str | tuple[str, str, str],
        *,
        revision: str = "v1",
        timeout_seconds: float = 60.0,
    ) -> tuple[list[str], SemanticRun]:
        """Compute a minimal justification (set of axioms) entailing the query."""
        ...

"""Predicate and operation registries for REVA warrant validation (T-106 / REVA-WK-005 / §10.4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Type

from pydantic import BaseModel
from reva.core.errors import PredicateUnknownError
from reva.kernel.authority import Authority, Epistemic


@dataclass
class PredicateEntry:
    name: str
    statement_model: Optional[Type[BaseModel]]
    allowed_authorities: Set[Authority] = field(default_factory=lambda: set(Authority))
    allowed_epistemic: Set[Epistemic] = field(default_factory=lambda: set(Epistemic))
    requires_coverage: bool = False
    description: str = ""


@dataclass
class OperationEntry:
    name: str
    description: str
    output_predicate: str
    required_parameters: List[str] = field(default_factory=list)


class PredicateRegistry:
    """Registry maintaining valid predicate and operation definitions."""

    def __init__(self) -> None:
        self._predicates: Dict[str, PredicateEntry] = {}
        self._operations: Dict[str, OperationEntry] = {}

    def register_predicate(
        self,
        name: str,
        statement_model: Optional[Type[BaseModel]] = None,
        allowed_authorities: Optional[Set[Authority]] = None,
        allowed_epistemic: Optional[Set[Epistemic]] = None,
        requires_coverage: bool = False,
        description: str = "",
    ) -> None:
        self._predicates[name] = PredicateEntry(
            name=name,
            statement_model=statement_model,
            allowed_authorities=allowed_authorities or set(Authority),
            allowed_epistemic=allowed_epistemic or set(Epistemic),
            requires_coverage=requires_coverage,
            description=description,
        )

    def get_predicate(self, name: str) -> PredicateEntry:
        if name not in self._predicates:
            raise PredicateUnknownError(f"Predicate '{name}' is not registered in the predicate registry")
        return self._predicates[name]

    def has_predicate(self, name: str) -> bool:
        return name in self._predicates

    def list_predicates(self) -> List[PredicateEntry]:
        return list(self._predicates.values())

    def register_operation(
        self,
        name: str,
        description: str,
        output_predicate: str,
        required_parameters: Optional[List[str]] = None,
    ) -> None:
        self._operations[name] = OperationEntry(
            name=name,
            description=description,
            output_predicate=output_predicate,
            required_parameters=required_parameters or [],
        )

    def get_operation(self, name: str) -> Optional[OperationEntry]:
        return self._operations.get(name)

    def list_operations(self) -> List[OperationEntry]:
        return list(self._operations.values())


# Global default registry
default_registry = PredicateRegistry()


def register_predicate(
    name: str,
    statement_model: Optional[Type[BaseModel]] = None,
    allowed_authorities: Optional[Set[Authority]] = None,
    allowed_epistemic: Optional[Set[Epistemic]] = None,
    requires_coverage: bool = False,
    description: str = "",
) -> None:
    default_registry.register_predicate(
        name=name,
        statement_model=statement_model,
        allowed_authorities=allowed_authorities,
        allowed_epistemic=allowed_epistemic,
        requires_coverage=requires_coverage,
        description=description,
    )


def get_predicate(name: str) -> Optional[PredicateEntry]:
    try:
        return default_registry.get_predicate(name)
    except PredicateUnknownError:
        return None


def has_predicate(name: str) -> bool:
    return default_registry.has_predicate(name)


def list_predicates() -> List[PredicateEntry]:
    return default_registry.list_predicates()


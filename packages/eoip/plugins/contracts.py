"""Versioned plugin contracts and capability negotiation (CRA-002.1).

Defines standard typing.Protocol interfaces for the 9 core extension points:
1. ConnectorContract
2. ParserContract
3. MapperContract
4. GraphStoreContract
5. SemanticEngineContract
6. SearchVectorIndexContract
7. ModelProviderContract
8. WorkflowActionContract
9. UIContributionContract

Also provides semver compatibility ranges and capability negotiation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version


class ContractKind(str, Enum):
    CONNECTOR = "connector"
    PARSER = "parser"
    MAPPER = "mapper"
    GRAPH_STORE = "graph_store"
    SEMANTIC_ENGINE = "semantic_engine"
    SEARCH_VECTOR_INDEX = "search_vector_index"
    MODEL_PROVIDER = "model_provider"
    WORKFLOW_ACTION = "workflow_action"
    UI_CONTRIBUTION = "ui_contribution"


# ---------------------------------------------------------------------------
# Protocols (CRA-002.1)
# ---------------------------------------------------------------------------

@runtime_checkable
class ConnectorContract(Protocol):
    """Protocol for data source connector plugins."""
    contract_version: str = "1.0.0"

    def discover(self, config: dict[str, Any]) -> list[dict[str, Any]]: ...
    def baseline(self, cursor: str | None = None) -> tuple[list[dict[str, Any]], str | None]: ...
    def poll(self, cursor: str) -> tuple[list[dict[str, Any]], str]: ...


@runtime_checkable
class ParserContract(Protocol):
    """Protocol for file/content format parsers."""
    contract_version: str = "1.0.0"

    def can_parse(self, mime_type: str, filename: str) -> bool: ...
    def parse(self, content_stream: Any, metadata: dict[str, Any]) -> dict[str, Any]: ...


@runtime_checkable
class MapperContract(Protocol):
    """Protocol for source-to-graph/RDF mapping plugins."""
    contract_version: str = "1.0.0"

    def compile_rules(self, rules: dict[str, Any]) -> Any: ...
    def map_record(self, record: dict[str, Any], context: dict[str, Any]) -> list[dict[str, Any]]: ...


@runtime_checkable
class GraphStoreContract(Protocol):
    """Protocol for storage backends (LPG or RDF)."""
    contract_version: str = "1.0.0"

    def capabilities(self) -> dict[str, Any]: ...
    def execute_query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]: ...
    def commit_assertions(self, assertions: list[dict[str, Any]]) -> dict[str, Any]: ...


@runtime_checkable
class SemanticEngineContract(Protocol):
    """Protocol for reasoners and semantic processors."""
    contract_version: str = "1.0.0"

    def reason(self, ontology_ref: str, graph_ref: str, options: dict[str, Any]) -> dict[str, Any]: ...
    def explain(self, inference_id: str) -> dict[str, Any]: ...


@runtime_checkable
class SearchVectorIndexContract(Protocol):
    """Protocol for vector and keyword search plugins."""
    contract_version: str = "1.0.0"

    def index_vectors(self, vectors: list[list[float]], metadata: list[dict[str, Any]]) -> list[str]: ...
    def search_similar(self, query_vector: list[float], top_k: int, filter_scope: dict[str, Any] | None = None) -> list[dict[str, Any]]: ...


@runtime_checkable
class ModelProviderContract(Protocol):
    """Protocol for LLM/embedding/graph-model providers."""
    contract_version: str = "1.0.0"

    def embed(self, texts: list[str]) -> list[list[float]]: ...
    def generate(self, prompt: str, token_budget: int, stop_sequences: list[str] | None = None) -> str: ...


@runtime_checkable
class WorkflowActionContract(Protocol):
    """Protocol for governed actions/write-back plugins."""
    contract_version: str = "1.0.0"

    def action_type(self) -> str: ...
    def validate_intent(self, intent: dict[str, Any]) -> tuple[bool, str | None]: ...
    def execute(self, intent: dict[str, Any]) -> dict[str, Any]: ...


@runtime_checkable
class UIContributionContract(Protocol):
    """Protocol for UI widget/dashboard contributions."""
    contract_version: str = "1.0.0"

    def render_manifest(self) -> dict[str, Any]: ...
    def get_component_definition(self) -> dict[str, Any]: ...


# ---------------------------------------------------------------------------
# Negotiation & Compatibility (CRA-002.1)
# ---------------------------------------------------------------------------

def normalize_range(spec: str) -> str:
    """Normalize npm-style semver prefixes (^1.0.0, ~1.0.0) into PEP 440 / SpecifierSet."""
    spec = spec.strip()
    if spec.startswith("^"):
        # ^1.2.3 -> >=1.2.3, <2.0.0
        # ^0.2.3 -> >=0.2.3, <0.3.0
        v_str = spec[1:].strip()
        parts = v_str.split(".")
        if len(parts) >= 1 and parts[0] != "0":
            next_major = int(parts[0]) + 1
            return f">={v_str},<{next_major}.0.0"
        elif len(parts) >= 2 and parts[0] == "0" and parts[1] != "0":
            next_minor = int(parts[1]) + 1
            return f">={v_str},<0.{next_minor}.0"
        else:
            return f"=={v_str}"
    elif spec.startswith("~"):
        # ~1.2.3 -> >=1.2.3, <1.3.0
        v_str = spec[1:].strip()
        parts = v_str.split(".")
        if len(parts) >= 2:
            next_minor = int(parts[1]) + 1
            return f">={v_str},<{parts[0]}.{next_minor}.0"
        else:
            return f"=={v_str}"
    return spec


@dataclass
class ContractNegotiationResult:
    compatible: bool
    status: str
    negotiated_contracts: dict[str, str] = field(default_factory=dict)
    incompatibilities: list[dict[str, str]] = field(default_factory=list)


def negotiate_contracts(
    host_supported: dict[str, str],
    plugin_contracts: dict[str, str],
) -> ContractNegotiationResult:
    """Negotiate contract versions between host and plugin.

    host_supported: map of contract_name -> supported version range (e.g. ">=1.0.0,<2.0.0" or "^1.0.0")
    plugin_contracts: map of contract_name -> implemented semver (e.g. "1.2.0")

    Returns ContractNegotiationResult. If any contract is incompatible,
    status is "PLUGIN_CONTRACT_INCOMPATIBLE".
    """
    negotiated: dict[str, str] = {}
    incompatibilities: list[dict[str, str]] = []

    for c_name, c_ver in plugin_contracts.items():
        if c_name not in host_supported:
            incompatibilities.append({
                "contract": c_name,
                "reason": f"Contract '{c_name}' not supported by host",
                "plugin_version": c_ver,
                "host_supported": "None",
            })
            continue

        raw_range = host_supported[c_name]
        norm_range = normalize_range(raw_range)

        try:
            v = Version(c_ver)
        except InvalidVersion:
            incompatibilities.append({
                "contract": c_name,
                "reason": f"Invalid plugin version format '{c_ver}'",
                "plugin_version": c_ver,
                "host_supported": raw_range,
            })
            continue

        try:
            spec = SpecifierSet(norm_range)
        except InvalidSpecifier:
            incompatibilities.append({
                "contract": c_name,
                "reason": f"Invalid host specifier range '{raw_range}'",
                "plugin_version": c_ver,
                "host_supported": raw_range,
            })
            continue

        if v in spec:
            negotiated[c_name] = c_ver
        else:
            incompatibilities.append({
                "contract": c_name,
                "reason": f"Version '{c_ver}' does not satisfy host requirement '{raw_range}'",
                "plugin_version": c_ver,
                "host_supported": raw_range,
            })

    compatible = len(incompatibilities) == 0 and len(plugin_contracts) > 0
    status = "OK" if compatible else "PLUGIN_CONTRACT_INCOMPATIBLE"

    return ContractNegotiationResult(
        compatible=compatible,
        status=status,
        negotiated_contracts=negotiated,
        incompatibilities=incompatibilities,
    )

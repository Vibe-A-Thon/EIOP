"""Proof-of-Done bindings specification, validation, and storage (T-201 / REVA-PD-001 / §7.6.3)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Union
import yaml
from pydantic import BaseModel, ConfigDict, Field

from reva.core.errors import RevaValidationError
from reva.core.ids import binding_digest as compute_binding_digest
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.authority import Depth
from reva.kernel.store import RevaStore
from reva.pd.obligations import Obligation


class OwnerRef(BaseModel):
    """Source code or file owner specification."""

    model_config = ConfigDict(extra="forbid", strict=False)

    repo_id: str
    path: str
    symbol: str  # Qualified name (e.g. module.Class.method) or "*file*"
    language: str = "python"
    owner_digest: Optional[str] = None


class ContractTypeRef(BaseModel):
    """Contract schema, parser, or model reference."""

    model_config = ConfigDict(extra="forbid", strict=False)

    schema_ref: Optional[str] = None
    parser_ref: Optional[str] = None
    model_ref: Optional[str] = None


class FixtureRef(BaseModel):
    """Test fixture or file verification reference."""

    model_config = ConfigDict(extra="forbid", strict=False)

    fixture_id: str
    case_kind: str
    depth: Depth = Depth.UNIT
    path: str
    sha256: Optional[str] = None


class VerifierSpec(BaseModel):
    """Verifier execution command and sandbox configuration."""

    model_config = ConfigDict(extra="forbid", strict=False)

    verifier_id: str
    argv: List[str]
    workdir: str = "."
    depth: Depth = Depth.UNIT
    profile: str = "unit"
    timeout_s: int = 900
    env_allow: List[str] = Field(default_factory=list)
    network: Literal["none", "loopback", "compose"] = "none"


class NondeterminismSpec(BaseModel):
    """Execution nondeterminism model and bounds."""

    model_config = ConfigDict(extra="forbid", strict=False)

    mode: Literal["deterministic", "partial_order", "statistical"] = "deterministic"
    runs: Optional[int] = None
    min_pass_ratio: Optional[float] = None


class PerformanceBudget(BaseModel):
    """Performance budget threshold."""

    model_config = ConfigDict(extra="forbid", strict=False)

    metric: str = "p95_ms"
    threshold: Union[int, float] = 0  # int stays int: floats are forbidden in hash-bearing JCS
    dataset: Optional[str] = None


class ReviewRef(BaseModel):
    """Human review reference for obligation or binding."""

    model_config = ConfigDict(extra="forbid", strict=False)

    reviewed_by: Optional[str] = None
    review_warrant_id: Optional[str] = None


class Binding(BaseModel):
    """Normative binding linking an obligation to code owners, fixtures, and verifiers."""

    model_config = ConfigDict(extra="forbid", strict=False)

    obligation_key: str
    obligation_version: int = 1
    owners: List[OwnerRef] = Field(default_factory=list)
    contract_type: Optional[ContractTypeRef] = None
    fixtures: List[FixtureRef] = Field(default_factory=list)
    verifier: VerifierSpec
    journeys: List[str] = Field(default_factory=list)
    nondeterminism: Optional[NondeterminismSpec] = None
    performance_budget: Optional[PerformanceBudget] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=False)

    def digest(self) -> str:
        return compute_binding_digest(self.canonical_dict())


def validate_bindings(
    bindings: List[Binding],
    obligations: Optional[List[Obligation]] = None,
) -> None:
    """Validate binding completeness and consistency against referenced obligations."""
    seen_keys: Set[str] = set()
    for b in bindings:
        if b.obligation_key in seen_keys:
            raise RevaValidationError(f"Duplicate binding for obligation key: {b.obligation_key}")
        seen_keys.add(b.obligation_key)

        if not b.owners:
            raise RevaValidationError(f"Binding for {b.obligation_key} must declare at least one owner")

    if obligations:
        ob_map = {ob.key: ob for ob in obligations}
        for b in bindings:
            if b.obligation_key not in ob_map:
                raise RevaValidationError(
                    f"Binding references unknown obligation key '{b.obligation_key}'"
                )
            ob = ob_map[b.obligation_key]
            if b.obligation_version != ob.version:
                raise RevaValidationError(
                    f"Binding version ({b.obligation_version}) does not match obligation version ({ob.version}) for '{b.obligation_key}'"
                )

            # Contract type presence rule
            if ob.requires_contract_type and not b.contract_type:
                raise RevaValidationError(
                    f"Obligation '{b.obligation_key}' requires contract_type, but none declared in binding"
                )

            # Fixture case kinds must be a subset of obligation case kinds
            ob_case_kinds = set(ob.case_kinds)
            for f in b.fixtures:
                if f.case_kind not in ob_case_kinds:
                    raise RevaValidationError(
                        f"Binding fixture '{f.fixture_id}' has case_kind '{f.case_kind}' not in obligation case_kinds {sorted(list(ob_case_kinds))}"
                    )

            # Journeys required for acceptance depth when layer is user-facing
            if ob.depth == Depth.ACCEPTANCE and not b.journeys:
                # If layer or obligation implies acceptance journeys
                if any(x in ob.key.lower() for x in ["ui", "api", "mcp", "cli", "journey"]):
                    raise RevaValidationError(
                        f"Acceptance obligation '{b.obligation_key}' must declare at least one journey in binding"
                    )

            # Performance budget required when performance is in case_kinds
            if "performance" in ob.case_kinds and not b.performance_budget:
                raise RevaValidationError(
                    f"Obligation '{b.obligation_key}' has performance case kind but lacks performance_budget in binding"
                )


def load_bindings(yaml_source: Union[str, Path]) -> List[Binding]:
    """Parse bindings YAML file or text with validation."""
    if isinstance(yaml_source, Path) or (
        isinstance(yaml_source, str) and "\n" not in yaml_source and Path(yaml_source).is_file()
    ):
        content = Path(yaml_source).read_text(encoding="utf-8")
    else:
        content = str(yaml_source)

    parsed = yaml.safe_load(content)
    if not parsed:
        return []

    items = parsed.get("bindings") if isinstance(parsed, dict) and "bindings" in parsed else parsed
    if not isinstance(items, list):
        raise RevaValidationError("Bindings document must be a list or contain a 'bindings' list")

    bindings = [Binding.model_validate(it) for it in items]
    validate_bindings(bindings)
    return bindings


def sync_bindings(store: RevaStore, tenant_id: str, bindings: List[Binding]) -> int:
    """Persist bindings into store."""
    validate_bindings(bindings)
    cur = store.conn.cursor()
    count = 0
    now = format_ts(utc_now_ms())

    for b in bindings:
        digest = b.digest()
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_bindings (
                tenant_id, obligation_key, obligation_version, binding_digest, binding, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                b.obligation_key,
                b.obligation_version,
                digest,
                b.model_dump_json(),
                now,
            ),
        )
        count += 1

    store.conn.commit()
    return count

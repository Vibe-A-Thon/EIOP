"""Obligation specifications, DAG validation, and repository persistence (T-201 / REVA-PD-001 / §7.6.2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Set, Union
import yaml
from pydantic import BaseModel, ConfigDict, Field

from reva.core.errors import RevaValidationError
from reva.core.ids import obligation_digest as compute_obligation_digest
from reva.kernel.authority import Authority, Depth, Epistemic
from reva.kernel.store import RevaStore

CaseKind = Literal[
    "positive",
    "negative",
    "malformed",
    "boundary",
    "concurrency",
    "lifecycle",
    "tamper",
    "leak",
    "scale",
    "static",
    "unit",
    "integration",
    "acceptance",
]


class Obligation(BaseModel):
    """Normative specification obligation defined in YAML."""

    model_config = ConfigDict(extra="forbid", strict=False)

    key: str
    version: int = 1
    requirement_id: str
    title: str
    description: str = ""
    case_kinds: List[str] = Field(default_factory=lambda: ["positive"])
    depth: Depth = Depth.UNIT
    authority: Authority = Authority.CONTROLLED_EXECUTION
    epistemic_state: Epistemic = Epistemic.OBSERVED
    dependencies: List[str] = Field(default_factory=list)
    requires_contract_type: Optional[str] = None
    disposition: Literal["active", "waived", "deprecated"] = "active"
    reviewed_warrant_id: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=False)

    def digest(self) -> str:
        return compute_obligation_digest(self.canonical_dict())


def validate_obligations_dag(obligations: List[Obligation]) -> None:
    """Validate uniqueness and acyclicity of obligation dependency graph."""
    keys: Set[str] = set()
    adj: Dict[str, List[str]] = {}

    for ob in obligations:
        if ob.key in keys:
            raise RevaValidationError(f"Duplicate obligation key: {ob.key}")
        keys.add(ob.key)
        adj[ob.key] = list(ob.dependencies)

    # Check that all referenced dependencies exist
    for ob in obligations:
        for dep in ob.dependencies:
            if dep not in keys:
                raise RevaValidationError(f"Obligation {ob.key} depends on unknown obligation {dep}")

    # DFS cycle detection
    visited: Dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

    def dfs(node: str, path: List[str]) -> None:
        visited[node] = 1
        for neighbor in adj.get(node, []):
            if visited.get(neighbor) == 1:
                cycle_path = " -> ".join(path + [neighbor])
                raise RevaValidationError(f"Cyclic obligation dependency detected: {cycle_path}")
            if visited.get(neighbor, 0) == 0:
                dfs(neighbor, path + [neighbor])
        visited[node] = 2

    for k in keys:
        if visited.get(k, 0) == 0:
            dfs(k, [k])


def load_obligations(yaml_source: Union[str, Path]) -> List[Obligation]:
    """Parse obligations YAML file or text with validation and DAG cycle check."""
    if isinstance(yaml_source, Path) or (isinstance(yaml_source, str) and "\n" not in yaml_source and Path(yaml_source).is_file()):
        content = Path(yaml_source).read_text(encoding="utf-8")
    else:
        content = str(yaml_source)

    parsed = yaml.safe_load(content)
    if not parsed:
        return []

    items = parsed.get("obligations") if isinstance(parsed, dict) and "obligations" in parsed else parsed
    if not isinstance(items, list):
        raise RevaValidationError("Obligations document must be a list or contain an 'obligations' list")

    obligations = [Obligation.model_validate(it) for it in items]
    validate_obligations_dag(obligations)
    return obligations


def sync_obligations(store: RevaStore, tenant_id: str, obligations: List[Obligation]) -> int:
    """Persist obligations into store with version change verification."""
    validate_obligations_dag(obligations)
    cur = store.conn.cursor()
    count = 0

    for ob in obligations:
        digest = ob.digest()
        row = cur.execute(
            "SELECT version, digest FROM reva_obligations WHERE tenant_id = ? AND key = ? ORDER BY version DESC LIMIT 1",
            (tenant_id, ob.key),
        ).fetchone()

        if row:
            stored_v = row["version"]
            stored_d = row["digest"]
            if stored_d != digest and ob.version <= stored_v:
                raise RevaValidationError(
                    f"Obligation {ob.key} definition changed without version increment (current version {stored_v})"
                )

        cur.execute(
            """
            INSERT OR REPLACE INTO reva_obligations (
                tenant_id, key, version, digest, definition, reviewed_warrant_id, disposition
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                ob.key,
                ob.version,
                digest,
                ob.model_dump_json(),
                ob.reviewed_warrant_id,
                ob.disposition,
            ),
        )
        count += 1

    store.conn.commit()
    return count

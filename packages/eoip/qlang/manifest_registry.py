"""Exact grammar and capability manifest registry per dialect and backend (CRA-024.1).

Validates queries against declared dialect grammar manifests. Any construct
not supported or explicitly marked unsupported fails with UNSUPPORTED_CAPABILITY.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional
import yaml
from pydantic import BaseModel, Field

from eoip.capabilities.model import UnsupportedCapabilityError


class DialectManifest(BaseModel):
    dialect: str
    backend: str
    supported_constructs: list[str] = Field(default_factory=list)
    unsupported_constructs: list[str] = Field(default_factory=list)
    capabilities: dict[str, Any] = Field(default_factory=dict)

    def is_construct_supported(self, construct: str) -> bool:
        c_upper = construct.strip().upper()
        if any(u.upper() == c_upper for u in self.unsupported_constructs):
            return False
        return any(s.upper() == c_upper for s in self.supported_constructs)


class ManifestRegistry:
    """Registry of dialect and backend grammar manifests."""

    _instance: Optional[ManifestRegistry] = None

    def __init__(self, manifest_dir: Optional[Path] = None) -> None:
        if manifest_dir is None:
            manifest_dir = Path(__file__).parent / "manifests"
        self.manifest_dir = manifest_dir
        self._manifests: dict[str, DialectManifest] = {}
        self.reload()

    @classmethod
    def get_instance(cls) -> ManifestRegistry:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reload(self) -> None:
        self._manifests.clear()
        if not self.manifest_dir.exists():
            return
        for yml_file in self.manifest_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(yml_file.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "dialect" in data:
                    manifest = DialectManifest(**data)
                    self._manifests[manifest.dialect.upper()] = manifest
            except Exception:
                pass

    def get_manifest(self, dialect: str) -> DialectManifest:
        d = dialect.strip().upper()
        if d not in self._manifests:
            raise UnsupportedCapabilityError(capability_id=dialect, construct=None)
        return self._manifests[d]

    def validate_dialect_construct(self, dialect: str, construct: str) -> None:
        manifest = self.get_manifest(dialect)
        if not manifest.is_construct_supported(construct):
            raise UnsupportedCapabilityError(capability_id=dialect, construct=construct)

    def check_query_constructs(self, dialect: str, query_text: str) -> None:
        """Inspects query text for explicitly unsupported constructs."""
        manifest = self.get_manifest(dialect)
        q_upper = query_text.upper()

        # Check explicit unsupported constructs
        for unsupp in manifest.unsupported_constructs:
            u_upper = unsupp.upper()
            # If construct is like 'DROP_TABLE' or 'EXEC', match words or token
            parts = u_upper.split("_")
            pattern = r"\b" + r"\s+".join(map(re.escape, parts)) + r"\b"
            if re.search(pattern, q_upper):
                raise UnsupportedCapabilityError(capability_id=dialect, construct=unsupp)

        # Special check for unbounded property paths in SPARQL
        if manifest.dialect == "SPARQL":
            # Match unbounded paths like :prop* or :prop+ or (/)+ without limits
            from eoip.query.sparql_backend import has_unbounded_path  # algebra, not text (CRA-024.7)

            if has_unbounded_path(query_text):
                raise UnsupportedCapabilityError(
                    capability_id=dialect,
                    construct="UNBOUNDED_PROPERTY_PATH"
                )

        # Special check for raw script execution or eval
        if any(unsupp in ("RAW_SCRIPT", "EVAL_CODE") for unsupp in manifest.unsupported_constructs):
            if re.search(r"\b(EXEC|EVAL|SCRIPT)\b", q_upper):
                raise UnsupportedCapabilityError(capability_id=dialect, construct="RAW_SCRIPT")

    def list_manifests(self) -> dict[str, Any]:
        return {k: v.model_dump() for k, v in self._manifests.items()}

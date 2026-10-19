"""REVA configuration module holding RevaSettings and environment loader (T-003)."""

from __future__ import annotations

import base64
import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RevaSettings(BaseSettings):
    """Central configuration for REVA."""

    model_config = SettingsConfigDict(
        env_prefix="REVA_",
        case_sensitive=False,
        extra="ignore",
    )

    enabled: bool = False
    store_url: str = "sqlite:///data/reva/reva.db"
    blob_root: str = "data/reva/blobs"
    kek: str = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="  # 32 zero bytes in base64
    sth_interval_s: int = 60
    audit_sample: float = 0.01
    sth_witness_dir: Optional[str] = None
    graph_projection: bool = True
    graph_warrant_ref_cap: int = 32
    ingest_warrants: bool = False
    answer_contract: bool = False
    mcp: bool = True
    ui: bool = True
    pd_boards: bool = True
    max_runs: int = 2
    reruns: int = 3
    mutation_min: float = 0.70
    sandbox_mode: str = "auto"
    response_max_bytes: int = 262144
    response_max_tokens: int = 32000
    continuation_ttl_s: int = 3600
    ab_max_file_bytes: int = 2097152
    service_url_map: Dict[str, Any] = Field(default_factory=dict)
    service_account_patterns: List[str] = Field(
        default_factory=lambda: [
            r"svc-[a-z0-9-]+",
            r"sa-[a-z0-9-]+",
            r"[a-z0-9-]+@[a-z0-9-]+\.iam\.gserviceaccount\.com",
        ]
    )
    as_log_mappings: Dict[str, Any] = Field(default_factory=dict)
    as_caller_map: Dict[str, Any] = Field(default_factory=dict)
    db_sample_rows: int = 0
    db_allow_writable_role: bool = False
    rr_min_window_days: int = 30
    auto_probes: bool = False
    gap_weights: Dict[str, int] = Field(
        default_factory=lambda: {"low": 1, "medium": 2, "high": 4, "critical": 8}
    )
    jira_writeback: bool = False
    vuln_match: bool = False
    osv_mirror_dir: Optional[str] = None
    ga_uncited_policy: str = "drop"
    acl_propagation_s: int = 60
    min_free_gb: int = 10
    bootstrap_reviewer: Optional[str] = None
    allow_degraded_unit: bool = False
    mutation_max_mutants: int = 60
    sp_max_binary_scan: int = 200
    as_max_record_bytes: int = 8388608
    db_instance_map: Dict[str, Any] = Field(default_factory=dict)
    service_name_map: Dict[str, Any] = Field(default_factory=dict)

    @field_validator(
        "service_url_map",
        "service_account_patterns",
        "as_log_mappings",
        "as_caller_map",
        "gap_weights",
        "db_instance_map",
        "service_name_map",
        mode="before",
    )
    @classmethod
    def parse_json_fields(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception as exc:
                raise ValueError(f"Invalid JSON string in configuration: {exc}") from exc
        return v

    @field_validator("kek")
    @classmethod
    def validate_kek(cls, v: str) -> str:
        try:
            raw = base64.b64decode(v)
            if len(raw) != 32:
                raise ValueError(f"REVA_KEK must decode to exactly 32 bytes, got {len(raw)}")
        except Exception as exc:
            raise ValueError(f"Invalid base64 KEK: {exc}") from exc
        return v


_current_settings: Optional[RevaSettings] = None


def get_settings() -> RevaSettings:
    """Return the active RevaSettings instance."""
    global _current_settings
    if _current_settings is None:
        _current_settings = RevaSettings()
    return _current_settings


def set_settings(s: Optional[RevaSettings]) -> None:
    """Set the active RevaSettings instance or clear it."""
    global _current_settings
    _current_settings = s


def clear_settings_cache() -> None:
    """Clear cached settings for test isolation."""
    global _current_settings
    _current_settings = None

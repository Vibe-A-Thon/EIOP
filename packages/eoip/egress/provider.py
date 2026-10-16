"""Service Provider plugin manifests with Data-Flow declarations (SR-CON-010/011).

Cloud capabilities (object storage, managed graph DB, KMS, IdP, queues,
LLM endpoints, monitoring sinks, ...) are delivered as installable
Service Provider plugins. Every plugin MUST ship a Data-Flow Manifest
declaring: data classes sent/received, destinations, regions, retention,
and whether data can leave the tenant boundary (SR-CON-011).

Installation MUST display the Data-Flow declaration and require admin
approval; the egress gateway enforces it at runtime — a plugin whose
Data-Flow manifest declares egress cannot be installed without the
admin consent record (SR-LLM-017) and the gateway denies calls that
exceed the declared data classes.

SR-CON-012 reference adapters (hyperscaler object storage / KMS /
identity / managed graph+search) are External gate: the contracts here
are provider-agnostic.
"""

from __future__ import annotations

import time
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PluginCapability(str):
    OBJECT_STORAGE = "object_storage"
    MANAGED_GRAPH_DB = "managed_graph_db"
    MANAGED_SEARCH = "managed_search"
    KMS_HSM = "kms_hsm"
    IDP = "idp"
    QUEUE = "queue"
    LLM_ENDPOINT = "llm_endpoint"
    MONITORING_SINK = "monitoring_sink"
    OCR = "ocr"


KNOWN_PLUGIN_CAPABILITIES: frozenset[str] = frozenset({
    PluginCapability.OBJECT_STORAGE, PluginCapability.MANAGED_GRAPH_DB,
    PluginCapability.MANAGED_SEARCH, PluginCapability.KMS_HSM,
    PluginCapability.IDP, PluginCapability.QUEUE,
    PluginCapability.LLM_ENDPOINT, PluginCapability.MONITORING_SINK,
    PluginCapability.OCR,
})


class DataFlowManifest(BaseModel):
    """Data-Flow declaration every Service Provider plugin MUST ship (SR-CON-011)."""

    model_config = ConfigDict(extra="forbid")

    data_classes_sent: list[str] = Field(default_factory=list, description="D0-D4 classes sent to the provider")
    data_classes_received: list[str] = Field(default_factory=list, description="D0-D4 classes received back")
    tags: list[str] = Field(default_factory=list, description="Orthogonal tags (PII, PHI, ...) that may flow")
    destinations: list[str] = Field(default_factory=list, description="Destination URLs / service endpoints")
    regions: list[str] = Field(default_factory=list, description="Processing regions")
    retention: str = Field(default="none", description="Provider retention assertion, e.g. 'zero_retention'")
    crosses_boundary: bool = Field(
        default=False,
        description="True when tenant data leaves the trust boundary (requires egress gateway enforcement)",
    )

    @field_validator("data_classes_sent", "data_classes_received")
    @classmethod
    def _valid_classes(cls, value: list[str]) -> list[str]:
        bad = [c for c in value if c not in {"D0", "D1", "D2", "D3", "D4"}]
        if bad:
            raise ValueError(f"unknown data classes: {bad}")
        return value


class ServiceProviderManifest(BaseModel):
    """Installable Service Provider plugin manifest (SR-CON-010)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Stable id, e.g. urn:eoip:egress:provider:<slug>")
    name: str = Field(min_length=1)
    version: str = "1.0.0"
    capability: str = Field(description=f"One of {sorted(KNOWN_PLUGIN_CAPABILITIES)}")
    provider: str = Field(default="", description="Vendor / operator name")
    data_flow: DataFlowManifest

    @field_validator("capability")
    @classmethod
    def _known_capability(cls, value: str) -> str:
        if value not in KNOWN_PLUGIN_CAPABILITIES:
            raise ValueError(
                f"unknown capability {value!r}; known: {sorted(KNOWN_PLUGIN_CAPABILITIES)}"
            )
        return value


class PluginInstallRecord(BaseModel):
    """Admin approval record for a plugin installation (SR-CON-011, SR-LLM-017)."""

    model_config = ConfigDict(extra="forbid")

    record_id: str
    manifest_id: str
    approved_by: str
    approved_at: float
    consent_ref: str = Field(default="", description="Signer/date/DPA reference of the admin consent")
    acknowledged_data_flow: bool = False


class PluginRegistry:
    """Registry of submitted/approved Service Provider plugins (SR-CON-010/011)."""

    def __init__(self) -> None:
        self._manifests: dict[str, ServiceProviderManifest] = {}
        self._installs: dict[str, PluginInstallRecord] = {}

    def submit(self, manifest: ServiceProviderManifest) -> None:
        self._manifests[manifest.id] = manifest

    def install(self, manifest_id: str, *, approved_by: str,
                consent_ref: str = "") -> PluginInstallRecord:
        """Install requires admin approval with the Data-Flow acknowledged (SR-CON-011)."""
        manifest = self._manifests.get(manifest_id)
        if manifest is None:
            raise KeyError(f"unknown plugin manifest {manifest_id}")
        if manifest.data_flow.crosses_boundary and not consent_ref:
            raise ValueError(
                "plugin crosses the tenant boundary: a consent/contract "
                "record (SR-LLM-017) is required before installation"
            )
        record = PluginInstallRecord(
            record_id=f"urn:eoip:egress:install:{uuid.uuid4().hex[:12]}",
            manifest_id=manifest_id,
            approved_by=approved_by,
            approved_at=time.time(),
            consent_ref=consent_ref,
            acknowledged_data_flow=True,
        )
        self._installs[manifest_id] = record
        return record

    def is_installed(self, manifest_id: str) -> bool:
        return manifest_id in self._installs

    def get(self, manifest_id: str) -> ServiceProviderManifest | None:
        return self._manifests.get(manifest_id)

    def install_record(self, manifest_id: str) -> PluginInstallRecord | None:
        return self._installs.get(manifest_id)

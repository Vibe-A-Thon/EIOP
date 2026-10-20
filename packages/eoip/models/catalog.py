"""Model registry with offline signed bundles (SR-LLM-003).

Per model: source, content hash, license terms (including whether commercial redistribution is
allowed - open-weight licenses differ), intended tasks, hardware profile, evaluation scores and
approval status. Offline model bundles are a directory with ``bundle.json`` (manifest listing every
file with its SHA-256) and ``bundle.sig`` (Ed25519 signature over the canonical manifest). A bundle
imports only if the signature verifies against a trusted publisher key and every file hash matches.
"""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RETIRED = "retired"


@dataclass(frozen=True)
class LicenseTerms:
    license_id: str  # e.g. "apache-2.0", "llama3.1-community", "gemma"
    commercial_use: bool
    commercial_redistribution: bool
    restrictions: tuple[str, ...] = ()


@dataclass
class ModelRecord:
    model_id: str
    source: str
    sha256: str
    license: LicenseTerms
    intended_tasks: tuple[str, ...]
    hardware_profile: str  # cpu-small | single-gpu | multi-gpu | air-gapped-appliance
    eval_scores: dict[str, float] = field(default_factory=dict)
    approval: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: str | None = None
    bundle_publisher: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["approval"] = self.approval.value
        return d


class BundleRejected(ValueError):
    pass


def _canonical(manifest: dict[str, Any]) -> bytes:
    return json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_bundle(directory: Path, *, model: dict[str, Any], private_key: Ed25519PrivateKey,
                 publisher: str) -> dict[str, Any]:
    """Write ``bundle.json`` + ``bundle.sig`` for the files already in ``directory`` (publisher side)."""
    files = {p.name: _sha256_file(p) for p in sorted(directory.iterdir())
             if p.is_file() and p.name not in {"bundle.json", "bundle.sig"}}
    manifest = {"publisher": publisher, "model": model, "files": files}
    (directory / "bundle.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    (directory / "bundle.sig").write_text(base64.b64encode(private_key.sign(_canonical(manifest))).decode())
    return manifest


class ModelCatalog:
    def __init__(self, *, trusted_publishers: dict[str, Ed25519PublicKey] | None = None,
                 min_eval_score: float = 0.0) -> None:
        self.models: dict[str, ModelRecord] = {}
        self.trusted = trusted_publishers or {}
        self.min_eval_score = min_eval_score
        self.audit: list[dict[str, Any]] = []

    def register(self, record: ModelRecord) -> ModelRecord:
        if record.model_id in self.models:
            raise ValueError(f"model {record.model_id} already registered")
        if len(record.sha256) != 64:
            raise ValueError("sha256 must be a 64-hex content hash")
        record.approval = ApprovalStatus.PENDING
        self.models[record.model_id] = record
        self.audit.append({"event": "model.registered", "model_id": record.model_id})
        return record

    def import_bundle(self, directory: Path) -> ModelRecord:
        """Offline import: verify signature, then every file hash, then register (pending)."""
        try:
            manifest = json.loads((directory / "bundle.json").read_text())
            signature = base64.b64decode((directory / "bundle.sig").read_text())
        except (OSError, ValueError) as exc:
            raise BundleRejected(f"unreadable bundle: {type(exc).__name__}") from exc
        key = self.trusted.get(manifest.get("publisher", ""))
        if key is None:
            raise BundleRejected("publisher is not trusted")
        try:
            key.verify(signature, _canonical(manifest))
        except InvalidSignature as exc:
            raise BundleRejected("bundle signature does not verify") from exc
        present = {p.name for p in directory.iterdir() if p.is_file()} - {"bundle.json", "bundle.sig"}
        if present != set(manifest["files"]):
            raise BundleRejected("bundle file list does not match the signed manifest")
        for name, digest in manifest["files"].items():
            if _sha256_file(directory / name) != digest:
                raise BundleRejected(f"hash mismatch for {name}")
        m = manifest["model"]
        weights_hash = manifest["files"][m["weights_file"]]
        record = ModelRecord(model_id=m["model_id"], source=m["source"], sha256=weights_hash,
                             license=LicenseTerms(**{**m["license"], "restrictions": tuple(m["license"].get(
                                 "restrictions", ()))}),
                             intended_tasks=tuple(m["intended_tasks"]), hardware_profile=m["hardware_profile"],
                             eval_scores=dict(m.get("eval_scores", {})), bundle_publisher=manifest["publisher"])
        return self.register(record)

    def approve(self, model_id: str, *, approver: str, use: str = "internal") -> ModelRecord:
        """Approval needs evaluation scores above the floor and a license that permits the use."""
        rec = self.models[model_id]
        if not rec.eval_scores or min(rec.eval_scores.values()) < self.min_eval_score:
            raise PermissionError("model evaluation scores are missing or below the approval floor")
        if use in {"commercial", "redistribution"} and not rec.license.commercial_use:
            raise PermissionError(f"license {rec.license.license_id} does not permit commercial use")
        if use == "redistribution" and not rec.license.commercial_redistribution:
            raise PermissionError(f"license {rec.license.license_id} restricts commercial redistribution")
        rec.approval, rec.approved_by = ApprovalStatus.APPROVED, approver
        self.audit.append({"event": "model.approved", "model_id": model_id, "approver": approver, "use": use})
        return rec

    def approved_for(self, task: str) -> list[ModelRecord]:
        return [r for r in self.models.values() if r.approval is ApprovalStatus.APPROVED and task in r.intended_tasks]

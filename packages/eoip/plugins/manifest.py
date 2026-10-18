"""Signed plugin manifest and declarative configuration validation (CRA-002.3, CRA-002.4).

Enforces:
1. Manifest structure with publisher identity, dependencies, permissions, config schema, migrations, uninstall.
2. File digest verification (SHA-256 for all plugin contents).
3. Cryptographic Ed25519 signature verification.
4. Declarative configuration validation rejecting code execution or shell escapes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519


# Patterns indicating forbidden code injection or shell execution in config fields (CRA-002.4)
_DANGEROUS_PATTERNS = [
    re.compile(r"__import__", re.IGNORECASE),
    re.compile(r"\b(eval|exec|compile)\s*\(", re.IGNORECASE),
    re.compile(r"\b(os\.system|subprocess\.)", re.IGNORECASE),
    re.compile(r"[;&|`$><]", re.IGNORECASE),  # shell metacharacters
    re.compile(r"^[a-zA-Z0-9_\.]+\:[a-zA-Z0-9_]+$"),  # module:function reference
]


class ManifestValidationError(ValueError):
    """Raised when manifest validation fails."""
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


@dataclass
class PluginPermission:
    resource: str  # e.g. "graph_read", "graph_write", "network", "filesystem", "models"
    scope: str = "*"
    description: str = ""


@dataclass
class PluginUninstallPolicy:
    retention: str = "retain"  # "retain", "delete", "archive"
    cleanup_tables: list[str] = field(default_factory=list)
    preserve_audit_logs: bool = True


@dataclass
class SignedPluginManifest:
    manifest_version: str
    plugin_id: str
    publisher_identity: str
    version: str
    contracts: dict[str, str]  # contract_name -> semver
    dependencies: list[str]  # e.g. ["pydantic>=2.0.0"]
    permissions: list[PluginPermission]
    config_schema: dict[str, Any]
    file_digests: dict[str, str]  # relative_path -> sha256_hex
    migrations: list[dict[str, Any]] = field(default_factory=list)
    uninstall: PluginUninstallPolicy = field(default_factory=PluginUninstallPolicy)
    public_key_hex: str = ""
    signature_hex: str = ""

    def canonical_bytes_for_signing(self) -> bytes:
        """Produce deterministic canonical JSON bytes excluding signature and public key."""
        data = asdict(self)
        data.pop("signature_hex", None)
        data.pop("public_key_hex", None)
        # canonical sorted json
        canonical_str = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return canonical_str.encode("utf-8")

    def sign(self, private_key: ed25519.Ed25519PrivateKey) -> str:
        """Sign manifest canonical bytes and populate signature_hex and public_key_hex."""
        payload = self.canonical_bytes_for_signing()
        sig = private_key.sign(payload)
        self.signature_hex = sig.hex()
        pub_bytes = private_key.public_key().public_bytes_raw()
        self.public_key_hex = pub_bytes.hex()
        return self.signature_hex

    def verify_signature(self) -> None:
        """Verify Ed25519 signature of the manifest."""
        if not self.signature_hex:
            raise ManifestValidationError("MANIFEST_UNSIGNED", "Plugin manifest has no signature")
        if not self.public_key_hex:
            raise ManifestValidationError("MANIFEST_UNSIGNED", "Plugin manifest has no public key")

        try:
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(self.public_key_hex))
            sig_bytes = bytes.fromhex(self.signature_hex)
        except Exception as e:
            raise ManifestValidationError("MANIFEST_SIGNATURE_INVALID", f"Invalid hex encoding: {e}")

        payload = self.canonical_bytes_for_signing()
        try:
            pub_key.verify(sig_bytes, payload)
        except InvalidSignature:
            raise ManifestValidationError(
                "MANIFEST_SIGNATURE_INVALID",
                f"Signature verification failed for plugin {self.plugin_id}",
            )

    def verify_file_digests(self, plugin_dir: Path) -> None:
        """Verify that all files in plugin_dir match recorded SHA-256 digests."""
        plugin_dir = plugin_dir.resolve()
        for rel_path, expected_digest in self.file_digests.items():
            # Check for path escape attempts in manifest
            if ".." in rel_path or os.path.isabs(rel_path):
                raise ManifestValidationError("MANIFEST_PATH_ESCAPE", f"Illegal file path in manifest: {rel_path}")
            file_path = (plugin_dir / rel_path).resolve()
            if not str(file_path).startswith(str(plugin_dir)):
                raise ManifestValidationError("MANIFEST_PATH_ESCAPE", f"Path escapes plugin directory: {rel_path}")
            if not file_path.is_file():
                raise ManifestValidationError("MANIFEST_FILE_MISSING", f"Manifest file missing on disk: {rel_path}")

            h = hashlib.sha256()
            with file_path.open("rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            actual_digest = h.hexdigest()
            if actual_digest.lower() != expected_digest.lower():
                raise ManifestValidationError(
                    "MANIFEST_DIGEST_MISMATCH",
                    f"Digest mismatch for {rel_path}: expected {expected_digest}, got {actual_digest}",
                )

    def validate_configuration(self, config: dict[str, Any]) -> None:
        """Validate declarative configuration for ordinary customization (CRA-002.4).

        Rejects arbitrary import/eval/shell execution attempts.
        """
        self._check_config_dict(config, path="")

    def _check_config_dict(self, d: dict[str, Any], path: str) -> None:
        for k, v in d.items():
            cur_path = f"{path}.{k}" if path else k
            # Check key
            for pat in _DANGEROUS_PATTERNS:
                if pat.search(str(k)):
                    raise ManifestValidationError(
                        "CONFIG_CODE_EXECUTION_DENIED",
                        f"Configuration key '{cur_path}' contains forbidden code or shell pattern",
                    )
            # Check value
            if isinstance(v, str):
                for pat in _DANGEROUS_PATTERNS:
                    if pat.search(v):
                        raise ManifestValidationError(
                            "CONFIG_CODE_EXECUTION_DENIED",
                            f"Configuration value at '{cur_path}' contains forbidden code or shell pattern: {v!r}",
                        )
            elif isinstance(v, dict):
                self._check_config_dict(v, cur_path)
            elif isinstance(v, list):
                for idx, item in enumerate(v):
                    item_path = f"{cur_path}[{idx}]"
                    if isinstance(item, str):
                        for pat in _DANGEROUS_PATTERNS:
                            if pat.search(item):
                                raise ManifestValidationError(
                                    "CONFIG_CODE_EXECUTION_DENIED",
                                    f"Configuration item at '{item_path}' contains forbidden code or shell pattern",
                                )
                    elif isinstance(item, dict):
                        self._check_config_dict(item, item_path)


def load_signed_manifest(manifest_path: Path) -> SignedPluginManifest:
    """Load and parse signed plugin manifest from eoip-plugin.json."""
    if not manifest_path.is_file():
        raise ManifestValidationError("MANIFEST_NOT_FOUND", f"Manifest not found: {manifest_path}")

    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ManifestValidationError("MANIFEST_JSON_INVALID", f"Manifest JSON parse error: {e}")

    # Build permissions
    perms = [
        PluginPermission(
            resource=p["resource"],
            scope=p.get("scope", "*"),
            description=p.get("description", ""),
        )
        for p in raw.get("permissions", [])
    ]

    # Build uninstall policy
    uninst = raw.get("uninstall", {})
    uninstall_policy = PluginUninstallPolicy(
        retention=uninst.get("retention", "retain"),
        cleanup_tables=uninst.get("cleanup_tables", []),
        preserve_audit_logs=uninst.get("preserve_audit_logs", True),
    )

    return SignedPluginManifest(
        manifest_version=raw.get("manifest_version", "1.0"),
        plugin_id=raw["plugin_id"],
        publisher_identity=raw["publisher_identity"],
        version=raw["version"],
        contracts=raw.get("contracts", {}),
        dependencies=raw.get("dependencies", []),
        permissions=perms,
        config_schema=raw.get("config_schema", {}),
        file_digests=raw.get("file_digests", {}),
        migrations=raw.get("migrations", []),
        uninstall=uninstall_policy,
        public_key_hex=raw.get("public_key_hex", ""),
        signature_hex=raw.get("signature_hex", ""),
    )

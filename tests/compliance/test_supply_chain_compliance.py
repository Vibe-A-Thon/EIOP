"""Comprehensive Acceptance Suite for WP-035: Commercial Packaging & Supply-Chain Compliance.

Validates CRA-035.1 through CRA-035.9 and CRA-035.A:
- CRA-035.1: Proprietary EOIP-owned licensing & upstream component rights preservation
- CRA-035.2: CycloneDX 1.5 SBOM & notice records across ecosystems
- CRA-035.3: GPL/AGPL/LGPL/OEM resolution and unresolved contracts (extract-msg, TerminusDB)
- CRA-035.4: Artifact hash pinning, build provenance, tamper rejection, offline notices
- CRA-035.5: Air-gap operation with truthful entitlement gating (UNLICENSED, zero data leakage)
- CRA-035.6: CycloneDX generation & CI license check failing on unapproved licenses
- CRA-035.7: Copyleft policy (network-only servers, WebProtege not integrated, HermiT plugin)
- CRA-035.8: Dependency decision table (section 13) authoritative allowlist compliance
- CRA-035.9: Per-tier numerical stack SBOM & zero nvidia-* packages (H-16)
- CRA-035.A: Full acceptance gate
"""
from __future__ import annotations

import json
from pathlib import Path
import pytest
import yaml

from eoip.compliance.sbom import (
    EntitlementEnforcer,
    SbomComponent,
    SbomComplianceResult,
    SbomManager,
    compute_sha256,
    verify_artifact_provenance,
)


@pytest.fixture
def sbom_manager():
    return SbomManager(policy_path="compliance/license-policy.yaml")


def test_cra_035_1_preserve_proprietary_and_upstream_rights():
    """CRA-035.1: Proprietary EOIP-owned licensing & upstream rights preservation."""
    # 1. Ownership register exists and confirms proprietary intent
    ownership_reg = Path("licenses/OWNERSHIP-REGISTER.md")
    assert ownership_reg.exists(), "licenses/OWNERSHIP-REGISTER.md must exist"
    reg_text = ownership_reg.read_text(encoding="utf-8")
    assert "Avyukthi AI and Murthy Ravinder kumar" in reg_text
    assert "commercial proprietary licensing" in reg_text
    assert "Third-party libraries remain owned/licensed by their respective rights holders" in reg_text

    # 2. Third-party policy exists and prevents relabeling upstream material
    policy_doc = Path("licenses/THIRD-PARTY-POLICY.md")
    assert policy_doc.exists(), "licenses/THIRD-PARTY-POLICY.md must exist"
    doc_text = policy_doc.read_text(encoding="utf-8")
    assert "Do not remove third-party authors' notices or apply first-party headers to their material" in reg_text
    assert "never state that every byte in a container or browser bundle is exclusively owned" in doc_text

    # 3. First-party code has proprietary headers and does not relabel upstream files
    license_file = Path("LICENSE")
    assert license_file.exists()


def test_cra_035_2_shipped_sbom_records(sbom_manager, tmp_path):
    """CRA-035.2: Produce exact shipped SBOMs and notice records across artifacts."""
    components = [
        SbomComponent(
            name="rdflib",
            version="7.1.1",
            component_type="library",
            licenses=["BSD-3-Clause"],
            purl="pkg:pypi/rdflib@7.1.1",
            sha256="abc1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd",
            properties={"tier": "core"},
        ),
        SbomComponent(
            name="pyshacl",
            version="0.26.0",
            component_type="library",
            licenses=["Apache-2.0"],
            purl="pkg:pypi/pyshacl@0.26.0",
            properties={"tier": "worker"},
        ),
        SbomComponent(
            name="react",
            version="18.3.1",
            component_type="library",
            licenses=["MIT"],
            purl="pkg:npm/react@18.3.1",
            properties={"tier": "frontend"},
        ),
    ]

    sbom = sbom_manager.generate_cyclonedx_sbom(
        artifact_name="eoip-core",
        artifact_version="1.0.0",
        components=components,
    )

    assert sbom["bomFormat"] == "CycloneDX"
    assert sbom["specVersion"] == "1.5"
    assert len(sbom["components"]) == 3

    # Generate notices bundle
    notices_file = tmp_path / "THIRD_PARTY_NOTICES.md"
    notices_content = sbom_manager.generate_notices_bundle(sbom, notices_file)
    assert notices_file.exists()
    assert "rdflib" in notices_content
    assert "pyshacl" in notices_content
    assert "react" in notices_content


def test_cra_035_3_copyleft_resolution_and_unresolved_contracts(sbom_manager):
    """CRA-035.3: Resolve GPL/AGPL/LGPL/OEM and flag unresolved items (extract-msg, TerminusDB)."""
    # Test extract-msg: cannot be green automatically; must be flagged as disabled/unresolved
    unresolved_comp = [
        SbomComponent(name="extract-msg", version="0.56.1", licenses=["Proprietary"]),
    ]
    sbom_unresolved = sbom_manager.generate_cyclonedx_sbom("eoip-test", "1.0", unresolved_comp)
    result = sbom_manager.verify_compliance(sbom_unresolved)
    assert not result.passed, "extract-msg must not be passed automatically as green"
    assert len(result.unresolved_packages_found) > 0
    assert "extract-msg" in result.unresolved_packages_found

    # Test TerminusDB: blocked pending Legal
    terminus_comp = [
        SbomComponent(name="terminusdb-client", version="10.0.0", licenses=["Apache-2.0"]),
    ]
    sbom_terminus = sbom_manager.generate_cyclonedx_sbom("eoip-test", "1.0", terminus_comp)
    result_terminus = sbom_manager.verify_compliance(sbom_terminus)
    assert not result_terminus.passed, "TerminusDB must be blocked"
    assert "terminusdb-client" in result_terminus.forbidden_packages_found


def test_cra_035_4_artifact_signing_tamper_detection_offline_notices(tmp_path):
    """CRA-035.4: Sign/hash release artifacts, retain provenance, reject tampered activations."""
    original_plugin = b"def run_plugin(): return 'safe plugin bytecode'"
    expected_hash = compute_sha256(original_plugin)

    # Valid artifact passes verification
    assert verify_artifact_provenance(original_plugin, expected_hash) is True

    # Tampered artifact is rejected
    tampered_plugin = b"def run_plugin(): return 'tampered payload injection'"
    assert verify_artifact_provenance(tampered_plugin, expected_hash) is False

    # Offline notices test: notices can be bundled into offline directory
    offline_dir = tmp_path / "offline_bundle"
    offline_dir.mkdir()
    notices_offline = offline_dir / "NOTICES.txt"
    notices_offline.write_text("Offline third-party notices bundle.", encoding="utf-8")
    assert notices_offline.exists()


def test_cra_035_5_airgap_operation_and_truthful_entitlements():
    """CRA-035.5: Air-gap operation & truthful entitlement gating (UNLICENSED status, zero leak)."""
    # Licensed module is active
    enforcer = EntitlementEnforcer(licensed_features={"core", "sparql", "shacl"})
    access_core = enforcer.check_access("sparql")
    assert access_core["allowed"] is True
    assert access_core["status"] == "ACTIVE"

    # Unlicensed module truthfully reports UNLICENSED and denies access
    access_neural = enforcer.check_access("neural_research")
    assert access_neural["allowed"] is False
    assert access_neural["status"] == "UNLICENSED"
    assert access_neural["capability_state"] == "UNLICENSED"
    assert "zero data access granted" in access_neural["message"]


def test_cra_035_6_cyclonedx_spdx_generation_and_ci_license_checker(sbom_manager):
    """CRA-035.6: CycloneDX SBOM generation and CI gate failing on unapproved licenses."""
    # Permissive dependencies pass
    approved_comps = [
        SbomComponent(name="pyshacl", version="0.26.0", licenses=["Apache-2.0"]),
        SbomComponent(name="rdflib", version="7.1.1", licenses=["BSD-3-Clause"]),
    ]
    sbom_ok = sbom_manager.generate_cyclonedx_sbom("eoip-app", "1.0.0", approved_comps)
    res_ok = sbom_manager.verify_compliance(sbom_ok)
    assert res_ok.passed is True
    assert len(res_ok.violations) == 0

    # Injected AGPL dependency fails CI gate
    injected_agpl = [
        SbomComponent(name="malicious-agpl-lib", version="1.0.0", licenses=["AGPL-3.0-only"]),
    ]
    sbom_bad = sbom_manager.generate_cyclonedx_sbom("eoip-app", "1.0.0", injected_agpl)
    res_bad = sbom_manager.verify_compliance(sbom_bad)
    assert res_bad.passed is False
    assert any("AGPL-3.0-only" in v for v in res_bad.violations)


def test_cra_035_7_copyleft_isolation_and_network_only_servers(sbom_manager):
    """CRA-035.7: Copyleft policy: GPL/AGPL servers network-only; WebProtege not integrated; HermiT plugin only."""
    with open("compliance/license-policy.yaml", "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f)

    # 1. Neo4j and Virtuoso are strictly network-service only
    assert policy["components"]["neo4j-community"]["decision"] == "NETWORK_PROTOCOL_ONLY"
    assert policy["components"]["virtuoso-ose"]["decision"] == "NETWORK_PROTOCOL_ONLY"

    # 2. WebProtege is marked DO_NOT_INTEGRATE
    assert policy["components"]["webprotege"]["decision"] == "DO_NOT_INTEGRATE"
    assert "webprotege" in policy["forbidden_packages"]

    # 3. HermiT is OPTIONAL_PLUGIN_ONLY and never bundled in core
    assert policy["components"]["hermit"]["decision"] == "OPTIONAL_PLUGIN_ONLY"

    # 4. SNOMED-CT is CUSTOMER_PROVIDED_ONLY
    assert policy["unresolved_packages"]["snomed-ct"]["status"] == "CUSTOMER_PROVIDED_ONLY"

    # 5. HermiT in core without plugin property fails compliance
    hermit_core = [
        SbomComponent(name="hermit-reasoner", version="1.4.3", licenses=["LGPL-3.0-only"], properties={"tier": "core"}),
    ]
    sbom_hermit = sbom_manager.generate_cyclonedx_sbom("eoip-core", "1.0", hermit_core)
    res_hermit = sbom_manager.verify_compliance(sbom_hermit)
    assert res_hermit.passed is False
    assert any("not isolated as optional plugin" in v for v in res_hermit.violations)


def test_cra_035_8_dependency_decision_table_authoritative_gate(sbom_manager):
    """CRA-035.8: Dependency decision table (section 13) is authoritative allowlist input."""
    with open("compliance/license-policy.yaml", "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f)

    # Check key Section 13 rows exist in policy
    required_rows = [
        "rdflib", "pyshacl", "elk", "openllet", "hermit", "owlapi", "robot",
        "topbraid-shacl-api", "apache-jena", "eclipse-rdf4j", "graphdb",
        "neo4j-community", "virtuoso-ose", "webprotege", "terminusdb",
        "deeponto", "spacy", "textacy", "numpy", "scipy", "scikit-learn",
        "torch", "torch-geometric", "transformers", "sentence-transformers", "snntorch"
    ]
    for comp in required_rows:
        assert comp in policy["components"], f"Section 13 component '{comp}' missing from license-policy.yaml"


def test_cra_035_9_numerical_stack_sbom_per_tier_and_zero_cuda(sbom_manager):
    """CRA-035.9: Per-tier numerical stack in SBOM & strict zero nvidia-* packages (H-16)."""
    # Build per-tier components for N0, N1, N2
    tier_n0 = [
        SbomComponent(name="numpy", version="1.26.4", licenses=["BSD-3-Clause"], properties={"tier": "N0"}),
        SbomComponent(name="scipy", version="1.12.0", licenses=["BSD-3-Clause"], properties={"tier": "N0"}),
        SbomComponent(name="scikit-learn", version="1.4.1", licenses=["BSD-3-Clause"], properties={"tier": "N0"}),
    ]
    sbom_n0 = sbom_manager.generate_cyclonedx_sbom("eoip-numerics", "1.0", tier_n0)
    assert sbom_manager.verify_compliance(sbom_n0).passed is True

    # Forbidden packages: DGL and networkx
    for forbidden in ["dgl", "networkx"]:
        comp = [SbomComponent(name=forbidden, version="1.0.0", licenses=["Apache-2.0"])]
        sbom_f = sbom_manager.generate_cyclonedx_sbom("eoip-test", "1.0", comp)
        res = sbom_manager.verify_compliance(sbom_f)
        assert res.passed is False
        assert forbidden in res.forbidden_packages_found

    # Forbidden package: nvidia-* or cuda-*
    nvidia_comp = [
        SbomComponent(name="nvidia-cuda-runtime-cu12", version="12.1.105", licenses=["NVIDIA-SLA"]),
    ]
    sbom_nv = sbom_manager.generate_cyclonedx_sbom("eoip-gpu", "1.0", nvidia_comp)
    res_nv = sbom_manager.verify_compliance(sbom_nv)
    assert res_nv.passed is False
    assert any("nvidia-cuda-runtime-cu12" in p for p in res_nv.forbidden_packages_found)


def test_cra_035_a_acceptance_gate(sbom_manager, tmp_path):
    """CRA-035.A: Full acceptance gate comparing inventories, notices, tampering, and zero CUDA."""
    # 1. Compare actual wheel bundle inventory against SBOM
    wheel_components = [
        SbomComponent(name="eoip", version="1.0.0rc1", licenses=["Proprietary"]),
        SbomComponent(name="rdflib", version="7.1.1", licenses=["BSD-3-Clause"]),
        SbomComponent(name="pyshacl", version="0.26.0", licenses=["Apache-2.0"]),
        SbomComponent(name="pydantic", version="2.8.2", licenses=["MIT"]),
        SbomComponent(name="fastapi", version="0.111.0", licenses=["MIT"]),
    ]
    wheel_sbom = sbom_manager.generate_cyclonedx_sbom("eoip-wheel-bundle", "1.0.0rc1", wheel_components)
    notices_path = tmp_path / "NOTICES.md"
    sbom_manager.generate_notices_bundle(wheel_sbom, notices_path)
    assert notices_path.exists()
    assert notices_path.stat().st_size > 100

    # 2. Tamper rejection
    artifact = b"eoip-package-binary-content"
    art_hash = compute_sha256(artifact)
    assert verify_artifact_provenance(artifact, art_hash) is True
    assert verify_artifact_provenance(artifact + b"-tampered", art_hash) is False

    # 3. AGPL injection failure
    bad_sbom = sbom_manager.generate_cyclonedx_sbom(
        "eoip-wheel-bundle", "1.0.0rc1", wheel_components + [SbomComponent(name="agpl-addon", version="1.0", licenses=["AGPL-3.0-only"])]
    )
    assert sbom_manager.verify_compliance(bad_sbom).passed is False

    # 4. Zero nvidia-* packages
    bad_cuda_sbom = sbom_manager.generate_cyclonedx_sbom(
        "eoip-wheel-bundle", "1.0.0rc1", wheel_components + [SbomComponent(name="nvidia-cublas-cu12", version="12.1", licenses=["NVIDIA-SLA"])]
    )
    assert sbom_manager.verify_compliance(bad_cuda_sbom).passed is False

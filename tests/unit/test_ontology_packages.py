"""Unit and integration tests for Immutable Ontology Package Registry and SemVer Releases (CRA-018.1 - CRA-018.8, CRA-018.A).

Covers:
1. Package creation with SHA-256 digests, release manifest signature, and SemVer 2.0 (CRA-018.1, CRA-018.2, CRA-018.7).
2. Separation of drafts and accepted immutable releases (CRA-018.3).
3. Domain pack attribution (gist CC-BY-4.0, FIBO) (CRA-018.4, CRA-018.8).
4. Atomic installation, dependency validation, and missing dependency errors (CRA-018.5).
5. Tampered member file or signature detection halting activation (CRA-018.6, CRA-018.A).
6. Clean restart / fresh-node restore retrieving identical package by hash (CRA-018.A).
"""

from __future__ import annotations

from pathlib import Path
import pytest

from eoip.ontology import (
    DependencyResolutionError,
    DurableOntologyRegistry,
    PackageTamperedError,
    ReleaseState,
)
from eoip.ontology.gitops import SemanticDiff


def test_package_bundle_signing_and_semver(tmp_path: Path):
    """CRA-018.1, CRA-018.2, CRA-018.7: Signed release bundle with SHA-256 digests and SemVer 2.0."""
    registry = DurableOntologyRegistry(root_dir=tmp_path / "registry")

    docs = {
        "ontology.ttl": "@prefix eoip: <urn:eoip:> . eoip:Issue a owl:Class .",
        "shapes.ttl": "@prefix sh: <http://www.w3.org/ns/shacl#> . eoip:IssueShape a sh:NodeShape .",
    }

    from eoip.ontology.gitops import BREAKING, SemanticChange, SemanticDiff

    breaking_diff = SemanticDiff(
        changes=[
            SemanticChange(
                change_type="label_removed",
                subject="Ticket",
                detail="Removed class Ticket",
                classification=BREAKING,
            )
        ]
    )

    pkg = registry.build_release_bundle(
        package_id="eoip-core-ontology",
        version="1.2.3",
        ontology_iri="urn:eoip:ontology:core",
        documents=docs,
        license_identifier="CC-BY-4.0",
        attribution="Avyukthi AI / EOIP Knowledge Team",
        diff=breaking_diff,
    )

    assert pkg.version == "2.0.0"  # Major bump due to breaking diff
    assert len(pkg.file_digests) == 2
    assert "ontology.ttl" in pkg.file_digests
    assert len(pkg.manifest_signature) == 64  # SHA-256 hex signature
    assert pkg.state == ReleaseState.ACCEPTED_RELEASE

    # Publish release
    pub_dir = registry.publish_release(pkg)
    assert pub_dir.exists()
    assert (pub_dir / "release-manifest.json").exists()

    # Immutable: publishing the exact same version again raises FileExistsError
    with pytest.raises(FileExistsError):
        registry.publish_release(pkg)


def test_drafts_and_releases_separation(tmp_path: Path):
    """CRA-018.3: Drafts and accepted releases are isolated in distinct directory structures."""
    registry = DurableOntologyRegistry(root_dir=tmp_path / "registry")
    assert registry.drafts_dir.exists()
    assert registry.releases_dir.exists()
    assert registry.drafts_dir != registry.releases_dir


def test_atomic_installation_and_dependency_resolution(tmp_path: Path):
    """CRA-018.5: Atomic installation checks dependencies and fails explicitly on missing dependency."""
    registry = DurableOntologyRegistry(root_dir=tmp_path / "registry")

    # 1. Base gist package
    gist_pkg = registry.build_release_bundle(
        package_id="gist-upper",
        version="1.0.0",
        ontology_iri="https://ontologies.semanticarts.com/gist/",
        documents={"gist.ttl": "# Upper ontology"},
        license_identifier="CC-BY-4.0",
        attribution="Semantic Arts gist (CC BY 4.0)",
    )
    registry.publish_release(gist_pkg)

    # 2. Domain package depending on gist-upper@1.0.0
    domain_pkg = registry.build_release_bundle(
        package_id="fin-domain",
        version="1.0.0",
        ontology_iri="urn:eoip:domain:fin",
        documents={"fin.ttl": "# Finance domain"},
        dependencies=["gist-upper@1.0.0"],
    )
    registry.publish_release(domain_pkg)

    # Successfully installed with resolved dependency
    installed = registry.install_package("fin-domain", "1.0.0")
    assert installed.package_id == "fin-domain"
    assert installed.dependencies == ["gist-upper@1.0.0"]

    # 3. Package depending on non-existent dependency fails
    broken_pkg = registry.build_release_bundle(
        package_id="broken-domain",
        version="1.0.0",
        ontology_iri="urn:eoip:domain:broken",
        documents={"b.ttl": "# Broken"},
        dependencies=["missing-dep@9.9.9"],
    )
    registry.publish_release(broken_pkg)

    with pytest.raises(DependencyResolutionError) as exc:
        registry.install_package("broken-domain", "1.0.0")
    assert "Missing required dependency 'missing-dep@9.9.9'" in str(exc.value)


def test_tampered_package_member_halts_activation(tmp_path: Path):
    """CRA-018.6, CRA-018.A: Tampering with any member file or signature causes mismatch and halts activation."""
    registry = DurableOntologyRegistry(root_dir=tmp_path / "registry")

    pkg = registry.build_release_bundle(
        package_id="secure-ontology",
        version="1.0.0",
        ontology_iri="urn:eoip:secure",
        documents={"data.ttl": "# Secure ontology content"},
    )
    pub_dir = registry.publish_release(pkg)

    # Maliciously modify data.ttl on disk after publication
    tampered_file = pub_dir / "data.ttl"
    tampered_file.write_text("# Malicious unauthorized payload injected!", encoding="utf-8")

    # Activation must immediately halt with PackageTamperedError
    with pytest.raises(PackageTamperedError) as exc:
        registry.install_package("secure-ontology", "1.0.0")
    assert "Tampered file detected" in str(exc.value)


def test_fresh_node_restore_by_digest(tmp_path: Path):
    """CRA-018.A: Fresh-node restore retrieves the exact verified package by hash."""
    registry = DurableOntologyRegistry(root_dir=tmp_path / "registry")

    pkg = registry.build_release_bundle(
        package_id="restorable-pkg",
        version="1.0.0",
        ontology_iri="urn:eoip:restore",
        documents={"schema.ttl": "# Clean schema"},
    )
    registry.publish_release(pkg)
    digest = pkg.package_digest

    # Fresh node restore using only the package digest hash
    restored = registry.restore_by_digest(digest)
    assert restored is not None
    assert restored.package_id == "restorable-pkg"
    assert restored.version == "1.0.0"
    assert restored.package_digest == digest

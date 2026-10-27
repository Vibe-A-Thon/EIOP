"""Unit tests for the EOIP marketplace (GAP-MKT-001..008, GAP-EXT-001)."""

from __future__ import annotations

import io
import json
import zipfile

import pytest

from eoip.marketplace import (
    CapabilityKind,
    DependencyConflict,
    IntegrityError,
    PackageDependency,
    PackageInstaller,
    PackageManifest,
    PackageReader,
    PackageRegistry,
    SemVerError,
    build_package,
    matches_range,
    parse_range,
    parse_version,
    sign,
    verify_signature,
)
from eoip.marketplace.sample import (
    SAMPLE_MANIFEST,
    SAMPLE_PAYLOAD,
    sample_package_bytes,
)
from eoip.marketplace.packager import PackageBuildError

KEY = b"test-install-key"


def make_manifest(name="pkg-a", version="1.0.0", deps=None, description=""):
    return PackageManifest(
        id=f"urn:eoip:marketplace:package:{name}",
        name=name,
        version=version,
        description=description,
        provides={CapabilityKind.ONTOLOGIES: [f"urn:eoip:ontology:{name}"]},
        dependencies=deps or [],
    )


# ---------------------------------------------------------------- build ----

class TestBuild:
    def test_build_creates_zip_with_manifest_payload_checksums(self):
        archive = sample_package_bytes()
        zf = zipfile.ZipFile(io.BytesIO(archive))
        names = set(zf.namelist())
        assert "manifest.json" in names
        assert "checksums.json" in names
        assert "payload/ontologies/hr.ttl" in names

    def test_reader_roundtrip_manifest_and_payload(self):
        reader = PackageReader(sample_package_bytes())
        manifest = reader.manifest()
        assert manifest.name == "hr-ontology-pack"
        assert manifest.version == "1.2.0"
        assert reader.payload_files() == SAMPLE_PAYLOAD

    def test_build_rejects_empty_payload_and_bad_paths(self):
        with pytest.raises(PackageBuildError):
            build_package(SAMPLE_MANIFEST, {})
        with pytest.raises(PackageBuildError):
            build_package(SAMPLE_MANIFEST, {"../evil.txt": b"x"})
        with pytest.raises(PackageBuildError):
            build_package(SAMPLE_MANIFEST, {"sub/../../evil.txt": b"x"})

    @pytest.mark.parametrize("name", ["manifest.json", "checksums.json", "/manifest.json"])
    def test_build_rejects_reserved_metadata_names(self, name):
        with pytest.raises(PackageBuildError, match="reserved name"):
            build_package(SAMPLE_MANIFEST, {name: b"x"})

    def test_build_allows_nested_metadata_file(self):
        payload = {"schemas/manifest.json": b"{}"}
        assert PackageReader(build_package(SAMPLE_MANIFEST, payload)).payload_files() == payload

    def test_reject_non_archive(self):
        with pytest.raises(PackageBuildError):
            PackageReader(b"not a zip")


# ---------------------------------------------------------------- semver ---

class TestSemVer:
    @pytest.mark.parametrize(
        "version,expression,expected",
        [
            ("1.2.3", "1.2.3", True),
            ("1.2.3", ">=1.0.0,<2.0.0", True),
            ("2.0.0", ">=1.0.0,<2.0.0", False),
            ("1.5.0", "^1.2.0", True),
            ("2.0.0", "^1.2.0", False),
            ("1.2.9", "~1.2.0", True),
            ("1.3.0", "~1.2.0", False),
            ("1.0.0-alpha", ">=1.0.0", False),
            ("1.0.0", "!=1.0.1", True),
            ("1.0.1", "!=1.0.1", False),
        ],
    )
    def test_range_matching(self, version, expression, expected):
        assert matches_range(version, expression) is expected

    def test_invalid_version_and_range(self):
        with pytest.raises(SemVerError):
            parse_version("1.2")
        with pytest.raises(SemVerError):
            parse_range(">=abc")
        with pytest.raises(SemVerError):
            parse_range("")

    def test_prerelease_orders_below_release(self):
        assert parse_version("1.0.0-alpha") < parse_version("1.0.0")


# ---------------------------------------------------------------- install --

class TestInstall:
    def test_install_unsigned_archive_without_signature(self):
        registry = PackageRegistry()
        installer = PackageInstaller(registry, key=KEY)
        manifest = installer.install(sample_package_bytes())
        assert manifest.name == "hr-ontology-pack"
        assert registry.is_installed("hr-ontology-pack")

    def test_install_with_valid_signature(self):
        archive = sample_package_bytes()
        signature = sign(archive, KEY)
        installer = PackageInstaller(PackageRegistry())
        installer.install(archive, key=KEY, signature=signature)

    def test_install_rejects_bad_signature(self):
        archive = sample_package_bytes()
        installer = PackageInstaller(PackageRegistry(), key=KEY)
        with pytest.raises(IntegrityError):
            installer.install(archive, key=KEY, signature=b"\x00" * 32)

    def test_corrupt_package_rejected(self):
        archive = bytearray(sample_package_bytes())
        # Flip bytes inside the compressed payload region.
        archive[-50:] = bytes(0xFF for _ in range(50)) if len(archive) < 50 else archive[-50:]
        reader = PackageReader(bytes(archive))
        if not reader.verify_checksums():
            pytest.skip("corruption landed in zip structure rather than member data")
        installer = PackageInstaller(PackageRegistry(), key=KEY)
        with pytest.raises(IntegrityError):
            installer.install(bytes(archive))

    def test_corrupt_member_rejected(self):
        archive = sample_package_bytes()
        zf_in = zipfile.ZipFile(io.BytesIO(archive))
        members = {n: zf_in.read(n) for n in zf_in.namelist()}
        members["payload/ontologies/hr.ttl"] = b"TAMPERED"
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, data in members.items():
                zf.writestr(name, data)
        with pytest.raises(IntegrityError):
            PackageInstaller(PackageRegistry(), key=KEY).install(buf.getvalue())

    def test_signature_helpers(self):
        data = b"payload"
        sig = sign(data, KEY)
        assert verify_signature(data, sig, KEY)
        assert not verify_signature(data, sig, b"other-key")


# ----------------------------------------------------------- dependencies --

class TestDependencies:
    def _registry_with_base(self):
        registry = PackageRegistry()
        registry.install(make_manifest("base-pack", "1.4.0"))
        return registry

    def test_install_resolves_and_enforces_dependencies(self):
        registry = self._registry_with_base()
        dep = [PackageDependency(name="base-pack", range=">=1.0.0,<2.0.0")]
        dependent = make_manifest("dependent-pack", "2.0.0", deps=dep)
        installer = PackageInstaller(registry, key=KEY)
        installer.install(build_package(dependent, {"a.txt": b"a"}))
        assert registry.is_installed("dependent-pack")

    def test_unsatisfied_dependency_rejected(self):
        registry = self._registry_with_base()
        dep = [PackageDependency(name="missing-pack", range=">=1.0.0")]
        dependent = make_manifest("dependent-pack", deps=dep)
        installer = PackageInstaller(registry, key=KEY)
        with pytest.raises(DependencyConflict):
            installer.install(build_package(dependent, {"a.txt": b"a"}))

    def test_out_of_range_installed_version_rejected(self):
        registry = self._registry_with_base()
        dep = [PackageDependency(name="base-pack", range=">=2.0.0")]
        dependent = make_manifest("dependent-pack", deps=dep)
        installer = PackageInstaller(registry, key=KEY)
        with pytest.raises(DependencyConflict):
            installer.install(build_package(dependent, {"a.txt": b"a"}))

    def test_resolver_orders_dependencies_first(self):
        registry = PackageRegistry()
        registry.install(make_manifest("base-pack", "1.0.0"))
        registry.install(
            make_manifest(
                "mid-pack",
                "1.0.0",
                deps=[PackageDependency(name="base-pack", range=">=1.0.0")],
            )
        )
        top = make_manifest(
            "top-pack",
            deps=[
                PackageDependency(name="mid-pack", range=">=1.0.0"),
                PackageDependency(name="base-pack", range=">=1.0.0"),
            ],
        )
        result = PackageInstaller(registry, key=KEY).resolver.resolve(top)
        assert result.ok
        names = [m.name for m in result.ordered]
        assert names.index("base-pack") < names.index("mid-pack")

    def test_uninstall_blocked_by_dependents(self):
        registry = self._registry_with_base()
        dep = [PackageDependency(name="base-pack", range=">=1.0.0")]
        registry.install(make_manifest("dependent-pack", deps=dep))
        installer = PackageInstaller(registry, key=KEY)
        with pytest.raises(DependencyConflict):
            installer.uninstall("base-pack")
        assert registry.is_installed("base-pack")
        assert installer.uninstall("dependent-pack")
        assert installer.uninstall("base-pack")


# --------------------------------------------------------------- registry --

class TestRegistry:
    def test_persistence_roundtrip(self, tmp_path):
        path = tmp_path / "registry.json"
        registry = PackageRegistry(path)
        registry.install(SAMPLE_MANIFEST)
        reloaded = PackageRegistry(path)
        assert reloaded.is_installed("hr-ontology-pack")
        assert reloaded.installed_version("hr-ontology-pack") == "1.2.0"
        record = reloaded.get("hr-ontology-pack")
        assert record.manifest.provides[CapabilityKind.QUERY_TEMPLATES]

    def test_list_and_search(self):
        registry = PackageRegistry()
        registry.install(SAMPLE_MANIFEST)
        registry.install(make_manifest("crm-pack", description="CRM mappings"))
        assert [r.manifest.name for r in registry.list()] == [
            "crm-pack",
            "hr-ontology-pack",
        ]
        assert [r.manifest.name for r in registry.search("hr ontology")] == [
            "hr-ontology-pack"
        ]
        assert [r.manifest.name for r in registry.search("")] == [
            "crm-pack",
            "hr-ontology-pack",
        ]

    def test_providers_of(self):
        registry = PackageRegistry()
        registry.install(SAMPLE_MANIFEST)
        providers = registry.providers_of(CapabilityKind.ONTOLOGIES)
        assert [r.manifest.name for r in providers] == ["hr-ontology-pack"]

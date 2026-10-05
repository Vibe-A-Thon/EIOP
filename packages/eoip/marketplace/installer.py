"""Dependency resolution and installation (GAP-MKT-004, GAP-MKT-005, GAP-MKT-006).

The resolver performs a deterministic topological resolution of a package's
dependency closure against an installed registry (stdlib only), picking the
highest already-installed version that satisfies each range. The installer
verifies checksums and the HMAC signature before registering a package, and
refuses uninstall while dependents remain.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from eoip.marketplace.manifest import PackageDependency, PackageManifest
from eoip.marketplace.packager import PackageReader
from eoip.marketplace.registry import PackageRegistry
from eoip.marketplace.semver import VersionRange


class DependencyConflict(Exception):
    """Raised when a dependency cannot be satisfied (GAP-MKT-004)."""


class IntegrityError(Exception):
    """Raised when checksum or signature verification fails (GAP-MKT-007)."""


@dataclass
class ResolutionResult:
    ordered: list[PackageManifest] = field(default_factory=list)
    """Dependency-first installation order (dependencies before dependents)."""

    missing: list[PackageDependency] = field(default_factory=list)
    """Dependencies with no installed candidate satisfying the range."""

    @property
    def ok(self) -> bool:
        return not self.missing


class DependencyResolver:
    """Resolve a manifest's dependency closure against the installed registry."""

    def __init__(self, registry: PackageRegistry) -> None:
        self._registry = registry

    def resolve(self, manifest: PackageManifest) -> ResolutionResult:
        result = ResolutionResult()
        visited: set[str] = set()
        visiting: set[str] = set()

        def visit(current: PackageManifest) -> None:
            for dep in current.dependencies:
                if dep.name in visiting:
                    raise DependencyConflict(f"cyclic dependency involving {dep.name}")
                candidate = self._registry.get(dep.name)
                if candidate is None or not VersionRange(dep.range).matches(
                    candidate.manifest.version
                ):
                    result.missing.append(dep)
                    continue
                if dep.name in visited:
                    continue
                visiting.add(dep.name)
                visit(candidate.manifest)
                visiting.discard(dep.name)
                visited.add(dep.name)
                result.ordered.append(candidate.manifest)

        visiting.add(manifest.name)
        visit(manifest)
        return result

    def dependents_of(self, name: str) -> list[str]:
        """Names of installed packages that declare a dependency on ``name``."""

        return [
            record.manifest.name
            for record in self._registry.list()
            if any(dep.name == name for dep in record.manifest.dependencies)
        ]


class PackageInstaller:
    """Verify, install and uninstall .eoipkg archives (GAP-MKT-005..007)."""

    def __init__(self, registry: PackageRegistry, *, key: bytes | None = None) -> None:
        self._registry = registry
        self._key = key
        self.resolver = DependencyResolver(registry)

    def install(self, archive: bytes, *, key: bytes | None = None, signature: bytes | None = None) -> PackageManifest:
        """Verify integrity then register the package.

        - Checksums are always verified against ``checksums.json``.
        - If ``signature`` is provided (or one is embedded as ``signature.bin``),
          it is verified with ``key`` / the installer's key / the env key.
        - Dependency ranges are checked against the installed registry; any
          unsatisfied dependency raises :class:`DependencyConflict`.
        """

        reader = PackageReader(archive)
        problems = reader.verify_checksums()
        if problems:
            raise IntegrityError("package integrity failure: " + "; ".join(problems))

        sig = signature
        if sig is None:
            try:
                import zipfile, io

                with zipfile.ZipFile(io.BytesIO(archive)) as zf:
                    sig = zf.read("signature.bin")
            except (KeyError, zipfile.BadZipFile):
                sig = None
        if sig is not None:
            from eoip.marketplace import signing

            verify_key = key if key is not None else self._key
            if verify_key is None:
                verify_key = signing.default_install_key()
            if not signing.verify_signature(archive, sig, verify_key):
                raise IntegrityError("package signature verification failed")

        manifest = reader.manifest()
        resolution = self.resolver.resolve(manifest)
        if not resolution.ok:
            missing = ", ".join(f"{d.name} {d.range}" for d in resolution.missing)
            raise DependencyConflict(f"unsatisfied dependencies for {manifest.name}: {missing}")

        self._registry.install(manifest)
        return manifest

    def uninstall(self, name: str) -> bool:
        """Remove a package; refuses while installed dependents remain."""

        dependents = self.resolver.dependents_of(name)
        if dependents:
            raise DependencyConflict(
                f"cannot uninstall {name}: required by {', '.join(sorted(dependents))}"
            )
        return self._registry.uninstall(name)

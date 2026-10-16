"""EOIP marketplace / extension packaging (GAP-MKT-001..008, GAP-EXT-001, §36, §45).

Builds, signs, verifies, installs and uninstalls ``.eoipkg`` extension
packages: zips with a Pydantic manifest, payload files, SHA-256 checksums,
and an HMAC-SHA256 signature using a shared install key (asymmetric
publisher signing is supported alongside HMAC; see §45).
"""

from eoip.marketplace.installer import (
    DependencyConflict,
    DependencyResolver,
    IntegrityError,
    PackageInstaller,
    ResolutionResult,
)
from eoip.marketplace.manifest import (
    CapabilityKind,
    PackageDependency,
    PackageManifest,
)
from eoip.marketplace.packager import (
    CHECKSUMS_FILENAME,
    MANIFEST_FILENAME,
    PackageBuildError,
    PackageReader,
    build_package,
    package_agent_workflow,
    package_connector_mapping,
    package_dashboard,
    package_query_template,
    package_validation_rules,
)
from eoip.marketplace.registry import InstalledRecord, PackageRegistry
from eoip.marketplace.semver import (
    SemVerError,
    Version,
    VersionRange,
    matches_range,
    parse_range,
    parse_version,
)
from eoip.marketplace.signing import (
    ENV_INSTALL_KEY,
    SIGNATURE_FILENAME,
    default_install_key,
    sign,
    sign_package_archive,
    strip_signature,
    verify_signature,
)

__all__ = [
    "CapabilityKind",
    "CHECKSUMS_FILENAME",
    "DependencyConflict",
    "DependencyResolver",
    "ENV_INSTALL_KEY",
    "InstalledRecord",
    "IntegrityError",
    "MANIFEST_FILENAME",
    "PackageBuildError",
    "PackageDependency",
    "PackageInstaller",
    "PackageManifest",
    "PackageReader",
    "PackageRegistry",
    "ResolutionResult",
    "SemVerError",
    "SIGNATURE_FILENAME",
    "Version",
    "VersionRange",
    "build_package",
    "default_install_key",
    "matches_range",
    "package_agent_workflow",
    "package_connector_mapping",
    "package_dashboard",
    "package_query_template",
    "package_validation_rules",
    "parse_range",
    "parse_version",
    "sign",
    "sign_package_archive",
    "strip_signature",
    "verify_signature",
]

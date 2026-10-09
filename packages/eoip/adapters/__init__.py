"""Database adapters package (gap analysis §6, SR-GDB-002/003/004).

Real protocol-compatible adapters (JanusGraph Gremlin-HTTP, Apache AGE query
builder, Neo4j verification), capability manifests for every backend in the
§6 lists, and a ``BackendCatalog`` with honesty validation (manifest-only
entries can never be instantiated as live stores).

Transport protocols EOIP does not implement in-repo (Bolt/RESP for
Memgraph/FalkorDB, OrientDB HTTP) are exposed as capability manifests plus
protocol interfaces marked **External gate** — never faked.
"""

from eoip.adapters.catalog import BackendCatalog, CatalogError
from eoip.adapters.manifests import AdapterStatus, CapabilityManifest, CertificationTier, load_manifests

__all__ = [
    "AdapterStatus",
    "BackendCatalog",
    "CapabilityManifest",
    "CatalogError",
    "CertificationTier",
    "load_manifests",
]

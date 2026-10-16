"""Built-in sample package used by tests and demos (GAP-MKT-003 fixture)."""

from __future__ import annotations

from eoip.marketplace.manifest import CapabilityKind, PackageManifest
from eoip.marketplace.packager import build_package

SAMPLE_MANIFEST = PackageManifest(
    id="urn:eoip:marketplace:package:hr-ontology-pack",
    name="hr-ontology-pack",
    version="1.2.0",
    description="Sample HR ontology pack with mappings and a query template.",
    author="EOIP Demo",
    platforms=["any"],
    provides={
        CapabilityKind.ONTOLOGIES: ["urn:eoip:ontology:hr"],
        CapabilityKind.MAPPINGS: ["urn:eoip:mapping:hr-crm"],
        CapabilityKind.QUERY_TEMPLATES: ["hr.headcount_by_department"],
    },
    dependencies=[],
)

SAMPLE_PAYLOAD = {
    "ontologies/hr.ttl": b"@prefix eoip: <urn:eoip:ontology:hr#> .\n",
    "mappings/hr-crm.yaml": b"source: hr\nsink: crm\n",
    "query_templates/headcount.sql": b"SELECT department, count(*) FROM hr GROUP BY 1;\n",
}


def sample_package_bytes() -> bytes:
    """Build the sample .eoipkg archive (unsigned; tests sign explicitly)."""

    return build_package(SAMPLE_MANIFEST, SAMPLE_PAYLOAD)

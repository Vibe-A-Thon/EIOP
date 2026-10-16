import json
import pytest
from eoip.connectors.sbom import SBOMConnector


@pytest.mark.req("G2-SRC-SBOM-002")
def test_sbom_spdx_package_extraction(tmp_path):
    spdx_file = tmp_path / "sample.spdx.json"
    spdx_data = {
        "spdxVersion": "SPDX-2.3",
        "name": "payments-backend",
        "packages": [
            {
                "SPDXID": "SPDXRef-Package-fastapi",
                "name": "fastapi",
                "versionInfo": "0.110.0",
                "downloadLocation": "https://pypi.org/project/fastapi/",
                "licenseConcluded": "MIT",
                "supplier": "Organization: Tiangolo",
            }
        ]
    }
    spdx_file.write_text(json.dumps(spdx_data), encoding="utf-8")

    connector = SBOMConnector(source_id="sbom-scanner")
    events = connector.extract_spdx(spdx_file)
    assert len(events) == 1
    pkg_event = events[0]
    assert pkg_event.metadata["record_kind"] == "spdx_package"
    assert "SPDXRef-Package-fastapi" in pkg_event.source_record_id
    assert pkg_event.payload["package_name"] == "fastapi"
    assert pkg_event.payload["license_concluded"] == "MIT"
    assert pkg_event.payload["document_name"] == "payments-backend"


@pytest.mark.req("G2-SRC-SBOM-003")
def test_sbom_cyclonedx_component_extraction(tmp_path):
    cdx_file = tmp_path / "sample.cdx.json"
    cdx_data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
        "components": [
            {
                "type": "library",
                "name": "pydantic",
                "version": "2.6.4",
                "purl": "pkg:pypi/pydantic@2.6.4",
                "bom-ref": "pkg:pypi/pydantic@2.6.4",
                "group": "pydantic",
            }
        ]
    }
    cdx_file.write_text(json.dumps(cdx_data), encoding="utf-8")

    connector = SBOMConnector(source_id="sbom-scanner")
    events = connector.extract_cyclonedx(cdx_file)
    assert len(events) == 1
    comp_event = events[0]
    assert comp_event.metadata["record_kind"] == "cyclonedx_component"
    assert "pydantic" in comp_event.source_record_id
    assert comp_event.payload["component_name"] == "pydantic"
    assert comp_event.payload["purl"] == "pkg:pypi/pydantic@2.6.4"


@pytest.mark.req("G2-SRC-SBOM-004")
def test_sbom_vulnerability_extraction_and_health(tmp_path):
    cdx_file = tmp_path / "sample_vuln.cdx.json"
    cdx_data = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": "urn:uuid:7b92f9-cdx-1",
        "components": [
            {"type": "library", "name": "aiohttp", "version": "3.8.0", "bom-ref": "aiohttp-3.8.0"}
        ],
        "vulnerabilities": [
            {
                "id": "CVE-2023-47627",
                "description": "HTTP request smuggling in aiohttp",
                "ratings": [{"severity": "high", "score": 7.5}],
                "affects": [{"ref": "aiohttp-3.8.0"}],
            }
        ]
    }
    cdx_file.write_text(json.dumps(cdx_data), encoding="utf-8")

    connector = SBOMConnector(source_id="sbom-vuln-audit")
    events = connector.extract_cyclonedx(cdx_file)
    assert len(events) == 2  # 1 component + 1 vulnerability
    vuln_event = next(e for e in events if e.metadata["record_kind"] == "cyclonedx_vulnerability")
    assert vuln_event.payload["vulnerability_id"] == "CVE-2023-47627"
    assert vuln_event.payload["ratings"][0]["severity"] == "high"

    health = connector.health()
    assert health.status == "HEALTHY"
    assert connector.checkpoint() is None

    discovery = connector.discover()
    format_ids = [r.resource_id for r in discovery.resources]
    assert "spdx" in format_ids
    assert "cyclonedx" in format_ids

"""Unit tests for extractors (inventory, provenance, boundary, api surface, db) and workflows."""

import io
import sqlite3
import tempfile
import zipfile
from pathlib import Path
import pytest

pytestmark = pytest.mark.reva_depth("unit")

from reva.extract.apisurface.miner import parse_combined_access_log, parse_har_entries
from reva.extract.artifacts.inventory import detect_format, inventory_archive
from reva.extract.boundaries.extractor import (
    extract_python_boundaries,
    match_client_server_endpoints,
)
from reva.extract.dbschema.introspect import introspect_sqlite
from reva.extract.provenance.extractor import (
    export_cyclonedx_sbom,
    export_spdx_sbom,
    extract_jvm_provenance,
    extract_npm_provenance,
    extract_python_provenance,
)
from reva.workflows.diff import compute_version_diff
from reva.workflows.drift import verify_system_drift


def test_archive_inventory_zip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("test.txt", b"hello world")
        zf.writestr("dir/inner.txt", b"inner content")

    zip_bytes = buf.getvalue()
    inv = inventory_archive(zip_bytes, filename="test.zip")
    assert inv.container_format == "zip"
    assert inv.total_members == 2
    assert inv.total_uncompressed_bytes == len(b"hello world") + len(b"inner content")


def test_provenance_and_sbom():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("META-INF/git.properties", "git.commit.id=c0ffee1234\ngit.branch=main\n")
        zf.writestr("META-INF/maven/com.example/demo/pom.properties", "groupId=com.example\nartifactId=demo\nversion=1.0.0\n")

    zf = zipfile.ZipFile(buf)
    prov = extract_jvm_provenance(zf)
    assert prov.commit_sha == "c0ffee1234"
    assert len(prov.components) == 1
    assert prov.components[0].purl == "pkg:maven/com.example/demo@1.0.0"

    # CycloneDX & SPDX export
    cdx = export_cyclonedx_sbom(prov)
    assert cdx["bomFormat"] == "CycloneDX"
    assert len(cdx["components"]) == 1

    spdx = export_spdx_sbom(prov)
    assert spdx["spdxVersion"] == "SPDX-2.3"
    assert len(spdx["packages"]) == 1


def test_boundary_extraction_and_matching():
    sample_code = """
from fastapi import FastAPI
app = FastAPI()

@app.get("/api/v1/users")
def list_users():
    return []

@app.post("/api/v1/users")
def create_user():
    import requests
    requests.post("http://billing-svc/charges")
    return {"status": "created"}
"""
    boundaries, resources = extract_python_boundaries(sample_code, "user-service", "main.py")
    assert len(boundaries) >= 3  # 2 routes + 1 http call
    routes = [b for b in boundaries if b.kind == "http_route"]
    calls = [b for b in boundaries if b.kind == "http_call"]
    assert len(routes) == 2
    assert len(calls) == 1

    # Endpoint matching
    matches = match_client_server_endpoints(calls, routes)
    # Different endpoints, no match expected
    assert len(matches) == 0


def test_api_surface_log_mining():
    log_line = '192.168.1.1 - - [18/Oct/2026:12:00:00 +0000] "GET /api/v1/health HTTP/1.1" 200 128 "-" "curl"'
    calls = parse_combined_access_log(log_line)
    assert len(calls) == 1
    assert calls[0].method == "GET"
    assert calls[0].path == "/api/v1/health"
    assert calls[0].status_code == 200


def test_db_schema_introspection():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        db_path = tf.name
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)")
    conn.commit()
    conn.close()

    schema = introspect_sqlite(db_path)
    assert len(schema.tables) == 1
    assert schema.tables[0].name == "users"
    col_names = [c.name for c in schema.tables[0].columns]
    assert "id" in col_names and "email" in col_names


def test_diff_and_drift_workflows():
    # Diff
    v1 = {"e1": {"label": "Service", "properties": {"version": "1.0"}}}
    v2 = {"e1": {"label": "Service", "properties": {"version": "2.0"}}, "e2": {"label": "Route", "properties": {}}}
    diff = compute_version_diff("t1", "c1", "c2", v1, v2)
    assert diff.modified_count == 1
    assert diff.added_count == 1
    assert diff.diff_id.startswith("dif1_")

    # Drift
    drift = verify_system_drift(
        tenant_id="t1",
        scope="service:billing",
        static_routes={"/charges", "/refunds"},
        runtime_observed_calls={"/charges", "/undeclared_api"},
    )
    assert drift.has_drift is True
    types = [a.anomaly_type for a in drift.anomalies]
    assert "undeclared_runtime_call" in types
    assert "dead_code_route" in types

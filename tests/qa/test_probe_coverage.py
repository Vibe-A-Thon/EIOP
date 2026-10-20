from qa.probe_coverage import analyze, probe_operations


def test_probe_inventory_distinguishes_covered_and_negative_routes():
    surface = {"operations": [
        {"method": "GET", "path": "/health/ready"},
        {"method": "POST", "path": "/api/v1/sources"},
        {"method": "PUT", "path": "/unprobed"},
    ]}
    report = analyze(surface, {("GET", "/health/ready"), ("POST", "/api/v1/sources"), ("GET", "/missing")})
    assert report["openapi_operations"] == 3
    assert report["qa_probed_operations"] == 2
    assert report["unprobed_operations"] == 1
    assert report["negative_or_undocumented_probes"] == [{"method": "GET", "path": "/missing"}]


def test_postman_probes_include_guarded_source_crud():
    operations = probe_operations()
    assert ("POST", "/api/v1/sources") in operations
    assert ("DELETE", "/api/v1/sources/{source_id}") in operations
    assert ("GET", "/health/ready") in operations

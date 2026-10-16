"""Unit tests for the schema profiler, key detection and explicit
relationship discovery (SR-ING-010, SR-ING-012, SR-ING-013, SR-ING-016)."""

import pytest
from eoip.ingest.profile import (
    CARDINALITY_CAP,
    DatasetProfile,
    SchemaProfiler,
    detect_key_candidates,
    diff_profiles,
    discover_relationships,
    edge_class_for_method,
    profile_records,
    tag_edge,
)

RECORDS = [
    {"id": "INC-1", "email": "a@example.com", "uuid": "12345678-1234-5678-1234-567812345678",
     "url": "https://example.com/x", "ip": "10.0.0.1", "ts": "2026-01-01T10:00:00Z",
     "currency": "EUR", "sha": "a" * 40, "ticket": "ABC-123",
     "path": "src/main.py", "status": "open", "amount": 12.5,
     "nested": {"a": 1, "b": {"c": "x"}}, "tags": ["x", "y"],
     "parent_id": None},
    {"id": "INC-2", "email": "b@example.com", "uuid": "22345678-1234-5678-1234-567812345678",
     "url": "https://example.com/y", "ip": "10.0.0.2", "ts": "2026-01-02T10:00:00Z",
     "currency": "USD", "sha": "b" * 40, "ticket": "ABC-124",
     "path": "src/other.py", "status": "closed", "amount": 7.0,
     "nested": {"a": 2, "b": {"c": "y"}}, "tags": ["y"],
     "parent_id": None},
    {"id": "INC-3", "email": "c@example.com", "uuid": "32345678-1234-5678-1234-567812345678",
     "url": "https://example.com/z", "ip": "10.0.0.3", "ts": "2026-01-03T10:00:00Z",
     "currency": "EUR", "sha": "c" * 40, "ticket": "DEF-200",
     "path": "docs/readme.md", "status": "open", "amount": None,
     "nested": {"a": 3, "b": {"c": "z"}}, "tags": [],
     "parent_id": None},
]


# --------------------------------------------------------------------------
# SR-ING-010: profiling

def test_profile_reports_types_nullability_cardinality():
    report = profile_records(RECORDS, dataset="incidents")
    assert report.record_count == 3
    fields = {f.path: f for f in report.fields}
    idf = fields["id"]
    assert idf.kind == "scalar"
    assert idf.observed_types == ["str"]
    assert idf.unique_ratio == 1.0
    assert idf.cardinality == 3
    amount = fields["amount"]
    assert amount.null_count == 1
    assert set(amount.observed_types) == {"float", "null"} or \
        set(amount.observed_types) == {"float"}
    assert amount.observed_types == ["float"]


def test_enum_candidate_detection():
    report = profile_records(RECORDS, dataset="incidents")
    fields = {f.path: f for f in report.fields}
    status = fields["status"]
    assert status.enum_candidate
    values = {ev.value for ev in status.enum_values}
    assert values == {"open", "closed"}
    counts = {ev.value: ev.count for ev in status.enum_values}
    assert counts == {"open": 2, "closed": 1}


def test_format_detection():
    report = profile_records(RECORDS, dataset="incidents")
    fields = {f.path: f for f in report.fields}
    assert "email" in fields["email"].formats
    assert "uuid" in fields["uuid"].formats
    assert "url" in fields["url"].formats
    assert "ip" in fields["ip"].formats
    assert "iso_datetime" in fields["ts"].formats
    assert "currency" in fields["currency"].formats
    assert "git_sha" in fields["sha"].formats
    assert "ticket_key" in fields["ticket"].formats
    assert "file_path" in fields["path"].formats


def test_nesting_shape_and_arrays():
    report = profile_records(RECORDS, dataset="incidents")
    fields = {f.path: f for f in report.fields}
    nested = fields["nested"]
    assert nested.kind == "object"
    assert nested.object_fields == ["a", "b"]
    assert nested.max_nesting_depth == 2  # nested -> b -> c
    tags = fields["tags"]
    assert tags.kind == "array"
    assert "str" in tags.array_item_types
    inner = fields["tags[]"]
    assert inner.kind == "scalar"
    assert inner.cardinality == 2


def test_streaming_updates_match_batch_profile():
    profiler = SchemaProfiler(dataset="incidents")
    for rec in RECORDS:
        profiler.update(rec)
    streamed = profiler.report()
    batched = profile_records(RECORDS, dataset="incidents")
    assert streamed == batched


def test_profile_is_deterministic_regardless_of_record_order():
    a = profile_records(list(reversed(RECORDS)), dataset="incidents")
    b = profile_records(RECORDS, dataset="incidents")
    assert a == b


def test_cardinality_cap_reports_lower_bound():
    records = [{"v": f"value-{i}"} for i in range(CARDINALITY_CAP + 5)]
    report = profile_records(records, dataset="big")
    field = {f.path: f for f in report.fields}["v"]
    assert field.cardinality_capped
    assert field.cardinality == CARDINALITY_CAP
    assert field.unique_ratio == 0.0


def test_drift_diff_detects_changes():
    before = profile_records(RECORDS, dataset="incidents")
    changed = [dict(r, status=r["status"], priority="high") for r in RECORDS]
    changed[0] = dict(changed[0], status="pending", id="NEW-1")
    # drop "sha" from every record so the field disappears entirely
    changed = [{k: v for k, v in r.items() if k != "sha"} for r in changed]
    after = profile_records(changed, dataset="incidents")
    drift = diff_profiles(before, after)
    changes = {(c.path, c.change) for c in drift.changes}
    assert ("priority", "added") in changes
    assert ("sha", "removed") in changes
    assert ("status", "type_changed") not in changes
    assert any(c.path == "status" and c.change == "enum_value_added"
               and c.detail == "pending" for c in drift.changes)


def test_drift_empty_for_identical_payloads():
    report = profile_records(RECORDS, dataset="incidents")
    assert diff_profiles(report, report).changes == []


# --------------------------------------------------------------------------
# SR-ING-012: key detection

def test_single_field_key_candidates():
    report = profile_records(RECORDS, dataset="incidents")
    keys = detect_key_candidates(report, records=RECORDS)
    single_fields = {k.fields[0] for k in keys if not k.composite}
    assert "id" in single_fields
    assert "uuid" in single_fields
    id_key = next(k for k in keys if k.fields == ["id"])
    assert id_key.name_hint
    assert id_key.unique_ratio == 1.0
    assert id_key.stability == 1.0


def test_enum_field_is_not_a_key_candidate():
    report = profile_records(RECORDS, dataset="incidents")
    keys = detect_key_candidates(report, records=RECORDS)
    assert all(k.fields != ["status"] for k in keys)


def test_composite_key_candidate():
    records = [
        {"first": "a", "last": "x", "v": 1},
        {"first": "a", "last": "y", "v": 2},
        {"first": "b", "last": "x", "v": 3},
    ]
    report = profile_records(records, dataset="people")
    keys = detect_key_candidates(report, records=records)
    composite = [k for k in keys if k.composite]
    assert any(k.fields == ["first", "last"] for k in composite)


def test_stability_scoring_against_baseline():
    baseline_records = [dict(r, id=f"OLD-{i}") for i, r in enumerate(RECORDS)]
    baseline = profile_records(baseline_records, dataset="incidents")
    report = profile_records(RECORDS, dataset="incidents")
    keys = detect_key_candidates(
        report, records=RECORDS,
        baseline=baseline, baseline_records=baseline_records,
    )
    id_key = next(k for k in keys if k.fields == ["id"])
    assert id_key.stability == 0.0  # all ids changed
    sha_key = next(k for k in keys if k.fields == ["sha"])
    assert sha_key.stability == 1.0  # unchanged between runs


# --------------------------------------------------------------------------
# SR-ING-013: explicit relationship discovery

def _orders_and_customers():
    customers = [
        {"customer_id": "C-1", "name": "Acme"},
        {"customer_id": "C-2", "name": "Globex"},
    ]
    orders = [
        {"order_id": "O-1", "customer_id": "C-1",
         "parent_id": "O-1",  # self hierarchy seed replaced below
         "related": ["C-1", "C-2"]},
        {"order_id": "O-2", "customer_id": "C-2",
         "related": ["C-2"]},
    ]
    return customers, orders


def test_foreign_key_like_discovery():
    customers, orders = _orders_and_customers()
    datasets = [
        DatasetProfile(name="customers",
                       report=profile_records(customers, dataset="customers"),
                       records=customers, primary_key="customer_id"),
        DatasetProfile(name="orders",
                       report=profile_records(orders, dataset="orders"),
                       records=orders, primary_key="order_id"),
    ]
    rels = discover_relationships(datasets)
    fk = [r for r in rels if r.method == "foreign_key_like"
          and r.from_field == "customer_id"]
    assert fk, rels
    assert fk[0].from_dataset == "orders"
    assert fk[0].to_dataset == "customers"
    assert fk[0].to_field == "customer_id"
    assert fk[0].evidence  # sample values present


def test_array_of_ids_discovery():
    customers, orders = _orders_and_customers()
    datasets = [
        DatasetProfile(name="customers",
                       report=profile_records(customers, dataset="customers"),
                       records=customers, primary_key="customer_id"),
        DatasetProfile(name="orders",
                       report=profile_records(orders, dataset="orders"),
                       records=orders, primary_key="order_id"),
    ]
    rels = discover_relationships(datasets)
    arr = [r for r in rels if r.method == "array_of_ids"]
    assert arr, rels
    assert arr[0].from_field == "related"
    assert arr[0].to_dataset == "customers"


def test_parent_pointer_discovery():
    nodes = [
        {"node_id": "N-1", "parent_id": None},
        {"node_id": "N-2", "parent_id": "N-1"},
        {"node_id": "N-3", "parent_id": "N-2"},
    ]
    datasets = [
        DatasetProfile(name="nodes",
                       report=profile_records(nodes, dataset="nodes"),
                       records=nodes, primary_key="node_id"),
    ]
    rels = discover_relationships(datasets)
    parents = [r for r in rels if r.method == "parent_pointer"]
    assert parents, rels
    assert parents[0].from_dataset == parents[0].to_dataset == "nodes"
    assert parents[0].to_field == "node_id"


def test_type_id_pair_discovery():
    events = [
        {"event_id": "E-1", "target_type": "customers", "target_id": "C-1"},
        {"event_id": "E-2", "target_type": "customers", "target_id": "C-2"},
    ]
    customers = [
        {"customer_id": "C-1", "name": "Acme"},
        {"customer_id": "C-2", "name": "Globex"},
    ]
    datasets = [
        DatasetProfile(name="events",
                       report=profile_records(events, dataset="events"),
                       records=events, primary_key="event_id"),
        DatasetProfile(name="customers",
                       report=profile_records(customers, dataset="customers"),
                       records=customers, primary_key="customer_id"),
    ]
    rels = discover_relationships(datasets)
    pairs = [r for r in rels if r.method == "type_id_pair"]
    assert pairs, rels
    assert pairs[0].to_dataset == "customers"


def test_relationship_discovery_is_deterministic():
    customers, orders = _orders_and_customers()
    def run():
        return discover_relationships([
            DatasetProfile(name="customers",
                           report=profile_records(customers, dataset="customers"),
                           records=customers, primary_key="customer_id"),
            DatasetProfile(name="orders",
                           report=profile_records(orders, dataset="orders"),
                           records=orders, primary_key="order_id"),
        ])
    assert run() == run()


# --------------------------------------------------------------------------
# SR-ING-016: edge class tagging

def test_explicit_methods_are_asserted():
    for method in ("foreign_key_like", "parent_pointer", "url_reference",
                   "array_of_ids", "type_id_pair"):
        assert tag_edge(method) == "ASSERTED"
        assert edge_class_for_method(method).edge_class == "ASSERTED"


def test_curated_overrides_and_unknown_degrades():
    assert tag_edge("foreign_key_like", curated=True) == "CURATED"
    assert tag_edge("some_future_ml_method") == "INFERRED"


# --------------------------------------------------------------------------
# Router surface

def test_build_router_exposes_expected_routes():
    pytest.importorskip("fastapi")
    from eoip.ingest.profile import build_router
    router = build_router()
    routes = sorted(r.path for r in router.routes)
    assert routes == [
        "/api/v1/ingest/profile",
        "/api/v1/ingest/profile/drift",
        "/api/v1/ingest/profile/keys",
        "/api/v1/ingest/profile/relationships",
    ]

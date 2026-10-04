"""Unit tests for the Knowledge Product catalog (GAP-KP-001..005)."""

from __future__ import annotations

import json

import pytest

from eoip.catalog.products import (
    ALLOWED_TRANSITIONS,
    KnowledgeProduct,
    KnowledgeProductCatalog,
    ProductNotFoundError,
    ProductState,
    ProductValidationError,
    SLO,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.fixture()
def catalog() -> KnowledgeProductCatalog:
    return KnowledgeProductCatalog(MemoryGraphStore())


def _product(name: str = "Dependency Health Index", **overrides) -> KnowledgeProduct:
    base = dict(
        name=name,
        owner="team-platform",
        domain="engineering",
        description="Aggregated dependency freshness per service",
        source_graphs=["urn:eoip:graph:code", "urn:eoip:graph:cicd"],
        ontology_version="0.4.0",
        quality_slo=SLO(metric="completeness", threshold=0.99, unit="ratio"),
        freshness_slo=SLO(metric="age", threshold=24, unit="hours"),
        access_policy="internal",
        apis=["/v1/dependency-health"],
        dashboards=["https://grafana.example.com/d/dep-health"],
        consumers=["urn:eoip:team:checkout", "urn:eoip:team:pricing"],
    )
    base.update(overrides)
    return KnowledgeProduct(**base)


# -- GAP-KP-001: model + CRUD ------------------------------------------------

def test_create_assigns_canonical_id(catalog):
    product = catalog.create(_product())
    assert product.product_id == "urn:eoip:catalog:knowledge-product:dependency-health-index"
    fetched = catalog.get(product.product_id)
    assert fetched.name == "Dependency Health Index"
    assert fetched.owner == "team-platform"
    assert fetched.source_graphs == ["urn:eoip:graph:code", "urn:eoip:graph:cicd"]
    assert fetched.quality_slo.threshold == 0.99
    assert fetched.freshness_slo.unit == "hours"
    assert fetched.access_policy == "internal"
    assert fetched.apis == ["/v1/dependency-health"]
    assert fetched.dashboards == ["https://grafana.example.com/d/dep-health"]
    assert fetched.consumers == ["urn:eoip:team:checkout", "urn:eoip:team:pricing"]
    assert fetched.state == ProductState.DRAFT
    assert fetched.created_at and fetched.updated_at


def test_create_duplicate_rejected(catalog):
    catalog.create(_product())
    with pytest.raises(ProductValidationError):
        catalog.create(_product())


def test_get_missing_raises(catalog):
    with pytest.raises(ProductNotFoundError):
        catalog.get("urn:eoip:catalog:knowledge-product:nope")


def test_update_preserves_state_and_created_at(catalog):
    created = catalog.create(_product())
    updated = catalog.update(
        _product(description="new description", product_id=created.product_id)
    )
    assert updated.description == "new description"
    assert updated.state == ProductState.DRAFT
    assert updated.created_at == created.created_at


def test_update_missing_raises(catalog):
    with pytest.raises(ProductNotFoundError):
        catalog.update(_product(product_id="urn:eoip:catalog:knowledge-product:ghost"))


def test_delete_tombstones(catalog):
    product = catalog.create(_product())
    assert catalog.delete(product.product_id) is True
    with pytest.raises(ProductNotFoundError):
        catalog.get(product.product_id)
    assert catalog.delete(product.product_id) is False


# -- GAP-KP-002: lifecycle states ---------------------------------------------

def test_happy_path_lifecycle(catalog):
    product = catalog.create(_product())
    pid = product.product_id
    for state in (
        ProductState.EXPERIMENTAL,
        ProductState.TRUSTED,
        ProductState.CERTIFIED,
        ProductState.DEPRECATED,
    ):
        product = catalog.transition(pid, state)
        assert product.state == state


def test_illegal_transition_rejected(catalog):
    product = catalog.create(_product())
    with pytest.raises(ProductValidationError):
        catalog.transition(product.product_id, ProductState.CERTIFIED)


def test_deprecated_is_terminal(catalog):
    product = catalog.create(_product())
    catalog.transition(product.product_id, ProductState.DEPRECATED)
    with pytest.raises(ProductValidationError):
        catalog.transition(product.product_id, ProductState.DRAFT)


def test_allowed_transitions_listing(catalog):
    product = catalog.create(_product())
    assert catalog.allowed_transitions(product.product_id) == ["Deprecated", "Experimental"]
    assert set(ALLOWED_TRANSITIONS[ProductState.CERTIFIED]) == {ProductState.DEPRECATED}


# -- GAP-KP-003: list with filters ---------------------------------------------

def _seed(catalog) -> None:
    catalog.create(_product("Alpha Index", owner="team-a", domain="engineering"))
    catalog.create(_product("Beta Feed", owner="team-b", domain="finance",
                            access_policy="public",
                            source_graphs=["urn:eoip:graph:work"],
                            consumers=["urn:eoip:team:treasury"]))


def test_list_all_sorted(catalog):
    _seed(catalog)
    products = catalog.list()
    assert [p.name for p in products] == ["Alpha Index", "Beta Feed"]


def test_list_filter_by_owner_and_domain(catalog):
    _seed(catalog)
    assert [p.name for p in catalog.list(owner="team-b")] == ["Beta Feed"]
    assert [p.name for p in catalog.list(domain="engineering")] == ["Alpha Index"]
    assert catalog.list(owner="team-x") == []


def test_list_filter_by_state_and_access_policy(catalog):
    _seed(catalog)
    assert len(catalog.list(state=ProductState.DRAFT)) == 2
    assert [p.name for p in catalog.list(access_policy="public")] == ["Beta Feed"]
    beta = catalog.list(owner="team-b")[0]
    catalog.transition(beta.product_id, ProductState.EXPERIMENTAL)
    assert [p.name for p in catalog.list(state="Experimental")] == ["Beta Feed"]


def test_list_filter_by_consumer(catalog):
    _seed(catalog)
    assert [p.name for p in catalog.list(consumer="urn:eoip:team:treasury")] == ["Beta Feed"]


# -- GAP-KP-004: export / import -----------------------------------------------

def test_export_import_roundtrip(catalog):
    original = catalog.create(_product())
    payload = catalog.export_json(original.product_id)

    other = KnowledgeProductCatalog(MemoryGraphStore())
    imported = other.import_json(payload)
    assert imported.model_dump() == catalog.get(original.product_id).model_dump()


def test_import_updates_existing_in_place(catalog):
    original = catalog.create(_product())
    data = json.loads(catalog.export_json(original.product_id))
    data["description"] = "changed externally"
    imported = catalog.import_json(json.dumps(data))
    assert imported.product_id == original.product_id
    assert imported.description == "changed externally"
    assert imported.created_at == original.created_at
    assert len(catalog.list()) == 1


def test_import_accepts_dict(catalog):
    imported = catalog.import_json(_product("Gamma Pack").model_dump())
    assert imported.name == "Gamma Pack"
    assert catalog.get(imported.product_id).state == ProductState.DRAFT


def test_export_all(catalog):
    _seed(catalog)
    exported = json.loads(catalog.export_all_json())
    assert len(exported) == 2


# -- GAP-KP-005: lineage ---------------------------------------------------------

def test_lineage_shape(catalog):
    product = catalog.create(_product())
    lineage = catalog.lineage(product.product_id)
    assert lineage["product_id"] == product.product_id
    assert [s["source_graph"] for s in lineage["source_graphs"]] == [
        "urn:eoip:graph:code",
        "urn:eoip:graph:cicd",
    ]
    assert all(s["direction"] == "upstream" for s in lineage["source_graphs"])
    assert [c["consumer"] for c in lineage["consumers"]] == [
        "urn:eoip:team:checkout",
        "urn:eoip:team:pricing",
    ]
    assert all(c["direction"] == "downstream" for c in lineage["consumers"])


def test_reverse_lineage_by_source_graph(catalog):
    _seed(catalog)
    products = catalog.products_for_source_graph("urn:eoip:graph:code")
    assert [p.name for p in products] == ["Alpha Index"]


def test_reverse_lineage_by_consumer(catalog):
    _seed(catalog)
    products = catalog.products_for_consumer("urn:eoip:team:checkout")
    assert [p.name for p in products] == ["Alpha Index"]

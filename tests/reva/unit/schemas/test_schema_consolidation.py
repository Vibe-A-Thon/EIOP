"""
Unit Tests for Schema Induction, SHACL Synthesis, and Multi-Plane Graph Projection (NS-REQ-*).
"""

import pytest

from packages.eoip.neural.schemas.models import NeuralSchema
from packages.eoip.neural.schemas.consolidation import SchemaInductionEngine
from packages.eoip.neural.schemas.planes_integration import GraphPlanesProjector


def test_schema_induction_and_shacl():
    engine = SchemaInductionEngine(min_support_ratio=0.70)

    # Observation stream
    instances = [
        {"endpoint": "/api/v1/auth", "latency": 15.2, "status": 200, "user_agent": "curl"},
        {"endpoint": "/api/v1/user", "latency": 22.0, "status": 200, "user_agent": "browser"},
        {"endpoint": "/api/v1/data", "latency": 45.1, "status": 404}, # missing user_agent
    ]

    schema = engine.induce_schema_from_instances(
        schema_name="APIRequestLog",
        domain="observability",
        instances=instances,
    )

    assert schema.schema_id.startswith("sch1_")
    assert "endpoint" in schema.slots
    assert "status" in schema.slots
    assert schema.slots["endpoint"].required  # present in 100% of instances
    assert not schema.slots["user_agent"].required  # present in only 66% (< 70% threshold)

    # Synthesize SHACL shape
    shacl = engine.synthesize_shacl_shape(schema)
    turtle = shacl.to_shacl_turtle()
    assert ":APIRequestLogShape a sh:NodeShape" in turtle
    assert "sh:path :endpoint" in turtle
    assert "sh:minCount 1" in turtle


def test_graph_planes_projector():
    projector = GraphPlanesProjector(tenant_id="tenant_omega")
    schema = NeuralSchema.create(
        name="MicroServiceConfig",
        domain="infrastructure",
        slots={},
    )

    # Project schema to Plane GL2
    gl2_vertex = projector.project_schema_to_gl2(schema)
    assert gl2_vertex.plane == "GL2"
    assert gl2_vertex.id == schema.schema_id

    # Project instance across planes
    inst_data = {"service_name": "payment-gw", "port": 8443}
    projection = projector.project_instance(
        schema=schema,
        instance_data=inst_data,
        logical_key="payment_gw_prod",
        blob_hash="a1b2c3d4" * 16,
        governing_decision_id="dec:adr/0001-payment-architecture.md",
    )

    ent_id = projection["entity_id"]
    assert ent_id.startswith("ent1_")

    vertices = projection["vertices"]
    planes = [v["plane"] for v in vertices]
    assert "GL1" in planes  # Entity
    assert "GL0" in planes  # Raw blob

    edges = projection["edges"]
    relations = [e["relation"] for e in edges]
    assert "INSTANTIATES_SCHEMA" in relations
    assert "DERIVED_FROM_BLOB" in relations
    assert "GOVERNED_BY_DECISION" in relations

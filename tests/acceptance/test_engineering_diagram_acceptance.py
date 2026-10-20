"""Acceptance tests for WP-015: Engineering Diagram Semantics (CRA-015.1-015.8, CRA-015.A)."""

import pytest
import rdflib
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef

from eoip.fileparse.diagram_parser import (
    DiagramAST,
    DiagramConnector,
    DiagramOntologyMapper,
    DiagramRenderer,
    DiagramShape,
    DiagramType,
    DrawIOParser,
    MermaidParser,
    PlantUMLParser,
    VisualDiagramExtractionCandidate,
    compile_to_rdf,
    compute_source_vs_graph_diff,
    generate_visual_candidates,
    sanitize_diagram_label,
)

EOIP = Namespace("https://enterprise-ontology.org/schema/eoip#")
EX = Namespace("http://example.org/diagram/")


# ---------------------------------------------------------------------------
# CRA-015.1: Notation-specific structured diagrams, source and parser coverage
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_1_notation_specific_drawio_chowlk_mermaid_plantuml():
    # 1. Draw.io / Chowlk XML
    drawio_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <mxfile>
      <diagram name="Architecture">
        <mxGraphModel>
          <root>
            <mxCell id="0"/>
            <mxCell id="1" parent="0"/>
            <mxCell id="c1" value="PaymentService" style="shape=rectangle;rounded=1;" vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="140" height="60" as="geometry"/>
            </mxCell>
            <mxCell id="c2" value="LedgerDB" style="shape=cylinder;whiteSpace=wrap;" vertex="1" parent="1">
              <mxGeometry x="350" y="100" width="120" height="80" as="geometry"/>
            </mxCell>
            <mxCell id="e1" value="writes_to" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="c1" target="c2" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
          </root>
        </mxGraphModel>
      </diagram>
    </mxfile>
    """
    drawio_parser = DrawIOParser()
    ast_drawio = drawio_parser.parse(drawio_xml)
    assert ast_drawio.diagram_format == "drawio_xml"
    assert len(ast_drawio.shapes) == 2
    assert len(ast_drawio.connectors) == 1
    assert ast_drawio.coverage_stats["coverage_pct"] >= 90.0

    # 2. Mermaid diagram
    mermaid_src = """
    flowchart LR
        subgraph Payments ["Payment Processing"]
            OrderService["Order Service"] -->|calls| FraudService["Fraud Detection"]
        end
    """
    mermaid_parser = MermaidParser()
    ast_mermaid = mermaid_parser.parse(mermaid_src)
    assert ast_mermaid.diagram_format == "mermaid"
    assert len(ast_mermaid.shapes) >= 2
    assert any(s.parent_id == "Payments" for s in ast_mermaid.shapes)

    # 3. PlantUML diagram
    puml_src = """
    @startuml
    package "Core Engine" {
        component Dispatcher
        database CacheStore
    }
    Dispatcher --> CacheStore : reads_from
    @enduml
    """
    puml_parser = PlantUMLParser()
    ast_puml = puml_parser.parse(puml_src)
    assert ast_puml.diagram_format == "plantuml"
    assert any(s.id == "Dispatcher" for s in ast_puml.shapes)
    assert any(s.id == "CacheStore" and s.shape_type == "database" for s in ast_puml.shapes)


# ---------------------------------------------------------------------------
# CRA-015.2: Components, containment, directions, cardinalities, no coercion
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_2_components_ports_containment_directions_no_silent_coercion():
    puml_src = """
    @startuml
    package "InventoryDomain" {
        queue MessageBus
        component InventoryWorker
    }
    database StockDB
    "1" MessageBus --> "0..*" InventoryWorker : consumes_from
    InventoryWorker -- StockDB : syncs
    @enduml
    """
    ast = PlantUMLParser().parse(puml_src)
    mapper = DiagramOntologyMapper()
    assertions = mapper.map_ast(ast)

    # Check containment
    bus = ast.get_shape("MessageBus")
    assert bus is not None
    assert bus.shape_type == "queue"
    assert bus.parent_id == "InventoryDomain"

    # Check cardinalities
    conn1 = next(c for c in ast.connectors if c.source_id == "MessageBus")
    assert conn1.cardinality_source == "1"
    assert conn1.cardinality_target == "0..*"
    assert conn1.direction == "directed"

    # Check undirected connection
    conn2 = next(c for c in ast.connectors if c.source_id == "InventoryWorker")
    assert conn2.direction == "undirected"

    # CRITICAL: Verify NO silent coercion to Service or CALLS
    bus_assert = next(a for a in assertions if a.get("entity_id") == "MessageBus")
    assert "Service" not in bus_assert["target_class"]
    assert "MessageQueue" in bus_assert["target_class"]

    sync_assert = next(a for a in assertions if a.get("source_id") == "InventoryWorker")
    assert sync_assert["predicate"] != "https://enterprise-ontology.org/schema/eoip#calls"


# ---------------------------------------------------------------------------
# CRA-015.3: Visual extraction candidate generation with uncertainty
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_3_visual_extraction_candidate_generation_with_bounding_regions():
    raw_detections = [
        {"confidence": 0.88, "bounding_box": (0.1, 0.2, 0.4, 0.5), "label": "AuthService", "shape": "rectangle"},
        {"confidence": 0.62, "bounding_box": (0.5, 0.6, 0.8, 0.9), "label": "UserCredentialsDB", "shape": "cylinder"},
    ]

    candidates = generate_visual_candidates(raw_detections)
    assert len(candidates) == 2

    c1 = candidates[0]
    assert c1.detected_label == "AuthService"
    assert c1.confidence == 0.88
    assert c1.uncertainty_score == 0.12
    assert c1.is_candidate is True
    assert c1.knowledge_state == "proposed"

    c2 = candidates[1]
    assert c2.inferred_shape == "cylinder"
    assert c2.uncertainty_score == 0.38
    assert c2.knowledge_state == "proposed"


# ---------------------------------------------------------------------------
# CRA-015.4: Source-versus-graph diff and loss ledger
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_4_source_versus_graph_diff_and_loss_ledger():
    mermaid_src = """
    flowchart TD
        A["Valid Service A"] -->|calls| B["Valid Service B"]
        A -->|unknown_proprietary_link| C["Valid Service C"]
        style A fill:#f9f,stroke:#333,stroke-width:4px
    """
    ast = MermaidParser().parse(mermaid_src)
    mapper = DiagramOntologyMapper()
    assertions = mapper.map_ast(ast)

    diff = compute_source_vs_graph_diff(ast, assertions)
    assert diff["source_shapes_count"] == 3
    assert diff["compiled_entities_count"] == 3
    assert diff["loss_ledger_count"] >= 1
    # Loss ledger must track unknown construct, blocking lossless claim
    assert diff["is_lossless"] is False
    assert diff["lossless_claim_allowed"] is False

    assert any(
        "unrecognized_connector" in entry["construct_type"] or "unknown_proprietary_link" in entry["raw_content"]
        for entry in diff["loss_ledger"]
    )


# ---------------------------------------------------------------------------
# CRA-015.5: Round-trip rendering and label sanitization
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_5_round_trip_rendering_and_label_sanitization():
    # Test sanitization against XSS and control sequences
    hostile_label = 'CustomerPortal <script>alert("xss")</script> & "Admin"'
    clean_label = sanitize_diagram_label(hostile_label)
    assert "<script>" not in clean_label
    assert "&lt;script&gt;" not in clean_label  # script tag fully stripped
    assert "&amp;" in clean_label
    assert "&quot;" in clean_label

    ast = DiagramAST(diagram_format="mermaid")
    ast.add_shape(DiagramShape(id="srv1", name=clean_label, shape_type="rectangle"))
    ast.add_shape(DiagramShape(id="db1", name="SecureDB", shape_type="cylinder"))
    ast.add_connector(DiagramConnector(id="c1", source_id="srv1", target_id="db1", label="reads_from"))

    # 1. Round-trip to Mermaid
    mermaid_rendered = DiagramRenderer.render_mermaid(ast)
    assert "flowchart LR" in mermaid_rendered
    assert 'srv1["CustomerPortal' in mermaid_rendered
    assert 'db1[("SecureDB")]' in mermaid_rendered
    assert "<script>" not in mermaid_rendered

    # 2. Round-trip to PlantUML
    puml_rendered = DiagramRenderer.render_plantuml(ast)
    assert "@startuml" in puml_rendered
    assert 'database "SecureDB" as db1' in puml_rendered
    assert "@enduml" in puml_rendered

    # 3. Round-trip to DrawIO XML
    drawio_rendered = DiagramRenderer.render_drawio_xml(ast)
    assert "<mxGraphModel>" in drawio_rendered
    assert 'value="SecureDB"' in drawio_rendered
    assert "<script>" not in drawio_rendered


# ---------------------------------------------------------------------------
# CRA-015.6: Structured formats (DrawIO XML, Chowlk, PlantUML, Mermaid AST)
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_6_structured_formats_shapes_connectors_ast():
    drawio_xml = """<mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="cls1" value="owl:Class Customer" style="chowlk:class" vertex="1" parent="1"/>
        <mxCell id="dt1" value="rdfs:Datatype xsd:string" style="chowlk:datatype" vertex="1" parent="1"/>
        <mxCell id="sub1" value="rdfs:subClassOf" style="endArrow=block;endFill=0;" edge="1" source="cls1" target="dt1" parent="1"/>
      </root>
    </mxGraphModel>"""
    ast = DrawIOParser().parse(drawio_xml)
    assert ast.diagram_type == DiagramType.CHOWLK_ONTOLOGY
    shape_types = [s.shape_type for s in ast.shapes]
    assert "chowlk_class" in shape_types
    assert "chowlk_datatype" in shape_types
    assert len(ast.connectors) == 1


# ---------------------------------------------------------------------------
# CRA-015.7: Configurable versioned shape and connector mapping table
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_7_configurable_versioned_ontology_mapping():
    custom_mapper = DiagramOntologyMapper(
        shape_mappings={"microservice": "http://example.org/ns#Microservice"},
        connector_mappings={"invokes_rpc": "http://example.org/ns#invokesRpc"},
        version="2.1.0",
    )

    ast = DiagramAST(diagram_format="custom")
    ast.add_shape(DiagramShape(id="api_gw", name="APIGateway", shape_type="microservice"))
    ast.add_shape(DiagramShape(id="order_svc", name="OrderService", shape_type="microservice"))
    ast.add_connector(DiagramConnector(id="rpc_1", source_id="api_gw", target_id="order_svc", label="invokes_rpc"))

    assertions = custom_mapper.map_ast(ast)
    assert len(assertions) == 3

    gw_assert = next(a for a in assertions if a.get("entity_id") == "api_gw")
    assert gw_assert["target_class"] == "http://example.org/ns#Microservice"
    assert gw_assert["knowledge_state"] == "proposed"
    assert gw_assert["mapping_version"] == "2.1.0"

    conn_assert = next(a for a in assertions if a.get("source_id") == "api_gw")
    assert conn_assert["predicate"] == "http://example.org/ns#invokesRpc"
    assert conn_assert["knowledge_state"] == "proposed"

    # Human review / approval converts proposed to asserted
    approved = DiagramOntologyMapper.approve_proposals(assertions, approver="lead_architect")
    assert all(a["knowledge_state"] == "asserted" for a in approved)
    assert all(a["approved_by"] == "lead_architect" for a in approved)


# ---------------------------------------------------------------------------
# CRA-015.8: Unrecognized connectors preserved as generic eoip:connectsTo (G10 fix)
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_8_unrecognized_connectors_preserved_as_generic_connectsTo():
    ast = DiagramAST(diagram_format="mermaid")
    ast.add_shape(DiagramShape(id="srv_x", name="ServiceX", shape_type="rectangle"))
    ast.add_shape(DiagramShape(id="legacy_box", name="LegacySystem", shape_type="custom_mainframe"))
    ast.add_connector(DiagramConnector(id="c_unknown", source_id="srv_x", target_id="legacy_box", label="obscure_wire_link"))

    mapper = DiagramOntologyMapper()
    assertions = mapper.map_ast(ast)

    # 1. Unrecognized shape is preserved as DiagramComponent
    legacy_assert = next(a for a in assertions if a.get("entity_id") == "legacy_box")
    assert legacy_assert["target_class"] == "https://enterprise-ontology.org/schema/eoip#DiagramComponent"
    assert legacy_assert["is_unrecognized"] is True

    # 2. Unrecognized connector is preserved as eoip:connectsTo (NEVER CALLS!)
    conn_assert = next(a for a in assertions if a.get("source_id") == "srv_x")
    assert conn_assert["predicate"] == "https://enterprise-ontology.org/schema/eoip#connectsTo"
    assert conn_assert["is_generic_fallback"] is True
    assert conn_assert["predicate"] != "https://enterprise-ontology.org/schema/eoip#calls"

    # 3. Loss ledger contains explicit entries
    assert len(ast.loss_ledger) == 2
    assert any(entry.construct_type == "unrecognized_shape" for entry in ast.loss_ledger)
    assert any(entry.construct_type == "unrecognized_connector" for entry in ast.loss_ledger)


# ---------------------------------------------------------------------------
# CRA-015.A: Acceptance Gate: Microservice diagram vs Gold Semantic Model
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-015")
def test_cra_015_a_microservice_diagram_gold_model_owl2_fidelity():
    """Compiles a microservice diagram into OWL 2 assertions and verifies 100% fidelity against gold model."""
    drawio_xml = """<mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="gw" value="APIGateway" style="shape=rectangle;" vertex="1" parent="1"/>
        <mxCell id="auth" value="AuthService" style="shape=rectangle;" vertex="1" parent="1"/>
        <mxCell id="users_db" value="UsersDB" style="shape=cylinder;" vertex="1" parent="1"/>
        <mxCell id="e1" value="calls" edge="1" source="gw" target="auth" parent="1"/>
        <mxCell id="e2" value="reads_from" edge="1" source="auth" target="users_db" parent="1"/>
        <mxCell id="e3_unsupported" value="proprietary_raw_socket" style="dashed=1;" edge="1" source="gw" target="users_db" parent="1"/>
      </root>
    </mxGraphModel>"""

    # 1. Parse diagram
    ast = DrawIOParser().parse(drawio_xml)
    assert len(ast.shapes) == 3
    assert len(ast.connectors) == 3

    # 2. Compile to RDF / OWL 2
    mapper = DiagramOntologyMapper()
    graph = compile_to_rdf(ast, mapper, base_iri="http://example.org/diagram/")

    # 3. Independently authored gold semantic model for the supported subset
    gold_graph = Graph()
    gold_graph.bind("ex", EX)
    gold_graph.bind("eoip", EOIP)
    gold_graph.bind("owl", OWL)

    gw_uri = URIRef("http://example.org/diagram/gw")
    auth_uri = URIRef("http://example.org/diagram/auth")
    db_uri = URIRef("http://example.org/diagram/users_db")

    gold_graph.add((gw_uri, RDF.type, EOIP.Service))
    gold_graph.add((auth_uri, RDF.type, EOIP.Service))
    gold_graph.add((db_uri, RDF.type, EOIP.Database))
    gold_graph.add((gw_uri, EOIP.calls, auth_uri))
    gold_graph.add((auth_uri, EOIP.readsFrom, db_uri))

    # 4. Verify 100% fidelity on the supported subset
    for s, p, o in gold_graph:
        assert (s, p, o) in graph, f"Missing expected gold triple in compiled diagram RDF: ({s}, {p}, {o})"

    # 5. Verify the unsupported link was preserved as generic eoip:connectsTo with loss ledger entry
    assert (gw_uri, EOIP.connectsTo, db_uri) in graph
    assert len(ast.loss_ledger) >= 1
    assert any("proprietary_raw_socket" in entry.raw_content for entry in ast.loss_ledger)

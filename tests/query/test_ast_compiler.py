"""Tests for Multi-Dialect QueryPlan AST Compiler (WP-KG3-03, GAP-04, INV-SELF-03, CAP-20, CRA-009.1)."""

import pytest
from eoip.query.ast_compiler import (
    ASTCompiler,
    FilterCondition,
    FilterOp,
    MatchPattern,
    OrderByClause,
    ProjectionField,
    QueryPlanAST,
)


def test_single_hop_pattern_transpilation():
    """Validates 1-hop traversal pattern transpilation across Cypher, Gremlin, and SPARQL."""
    pattern = MatchPattern(
        start_var="svc",
        start_label="Service",
        edge_label="DEPENDS_ON",
        direction="OUT",
        end_var="db",
        end_label="Database",
    )
    ast = QueryPlanAST(
        patterns=[pattern],
        filters=[FilterCondition(field="svc.tier", operator=FilterOp.EQ, value="TIER_1")],
        projections=[
            ProjectionField(expr="svc.name", alias="service_name"),
            ProjectionField(expr="db.name", alias="db_name"),
        ],
        order_by=[OrderByClause(field="svc.name", descending=False)],
        limit=50,
        offset=10,
    )

    # 1. Cypher validation
    cypher = ASTCompiler.compile_cypher(ast)
    assert "MATCH (svc:Service)-[:DEPENDS_ON]->(db:Database)" in cypher
    assert "WHERE svc.tier = 'TIER_1'" in cypher
    assert "RETURN svc.name AS service_name, db.name AS db_name" in cypher
    assert "ORDER BY svc.name ASC" in cypher
    assert "SKIP 10 LIMIT 50" in cypher

    # 2. Gremlin validation
    gremlin = ASTCompiler.compile_gremlin(ast)
    assert "g.V().hasLabel('Service').as('svc').out('DEPENDS_ON').hasLabel('Database').as('db')" in gremlin
    assert ".has('tier', P.eq('TIER_1'))" in gremlin
    assert ".order().by('svc.name', Order.asc)" in gremlin
    assert ".range(10, 60)" in gremlin

    # 3. SPARQL validation
    sparql = ASTCompiler.compile_sparql(ast)
    assert "?svc a :Service ." in sparql
    assert "?svc :DEPENDS_ON ?db ." in sparql
    assert "?db a :Database ." in sparql
    assert 'FILTER (?svc_tier = "TIER_1")' in sparql
    assert "LIMIT 50" in sparql
    assert "OFFSET 10" in sparql


def test_variable_length_path_transpilation():
    """Validates variable-length transitive paths (e.g. *1..3) without regex breaking."""
    pattern = MatchPattern(
        start_var="src",
        start_label="Microservice",
        edge_label="CALLS",
        direction="OUT",
        min_hops=1,
        max_hops=4,
        end_var="target",
        end_label="Microservice",
    )
    ast = QueryPlanAST(
        patterns=[pattern],
        filters=[FilterCondition(field="src.name", operator=FilterOp.STARTS_WITH, value="auth-")],
        projections=[ProjectionField(expr="target.name")],
        limit=100,
    )

    cypher = ASTCompiler.compile_cypher(ast)
    assert "MATCH (src:Microservice)-[:CALLS*1..4]->(target:Microservice)" in cypher
    assert "src.name STARTS WITH 'auth-'" in cypher

    gremlin = ASTCompiler.compile_gremlin(ast)
    assert ".repeat(out('CALLS')).times(4)" in gremlin

    sparql = ASTCompiler.compile_sparql(ast)
    assert ":CALLS{ 1,4 }" in sparql


def test_complex_filtering_and_aggregation():
    """Validates IN, CONTAINS, and aggregation projections."""
    ast = QueryPlanAST(
        patterns=[MatchPattern(start_var="n", start_label="Incident")],
        filters=[
            FilterCondition(field="n.severity", operator=FilterOp.IN, value=["SEV-1", "SEV-2"]),
            FilterCondition(field="n.summary", operator=FilterOp.CONTAINS, value="outage"),
        ],
        projections=[ProjectionField(expr="n.id", alias="incident_count", aggregation="COUNT")],
    )

    cypher = ASTCompiler.compile_cypher(ast)
    assert "n.severity IN ['SEV-1', 'SEV-2']" in cypher
    assert "n.summary CONTAINS 'outage'" in cypher
    assert "RETURN COUNT(n.id) AS incident_count" in cypher

    gremlin = ASTCompiler.compile_gremlin(ast)
    assert ".has('severity', P.within('SEV-1', 'SEV-2'))" in gremlin
    assert ".count()" in gremlin

    sparql = ASTCompiler.compile_sparql(ast)
    assert '?n_severity IN ("SEV-1", "SEV-2")' in sparql
    assert 'contains(str(?n_summary), "outage")' in sparql
    assert "(COUNT(?n_id) AS ?incident_count)" in sparql


def test_from_dict_ir_parsing():
    """Validates deserialization from dictionary IR to AST."""
    ir = {
        "patterns": [
            {
                "start_var": "team",
                "start_label": "Team",
                "edge_label": "OWNS",
                "end_var": "service",
                "end_label": "Service",
            }
        ],
        "filters": [{"field": "team.name", "operator": "=", "value": "Platform"}],
        "projections": [{"expr": "service.name", "alias": "owned_service"}],
        "limit": 25,
    }
    ast = ASTCompiler.from_dict(ir)
    assert len(ast.patterns) == 1
    assert ast.patterns[0].start_label == "Team"
    assert ast.filters[0].operator == FilterOp.EQ
    assert ast.limit == 25

    cypher = ASTCompiler.compile_cypher(ast)
    assert "MATCH (team:Team)-[:OWNS]->(service:Service)" in cypher
    assert "WHERE team.name = 'Platform'" in cypher
    assert "LIMIT 25" in cypher

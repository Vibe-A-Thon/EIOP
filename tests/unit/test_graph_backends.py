import json
from urllib.parse import parse_qs

import httpx
from eoip.graph.backends import backend_capabilities, resolve_graph_backend_config
from eoip.graph.neo4j import Neo4jGraphStore
from eoip.graph.neptune import NeptuneGraphStore


def test_graph_backend_config_selects_primary_from_yaml(tmp_path, monkeypatch):
    cfg = tmp_path / "graph-store.yaml"
    cfg.write_text(
        """
primary: neptune
connections:
  hugegraph:
    type: hugegraph
    url: http://hugegraph:8080
  neptune:
    type: neptune
    url: https://neptune.example:8182
    database: prod
""",
        encoding="utf-8",
    )
    monkeypatch.delenv("EOIP_GRAPH_BACKEND", raising=False)
    monkeypatch.delenv("EOIP_GRAPH_URL", raising=False)

    backend, config = resolve_graph_backend_config(cfg)

    assert backend == "neptune"
    assert config["url"] == "https://neptune.example:8182"
    assert config["database"] == "prod"


def test_graph_backend_env_can_switch_connection(tmp_path, monkeypatch):
    cfg = tmp_path / "graph-store.yaml"
    cfg.write_text(
        """
primary: hugegraph
connections:
  hugegraph:
    type: hugegraph
    url: http://hugegraph:8080
  neptune:
    type: neptune
    url: https://neptune.example:8182
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("EOIP_GRAPH_BACKEND", "neptune")
    monkeypatch.setenv("EOIP_GRAPH_URL", "https://override.example:8182")

    backend, config = resolve_graph_backend_config(cfg)

    assert backend == "neptune"
    assert config["url"] == "https://override.example:8182"


def test_backend_capability_catalog_includes_neptune_and_app_languages():
    caps = backend_capabilities("neptune")

    assert "openCypher" in caps["query_languages"]
    assert "SPARQL" in caps["query_languages"]
    assert "EOQL" in caps["application_query_languages"]
    assert "shacl" in caps["exports"]


def test_backend_capability_catalog_includes_neo4j_and_cypher():
    caps = backend_capabilities("neo4j")

    assert caps["native_query_language"] == "Cypher"
    assert "Cypher" in caps["query_languages"]
    assert "EOQL" in caps["application_query_languages"]
    assert "cypher" in caps["exports"]


def test_graph_backend_env_can_switch_to_neo4j_connection(tmp_path, monkeypatch):
    cfg = tmp_path / "graph-store.yaml"
    cfg.write_text(
        """
primary: hugegraph
connections:
  hugegraph:
    type: hugegraph
    url: http://hugegraph:8080
  neo4j:
    type: neo4j
    url: http://neo4j:7474
    database: client
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("EOIP_GRAPH_BACKEND", "neo4j")
    monkeypatch.setenv("EOIP_GRAPH_URL", "http://override-neo4j:7474")

    backend, config = resolve_graph_backend_config(cfg)

    assert backend == "neo4j"
    assert config["url"] == "http://override-neo4j:7474"
    assert config["database"] == "client"


def test_neptune_store_uses_canonical_graph_contract_over_opencypher():
    nodes_by_vid = {}
    edges_by_key = {}

    def handler(request: httpx.Request) -> httpx.Response:
        body = parse_qs(request.content.decode())
        query = body["query"][0]
        params = json.loads(body.get("parameters", ["{}"])[0])

        if "RETURN 1 AS ok" in query:
            return httpx.Response(200, json={"results": [{"ok": 1}]})

        if "MERGE (n:" in query:
            props = dict(params["props"])
            node = {
                "~id": props["eoip_vid"],
                "~labels": [props["entity_type"]],
                "~properties": props,
            }
            nodes_by_vid[props["eoip_vid"]] = node
            return httpx.Response(200, json={"results": [{"n": node}]})

        if "MATCH (n {eoip_vid: $vid})" in query:
            node = nodes_by_vid.get(params["vid"])
            return httpx.Response(200, json={"results": [{"n": node}] if node else []})

        if "MERGE (a)-[r:" in query:
            props = dict(params["props"])
            edge = {
                "~id": props["edge_key"],
                "~type": props["relationship_type"],
                "~start": props["out_v"],
                "~end": props["in_v"],
                "~properties": props,
            }
            edges_by_key[props["edge_key"]] = edge
            return httpx.Response(200, json={"results": [{"r": edge}]})

        if "MATCH ()-[r {edge_key: $edge_key}]->()" in query:
            edge = edges_by_key.get(params["edge_key"])
            return httpx.Response(200, json={"results": [{"r": edge}] if edge else []})

        return httpx.Response(200, json={"results": []})

    store = NeptuneGraphStore(
        "https://neptune.example:8182",
        transport=httpx.MockTransport(handler),
    )

    commit = store.upsert_vertex(
        "Commit",
        {"canonical_id": "commit:1", "commit_sha": "abc123", "message": "Initial"},
    )
    item = store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "item:1", "issue_key": "ITEM-1", "summary": "Story"},
    )
    edge = store.upsert_edge("IMPLEMENTS", commit["vid"], item["vid"], {"fact_key": "fixture"})

    assert store.health()
    assert commit["canonical_id"] == "commit:1"
    assert item["label"] == "WorkItem"
    assert edge["label"] == "IMPLEMENTS"
    assert store.find_edge_by_key(edge["eid"])["out_cid"] == "commit:1"


def test_neo4j_store_uses_canonical_graph_contract_over_cypher_http():
    nodes_by_vid = {}
    nodes_by_canonical = {}
    edges_by_key = {}

    def neo4j_response(columns, rows):
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "columns": columns,
                        "data": [{"row": row} for row in rows],
                    }
                ],
                "errors": [],
            },
        )

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode())
        statement = payload["statements"][0]["statement"]
        params = payload["statements"][0].get("parameters", {})

        if "RETURN 1 AS ok" in statement:
            return neo4j_response(["ok"], [[1]])

        if "MERGE (n:EOIPEntity:" in statement:
            props = dict(params["props"])
            nodes_by_vid[props["eoip_vid"]] = props
            nodes_by_canonical[props["canonical_id"]] = props
            return neo4j_response(["props", "label", "vid"], [[props, props["entity_type"], props["eoip_vid"]]])

        if "MATCH (n:EOIPEntity {eoip_vid: $vid})" in statement:
            props = nodes_by_vid.get(params["vid"])
            rows = [[props, props["entity_type"], props["eoip_vid"]]] if props else []
            return neo4j_response(["props", "label", "vid"], rows)

        if "MATCH (n:EOIPEntity {canonical_id: $canonical_id})" in statement:
            props = nodes_by_canonical.get(params["canonical_id"])
            rows = [[props, props["entity_type"], props["eoip_vid"]]] if props else []
            return neo4j_response(["props", "label", "vid"], rows)

        if "MERGE (a)-[r:" in statement:
            props = dict(params["props"])
            edges_by_key[props["edge_key"]] = props
            return neo4j_response(["props", "type"], [[props, props["relationship_type"]]])

        if "MATCH ()-[r {edge_key: $edge_key}]->()" in statement:
            props = edges_by_key.get(params["edge_key"])
            rows = [[props, props["relationship_type"]]] if props else []
            return neo4j_response(["props", "type"], rows)

        if "RETURN count(n) AS c" in statement:
            return neo4j_response(["c"], [[0]])

        if "RETURN count(r) AS c" in statement:
            return neo4j_response(["c"], [[0]])

        return neo4j_response([], [])

    store = Neo4jGraphStore(
        "http://neo4j.example:7474",
        database="client",
        transport=httpx.MockTransport(handler),
    )

    commit = store.upsert_vertex(
        "Commit",
        {"canonical_id": "commit:1", "commit_sha": "abc123", "message": "Initial"},
    )
    item = store.upsert_vertex(
        "WorkItem",
        {"canonical_id": "item:1", "issue_key": "ITEM-1", "summary": "Story"},
    )
    edge = store.upsert_edge("IMPLEMENTS", commit["vid"], item["vid"], {"fact_key": "fixture"})

    assert store.health()
    assert commit["canonical_id"] == "commit:1"
    assert item["label"] == "WorkItem"
    assert edge["label"] == "IMPLEMENTS"
    assert store.find_edge_by_key(edge["eid"])["in_cid"] == "item:1"

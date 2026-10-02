import json
from pathlib import Path

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.meta import bootstrap_meta_graph
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.repository import RepositoryIngestionService
from eoip.ontology.manifest import VERTEX_LABELS, edge_endpoints_valid


def load_demo(store, data_dir, project_root=None):
    root = Path(project_root or Path(__file__).resolve().parents[2])
    capture = FileEventCapture(Path(data_dir) / "raw")

    bootstrap_meta_graph(store)

    jira = JiraIngestionService(
        store,
        JiraJsonConnector.from_yaml(str(root / "config/mappings/jira-mvp.yaml")),
        capture,
        Path(data_dir) / "dlq",
    )
    jira_result = jira.ingest(
        json.loads((root / "examples/jira/sample-jira.json").read_text(encoding="utf-8"))
    )
    metadata = json.loads((root / "examples/gitlab/sample-gitlab.json").read_text(encoding="utf-8"))
    git_result = RepositoryIngestionService(store, capture).ingest(
        root / "examples/demo-repo", metadata=metadata
    )

    _link_domains(store)

    return {"jira": jira_result, "git": git_result}


def _link_domains(store) -> None:
    domain_vertices = {}
    for dv in store.find_vertices(label="GraphDomain", limit=100):
        domain_vertices[dv["properties"].get("name", "")] = dv

    for vertex in store.find_vertices(limit=50_000):
        label = vertex["label"]
        spec = VERTEX_LABELS.get(label)
        if spec is None:
            continue
        domain_name = spec[0]
        domain_node = domain_vertices.get(domain_name)
        if domain_node is None:
            continue
        if not edge_endpoints_valid("BELONGS_TO_DOMAIN", label, "GraphDomain"):
            continue
        existing = store.edges_from(vertex["vid"])
        already_linked = any(
            e["label"] == "BELONGS_TO_DOMAIN" and e["in_cid"] == domain_node["canonical_id"]
            for e in existing
        )
        if not already_linked:
            store.upsert_edge(
                "BELONGS_TO_DOMAIN",
                vertex["vid"],
                domain_node["vid"],
                {"fact_key": f"domain:{vertex['canonical_id']}:{domain_name}"},
            )

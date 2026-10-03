import json
from pathlib import Path

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.demo_scenarios import load_demo_scenario_pack
from eoip.graph.meta import bootstrap_meta_graph, link_domains
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.repository import RepositoryIngestionService


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

    enterprise_result = load_demo_scenario_pack(
        store,
        data_dir,
        project_root=root,
    )

    link_domains(store, store.find_vertices(limit=50_000))

    return {"jira": jira_result, "git": git_result, "enterprise": enterprise_result}

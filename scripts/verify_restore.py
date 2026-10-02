"""Verify a real HugeGraph restore in an isolated, disposable container."""

import json
from pathlib import Path

from eoip.graph.traversal import GraphTraversal
from eoip.runtime import create_store, data_root
from eoip.snapshot import restore


def main():
    source = max(Path("/source/backups").glob("*.json"), key=lambda path: path.name)
    payload = json.loads(source.read_text())["payload"]
    store = create_store()
    try:
        result = restore(store, data_root(), source)
        assert store.count_vertices() == len(payload["vertices"])
        assert store.count_edges() == len(payload["edges"])
        symbols = store.find_vertices(label="CodeSymbol", filters={"name": "compute_impact"})
        assert symbols
        path = GraphTraversal(store).find_path("urn:eoip:work:item:jira:EOIP-1", symbols[0]["canonical_id"])
        assert path and {edge["label"] for edge in path["edges"]}.issuperset(
            {"IMPLEMENTS", "MODIFIES", "DECLARES"}
        )
        assert all(edge["properties"].get("evidence_key") for edge in path["edges"])
        print(f"PASS: isolated HugeGraph restore: {result}; golden path and source evidence preserved")
    finally:
        store.close()


if __name__ == "__main__":
    main()

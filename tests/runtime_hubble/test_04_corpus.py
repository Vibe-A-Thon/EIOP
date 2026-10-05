"""Verify the entire source-preserving demo corpus through real Hubble queries."""

import json
from pathlib import Path

from eoip.fileparse.engine import FileParser
from eoip.graph.hugegraph import HugeGraphStore

from scripts.load_demo_corpus import TEXT_SOURCE_EXTENSIONS, corpus_files

ROOT = Path(__file__).resolve().parents[2]


def test_full_demo_corpus_and_jira_are_readable(api, hubble):
    for folder in ("manual", "pipelines"):
        document = json.loads((ROOT / "demo" / "demodata" / folder / "jira.json").read_text())
        for issue in document["issues"]:
            canonical_id = f"urn:eoip:work:item:jira:{issue['key']}"
            response = api.get(f"/api/v1/entities/{canonical_id}")
            response.raise_for_status()
            assert canonical_id in response.text

    parser = FileParser()
    canonical_ids = []
    for path in corpus_files(ROOT):
        filename = path.name + ".txt" if path.suffix.lower() in TEXT_SOURCE_EXTENSIONS else path.name
        result = parser.parse_bytes(
            path.read_bytes(), filename, source_id="demo_corpus",
            source_uri="fixture://demo/demodata/" + path.relative_to(ROOT / "demo" / "demodata").as_posix(),
        )
        assert result.status == "SUCCEEDED"
        canonical_ids.extend(item.document_id for item in result.documents)
        canonical_ids.extend(item.chunk_id for item in result.chunks)
    assert canonical_ids
    for offset in range(0, len(canonical_ids), 50):
        batch = canonical_ids[offset:offset + 50]
        arguments = ",".join(json.dumps(HugeGraphStore.vertex_id(cid)) for cid in batch)
        actual = hubble(f"g.V({arguments}).values('canonical_id').fold()")["json_view"]["data"]
        assert len(actual) == 1
        assert set(actual[0]) == set(batch), "A demo document or RAG chunk is missing from HugeGraph"

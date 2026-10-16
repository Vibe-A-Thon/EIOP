"""Tests for SemanticPipeline post-ingestion orchestrator."""

from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.semantic_pipeline import (
    PipelineStage,
    SemanticPipeline,
    SemanticPipelineResult,
    StageResult,
    StageStatus,
)


def _vertex(store, label, canonical_id, **props):
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **props})


def _build_store():
    store = MemoryGraphStore()
    a = _vertex(store, "WorkItem", "item:A", issue_key="A-1")
    b = _vertex(store, "WorkItem", "item:B", issue_key="B-1")
    c = _vertex(store, "Commit", "commit:C", commit_sha="abc123")
    d = _vertex(store, "File", "file:D", repo_id="repo1", path="d.py")
    store.upsert_edge("IMPLEMENTS", c["vid"], a["vid"], {})
    store.upsert_edge("MODIFIES", c["vid"], d["vid"], {})
    store.upsert_edge("IMPLEMENTS", c["vid"], b["vid"], {})
    return store


def test_pipeline_runs_all_stages():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(pipeline_id="test-1")
    assert isinstance(result, SemanticPipelineResult)
    assert result.pipeline_id == "test-1"
    assert len(result.stages) == len(PipelineStage)
    assert result.overall_status == "completed"
    assert result.total_duration_ms >= 0


def test_pipeline_run_specific_stages():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-2",
        stages=[PipelineStage.SEARCH_INDEX, PipelineStage.ANALYTICS],
    )
    assert len(result.stages) == 2
    stage_names = [s.stage for s in result.stages]
    assert PipelineStage.SEARCH_INDEX in stage_names
    assert PipelineStage.ANALYTICS in stage_names


def test_pipeline_metadata_enrichment():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-enrich",
        stages=[PipelineStage.METADATA_ENRICHMENT],
    )
    assert len(result.stages) == 1
    assert result.stages[0].status == StageStatus.COMPLETED


def test_pipeline_search_index():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-search",
        stages=[PipelineStage.SEARCH_INDEX],
    )
    assert result.stages[0].status == StageStatus.COMPLETED
    assert result.stages[0].items_processed >= 4


def test_pipeline_analytics():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-analytics",
        stages=[PipelineStage.ANALYTICS],
    )
    assert result.stages[0].status == StageStatus.COMPLETED
    assert "graph_statistics" in result.stages[0].details


def test_pipeline_validation():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-validation",
        stages=[PipelineStage.VALIDATION],
    )
    assert result.stages[0].status == StageStatus.COMPLETED


def test_pipeline_event_publish():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-events",
        stages=[PipelineStage.EVENT_PUBLISH],
    )
    assert result.stages[0].status == StageStatus.COMPLETED
    assert result.stages[0].details["events_published"] == 1


def test_pipeline_to_dict():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(pipeline_id="test-dict")
    d = result.to_dict()
    assert d["pipeline_id"] == "test-dict"
    assert isinstance(d["stages"], list)
    assert "total_duration_ms" in d
    assert "overall_status" in d


def test_stage_result_to_dict():
    sr = StageResult(
        stage=PipelineStage.ANALYTICS,
        status=StageStatus.COMPLETED,
        duration_ms=42.5,
        items_processed=10,
    )
    d = sr.to_dict()
    assert d["stage"] == "analytics"
    assert d["status"] == "completed"
    assert d["duration_ms"] == 42.5


def test_pipeline_empty_store():
    store = MemoryGraphStore()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(pipeline_id="test-empty")
    assert result.overall_status == "completed"


def test_pipeline_auto_id():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run()
    assert result.pipeline_id.startswith("sem-")


def test_pipeline_with_scope():
    store = _build_store()
    pipeline = SemanticPipeline(store)
    result = pipeline.run(
        pipeline_id="test-scope",
        stages=[PipelineStage.METADATA_ENRICHMENT],
        scope={"domain": "WORK"},
    )
    assert result.overall_status == "completed"

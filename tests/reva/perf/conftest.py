"""REVA performance harness (NFR-001/002/003/008) on a file-backed SQLite store."""

from __future__ import annotations

import json
import os
import statistics
from pathlib import Path

import pytest
from pydantic import BaseModel

from reva.kernel.authority import Authority, ConfidenceBand
from reva.kernel.blobs import BlobStore
from reva.kernel.builder import WarrantDraftBuilder
from reva.kernel.kernel import WarrantKernel
from reva.kernel.predicates import has_predicate, register_predicate
from reva.kernel.producers import register_producer
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog

RESULTS = Path(os.environ.get("REVA_PERF_RESULTS", "test-results/reva-perf.json"))


class PerfMetric(BaseModel):
    lines_of_code: int = 0


def p95(samples: list[float]) -> float:
    return statistics.quantiles(samples, n=20)[18]


def record(name: str, value: float, budget: float, unit: str) -> None:
    """Append one measurement to the perf results file uploaded by the lane."""
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}
    data[name] = {"value": round(value, 4), "budget": budget, "unit": unit}
    RESULTS.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    print(f"{name}: {value:.4f} {unit} (budget {budget})")


@pytest.fixture
def perf_kernel(tmp_path):
    if not has_predicate("reva.pred.perf_metric"):
        register_predicate(name="reva.pred.perf_metric", statement_model=PerfMetric, description="perf metric")
    store = RevaStore(str(tmp_path / "perf.db"))
    log = TransparencyLog(store, "reva_main_log")
    kernel = WarrantKernel(store=store, blobs=BlobStore(root_dir=str(tmp_path / "cas")), log=log)
    producer = register_producer(store, "t1", "tool", "perf", "1.0.0")

    def draft(i: int):
        return (
            WarrantDraftBuilder("reva.pred.perf_metric", f"subject-{i}")
            .producer(producer.producer_id, producer.name, producer.version, producer_type="tool",
                      key_id=producer.active_key_id)
            .about_artifact(f"{i:064x}")
            .authority(Authority.SHIPPED_ARTIFACT)
            .observed()
            .confidence(ConfidenceBand.EXACT, 10000)
            .statement({"lines_of_code": i})
            .build()
        )

    yield kernel, store, log, draft
    store.conn.close()

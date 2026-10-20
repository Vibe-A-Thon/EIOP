"""Shared fixtures for REVA acceptance journeys (API level): real SQLite file store, CAS blobs, REST router."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from reva.api import register_reva_error_handlers, reva_router, set_api_kernel
from reva.kernel.authority import Authority, ConfidenceBand
from reva.kernel.blobs import BlobStore
from reva.kernel.builder import WarrantDraftBuilder
from reva.kernel.kernel import WarrantKernel
from reva.kernel.predicates import has_predicate, register_predicate
from reva.kernel.producers import register_producer
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog


class JourneyMetric(BaseModel):
    lines_of_code: int = 0


@pytest.fixture(autouse=True, scope="session")
def _journey_predicate():
    if not has_predicate("reva.pred.journey_metric"):
        register_predicate(name="reva.pred.journey_metric", statement_model=JourneyMetric,
                           description="acceptance-journey metric")


@pytest.fixture
def stack(tmp_path):
    """A kernel on a file-backed store (not :memory:) plus the REST router over it."""
    store = RevaStore(str(tmp_path / "reva.db"))
    log = TransparencyLog(store, "reva_main_log")
    kernel = WarrantKernel(store=store, blobs=BlobStore(root_dir=str(tmp_path / "cas")), log=log)
    set_api_kernel(kernel)
    app = FastAPI()
    app.include_router(reva_router, prefix="/api/reva/v1")
    register_reva_error_handlers(app)  # as apps/api/main.py mounts it
    producer = register_producer(store, "t1", "tool", "journey-scanner", "1.0.0")

    def draft(subject: str, loc: int, artifact: str = "c" * 64, valid=None):
        builder = (
            WarrantDraftBuilder("reva.pred.journey_metric", subject)
            .producer(producer.producer_id, producer.name, producer.version, producer_type="tool",
                      key_id=producer.active_key_id)
            .about_artifact(artifact)
            .authority(Authority.SHIPPED_ARTIFACT)
            .observed()
            .confidence(ConfidenceBand.EXACT, 10000)
            .statement({"lines_of_code": loc})
        )
        if valid is not None:
            builder = builder.valid(*valid)
        return builder.build()

    with TestClient(app) as client:
        yield {"store": store, "kernel": kernel, "log": log, "client": client, "producer": producer,
               "draft": draft, "path": tmp_path / "reva.db"}
    store.conn.close()

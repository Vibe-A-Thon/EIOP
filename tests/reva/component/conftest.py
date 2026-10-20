"""Shared fixtures for REVA component tests: real SQLite file store, CAS blobs, REST router."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from reva.api import reva_router, set_api_kernel
from reva.kernel.authority import Authority, ConfidenceBand
from reva.kernel.blobs import BlobStore
from reva.kernel.builder import WarrantDraftBuilder
from reva.kernel.kernel import WarrantKernel
from reva.kernel.predicates import register_predicate
from reva.kernel.producers import register_producer
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog


class ComponentMetric(BaseModel):
    lines_of_code: int = 0


@pytest.fixture(autouse=True, scope="session")
def _component_predicate():
    try:
        register_predicate(name="reva.pred.component_metric", statement_model=ComponentMetric,
                           description="component-test metric")
    except Exception:  # already registered in this process
        pass


@pytest.fixture
def stack(tmp_path):
    """A kernel on a file-backed store (not :memory:) plus the REST router over it."""
    store = RevaStore(str(tmp_path / "reva.db"))
    log = TransparencyLog(store, "reva_main_log")
    kernel = WarrantKernel(store=store, blobs=BlobStore(root_dir=str(tmp_path / "cas")), log=log)
    set_api_kernel(kernel)
    app = FastAPI()
    app.include_router(reva_router, prefix="/api/reva/v1")
    producer = register_producer(store, "t1", "tool", "component-scanner", "1.0.0")

    def draft(subject: str, loc: int, artifact: str = "c" * 64):
        return (
            WarrantDraftBuilder("reva.pred.component_metric", subject)
            .producer(producer.producer_id, producer.name, producer.version, producer_type="tool",
                      key_id=producer.active_key_id)
            .about_artifact(artifact)
            .authority(Authority.SHIPPED_ARTIFACT)
            .observed()
            .confidence(ConfidenceBand.EXACT, 10000)
            .statement({"lines_of_code": loc})
            .build()
        )

    with TestClient(app) as client:
        yield {"store": store, "kernel": kernel, "log": log, "client": client, "producer": producer,
               "draft": draft, "path": tmp_path / "reva.db"}
    store.conn.close()

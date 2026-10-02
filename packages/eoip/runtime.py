"""Shared environment configuration for Docker processes."""

import os
from pathlib import Path

from eoip.graph.hugegraph import HugeGraphStore


def create_store():
    return HugeGraphStore(
        os.getenv("EOIP_HUGEGRAPH_URL", "http://hugegraph-server:8080"),
        os.getenv("EOIP_HUGEGRAPH_GRAPH", "hugegraph"),
        os.getenv("EOIP_HUGEGRAPH_USER", "admin"),
        os.getenv("EOIP_HUGEGRAPH_PASSWORD", ""),
    )


def data_root():
    return Path(os.getenv("EOIP_DATA_DIR", "/data"))


def api_token():
    value = os.getenv("EOIP_API_TOKEN", "")
    if len(value) < 24:
        raise RuntimeError("EOIP_API_TOKEN must contain at least 24 characters; run scripts/docker.ps1 first")
    return value

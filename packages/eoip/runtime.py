"""Shared environment configuration for Docker processes."""

import os
from pathlib import Path

from eoip.graph.backends import create_graph_store


def create_store():
    return create_graph_store()


def data_root():
    return Path(os.getenv("EOIP_DATA_DIR", "/data"))


def api_token():
    value = os.getenv("EOIP_API_TOKEN", "")
    if len(value) < 24:
        raise RuntimeError("EOIP_API_TOKEN must contain at least 24 characters; run scripts/container.ps1 first")
    return value

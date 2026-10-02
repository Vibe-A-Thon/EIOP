"""Environment-backed configuration for on-prem REST connectors."""

from __future__ import annotations

import os
from collections.abc import Mapping
from uuid import uuid4

from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.servicenow import ServiceNowConnector


def connector_from_environment(
    source_system: str,
    *,
    correlation_id: str | None = None,
    environ: Mapping[str, str] | None = None,
):
    """Build a source connector from environment values without serializing secrets."""
    variables = os.environ if environ is None else environ
    prefix = {"confluence": "EOIP_CONFLUENCE", "servicenow": "EOIP_SERVICENOW"}.get(source_system)
    correlation_id = correlation_id or str(uuid4())
    if prefix is None:
        raise ValueError(f"unsupported REST connector: {source_system}")

    base_url = variables.get(f"{prefix}_URL", "").strip()
    token = variables.get(f"{prefix}_TOKEN", "").strip() or None
    username = variables.get(f"{prefix}_USERNAME", "").strip() or None
    password = variables.get(f"{prefix}_PASSWORD", "") or None
    if not base_url or bool(username) != bool(password) or (token and username) or not (token or username):
        raise ConnectorError(source_system, "configuration_error", correlation_id)

    connector_class = {
        "confluence": ConfluenceConnector,
        "servicenow": ServiceNowConnector,
    }[source_system]
    try:
        return connector_class(base_url, token=token, username=username, password=password)
    except ValueError as exc:
        raise ConnectorError(source_system, "configuration_error", correlation_id) from exc

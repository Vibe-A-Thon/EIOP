"""Stable connector errors shared by remote source adapters."""

from __future__ import annotations


class ConnectorError(RuntimeError):
    def __init__(self, source_system: str, category: str, correlation_id: str) -> None:
        self.source_system = source_system
        self.category = category
        self.correlation_id = correlation_id
        super().__init__(f"{source_system} connector {category} (correlation_id={correlation_id})")

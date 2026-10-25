"""FT-F08: UniversalDatabaseAdapter SQL/AQL translation binds values, allow-lists names."""

from __future__ import annotations

import sqlite3

import pytest

from eoip.graph.database_adapters import (
    DatabaseConfig,
    DatabaseType,
    UniversalDatabaseAdapter,
    UnsafeIdentifierError,
)

PAYLOADS = ["1 OR 1=1", "x'--", "x' OR '1'='1", "\u2019 OR 1=1 --", "a;DROP TABLE Person"]


def _adapter(db: DatabaseType, client=None) -> UniversalDatabaseAdapter:
    options = {"native_client": client} if client is not None else {}
    return UniversalDatabaseAdapter(DatabaseConfig(db_type=db, options=options))


class _SqliteClient:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute('CREATE TABLE "Person" (name TEXT)')
        self.conn.executemany('INSERT INTO "Person" VALUES (?)', [("alice",), ("bob",)])

    def execute(self, query, parameters):
        return [dict(zip(("name",), row)) for row in self.conn.execute(query, parameters or {})]


@pytest.mark.parametrize("payload", PAYLOADS)
def test_sql_values_are_bound_not_interpolated(payload: str) -> None:
    query, params = _adapter(DatabaseType.SQLITE).translate_query_bound(
        f'MATCH (p:Person) WHERE p.name = "{payload}" RETURN p LIMIT 5'
    )
    assert payload not in query
    assert query == 'SELECT * FROM "Person" WHERE "name" = :p0 LIMIT :limit'
    assert params == {"p0": payload, "limit": 5}


@pytest.mark.parametrize("payload", PAYLOADS)
def test_payloads_match_nothing_when_executed(payload: str) -> None:
    client = _SqliteClient()
    rows = _adapter(DatabaseType.SQLITE, client).execute_query(
        f'MATCH (p:Person) WHERE p.name = "{payload}" RETURN p'
    )
    assert rows == []
    # Table still intact.
    assert client.conn.execute('SELECT count(*) FROM "Person"').fetchone()[0] == 2


def test_legit_value_still_matches() -> None:
    rows = _adapter(DatabaseType.SQLITE, _SqliteClient()).execute_query(
        "MATCH (p:Person) WHERE p.name = 'alice' RETURN p"
    )
    assert rows == [{"name": "alice"}]


@pytest.mark.parametrize("payload", PAYLOADS)
def test_aql_uses_bind_vars(payload: str) -> None:
    query, params = _adapter(DatabaseType.ARANGODB).translate_query_bound(
        f'MATCH (p:Person) WHERE p.name = "{payload}" RETURN p LIMIT 3'
    )
    assert payload not in query
    assert query == "FOR p IN @@collection FILTER p.@attr == @value LIMIT @limit RETURN p"
    assert params == {"@collection": "Person", "attr": "name", "value": payload, "limit": 3}


def test_non_ascii_identifier_is_rejected() -> None:
    with pytest.raises(UnsafeIdentifierError):
        _adapter(DatabaseType.POSTGRESQL).translate_query("MATCH (p:Pers\u00f6n) RETURN p")


def test_age_refuses_dollar_quote_breakout() -> None:
    with pytest.raises(UnsafeIdentifierError):
        _adapter(DatabaseType.APACHE_AGE).translate_query("MATCH (n) RETURN n $$; DROP TABLE x; --")


def test_dry_run_reports_parameters_separately() -> None:
    result = _adapter(DatabaseType.POSTGRESQL).execute_query("MATCH (p:Person) WHERE p.name = 'x' RETURN p")
    assert result[0]["mode"] == "dry_run"
    assert result[0]["query"] == 'SELECT * FROM "Person" WHERE "name" = :p0'
    assert result[0]["parameters"] == {"p0": "x"}

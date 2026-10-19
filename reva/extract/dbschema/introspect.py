"""Relational database schema introspection (T-602 / REVA-DB-001..005)."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool = True
    primary_key: bool = False
    default_value: Optional[str] = None


@dataclass
class ForeignKeyInfo:
    column_name: str
    referred_table: str
    referred_column: str


@dataclass
class TableInfo:
    name: str
    columns: List[ColumnInfo] = field(default_factory=list)
    foreign_keys: List[ForeignKeyInfo] = field(default_factory=list)
    indexes: List[str] = field(default_factory=list)


@dataclass
class DatabaseSchema:
    dialect: str
    tables: List[TableInfo] = field(default_factory=list)


def introspect_sqlite(db_path: Union[str, Path]) -> DatabaseSchema:
    """Introspect SQLite database file using PRAGMA inspection."""
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Get tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    table_names = [r[0] for r in cur.fetchall()]

    tables: List[TableInfo] = []
    for t in table_names:
        # Columns: (cid, name, type, notnull, dflt_value, pk)
        cur.execute(f"PRAGMA table_info('{t}')")
        cols = []
        for c in cur.fetchall():
            cols.append(
                ColumnInfo(
                    name=c[1],
                    data_type=c[2] or "TEXT",
                    nullable=(c[3] == 0),
                    default_value=c[4],
                    primary_key=(c[5] == 1),
                )
            )

        # Foreign keys: (id, seq, table, from, to, on_update, on_delete, match)
        cur.execute(f"PRAGMA foreign_key_list('{t}')")
        fks = []
        for fk in cur.fetchall():
            fks.append(
                ForeignKeyInfo(
                    column_name=fk[3],
                    referred_table=fk[2],
                    referred_column=fk[4],
                )
            )

        # Indexes
        cur.execute(f"PRAGMA index_list('{t}')")
        indexes = [idx[1] for idx in cur.fetchall()]

        tables.append(TableInfo(name=t, columns=cols, foreign_keys=fks, indexes=indexes))

    conn.close()
    return DatabaseSchema(dialect="sqlite", tables=tables)

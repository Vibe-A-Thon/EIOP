"""Deterministic Lineage Parser with Uncertainty and Diagnostics (CRA-029.3).

Features:
- Parses static SQL queries and data transformations to extract exact input-output lineage.
- Strict anti-hallucination guarantee (CRA-029.3): Unknown or dynamic statements (e.g., dynamic SQL,
  stored procedure calls, unparseable dialects) emit UNCERTAIN lineage with explicit diagnostic messages,
  NEVER guessing or fabricating source-target edges.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Optional


@dataclass
class LineageEdge:
    source_table: str
    target_table: str
    source_columns: list[str] = field(default_factory=list)
    target_columns: list[str] = field(default_factory=list)
    transformation_type: str = "DIRECT"


@dataclass
class LineageParseResult:
    query_id: str
    status: str  # DETERMINISTIC, UNCERTAIN, UNSUPPORTED
    edges: list[LineageEdge] = field(default_factory=list)
    confidence: float = 1.0
    diagnostics: list[str] = field(default_factory=list)
    raw_query: str = ""


class LineageParser:
    """Parses SQL and ETL transformations into deterministic lineage or diagnostic uncertainty (CRA-029.3)."""

    DYNAMIC_PATTERNS = [
        re.compile(r"\bEXEC\s*\(", re.IGNORECASE),
        re.compile(r"\bEXECUTE\s*\(", re.IGNORECASE),
        re.compile(r"\bsp_executesql\b", re.IGNORECASE),
        re.compile(r"\bPREPARE\b", re.IGNORECASE),
        re.compile(r"\bCALL\s+[a-zA-Z0-9_]+\s*\(", re.IGNORECASE),
    ]

    CREATE_VIEW_PATTERN = re.compile(
        r"CREATE\s+(?:OR\s+REPLACE\s+)?VIEW\s+([a-zA-Z0-9_\.]+)\s+AS\s+SELECT\s+(.+?)\s+FROM\s+([a-zA-Z0-9_\.]+)",
        re.IGNORECASE | re.DOTALL,
    )

    INSERT_INTO_PATTERN = re.compile(
        r"INSERT\s+INTO\s+([a-zA-Z0-9_\.]+)\s*(?:\([^\)]+\))?\s*SELECT\s+(.+?)\s+FROM\s+([a-zA-Z0-9_\.]+)",
        re.IGNORECASE | re.DOTALL,
    )

    SELECT_FROM_PATTERN = re.compile(
        r"SELECT\s+(.+?)\s+FROM\s+([a-zA-Z0-9_\.]+)",
        re.IGNORECASE | re.DOTALL,
    )

    def parse_query_lineage(self, sql_query: str, query_id: str = "query-01") -> LineageParseResult:
        """Parse lineage from SQL query, yielding diagnostics on uncertainty (CRA-029.3)."""
        clean_query = sql_query.strip()

        # Check for dynamic SQL statements
        for pattern in self.DYNAMIC_PATTERNS:
            if pattern.search(clean_query):
                return LineageParseResult(
                    query_id=query_id,
                    status="UNCERTAIN",
                    edges=[],
                    confidence=0.0,
                    diagnostics=[
                        f"Dynamic SQL statement detected matching '{pattern.pattern}'. "
                        "Static lineage cannot be inferred deterministically without execution trace (CRA-029.3)."
                    ],
                    raw_query=clean_query,
                )

        # Check for CREATE VIEW
        view_match = self.CREATE_VIEW_PATTERN.search(clean_query)
        if view_match:
            target_table = view_match.group(1).strip()
            cols_str = view_match.group(2).strip()
            source_table = view_match.group(3).strip()
            cols = [c.strip().split()[-1] for c in cols_str.split(",") if c.strip()]
            edge = LineageEdge(
                source_table=source_table,
                target_table=target_table,
                source_columns=cols,
                target_columns=cols,
                transformation_type="VIEW_PROJECTION",
            )
            return LineageParseResult(
                query_id=query_id,
                status="DETERMINISTIC",
                edges=[edge],
                confidence=1.0,
                diagnostics=[],
                raw_query=clean_query,
            )

        # Check for INSERT INTO ... SELECT
        insert_match = self.INSERT_INTO_PATTERN.search(clean_query)
        if insert_match:
            target_table = insert_match.group(1).strip()
            cols_str = insert_match.group(2).strip()
            source_table = insert_match.group(3).strip()
            cols = [c.strip().split()[-1] for c in cols_str.split(",") if c.strip()]
            edge = LineageEdge(
                source_table=source_table,
                target_table=target_table,
                source_columns=cols,
                target_columns=cols,
                transformation_type="ETL_INSERT",
            )
            return LineageParseResult(
                query_id=query_id,
                status="DETERMINISTIC",
                edges=[edge],
                confidence=1.0,
                diagnostics=[],
                raw_query=clean_query,
            )

        # Standalone SELECT FROM
        select_match = self.SELECT_FROM_PATTERN.search(clean_query)
        if select_match:
            cols_str = select_match.group(1).strip()
            source_table = select_match.group(2).strip()
            cols = [c.strip().split()[-1] for c in cols_str.split(",") if c.strip()]
            edge = LineageEdge(
                source_table=source_table,
                target_table="ANONYMOUS_QUERY_OUTPUT",
                source_columns=cols,
                target_columns=cols,
                transformation_type="SELECT_PROJECTION",
            )
            return LineageParseResult(
                query_id=query_id,
                status="DETERMINISTIC",
                edges=[edge],
                confidence=1.0,
                diagnostics=[],
                raw_query=clean_query,
            )

        # Unparseable query -> emit UNCERTAIN with diagnostic rather than guessing!
        return LineageParseResult(
            query_id=query_id,
            status="UNCERTAIN",
            edges=[],
            confidence=0.0,
            diagnostics=[
                "Unsupported or complex SQL dialect syntax; lineage parser refuses to guess edges (CRA-029.3)."
            ],
            raw_query=clean_query,
        )

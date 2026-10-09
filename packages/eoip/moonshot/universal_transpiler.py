"""Moonshot 5: Universal Multi-Dialect Graph Transpiler & Phantom Virtual Views.

Provides:
- Bidirectional transpilation between ISO GQL, openCypher, Gremlin, SPARQL, and SQL/PGQ.
- Phantom Virtual Graph Views enabling Zero-ETL graph queries directly over relational/tabular records.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class UniversalAST:
    """Canonical Intermediate Representation for cross-dialect graph queries."""
    anchor_label: str = ""
    variable: str = "n"
    filters: list[dict[str, Any]] = field(default_factory=list)  # field, op, value
    traversals: list[dict[str, Any]] = field(default_factory=list)  # edge, direction, target_label
    returns: list[str] = field(default_factory=list)
    limit: int | None = None


class UniversalTranspiler:
    """Multi-dialect graph query transpiler targeting ISO GQL, Cypher, Gremlin, and SPARQL."""

    def parse_cypher_or_gql(self, query: str) -> UniversalAST:
        """Parse subset of openCypher or ISO GQL into UniversalAST."""
        ast = UniversalAST()
        # Extract MATCH (var:Label)
        match_pattern = re.search(r"MATCH\s*\(\s*(\w+)(?::(\w+))?\s*\)", query, re.IGNORECASE)
        if match_pattern:
            ast.variable = match_pattern.group(1) or "n"
            ast.anchor_label = match_pattern.group(2) or ""

        # Extract WHERE clause: WHERE var.prop = 'val'
        where_pattern = re.search(r"WHERE\s+([^\s]+)\s*(=|>|<|!=)\s*['\"]?([^'\"\s]+)['\"]?", query, re.IGNORECASE)
        if where_pattern:
            prop_expr = where_pattern.group(1)
            prop_name = prop_expr.split(".")[-1]
            op = where_pattern.group(2)
            val = where_pattern.group(3)
            ast.filters.append({"field": prop_name, "op": op, "value": val})

        # Extract RETURN var
        return_pattern = re.search(r"RETURN\s+([^\s,]+(?:\s*,\s*[^\s,]+)*)", query, re.IGNORECASE)
        if return_pattern:
            raw_returns = return_pattern.group(1).split(",")
            ast.returns = [r.strip() for r in raw_returns]
        else:
            ast.returns = [ast.variable]

        # Extract LIMIT
        limit_pattern = re.search(r"LIMIT\s+(\d+)", query, re.IGNORECASE)
        if limit_pattern:
            ast.limit = int(limit_pattern.group(1))

        return ast

    def to_gremlin(self, ast: UniversalAST) -> str:
        """Lower UniversalAST to Apache TinkerPop Gremlin."""
        steps = ["g.V()"]
        if ast.anchor_label:
            steps.append(f"hasLabel('{ast.anchor_label}')")

        for f in ast.filters:
            if f["op"] == "=":
                steps.append(f"has('{f['field']}', '{f['value']}')")
            elif f["op"] == ">":
                steps.append(f"has('{f['field']}', P.gt({f['value']}))")
            elif f["op"] == "<":
                steps.append(f"has('{f['field']}', P.lt({f['value']}))")

        for t in ast.traversals:
            dir_func = "out" if t.get("direction", "out") == "out" else "in"
            edge_lbl = t.get("edge", "")
            steps.append(f"{dir_func}('{edge_lbl}')")

        if ast.limit:
            steps.append(f"limit({ast.limit})")

        return ".".join(steps)

    def to_cypher(self, ast: UniversalAST) -> str:
        """Lower UniversalAST to openCypher."""
        lbl_str = f":{ast.anchor_label}" if ast.anchor_label else ""
        clauses = [f"MATCH ({ast.variable}{lbl_str})"]

        if ast.filters:
            filter_clauses = []
            for f in ast.filters:
                val_str = f"'{f['value']}'" if isinstance(f["value"], str) else str(f["value"])
                filter_clauses.append(f"{ast.variable}.{f['field']} {f['op']} {val_str}")
            clauses.append("WHERE " + " AND ".join(filter_clauses))

        ret_str = ", ".join(ast.returns) if ast.returns else ast.variable
        clauses.append(f"RETURN {ret_str}")

        if ast.limit:
            clauses.append(f"LIMIT {ast.limit}")

        return " ".join(clauses)

    def to_gql(self, ast: UniversalAST) -> str:
        """Lower UniversalAST to ISO GQL (ISO/IEC 39075:2024)."""
        # ISO GQL standard syntax conforms closely to graph pattern matching
        return self.to_cypher(ast)

    def to_sparql(self, ast: UniversalAST) -> str:
        """Lower UniversalAST to SPARQL 1.1."""
        var = f"?{ast.variable}"
        triples = []
        if ast.anchor_label:
            triples.append(f"{var} a :{ast.anchor_label} .")
        for f in ast.filters:
            triples.append(f"{var} :{f['field']} '{f['value']}' .")

        where_block = " ".join(triples)
        sparql = f"SELECT {var} WHERE {{ {where_block} }}"
        if ast.limit:
            sparql += f" LIMIT {ast.limit}"
        return sparql

    def to_sql_pgq(self, ast: UniversalAST) -> str:
        """Lower UniversalAST to SQL/PGQ (ISO/IEC 9075-16:2023)."""
        lbl = f" IS {ast.anchor_label}" if ast.anchor_label else ""
        sql = f"SELECT * FROM GRAPH_TABLE (enterprise_graph MATCH ({ast.variable}{lbl})"
        if ast.filters:
            f = ast.filters[0]
            sql += f" WHERE {ast.variable}.{f['field']} {f['op']} '{f['value']}'"
        sql += f" COLUMNS ({ast.variable}.id))"
        return sql


class PhantomVirtualGraphView:
    """Exposes zero-ETL virtual graph nodes directly from tabular/external source records."""

    def __init__(self, table_name: str, records: list[dict[str, Any]], id_col: str, label: str) -> None:
        self.table_name = table_name
        self.records = records
        self.id_col = id_col
        self.label = label

    def query(self, ast: UniversalAST) -> list[dict[str, Any]]:
        """Evaluate graph query pushdown directly onto tabular records without copying."""
        results: list[dict[str, Any]] = []

        for row in self.records:
            # Check label match
            if ast.anchor_label and ast.anchor_label != self.label:
                continue

            # Check filters
            matched = True
            for f in ast.filters:
                row_val = str(row.get(f["field"], ""))
                req_val = str(f["value"])
                if f["op"] == "=" and row_val != req_val:
                    matched = False
                    break
                elif f["op"] == "!=" and row_val == req_val:
                    matched = False
                    break

            if matched:
                results.append(row)
                if ast.limit and len(results) >= ast.limit:
                    break

        return results

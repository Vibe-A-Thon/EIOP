"""SQL SELECT front-end — subset for the SQL analytics surface.

Supported subset:
  SELECT col[, col | COUNT(*)] FROM table
  [WHERE col op value [AND ...]]
  [GROUP BY col] [ORDER BY col [ASC|DESC]] [LIMIT n]

Operators: ``=``, ``!=``, ``>``, ``<``, ``>=``, ``<=``, ``LIKE``.
Aggregates: ``count(*)``. Executes over a fixture of named tables
(``{"tables": {"name": [row, ...]}}``). Deterministic stdlib-only parser —
no external SQL engine.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_SELECT = re.compile(
    r"^SELECT\s+(?P<select>.+?)\s+FROM\s+(?P<from>[A-Za-z_][\w.-]*)"
    r"(?:\s+WHERE\s+(?P<where>.+?))?"
    r"(?:\s+GROUP\s+BY\s+(?P<group>[A-Za-z_][\w.-]*))?"
    r"(?:\s+ORDER\s+BY\s+(?P<order>[A-Za-z_][\w.-]*)(?:\s+(?P<dir>ASC|DESC))?)?"
    r"(?:\s+LIMIT\s+(?P<limit>\d+))?$",
    re.IGNORECASE | re.DOTALL,
)


def _literal(raw: str) -> Any:
    raw = raw.strip()
    if (raw.startswith("'") and raw.endswith("'")) or (raw.startswith('"') and raw.endswith('"')):
        return raw[1:-1]
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw


def parse(query: str) -> QLangPlan:
    """Parse a SQL SELECT subset statement into a QLangPlan."""
    q = re.sub(r"\s+", " ", query.strip().rstrip(";"))
    m = _SELECT.match(q)
    if not m:
        raise QLangParseError(
            "Invalid SQL subset. Supported: SELECT <cols> FROM <t> "
            "[WHERE ..] [GROUP BY ..] [ORDER BY ..] [LIMIT n]"
        )
    select_raw = m.group("select").strip()
    if select_raw.upper() == "COUNT(*)":
        count_star = True
        columns: list[str] = []
    else:
        items = [c.strip() for c in select_raw.split(",")]
        count_star = any(c.upper() == "COUNT(*)" for c in items)
        columns = [c for c in items if c.upper() != "COUNT(*)"]
        if columns == ["*"]:
            pass  # full-row projection
        elif not all(re.fullmatch(r"[A-Za-z_][\w.-]*", c) for c in columns):
            raise QLangParseError(f"Unsupported SQL SELECT list: {select_raw!r}")

    wheres: list[dict[str, Any]] = []
    if m.group("where"):
        for cond in re.split(r"\s+AND\s+", m.group("where"), flags=re.IGNORECASE):
            cm = re.fullmatch(
                r"([A-Za-z_][\w.-]*)\s*(>=|<=|!=|=|>|<|LIKE)\s*(.+?)", cond.strip(), re.IGNORECASE
            )
            if not cm:
                raise QLangParseError(f"Unsupported SQL WHERE condition: {cond!r}")
            op = cm.group(2).upper() if cm.group(2).upper() == "LIKE" else cm.group(2)
            wheres.append({"field": cm.group(1), "op": op, "value": _literal(cm.group(3))})

    return QLangPlan(
        language="sql",
        intent="AGGREGATE" if count_star or m.group("group") else ("FILTER" if wheres else "PROJECT"),
        operation="SQL-SELECT",
        source=q,
        projection=columns,
        group_by=[m.group("group")] if m.group("group") else [],
        aggregates={"count": "count"} if count_star else {},
        order_by=([m.group("order") + (" DESC" if m.group("dir") else "")] if m.group("order") else []),
        limit=int(m.group("limit")) if m.group("limit") else 50,
        extra={
            "table": m.group("from"),
            "wheres": wheres,
            "count_star": count_star,
        },
    )


def _row_matches(row: dict[str, Any], wheres: list[dict[str, Any]]) -> bool:
    for w in wheres:
        actual = row.get(w["field"])
        op, val = w["op"], w["value"]
        if op == "LIKE":
            pattern = re.escape(str(val)).replace(r"%", ".*").replace(r"_", ".")
            if actual is None or not re.fullmatch(pattern, str(actual)):
                return False
        elif op == "=":
            if str(actual) != str(val):
                return False
        elif op == "!=":
            if str(actual) == str(val):
                return False
        else:
            try:
                a, b = float(actual), float(val)
            except (TypeError, ValueError):
                return False
            if not {
                ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b,
            }[op]:
                return False
    return True


def evaluate(plan: QLangPlan, tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Execute a parsed SQL SELECT over a fixture of named tables."""
    table = plan.extra["table"]
    if table not in tables:
        raise QLangParseError(f"Unknown table: {table!r}")
    rows = [r for r in tables[table] if _row_matches(r, plan.extra["wheres"])]

    if plan.extra["count_star"] and not plan.group_by:
        rows = [{"count": len(rows)}]
    elif plan.group_by:
        by = plan.group_by[0]
        buckets: dict[Any, list[dict[str, Any]]] = {}
        for r in rows:
            buckets.setdefault(r.get(by), []).append(r)
        if plan.extra["count_star"]:
            rows = [{by: k, "count": len(v)} for k, v in buckets.items()]
        else:
            rows = [{by: k, **{c: v[0].get(c) for c in plan.projection if c != by}} for k, v in buckets.items()]

    for spec in reversed(plan.order_by):
        parts = spec.split()
        key = parts[0]
        rows.sort(key=lambda r: str(r.get(key)), reverse=len(parts) > 1)

    if plan.projection and plan.projection != ["*"] and not plan.group_by:
        rows = [{c: r.get(c) for c in plan.projection} for r in rows]
    return rows[: plan.limit]


def parse_and_evaluate(query: str, tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    return evaluate(parse(query), tables)

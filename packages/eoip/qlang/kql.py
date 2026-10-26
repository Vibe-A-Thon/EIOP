"""KQL front-end (Kibana/KQL subset): ``search`` / ``where`` / ``summarize``.

Supported subset:
  <source> [| where field == value] [| where field != value]*
  [| summarize count() by field] [| take n | limit n]

Sources: a bare table name (fixture key) or ``search "<query>"`` /
``search field:value``. Executes over a fixture dict of tables, where each
table is a list of row dicts. Deterministic — no external Kusto engine.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_WHERE = re.compile(r"^where\s+([A-Za-z_][\w.-]*)\s*(==|!=)\s*(.+?)\s*$")
_SUMMARIZE = re.compile(r"^summarize\s+(\w+)\s*\((\w*)\)(?:\s+by\s+([A-Za-z_][\w.-]*))?$")
_SEARCH = re.compile(r'^search\s+("([^"]*)"|([A-Za-z_][\w.-]*):(.+))$')


def parse(query: str) -> QLangPlan:
    """Parse a KQL subset pipeline into a QLangPlan."""
    q = query.strip()
    if not q:
        raise QLangParseError("Empty KQL query")
    parts = [p.strip() for p in q.split("|")]
    source = parts[0]
    sm = _SEARCH.match(source)
    if sm:
        table = None
        search = {"term": sm.group(2), "field": sm.group(3), "value": sm.group(4)}
    else:
        if not re.fullmatch(r"[A-Za-z_][\w.-]*", source):
            raise QLangParseError(f"Invalid KQL source: {source!r}")
        table = source
        search = None

    wheres: list[dict[str, Any]] = []
    summarize: dict[str, Any] | None = None
    take: int | None = None
    for stage in parts[1:]:
        if not stage:
            continue
        wm = _WHERE.match(stage)
        if wm:
            wheres.append({"field": wm.group(1), "op": wm.group(2), "value": _literal(wm.group(3))})
            continue
        gm = _SUMMARIZE.match(stage)
        if gm:
            summarize = {"func": gm.group(1), "arg": gm.group(2) or None, "by": gm.group(3)}
            continue
        tm = re.match(r"^(?:take|limit)\s+(\d+)$", stage)
        if tm:
            take = int(tm.group(1))
            continue
        raise QLangParseError(f"Unsupported KQL stage: {stage!r}")
    if summarize and summarize["func"] != "count":
        raise QLangParseError(f"Unsupported KQL summarize function: {summarize['func']!r}")

    intent: Any = "AGGREGATE" if summarize else "FILTER"
    return QLangPlan(
        language="kql_kibana",
        intent=intent,
        operation="KQL",
        source=q,
        group_by=[summarize["by"]] if summarize and summarize["by"] else [],
        aggregates={"count": "count"} if summarize else {},
        limit=take or 50,
        extra={"table": table, "search": search, "wheres": wheres, "summarize": summarize},
    )


def _literal(raw: str) -> Any:
    raw = raw.strip()
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw


def evaluate(plan: QLangPlan, tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Evaluate a parsed KQL query over a fixture of named tables."""
    table = plan.extra["table"]
    if table is None:
        rows = [r for t in tables.values() for r in t]
    else:
        if table not in tables:
            raise QLangParseError(f"Unknown KQL table: {table!r}")
        rows = list(tables[table])

    search = plan.extra["search"]
    if search:
        if search["term"] is not None:
            needle = search["term"].casefold()
            rows = [r for r in rows if any(needle in str(v).casefold() for v in r.values())]
        else:
            rows = [r for r in rows if str(r.get(search["field"])) == str(search["value"])]

    for w in plan.extra["wheres"]:
        if w["op"] == "==":
            rows = [r for r in rows if str(r.get(w["field"])) == str(w["value"])]
        else:
            rows = [r for r in rows if str(r.get(w["field"])) != str(w["value"])]

    summarize = plan.extra["summarize"]
    if summarize:
        by = summarize["by"]
        if by:
            buckets: dict[Any, int] = {}
            for r in rows:
                buckets[r.get(by)] = buckets.get(r.get(by), 0) + 1
            rows = [{by: k, "count": v} for k, v in sorted(buckets.items(), key=lambda x: -x[1])]
        else:
            rows = [{"count": len(rows)}]
    return rows[: plan.limit]


def parse_and_evaluate(query: str, tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    return evaluate(parse(query), tables)

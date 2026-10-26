"""PromQL front-end — instant and range queries over /metrics-style series.

Supported subset:
  * instant vector: ``metric``, ``metric{label="v", other!="x"}``,
    aggregation ``sum(metric) by (label)`` / ``avg(metric)``;
  * range query: same expression wrapped with start/end/step parameters
    supplied by the caller (``evaluate_range``), plus range-vector
    selectors inside ``rate``/``increase`` are parsed into the plan IR but
    rate evaluation over samples is provided for per-second deltas.

Series fixtures: ``[{"metric": str, "labels": {..}, "samples": [[t, v], ...]}]``.
Timestamps are seconds (int/float). Deterministic — no Prometheus server.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_SELECTOR = re.compile(
    r"^(?P<metric>[A-Za-z_:][A-Za-z0-9_:]*)(?:\{(?P<labels>[^}]*)\})?(?:\[(?P<range>[0-9]+[smhd])\])?$"
)
_AGG = re.compile(
    r"^(?P<func>sum|avg|min|max|count)\s*\((?P<inner>.+?)\)\s*(?:by\s*\((?P<by>[^)]+)\))?$"
)
_RATE = re.compile(
    r"^(?P<func>rate|increase)\s*\(\s*(?P<metric>[A-Za-z_:][A-Za-z0-9_:]*)(?:\{(?P<labels>[^}]*)\})?\s*\[(?P<window>[0-9]+[smhd])\]\s*\)"
    r"(?:\s*by\s*\((?P<by>[^)]+)\))?$"
)

_RANGE_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def _parse_labels(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    out: dict[str, str] = {}
    for pair in raw.split(","):
        pm = re.fullmatch(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*(!=|=~|!~|=)\s*\"([^\"]*)\"\s*", pair)
        if not pm:
            raise QLangParseError(f"Invalid PromQL label matcher: {pair!r}")
        op = pm.group(2)
        if op not in ("=", "!="):
            raise QLangParseError(f"PromQL regex matchers {op!r} are outside the subset")
        out[pm.group(1)] = f"{op}{pm.group(3)}"
    return out


def _range_seconds(raw: str) -> int:
    return int(raw[:-1]) * _RANGE_SECONDS[raw[-1]]


def parse(query: str) -> QLangPlan:
    """Parse a PromQL instant expression into a QLangPlan."""
    q = re.sub(r"\s+", " ", query.strip())
    if not q:
        raise QLangParseError("Empty PromQL query")

    rm = _RATE.match(q)
    if rm:
        return QLangPlan(
            language="promql",
            intent="AGGREGATE",
            operation="PromQL-rate",
            source=q,
            group_by=[b.strip() for b in (rm.group("by") or "").split(",") if b.strip()],
            aggregates={"value": rm.group("func")},
            extra={
                "kind": "rate",
                "func": rm.group("func"),
                "metric": rm.group("metric"),
                "labels": _parse_labels(rm.group("labels")),
                "window_s": _range_seconds(rm.group("window")),
            },
        )

    am = _AGG.match(q)
    if am:
        inner = am.group("inner").strip()
        sm = _SELECTOR.match(inner)
        if not sm or sm.group("range"):
            raise QLangParseError(f"Unsupported PromQL aggregation input: {inner!r}")
        return QLangPlan(
            language="promql",
            intent="AGGREGATE",
            operation="PromQL-aggregate",
            source=q,
            group_by=[b.strip() for b in (am.group("by") or "").split(",") if b.strip()],
            aggregates={"value": am.group("func")},
            extra={
                "kind": "aggregate",
                "func": am.group("func"),
                "metric": sm.group("metric"),
                "labels": _parse_labels(sm.group("labels")),
            },
        )

    sm = _SELECTOR.match(q)
    if sm:
        return QLangPlan(
            language="promql",
            intent="PROJECT",
            operation="PromQL-instant",
            source=q,
            extra={
                "kind": "instant",
                "metric": sm.group("metric"),
                "labels": _parse_labels(sm.group("labels")),
                "range_s": _range_seconds(sm.group("range")) if sm.group("range") else None,
            },
        )
    raise QLangParseError(f"Unsupported PromQL expression: {q!r}")


def _label_match(labels: dict[str, str], matchers: dict[str, str]) -> bool:
    for key, cond in matchers.items():
        op, val = cond[0], cond[1:]
        if op == "=" and labels.get(key) != val:
            return False
        if op == "!=" and labels.get(key) == val:
            return False
    return True


def _select(
    series: list[dict[str, Any]], metric: str, matchers: dict[str, str]
) -> list[dict[str, Any]]:
    return [s for s in series if s["metric"] == metric and _label_match(s.get("labels", {}), matchers)]


def evaluate(plan: QLangPlan, series: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Evaluate an instant PromQL query over a series fixture."""
    kind = plan.extra["kind"]
    selected = _select(series, plan.extra["metric"], plan.extra["labels"])
    if kind == "instant":
        out = []
        for s in selected:
            if not s["samples"]:
                continue
            t, v = s["samples"][-1]
            out.append({"metric": s["metric"], "labels": s.get("labels", {}), "t": t, "value": v})
        return out
    if kind == "aggregate":
        vals = [s["samples"][-1][1] for s in selected if s["samples"]]
        func = plan.extra["func"]
        if func == "count":
            value: Any = len(vals)
        elif not vals:
            value = None
        elif func == "sum":
            value = sum(vals)
        elif func == "avg":
            value = sum(vals) / len(vals)
        elif func == "min":
            value = min(vals)
        else:
            value = max(vals)
        if plan.group_by:
            out = []
            groups: dict[tuple, list[float]] = {}
            for s in selected:
                if not s["samples"]:
                    continue
                key = tuple(s.get("labels", {}).get(b) for b in plan.group_by)
                groups.setdefault(key, []).append(s["samples"][-1][1])
            for key, gvals in sorted(groups.items()):
                gval: Any = len(gvals) if func == "count" else (
                    sum(gvals) if func == "sum"
                    else sum(gvals) / len(gvals) if func == "avg"
                    else min(gvals) if func == "min"
                    else max(gvals)
                )
                out.append({"labels": dict(zip(plan.group_by, key)), "value": gval})
            return out
        return [{"metric": plan.extra["metric"], "value": value}]
    if kind == "rate":
        window = plan.extra["window_s"]
        func = plan.extra["func"]
        out = []
        for s in selected:
            samples = [sv for sv in s["samples"] if sv[0] > (s["samples"][-1][0] - window)] if s["samples"] else []
            if len(samples) < 2:
                out.append({"metric": s["metric"], "labels": s.get("labels", {}), "value": 0.0})
                continue
            delta_v = samples[-1][1] - samples[0][1]
            delta_t = samples[-1][0] - samples[0][0]
            per_sec = (delta_v / delta_t) if delta_t > 0 else 0.0
            out.append({
                "metric": s["metric"],
                "labels": s.get("labels", {}),
                "value": per_sec if func == "rate" else per_sec * window,
            })
        return out
    raise QLangParseError(f"Unknown PromQL plan kind: {kind!r}")


def evaluate_range(
    plan: QLangPlan,
    series: list[dict[str, Any]],
    start: float,
    end: float,
    step: float,
) -> list[dict[str, Any]]:
    """Evaluate as a range query: instant value re-sampled at each step.

    For instant/aggregate plans the value is the latest sample at or before
    each step timestamp.
    """
    if step <= 0:
        raise QLangParseError("Range step must be positive")
    out = []
    ts = start
    while ts <= end:
        windowed = []
        for s in _select(series, plan.extra["metric"], plan.extra["labels"]):
            prior = [sv for sv in s["samples"] if sv[0] <= ts]
            windowed.append({**s, "samples": prior})
        vals = evaluate(plan, windowed)
        out.append({"t": ts, "result": vals})
        ts += step
    return out

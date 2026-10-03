"""Process mining engine (G2-PM-001..005, G2-T0720..0723).

Normalizes event logs from Jira/ServiceNow/CI/CD, discovers observed process
paths, compares to designed flows, and reports deviations/bottlenecks.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from eoip.graph.store import GraphStore


@dataclass
class ProcessCase:
    case_id: str
    events: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"case_id": self.case_id, "events": self.events, "length": len(self.events)}


def extract_cases_from_graph(store: GraphStore, *, source_label: str = "WorkItem") -> list[ProcessCase]:
    """Extract process cases from graph event data.

    Each WorkItem/Incident/ChangeRequest is treated as a case.
    Its WorkItemChange/ProcessEvent children are the events.
    """
    cases: list[ProcessCase] = []
    entities = store.find_vertices(label=source_label, limit=10_000)

    for entity in entities:
        events: list[dict] = []

        edges = store.find_edges(out_v=entity["vid"], limit=500)
        for edge in edges:
            if edge["label"] not in ("HAS_CHANGE", "HAS_COMMENT"):
                continue
            target = store.get_vertex(edge["in_v"])
            if not target:
                continue
            events.append({
                "event_id": target["canonical_id"],
                "label": target["label"],
                "field": target["properties"].get("field_name", ""),
                "from_value": target["properties"].get("from_value", ""),
                "to_value": target["properties"].get("to_value", ""),
                "timestamp": target["properties"].get("created_at", ""),
                "actor": target["properties"].get("source_id", ""),
            })

        events.sort(key=lambda e: e.get("timestamp", ""))
        if events:
            cases.append(ProcessCase(case_id=entity["canonical_id"], events=events))

    return cases


def discover_process_paths(cases: list[ProcessCase]) -> dict:
    """Discover the observed process paths from case event data.

    Returns frequent paths and transition frequencies.
    """
    path_counter: Counter[tuple[str, ...]] = Counter()
    transition_counter: Counter[tuple[str, str]] = Counter()

    for case in cases:
        status_events = [e for e in case.events if e.get("field") == "status"]
        if not status_events:
            path = tuple(e.get("label", "event") for e in case.events)
        else:
            path = tuple(e["to_value"] for e in status_events if e.get("to_value"))

        if path:
            path_counter[path] += 1
            for i in range(len(path) - 1):
                transition_counter[(path[i], path[i + 1])] += 1

    paths = [
        {"path": list(p), "count": c, "frequency": c / len(cases) if cases else 0}
        for p, c in path_counter.most_common(20)
    ]

    transitions = [
        {"from": f, "to": t, "count": c}
        for (f, t), c in transition_counter.most_common(50)
    ]

    return {
        "total_cases": len(cases),
        "unique_paths": len(path_counter),
        "paths": paths,
        "transitions": transitions,
    }


def compare_to_designed_flow(
    observed_paths: dict,
    designed_steps: list[str],
) -> dict:
    """Compare observed process paths against a designed flow.

    Returns deviations: skipped steps, extra steps, rework loops, bottlenecks.
    """
    deviations: list[dict] = []
    designed_set = set(designed_steps)

    for path_info in observed_paths.get("paths", []):
        path = path_info["path"]
        path_set = set(path)

        skipped = [s for s in designed_steps if s not in path_set]
        if skipped:
            deviations.append({
                "type": "skipped_steps",
                "path": path,
                "skipped": skipped,
                "count": path_info["count"],
                "severity": "WARNING",
            })

        extra = [s for s in path if s not in designed_set]
        if extra:
            deviations.append({
                "type": "extra_steps",
                "path": path,
                "extra": extra,
                "count": path_info["count"],
                "severity": "INFO",
            })

        for i in range(len(path) - 1):
            for j in range(i + 2, len(path)):
                if path[i] == path[j]:
                    deviations.append({
                        "type": "rework_loop",
                        "path": path,
                        "loop_step": path[i],
                        "loop_span": j - i,
                        "count": path_info["count"],
                        "severity": "WARNING",
                    })
                    break

    bottlenecks: list[dict] = []
    transition_times: dict[str, list[float]] = defaultdict(list)
    for t in observed_paths.get("transitions", []):
        if t["count"] > len(observed_paths.get("paths", [])) * 0.5:
            bottlenecks.append({
                "from": t["from"],
                "to": t["to"],
                "count": t["count"],
                "is_bottleneck": True,
            })

    return {
        "designed_steps": designed_steps,
        "deviations": deviations,
        "deviation_count": len(deviations),
        "bottlenecks": bottlenecks,
        "conformance_rate": 1.0 - (len(deviations) / max(len(observed_paths.get("paths", [])), 1)),
    }


def deviation_report(store: GraphStore, designed_steps: list[str] | None = None) -> dict:
    """Full deviation report: extract cases, discover paths, compare to designed flow."""
    cases = extract_cases_from_graph(store)
    observed = discover_process_paths(cases)

    if designed_steps:
        comparison = compare_to_designed_flow(observed, designed_steps)
    else:
        comparison = {"designed_steps": [], "deviations": [], "deviation_count": 0, "bottlenecks": [], "conformance_rate": 1.0}

    return {
        "cases": [c.to_dict() for c in cases[:50]],
        "observed_paths": observed,
        "comparison": comparison,
    }

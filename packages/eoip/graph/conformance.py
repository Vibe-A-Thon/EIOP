"""Architecture conformance engine (G2-ARCHC-001..009, G2-T0710..0715).

Declarative architecture rule DSL, rule compiler to graph queries,
and conformance checker that reports violating paths.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

from eoip.graph.store import GraphStore
from eoip.ontology.manifest import VERTEX_LABELS


class RuleKind(str, Enum):
    MUST_NOT_DEPEND = "MUST_NOT_DEPEND"
    MUST_NOT_ACCESS = "MUST_NOT_ACCESS"
    MUST_HAVE = "MUST_HAVE"
    MUST_NOT_CROSS = "MUST_NOT_CROSS"


@dataclass
class ArchRule:
    id: str
    kind: RuleKind
    source: str
    target: str
    description: str = ""
    max_depth: int = 4
    severity: str = "ERROR"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "source": self.source,
            "target": self.target,
            "description": self.description,
            "max_depth": self.max_depth,
            "severity": self.severity,
        }


@dataclass
class ConformanceFinding:
    rule_id: str
    severity: str
    message: str
    violating_path: list[dict] = field(default_factory=list)
    source_file: str | None = None
    source_symbol: str | None = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "violating_path": self.violating_path,
            "source_file": self.source_file,
            "source_symbol": self.source_symbol,
        }


def parse_rules(dsl_text: str) -> list[ArchRule]:
    """Parse architecture rules from DSL text.

    Format:
        RULE <id>: <source> MUST_NOT_DEPEND <target> [SEVERITY <level>] [DEPTH <n>]
        RULE <id>: <source> MUST_NOT_ACCESS <target>
        RULE <id>: <source> MUST_HAVE <property/connection>
        RULE <id>: <source> MUST_NOT_CROSS <boundary>
    """
    rules: list[ArchRule] = []
    pattern = re.compile(
        r"RULE\s+(\S+)\s*:\s*(\S+)\s+(MUST_NOT_DEPEND|MUST_NOT_ACCESS|MUST_HAVE|MUST_NOT_CROSS)\s+(\S+)"
        r"(?:\s+SEVERITY\s+(\S+))?(?:\s+DEPTH\s+(\d+))?",
        re.IGNORECASE,
    )
    for match in pattern.finditer(dsl_text):
        rules.append(ArchRule(
            id=match.group(1),
            kind=RuleKind(match.group(3).upper()),
            source=match.group(2),
            target=match.group(4),
            severity=match.group(5) or "ERROR",
            max_depth=int(match.group(6)) if match.group(6) else 4,
        ))
    return rules


def compile_rule(rule: ArchRule, store: GraphStore) -> list[ConformanceFinding]:
    """Compile and execute a single architecture rule against the graph."""
    if rule.kind == RuleKind.MUST_NOT_DEPEND:
        return _check_must_not_depend(rule, store)
    elif rule.kind == RuleKind.MUST_NOT_ACCESS:
        return _check_must_not_access(rule, store)
    elif rule.kind == RuleKind.MUST_HAVE:
        return _check_must_have(rule, store)
    elif rule.kind == RuleKind.MUST_NOT_CROSS:
        return _check_must_not_cross(rule, store)
    return []


def _resolve_vertices(store: GraphStore, pattern: str) -> list[dict]:
    """Resolve a pattern to matching vertices (label, domain, or name glob)."""
    if pattern in VERTEX_LABELS:
        return store.find_vertices(label=pattern, limit=10_000)
    domain_vertices = [
        v for v in store.find_vertices(limit=10_000)
        if VERTEX_LABELS.get(v["label"], ("",))[0] == pattern
    ]
    if domain_vertices:
        return domain_vertices
    return [
        v for v in store.find_vertices(limit=10_000)
        if pattern.lower() in (v["properties"].get("name", "") or "").lower()
    ]


def _check_must_not_depend(rule: ArchRule, store: GraphStore) -> list[ConformanceFinding]:
    findings: list[ConformanceFinding] = []
    sources = _resolve_vertices(store, rule.source)
    targets = _resolve_vertices(store, rule.target)
    target_vids = {t["vid"] for t in targets}

    for src in sources:
        path = _find_path_to(store, src["vid"], target_vids, rule.max_depth)
        if path:
            findings.append(ConformanceFinding(
                rule_id=rule.id,
                severity=rule.severity,
                message=f"{rule.source} depends on {rule.target} via {len(path)}-hop path",
                violating_path=path,
                source_file=src["properties"].get("path"),
                source_symbol=src["properties"].get("qualified_name"),
            ))
    return findings


def _check_must_not_access(rule: ArchRule, store: GraphStore) -> list[ConformanceFinding]:
    """Direct-access check: flags a direct edge to the target (1 hop, any label).

    Unlike MUST_NOT_DEPEND (transitive reachability), MUST_NOT_ACCESS models
    a boundary that must never be crossed directly, even in one step.
    """
    findings: list[ConformanceFinding] = []
    sources = _resolve_vertices(store, rule.source)
    targets = _resolve_vertices(store, rule.target)
    target_vids = {t["vid"] for t in targets}
    for src in sources:
        for edge in store.edges_from(src["vid"], limit=500):
            if edge["in_v"] in target_vids:
                findings.append(ConformanceFinding(
                    rule_id=rule.id,
                    severity=rule.severity,
                    message=f"{rule.source} directly accesses {rule.target} via {edge['label']}",
                    violating_path=[src["canonical_id"], edge["label"], edge.get("in_cid") or edge["in_v"]],
                    source_file=src["properties"].get("path"),
                    source_symbol=src["properties"].get("qualified_name"),
                ))
    return findings


def _check_must_have(rule: ArchRule, store: GraphStore) -> list[ConformanceFinding]:
    findings: list[ConformanceFinding] = []
    sources = _resolve_vertices(store, rule.source)
    for src in sources:
        edges = store.find_edges(out_v=src["vid"], limit=500)
        in_edges = store.find_edges(in_v=src["vid"], limit=500)
        all_edges = edges + in_edges

        connected_labels = set()
        for e in all_edges:
            peer_vid = e["in_v"] if e["out_v"] == src["vid"] else e["out_v"]
            peer = store.get_vertex(peer_vid)
            if peer:
                connected_labels.add(peer["label"])

        has_prop = src["properties"].get(rule.target) is not None
        has_connection = rule.target in connected_labels

        if not has_prop and not has_connection:
            findings.append(ConformanceFinding(
                rule_id=rule.id,
                severity=rule.severity,
                message=f"{src['canonical_id']} ({rule.source}) missing required {rule.target}",
                source_file=src["properties"].get("path"),
            ))
    return findings


def _check_must_not_cross(rule: ArchRule, store: GraphStore) -> list[ConformanceFinding]:
    findings: list[ConformanceFinding] = []
    sources = _resolve_vertices(store, rule.source)
    for src in sources:
        src_domain = VERTEX_LABELS.get(src["label"], ("",))[0]
        edges = store.find_edges(out_v=src["vid"], limit=500)
        for e in edges:
            if e["label"] in ("BELONGS_TO_DOMAIN", "EVIDENCED_BY", "INGESTED_IN", "VALIDATED_BY"):
                continue
            target = store.get_vertex(e["in_v"])
            if not target:
                continue
            target_domain = VERTEX_LABELS.get(target["label"], ("",))[0]
            if target_domain == rule.target and src_domain != rule.target:
                findings.append(ConformanceFinding(
                    rule_id=rule.id,
                    severity=rule.severity,
                    message=f"{src['canonical_id']} crosses into {rule.target} domain via {e['label']}",
                    violating_path=[
                        {"vid": src["vid"], "label": src["label"], "canonical_id": src["canonical_id"]},
                        {"edge": e["label"]},
                        {"vid": target["vid"], "label": target["label"], "canonical_id": target["canonical_id"]},
                    ],
                ))
    return findings


def _find_path_to(store: GraphStore, start_vid: str, target_vids: set[str], max_depth: int) -> list[dict]:
    """BFS to find a path from start to any target vertex."""
    visited: set[str] = {start_vid}
    queue: list[tuple[str, list[dict]]] = [(start_vid, [])]

    for _ in range(max_depth):
        next_queue: list[tuple[str, list[dict]]] = []
        for vid, path in queue:
            edges = store.find_edges(out_v=vid, limit=200)
            for e in edges:
                if e["label"] in ("BELONGS_TO_DOMAIN", "EVIDENCED_BY", "INGESTED_IN", "VALIDATED_BY"):
                    continue
                if e["in_v"] in visited:
                    continue
                visited.add(e["in_v"])
                target = store.get_vertex(e["in_v"])
                if not target:
                    continue
                new_path = path + [
                    {"vid": vid, "edge": e["label"]},
                    {"vid": e["in_v"], "label": target["label"], "canonical_id": target["canonical_id"]},
                ]
                if e["in_v"] in target_vids:
                    return new_path
                next_queue.append((e["in_v"], new_path))
        queue = next_queue
        if not queue:
            break
    return []


def check_conformance(store: GraphStore, rules: list[ArchRule]) -> dict:
    """Run all architecture conformance rules and return findings."""
    all_findings: list[dict] = []
    for rule in rules:
        findings = compile_rule(rule, store)
        all_findings.extend(f.to_dict() for f in findings)

    errors = [f for f in all_findings if f["severity"] == "ERROR"]
    return {
        "rules_checked": len(rules),
        "findings": all_findings,
        "total_violations": len(all_findings),
        "errors": len(errors),
        "warnings": len(all_findings) - len(errors),
        "conformant": len(errors) == 0,
    }

"""KGR-G-017: PR-Level Cross-Repo Graph Impact Triage MCP Tools.

Provides `list_prs`, `get_pr_impact`, and `triage_prs` MCP tool
endpoints with risk scoring, ownership attribution, and reviewer
suggestion based on graph-derived code ownership and dependency data.
"""

from __future__ import annotations

import hashlib
import logging
import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from eoip.graph.store import GraphStore

log = logging.getLogger("eoip.agents.mcp_pr_tools")


class RiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    MINIMAL = "MINIMAL"


@dataclass
class PRFile:
    path: str
    change_type: str  # added, modified, deleted, renamed
    additions: int = 0
    deletions: int = 0
    old_path: str | None = None


@dataclass
class PullRequest:
    pr_id: str
    title: str
    author: str
    base_branch: str
    head_branch: str
    files: list[PRFile]
    repo_id: str
    created_at: float = 0.0
    labels: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class ImpactedEntity:
    canonical_id: str
    entity_type: str
    name: str
    impact_type: str  # direct_change, transitive_dependency, shared_owner
    risk_contribution: float = 0.0
    owner: str | None = None
    depth: int = 0


@dataclass
class PRImpactReport:
    pr_id: str
    risk_level: RiskLevel
    risk_score: float
    impacted_entities: list[ImpactedEntity]
    affected_services: list[str]
    suggested_reviewers: list[str]
    ownership_attribution: dict[str, list[str]]
    blast_radius: int
    summary: str = ""
    signals: dict[str, Any] = field(default_factory=dict)


@dataclass
class TriageResult:
    prs: list[PRImpactReport]
    high_risk_count: int = 0
    total_blast_radius: int = 0
    triage_duration_ms: int = 0


class PRImpactCalculator:
    """Calculates graph-based impact of a pull request by tracing file changes
    through the dependency graph to affected services and owners."""

    def __init__(self, store: GraphStore, *, max_depth: int = 4) -> None:
        self.store = store
        self.max_depth = max_depth

    def calculate(self, pr: PullRequest) -> PRImpactReport:
        impacted: list[ImpactedEntity] = []
        affected_services: set[str] = set()
        owners: dict[str, list[str]] = {}

        for f in pr.files:
            file_entities = self._find_entities_for_file(f.path, pr.repo_id)
            for entity in file_entities:
                impacted.append(ImpactedEntity(
                    canonical_id=entity.get("canonical_id", ""),
                    entity_type=str(entity.get("label", "CodeSymbol")),
                    name=str(entity.get("name", f.path)),
                    impact_type="direct_change",
                    depth=0,
                ))

            transitive = self._find_transitive_impact(file_entities, pr.repo_id)
            impacted.extend(transitive)

            file_owners = self._find_owners(f.path, pr.repo_id)
            if file_owners:
                owners[f.path] = file_owners

        for entity in impacted:
            service = self._find_owning_service(entity.canonical_id)
            if service:
                affected_services.add(service)

        risk_score = RiskScorer.score(pr, impacted, affected_services)
        risk_level = RiskScorer.classify(risk_score)
        reviewers = ReviewerSuggester.suggest(owners, pr.author, impacted)

        return PRImpactReport(
            pr_id=pr.pr_id,
            risk_level=risk_level,
            risk_score=risk_score,
            impacted_entities=impacted,
            affected_services=sorted(affected_services),
            suggested_reviewers=reviewers,
            ownership_attribution=owners,
            blast_radius=len(impacted),
            summary=self._build_summary(pr, risk_level, impacted, affected_services),
            signals=self._compute_signals(pr, impacted),
        )

    def _find_entities_for_file(self, path: str, repo_id: str) -> list[dict[str, Any]]:
        vertices = self.store.find_vertex_by_property("CodeSymbol", "path", path)
        return [dict(v) for v in vertices]

    def _find_transitive_impact(self, direct_entities: list[dict[str, Any]], repo_id: str) -> list[ImpactedEntity]:
        transitive: list[ImpactedEntity] = []
        visited: set[str] = set()
        queue: list[tuple[str, int]] = []

        for entity in direct_entities:
            cid = entity.get("canonical_id", "")
            if cid:
                queue.append((cid, 0))
                visited.add(cid)

        while queue:
            current_id, depth = queue.pop(0)
            if depth >= self.max_depth:
                continue

            try:
                edges = self.store.edges_to(
                    current_id,
                    labels=["DEPENDS_ON", "IMPORTS", "CALLS", "CROSS_REPO_DEPENDS_ON"],
                )
            except Exception:
                continue

            for edge in edges:
                dep_id = str(edge.get("out_v") or edge.get("out_cid", ""))
                if dep_id and dep_id not in visited:
                    visited.add(dep_id)
                    vertex = self.store.get_vertex(dep_id) or self.store.get_vertex_by_canonical_id(dep_id)
                    if vertex:
                        transitive.append(ImpactedEntity(
                            canonical_id=dep_id,
                            entity_type=str(vertex.get("label", "CodeSymbol")),
                            name=str(vertex.get("name", dep_id)),
                            impact_type="transitive_dependency",
                            depth=depth + 1,
                        ))
                        queue.append((dep_id, depth + 1))

        return transitive

    def _find_owners(self, path: str, repo_id: str) -> list[str]:
        owners: list[str] = []
        vertices = self.store.find_vertex_by_property("CodeSymbol", "path", path)
        for v in vertices:
            cid = str(v.get("canonical_id", ""))
            if not cid:
                continue
            owner_edges = self.store.edges_to(cid, labels=["OWNS", "MAINTAINS", "AUTHORED"])
            for edge in owner_edges:
                owner_id = str(edge.get("out_v") or edge.get("out_cid", ""))
                owner_vertex = self.store.get_vertex(owner_id) or self.store.get_vertex_by_canonical_id(owner_id)
                if owner_vertex:
                    owners.append(str(owner_vertex.get("name", owner_id)))
        return list(set(owners))

    def _find_owning_service(self, entity_id: str) -> str | None:
        try:
            edges = self.store.edges_from(entity_id, labels=["PART_OF", "BELONGS_TO", "DEPLOYED_IN"])
        except Exception:
            return None
        for edge in edges:
            target_id = str(edge.get("in_v") or edge.get("in_cid", ""))
            target = self.store.get_vertex(target_id) or self.store.get_vertex_by_canonical_id(target_id)
            if target and target.get("label") in ("Service", "Microservice", "Application"):
                return str(target.get("name", target_id))
        return None

    @staticmethod
    def _build_summary(
        pr: PullRequest, risk: RiskLevel, impacted: list[ImpactedEntity], services: set[str]
    ) -> str:
        parts = [f"PR #{pr.pr_id}: {risk.value} risk"]
        parts.append(f"{len(pr.files)} files changed")
        parts.append(f"{len(impacted)} entities impacted")
        if services:
            parts.append(f"services: {', '.join(sorted(services)[:5])}")
        return " | ".join(parts)

    @staticmethod
    def _compute_signals(pr: PullRequest, impacted: list[ImpactedEntity]) -> dict[str, Any]:
        total_additions = sum(f.additions for f in pr.files)
        total_deletions = sum(f.deletions for f in pr.files)
        return {
            "file_count": len(pr.files),
            "additions": total_additions,
            "deletions": total_deletions,
            "churn": total_additions + total_deletions,
            "blast_radius": len(impacted),
            "max_depth": max((e.depth for e in impacted), default=0),
            "direct_impacts": sum(1 for e in impacted if e.impact_type == "direct_change"),
            "transitive_impacts": sum(1 for e in impacted if e.impact_type == "transitive_dependency"),
        }


class RiskScorer:
    """Scores the risk of a PR based on file changes, blast radius, and service impact."""

    @staticmethod
    def score(pr: PullRequest, impacted: list[ImpactedEntity], services: set[str]) -> float:
        churn = sum(f.additions + f.deletions for f in pr.files)
        churn_score = min(1.0, math.log1p(churn) / 10.0)

        blast_score = min(1.0, len(impacted) / 50.0)

        service_score = min(1.0, len(services) / 5.0)

        delete_ratio = (
            sum(f.deletions for f in pr.files) / max(churn, 1)
        )
        file_count_score = min(1.0, len(pr.files) / 20.0)

        total = (
            churn_score * 0.2
            + blast_score * 0.3
            + service_score * 0.25
            + delete_ratio * 0.1
            + file_count_score * 0.15
        )
        return round(min(1.0, total), 3)

    @staticmethod
    def classify(score: float) -> RiskLevel:
        if score >= 0.8:
            return RiskLevel.CRITICAL
        if score >= 0.6:
            return RiskLevel.HIGH
        if score >= 0.4:
            return RiskLevel.MEDIUM
        if score >= 0.2:
            return RiskLevel.LOW
        return RiskLevel.MINIMAL


class ReviewerSuggester:
    """Suggests reviewers based on code ownership and expertise from the graph."""

    @staticmethod
    def suggest(
        ownership: dict[str, list[str]],
        author: str,
        impacted: list[ImpactedEntity],
        max_reviewers: int = 3,
    ) -> list[str]:
        owner_scores: dict[str, float] = {}
        for path, owners in ownership.items():
            for owner in owners:
                if owner == author:
                    continue
                owner_scores[owner] = owner_scores.get(owner, 0) + 1.0

        for entity in impacted:
            if entity.owner and entity.owner != author:
                weight = 1.0 / (entity.depth + 1)
                owner_scores[entity.owner] = owner_scores.get(entity.owner, 0) + weight

        ranked = sorted(owner_scores.items(), key=lambda x: x[1], reverse=True)
        return [name for name, _ in ranked[:max_reviewers]]


class MCPPRToolHandler:
    """MCP tool handler exposing list_prs, get_pr_impact, and triage_prs."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store
        self._calculator = PRImpactCalculator(store)

    def list_prs(self, args: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
        repo_id = args.get("repo_id", "")
        state = args.get("state", "open")
        limit = args.get("limit", 20)
        prs = self.store.find_vertices(
            label="PullRequest",
            filters={"repo_id": repo_id, "state": state},
            limit=limit,
        )
        return [dict(pr) for pr in prs], [f"vertex:{pr.get('canonical_id')}" for pr in prs]

    def get_pr_impact(self, args: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        pr_data = args.get("pr", {})
        pr = PullRequest(
            pr_id=pr_data.get("pr_id", ""),
            title=pr_data.get("title", ""),
            author=pr_data.get("author", ""),
            base_branch=pr_data.get("base_branch", "main"),
            head_branch=pr_data.get("head_branch", ""),
            repo_id=pr_data.get("repo_id", ""),
            files=[
                PRFile(
                    path=f.get("path", ""),
                    change_type=f.get("change_type", "modified"),
                    additions=f.get("additions", 0),
                    deletions=f.get("deletions", 0),
                )
                for f in pr_data.get("files", [])
            ],
        )
        report = self._calculator.calculate(pr)
        return {
            "pr_id": report.pr_id,
            "risk_level": report.risk_level.value,
            "risk_score": report.risk_score,
            "blast_radius": report.blast_radius,
            "affected_services": report.affected_services,
            "suggested_reviewers": report.suggested_reviewers,
            "summary": report.summary,
            "signals": report.signals,
        }, [f"pr:{report.pr_id}"]

    def triage_prs(self, args: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        started = time.monotonic()
        pr_list = args.get("prs", [])
        reports: list[PRImpactReport] = []
        for pr_data in pr_list:
            pr = PullRequest(
                pr_id=pr_data.get("pr_id", ""),
                title=pr_data.get("title", ""),
                author=pr_data.get("author", ""),
                base_branch=pr_data.get("base_branch", "main"),
                head_branch=pr_data.get("head_branch", ""),
                repo_id=pr_data.get("repo_id", ""),
                files=[
                    PRFile(
                        path=f.get("path", ""),
                        change_type=f.get("change_type", "modified"),
                        additions=f.get("additions", 0),
                        deletions=f.get("deletions", 0),
                    )
                    for f in pr_data.get("files", [])
                ],
            )
            reports.append(self._calculator.calculate(pr))

        reports.sort(key=lambda r: r.risk_score, reverse=True)
        elapsed = int((time.monotonic() - started) * 1000)

        triage = TriageResult(
            prs=reports,
            high_risk_count=sum(1 for r in reports if r.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH)),
            total_blast_radius=sum(r.blast_radius for r in reports),
            triage_duration_ms=elapsed,
        )
        return {
            "triage_count": len(triage.prs),
            "high_risk_count": triage.high_risk_count,
            "total_blast_radius": triage.total_blast_radius,
            "duration_ms": triage.triage_duration_ms,
            "ranked_prs": [
                {
                    "pr_id": r.pr_id,
                    "risk_level": r.risk_level.value,
                    "risk_score": r.risk_score,
                    "blast_radius": r.blast_radius,
                    "summary": r.summary,
                }
                for r in triage.prs
            ],
        }, [f"triage:{len(reports)}"]

"""Co-change coupling edges from commit histories.

Purely deterministic: from a stream of commits ``{commit_id, files[]}``,
count pairwise co-occurrence, then emit scored ``CO_CHANGED`` edge proposals
for pairs meeting support/confidence thresholds. Confidence is the standard
association-rule confidence max(|A∩B|/|A|, |A∩B|/|B|); lift is recorded as
evidence. LLM hooks are not required; if a caller supplies a hook callable it
is applied to proposals only and its absence is a no-op.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from itertools import combinations

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import GraphDelta, ProposedEdge

ScoringHook = Callable[[ProposedEdge], ProposedEdge | None]
"""Optional post-scoring hook; return None to drop a proposal (graceful fallback when absent)."""


class CoChangeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_support: int = Field(default=2, ge=1)
    min_confidence: float = Field(default=0.2, ge=0.0, le=1.0)
    min_files_per_commit: int = Field(default=2, ge=2)
    max_files_per_commit: int = Field(default=200, ge=2)
    top_k: int = Field(default=1000, ge=1)


def build_cochange_edges(
    commits: Iterable[dict],
    config: CoChangeConfig | None = None,
    hook: ScoringHook | None = None,
) -> GraphDelta:
    """Score file-pair co-change edges from commit history.

    ``commits`` items: ``{"commit_id": str, "files": [str, ...]}``.
    Commits with fewer than ``min_files_per_commit`` or more than
    ``max_files_per_commit`` files are skipped (merge-commit noise guard).
    """
    cfg = config or CoChangeConfig()
    pair_counts: dict[tuple[str, str], int] = {}
    file_counts: dict[str, int] = {}
    commit_count = 0

    for commit in commits:
        files = sorted({f for f in (commit.get("files") or []) if f})
        if not (cfg.min_files_per_commit <= len(files) <= cfg.max_files_per_commit):
            continue
        commit_count += 1
        for f in files:
            file_counts[f] = file_counts.get(f, 0) + 1
        for a, b in combinations(files, 2):
            pair_counts[(a, b)] = pair_counts.get((a, b), 0) + 1

    proposals: list[ProposedEdge] = []
    for (a, b), count in sorted(pair_counts.items()):
        if count < cfg.min_support:
            continue
        support_a, support_b = file_counts[a], file_counts[b]
        confidence = count / min(support_a, support_b)
        if confidence < cfg.min_confidence:
            continue
        expected = (support_a * support_b) / max(commit_count, 1)
        lift = count / expected if expected else 0.0
        edge = ProposedEdge.make(
            "CO_CHANGED",
            a,
            b,
            score=confidence,
            method="co-change:pairwise",
            support=count,
            confidence=round(confidence, 6),
            lift=round(lift, 6),
            support_a=support_a,
            support_b=support_b,
        )
        if hook is not None:
            edge = hook(edge)  # optional hook; graceful fallback when None
            if edge is None:
                continue
        proposals.append(edge)

    proposals.sort(key=lambda e: (-e.score, e.from_id, e.to_id))
    proposals = proposals[: cfg.top_k]
    return GraphDelta.make(
        "cochange",
        repr((commit_count, sorted(cfg.model_dump().items()))),
        edges=proposals,
        notes=[f"commits_considered={commit_count}"],
    )

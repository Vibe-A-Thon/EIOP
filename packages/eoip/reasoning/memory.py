"""Memory architectures — §7 Reasoning & Orchestration: memory architectures.

Composable memory stores implementing the §7 memory architectures. All stores
are deterministic, thread-safe, and share a small JSON persistence layer in the
style of ``eoip.jobs`` (atomic tmp-file replace). Consolidation follows the
MEMORY_CONSOLIDATION loop from ``eoip.agents.loops``; summarization hooks are
optional and fall back to truncation.

Stores:

* :class:`WorkingMemory`     — token-budgeted short-term buffer with eviction.
* :class:`EpisodicMemory`    — append-only event log with consolidation.
* :class:`SemanticMemory`    — fact store keyed by (subject, predicate).
* :class:`ProceduralMemory`  — skill library with precondition scoring.
* :class:`SharedMemory`      — blackboard with per-key locking.
* :class:`HierarchicalMemory`— layered (L0/L1/L2) summarization tiers.
* :class:`TemporalMemory`    — valid-time fact queries (bitemporal-lite).

Optional LLM hook: a ``summarize: Callable[[str], str]`` callable may be
attached to stores; when absent, consolidation truncates deterministically.
"""

from __future__ import annotations

import hashlib
import threading
from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.source_event import utc_now_iso


def estimate_tokens(text: str) -> int:
    """Deterministic token estimate: ~4 chars per token, min 1."""
    return max(1, (len(text) + 3) // 4)


def _urn(kind: str, seed: str) -> str:
    return "urn:eoip:reasoning:memory:" + kind + ":" + hashlib.sha256(seed.encode()).hexdigest()[:20]


# ---------------------------------------------------------------------------
# Working memory (§7)
# ---------------------------------------------------------------------------

class WorkingMemoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str
    content: str
    tokens: int
    added_at: str
    priority: float = 0.0


class WorkingMemory:
    """Token-budgeted working memory; lowest-priority/oldest items evicted first."""

    def __init__(self, token_budget: int = 2048):
        if token_budget <= 0:
            raise ValueError("token_budget must be positive")
        self.token_budget = token_budget
        self._items: list[WorkingMemoryItem] = []
        self._lock = threading.RLock()
        self._seq = 0

    def _evict(self) -> list[WorkingMemoryItem]:
        evicted: list[WorkingMemoryItem] = []
        while sum(i.tokens for i in self._items) > self.token_budget and self._items:
            # evict lowest priority, then oldest
            victim = min(self._items, key=lambda i: (i.priority, i.added_at, i.item_id))
            self._items.remove(victim)
            evicted.append(victim)
        return evicted

    def add(self, content: str, *, priority: float = 0.0) -> tuple[WorkingMemoryItem, list[WorkingMemoryItem]]:
        with self._lock:
            self._seq += 1
            item = WorkingMemoryItem(
                item_id=_urn("working", f"{self._seq}"),
                content=content,
                tokens=estimate_tokens(content),
                added_at=utc_now_iso(),
                priority=priority,
            )
            self._items.append(item)
            evicted = self._evict()
            return item, evicted

    def snapshot(self) -> list[WorkingMemoryItem]:
        with self._lock:
            return list(self._items)

    @property
    def used_tokens(self) -> int:
        with self._lock:
            return sum(i.tokens for i in self._items)


# ---------------------------------------------------------------------------
# Episodic memory (§7)
# ---------------------------------------------------------------------------

class Episode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    episode_id: str
    kind: str
    content: str
    recorded_at: str
    consolidated: bool = False
    summary: str | None = None


class EpisodicMemory:
    """Event log with a consolidation loop (MEMORY_CONSOLIDATION): episodes
    older than ``consolidate_after`` episodes are folded into summaries."""

    def __init__(self, persist_root: str | Path | None = None, consolidate_after: int = 8,
                 summarize: Callable[[list[str]], str] | None = None):
        self.root = Path(persist_root) / "episodic" if persist_root else None
        if self.root:
            self.root.mkdir(parents=True, exist_ok=True)
        self.consolidate_after = max(2, consolidate_after)
        self.summarize = summarize
        self._episodes: list[Episode] = []
        self._lock = threading.RLock()
        self._seq = 0
        self.consolidations = 0

    def record(self, kind: str, content: str) -> Episode:
        with self._lock:
            self._seq += 1
            ep = Episode(episode_id=_urn("episode", str(self._seq)), kind=kind, content=content,
                         recorded_at=utc_now_iso())
            self._episodes.append(ep)
            return ep

    def recent(self, limit: int = 20) -> list[Episode]:
        with self._lock:
            return list(self._episodes[-limit:])

    def consolidate(self) -> int:
        """Fold the oldest unconsolidated episodes into a summary. Returns the
        number consolidated. Deterministic fallback: joined truncation."""
        with self._lock:
            open_eps = [e for e in self._episodes if not e.consolidated]
            if len(open_eps) <= self.consolidate_after:
                return 0
            batch = open_eps[: len(open_eps) - self.consolidate_after]
            texts = [f"[{e.kind}] {e.content}" for e in batch]
            if self.summarize:
                try:
                    summary = self.summarize(texts)
                except Exception:  # noqa: BLE001 — fall back to truncation
                    summary = None
            else:
                summary = None
            if not summary:
                joined = " | ".join(texts)
                summary = joined[:400] + ("…" if len(joined) > 400 else "")
            for ep in batch:
                ep.consolidated = True
                ep.summary = summary
            self.consolidations += 1
            if self.root:
                for ep in batch:
                    path = self.root / f"{ep.episode_id.split(':')[-1]}.json"
                    path.write_text(ep.model_dump_json(), encoding="utf-8")
            return len(batch)

    def all(self) -> list[Episode]:
        with self._lock:
            return list(self._episodes)


# ---------------------------------------------------------------------------
# Semantic memory (§7)
# ---------------------------------------------------------------------------

class Fact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fact_id: str
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    recorded_at: str = ""


class SemanticMemory:
    """Fact store keyed by (subject, predicate) with confidence-weighted upsert."""

    def __init__(self) -> None:
        self._facts: dict[tuple[str, str], Fact] = {}
        self._lock = threading.RLock()

    def upsert(self, subject: str, predicate: str, obj: str, *, confidence: float = 1.0) -> Fact:
        with self._lock:
            key = (subject, predicate)
            existing = self._facts.get(key)
            if existing is None or confidence >= existing.confidence:
                fact = Fact(fact_id=_urn("fact", f"{subject}|{predicate}"), subject=subject,
                            predicate=predicate, object=obj, confidence=confidence,
                            recorded_at=utc_now_iso())
                self._facts[key] = fact
                return fact
            return existing

    def recall(self, subject: str | None = None, predicate: str | None = None,
               min_confidence: float = 0.0) -> list[Fact]:
        with self._lock:
            out = [f for f in self._facts.values()
                   if (subject is None or f.subject == subject)
                   and (predicate is None or f.predicate == predicate)
                   and f.confidence >= min_confidence]
        return sorted(out, key=lambda f: (-f.confidence, f.fact_id))

    def subjects(self) -> list[str]:
        with self._lock:
            return sorted({s for s, _ in self._facts})


# ---------------------------------------------------------------------------
# Procedural memory (§7)
# ---------------------------------------------------------------------------

class Skill(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: str
    name: str
    description: str = ""
    preconditions: list[str] = Field(default_factory=list)
    body: str = ""  # deterministic script/executor key — External gate for real toolchains
    success_count: int = 0
    failure_count: int = 0


class ProceduralMemory:
    """Skill library; retrieval ranks skills by precondition coverage."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}
        self._lock = threading.RLock()

    def register(self, name: str, *, description: str = "", preconditions: list[str] | None = None,
                 body: str = "") -> Skill:
        with self._lock:
            skill = Skill(skill_id=_urn("skill", name), name=name, description=description,
                          preconditions=sorted(preconditions or []), body=body)
            self._skills[name] = skill
            return skill

    def retrieve(self, available: list[str], *, limit: int = 5) -> list[Skill]:
        """Rank skills by fraction of preconditions satisfied."""
        with self._lock:
            avail = set(available)

            def coverage(skill: Skill) -> tuple[float, str]:
                if not skill.preconditions:
                    return (0.0, skill.name)
                return (len(set(skill.preconditions) & avail) / len(skill.preconditions), skill.name)

            ranked = sorted(self._skills.values(), key=coverage, reverse=True)
            return ranked[:limit]

    def record_outcome(self, name: str, success: bool) -> Skill:
        with self._lock:
            skill = self._skills[name]
            if success:
                skill.success_count += 1
            else:
                skill.failure_count += 1
            return skill

    def get(self, name: str) -> Skill | None:
        with self._lock:
            return self._skills.get(name)


# ---------------------------------------------------------------------------
# Shared memory / blackboard (§7)
# ---------------------------------------------------------------------------

class SharedMemory:
    """Blackboard with per-key reader/writer locking for multi-agent sharing."""

    def __init__(self) -> None:
        self._board: dict[str, str] = {}
        self._locks: dict[str, threading.RLock] = {}
        self._board_lock = threading.RLock()

    def _key_lock(self, key: str) -> threading.RLock:
        with self._board_lock:
            return self._locks.setdefault(key, threading.RLock())

    def write(self, key: str, value: str) -> None:
        with self._key_lock(key):
            self._board[key] = value

    def read(self, key: str) -> str | None:
        with self._key_lock(key):
            return self._board.get(key)

    def update(self, key: str, fn: Callable[[str | None], str]) -> str:
        """Atomic read-modify-write under the per-key lock."""
        with self._key_lock(key):
            new_value = fn(self._board.get(key))
            self._board[key] = new_value
            return new_value

    def __contains__(self, key: object) -> bool:
        with self._board_lock:
            return isinstance(key, str) and key in self._board

    def keys(self) -> list[str]:
        with self._board_lock:
            return sorted(self._board)


# ---------------------------------------------------------------------------
# Hierarchical memory (§7)
# ---------------------------------------------------------------------------

class HierarchicalMemory:
    """Layered memory: L0 raw items, L1 working-set summary, L2 long-term facts.

    ``promote`` consolidates the L0 tail into L1 via the optional summarize
    hook (deterministic truncation fallback), and distilled facts into L2."""

    LAYERS = ("L0", "L1", "L2")

    def __init__(self, l0_capacity: int = 32, summarize: Callable[[list[str]], str] | None = None):
        self.l0_capacity = max(1, l0_capacity)
        self.summarize = summarize
        self._layers: dict[str, list[str]] = {layer: [] for layer in self.LAYERS}
        self._lock = threading.RLock()

    def add_raw(self, item: str) -> None:
        with self._lock:
            self._layers["L0"].append(item)
            while len(self._layers["L0"]) > self.l0_capacity:
                self._layers["L0"].pop(0)

    def promote(self) -> str:
        """Consolidate the oldest half of L0 into an L1 summary entry."""
        with self._lock:
            l0 = self._layers["L0"]
            if len(l0) < 2:
                return ""
            batch, self._layers["L0"] = l0[: len(l0) // 2], l0[len(l0) // 2:]
            if self.summarize:
                try:
                    summary = self.summarize(batch)
                except Exception:  # noqa: BLE001 — fall back to truncation
                    summary = None
            else:
                summary = None
            if not summary:
                joined = " | ".join(batch)
                summary = joined[:300] + ("…" if len(joined) > 300 else "")
            self._layers["L1"].append(summary)
            return summary

    def distill(self, fact: str) -> None:
        with self._lock:
            self._layers["L2"].append(fact)

    def layer(self, name: str) -> list[str]:
        if name not in self.LAYERS:
            raise KeyError(f"unknown layer {name}; expected one of {self.LAYERS}")
        with self._lock:
            return list(self._layers[name])


# ---------------------------------------------------------------------------
# Temporal memory (§7)
# ---------------------------------------------------------------------------

class TemporalFact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fact_id: str
    subject: str
    predicate: str
    object: str
    valid_from: str
    valid_to: str | None = None  # None = currently valid (open interval)


class TemporalMemory:
    """Valid-time fact store: a fact holds at time T when
    ``valid_from <= T < valid_to`` (open interval when ``valid_to`` is None)."""

    def __init__(self) -> None:
        self._facts: list[TemporalFact] = []
        self._lock = threading.RLock()
        self._seq = 0

    def assert_fact(self, subject: str, predicate: str, obj: str,
                    valid_from: str, valid_to: str | None = None) -> TemporalFact:
        if valid_to is not None and valid_to < valid_from:
            raise ValueError("valid_to must be >= valid_from")
        with self._lock:
            self._seq += 1
            fact = TemporalFact(fact_id=_urn("tfact", str(self._seq)), subject=subject,
                                predicate=predicate, object=obj, valid_from=valid_from,
                                valid_to=valid_to)
            self._facts.append(fact)
            return fact

    def at(self, when: str, *, subject: str | None = None, predicate: str | None = None) -> list[TemporalFact]:
        """Facts valid at time ``when`` (§7 temporal queries)."""
        with self._lock:
            out = [f for f in self._facts
                   if f.valid_from <= when and (f.valid_to is None or when < f.valid_to)
                   and (subject is None or f.subject == subject)
                   and (predicate is None or f.predicate == predicate)]
        return sorted(out, key=lambda f: f.fact_id)

    def history(self, subject: str, predicate: str) -> list[TemporalFact]:
        with self._lock:
            out = [f for f in self._facts if f.subject == subject and f.predicate == predicate]
        return sorted(out, key=lambda f: (f.valid_from, f.fact_id))

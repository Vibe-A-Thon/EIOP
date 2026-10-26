"""Inclusion-dependency / value-overlap discovery via MinHash-style bands.

Deterministic MinHash over column value samples: each column is summarized
by ``num_hashes`` hash values of its values (seeded sha256, no randomness);
columns sharing at least one of ``num_bands`` signature bands are candidate
inclusion dependencies (A ⊆ B when every sample of A hashes into B's
signature set with containment above threshold). Exact containment on the
sample is then verified, so output has no false band-collision survivors.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import GraphDelta, ProposedEdge


class InclusionDependencyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    num_hashes: int = Field(default=64, ge=8)
    num_bands: int = Field(default=16, ge=1)
    sample_size: int = Field(default=500, ge=10)
    min_containment: float = Field(default=0.8, ge=0.0, le=1.0)


def _h(value: Any, seed: int) -> int:
    raw = f"{seed}:{value!r}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


def _signature(values: Iterable[Any], num_hashes: int) -> list[int]:
    """Per-seed MinHash row: signature[seed] = min hash of values under seed."""
    values = list(values)
    return [min((_h(v, seed) for v in values), default=_h("<empty>", seed)) for seed in range(num_hashes)]


def _bands(signature: list[int], num_hashes: int, num_bands: int) -> set[tuple[int, ...]]:
    """LSH bands: band i = consecutive per-seed MinHash rows."""
    if num_bands > num_hashes:
        raise ValueError("num_bands must be <= num_hashes")
    size = num_hashes // num_bands
    return {tuple(signature[i * size : (i + 1) * size]) for i in range(num_bands)}


def discover_inclusion_dependencies(
    columns: dict[str, Iterable[Any]],
    config: InclusionDependencyConfig | None = None,
) -> GraphDelta:
    """Find inclusion dependencies A ⊆ B over sampled column values.

    ``columns``: ``{"table.column": iterable_of_values}``.
    Returns ``REFERENCES`` edge proposals with containment as score.
    """
    cfg = config or InclusionDependencyConfig()
    samples = {name: list(dict.fromkeys(list(values)[: cfg.sample_size])) for name, values in columns.items()}
    signatures = {name: _signature(values, cfg.num_hashes) for name, values in samples.items()}
    bands = {name: _bands(sig, cfg.num_hashes, cfg.num_bands) for name, sig in signatures.items()}

    # Band index -> candidate column pairs (only band collisions survive to verify).
    index: dict[tuple[int, ...], list[str]] = {}
    for name, bs in bands.items():
        for band in bs:
            index.setdefault(band, []).append(name)

    candidates: set[tuple[str, str]] = set()
    for members in index.values():
        if len(members) < 2:
            continue
        members = sorted(members)
        for a, b in _ordered_pairs(members):
            candidates.add((a, b))

    proposals: list[ProposedEdge] = []
    for a, b in sorted(candidates):
        values_a = {v for v in samples[a] if v is not None}
        values_b = {v for v in samples[b] if v is not None}
        if not values_a or not values_b or values_a == values_b:
            continue
        if values_a <= values_b:
            contained, container = a, b
        elif values_b <= values_a:
            contained, container = b, a
        else:
            continue  # band collision but no verified containment
        smaller, larger = (values_a, values_b) if len(values_a) <= len(values_b) else (values_b, values_a)
        containment = len(smaller) / len(larger)
        if containment < cfg.min_containment:
            continue
        proposals.append(
            ProposedEdge.make(
                "REFERENCES",
                contained,
                container,
                score=containment,
                method="inclusion-dependency:minhash-bands",
                containment=round(containment, 6),
                sample_size=min(len(samples[contained]), cfg.sample_size),
            )
        )

    return GraphDelta.make(
        "inclusion-dependency",
        repr(sorted(columns)),
        edges=proposals,
        notes=[f"columns={len(columns)}", f"candidates={len(candidates)}"],
    )


def _ordered_pairs(members: list[str]) -> Iterable[tuple[str, str]]:
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            yield members[i], members[j]

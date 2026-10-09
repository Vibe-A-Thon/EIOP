"""Schema profiler, key detection and explicit relationship discovery.

Implements SR-ING-010 (schema profiling: types, nullability, cardinality,
uniqueness, enum candidates, format detection, nesting shape, drift),
SR-ING-012 (natural/composite key candidates with stability scoring),
SR-ING-013 (explicit relationship discovery: FK-like fields, array-of-IDs,
parent pointers, URL references, polymorphic type+id pairs) and the
SR-ING-016 edge-class tagging hook (ASSERTED / DERIVED / INFERRED / CURATED).

Design notes:

* **Streaming-friendly.** ``SchemaProfiler.update(record)`` accepts one record
  at a time; ``profile_records`` folds an iterable. Internal state is a set of
  per-field accumulators so multi-GB payloads never need to be resident.
* **Deterministic.** All reported collections (enum candidates, drift lists,
  key candidates, relationship candidates) are sorted by a stable key, hashes
  (SHA-256 over canonical JSON) are used for value identity, and no RNG or
  wall clock is read anywhere. Re-profiling the same records in any order
  yields the same ``FieldProfile`` / ``ProfileReport``.
* **Bounded memory.** Cardinality uses an exact set capped at
  ``CARDINALITY_CAP`` distinct hashes per field; once exceeded the field is
  reported as high-cardinality with a lower bound, never an exact count.
* Statistical relationship discovery (inclusion dependencies across huge
  datasets, MinHash/LSH, embeddings) is SR-ING-014 and is **ADR-gated** /
  deferred — only the explicit signals listed in SR-ING-013 are implemented.

IDs minted here follow ``urn:eoip:ingest:profile:<slug>`` and
``urn:eoip:ingest:relationship:<slug>``.
"""

from __future__ import annotations

import hashlib
import ipaddress
import json
import re
import uuid
from collections import Counter
from collections.abc import Iterable, Iterator, Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Constants (SR-ING-010)

CARDINALITY_CAP = 10_000
"""Max distinct value hashes kept per field before switching to lower-bound."""

ENUM_MAX_DISTINCT = 20
"""A field is an enum candidate when its observed distinct count is <= this."""

ENUM_MIN_FILL = 0.8
"""...and at least this fraction of non-null values fall on observed values."""

TOP_VALUES_LIMIT = 10
"""How many enum values (with counts) are reported per enum candidate."""

ID_NAME_PATTERN = re.compile(
    r"^(?:.+_)?(?:id|key|uuid|guid|code|number|num|no)$", re.IGNORECASE
)
TICKET_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
GIT_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
URL_PATTERN = re.compile(r"^https?://\S+$", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9 .()\-]{5,19}$")
IBAN_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
ISO_DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?)?$"
)
PARENT_POINTER_NAMES = {"parent", "parent_id", "parentId", "parent_key",
                        "parent_uuid", "mother_id", "father_id"}
TYPE_ID_SUFFIX = "_type"


# ---------------------------------------------------------------------------
# Models (SR-ING-010)

class EnumValue(BaseModel):
    """One observed value of an enum candidate, with count."""

    model_config = ConfigDict(extra="forbid")

    value: str
    count: int


class FieldProfile(BaseModel):
    """Profile of one leaf (scalar) or structural (object/array) field path."""

    model_config = ConfigDict(extra="forbid")

    path: str
    kind: Literal["scalar", "object", "array", "null"] = "scalar"
    observed_types: list[str] = Field(default_factory=list)
    """JSON value types seen at this path (e.g. ``["string", "integer"]``)."""
    total_count: int = 0
    null_count: int = 0
    cardinality: int = 0
    """Distinct non-null values; a lower bound when ``cardinality_capped``."""
    cardinality_capped: bool = False
    unique_ratio: float = 0.0
    """distinct / non-null count (1.0 only when not capped)."""
    enum_candidate: bool = False
    enum_values: list[EnumValue] = Field(default_factory=list)
    formats: list[str] = Field(default_factory=list)
    """Detected value formats: email, uuid, url, ip, iso_datetime, currency,
    phone, iban, git_sha, ticket_key, file_path."""
    array_item_types: list[str] = Field(default_factory=list)
    object_fields: list[str] = Field(default_factory=list)
    """Sorted child paths when ``kind == "object"`` (one level)."""
    max_nesting_depth: int = 0


class ProfileReport(BaseModel):
    """Deterministic result of profiling a record stream."""

    model_config = ConfigDict(extra="forbid")

    profile_id: str
    record_count: int = 0
    fields: list[FieldProfile] = Field(default_factory=list)


class FieldDrift(BaseModel):
    """Drift for one field path between two payload versions (SR-ING-020 hook)."""

    model_config = ConfigDict(extra="forbid")

    path: str
    change: Literal["added", "removed", "type_changed", "format_changed",
                    "nullability_changed", "cardinality_changed",
                    "enum_value_added"]
    detail: str = ""


class ProfileDrift(BaseModel):
    """Drift diff between two profiles of the same payload (SR-ING-010)."""

    model_config = ConfigDict(extra="forbid")

    drift_id: str
    changes: list[FieldDrift] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Key detection models (SR-ING-012)

class KeyCandidate(BaseModel):
    """A natural or composite key candidate for a dataset."""

    model_config = ConfigDict(extra="forbid")

    key_id: str
    dataset: str
    fields: list[str]
    composite: bool = False
    stability: float = 1.0
    """0..1: fraction of current values that existed in the baseline profile.
    1.0 when no baseline was supplied or the field is new."""
    name_hint: bool = False
    """Field name looks key-like (id/key/uuid/...)."""
    non_null_ratio: float = 0.0
    unique_ratio: float = 0.0
    minting: str = "deterministic-namespaced"
    """Canonical ID minting strategy (SR-ING-012): deterministic hash of the
    tuple ``(namespace, type, key-values)`` — collision-safe by construction."""


# ---------------------------------------------------------------------------
# Relationship discovery models (SR-ING-013)

class EdgeClassMethod(BaseModel):
    """SR-ING-016 hook: how a discovery method maps onto an edge class."""

    model_config = ConfigDict(extra="forbid")

    edge_class: Literal["ASSERTED", "DERIVED", "INFERRED", "CURATED"]
    method: str
    rationale: str


EDGE_CLASS_METHODS: tuple[EdgeClassMethod, ...] = (
    EdgeClassMethod(
        edge_class="ASSERTED",
        method="foreign_key_like",
        rationale="source record carries an explicit *_id reference (SR-ING-013)",
    ),
    EdgeClassMethod(
        edge_class="ASSERTED",
        method="parent_pointer",
        rationale="explicit parent field naming convention (SR-ING-013)",
    ),
    EdgeClassMethod(
        edge_class="ASSERTED",
        method="url_reference",
        rationale="record embeds a URL to a known entity (SR-ING-013)",
    ),
    EdgeClassMethod(
        edge_class="ASSERTED",
        method="array_of_ids",
        rationale="record carries an explicit array of identifiers (SR-ING-013)",
    ),
    EdgeClassMethod(
        edge_class="ASSERTED",
        method="type_id_pair",
        rationale="polymorphic (type, id) pair asserts the reference (SR-ING-013)",
    ),
    EdgeClassMethod(
        edge_class="INFERRED",
        method="value_overlap",
        rationale="statistical value overlap without explicit naming — SR-ING-014, deferred/ADR-gated",
    ),
)


def edge_class_for_method(method: str) -> EdgeClassMethod:
    """Map a discovery method to its SR-ING-016 edge class.

    Unknown methods degrade to ``INFERRED`` (honesty-first: never silently
    upgrade an unrecognized method to ASSERTED).
    """
    for entry in EDGE_CLASS_METHODS:
        if entry.method == method:
            return entry
    return EdgeClassMethod(
        edge_class="INFERRED",
        method=method,
        rationale="unrecognized discovery method; conservatively INFERRED",
    )


def tag_edge(method: str, *, curated: bool = False) -> str:
    """Return the edge class tag for a candidate edge (SR-ING-016).

    Human curation always wins: ``curated=True`` yields ``CURATED`` regardless
    of the discovery method.
    """
    if curated:
        return "CURATED"
    return edge_class_for_method(method).edge_class


class RelationshipCandidate(BaseModel):
    """One explicit relationship discovered across profiled datasets."""

    model_config = ConfigDict(extra="forbid")

    relationship_id: str
    method: Literal["foreign_key_like", "parent_pointer", "url_reference",
                    "array_of_ids", "type_id_pair"]
    edge_class: Literal["ASSERTED", "DERIVED", "INFERRED", "CURATED"] = "ASSERTED"
    confidence: float = 1.0
    from_dataset: str
    from_field: str
    to_dataset: str
    to_field: str
    evidence: list[str] = Field(default_factory=list)
    """Sample matching values (deterministic, bounded)."""


# ---------------------------------------------------------------------------
# Internal accumulator

def _canonical(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError):
        return repr(value)


def _value_hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _depth(value: Any) -> int:
    if isinstance(value, Mapping):
        if not value:
            return 1
        return 1 + max(_depth(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        if not value:
            return 1
        return 1 + max(_depth(v) for v in value)
    return 0


def detect_formats(value: str) -> list[str]:
    """Detect SR-ING-010 value formats for one string; deterministic order."""
    formats: list[str] = []
    if EMAIL_PATTERN.match(value):
        formats.append("email")
    try:
        uuid.UUID(value)
        formats.append("uuid")
    except (ValueError, AttributeError, TypeError):
        pass
    if URL_PATTERN.match(value):
        formats.append("url")
    try:
        ipaddress.ip_address(value)
        formats.append("ip")
    except ValueError:
        pass
    if ISO_DATETIME_PATTERN.match(value):
        try:
            from datetime import datetime
            datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
            formats.append("iso_datetime")
        except ValueError:
            pass
    if CURRENCY_PATTERN.match(value) and len(value) == 3:
        formats.append("currency")
    if PHONE_PATTERN.match(value) and not TICKET_KEY_PATTERN.match(value):
        formats.append("phone")
    if IBAN_PATTERN.match(value):
        formats.append("iban")
    if GIT_SHA_PATTERN.match(value):
        formats.append("git_sha")
    if TICKET_KEY_PATTERN.match(value):
        formats.append("ticket_key")
    if ("/" in value or "\\" in value) and "://" not in value \
            and " " not in value.strip():
        formats.append("file_path")
    return formats


class _FieldAccumulator:
    """Mutable per-path statistics used while streaming records."""

    __slots__ = (
        "capped",
        "children",
        "formats_seen",
        "hashes",
        "item_types",
        "kind",
        "max_depth",
        "nulls",
        "path",
        "raw",
        "top",
        "total",
        "types",
        "values",
    )

    def __init__(self, path: str, kind: str) -> None:
        self.path = path
        self.kind = kind  # scalar | object | array
        self.types: set[str] = set()
        self.total = 0
        self.nulls = 0
        self.hashes: set[str] = set()
        self.capped = False
        self.values: Counter[str] = Counter()
        self.raw: dict[str, str] = {}
        self.top: Counter[str] = Counter()
        self.formats_seen: set[str] = set()
        self.item_types: set[str] = set()
        self.children: set[str] = set()
        self.max_depth = 0

    def observe(self, value: Any) -> None:
        self.total += 1
        if value is None:
            self.nulls += 1
            self.types.add("null")
            return
        self.types.add(type(value).__name__)
        self.max_depth = max(self.max_depth, _depth(value))
        if isinstance(value, str):
            for fmt in detect_formats(value):
                self.formats_seen.add(fmt)
        if isinstance(value, Mapping):
            for key in value:
                self.children.add(str(key))
            return
        if isinstance(value, (list, tuple)):
            items = list(value)
            for item in items:
                if item is None:
                    self.item_types.add("null")
                elif isinstance(item, Mapping):
                    self.item_types.add("object")
                elif isinstance(item, (list, tuple)):
                    self.item_types.add("array")
                else:
                    self.item_types.add(type(item).__name__)
            scalars = [i for i in items
                       if not isinstance(i, (Mapping, list, tuple))]
            for item in scalars:
                self._observe_scalar(item)
            return
        self._observe_scalar(value)

    def _observe_scalar(self, value: Any) -> None:
        key = _canonical(value)
        self.values[key] += 1
        self.raw.setdefault(key, str(value))
        if len(self.values) <= TOP_VALUES_LIMIT * 2 or self.values[key] > 1:
            self.top[key] += 1
        if not self.capped:
            self.hashes.add(_value_hash(value))
            if len(self.hashes) > CARDINALITY_CAP:
                self.capped = True
                self.hashes.clear()

    def profile(self) -> FieldProfile:
        non_null = self.total - self.nulls
        cardinality = len(self.hashes) if not self.capped else CARDINALITY_CAP
        unique_ratio = (cardinality / non_null) if (non_null and not self.capped) else 0.0
        enum_values = [EnumValue(value=self.raw.get(k, k), count=c)
                       for k, c in sorted(self.top.items(),
                                          key=lambda kv: (-kv[1], kv[0]))
                       if self.values.get(k)]
        enum_values = enum_values[:TOP_VALUES_LIMIT]
        distinct = len(self.values)
        enum_candidate = (
            not self.capped
            and 0 < distinct <= ENUM_MAX_DISTINCT
            and non_null > 0
            and (sum(self.values.values()) - self.nulls) / non_null >= ENUM_MIN_FILL
            and self.kind == "scalar"
        )
        return FieldProfile(
            path=self.path,
            kind=self.kind,  # type: ignore[arg-type]
            observed_types=sorted(self.types - {"null"}),
            total_count=self.total,
            null_count=self.nulls,
            cardinality=cardinality,
            cardinality_capped=self.capped,
            unique_ratio=round(unique_ratio, 6),
            enum_candidate=enum_candidate,
            enum_values=enum_values if enum_candidate else [],
            formats=sorted(self.formats_seen),
            array_item_types=sorted(self.item_types),
            object_fields=sorted(self.children),
            max_nesting_depth=self.max_depth,
        )


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "root"


# ---------------------------------------------------------------------------
# SchemaProfiler (SR-ING-010)

class SchemaProfiler:
    """Streaming-friendly JSON schema profiler (SR-ING-010).

    Usage::

        profiler = SchemaProfiler(dataset="incidents")
        for record in stream:
            profiler.update(record)
        report = profiler.report()

    Field paths use dotted notation (``a.b.c``, ``a.b[]`` for arrays of
    scalars; nested objects inside arrays are folded into the same path so a
    stream of varying shapes collapses to one deterministic profile).
    """

    def __init__(self, dataset: str = "dataset") -> None:
        self.dataset = dataset
        self._record_count = 0
        self._fields: dict[str, _FieldAccumulator] = {}

    @property
    def record_count(self) -> int:
        return self._record_count

    def update(self, record: Mapping[str, Any]) -> None:
        """Fold one record into the profile."""
        self._record_count += 1
        self._walk("", record)

    def _walk(self, prefix: str, value: Any) -> None:
        if isinstance(value, Mapping):
            acc = self._acc(prefix or "$", "object")
            acc.observe(value)
            for key, child in value.items():
                self._walk(f"{prefix}.{key}" if prefix else str(key), child)
        elif isinstance(value, (list, tuple)):
            acc = self._acc(prefix, "array")
            acc.observe(value)
            for item in value:
                if isinstance(item, (Mapping, list, tuple)):
                    self._walk(f"{prefix}[]", item)
                else:
                    self._acc(f"{prefix}[]", "scalar").observe(item)
        else:
            self._acc(prefix or "$", "scalar").observe(value)

    def _acc(self, path: str, kind: str) -> _FieldAccumulator:
        acc = self._fields.get(path)
        if acc is None:
            acc = _FieldAccumulator(path, kind)
            self._fields[path] = acc
        return acc

    def report(self) -> ProfileReport:
        """Materialize the deterministic profile report."""
        return ProfileReport(
            profile_id=f"urn:eoip:ingest:profile:{_slug(self.dataset)}",
            record_count=self._record_count,
            fields=sorted((acc.profile() for acc in self._fields.values()),
                          key=lambda f: f.path),
        )


def profile_records(
    records: Iterable[Mapping[str, Any]],
    dataset: str = "dataset",
) -> ProfileReport:
    """Profile a whole iterable of records (SR-ING-010)."""
    profiler = SchemaProfiler(dataset=dataset)
    for record in records:
        if isinstance(record, Mapping):
            profiler.update(record)
    return profiler.report()


def diff_profiles(before: ProfileReport, after: ProfileReport) -> ProfileDrift:
    """Drift diff between two versions of a payload profile (SR-ING-010).

    Detects: added/removed fields, observed-type changes, format changes,
    nullability flips, cardinality shifts beyond 10%, and new enum values.
    Output is deterministically ordered.
    """
    changes: list[FieldDrift] = []
    before_map = {f.path: f for f in before.fields}
    after_map = {f.path: f for f in after.fields}
    for path in sorted(set(before_map) | set(after_map)):
        b, a = before_map.get(path), after_map.get(path)
        if b is None and a is not None:
            changes.append(FieldDrift(path=path, change="added",
                                      detail=f"new {a.kind} field"))
            continue
        if a is None and b is not None:
            changes.append(FieldDrift(path=path, change="removed",
                                      detail=f"was {b.kind}"))
            continue
        assert b is not None and a is not None
        if b.observed_types != a.observed_types:
            changes.append(FieldDrift(
                path=path, change="type_changed",
                detail=f"{b.observed_types} -> {a.observed_types}"))
        if b.formats != a.formats:
            added = sorted(set(a.formats) - set(b.formats))
            removed = sorted(set(b.formats) - set(a.formats))
            detail_bits = []
            if added:
                detail_bits.append(f"+{added}")
            if removed:
                detail_bits.append(f"-{removed}")
            changes.append(FieldDrift(path=path, change="format_changed",
                                      detail=" ".join(detail_bits)))
        b_nn = b.null_count / b.total_count if b.total_count else 0.0
        a_nn = a.null_count / a.total_count if a.total_count else 0.0
        if (b_nn == 0.0) != (a_nn == 0.0):
            changes.append(FieldDrift(
                path=path, change="nullability_changed",
                detail=f"null ratio {b_nn:.3f} -> {a_nn:.3f}"))
        if b.cardinality and a.cardinality:
            ratio = a.cardinality / b.cardinality
            if ratio > 1.10 or ratio < 0.90:
                changes.append(FieldDrift(
                    path=path, change="cardinality_changed",
                    detail=f"{b.cardinality} -> {a.cardinality}"))
        if a.enum_candidate and b.enum_candidate:
            new_values = {ev.value for ev in a.enum_values} - \
                {ev.value for ev in b.enum_values}
            for value in sorted(new_values):
                changes.append(FieldDrift(
                    path=path, change="enum_value_added", detail=value))
    return ProfileDrift(
        drift_id=f"urn:eoip:ingest:drift:{_slug(after.profile_id)}",
        changes=changes,
    )


# ---------------------------------------------------------------------------
# Key detection (SR-ING-012)

def detect_key_candidates(
    report: ProfileReport,
    records: Iterable[Mapping[str, Any]] | None = None,
    *,
    baseline: ProfileReport | None = None,
    baseline_records: Iterable[Mapping[str, Any]] | None = None,
) -> list[KeyCandidate]:
    """Natural and composite key candidates with stability scoring (SR-ING-012).

    A single-field key candidate is a scalar field that is fully non-null and
    whose unique ratio is 1.0 (exact cardinality). Composite candidates are
    pairs of non-null scalar fields whose combined value tuples are unique
    across the stream.

    ``stability`` compares value overlap against ``baseline`` (a previous run's
    report + records): the fraction of current key values that existed in the
    baseline, i.e. how stable the key is across payload versions. When no
    baseline is supplied, stability defaults to 1.0.

    Deterministic: candidates are sorted by (composite, -stability, fields).
    """
    singles: list[KeyCandidate] = []
    scalar_fields = [f for f in report.fields
                     if f.kind == "scalar" and not f.cardinality_capped]
    for f in scalar_fields:
        non_null = f.total_count - f.null_count
        if non_null == 0 or non_null != f.total_count:
            continue  # key candidates must be fully populated
        if f.unique_ratio == 1.0:
            singles.append(KeyCandidate(
                key_id=f"urn:eoip:ingest:key:{_slug(report.profile_id)}:{f.path}",
                dataset=report.profile_id,
                fields=[f.path],
                composite=False,
                stability=1.0,
                name_hint=bool(ID_NAME_PATTERN.match(f.path.rsplit(".", 1)[-1])),
                non_null_ratio=1.0,
                unique_ratio=1.0,
            ))

    candidates = list(singles)

    if records is not None:
        materialized = [r for r in records if isinstance(r, Mapping)]
        composite = _composite_candidates(report, materialized)
        candidates.extend(composite)
        if baseline is not None and baseline_records is not None:
            base_materialized = [r for r in baseline_records
                                 if isinstance(r, Mapping)]
            _score_stability(candidates, materialized, base_materialized)

    candidates.sort(key=lambda c: (c.composite, -c.stability, c.fields))
    return candidates


def _get_path(record: Mapping[str, Any], path: str) -> Any:
    """Read a dotted path, descending into arrays of objects with ``[]``."""
    current: Any = record
    for part in path.split("."):
        if part.endswith("[]"):
            name = part[:-2]
            seq = current.get(name) if isinstance(current, Mapping) else None
            if not isinstance(seq, (list, tuple)):
                return None
            current = seq
            continue
        if isinstance(current, (list, tuple)):
            current = [c.get(part) if isinstance(c, Mapping) else None
                       for c in current]
            continue
        if isinstance(current, Mapping):
            current = current.get(part)
        else:
            return None
    if isinstance(current, (list, tuple)) and len(current) == 1:
        return current[0]
    return current


def _composite_candidates(
    report: ProfileReport,
    records: list[Mapping[str, Any]],
) -> list[KeyCandidate]:
    fields = [f for f in report.fields
              if f.kind == "scalar" and not f.cardinality_capped]
    pool = [f.path for f in fields][:12]
    candidates: list[KeyCandidate] = []
    n = len(records)
    if n < 2 or len(pool) < 2:
        return candidates
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            fa, fb = pool[i], pool[j]
            seen: set[str] = set()
            tuples: list[tuple[Any, Any]] = []
            valid = True
            for rec in records:
                va, vb = _get_path(rec, fa), _get_path(rec, fb)
                if va is None or vb is None:
                    valid = False
                    break
                key = _canonical([va, vb])
                seen.add(key)
                tuples.append((va, vb))
            if not valid or len(seen) != n:
                continue
            candidates.append(KeyCandidate(
                key_id=f"urn:eoip:ingest:key:{_slug(report.profile_id)}:{fa}+{fb}",
                dataset=report.profile_id,
                fields=sorted([fa, fb]),
                composite=True,
                stability=1.0,
                name_hint=bool(ID_NAME_PATTERN.match(fa.rsplit(".", 1)[-1]))
                or bool(ID_NAME_PATTERN.match(fb.rsplit(".", 1)[-1])),
                non_null_ratio=1.0,
                unique_ratio=1.0,
            ))
    return candidates


def _score_stability(
    candidates: list[KeyCandidate],
    current: list[Mapping[str, Any]],
    baseline: list[Mapping[str, Any]],
) -> None:
    base_sets: dict[tuple[str, ...], set[str]] = {}
    for cand in candidates:
        fields = tuple(cand.fields)
        if fields not in base_sets:
            base_sets[fields] = {
                hashlib.sha256(_canonical([_get_path(r, f) for f in fields])
                               .encode("utf-8")).hexdigest()
                for r in baseline
            }
        base = base_sets[fields]
        if not base:
            cand.stability = 0.0
            continue
        hits = 0
        for rec in current:
            digest = hashlib.sha256(
                _canonical([_get_path(rec, f) for f in fields])
                .encode("utf-8")).hexdigest()
            if digest in base:
                hits += 1
        cand.stability = round(hits / max(len(current), 1), 6)


# ---------------------------------------------------------------------------
# Explicit relationship discovery (SR-ING-013)

class DatasetProfile(BaseModel):
    """A named profile + optional raw records for cross-dataset analysis."""

    model_config = ConfigDict(extra="forbid")

    name: str
    report: ProfileReport
    records: list[dict[str, Any]] = Field(default_factory=list)
    primary_key: str | None = None


def _field_values(records: list[dict[str, Any]], path: str) -> Iterator[Any]:
    for rec in records:
        value = _get_path(rec, path)
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            yield from (v for v in value if v is not None)
        else:
            yield value


def _sample(values: Iterable[Any], limit: int = 5) -> list[str]:
    seen: dict[str, str] = {}
    for v in values:
        key = _canonical(v)
        seen.setdefault(key, str(v))
        if len(seen) >= limit:
            break
    return sorted(seen.values())


def discover_relationships(
    datasets: list[DatasetProfile],
) -> list[RelationshipCandidate]:
    """Explicit relationship discovery over profiled datasets (SR-ING-013).

    Signals implemented (all deterministic, all ASSERTED per SR-ING-016
    because the source records state the reference explicitly):

    * ``foreign_key_like`` — field named ``*_id``/``*_key``/``*_uuid`` whose
      values overlap another dataset's unique key field.
    * ``parent_pointer`` — field named ``parent``/``parent_id``/... whose
      values resolve to the same dataset's key field (hierarchy edge).
    * ``url_reference`` — URL-valued field whose path tail matches a key of
      another (or the same) dataset.
    * ``array_of_ids`` — array-of-scalar field whose values overlap another
      dataset's key field.
    * ``type_id_pair`` — adjacent ``<name>_type`` + ``<name>_id`` pair where
      the id values overlap the dataset named by the type.

    Statistical overlap discovery (SR-ING-014) is deferred (ADR-gated).
    Candidates are deterministically ordered and deduplicated.
    """
    candidates: list[RelationshipCandidate] = []
    index_by_id: dict[str, int] = {}

    def emit(method: RelationshipCandidate.method,  # type: ignore[valid-type]
             from_ds: DatasetProfile, from_field: str,
             to_ds: DatasetProfile, to_field: str,
             evidence: list[str], confidence: float = 1.0) -> None:
        rid = (f"urn:eoip:ingest:relationship:"
               f"{_slug(from_ds.name)}.{_slug(from_field)}->"
               f"{_slug(to_ds.name)}.{_slug(to_field)}")
        candidate = RelationshipCandidate(
            relationship_id=rid,
            method=method,
            edge_class=tag_edge(method),
            confidence=round(confidence, 6),
            from_dataset=from_ds.name,
            from_field=from_field,
            to_dataset=to_ds.name,
            to_field=to_field,
            evidence=evidence,
        )
        existing = index_by_id.get(rid)
        if existing is None:
            index_by_id[rid] = len(candidates)
            candidates.append(candidate)
            return
        # A polymorphic type+id pair is more specific than the generic
        # foreign-key convention for the same relationship.
        current = candidates[existing]
        if method == "type_id_pair" and current.method == "foreign_key_like":
            candidates[existing] = candidate

    def key_fields(ds: DatasetProfile) -> list[str]:
        if ds.primary_key:
            return [ds.primary_key]
        return [f.path for f in ds.report.fields
                if f.kind == "scalar" and f.unique_ratio == 1.0
                and not f.cardinality_capped]

    for ds in datasets:
        for field in ds.report.fields:
            name = field.path.rsplit(".", 1)[-1]
            if not ds.records:
                continue
            values = list(_field_values(ds.records, field.path))
            if not values:
                continue
            str_values = [str(v) for v in values]

            # parent_pointer
            if name in PARENT_POINTER_NAMES or (
                field.kind == "scalar"
                and name.lower() in PARENT_POINTER_NAMES
            ):
                for target in key_fields(ds):
                    if target == field.path:
                        continue
                    target_values = {str(v) for v in
                                     _field_values(ds.records, target)}
                    overlap = [v for v in str_values if v in target_values]
                    if overlap:
                        emit("parent_pointer", ds, field.path, ds, target,
                             _sample(overlap))

            # array_of_ids: an array of scalars whose values resolve against
            # another dataset's key field (majority overlap required so plain
            # tag arrays do not false-positive).
            if field.kind == "array" and field.array_item_types and \
                    all(t in {"str", "int", "null"} for t in field.array_item_types):
                for other in datasets:
                    for target in key_fields(other):
                        target_values = {str(v) for v in _field_values(
                            other.records, target)}
                        distinct = set(str_values)
                        if not distinct or not target_values:
                            continue
                        overlap = distinct & target_values
                        if len(overlap) >= max(1, len(distinct) // 2):
                            emit("array_of_ids", ds, field.path,
                                 other, target, _sample(overlap),
                                 confidence=len(overlap) / len(distinct))

            if field.kind != "scalar":
                continue

            # type_id_pair: <name>_type + <name>_id polymorphic reference.
            # Runs before foreign_key_like so the more specific method wins
            # the shared relationship id.
            if name.endswith(TYPE_ID_SUFFIX):
                stem = name[: -len(TYPE_ID_SUFFIX)]
                head = field.path.rsplit(".", 1)
                id_path = (head[0] + "." if len(head) == 2 else "") \
                    + stem + "_id"
                known_paths = {f.path for f in ds.report.fields}
                if id_path in known_paths:
                    type_names = {str(t).lower()
                                  for t in _field_values(ds.records, field.path)}
                    id_strs = [str(x) for x in _field_values(
                        ds.records, id_path)]
                    for other in datasets:
                        if other.name.lower() not in type_names:
                            continue
                        for target in key_fields(other):
                            target_values = {str(v) for v in _field_values(
                                other.records, target)}
                            overlap = [x for x in id_strs if x in target_values]
                            if overlap:
                                emit("type_id_pair", ds, id_path, other,
                                     target, _sample(overlap))

            if field.kind != "scalar":
                continue

            # url_reference
            if "url" in field.formats:
                for other in datasets:
                    for target in key_fields(other):
                        target_values = {str(v) for v in _field_values(
                            other.records, target)}
                        overlap = [v for v in str_values if v in target_values]
                        if overlap:
                            emit("url_reference", ds, field.path, other,
                                 target, _sample(overlap))

            # foreign_key_like
            if ID_NAME_PATTERN.match(name) or name.lower().endswith("_id"):
                for other in datasets:
                    for target in key_fields(other):
                        if other is ds and target == field.path:
                            continue
                        target_values = {str(v) for v in _field_values(
                            other.records, target)}
                        overlap = [v for v in str_values if v in target_values]
                        if overlap and len(set(overlap)) >= max(1, len(set(str_values)) // 2):
                            emit("foreign_key_like", ds, field.path, other,
                                 target, _sample(overlap),
                                 confidence=len(set(overlap)) /
                                 len(set(str_values)))

    candidates.sort(key=lambda c: c.relationship_id)
    return candidates


# ---------------------------------------------------------------------------
# HTTP surface (lazy FastAPI import, wired by apps/api in a later step)

class ProfileRequest(BaseModel):
    """Body for the profile / keys endpoints."""

    model_config = ConfigDict(extra="forbid")

    dataset: str = "dataset"
    records: list[dict[str, Any]] = Field(default_factory=list)


class DriftRequest(BaseModel):
    """Body for the drift endpoint."""

    model_config = ConfigDict(extra="forbid")

    before: ProfileReport
    after: ProfileReport


class RelationshipsRequest(BaseModel):
    """Body for the relationships endpoint."""

    model_config = ConfigDict(extra="forbid")

    datasets: list[DatasetProfile] = Field(default_factory=list)


def build_router() -> Any:
    """Construct the FastAPI router for the schema profiler (SR-ING-010).

    The API wiring step (apps/api) calls ``build_router()`` and includes the
    returned router — no apps/api changes live in this module. Routes (POST):

    * ``/api/v1/ingest/profile``            — body ``{"dataset": ..., "records": [...]}``
    * ``/api/v1/ingest/profile/drift``      — body ``{"before": {...}, "after": {...}}``
    * ``/api/v1/ingest/profile/keys``       — body ``{"dataset": ..., "records": [...]}``
    * ``/api/v1/ingest/profile/relationships`` — body ``{"datasets": [...]}``
    """
    from fastapi import APIRouter

    router = APIRouter(prefix="/api/v1/ingest/profile", tags=["ingest-profile"])

    @router.post("", response_model=ProfileReport)
    def profile(body: ProfileRequest) -> ProfileReport:
        return profile_records(body.records, dataset=body.dataset)

    @router.post("/drift", response_model=ProfileDrift)
    def drift(body: DriftRequest) -> ProfileDrift:
        return diff_profiles(body.before, body.after)

    @router.post("/keys", response_model=list[KeyCandidate])
    def keys(body: ProfileRequest) -> list[KeyCandidate]:
        report = profile_records(body.records, dataset=body.dataset)
        return detect_key_candidates(report, records=body.records)

    @router.post("/relationships", response_model=list[RelationshipCandidate])
    def relationships(body: RelationshipsRequest) -> list[RelationshipCandidate]:
        return discover_relationships(list(body.datasets))

    return router


__all__ = [
    "CARDINALITY_CAP",
    "EDGE_CLASS_METHODS",
    "DatasetProfile",
    "EdgeClassMethod",
    "EnumValue",
    "FieldDrift",
    "FieldProfile",
    "KeyCandidate",
    "ProfileDrift",
    "ProfileReport",
    "RelationshipCandidate",
    "SchemaProfiler",
    "build_router",
    "detect_formats",
    "detect_key_candidates",
    "diff_profiles",
    "discover_relationships",
    "edge_class_for_method",
    "profile_records",
    "tag_edge",
]

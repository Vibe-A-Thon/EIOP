"""Executable GAP requirement registry and coverage scanner.

The competitive GAP documents are large roadmap contracts.  This module turns
their requirement IDs into machine-readable records and scans the codebase for
explicit implementation/test evidence so completion claims remain auditable.

Implements:
- GAP-CP-009: semantic contracts are machine-readable and testable.
- GAP-KGCI-001: CLI runnable in CI.
- GAP-KGCI-002: machine-readable report.
- GAP-KGCI-003: fail build on configured semantic regression.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

REQ_ID_RE = re.compile(r"\b((?:GAP|G2)-([A-Z0-9]+(?:-[A-Z0-9]+)*)-(\d{3}))\b")
REQ_RANGE_RE = re.compile(
    r"\b(GAP|G2)-([A-Z0-9]+(?:-[A-Z0-9]+)*)-(\d{3})"
    r"\s*(?:\.\.|through)\s*(?:(?:GAP|G2)-\2-)?(\d{3})\b",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
REQUIREMENT_LINE_RE = re.compile(r"^\s*[-*]\s+\*\*((?:GAP|G2)-[A-Z0-9-]+-\d{3})[:*]")

DEFAULT_REQUIREMENTS_DOC = Path("EOIP-engg-doc-pkg/gaps-requirements.md")
DEFAULT_IMPLEMENTATION_DOC = Path("EOIP-engg-doc-pkg/gaps-implementation.md")
G2_REQUIREMENTS_DOC = Path("EOIP-engg-doc-pkg/gaps2-requirements.md")
G2_IMPLEMENTATION_DOC = Path("EOIP-engg-doc-pkg/gaps2-implementation.md")
DEFAULT_EVIDENCE_ROOTS = (
    Path("packages"),
    Path("apps"),
    Path("scripts"),
    Path("deploy"),
)
DEFAULT_TEST_ROOTS = (Path("tests"),)
SOURCE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".ps1", ".yml", ".yaml", ".toml"}
TEST_EXTENSIONS = SOURCE_EXTENSIONS | {".md"}
SKIP_PATH_PARTS = {
    ".git",
    ".venv",
    ".vscode-test",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    ".pytest_cache",
    ".ruff_cache",
}

PRIORITY_BY_PREFIX = {
    # P0 core differentiation
    "SDT": "P0",
    "PROV": "P0",
    "GITOPS": "P0",
    "KQ": "P0",
    "ARCH": "P0",
    "CHANGE": "P0",
    "RET": "P0",
    "KRAG": "P0",
    "AI": "P0",
    "HG": "P0",
    "STUDIO": "P0",
    "NOCODE": "P0",
    "CATALOG": "P0",
    "KGCI": "P0",
    "OFFLINE": "P0",
    "AGOV": "P0",
    # P1 enterprise maturity
    "FED": "P1",
    "FABRIC": "P1",
    "TEMP": "P1",
    "ER": "P1",
    "TRUST": "P1",
    "DRIFT": "P1",
    "CDC": "P1",
    "KP": "P1",
    "TRUTH": "P1",
    "QI": "P1",
    "TAX": "P1",
    "GRAPHTEST": "P1",
    "SEC": "P1",
    "HA": "P1",
    "SEARCH": "P1",
    "OBS": "P1",
    "GDS": "P1",
    # P2 advanced differentiation
    "APP": "P2",
    "MKT": "P2",
    "TEMPLATE": "P2",
    "REC": "P2",
    "AKO": "P2",
    "CACHE": "P2",
    "LIFE": "P2",
}

DEFAULT_GATE_BLOCKING_STATUSES = ("partial", "planned")


@dataclass(frozen=True)
class EvidenceRef:
    path: str
    line: int
    excerpt: str

    def to_dict(self) -> dict:
        return {"path": self.path, "line": self.line, "excerpt": self.excerpt}


@dataclass
class GapRequirement:
    requirement_id: str
    title: str
    description: str
    source_path: str
    source_line: int
    section: str
    phase: str | None = None
    priority: str = "P2"
    implementation_refs: list[EvidenceRef] = field(default_factory=list)
    test_refs: list[EvidenceRef] = field(default_factory=list)

    @property
    def prefix(self) -> str:
        return _prefix(self.requirement_id)

    @property
    def status(self) -> str:
        if self.implementation_refs and self.test_refs:
            return "done"
        if self.implementation_refs or self.test_refs:
            return "partial"
        return "planned"

    @property
    def acceptance_issues(self) -> list[str]:
        issues: list[str] = []
        if not self.implementation_refs:
            issues.append("missing_implementation_evidence")
        if not self.test_refs:
            issues.append("missing_test_evidence")
        return issues

    def to_dict(self) -> dict:
        return {
            "requirement_id": self.requirement_id,
            "title": self.title,
            "description": self.description,
            "source_path": self.source_path,
            "source_line": self.source_line,
            "section": self.section,
            "phase": self.phase,
            "priority": self.priority,
            "status": self.status,
            "acceptance_issues": self.acceptance_issues,
            "implementation_refs": [ref.to_dict() for ref in self.implementation_refs],
            "test_refs": [ref.to_dict() for ref in self.test_refs],
        }


@dataclass
class GapCoverageReport:
    requirements: list[GapRequirement]

    def to_dict(self) -> dict:
        by_status = _count_by(req.status for req in self.requirements)
        by_priority = _count_by(req.priority for req in self.requirements)
        by_phase = _count_by(req.phase or "unmapped" for req in self.requirements)
        return {
            "total": len(self.requirements),
            "by_status": by_status,
            "by_priority": by_priority,
            "by_phase": by_phase,
            "completion": {
                "done": by_status.get("done", 0),
                "partial": by_status.get("partial", 0),
                "planned": by_status.get("planned", 0),
                "done_ratio": _ratio(by_status.get("done", 0), len(self.requirements)),
                "covered_ratio": _ratio(
                    by_status.get("done", 0) + by_status.get("partial", 0),
                    len(self.requirements),
                ),
            },
            "completion_gate": self.completion_gate(include_requirements=False),
            "requirements": [req.to_dict() for req in self.requirements],
        }

    def completion_gate(
        self,
        *,
        max_priority: str = "P0",
        blocking_statuses: Iterable[str] = DEFAULT_GATE_BLOCKING_STATUSES,
        include_requirements: bool = True,
    ) -> dict:
        """Return a release gate over requirements that must be fully done.

        ``max_priority=P1`` includes P0 and P1 requirements.  A requirement is
        blocking when it is in one of ``blocking_statuses``; by default that
        means either no implementation/test evidence or only one side present.
        """
        blocking_status_set = set(blocking_statuses)
        max_rank = _priority_rank(max_priority)
        blockers = [
            req
            for req in self.requirements
            if _priority_rank(req.priority) <= max_rank and req.status in blocking_status_set
        ]
        blocker_ids = [req.requirement_id for req in blockers]
        return {
            "passed": not blockers,
            "policy": {
                "max_priority": max_priority,
                "blocking_statuses": sorted(blocking_status_set),
                "definition_of_done": [
                    "requirement parsed from GAP source document",
                    "implementation evidence found in product code",
                    "test evidence found in automated tests",
                ],
            },
            "blocked_total": len(blockers),
            "by_status": _count_by(req.status for req in blockers),
            "by_priority": _count_by(req.priority for req in blockers),
            "blocking_requirement_ids": blocker_ids,
            "blockers": [req.to_dict() for req in blockers] if include_requirements else [],
        }


def load_gap_requirements(
    repo_root: Path,
    *,
    requirements_doc: Path = DEFAULT_REQUIREMENTS_DOC,
    implementation_doc: Path = DEFAULT_IMPLEMENTATION_DOC,
) -> list[GapRequirement]:
    """Read every line of the GAP docs and return canonical requirement records."""
    requirements_path = repo_root / requirements_doc
    implementation_path = repo_root / implementation_doc
    phase_map = _load_phase_map(implementation_path)
    requirements = _parse_requirements(requirements_path, phase_map, repo_root)
    return sorted(requirements.values(), key=lambda req: _id_sort_key(req.requirement_id))


def build_gap_coverage_report(
    repo_root: Path,
    *,
    requirements_doc: Path = DEFAULT_REQUIREMENTS_DOC,
    implementation_doc: Path = DEFAULT_IMPLEMENTATION_DOC,
    evidence_roots: Iterable[Path] = DEFAULT_EVIDENCE_ROOTS,
    test_roots: Iterable[Path] = DEFAULT_TEST_ROOTS,
) -> GapCoverageReport:
    requirements = load_gap_requirements(
        repo_root,
        requirements_doc=requirements_doc,
        implementation_doc=implementation_doc,
    )
    by_id = {req.requirement_id: req for req in requirements}
    implementation_refs = _scan_evidence(repo_root, evidence_roots, SOURCE_EXTENSIONS, by_id)
    test_refs = _scan_evidence(repo_root, test_roots, TEST_EXTENSIONS, by_id)
    for req_id, refs in implementation_refs.items():
        by_id[req_id].implementation_refs = refs
    for req_id, refs in test_refs.items():
        by_id[req_id].test_refs = refs
    return GapCoverageReport(requirements=requirements)


def _parse_requirements(path: Path, phase_map: dict[str, str], repo_root: Path) -> dict[str, GapRequirement]:
    requirements: dict[str, GapRequirement] = {}
    section_stack: list[tuple[int, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, start=1):
        heading = HEADING_RE.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2).strip()
            parent_section = " / ".join(name for lvl, name in section_stack if lvl < level)
            section_stack = [(lvl, name) for lvl, name in section_stack if lvl < level]
            section_stack.append((level, title))
            for req_id in _ids_from_line(title):
                prefix = _prefix(req_id)
                requirements[req_id] = GapRequirement(
                    requirement_id=req_id,
                    title=title[:160],
                    description=title,
                    source_path=_rel(path, repo_root),
                    source_line=line_number,
                    section=parent_section or title,
                    phase=phase_map.get(req_id),
                    priority=PRIORITY_BY_PREFIX.get(prefix, "P2"),
                )
            continue

        ids = _ids_from_line(line)
        if not ids:
            continue
        explicit_requirement = REQUIREMENT_LINE_RE.match(line)
        description = _clean_description(line)
        section = " / ".join(name for _, name in section_stack)
        for req_id in ids:
            if req_id in requirements and not explicit_requirement:
                continue
            prefix = _prefix(req_id)
            requirements[req_id] = GapRequirement(
                requirement_id=req_id,
                title=description.split(".")[0][:160],
                description=description,
                source_path=_rel(path, repo_root),
                source_line=line_number,
                section=section,
                phase=phase_map.get(req_id),
                priority=PRIORITY_BY_PREFIX.get(prefix, "P2"),
            )
    return requirements


def _load_phase_map(path: Path) -> dict[str, str]:
    phase_map: dict[str, str] = {}
    current_phase: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = HEADING_RE.match(line)
        if heading and ("Phase " in heading.group(2) or re.search(r"\bG2-P\d+\b", heading.group(2))):
            current_phase = heading.group(2).strip()
            continue
        if not current_phase:
            continue
        for req_id in _ids_from_line(line):
            phase_map.setdefault(req_id, current_phase)
    return phase_map


def _ids_from_line(line: str) -> list[str]:
    line = line.replace("*", "").replace("`", "")
    ids: set[str] = set()
    for family, prefix, start, end in REQ_RANGE_RE.findall(line):
        start_i, end_i = int(start), int(end)
        if start_i <= end_i and end_i - start_i <= 200:
            ids.update(f"{family.upper()}-{prefix.upper()}-{idx:03d}" for idx in range(start_i, end_i + 1))
    for req_id, _prefix_value, _number in REQ_ID_RE.findall(line):
        ids.add(req_id.upper())
    return sorted(ids, key=_id_sort_key)


def _clean_description(line: str) -> str:
    text = re.sub(r"^\s*[-*]\s+", "", line.strip())
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"`", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.rstrip()


def _scan_evidence(
    repo_root: Path,
    roots: Iterable[Path],
    extensions: set[str],
    requirements: dict[str, GapRequirement],
) -> dict[str, list[EvidenceRef]]:
    refs: dict[str, list[EvidenceRef]] = {req_id: [] for req_id in requirements}
    for root in roots:
        absolute_root = repo_root / root
        if not absolute_root.exists():
            continue
        for path in _iter_evidence_files(absolute_root, extensions):
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            for line_number, line in enumerate(lines, start=1):
                for req_id in _ids_from_line(line):
                    if req_id in refs and len(refs[req_id]) < 20:
                        refs[req_id].append(
                            EvidenceRef(
                                path=_rel(path, repo_root),
                                line=line_number,
                                excerpt=line.strip()[:240],
                            )
                        )
    return refs


def _iter_evidence_files(root: Path, extensions: set[str]) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_PATH_PARTS]
        current_dir = Path(dirpath)
        for filename in filenames:
            path = current_dir / filename
            if path.suffix in extensions and not _skip_path(path):
                yield path


def _skip_path(path: Path) -> bool:
    return bool(SKIP_PATH_PARTS.intersection(path.parts))


def _id_sort_key(req_id: str) -> tuple[str, int]:
    match = REQ_ID_RE.search(req_id)
    if not match:
        return req_id, 0
    return match.group(2), int(match.group(3))


def _prefix(req_id: str) -> str:
    match = REQ_ID_RE.search(req_id)
    if match:
        return match.group(2)
    parts = req_id.split("-")
    return "-".join(parts[1:-1]) if len(parts) > 2 else req_id


def _count_by(values: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _priority_rank(priority: str) -> int:
    match = re.fullmatch(r"P(\d+)", priority.upper())
    return int(match.group(1)) if match else 99


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()

"""Diff hunk parsing and commit-to-symbol linking (FR-CODE-003).

Parses unified diff output to extract changed line ranges, then intersects
those ranges with known symbol positions to produce symbol-level commit links.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DiffHunk:
    path: str
    old_start: int
    old_count: int
    new_start: int
    new_count: int

    @property
    def new_end(self) -> int:
        return self.new_start + max(self.new_count - 1, 0)


_HUNK_HEADER = re.compile(r"^@@\s+-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@")
_DIFF_FILE = re.compile(r"^(?:diff --git a/.+ b/(.+)|--- a/.+|\+\+\+ b/(.+))$")


def parse_unified_diff(diff_text: str) -> list[DiffHunk]:
    hunks: list[DiffHunk] = []
    current_path: str | None = None

    for line in diff_text.splitlines():
        file_match = _DIFF_FILE.match(line)
        if file_match:
            path = file_match.group(1) or file_match.group(2)
            if path:
                current_path = path
            continue

        hunk_match = _HUNK_HEADER.match(line)
        if hunk_match and current_path:
            old_start = int(hunk_match.group(1))
            old_count = int(hunk_match.group(2) or "1")
            new_start = int(hunk_match.group(3))
            new_count = int(hunk_match.group(4) or "1")
            hunks.append(DiffHunk(
                path=current_path,
                old_start=old_start,
                old_count=old_count,
                new_start=new_start,
                new_count=new_count,
            ))

    return hunks


@dataclass(frozen=True)
class SymbolRange:
    canonical_id: str
    name: str
    start_line: int
    end_line: int


@dataclass
class CommitSymbolLink:
    commit_id: str
    symbol_id: str
    symbol_name: str
    hunk_start: int
    hunk_end: int
    overlap_lines: int
    link_type: str = "MODIFIED"


def _ranges_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> int:
    overlap_start = max(a_start, b_start)
    overlap_end = min(a_end, b_end)
    if overlap_start > overlap_end:
        return 0
    return overlap_end - overlap_start + 1


def link_commit_to_symbols(
    commit_id: str,
    hunks: list[DiffHunk],
    symbols_by_path: dict[str, list[SymbolRange]],
) -> list[CommitSymbolLink]:
    links: list[CommitSymbolLink] = []
    seen: set[tuple[str, str]] = set()

    for hunk in hunks:
        path_symbols = symbols_by_path.get(hunk.path, [])
        for symbol in path_symbols:
            overlap = _ranges_overlap(
                hunk.new_start, hunk.new_end,
                symbol.start_line, symbol.end_line,
            )
            if overlap > 0:
                key = (commit_id, symbol.canonical_id)
                if key not in seen:
                    seen.add(key)
                    links.append(CommitSymbolLink(
                        commit_id=commit_id,
                        symbol_id=symbol.canonical_id,
                        symbol_name=symbol.name,
                        hunk_start=hunk.new_start,
                        hunk_end=hunk.new_end,
                        overlap_lines=overlap,
                    ))

    return links


def symbols_from_store(store, repo_id: str) -> dict[str, list[SymbolRange]]:
    by_path: dict[str, list[SymbolRange]] = {}
    for vertex in store.vertices():
        if vertex["label"] != "CodeSymbol":
            continue
        props = vertex["properties"]
        if props.get("repo_id") != repo_id:
            continue
        path = props.get("path", "")
        sr = SymbolRange(
            canonical_id=props.get("canonical_id", ""),
            name=props.get("name", ""),
            start_line=props.get("start_line", 0),
            end_line=props.get("end_line", 0),
        )
        by_path.setdefault(path, []).append(sr)
    return by_path

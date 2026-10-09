"""KGR-G-012: Incremental Differential AST Re-Index (Git Hook).

Git hook-triggered file-diff-only re-parsing that re-indexes only
changed files, propagating symbol impact through the dependency graph.
Target: < 2 seconds for ≤ 100 changed files.
"""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from eoip.codegraph.parser import CodeParser, ParsedFile
from eoip.graph.store import GraphStore

log = logging.getLogger("eoip.ingestion.incremental_indexer")


@dataclass(frozen=True)
class FileChange:
    path: str
    change_type: str  # added, modified, deleted, renamed
    old_path: str | None = None
    content_hash: str | None = None


@dataclass
class SymbolImpact:
    """Impact of a symbol change on dependent symbols."""
    symbol_id: str
    symbol_name: str
    file_path: str
    impact_type: str  # modified, removed, signature_changed
    affected_dependents: list[str] = field(default_factory=list)
    propagation_depth: int = 0


@dataclass
class IncrementalIndexResult:
    files_processed: int = 0
    files_skipped: int = 0
    symbols_added: int = 0
    symbols_updated: int = 0
    symbols_removed: int = 0
    impacts: list[SymbolImpact] = field(default_factory=list)
    duration_ms: int = 0
    errors: list[str] = field(default_factory=list)


class FileHashCache:
    """Tracks content hashes to skip unchanged files."""

    def __init__(self, cache_path: Path | None = None) -> None:
        self._cache_path = cache_path
        self._hashes: dict[str, str] = {}
        if cache_path and cache_path.exists():
            try:
                self._hashes = json.loads(cache_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._hashes = {}

    def get(self, path: str) -> str | None:
        return self._hashes.get(path)

    def set(self, path: str, content_hash: str) -> None:
        self._hashes[path] = content_hash

    def remove(self, path: str) -> None:
        self._hashes.pop(path, None)

    def save(self) -> None:
        if self._cache_path:
            self._cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._cache_path.write_text(json.dumps(self._hashes), encoding="utf-8")


class GitDiffParser:
    """Parses git diff output to produce structured FileChange records."""

    def parse_diff(self, repo_root: str, base_ref: str = "HEAD~1", head_ref: str = "HEAD") -> list[FileChange]:
        result = subprocess.run(
            ["git", "diff", "--name-status", "--diff-filter=ACDMR", base_ref, head_ref],
            capture_output=True, text=True, cwd=repo_root,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git diff failed: {result.stderr}")

        changes: list[FileChange] = []
        for line in result.stdout.strip().splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            status = parts[0]
            if status == "A":
                changes.append(FileChange(path=parts[1], change_type="added"))
            elif status == "M":
                changes.append(FileChange(path=parts[1], change_type="modified"))
            elif status == "D":
                changes.append(FileChange(path=parts[1], change_type="deleted"))
            elif status.startswith("R"):
                changes.append(FileChange(path=parts[2], change_type="renamed", old_path=parts[1]))

        return changes

    def parse_staged(self, repo_root: str) -> list[FileChange]:
        result = subprocess.run(
            ["git", "diff", "--name-status", "--cached"],
            capture_output=True, text=True, cwd=repo_root,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git diff --cached failed: {result.stderr}")

        changes: list[FileChange] = []
        for line in result.stdout.strip().splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            status = parts[0]
            if status == "A":
                changes.append(FileChange(path=parts[1], change_type="added"))
            elif status == "M":
                changes.append(FileChange(path=parts[1], change_type="modified"))
            elif status == "D":
                changes.append(FileChange(path=parts[1], change_type="deleted"))

        return changes


INDEXABLE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".java", ".go", ".rs", ".cs", ".cpp", ".cc", ".h", ".hpp"}


class SymbolImpactPropagator:
    """Propagates symbol changes through the dependency graph."""

    def __init__(self, store: GraphStore, max_depth: int = 3) -> None:
        self.store = store
        self.max_depth = max_depth

    def propagate(self, changed_symbols: list[dict[str, str]]) -> list[SymbolImpact]:
        impacts: list[SymbolImpact] = []
        for sym in changed_symbols:
            impact = SymbolImpact(
                symbol_id=sym.get("canonical_id", ""),
                symbol_name=sym.get("name", ""),
                file_path=sym.get("path", ""),
                impact_type=sym.get("change_type", "modified"),
            )
            dependents = self._find_dependents(sym.get("canonical_id", ""), depth=0)
            impact.affected_dependents = dependents
            impact.propagation_depth = min(self.max_depth, len(dependents))
            impacts.append(impact)
        return impacts

    def _find_dependents(self, symbol_id: str, depth: int) -> list[str]:
        if depth >= self.max_depth or not symbol_id:
            return []
        dependents: list[str] = []
        try:
            edges = self.store.edges_to(symbol_id, labels=["DEPENDS_ON", "IMPORTS", "CALLS", "CROSS_REPO_DEPENDS_ON"])
        except Exception:
            return []
        for edge in edges:
            dep_id = str(edge.get("out_v") or edge.get("out_cid", ""))
            if dep_id:
                dependents.append(dep_id)
                dependents.extend(self._find_dependents(dep_id, depth + 1))
        return list(set(dependents))


class IncrementalIndexer:
    """Performs incremental AST re-indexing triggered by git diffs."""

    def __init__(
        self,
        store: GraphStore,
        repo_root: str,
        *,
        parser: CodeParser | None = None,
        cache_path: Path | None = None,
        max_propagation_depth: int = 3,
    ) -> None:
        self.store = store
        self.repo_root = Path(repo_root)
        self.parser = parser or CodeParser()
        self.cache = FileHashCache(cache_path)
        self._diff_parser = GitDiffParser()
        self._propagator = SymbolImpactPropagator(store, max_propagation_depth)

    def index_diff(self, base_ref: str = "HEAD~1", head_ref: str = "HEAD") -> IncrementalIndexResult:
        started = time.monotonic()
        changes = self._diff_parser.parse_diff(str(self.repo_root), base_ref, head_ref)
        return self._process_changes(changes, started)

    def index_staged(self) -> IncrementalIndexResult:
        started = time.monotonic()
        changes = self._diff_parser.parse_staged(str(self.repo_root))
        return self._process_changes(changes, started)

    def index_files(self, file_paths: list[str]) -> IncrementalIndexResult:
        started = time.monotonic()
        changes = []
        for p in file_paths:
            full = self.repo_root / p
            if full.exists():
                changes.append(FileChange(path=p, change_type="modified"))
            else:
                changes.append(FileChange(path=p, change_type="deleted"))
        return self._process_changes(changes, started)

    def _process_changes(self, changes: list[FileChange], started: float) -> IncrementalIndexResult:
        result = IncrementalIndexResult()
        indexable = [c for c in changes if Path(c.path).suffix.lower() in INDEXABLE_EXTENSIONS]

        changed_symbols: list[dict[str, str]] = []
        for change in indexable:
            try:
                syms = self._process_file(change, result)
                changed_symbols.extend(syms)
            except Exception as exc:
                result.errors.append(f"{change.path}: {exc}")

        if changed_symbols:
            result.impacts = self._propagator.propagate(changed_symbols)

        self.cache.save()
        result.duration_ms = int((time.monotonic() - started) * 1000)
        return result

    def _process_file(self, change: FileChange, result: IncrementalIndexResult) -> list[dict[str, str]]:
        changed_symbols: list[dict[str, str]] = []

        if change.change_type == "deleted":
            self._handle_deletion(change.path, result, changed_symbols)
            return changed_symbols

        if change.change_type == "renamed" and change.old_path:
            self._handle_deletion(change.old_path, result, changed_symbols)

        full_path = self.repo_root / change.path
        if not full_path.exists():
            result.files_skipped += 1
            return changed_symbols

        source = full_path.read_text(encoding="utf-8", errors="replace")
        content_hash = hashlib.sha256(source.encode()).hexdigest()

        cached_hash = self.cache.get(change.path)
        if cached_hash == content_hash:
            result.files_skipped += 1
            return changed_symbols

        try:
            parsed = self.parser.parse("local", change.path, source)
        except ValueError:
            result.files_skipped += 1
            return changed_symbols

        for sym in parsed.symbols:
            existing = self.store.get_vertex_by_canonical_id(sym.canonical_id)
            if existing:
                self.store.upsert_vertex("CodeSymbol", {
                    "canonical_id": sym.canonical_id,
                    "name": sym.name,
                    "qualified_name": sym.qualified_name,
                    "kind": sym.kind,
                    "path": change.path,
                    "start_line": sym.start_line,
                    "end_line": sym.end_line,
                })
                result.symbols_updated += 1
                changed_symbols.append({
                    "canonical_id": sym.canonical_id,
                    "name": sym.name,
                    "path": change.path,
                    "change_type": "modified",
                })
            else:
                self.store.upsert_vertex("CodeSymbol", {
                    "canonical_id": sym.canonical_id,
                    "name": sym.name,
                    "qualified_name": sym.qualified_name,
                    "kind": sym.kind,
                    "path": change.path,
                    "start_line": sym.start_line,
                    "end_line": sym.end_line,
                })
                result.symbols_added += 1

        self.cache.set(change.path, content_hash)
        result.files_processed += 1
        return changed_symbols

    def _handle_deletion(self, path: str, result: IncrementalIndexResult, changed_symbols: list[dict[str, str]]) -> None:
        symbols = self.store.find_vertex_by_property("CodeSymbol", "path", path)
        for sym in symbols:
            cid = str(sym.get("canonical_id", ""))
            self.store.tombstone_vertex(cid)
            result.symbols_removed += 1
            changed_symbols.append({
                "canonical_id": cid,
                "name": str(sym.get("name", "")),
                "path": path,
                "change_type": "removed",
            })
        self.cache.remove(path)
        result.files_processed += 1


GIT_HOOK_SCRIPT = """#!/bin/sh
# EOIP Incremental AST Re-Index — post-commit hook
# Automatically re-indexes changed code files after each commit.
python -c "
from eoip.ingestion.incremental_indexer import IncrementalIndexer
from eoip.graph.store import GraphStore
# Configure your store here
# indexer = IncrementalIndexer(store, '.')
# result = indexer.index_diff()
# print(f'Indexed {result.files_processed} files, {result.symbols_added} new, {result.symbols_updated} updated, {result.symbols_removed} removed in {result.duration_ms}ms')
" 2>/dev/null || true
"""


class GitHookInstaller:
    """Installs git hooks for automatic incremental re-indexing."""

    @staticmethod
    def install(repo_root: str, hook_type: str = "post-commit") -> Path:
        hooks_dir = Path(repo_root) / ".git" / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_path = hooks_dir / hook_type
        hook_path.write_text(GIT_HOOK_SCRIPT, encoding="utf-8")
        hook_path.chmod(0o755)
        log.info("Installed %s hook at %s", hook_type, hook_path)
        return hook_path

    @staticmethod
    def uninstall(repo_root: str, hook_type: str = "post-commit") -> bool:
        hook_path = Path(repo_root) / ".git" / "hooks" / hook_type
        if hook_path.exists():
            hook_path.unlink()
            return True
        return False

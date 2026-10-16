"""KGR-G-012: Incremental Differential AST Re-Index (Git Hook).

Git hook-triggered file-diff-only re-parsing that re-indexes only
changed files, propagating symbol impact through the dependency graph.
Target: < 2 seconds for ≤ 100 changed files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eoip.codegraph.parser import PARSER_VERSION, CodeParser, ParsedFile
from eoip.graph.memory import MemoryGraphStore
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
    files_changed: list[FileChange] = field(default_factory=list)
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
            capture_output=True, text=True, cwd=repo_root, check=False,
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
            capture_output=True, text=True, cwd=repo_root, check=False,
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
            elif status.startswith("R"):
                changes.append(FileChange(path=parts[2], change_type="renamed", old_path=parts[1]))

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
            vertex = self.store.get_vertex_by_canonical_id(symbol_id)
            if not vertex:
                return []
            edges = self.store.edges_to(vertex["vid"], labels=["DEPENDS_ON", "IMPORTS", "CALLS"])
        except (AttributeError, KeyError, TypeError, ValueError):
            return []
        for edge in edges:
            dep_id = str(edge.get("out_cid") or edge.get("out_v") or "")
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
        repo_id: str = "local",
    ) -> None:
        self.store = store
        self.repo_root = Path(repo_root)
        self.repo_id = repo_id
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
        result.files_changed = indexable

        changed_symbols: list[dict[str, str]] = []
        for change in indexable:
            try:
                syms = self._process_file(change, result)
                changed_symbols.extend(syms)
            except (OSError, AttributeError, KeyError, TypeError, ValueError) as exc:
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
            parsed = self.parser.parse(self.repo_id, change.path, source)
        except ValueError:
            result.files_skipped += 1
            return changed_symbols
        if parsed.parse_errors:
            result.files_skipped += 1
            result.errors.extend(f"{change.path}: {error}" for error in parsed.parse_errors)
            return changed_symbols

        changed_symbols.extend(self._upsert_parsed_file(parsed, change, result))

        self.cache.set(change.path, content_hash)
        result.files_processed += 1
        return changed_symbols

    def _upsert_parsed_file(
        self,
        parsed: ParsedFile,
        change: FileChange,
        result: IncrementalIndexResult,
    ) -> list[dict[str, str]]:
        changed_symbols: list[dict[str, str]] = []
        file_vertex = self.store.upsert_vertex(
            "File",
            {
                "canonical_id": self._file_cid(parsed.path),
                "repo_id": self.repo_id,
                "path": parsed.path,
                "language": parsed.language,
                "content_hash": parsed.content_hash,
            },
        )
        current_symbol_ids = {symbol.canonical_id for symbol in parsed.symbols}
        for existing in self.store.find_vertex_by_property(
            "CodeSymbol", "path", parsed.path, limit=100_000, include_deleted=False
        ):
            cid = str(existing.get("canonical_id") or existing.get("properties", {}).get("canonical_id") or "")
            if cid and cid not in current_symbol_ids:
                self.store.tombstone_vertex(cid)
                result.symbols_removed += 1
                changed_symbols.append({
                    "canonical_id": cid,
                    "name": str(existing.get("properties", {}).get("name", "")),
                    "path": parsed.path,
                    "change_type": "removed",
                })

        symbol_vertices = {}
        for symbol in parsed.symbols:
            existing = self.store.get_vertex_by_canonical_id(symbol.canonical_id)
            symbol_vertex = self.store.upsert_vertex(
                "CodeSymbol",
                {
                    "canonical_id": symbol.canonical_id,
                    "name": symbol.name,
                    "qualified_name": symbol.qualified_name,
                    "symbol_kind": symbol.kind,
                    "repo_id": self.repo_id,
                    "path": parsed.path,
                    "start_line": symbol.start_line,
                    "end_line": symbol.end_line,
                    "start_column": symbol.start_column,
                    "end_column": symbol.end_column,
                    "language": parsed.language,
                    "parser_version": PARSER_VERSION,
                },
            )
            symbol_vertices[symbol.canonical_id] = symbol_vertex
            if existing:
                result.symbols_updated += 1
                change_type = "modified"
            else:
                result.symbols_added += 1
                change_type = "added"
            changed_symbols.append({
                "canonical_id": symbol.canonical_id,
                "name": symbol.name,
                "path": parsed.path,
                "change_type": change_type,
            })
            self.store.upsert_edge(
                "DECLARES",
                file_vertex["vid"],
                symbol_vertex["vid"],
                {"fact_key": f"declares:{symbol.canonical_id}"},
            )

        for imported_module in parsed.imports:
            dependency = self.store.upsert_vertex(
                "Dependency",
                {
                    "canonical_id": f"urn:eoip:code:dependency:{parsed.language}:{imported_module}",
                    "name": imported_module,
                    "language": parsed.language,
                    "resolved": False,
                },
            )
            self.store.upsert_edge(
                "IMPORTS",
                file_vertex["vid"],
                dependency["vid"],
                {"fact_key": f"imports:{parsed.path}:{imported_module}"},
            )

        for call in parsed.calls:
            caller = symbol_vertices.get(call.caller_id) or self.store.get_vertex_by_canonical_id(call.caller_id)
            callee = symbol_vertices.get(call.target_id) or self.store.get_vertex_by_canonical_id(call.target_id)
            if caller and callee:
                self.store.upsert_edge(
                    "CALLS",
                    caller["vid"],
                    callee["vid"],
                    {"fact_key": f"calls:{call.caller_id}:{call.target_id}"},
                )
        for caller_id, callee_name in self._cross_file_call_candidates(parsed):
            caller = symbol_vertices.get(caller_id) or self.store.get_vertex_by_canonical_id(caller_id)
            callee = self._unique_symbol_named(callee_name, excluding_path=parsed.path)
            if caller and callee:
                self.store.upsert_edge(
                    "CALLS",
                    caller["vid"],
                    callee["vid"],
                    {"fact_key": f"cross-file-calls:{caller_id}:{callee['canonical_id']}"},
                )
        return changed_symbols

    def _cross_file_call_candidates(self, parsed: ParsedFile) -> list[tuple[str, str]]:
        by_qualified = {symbol.qualified_name: symbol for symbol in parsed.symbols}
        out: list[tuple[str, str]] = []
        for caller_name, callee_name in getattr(parsed, "_pending_calls", []):
            caller = by_qualified.get(caller_name)
            if caller:
                out.append((caller.canonical_id, callee_name))
        return out

    def _unique_symbol_named(self, name: str, *, excluding_path: str) -> dict | None:
        matches = [
            vertex for vertex in self.store.find_vertices("CodeSymbol", {"name": name}, limit=50)
            if vertex["properties"].get("path") != excluding_path
        ]
        return matches[0] if len(matches) == 1 else None

    def _file_cid(self, path: str) -> str:
        return f"urn:eoip:code:file:{self.repo_id}:{path}"

    def _handle_deletion(self, path: str, result: IncrementalIndexResult, changed_symbols: list[dict[str, str]]) -> None:
        self.store.tombstone_vertex(self._file_cid(path))
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

GIT_HOOK_SCRIPT = """#!/bin/sh
# EOIP Incremental AST Re-Index - post-commit hook (KGR-G-012)
# Runs diff-only indexing and writes a local evidence event without demo data.
repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -n "$repo_root" ]; then
  python -m eoip.ingestion.incremental_indexer \\
    --repo-root "$repo_root" \\
    --base-ref HEAD~1 \\
    --head-ref HEAD \\
    --trigger POST_COMMIT \\
    --report "$repo_root/.eoip/incremental-index/last-event.json" \\
    >> "$repo_root/.git/eoip-incremental-index.log" 2>&1 || true
fi
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


def result_to_event(
    result: IncrementalIndexResult,
    *,
    commit_sha: str,
    trigger: str = "MANUAL",
) -> dict[str, Any]:
    direct_dependents = {dep for impact in result.impacts for dep in impact.affected_dependents[:1]}
    transitive_dependents = {dep for impact in result.impacts for dep in impact.affected_dependents[1:]}
    payload = {
        "schema_version": "1.0",
        "event_id": hashlib.sha256(
            json.dumps(
                {
                    "commit_sha": commit_sha,
                    "trigger": trigger,
                    "files": [change.path for change in result.files_changed],
                    "duration_ms": result.duration_ms,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()[:16],
        "commit_sha": commit_sha,
        "trigger": trigger,
        "files_changed": [
            {
                "path": change.path,
                "change_type": change.change_type.upper(),
                "old_path": change.old_path,
                "content_hash": change.content_hash,
            }
            for change in result.files_changed
        ],
        "symbols_updated": result.symbols_added + result.symbols_updated,
        "symbols_removed": result.symbols_removed,
        "impact_propagation": {
            "direct_dependents": len(direct_dependents),
            "transitive_dependents": len(transitive_dependents),
            "propagation_depth": max([impact.propagation_depth for impact in result.impacts] or [0]),
        },
        "duration_ms": result.duration_ms,
        "created_at": datetime.now(UTC).isoformat(),
        "metadata": {
            "requirement_id": "KGR-G-012",
            "files_processed": result.files_processed,
            "files_skipped": result.files_skipped,
            "symbols_added": result.symbols_added,
            "errors": result.errors,
            "impacts": [
                {
                    "symbol_id": impact.symbol_id,
                    "symbol_name": impact.symbol_name,
                    "file_path": impact.file_path,
                    "impact_type": impact.impact_type,
                    "affected_dependents": impact.affected_dependents,
                    "propagation_depth": impact.propagation_depth,
                }
                for impact in result.impacts
            ],
        },
    }
    return payload


def _git(repo_root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _resolve_commit(repo_root: Path, ref: str) -> str:
    try:
        return _git(repo_root, "rev-parse", ref)
    except (OSError, subprocess.CalledProcessError):
        return "0" * 40


def run_incremental_index(
    *,
    repo_root: Path,
    base_ref: str = "HEAD~1",
    head_ref: str = "HEAD",
    trigger: str = "MANUAL",
    report: Path | None = None,
    cache_path: Path | None = None,
    staged: bool = False,
) -> dict[str, Any]:
    store = MemoryGraphStore()
    indexer = IncrementalIndexer(
        store,
        str(repo_root),
        cache_path=cache_path or repo_root / ".eoip" / "incremental-index" / "hashes.json",
    )
    result = indexer.index_staged() if staged else indexer.index_diff(base_ref, head_ref)
    event = result_to_event(result, commit_sha=_resolve_commit(repo_root, head_ref), trigger=trigger)
    if report:
        target = report if report.is_absolute() else repo_root / report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(event, indent=2, sort_keys=True), encoding="utf-8")
    return event


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run or install the KGR-G-012 incremental AST indexer.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", default="HEAD~1")
    parser.add_argument("--head-ref", default="HEAD")
    parser.add_argument("--trigger", choices=["PRE_COMMIT", "POST_COMMIT", "POST_MERGE", "MANUAL", "WATCH"], default="MANUAL")
    parser.add_argument("--report", type=Path, default=Path(".eoip/incremental-index/last-event.json"))
    parser.add_argument("--cache-path", type=Path)
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args(argv)
    event = run_incremental_index(
        repo_root=args.repo_root.resolve(),
        base_ref=args.base_ref,
        head_ref=args.head_ref,
        trigger=args.trigger,
        report=args.report,
        cache_path=args.cache_path,
        staged=args.staged,
    )
    print(
        "Incremental index event "
        f"{event['event_id']}: {event['metadata']['files_processed']} files, "
        f"{event['symbols_updated']} symbols updated, {event['symbols_removed']} removed"
    )
    return 1 if event["metadata"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

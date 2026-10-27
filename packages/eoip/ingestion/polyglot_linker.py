"""KGR-G-001: Polyglot Cross-Repository AST Linker.

Extends the base code_graph parser with URI-namespaced cross-repository
symbol resolution.  Supports Python, TypeScript, Java, Go, Rust, C#, and
C++ import/dependency conventions.  Produces CROSS_REPO_DEPENDS_ON edges
linking symbols across repository boundaries.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Any

from eoip.codegraph.parser import CodeParser, ParsedFile, ParsedSymbol
from eoip.graph.store import Edge, GraphStore, Vertex


class Language(str, Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    CSHARP = "csharp"
    CPP = "cpp"


EXTENSION_MAP: dict[str, Language] = {
    ".py": Language.PYTHON,
    ".ts": Language.TYPESCRIPT,
    ".tsx": Language.TYPESCRIPT,
    ".js": Language.TYPESCRIPT,
    ".jsx": Language.TYPESCRIPT,
    ".java": Language.JAVA,
    ".go": Language.GO,
    ".rs": Language.RUST,
    ".cs": Language.CSHARP,
    ".cpp": Language.CPP,
    ".cc": Language.CPP,
    ".cxx": Language.CPP,
    ".h": Language.CPP,
    ".hpp": Language.CPP,
}


@dataclass(frozen=True)
class URISymbol:
    """A universally-addressable symbol across repositories."""
    repo_id: str
    path: str
    name: str
    kind: str
    language: Language

    @property
    def uri(self) -> str:
        return f"eoip://{self.repo_id}/{self.path}#{self.name}"

    @property
    def canonical_id(self) -> str:
        return hashlib.sha256(self.uri.encode()).hexdigest()[:24]


@dataclass(frozen=True)
class CrossRepoDependency:
    source: URISymbol
    target_uri: str
    import_path: str
    confidence: float = 1.0
    resolution_method: str = "exact"


@dataclass
class SymbolRegistry:
    """Global index of all symbols across all repositories."""
    _by_uri: dict[str, URISymbol] = field(default_factory=dict)
    _by_name: dict[str, list[URISymbol]] = field(default_factory=dict)
    _by_module: dict[str, list[URISymbol]] = field(default_factory=dict)

    def register(self, symbol: URISymbol) -> None:
        self._by_uri[symbol.uri] = symbol
        self._by_name.setdefault(symbol.name, []).append(symbol)
        module_key = f"{symbol.repo_id}:{PurePosixPath(symbol.path).parent.as_posix()}"
        self._by_module.setdefault(module_key, []).append(symbol)

    def resolve_by_uri(self, uri: str) -> URISymbol | None:
        return self._by_uri.get(uri)

    def resolve_by_name(self, name: str) -> list[URISymbol]:
        return self._by_name.get(name, [])

    def resolve_by_module(self, repo_id: str, module_path: str) -> list[URISymbol]:
        key = f"{repo_id}:{module_path}"
        return self._by_module.get(key, [])

    def all_symbols(self) -> list[URISymbol]:
        return list(self._by_uri.values())

    @property
    def size(self) -> int:
        return len(self._by_uri)


_PYTHON_IMPORT_RE = re.compile(
    r"^(?:from\s+([\w.]+)\s+import\s+([\w*,\s]+)|import\s+([\w.,\s]+))", re.MULTILINE
)
_TS_IMPORT_RE = re.compile(
    r"""import\s+(?:\{([^}]+)\}|(\w+))\s+from\s+['"]([^'"]+)['"]""", re.MULTILINE
)
_JAVA_IMPORT_RE = re.compile(r"^import\s+(?:static\s+)?([\w.]+\.\*?);", re.MULTILINE)
_GO_IMPORT_RE = re.compile(r'"([\w./]+)"')
_RUST_USE_RE = re.compile(r"^use\s+([\w:]+)(?:::\{([^}]+)\})?;", re.MULTILINE)
_CSHARP_USING_RE = re.compile(r"^using\s+(?:static\s+)?([\w.]+);", re.MULTILINE)
_CPP_INCLUDE_RE = re.compile(r'^#include\s+[<"]([^>"]+)[>"]', re.MULTILINE)


@dataclass
class ImportDescriptor:
    raw_import: str
    module_path: str
    imported_names: list[str]
    language: Language
    is_wildcard: bool = False


class PolyglotImportParser:
    """Extracts typed import descriptors from source code across 7 languages."""

    def parse(self, source: str, language: Language) -> list[ImportDescriptor]:
        dispatch = {
            Language.PYTHON: self._parse_python,
            Language.TYPESCRIPT: self._parse_typescript,
            Language.JAVA: self._parse_java,
            Language.GO: self._parse_go,
            Language.RUST: self._parse_rust,
            Language.CSHARP: self._parse_csharp,
            Language.CPP: self._parse_cpp,
        }
        handler = dispatch.get(language)
        if handler is None:
            return []
        return handler(source)

    def _parse_python(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _PYTHON_IMPORT_RE.finditer(source):
            if m.group(1):
                module = m.group(1)
                names = [n.strip() for n in m.group(2).split(",")]
                results.append(ImportDescriptor(
                    raw_import=m.group(0),
                    module_path=module.replace(".", "/"),
                    imported_names=names,
                    language=Language.PYTHON,
                    is_wildcard="*" in names,
                ))
            elif m.group(3):
                for mod in m.group(3).split(","):
                    mod = mod.strip()
                    results.append(ImportDescriptor(
                        raw_import=m.group(0),
                        module_path=mod.replace(".", "/"),
                        imported_names=[mod.split(".")[-1]],
                        language=Language.PYTHON,
                    ))
        return results

    def _parse_typescript(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _TS_IMPORT_RE.finditer(source):
            named = m.group(1)
            default = m.group(2)
            path = m.group(3)
            names = (
                [n.strip().split(" as ")[0].strip() for n in named.split(",")]
                if named else [default] if default else []
            )
            results.append(ImportDescriptor(
                raw_import=m.group(0),
                module_path=path,
                imported_names=names,
                language=Language.TYPESCRIPT,
            ))
        return results

    def _parse_java(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _JAVA_IMPORT_RE.finditer(source):
            full_path = m.group(1)
            parts = full_path.rsplit(".", 1)
            results.append(ImportDescriptor(
                raw_import=m.group(0),
                module_path=parts[0].replace(".", "/") if len(parts) > 1 else full_path.replace(".", "/"),
                imported_names=[parts[-1]],
                language=Language.JAVA,
                is_wildcard=parts[-1] == "*",
            ))
        return results

    def _parse_go(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _GO_IMPORT_RE.finditer(source):
            pkg = m.group(1)
            results.append(ImportDescriptor(
                raw_import=m.group(0),
                module_path=pkg,
                imported_names=[pkg.rsplit("/", 1)[-1]],
                language=Language.GO,
            ))
        return results

    def _parse_rust(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _RUST_USE_RE.finditer(source):
            base = m.group(1).replace("::", "/")
            braced = m.group(2)
            names = [n.strip() for n in braced.split(",")] if braced else [base.rsplit("/", 1)[-1]]
            results.append(ImportDescriptor(
                raw_import=m.group(0),
                module_path=base,
                imported_names=names,
                language=Language.RUST,
            ))
        return results

    def _parse_csharp(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _CSHARP_USING_RE.finditer(source):
            ns = m.group(1)
            results.append(ImportDescriptor(
                raw_import=m.group(0),
                module_path=ns.replace(".", "/"),
                imported_names=[ns.rsplit(".", 1)[-1]],
                language=Language.CSHARP,
            ))
        return results

    def _parse_cpp(self, source: str) -> list[ImportDescriptor]:
        results: list[ImportDescriptor] = []
        for m in _CPP_INCLUDE_RE.finditer(source):
            path = m.group(1)
            results.append(ImportDescriptor(
                raw_import=m.group(0),
                module_path=path,
                imported_names=[PurePosixPath(path).stem],
                language=Language.CPP,
            ))
        return results


class CrossRepoSymbolResolver:
    """Resolves cross-repository symbol dependencies using the global registry."""

    def __init__(self, registry: SymbolRegistry, repo_aliases: dict[str, str] | None = None) -> None:
        self.registry = registry
        self.repo_aliases = repo_aliases or {}
        self._import_parser = PolyglotImportParser()

    def resolve_imports(
        self,
        source: str,
        source_repo_id: str,
        source_path: str,
        language: Language,
    ) -> list[CrossRepoDependency]:
        descriptors = self._import_parser.parse(source, language)
        dependencies: list[CrossRepoDependency] = []

        for desc in descriptors:
            resolved = self._resolve_descriptor(desc, source_repo_id, source_path, language)
            dependencies.extend(resolved)

        return dependencies

    def _resolve_descriptor(
        self,
        desc: ImportDescriptor,
        source_repo_id: str,
        source_path: str,
        language: Language,
    ) -> list[CrossRepoDependency]:
        results: list[CrossRepoDependency] = []
        source_sym = URISymbol(
            repo_id=source_repo_id,
            path=source_path,
            name=PurePosixPath(source_path).stem,
            kind="file",
            language=language,
        )

        for name in desc.imported_names:
            if name == "*":
                continue
            candidates = self.registry.resolve_by_name(name)
            cross_repo = [c for c in candidates if c.repo_id != source_repo_id]
            if cross_repo:
                best = self._rank_candidates(cross_repo, desc.module_path)
                results.append(CrossRepoDependency(
                    source=source_sym,
                    target_uri=best.uri,
                    import_path=desc.raw_import,
                    confidence=1.0 if len(cross_repo) == 1 else 0.8,
                    resolution_method="name_match" if len(cross_repo) == 1 else "ranked",
                ))

        return results

    def _rank_candidates(self, candidates: list[URISymbol], module_path: str) -> URISymbol:
        scored: list[tuple[float, URISymbol]] = []
        for c in candidates:
            score = 0.0
            if module_path in c.path:
                score += 10.0
            alias = self.repo_aliases.get(c.repo_id, c.repo_id)
            if alias in module_path:
                score += 5.0
            if c.kind in ("class", "interface", "struct"):
                score += 2.0
            elif c.kind == "function":
                score += 1.0
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]


class PolyglotCrossRepoLinker:
    """Top-level orchestrator that ingests multiple repositories
    and emits CROSS_REPO_DEPENDS_ON edges into the graph store."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store
        self.registry = SymbolRegistry()
        self.parser = CodeParser()
        self._import_parser = PolyglotImportParser()

    def index_repository(self, repo_id: str, files: dict[str, str]) -> dict[str, Any]:
        """Index all source files from a repository into the symbol registry."""
        indexed = 0
        errors: list[str] = []
        for path, source in files.items():
            ext = PurePosixPath(path).suffix.casefold()
            lang = EXTENSION_MAP.get(ext)
            if lang is None:
                continue
            try:
                symbols = self._extract_symbols(repo_id, path, source, lang)
                for sym in symbols:
                    self.registry.register(sym)
                    self.store.upsert_vertex("CodeSymbol", {
                        "canonical_id": sym.canonical_id,
                        "uri": sym.uri,
                        "name": sym.name,
                        "kind": sym.kind,
                        "repo_id": repo_id,
                        "path": path,
                        "language": lang.value,
                    })
                indexed += 1
            except Exception as exc:
                errors.append(f"{path}: {exc}")

        return {"repo_id": repo_id, "files_indexed": indexed, "symbols": self.registry.size, "errors": errors}

    def link_cross_repo_dependencies(
        self,
        repo_aliases: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Resolve and persist all cross-repository dependency edges."""
        CrossRepoSymbolResolver(self.registry, repo_aliases)
        edge_count = 0
        unresolved: list[str] = []

        by_repo: dict[str, list[URISymbol]] = {}
        for sym in self.registry.all_symbols():
            by_repo.setdefault(sym.repo_id, []).append(sym)

        for repo_id, symbols in by_repo.items():
            for sym in symbols:
                candidates = self.registry.resolve_by_name(sym.name)
                cross = [c for c in candidates if c.repo_id != repo_id]
                for target in cross:
                    self.store.upsert_edge(
                        "CROSS_REPO_DEPENDS_ON",
                        sym.canonical_id,
                        target.canonical_id,
                        {
                            "source_repo": repo_id,
                            "target_repo": target.repo_id,
                            "source_uri": sym.uri,
                            "target_uri": target.uri,
                            "resolution_method": "symbol_name",
                        },
                    )
                    edge_count += 1

        return {
            "edges_created": edge_count,
            "total_symbols": self.registry.size,
            "repos_linked": len(by_repo),
            "unresolved": unresolved,
        }

    def _extract_symbols(
        self, repo_id: str, path: str, source: str, language: Language
    ) -> list[URISymbol]:
        symbols: list[URISymbol] = []
        lines = source.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            name = self._extract_definition_name(stripped, language)
            if name:
                kind = self._classify_kind(stripped, language)
                symbols.append(URISymbol(
                    repo_id=repo_id,
                    path=path,
                    name=name,
                    kind=kind,
                    language=language,
                ))
        return symbols

    @staticmethod
    def _extract_definition_name(line: str, language: Language) -> str | None:
        patterns: dict[Language, list[re.Pattern[str]]] = {
            Language.PYTHON: [
                re.compile(r"^(?:async\s+)?def\s+(\w+)"),
                re.compile(r"^class\s+(\w+)"),
            ],
            Language.TYPESCRIPT: [
                re.compile(r"^(?:export\s+)?(?:async\s+)?function\s+(\w+)"),
                re.compile(r"^(?:export\s+)?class\s+(\w+)"),
                re.compile(r"^(?:export\s+)?interface\s+(\w+)"),
                re.compile(r"^(?:export\s+)?(?:const|let)\s+(\w+)"),
            ],
            Language.JAVA: [
                re.compile(r"(?:public|private|protected)?\s*(?:static\s+)?(?:class|interface|enum)\s+(\w+)"),
                re.compile(r"(?:public|private|protected)\s+\w+\s+(\w+)\s*\("),
            ],
            Language.GO: [
                re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)"),
                re.compile(r"^type\s+(\w+)\s+(?:struct|interface)"),
            ],
            Language.RUST: [
                re.compile(r"^(?:pub\s+)?fn\s+(\w+)"),
                re.compile(r"^(?:pub\s+)?struct\s+(\w+)"),
                re.compile(r"^(?:pub\s+)?trait\s+(\w+)"),
                re.compile(r"^(?:pub\s+)?enum\s+(\w+)"),
            ],
            Language.CSHARP: [
                re.compile(r"(?:public|private|protected|internal)\s+(?:static\s+)?(?:class|interface|struct|enum)\s+(\w+)"),
                re.compile(r"(?:public|private|protected|internal)\s+\w+\s+(\w+)\s*\("),
            ],
            Language.CPP: [
                re.compile(r"^(?:class|struct)\s+(\w+)"),
                re.compile(r"^\w[\w:*&<>\s]+\s+(\w+)\s*\("),
            ],
        }
        for pat in patterns.get(language, []):
            m = pat.match(line)
            if m:
                return m.group(1)
        return None

    @staticmethod
    def _classify_kind(line: str, language: Language) -> str:
        lower = line.lower()
        if any(kw in lower for kw in ("class ", "struct ", "type ")):
            return "class"
        if any(kw in lower for kw in ("interface ", "trait ", "protocol ")):
            return "interface"
        if any(kw in lower for kw in ("def ", "func ", "fn ", "function ")):
            return "function"
        if any(kw in lower for kw in ("enum ",)):
            return "enum"
        if any(kw in lower for kw in ("const ", "let ", "var ")):
            return "variable"
        return "symbol"

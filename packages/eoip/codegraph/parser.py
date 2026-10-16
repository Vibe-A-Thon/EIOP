"""Deterministic Python and TypeScript symbol extraction."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import PurePosixPath

PARSER_VERSION = "eoip-code-parser/1.0"


@dataclass(frozen=True)
class ParsedSymbol:
    canonical_id: str
    name: str
    qualified_name: str
    kind: str
    start_line: int
    end_line: int
    start_column: int
    end_column: int


@dataclass(frozen=True)
class ParsedCall:
    caller_id: str
    callee_name: str
    target_id: str


@dataclass
class ParsedFile:
    repo_id: str
    path: str
    language: str
    content_hash: str
    symbols: list[ParsedSymbol] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    calls: list[ParsedCall] = field(default_factory=list)
    unresolved_calls: list[str] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)


class CodeParser:
    def parse(self, repo_id: str, path: str, source: str) -> ParsedFile:
        normalized_path = PurePosixPath(path.replace("\\", "/")).as_posix()
        suffix = PurePosixPath(normalized_path).suffix.casefold()
        language = {".py": "python", ".ts": "typescript", ".tsx": "typescript"}.get(suffix)
        if language is None:
            raise ValueError(f"unsupported source extension: {suffix or '<none>'}")
        import hashlib

        result = ParsedFile(
            repo_id=repo_id,
            path=normalized_path,
            language=language,
            content_hash=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        )
        if language == "python":
            self._parse_python(result, source)
        else:
            self._parse_typescript(result, source)
        self._resolve_calls(result)
        result.imports = sorted(set(result.imports))
        result.unresolved_calls = sorted(set(result.unresolved_calls))
        return result

    def _parse_python(self, result: ParsedFile, source: str) -> None:
        try:
            tree = ast.parse(source, filename=result.path)
        except SyntaxError as exc:
            result.parse_errors.append(f"{exc.msg} at {exc.lineno}:{exc.offset}")
            return

        definitions: list[tuple[ast.AST, list[str]]] = []
        calls: list[tuple[str, str]] = []

        def visit(node: ast.AST, scope: list[str]) -> None:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = node.name
                definitions.append((node, [*scope, name]))
                scope = [*scope, name]
                for child in ast.iter_child_nodes(node):
                    visit(child, scope)
                return
            if isinstance(node, ast.Import):
                result.imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                prefix = "." * node.level + (node.module or "")
                if prefix:
                    result.imports.append(prefix)
            elif isinstance(node, ast.Call) and scope:
                called_name = _python_call_name(node.func)
                if called_name:
                    calls.append((".".join(scope), called_name))
            for child in ast.iter_child_nodes(node):
                visit(child, scope)

        visit(tree, [])
        for node, scope in definitions:
            name = scope[-1]
            result.symbols.append(
                self._symbol(
                    result,
                    name,
                    ".".join(scope),
                    "class" if isinstance(node, ast.ClassDef) else "function",
                    node.lineno,
                    node.end_lineno or node.lineno,
                    node.col_offset + 1,
                    (node.end_col_offset or node.col_offset) + 1,
                )
            )
        result._pending_calls = calls

    def _parse_typescript(self, result: ParsedFile, source: str) -> None:
        try:
            import tree_sitter_typescript
            from tree_sitter import Language, Parser
        except ImportError:
            result.parse_errors.append("TypeScript grammar unavailable; install the codeparse extra")
            return

        parser = Parser(Language(tree_sitter_typescript.language_typescript()))
        tree = parser.parse(source.encode("utf-8"))
        if tree is None:
            result.parse_errors.append("Tree-sitter did not return a syntax tree")
            return
        if tree.root_node.has_error:
            result.parse_errors.append("TypeScript syntax contains ERROR or MISSING nodes")

        definitions: list[tuple[str, str, str, int, int, int, int]] = []
        calls: list[tuple[str, str]] = []

        def node_text(node) -> str:
            return source.encode("utf-8")[node.start_byte : node.end_byte].decode("utf-8")

        def visit(node, scope: list[str]) -> None:
            current_scope = scope
            name_node = node.child_by_field_name("name")
            kind = None
            if node.type == "function_declaration":
                kind = "function"
            elif node.type == "class_declaration":
                kind = "class"
            elif node.type == "method_definition":
                kind = "method"
            elif node.type == "variable_declarator":
                value_node = node.child_by_field_name("value")
                if value_node is not None and value_node.type in {"arrow_function", "function_expression"}:
                    kind = "function"
            if kind:
                if name_node is None and node.type == "variable_declarator":
                    name_node = node.child_by_field_name("name")
                if name_node is not None:
                    name = node_text(name_node)
                    qualified_name = ".".join([*scope, name])
                    definitions.append(
                        (
                            name,
                            qualified_name,
                            kind,
                            node.start_point.row + 1,
                            node.end_point.row + 1,
                            node.start_point.column + 1,
                            node.end_point.column + 1,
                        )
                    )
                    current_scope = [*scope, name]
            if node.type == "import_statement":
                source_node = node.child_by_field_name("source")
                if source_node is not None:
                    result.imports.append(node_text(source_node).strip("\"'"))
            if node.type == "call_expression" and current_scope:
                function_node = node.child_by_field_name("function")
                if function_node is not None:
                    calls.append((".".join(current_scope), node_text(function_node).split(".")[-1]))
            for child in node.children:
                visit(child, current_scope)

        visit(tree.root_node, [])
        result.symbols.extend(self._symbol(result, *definition) for definition in definitions)
        result._pending_calls = calls

    def _resolve_calls(self, result: ParsedFile) -> None:
        pending = getattr(result, "_pending_calls", [])
        by_name: dict[str, list[ParsedSymbol]] = {}
        by_qualified: dict[str, ParsedSymbol] = {}
        for symbol in result.symbols:
            by_name.setdefault(symbol.name, []).append(symbol)
            by_qualified[symbol.qualified_name] = symbol
        for caller_name, callee_name in pending:
            caller = by_qualified.get(caller_name)
            candidates = by_name.get(callee_name, [])
            if caller is not None and len(candidates) == 1:
                result.calls.append(ParsedCall(caller.canonical_id, callee_name, candidates[0].canonical_id))
            else:
                result.unresolved_calls.append(callee_name)

    def _symbol(
        self,
        result: ParsedFile,
        name: str,
        qualified_name: str,
        kind: str,
        start_line: int,
        end_line: int,
        start_column: int,
        end_column: int,
    ) -> ParsedSymbol:
        canonical_id = f"urn:eoip:code:symbol:{result.repo_id}:{result.path}:{qualified_name}"
        return ParsedSymbol(
            canonical_id=canonical_id,
            name=name,
            qualified_name=qualified_name,
            kind=kind,
            start_line=start_line,
            end_line=end_line,
            start_column=start_column,
            end_column=end_column,
        )


def _python_call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None

"""Owner digest computation for Python, JS/TS/TSX, Java and whole-file targets (T-202 / REVA-PD-002 / §7.6.3)."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
import hashlib
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, Union

# Lazy-loaded tree-sitter parsers
_PARSERS: dict = {}


def _get_parser(lang_name: str):
    if lang_name in _PARSERS:
        return _PARSERS[lang_name]

    try:
        from tree_sitter import Language, Parser

        if lang_name == "python":
            import tree_sitter_python
            lang = Language(tree_sitter_python.language())
        elif lang_name in ("typescript", "ts"):
            import tree_sitter_typescript
            lang = Language(tree_sitter_typescript.language_typescript())
        elif lang_name in ("tsx", "javascript", "js", "jsx"):
            import tree_sitter_typescript
            lang = Language(tree_sitter_typescript.language_tsx())
        elif lang_name == "java":
            import tree_sitter_java
            lang = Language(tree_sitter_java.language())
        else:
            return None

        parser = Parser(lang)
        _PARSERS[lang_name] = parser
        return parser
    except Exception:
        return None


@dataclass
class DigestResult:
    """Outcome of owner symbol resolution and digest computation."""

    status: Literal["found", "not_found", "ambiguous"]
    digest: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    span_bytes: Optional[bytes] = None
    candidates: List[str] = field(default_factory=list)


def normalize_source_bytes(raw_bytes: bytes) -> bytes:
    """Normalize source code bytes: UTF-8, LF line endings, rstrip each line."""
    text = raw_bytes.decode("utf-8", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    # Strip any trailing blank lines for deterministic hashing
    normalized = "\n".join(lines).strip()
    return normalized.encode("utf-8")


def hash_normalized(norm_bytes: bytes) -> str:
    """Compute SHA-256 hex digest of normalized source bytes."""
    return hashlib.sha256(norm_bytes).hexdigest()


def compute_owner_digest(
    source: Union[str, bytes, Path],
    symbol: str,
    language: str = "python",
    path: Optional[str] = None,
) -> DigestResult:
    """Compute owner digest for a symbol in a source file, supporting *file* mode."""
    if isinstance(source, Path):
        raw_bytes = source.read_bytes()
    elif isinstance(source, str):
        p = Path(source)
        if "\n" not in source and p.is_file():
            raw_bytes = p.read_bytes()
        else:
            raw_bytes = source.encode("utf-8")
    else:
        raw_bytes = source

    # Whole-file mode
    if symbol == "*file*":
        norm = normalize_source_bytes(raw_bytes)
        lines = raw_bytes.split(b"\n")
        return DigestResult(
            status="found",
            digest=hash_normalized(norm),
            start_line=1,
            end_line=len(lines),
            span_bytes=norm,
        )

    lang_lower = language.lower()

    # Try tree-sitter parser
    parser = _get_parser(lang_lower)
    if parser is not None:
        try:
            tree = parser.parse(raw_bytes)
            root = tree.root_node
            if lang_lower == "python":
                return _resolve_python_ts(raw_bytes, root, symbol)
            elif lang_lower in ("typescript", "ts", "tsx", "javascript", "js", "jsx"):
                return _resolve_js_ts(raw_bytes, root, symbol)
            elif lang_lower == "java":
                return _resolve_java(raw_bytes, root, symbol)
        except Exception:
            pass

    # Fallback to Python AST for python if tree-sitter failed or not available
    if lang_lower == "python":
        return _resolve_python_ast(raw_bytes, symbol)

    return DigestResult(status="not_found")


def _resolve_python_ast(raw_bytes: bytes, symbol: str) -> DigestResult:
    """Fallback Python symbol resolution using standard ast library."""
    try:
        source_text = raw_bytes.decode("utf-8", errors="replace")
        tree = ast.parse(source_text)
    except Exception:
        return DigestResult(status="not_found")

    symbol.split(".")
    candidates: List[Tuple[str, ast.AST]] = []

    def walk(node: ast.AST, prefix: List[str]):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                curr = prefix + [child.name]
                candidates.append((".".join(curr), child))
                walk(child, curr)

    walk(tree, [])

    # Exact match on dotted suffix or name
    matches = [c for c in candidates if c[0] == symbol or c[0].endswith("." + symbol) or symbol.endswith("." + c[0])]
    if not matches:
        return DigestResult(status="not_found")
    if len(matches) > 1:
        # Check if one is exact match
        exact = [m for m in matches if m[0] == symbol]
        if len(exact) == 1:
            matches = exact
        else:
            return DigestResult(status="ambiguous", candidates=[m[0] for m in matches])

    matched_name, node = matches[0]
    # Span lines (1-indexed)
    start_line = node.lineno
    if getattr(node, "decorator_list", None):
        start_line = min(d.lineno for d in node.decorator_list)
    end_line = getattr(node, "end_lineno", start_line)

    lines = source_text.splitlines()
    span_text = "\n".join(lines[start_line - 1 : end_line])
    norm = normalize_source_bytes(span_text.encode("utf-8"))
    return DigestResult(
        status="found",
        digest=hash_normalized(norm),
        start_line=start_line,
        end_line=end_line,
        span_bytes=norm,
    )


def _resolve_python_ts(raw_bytes: bytes, root: Any, symbol: str) -> DigestResult:
    """Resolve Python symbols using tree-sitter."""
    matches = []

    def get_ident(node) -> Optional[str]:
        for child in node.children:
            if child.type == "identifier":
                return raw_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def walk(node: Any, prefix: List[str]):
        for child in node.children:
            # Handle decorator wrapping
            if child.type == "decorated_definition":
                definition = None
                for sub in child.children:
                    if sub.type in ("function_definition", "class_definition"):
                        definition = sub
                        break
                if definition is not None:
                    name = get_ident(definition)
                    if name:
                        curr = prefix + [name]
                        matches.append((".".join(curr), child))
                        walk(definition, curr)
                continue

            if child.type in ("function_definition", "class_definition"):
                name = get_ident(child)
                if name:
                    curr = prefix + [name]
                    matches.append((".".join(curr), child))
                    walk(child, curr)

    walk(root, [])

    filtered = [m for m in matches if m[0] == symbol or m[0].endswith("." + symbol) or symbol.endswith("." + m[0])]
    if not filtered:
        return _resolve_python_ast(raw_bytes, symbol)
    if len(filtered) > 1:
        exact = [m for m in filtered if m[0] == symbol]
        if len(exact) == 1:
            filtered = exact
        else:
            return DigestResult(status="ambiguous", candidates=[m[0] for m in filtered])

    _, node = filtered[0]
    span = raw_bytes[node.start_byte : node.end_byte]
    norm = normalize_source_bytes(span)
    start_line = node.start_point[0] + 1
    end_line = node.end_point[0] + 1

    return DigestResult(
        status="found",
        digest=hash_normalized(norm),
        start_line=start_line,
        end_line=end_line,
        span_bytes=norm,
    )


def _resolve_js_ts(raw_bytes: bytes, root: Any, symbol: str) -> DigestResult:
    """Resolve JS/TS/TSX symbols using tree-sitter."""
    matches = []

    def get_ident(node) -> Optional[str]:
        for child in node.children:
            if child.type in ("identifier", "type_identifier", "property_identifier"):
                return raw_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def walk(node: Any, prefix: List[str]):
        for child in node.children:
            target = child
            if child.type == "export_statement":
                # Span includes export statement wrapper
                for sub in child.children:
                    if sub.type in ("function_declaration", "class_declaration", "lexical_declaration"):
                        target = child
                        child = sub
                        break

            if child.type in ("function_declaration", "class_declaration"):
                name = get_ident(child)
                if name:
                    curr = prefix + [name]
                    matches.append((".".join(curr), target))
                    walk(child, curr)
            elif child.type == "method_definition":
                name = get_ident(child)
                if name:
                    curr = prefix + [name]
                    matches.append((".".join(curr), target))
                    walk(child, curr)
            elif child.type == "lexical_declaration":
                # const X = () => ...
                for decl in child.children:
                    if decl.type == "variable_declarator":
                        name = get_ident(decl)
                        if name:
                            curr = prefix + [name]
                            matches.append((".".join(curr), target))
            else:
                walk(child, prefix)

    walk(root, [])

    filtered = [m for m in matches if m[0] == symbol or m[0].endswith("." + symbol) or symbol.endswith("." + m[0])]
    if not filtered:
        return DigestResult(status="not_found")
    if len(filtered) > 1:
        exact = [m for m in filtered if m[0] == symbol]
        if len(exact) == 1:
            filtered = exact
        else:
            return DigestResult(status="ambiguous", candidates=[m[0] for m in filtered])

    _, node = filtered[0]
    span = raw_bytes[node.start_byte : node.end_byte]
    norm = normalize_source_bytes(span)
    return DigestResult(
        status="found",
        digest=hash_normalized(norm),
        start_line=node.start_point[0] + 1,
        end_line=node.end_point[0] + 1,
        span_bytes=norm,
    )


def _resolve_java(raw_bytes: bytes, root: Any, symbol: str) -> DigestResult:
    """Resolve Java symbols using tree-sitter with overload disambiguation."""
    matches = []

    def get_ident(node) -> Optional[str]:
        for child in node.children:
            if child.type == "identifier":
                return raw_bytes[child.start_byte : child.end_byte].decode("utf-8")
        return None

    def walk(node: Any, prefix: List[str]):
        for child in node.children:
            if child.type in (
                "class_declaration",
                "interface_declaration",
                "record_declaration",
                "enum_declaration",
            ):
                name = get_ident(child)
                if name:
                    curr = prefix + [name]
                    matches.append((".".join(curr), child))
                    walk(child, curr)
            elif child.type in ("method_declaration", "constructor_declaration"):
                name = get_ident(child)
                if name:
                    # Collect param types for overloads
                    params = []
                    for sub in child.children:
                        if sub.type == "formal_parameters":
                            for param in sub.children:
                                if param.type == "formal_parameter":
                                    for pchild in param.children:
                                        if pchild.type in ("type_identifier", "integral_type", "floating_point_type", "boolean_type"):
                                            params.append(raw_bytes[pchild.start_byte : pchild.end_byte].decode("utf-8"))
                    param_sig = f"({','.join(params)})"
                    full_name = ".".join(prefix + [name])
                    matches.append((full_name, child))
                    matches.append((f"{full_name}{param_sig}", child))
            else:
                walk(child, prefix)

    walk(root, [])

    filtered = [m for m in matches if m[0] == symbol or m[0].endswith("." + symbol) or symbol.endswith("." + m[0])]
    if not filtered:
        return DigestResult(status="not_found")
    if len(filtered) > 1:
        exact = [m for m in filtered if m[0] == symbol]
        if len(exact) == 1:
            filtered = exact
        else:
            return DigestResult(status="ambiguous", candidates=list(set(m[0] for m in filtered)))

    _, node = filtered[0]
    span = raw_bytes[node.start_byte : node.end_byte]
    norm = normalize_source_bytes(span)
    return DigestResult(
        status="found",
        digest=hash_normalized(norm),
        start_line=node.start_point[0] + 1,
        end_line=node.end_point[0] + 1,
        span_bytes=norm,
    )

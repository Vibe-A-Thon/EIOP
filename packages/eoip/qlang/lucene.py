"""Lucene query-syntax front-end — classic Lucene query parser subset.

Supported subset: bare terms, ``"quoted phrases"``, ``field:value``,
``field:"quoted phrase"``, boolean ``AND`` / ``OR`` / ``NOT`` (uppercase),
parenthesised groups, and inclusive ranges ``field:[a TO b]``.
Default operator is OR, matching classic Lucene. Executes over document
fixtures (list of dicts); a term with no field matches any string field.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_TOKEN_RE = re.compile(
    r"""
    (?P<lparen>\()
    |(?P<rparen>\))
    |(?P<range>[A-Za-z_][\w.-]*:\[[^\]]+\])
    |(?P<phrase>[A-Za-z_][\w.-]*:"[^"]*"|"[^"]*")
    |(?P<field>[A-Za-z_][\w.-]*:[^\s()]+)
    |(?P<term>[^\s()]+)
    |(?P<ws>\s+)
    |(?P<op>\b(?:AND|OR|NOT)\b)
    """,
    re.VERBOSE,
)


def _tokenize(query: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    pos = 0
    while pos < len(query):
        if query[pos].isspace():
            pos += 1
            continue
        # explicit operators take priority over term/field scanning
        op = re.match(r"(AND|OR|NOT)\b", query[pos:])
        if op and (not tokens or tokens[-1][0] not in ("AND", "OR", "NOT", "LPAREN")):
            tokens.append((op.group(1), op.group(1)))
            pos += op.end()
            continue
        m = _TOKEN_RE.match(query, pos)
        if not m:
            raise QLangParseError(f"Unexpected token at offset {pos}: {query[pos:]!r}")
        pos = m.end()
        kind = m.lastgroup
        text = m.group()
        if kind == "range":
            fm = re.match(r"([A-Za-z_][\w.-]*):\[(.+?)\s+TO\s+(.+?)\]", text)
            if not fm:
                raise QLangParseError(f"Invalid Lucene range: {text!r}")
            tokens.append(("RANGE", text))
        elif kind == "phrase":
            tokens.append(("PHRASE", text))
        elif kind == "field":
            tokens.append(("FIELD", text))
        elif kind == "term":
            tokens.append(("TERM", text))
        elif kind == "lparen":
            tokens.append(("LPAREN", text))
        elif kind == "rparen":
            tokens.append(("RPAREN", text))
        else:
            raise QLangParseError(f"Unexpected token: {text!r}")
    return tokens


class _Parser:
    """Recursive-descent parser: OR < AND < NOT < primary."""

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> tuple[str, str] | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _next(self) -> tuple[str, str]:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse_or(self) -> Any:
        node = self.parse_and()
        while self._peek() and self._peek()[0] == "OR":
            self._next()
            node = ("or", node, self.parse_and())
        return node

    def parse_and(self) -> Any:
        node = self.parse_not()
        while self._peek() and self._peek()[0] == "AND":
            self._next()
            node = ("and", node, self.parse_not())
        return node

    def parse_not(self) -> Any:
        if self._peek() and self._peek()[0] == "NOT":
            self._next()
            return ("not", self.parse_not())
        return self.parse_primary()

    def parse_primary(self) -> Any:
        tok = self._peek()
        if tok is None:
            raise QLangParseError("Unexpected end of Lucene query")
        if tok[0] == "LPAREN":
            self._next()
            node = self.parse_or()
            if not self._peek() or self._peek()[0] != "RPAREN":
                raise QLangParseError("Unbalanced parenthesis in Lucene query")
            self._next()
            return node
        if tok[0] == "RANGE":
            self._next()
            fm = re.match(r"([A-Za-z_][\w.-]*):\[(.+?)\s+TO\s+(.+?)\]", tok[1])
            return ("range", fm.group(1), fm.group(2), fm.group(3))
        if tok[0] == "PHRASE":
            self._next()
            if tok[1].startswith('"'):
                return ("phrase", None, tok[1][1:-1])
            field, _, phrase = tok[1].partition(":")
            return ("phrase", field, phrase.strip('"'))
        if tok[0] == "FIELD":
            self._next()
            field, _, value = tok[1].partition(":")
            return ("term", field, value)
        if tok[0] == "TERM":
            self._next()
            return ("term", None, tok[1])
        raise QLangParseError(f"Unexpected token {tok!r} in Lucene query")


def parse(query: str) -> QLangPlan:
    """Parse a Lucene query string into a QLangPlan with the AST in ``extra['ast']``."""
    tokens = _tokenize(query.strip())
    if not tokens:
        raise QLangParseError("Empty Lucene query")
    ast = _Parser(tokens).parse_or()
    return QLangPlan(
        language="lucene",
        intent="FILTER",
        operation="Lucene",
        source=query.strip(),
        extra={"ast": ast},
    )


def _matches(node: Any, doc: dict[str, Any], default_fields: list[str] | None) -> bool:
    op = node[0]
    if op == "or":
        return _matches(node[1], doc, default_fields) or _matches(node[2], doc, default_fields)
    if op == "and":
        return _matches(node[1], doc, default_fields) and _matches(node[2], doc, default_fields)
    if op == "not":
        return not _matches(node[1], doc, default_fields)
    if op == "range":
        _, field, lo, hi = node
        val = doc.get(field)
        if val is None:
            return False
        try:
            return float(lo) <= float(val) <= float(hi)
        except (TypeError, ValueError):
            return str(lo) <= str(val) <= str(hi)
    if op == "phrase":
        _, field, phrase = node
        return _term_match(doc, field, phrase, exact_phrase=True, default_fields=default_fields)
    if op == "term":
        _, field, value = node
        return _term_match(doc, field, value, exact_phrase=False, default_fields=default_fields)
    return False


def _term_match(
    doc: dict[str, Any],
    field: str | None,
    value: str,
    *,
    exact_phrase: bool,
    default_fields: list[str] | None,
) -> bool:
    def _one(v: Any) -> bool:
        s = str(v)
        return s == value if exact_phrase else value.casefold() in s.casefold()

    if field is not None:
        return field in doc and _one(doc[field])
    fields = default_fields if default_fields is not None else list(doc.keys())
    return any(f in doc and _one(doc[f]) for f in fields)


def evaluate(
    plan: QLangPlan,
    docs: list[dict[str, Any]],
    *,
    default_fields: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Evaluate a parsed Lucene query over a list of document dicts."""
    return [d for d in docs if _matches(plan.extra["ast"], d, default_fields)]


def parse_and_evaluate(
    query: str,
    docs: list[dict[str, Any]],
    *,
    default_fields: list[str] | None = None,
) -> list[dict[str, Any]]:
    return evaluate(parse(query), docs, default_fields=default_fields)

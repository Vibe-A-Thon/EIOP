"""Bounded extraction helpers shared by native parsers and archive adapters."""

from __future__ import annotations

import base64
import importlib
import math
from datetime import date, datetime, time
from pathlib import Path, PurePosixPath
from typing import BinaryIO

from eoip.fileparse.contracts import ParsedDocument, ParseError, ParseOptions, Section, Table
from pydantic import JsonValue


def dependency(module: str):
    try:
        return importlib.import_module(module)
    except ModuleNotFoundError as exc:
        if exc.name != module and not module.startswith(f"{exc.name}."):
            raise
        raise ParseError("dependency_unavailable", f"{module} requires the eoip[fileparse] extra") from exc


def decode_text(content: bytes, encoding: str) -> str:
    if content.startswith((b"\xff\xfe", b"\xfe\xff")):
        encoding = "utf-16"
    elif content.startswith(b"\xef\xbb\xbf"):
        encoding = "utf-8-sig"
    try:
        text = content.decode(encoding, errors="strict")
    except (UnicodeDecodeError, LookupError) as exc:
        raise ParseError("invalid_encoding", f"Cannot decode text as {encoding}; set an explicit encoding") from exc
    if "\x00" in text:
        raise ParseError("invalid_text", "Text contains NUL bytes; a binary file must use its binary parser")
    return text


def safe_member_name(name: str) -> str:
    normalized = name.replace("\\", "/")
    parts = PurePosixPath(normalized).parts
    if (
        not parts or normalized.startswith("/") or any(part in {".", ".."} for part in normalized.split("/"))
        or any(":" in part or "\x00" in part for part in parts)
    ):
        raise ParseError("unsafe_member", "Archive/attachment name is absolute or contains unsafe path components")
    return "/".join(parts)


def bounded_read(stream: BinaryIO, limit: int) -> bytes:
    content = stream.read(limit + 1)
    if len(content) > limit:
        raise ParseError("size_limit", f"Expanded content exceeds the {limit}-byte limit")
    return content


def validate_database_snapshot(path: Path) -> None:
    if path.suffix.lower() in {".db", ".sqlite", ".sqlite3"}:
        wal = path.with_name(path.name + "-wal")
        if wal.exists() and wal.stat().st_size:
            raise ParseError("unsupported_database", "SQLite WAL is present; create a consistent backup first")


def json_cell(value: object) -> JsonValue:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else {"type": "nonfinite", "value": str(value)}
    if isinstance(value, (date, datetime, time)):
        return value.isoformat()
    if isinstance(value, bytes):
        return {"type": "blob", "encoding": "base64", "value": base64.b64encode(value).decode("ascii")}
    raise ParseError("invalid_cell", f"Unsupported cell type: {type(value).__name__}")


class Extraction:
    def __init__(self, document: ParsedDocument, options: ParseOptions) -> None:
        self.document = document
        self.options = options
        self.text_chars = 0
        self.rows = 0

    def section(self, kind: str, text: str, **locator: JsonValue) -> None:
        if not text.strip():
            return
        self.text_chars += len(text)
        if self.text_chars > self.options.max_text_chars:
            raise ParseError("text_limit", "Extracted text exceeds max_text_chars")
        if len(self.document.sections) >= self.options.max_sections:
            raise ParseError("section_limit", "Extracted sections exceed max_sections")
        self.document.sections.append(
            Section(index=len(self.document.sections), kind=kind, text=text, locator=locator)
        )

    def table(self, name: str, columns: list[str], rows: list[list[JsonValue]], **locator: JsonValue) -> None:
        self.rows += len(rows)
        if self.rows > self.options.max_rows:
            raise ParseError("row_limit", "Tabular records exceed max_rows; split the input explicitly")
        self.document.tables.append(Table(name=name, columns=columns, rows=rows, locator=locator))
        for index, row in enumerate(rows):
            values = [
                f"{columns[i] if i < len(columns) else f'column_{i + 1}'}: {value}"
                for i, value in enumerate(row) if value is not None
            ]
            self.section("table_row", " | ".join(values), table=name, row=index + 1, **locator)

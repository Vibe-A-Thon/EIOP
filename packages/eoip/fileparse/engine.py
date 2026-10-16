"""Format dispatch, global nested-container budgets, provenance and RAG chunks."""

from __future__ import annotations

import hashlib
import json
import logging
import mimetypes
import sqlite3
import tarfile
import zipfile
import zlib
from pathlib import Path
from urllib.parse import quote

from eoip.fileparse.archives import archive_members, checked_zip
from eoip.fileparse.common import Extraction, safe_member_name, validate_database_snapshot
from eoip.fileparse.contracts import (
    FileIssue,
    ParsedDocument,
    ParseError,
    ParseOptions,
    ParseResult,
    RagChunk,
)
from eoip.fileparse.media import email_members, parse_image
from eoip.fileparse.office import parse_database, parse_office
from eoip.fileparse.text import parse_text
from eoip.fileparse.tools import convert_legacy

logger = logging.getLogger(__name__)
TEXT = {".txt", ".csv", ".json", ".xml", ".html", ".htm", ".xhtml", ".rtf"}
OFFICE = {".docx", ".xlsx", ".xls", ".pptx"}
LEGACY = {".doc", ".ppt", ".wps", ".wpd"}
IMAGES = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".bmp", ".webp"}
ARCHIVES = {".zip", ".rar", ".tar", ".gz", ".7z", ".tgz"}
EMAIL = {".eml", ".msg"}
SUPPORTED_EXTENSIONS = TEXT | OFFICE | LEGACY | IMAGES | ARCHIVES | EMAIL | {".db", ".sqlite", ".sqlite3"}


def format_catalog() -> list[dict]:
    groups = [
        (TEXT - {".rtf", ".xml"}, "native_text", []),
        ({".rtf"}, "native_rtf", ["striprtf"]),
        ({".xml"}, "native_xml", ["defusedxml"]),
        (OFFICE, "native_office", ["python-docx / openpyxl / xlrd / python-pptx"]),
        (LEGACY, "local_conversion", ["LibreOffice (format/filter dependent)"]),
        (IMAGES, "image_metadata", ["Pillow", "Tesseract (only when OCR is requested)"]),
        ({".db", ".sqlite", ".sqlite3"}, "sqlite_readonly", []),
        ({".eml"}, "mime_email", []),
        ({".msg"}, "outlook_email", ["extract-msg"]),
        ({".zip", ".tar", ".gz", ".tgz"}, "native_archive", []),
        ({".7z"}, "memory_archive", ["py7zr"]),
        ({".rar"}, "local_archive", ["rarfile", "unrar / unar / 7z for compressed members"]),
    ]
    return [
        {"extension": extension, "adapter": adapter, "requirements": requirements}
        for extensions, adapter, requirements in groups for extension in sorted(extensions)
    ]


class FileParser:
    def __init__(self, options: ParseOptions | None = None) -> None:
        self.options = options or ParseOptions()

    def parse_path(self, path: str | Path, *, source_id: str = "local_files") -> ParseResult:
        source = Path(path).resolve(strict=True)
        if not source.is_file():
            raise ParseError("invalid_file", "Input must be a regular file")
        if source.stat().st_size > self.options.max_file_bytes:
            raise ParseError("size_limit", "Input exceeds max_file_bytes")
        validate_database_snapshot(source)
        from eoip.fileparse.common import bounded_read

        with source.open("rb") as stream:
            content = bounded_read(stream, self.options.max_file_bytes)
        return self.parse_bytes(content, source.name, source_id=source_id, source_uri=source.as_uri())

    def parse_bytes(
        self, content: bytes, filename: str, *, source_id: str = "local_files", source_uri: str | None = None,
    ) -> ParseResult:
        if not source_id.strip() or len(source_id) > 128:
            raise ParseError("invalid_source", "source_id must contain 1-128 characters")
        filename = safe_member_name(filename)
        if len(content) > self.options.max_file_bytes:
            raise ParseError("size_limit", "Input exceeds max_file_bytes")
        result = ParseResult()
        budget = {"bytes": 0, "members": 0, "text": 0, "rows": 0, "sections": 0}
        self._parse(
            content, filename, source_id, source_uri or f"file-upload://{quote(source_id, safe='')}/{quote(filename)}",
            None, 0, result, budget,
        )
        for document in result.documents:
            result.chunks.extend(self._chunks(document))
        if result.errors:
            result.status = "PARTIAL" if any(
                doc.sections or doc.format in {ext[1:] for ext in IMAGES}
                for doc in result.documents
            ) else "FAILED"
        return result

    def _parse(self, content, filename, source_id, uri, parent_id, depth, result, budget):
        if depth > self.options.max_depth:
            raise ParseError("depth_limit", "Nested archives/attachments exceed max_depth")
        budget["bytes"] += len(content)
        budget["members"] += 1
        if budget["bytes"] > self.options.max_expanded_bytes:
            raise ParseError("size_limit", "Nested inputs exceed the shared max_expanded_bytes budget")
        if budget["members"] > self.options.max_members:
            raise ParseError("member_limit", "Nested inputs exceed the shared max_members budget")
        suffix = Path(filename).suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise ParseError("unsupported_format", f"No local adapter for {suffix or 'extensionless files'}")
        digest = hashlib.sha256(content).hexdigest()
        identity = hashlib.sha256(f"{source_id}\0{uri}\0{digest}".encode()).hexdigest()
        document = ParsedDocument(
            document_id=f"urn:eoip:knowledge:document:file:{identity}", source_id=source_id,
            source_name=filename, source_uri=uri, parent_id=parent_id, content_hash=digest,
            size_bytes=len(content), format=suffix[1:], title=Path(filename).name,
            media_type=mimetypes.guess_type(filename)[0] or "application/octet-stream",
        )
        out = Extraction(document, self.options)
        try:
            if suffix in TEXT:
                parse_text(content, suffix, out)
            elif suffix in OFFICE:
                if suffix != ".xls":
                    self._office_budget(content, budget)
                parse_office(content, suffix, out)
            elif suffix in LEGACY:
                converted, target = convert_legacy(content, suffix, self.options)
                self._office_budget(converted, budget)
                parse_office(converted, target, out)
                document.metadata["converted_format"] = target[1:]
                document.metadata["conversion_tool"] = "LibreOffice"
            elif suffix in IMAGES:
                parse_image(content, out)
            elif suffix in {".db", ".sqlite", ".sqlite3"}:
                parse_database(content, out)
            elif suffix in EMAIL:
                self._children(email_members(content, suffix, out), document, depth, result, budget)
            else:
                archive_name = filename[:-4] + ".tar.gz" if suffix == ".tgz" else filename
                archive_suffix = ".gz" if suffix == ".tgz" else suffix
                self._children(
                    archive_members(content, archive_name, archive_suffix, self.options),
                    document, depth, result, budget,
                )
                document.metadata["container"] = True
        except ParseError:
            raise
        except (ValueError, TypeError, KeyError, OSError, EOFError, RecursionError,
                zipfile.BadZipFile, tarfile.TarError, sqlite3.Error, zlib.error) as exc:
            logger.warning("File decoding failed", extra={"file_format": suffix, "error_type": type(exc).__name__})
            raise ParseError("invalid_format", f"{suffix} decoding failed ({type(exc).__name__})") from exc
        for key, count, limit in (
            ("text", out.text_chars, self.options.max_text_chars),
            ("rows", out.rows, self.options.max_rows),
            ("sections", len(document.sections), self.options.max_sections),
        ):
            budget[key] += count
            if budget[key] > limit:
                raise ParseError(f"{key}_limit", f"Nested outputs exceed the shared {key} budget")
        if not document.sections and suffix not in ARCHIVES | IMAGES:
            document.warnings.append("No extractable text was found")
        result.documents.append(document)

    def _office_budget(self, content: bytes, budget: dict[str, int]) -> None:
        with checked_zip(content, self.options) as archive:
            budget["bytes"] += sum(item.file_size for item in archive.infolist())
            if budget["bytes"] > self.options.max_expanded_bytes:
                raise ParseError("size_limit", "Office expansion exceeds shared max_expanded_bytes")

    def _children(self, members, parent, depth, result, budget):
        seen = set()
        for name, content in members:
            name = safe_member_name(name)
            if name in seen:
                raise ParseError("duplicate_member", "Container has duplicate member names")
            seen.add(name)
            document_start = len(result.documents)
            error_start = len(result.errors)
            try:
                self._parse(
                    content, name, parent.source_id, f"{parent.source_uri}!/{quote(name)}",
                    parent.document_id, depth + 1, result, budget,
                )
            except ParseError as exc:
                del result.documents[document_start:]
                del result.errors[error_start:]
                if exc.code.endswith("_limit") or exc.code in {"unsafe_member", "duplicate_member"}:
                    raise
                logger.warning("Container member decoding failed", extra={"error_category": exc.code})
                result.errors.append(FileIssue(source_name=f"{parent.source_name}!/{name}", code=exc.code, message=str(exc)))

    def _chunks(self, document: ParsedDocument):
        for section in document.sections:
            start = 0
            while start < len(section.text):
                end = min(start + self.options.chunk_chars, len(section.text))
                text = section.text[start:end]
                identity = hashlib.sha256(
                    f"{document.document_id}\0{document.parser_version}\0{section.index}\0{start}\0{end}\0{text}".encode()
                ).hexdigest()
                yield RagChunk(
                    chunk_id=f"urn:eoip:knowledge:section:file:{identity}", document_id=document.document_id,
                    source_id=document.source_id, source_uri=document.source_uri, content_hash=document.content_hash,
                    section_index=section.index, start_char=start, end_char=end, text=text,
                    locator=section.locator, citations=[f"{document.source_uri}#section={section.index}&chars={start}:{end}"],
                )
                if end == len(section.text):
                    break
                start = end - self.options.chunk_overlap

    @staticmethod
    def to_json(result: ParseResult) -> str:
        return json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2, allow_nan=False) + "\n"

"""Format dispatch, global nested-container budgets, provenance and RAG chunks."""

from __future__ import annotations

import base64
import hashlib
import importlib
import io
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

CORE_FORMATS = {".txt", ".csv", ".json", ".xml", ".html", ".rtf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
EXTENDED_FORMATS = {".tsv", ".yaml", ".yml", ".jsonld", ".xhtml", ".htm", ".md", ".markdown", ".adoc", ".asciidoc", ".odt", ".odp", ".ods", ".pdf"}

TEXT = {".txt", ".csv", ".tsv", ".json", ".jsonld", ".yaml", ".yml", ".xml", ".html", ".htm", ".xhtml", ".rtf", ".md", ".markdown", ".adoc", ".asciidoc"}
OFFICE = {".docx", ".xlsx", ".xls", ".pptx", ".odt", ".ods", ".odp", ".pdf"}
LEGACY = {".doc", ".ppt", ".wps", ".wpd"}
IMAGES = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".bmp", ".webp"}
ARCHIVES = {".zip", ".rar", ".tar", ".gz", ".7z", ".tgz", ".bz2"}
EMAIL = {".eml", ".msg", ".mbox"}
DATABASE = {".db", ".sqlite", ".sqlite3"}
SUPPORTED_EXTENSIONS = TEXT | OFFICE | LEGACY | IMAGES | ARCHIVES | EMAIL | DATABASE

FORMAT_DEPENDENCIES = {
    ".rtf": ["striprtf"],
    ".xml": ["defusedxml"],
    ".yaml": ["yaml"],
    ".yml": ["yaml"],
    ".docx": ["docx"],
    ".xlsx": ["openpyxl"],
    ".xls": ["xlrd"],
    ".pptx": ["pptx"],
    ".pdf": ["pypdf"],
    ".odt": ["defusedxml"],
    ".ods": ["defusedxml"],
    ".odp": ["defusedxml"],
    ".doc": ["soffice"],
    ".ppt": ["soffice"],
    ".wps": ["soffice"],
    ".wpd": ["soffice"],
    ".msg": ["extract_msg"],
    ".7z": ["py7zr"],
    ".rar": ["rarfile"],
}


def check_dependency_available(pkg: str) -> bool:
    try:
        importlib.import_module(pkg)
        return True
    except (ImportError, Exception):
        return False


def get_format_readiness(extension: str, libreoffice_path: str | None = None) -> dict:
    ext = extension.lower() if extension.startswith(".") else f".{extension.lower()}"
    reqs = FORMAT_DEPENDENCIES.get(ext, [])
    missing = []
    for req in reqs:
        if req == "soffice":
            import shutil
            if not shutil.which(libreoffice_path or "soffice"):
                missing.append("LibreOffice (soffice)")
        else:
            if not check_dependency_available(req.split(".")[0]):
                missing.append(req)
    cat = "core" if ext in CORE_FORMATS else ("extended" if ext in EXTENDED_FORMATS else "system")
    return {
        "extension": ext,
        "status": "UNAVAILABLE" if missing else "AVAILABLE",
        "missing_dependencies": missing,
        "category": cat,
    }


def detect_format(content: bytes, filename: str | None = None) -> str:
    if content.startswith(b"%PDF-"):
        return ".pdf"
    if content.startswith(b"SQLite format 3\x00"):
        return ".db"
    if content.lstrip().startswith(b"{\\rtf"):
        return ".rtf"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if content.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if content.startswith((b"II*\x00", b"MM\x00*")):
        return ".tif"
    if content.startswith(b"BM") and len(content) >= 14:
        return ".bmp"
    if content.startswith(b"RIFF") and len(content) >= 12 and content[8:12] == b"WEBP":
        return ".webp"
    if content.startswith(b"7z\xbc\xaf\x27\x1c"):
        return ".7z"
    if content.startswith(b"\x1f\x8b"):
        return ".gz"
    if len(content) >= 512 and content[257:262] == b"ustar":
        return ".tar"
    if content.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
        if filename:
            ext = Path(filename).suffix.lower()
            if ext in {".doc", ".xls", ".ppt", ".msg"}:
                return ext
        return ".doc"
    if content.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                names = z.namelist()
                if any(n.startswith("word/") for n in names):
                    return ".docx"
                if any(n.startswith("xl/") for n in names):
                    return ".xlsx"
                if any(n.startswith("ppt/") for n in names):
                    return ".pptx"
                if "mimetype" in names:
                    mt = z.read("mimetype").strip()
                    if b"oasis.opendocument.text" in mt:
                        return ".odt"
                    if b"oasis.opendocument.spreadsheet" in mt:
                        return ".ods"
                    if b"oasis.opendocument.presentation" in mt:
                        return ".odp"
                if "content.xml" in names:
                    return ".odt"
                return ".zip"
        except Exception:
            return ".zip"

    head = content[:2048].lstrip()
    head_lower = head.lower()
    if head_lower.startswith(b"<!doctype html") or b"<html" in head_lower:
        return ".html"
    if head_lower.startswith(b"<?xml") or (head.startswith(b"<") and b">" in head and not head.startswith(b"<!")):
        return ".xml"

    if (head.startswith(b"{") and content.rstrip().endswith(b"}")) or (head.startswith(b"[") and content.rstrip().endswith(b"]")):
        try:
            val = json.loads(content.decode("utf-8"))
            if isinstance(val, dict) and "@context" in val:
                return ".jsonld"
            return ".json"
        except Exception:
            pass

    if filename:
        ext = Path(filename).suffix.lower()
        if ext in SUPPORTED_EXTENSIONS:
            return ext
    return ""


def format_catalog() -> list[dict]:
    groups = [
        (TEXT - {".rtf", ".xml", ".yaml", ".yml"}, "native_text", []),
        ({".yaml", ".yml"}, "native_yaml", ["yaml"]),
        ({".rtf"}, "native_rtf", ["striprtf"]),
        ({".xml"}, "native_xml", ["defusedxml"]),
        ({".docx"}, "native_docx", ["python-docx"]),
        ({".xlsx"}, "native_xlsx", ["openpyxl"]),
        ({".xls"}, "native_xls", ["xlrd"]),
        ({".pptx"}, "native_pptx", ["python-pptx"]),
        ({".pdf"}, "native_pdf", ["pypdf"]),
        ({".odt", ".ods", ".odp"}, "native_odf", ["defusedxml"]),
        (LEGACY, "local_conversion", ["LibreOffice (format/filter dependent)"]),
        (IMAGES, "image_metadata", ["Pillow", "Tesseract (only when OCR is requested)"]),
        (DATABASE, "sqlite_readonly", []),
        ({".eml"}, "mime_email", []),
        ({".msg"}, "outlook_email", ["extract-msg"]),
        ({".zip", ".tar", ".gz", ".tgz"}, "native_archive", []),
        ({".7z"}, "memory_archive", ["py7zr"]),
        ({".rar"}, "local_archive", ["rarfile", "unrar / unar / 7z for compressed members"]),
    ]
    catalog = []
    for extensions, adapter, requirements in groups:
        for extension in sorted(extensions):
            readiness = get_format_readiness(extension)
            catalog.append({
                "extension": extension,
                "adapter": adapter,
                "requirements": requirements,
                "status": readiness["status"],
                "missing_dependencies": readiness["missing_dependencies"],
                "category": readiness["category"],
            })
    return catalog


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
        initial_metadata: dict[str, any] | None = None,
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
            None, 0, result, budget, parent=None, initial_metadata=initial_metadata,
        )
        for document in result.documents:
            result.chunks.extend(self._chunks(document))
        if result.errors:
            result.status = "PARTIAL" if any(
                doc.sections or doc.format in {ext[1:] for ext in IMAGES}
                for doc in result.documents
            ) else "FAILED"
        return result

    def _parse(self, content, filename, source_id, uri, parent_id, depth, result, budget, parent=None, initial_metadata=None):
        if depth > self.options.max_depth:
            raise ParseError("depth_limit", "Nested archives/attachments exceed max_depth")
        budget["bytes"] += len(content)
        budget["members"] += 1
        if budget["bytes"] > self.options.max_expanded_bytes:
            raise ParseError("size_limit", "Nested inputs exceed the shared max_expanded_bytes budget")
        if budget["members"] > self.options.max_members:
            raise ParseError("member_limit", "Nested inputs exceed the shared max_members budget")
        supported = set(SUPPORTED_EXTENSIONS)
        if not self.options.enable_pdf:
            supported.discard(".pdf")
        detected = detect_format(content, filename)
        suffix = Path(filename).suffix.lower()
        if suffix not in supported or (detected in OFFICE and suffix in {".zip", ""}):
            suffix = detected or suffix
        if suffix not in supported:
            raise ParseError("unsupported_format", f"No local adapter for {suffix or 'extensionless files'}")
        digest = hashlib.sha256(content).hexdigest()
        identity = hashlib.sha256(f"{source_id}\0{uri}\0{digest}".encode()).hexdigest()
        readiness_info = get_format_readiness(suffix, self.options.libreoffice_path)
        document = ParsedDocument(
            document_id=f"urn:eoip:knowledge:document:file:{identity}", source_id=source_id,
            source_name=filename, source_uri=uri, parent_id=parent_id, content_hash=digest,
            size_bytes=len(content), format=suffix[1:], title=Path(filename).name,
            media_type=mimetypes.guess_type(filename)[0] or "application/octet-stream",
            raw_bytes_base64=base64.b64encode(content).decode("ascii"),
            readiness=readiness_info["status"],
        )
        if initial_metadata and not parent:
            document.metadata.update(initial_metadata)
        if parent:
            for key in ("acl", "retention_policy", "legal_hold", "tenant_id", "classification", "matter_id"):
                if key in parent.metadata:
                    document.metadata[key] = parent.metadata[key]
        out = Extraction(document, self.options)
        try:
            if suffix in TEXT:
                parse_text(content, suffix, out)
            elif suffix in OFFICE:
                if suffix not in {".xls", ".pdf"}:
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
            elif suffix in DATABASE:
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
                    parent.document_id, depth + 1, result, budget, parent=parent,
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
                ev_locator = {
                    "document_id": document.document_id,
                    "source_system": document.source_id,
                    "source_revision": str(section.locator.get("source_revision") or document.content_hash[:16]),
                    "page_number": section.locator.get("page") or section.locator.get("page_number"),
                    "slide_number": section.locator.get("slide") or section.locator.get("slide_number"),
                    "sheet_name": str(section.locator.get("sheet") or section.locator.get("sheet_name")) if (section.locator.get("sheet") or section.locator.get("sheet_name")) else None,
                    "cell": str(section.locator.get("cell")) if section.locator.get("cell") else None,
                    "paragraph_index": section.locator.get("paragraph") or section.locator.get("block"),
                    "char_start": start,
                    "char_end": end,
                }
                yield RagChunk(
                    chunk_id=f"urn:eoip:knowledge:section:file:{identity}", document_id=document.document_id,
                    source_id=document.source_id, source_uri=document.source_uri, content_hash=document.content_hash,
                    section_index=section.index, start_char=start, end_char=end, text=text,
                    locator=section.locator, citations=[f"{document.source_uri}#section={section.index}&chars={start}:{end}"],
                    evidence_locator=ev_locator,
                )
                if end == len(section.text):
                    break
                next_start = end - self.options.chunk_overlap
                if next_start <= start:
                    next_start = start + 1
                start = next_start

    @staticmethod
    def to_json(result: ParseResult) -> str:
        return json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2, allow_nan=False) + "\n"

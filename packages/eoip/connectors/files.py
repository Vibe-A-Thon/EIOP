"""Binary-safe local file acquisition using the existing connector protocol."""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from urllib.parse import quote

from eoip.connectors.generic import LocalFileConnector, LocalFileScope
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities
from eoip.fileparse.common import bounded_read, safe_member_name, validate_database_snapshot
from eoip.fileparse.contracts import PARSER_VERSION, ParseError
from eoip.fileparse.engine import SUPPORTED_EXTENSIONS
from pydantic import Field


def file_event(content: bytes, filename: str, source_id: str, *, source_uri: str | None = None) -> SourceEventV2:
    filename = safe_member_name(filename)
    digest = hashlib.sha256(content).hexdigest()
    uri = source_uri or f"file-upload://{quote(source_id, safe='')}/{quote(filename)}"
    event_id = hashlib.sha256(f"{source_id}\0{uri}\0{digest}".encode()).hexdigest()
    now = utc_now_iso()
    return SourceEventV2(
        event_id=event_id, source_system="documents", source_instance_id=source_id,
        source_record_id=uri, source_record_type="binary_file", content_hash=digest,
        source_version=digest, event_time=now, captured_at=now,
        payload={"filename": filename, "encoding": "base64", "content": base64.b64encode(content).decode("ascii")},
        metadata={"connector": PARSER_VERSION, "size_bytes": len(content)},
    )


class FileParsingConnector(LocalFileConnector):
    """Capture bytes first; parsing occurs at the ingestion boundary, not acquisition."""

    def __init__(self, source_id: str, scope: LocalFileScope) -> None:
        super().__init__(source_id, scope)
        if not all(root.is_dir() for root in self._roots):
            raise ValueError("File parser roots must be directories")
        if any(suffix.casefold() not in SUPPORTED_EXTENSIONS for suffix in scope.suffixes):
            raise ParseError("unsupported_format", "Configured suffix has no file parsing adapter")

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(polling=True, reconciliation=False)

    def _files(self, root: Path):
        suffixes = {suffix.casefold() for suffix in self.scope.suffixes}
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.casefold() not in suffixes:
                continue
            if path.suffix.casefold() not in SUPPORTED_EXTENSIONS:
                raise ParseError("unsupported_format", "Configured suffix has no file parsing adapter")
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(root):
                raise ParseError("unsafe_path", "File escapes its configured source root")
            if self._excluded(resolved):
                continue
            if resolved.stat().st_size > self.scope.max_file_bytes:
                raise ParseError("size_limit", "Source file exceeds max_file_bytes")
            yield resolved

    def _events(self):
        count = 0
        seen = set()
        for root in self._roots:
            for path in self._files(root):
                if path in seen:
                    continue
                seen.add(path)
                count += 1
                if count > self.scope.max_files:
                    raise ParseError("member_limit", "Source exceeds max_files; baseline is incomplete")
                yield self._event(path)

    def handle_event(self, event: dict):
        path = event.get("path")
        if not isinstance(path, str) or not path:
            raise ParseError("invalid_event", "File change event requires a nonempty path")
        return iter((self.fetch_record(path),))

    def _event(self, path: Path) -> SourceEventV2:
        if self._excluded(path):
            raise ParseError("unsafe_path", "Requested file is excluded from the configured scope")
        if path.suffix.casefold() not in {suffix.casefold() for suffix in self.scope.suffixes}:
            raise ParseError("unsupported_format", "Requested file suffix is outside the configured scope")
        validate_database_snapshot(path)
        with path.open("rb") as stream:
            content = bounded_read(stream, self.scope.max_file_bytes)
        return file_event(content, path.name, self.source_id, source_uri=path.as_uri())

    def _excluded(self, path: Path) -> bool:
        return any(
            path.is_relative_to(Path(excluded).resolve())
            for excluded in getattr(self.scope, "excluded_paths", [])
        )


class FileParsingScope(LocalFileScope):
    """A local scope whose defaults select every supported file format."""

    suffixes: list[str] = Field(default_factory=lambda: sorted(SUPPORTED_EXTENSIONS), max_length=100)
    max_file_bytes: int = Field(default=20_000_000, ge=1, le=100_000_000)
    excluded_paths: list[str] = Field(default_factory=list, max_length=1000)

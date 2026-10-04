"""Archive members are read in memory, never extracted into caller directories."""

from __future__ import annotations

import gzip
import io
import lzma
import stat
import tarfile
import zipfile
from collections.abc import Iterator

from eoip.fileparse.common import bounded_read, dependency, safe_member_name
from eoip.fileparse.contracts import ParseError, ParseOptions


def checked_zip(content: bytes, options: ParseOptions) -> zipfile.ZipFile:
    archive = zipfile.ZipFile(io.BytesIO(content))
    try:
        entries = archive.infolist()
        if len(entries) > options.max_members:
            raise ParseError("member_limit", "ZIP exceeds max_members")
        names = set()
        total = 0
        for entry in entries:
            name = safe_member_name(entry.filename.rstrip("/"))
            if name in names:
                raise ParseError("duplicate_member", "ZIP contains duplicate member names")
            names.add(name)
            if entry.flag_bits & 1:
                raise ParseError("encrypted_file", "Encrypted ZIP/Office files require a decrypted local copy")
            if stat.S_ISLNK(entry.external_attr >> 16):
                raise ParseError("unsafe_member", "ZIP symlinks are not supported")
            total += entry.file_size
            if total > options.max_expanded_bytes or entry.file_size > options.max_expanded_bytes:
                raise ParseError("size_limit", "ZIP uncompressed bytes exceed max_expanded_bytes")
        return archive
    except (ParseError, ValueError):
        archive.close()
        raise


def archive_members(content: bytes, filename: str, suffix: str, options: ParseOptions) -> Iterator[tuple[str, bytes]]:
    if suffix == ".zip":
        with checked_zip(content, options) as archive:
            for entry in archive.infolist():
                if not entry.is_dir():
                    with archive.open(entry) as stream:
                        yield safe_member_name(entry.filename), bounded_read(stream, options.max_expanded_bytes)
    elif suffix == ".tar":
        with tarfile.open(fileobj=io.BytesIO(content), mode="r:") as archive:
            count = 0
            total = 0
            for entry in archive:
                count += 1
                if count > options.max_members:
                    raise ParseError("member_limit", "TAR exceeds max_members")
                name = safe_member_name(entry.name.rstrip("/"))
                if entry.isdir():
                    continue
                if not entry.isfile():
                    raise ParseError("unsafe_member", "TAR links/devices are not supported")
                total += entry.size
                if total > options.max_expanded_bytes:
                    raise ParseError("size_limit", "TAR exceeds max_expanded_bytes")
                stream = archive.extractfile(entry)
                if stream is None:
                    raise ParseError("invalid_archive", "TAR member has no readable contents")
                with stream:
                    yield name, bounded_read(stream, options.max_expanded_bytes)
    elif suffix == ".gz":
        with gzip.GzipFile(fileobj=io.BytesIO(content)) as stream:
            data = bounded_read(stream, options.max_expanded_bytes)
        name = filename[:-3]
        if name.endswith(".tgz") or not name:
            raise ParseError("invalid_archive", "GZIP needs a filename indicating its uncompressed format")
        yield name, data
    elif suffix == ".rar":
        rarfile = dependency("rarfile")
        try:
            with rarfile.RarFile(io.BytesIO(content)) as archive:
                entries = archive.infolist()
                if len(entries) > options.max_members:
                    raise ParseError("member_limit", "RAR exceeds max_members")
                if archive.needs_password():
                    raise ParseError("encrypted_file", "Encrypted RAR requires a decrypted local copy")
                if sum(item.file_size for item in entries) > options.max_expanded_bytes:
                    raise ParseError("size_limit", "RAR exceeds max_expanded_bytes")
                for entry in entries:
                    name = safe_member_name(entry.filename.rstrip("/"))
                    if entry.isdir():
                        continue
                    if entry.is_symlink():
                        raise ParseError("unsafe_member", "RAR symlinks are not supported")
                    with archive.open(entry) as stream:
                        yield name, bounded_read(stream, options.max_expanded_bytes)
        except rarfile.RarCannotExec as exc:
            raise ParseError("tool_unavailable", "Compressed RAR requires a local unrar/unar/7z backend") from exc
        except rarfile.Error as exc:
            raise ParseError("invalid_archive", "RAR decoding failed") from exc
    else:
        yield from seven_zip_members(content, options)


def seven_zip_members(content: bytes, options: ParseOptions) -> Iterator[tuple[str, bytes]]:
    py7zr = dependency("py7zr")
    seven_io = dependency("py7zr.io")

    class Sink(seven_io.Py7zIO):
        def __init__(self, factory):
            self.stream = io.BytesIO()
            self.factory = factory

        def write(self, data):
            self.factory.written += len(data)
            if self.factory.written > options.max_expanded_bytes:
                raise ParseError("size_limit", "7z expanded bytes exceed max_expanded_bytes")
            return self.stream.write(data)

        def read(self, size=None):
            return self.stream.read(-1 if size is None else size)

        def seek(self, offset, whence=0):
            return self.stream.seek(offset, whence)

        def flush(self):
            return None

        def size(self):
            return len(self.stream.getbuffer())

    class Factory(seven_io.WriterFactory):
        def __init__(self):
            self.outputs: dict[str, Sink] = {}
            self.written = 0

        def create(self, filename):
            name = safe_member_name(filename)
            if name in self.outputs:
                raise ParseError("duplicate_member", "7z contains duplicate member names")
            sink = Sink(self)
            self.outputs[name] = sink
            return sink

    try:
        with py7zr.SevenZipFile(io.BytesIO(content), mode="r") as archive:
            entries = archive.list()
            if len(entries) > options.max_members:
                raise ParseError("member_limit", "7z exceeds max_members")
            if archive.needs_password():
                raise ParseError("encrypted_file", "Encrypted 7z requires a decrypted local copy")
            if sum(entry.uncompressed or 0 for entry in entries) > options.max_expanded_bytes:
                raise ParseError("size_limit", "7z exceeds max_expanded_bytes")
            for entry in entries:
                safe_member_name(entry.filename.rstrip("/"))
            # Validate link/device metadata before even memory-only extraction.
            for entry in archive.files:
                if entry.is_symlink or entry.is_junction or entry.is_socket:
                    raise ParseError("unsafe_member", "7z links/devices are not supported")
            factory = Factory()
            archive.extractall(factory=factory)
            for name, sink in factory.outputs.items():
                yield name, sink.stream.getvalue()
    except (py7zr.exceptions.ArchiveError, lzma.LZMAError) as exc:
        raise ParseError("invalid_archive", "7z decoding failed") from exc

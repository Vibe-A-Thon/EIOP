"""
Pure-Python Dalvik Executable (DEX) Header & Bytecode Parser (REVA-MB-002, T-ENH-016).
Parses DEX headers and extracts class definitions, method counts, and checksums.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from reva.core.errors import RevaValidationError


@dataclass
class DEXHeader:
    version: str
    checksum: int
    signature: str
    file_size_bytes: int
    string_ids_count: int
    type_ids_count: int
    proto_ids_count: int
    field_ids_count: int
    method_ids_count: int
    class_defs_count: int
    sha256: str = ""


class DEXParser:
    """
    Parses Android Dalvik Executable (.dex) headers.
    """

    MAGIC_PREFIX = b"dex\n"

    def parse_bytes(self, data: bytes) -> DEXHeader:
        if len(data) < 112:
            raise RevaValidationError("Invalid DEX file: payload too short for header")

        if not data.startswith(self.MAGIC_PREFIX):
            raise RevaValidationError("Invalid DEX magic bytes")

        version_bytes = data[4:7]
        version = version_bytes.decode("ascii", errors="replace")

        # Offset 8: checksum (uint32)
        checksum = struct.unpack_from("<I", data, 8)[0]
        # Offset 12: signature (20-byte SHA-1)
        signature = data[12:32].hex()
        # Offset 32: file_size (uint32)
        file_size = struct.unpack_from("<I", data, 32)[0]

        # Offset 56: string_ids_size
        string_ids_size = struct.unpack_from("<I", data, 56)[0]
        # Offset 64: type_ids_size
        type_ids_size = struct.unpack_from("<I", data, 64)[0]
        # Offset 72: proto_ids_size
        proto_ids_size = struct.unpack_from("<I", data, 72)[0]
        # Offset 80: field_ids_size
        field_ids_size = struct.unpack_from("<I", data, 80)[0]
        # Offset 88: method_ids_size
        method_ids_size = struct.unpack_from("<I", data, 88)[0]
        # Offset 96: class_defs_size
        class_defs_size = struct.unpack_from("<I", data, 96)[0]

        sha256 = hashlib.sha256(data).hexdigest()

        return DEXHeader(
            version=version,
            checksum=checksum,
            signature=signature,
            file_size_bytes=file_size,
            string_ids_count=string_ids_size,
            type_ids_count=type_ids_size,
            proto_ids_count=proto_ids_size,
            field_ids_count=field_ids_size,
            method_ids_count=method_ids_size,
            class_defs_count=class_defs_size,
            sha256=sha256,
        )

    def parse_file(self, file_path: str | Path) -> DEXHeader:
        raw = Path(file_path).read_bytes()
        return self.parse_bytes(raw)

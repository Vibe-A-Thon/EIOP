"""
WebAssembly (WASM) Binary Module Decoder (REVA-FM-003, T-ENH-023).
Parses WASM binary magic, version, and section headers without external runtimes.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from reva.core.errors import RevaValidationError


@dataclass
class WASMSection:
    section_id: int
    name: str
    offset: int
    size_bytes: int


@dataclass
class WASMModuleInfo:
    version: int
    sha256: str
    sections: List[WASMSection] = field(default_factory=list)
    has_type_section: bool = False
    has_import_section: bool = False
    has_export_section: bool = False
    has_code_section: bool = False


class WASMDecoder:
    """
    Decodes WebAssembly 1.0/2.0 binary modules.
    """

    MAGIC = b"\x00asm"
    SECTION_NAMES = {
        0: "Custom",
        1: "Type",
        2: "Import",
        3: "Function",
        4: "Table",
        5: "Memory",
        6: "Global",
        7: "Export",
        8: "Start",
        9: "Element",
        10: "Code",
        11: "Data",
        12: "DataCount",
    }

    def decode_bytes(self, data: bytes) -> WASMModuleInfo:
        if len(data) < 8:
            raise RevaValidationError("Payload too short for WebAssembly module header")

        if not data.startswith(self.MAGIC):
            raise RevaValidationError("Invalid WebAssembly magic bytes (expected \\x00asm)")

        version = struct.unpack_from("<I", data, 4)[0]
        sha256 = hashlib.sha256(data).hexdigest()

        sections: List[WASMSection] = []
        offset = 8
        n = len(data)

        while offset < n:
            sec_id = data[offset]
            offset += 1

            # Read LEB128 size
            sec_size = 0
            shift = 0
            while offset < n:
                byte_val = data[offset]
                offset += 1
                sec_size |= (byte_val & 0x7F) << shift
                if not (byte_val & 0x80):
                    break
                shift += 7

            sec_name = self.SECTION_NAMES.get(sec_id, f"Unknown_{sec_id}")
            sections.append(WASMSection(
                section_id=sec_id,
                name=sec_name,
                offset=offset,
                size_bytes=sec_size,
            ))
            offset += sec_size

        return WASMModuleInfo(
            version=version,
            sha256=sha256,
            sections=sections,
            has_type_section=any(s.section_id == 1 for s in sections),
            has_import_section=any(s.section_id == 2 for s in sections),
            has_export_section=any(s.section_id == 7 for s in sections),
            has_code_section=any(s.section_id == 10 for s in sections),
        )

    def decode_file(self, file_path: str | Path) -> WASMModuleInfo:
        raw = Path(file_path).read_bytes()
        return self.decode_bytes(raw)

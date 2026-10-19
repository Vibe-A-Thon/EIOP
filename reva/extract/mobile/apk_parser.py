"""
Pure-Python APK/AAB Archive Parser & Zip-Bomb Guard (REVA-MB-001, T-ENH-015).
Safe triage of Android packages without executing runtime tools.
"""

from __future__ import annotations

import hashlib
import io
import os
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from reva.core.errors import RevaResourceLimitError, RevaValidationError


@dataclass
class APKMetadata:
    sha256: str
    file_size_bytes: int
    total_uncompressed_bytes: int
    decompression_ratio: float
    has_manifest: bool
    dex_files: List[str] = field(default_factory=list)
    native_libraries: Dict[str, List[str]] = field(default_factory=dict)  # abi -> list of .so names
    member_count: int = 0
    package_name: Optional[str] = None


class APKParser:
    """
    Safely triages Android APK and AAB packages with zip-bomb protection.
    """

    MAX_RATIO = 200.0  # Max uncompressed / compressed ratio
    MAX_FILE_BYTES = 500 * 1024 * 1024  # 500 MiB limit

    def parse_bytes(self, data: bytes) -> APKMetadata:
        sha256 = hashlib.sha256(data).hexdigest()
        size = len(data)
        if size > self.MAX_FILE_BYTES:
            raise RevaResourceLimitError(f"Package exceeds maximum allowed size of {self.MAX_FILE_BYTES} bytes")

        try:
            zf = zipfile.ZipFile(io.BytesIO(data))
        except zipfile.BadZipFile as e:
            raise RevaValidationError(f"Invalid or corrupted APK/ZIP archive: {e}") from e

        total_uncompressed = 0
        dex_files = []
        native_libs: Dict[str, List[str]] = {}
        has_manifest = False

        for info in zf.infolist():
            total_uncompressed += info.file_size
            name = info.filename

            if name == "AndroidManifest.xml":
                has_manifest = True
            elif name.endswith(".dex"):
                dex_files.append(name)
            elif name.startswith("lib/") and name.endswith(".so"):
                parts = name.split("/")
                if len(parts) >= 3:
                    abi = parts[1]
                    so_name = parts[-1]
                    native_libs.setdefault(abi, []).append(so_name)

        ratio = (total_uncompressed / size) if size > 0 else 0.0
        if ratio > self.MAX_RATIO:
            raise RevaResourceLimitError(f"Zip-bomb protection triggered: decompression ratio {ratio:.1f} > {self.MAX_RATIO}")

        return APKMetadata(
            sha256=sha256,
            file_size_bytes=size,
            total_uncompressed_bytes=total_uncompressed,
            decompression_ratio=ratio,
            has_manifest=has_manifest,
            dex_files=dex_files,
            native_libraries=native_libs,
            member_count=len(zf.infolist()),
        )

    def parse_file(self, file_path: str | Path) -> APKMetadata:
        raw = Path(file_path).read_bytes()
        return self.parse_bytes(raw)

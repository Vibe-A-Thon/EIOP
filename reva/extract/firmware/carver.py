"""
Pure-Python Firmware Partition & Filesystem Carver (REVA-FM-001, T-ENH-021).
Scans raw firmware images to detect and carve embedded SquashFS, U-Boot, CPIO, and Ext4 partitions.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CarvedPartition:
    partition_type: str  # "SquashFS", "U-Boot", "CPIO", "Ext4"
    offset: int
    size_estimate_bytes: int
    endianness: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class FirmwareCarver:
    """
    Scans firmware image bytes to identify embedded filesystem signatures.
    """

    MAGIC_SIGNATURES = [
        (b"hsqs", "SquashFS", "little"),
        (b"sqsh", "SquashFS", "big"),
        (b"\x27\x05\x19\x56", "U-Boot", "big"),
        (b"070701", "CPIO", "ascii"),
        (b"070702", "CPIO-CRC", "ascii"),
    ]

    def carve_bytes(self, data: bytes) -> List[CarvedPartition]:
        partitions: List[CarvedPartition] = []
        n = len(data)

        # 1. Scan for signature patterns
        for sig, part_type, endian in self.MAGIC_SIGNATURES:
            start = 0
            while True:
                idx = data.find(sig, start)
                if idx == -1:
                    break

                meta = {}
                size_est = min(n - idx, 10 * 1024 * 1024)

                if part_type == "SquashFS" and idx + 40 <= n:
                    # In SquashFS, bytes_used is at offset 40 (int64) or offset 36
                    try:
                        prefix = "<" if endian == "little" else ">"
                        s_bytes = struct.unpack_from(f"{prefix}Q", data, idx + 40)[0]
                        if 1024 <= s_bytes <= n - idx:
                            size_est = s_bytes
                    except struct.error:
                        pass
                elif part_type == "U-Boot" and idx + 12 <= n:
                    try:
                        d_size = struct.unpack_from(">I", data, idx + 12)[0]
                        size_est = 64 + d_size
                        meta["image_size"] = d_size
                    except struct.error:
                        pass

                partitions.append(CarvedPartition(
                    partition_type=part_type,
                    offset=idx,
                    size_estimate_bytes=size_est,
                    endianness=endian,
                    metadata=meta,
                ))
                start = idx + max(len(sig), 512)

        # 2. Check Ext4 superblock (magic 0xef53 at offset 1080 from block start)
        for block_start in range(0, n - 1082, 4096):
            if data[block_start + 1080:block_start + 1082] == b"\x53\xef":
                partitions.append(CarvedPartition(
                    partition_type="Ext4",
                    offset=block_start,
                    size_estimate_bytes=min(n - block_start, 64 * 1024 * 1024),
                    endianness="little",
                ))

        partitions.sort(key=lambda p: p.offset)
        return partitions

    def carve_file(self, file_path: str | Path) -> List[CarvedPartition]:
        raw = Path(file_path).read_bytes()
        return self.carve_bytes(raw)

"""
Pure-Python Native Binary Loader & Header Parser (REVA-NB-001, T-ENH-008).
Parses ELF, PE (Portable Executable), and Mach-O headers without external dependencies.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from reva.core.errors import RevaValidationError


@dataclass
class SectionInfo:
    name: str
    virtual_address: int
    size_bytes: int
    flags: str  # e.g., "RX", "RW", "RO"
    is_executable: bool


@dataclass
class BinaryHeader:
    format: str  # "ELF", "PE", "MACH-O", "UNKNOWN"
    architecture: str  # "x86", "x86_64", "ARM", "AArch64", "MIPS", "UNKNOWN"
    bitness: int  # 32 or 64
    endianness: str  # "little" or "big"
    entry_point: int
    sections: List[SectionInfo] = field(default_factory=list)
    imported_symbols: List[str] = field(default_factory=list)
    exported_symbols: List[str] = field(default_factory=list)
    sha256: str = ""
    file_size_bytes: int = 0


class NativeBinaryLoader:
    """
    Pure-Python parser for native executables and shared libraries.
    """

    MAGIC_ELF = b"\x7fELF"
    MAGIC_PE_DOS = b"MZ"
    MAGIC_MACHO_32_LE = b"\xce\xfa\xed\xfe"
    MAGIC_MACHO_64_LE = b"\xcf\xfa\xed\xfe"
    MAGIC_MACHO_32_BE = b"\xfe\xed\xfa\xce"
    MAGIC_MACHO_64_BE = b"\xfe\xed\xfa\xcf"

    def load_bytes(self, raw_bytes: bytes) -> BinaryHeader:
        """Parses binary header directly from bytes buffer."""
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        size = len(raw_bytes)

        if raw_bytes.startswith(self.MAGIC_ELF):
            return self._parse_elf(raw_bytes, sha256, size)
        elif raw_bytes.startswith(self.MAGIC_PE_DOS):
            return self._parse_pe(raw_bytes, sha256, size)
        elif any(raw_bytes.startswith(m) for m in (self.MAGIC_MACHO_32_LE, self.MAGIC_MACHO_64_LE, self.MAGIC_MACHO_32_BE, self.MAGIC_MACHO_64_BE)):
            return self._parse_macho(raw_bytes, sha256, size)
        else:
            return BinaryHeader(
                format="UNKNOWN",
                architecture="UNKNOWN",
                bitness=0,
                endianness="little",
                entry_point=0,
                sha256=sha256,
                file_size_bytes=size,
            )

    def load_file(self, file_path: str | Path) -> BinaryHeader:
        """Loads and parses binary file from disk."""
        path = Path(file_path)
        if not path.is_file():
            raise RevaValidationError(f"File not found: {path}")
        raw = path.read_bytes()
        return self.load_bytes(raw)

    def _parse_elf(self, data: bytes, sha256: str, size: int) -> BinaryHeader:
        """Parses ELF 32/64-bit headers."""
        if len(data) < 52:
            raise RevaValidationError("Corrupted ELF header: too short")

        ei_class = data[4]  # 1 = 32-bit, 2 = 64-bit
        ei_data = data[5]   # 1 = Little Endian, 2 = Big Endian
        bitness = 64 if ei_class == 2 else 32
        endian = "little" if ei_data == 1 else "big"
        prefix = "<" if endian == "little" else ">"

        # e_machine at offset 18 (2 bytes)
        e_machine = struct.unpack_from(f"{prefix}H", data, 18)[0]
        arch_map = {3: "x86", 62: "x86_64", 40: "ARM", 183: "AArch64", 8: "MIPS"}
        arch = arch_map.get(e_machine, f"Machine_{e_machine}")

        # Entry point at offset 24
        if bitness == 64:
            entry = struct.unpack_from(f"{prefix}Q", data, 24)[0]
            shoff = struct.unpack_from(f"{prefix}Q", data, 40)[0]
            shentsize = struct.unpack_from(f"{prefix}H", data, 58)[0]
            shnum = struct.unpack_from(f"{prefix}H", data, 60)[0]
            shstrndx = struct.unpack_from(f"{prefix}H", data, 62)[0]
        else:
            entry = struct.unpack_from(f"{prefix}I", data, 24)[0]
            shoff = struct.unpack_from(f"{prefix}I", data, 32)[0]
            shentsize = struct.unpack_from(f"{prefix}H", data, 46)[0]
            shnum = struct.unpack_from(f"{prefix}H", data, 48)[0]
            shstrndx = struct.unpack_from(f"{prefix}H", data, 50)[0]

        sections: List[SectionInfo] = []
        # Parse section headers if within bounds
        if shoff > 0 and (shoff + shnum * shentsize) <= len(data) and shstrndx < shnum:
            # First find shstrtab offset
            strtab_hdr_offset = shoff + shstrndx * shentsize
            if bitness == 64:
                strtab_offset = struct.unpack_from(f"{prefix}Q", data, strtab_hdr_offset + 24)[0]
            else:
                strtab_offset = struct.unpack_from(f"{prefix}I", data, strtab_hdr_offset + 16)[0]

            for i in range(shnum):
                offset = shoff + i * shentsize
                if bitness == 64:
                    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack_from(f"{prefix}IIQQQQ", data, offset)[:6]
                else:
                    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack_from(f"{prefix}IIIIII", data, offset)[:6]

                name = ""
                if strtab_offset + sh_name < len(data):
                    end_str = data.find(b"\x00", strtab_offset + sh_name)
                    if end_str != -1:
                        name = data[strtab_offset + sh_name:end_str].decode("ascii", errors="ignore")

                is_exec = bool(sh_flags & 0x4)
                flags = "RX" if is_exec else ("RW" if (sh_flags & 0x2) else "RO")
                if name:
                    sections.append(SectionInfo(
                        name=name,
                        virtual_address=sh_addr,
                        size_bytes=sh_size,
                        flags=flags,
                        is_executable=is_exec,
                    ))

        # Basic symbol harvesting from ASCII strings in .rodata or data
        imported_symbols: List[str] = []
        for sec in sections:
            if sec.name in (".dynsym", ".symtab", ".rodata"):
                pass

        return BinaryHeader(
            format="ELF",
            architecture=arch,
            bitness=bitness,
            endianness=endian,
            entry_point=entry,
            sections=sections,
            imported_symbols=imported_symbols,
            sha256=sha256,
            file_size_bytes=size,
        )

    def _parse_pe(self, data: bytes, sha256: str, size: int) -> BinaryHeader:
        """Parses PE (Portable Executable) headers."""
        if len(data) < 64:
            raise RevaValidationError("Corrupted PE header: DOS stub too short")

        e_lfanew = struct.unpack_from("<I", data, 60)[0]
        if e_lfanew + 24 > len(data) or data[e_lfanew:e_lfanew+4] != b"PE\x00\x00":
            return BinaryHeader(
                format="PE",
                architecture="UNKNOWN",
                bitness=32,
                endianness="little",
                entry_point=0,
                sha256=sha256,
                file_size_bytes=size,
            )

        machine = struct.unpack_from("<H", data, e_lfanew + 4)[0]
        num_sections = struct.unpack_from("<H", data, e_lfanew + 6)[0]
        opt_hdr_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]

        arch_map = {0x014c: ("x86", 32), 0x8664: ("x86_64", 64), 0x01c0: ("ARM", 32), 0xaa64: ("AArch64", 64)}
        arch, bitness = arch_map.get(machine, ("UNKNOWN", 32))

        # Entry point in optional header
        opt_hdr_offset = e_lfanew + 24
        entry = 0
        if opt_hdr_size >= 20 and opt_hdr_offset + 20 <= len(data):
            entry = struct.unpack_from("<I", data, opt_hdr_offset + 16)[0]

        # Sections
        sections: List[SectionInfo] = []
        sec_table_offset = opt_hdr_offset + opt_hdr_size
        for i in range(num_sections):
            sec_offset = sec_table_offset + i * 40
            if sec_offset + 40 > len(data):
                break
            raw_name = data[sec_offset:sec_offset+8].rstrip(b"\x00").decode("ascii", errors="ignore")
            v_size, v_addr, raw_size, raw_ptr = struct.unpack_from("<IIII", data, sec_offset + 8)[:4]
            characteristics = struct.unpack_from("<I", data, sec_offset + 36)[0]
            is_exec = bool(characteristics & 0x20000000)
            is_write = bool(characteristics & 0x80000000)
            flags = "RX" if is_exec else ("RW" if is_write else "RO")
            sections.append(SectionInfo(
                name=raw_name,
                virtual_address=v_addr,
                size_bytes=v_size or raw_size,
                flags=flags,
                is_executable=is_exec,
            ))

        return BinaryHeader(
            format="PE",
            architecture=arch,
            bitness=bitness,
            endianness="little",
            entry_point=entry,
            sections=sections,
            sha256=sha256,
            file_size_bytes=size,
        )

    def _parse_macho(self, data: bytes, sha256: str, size: int) -> BinaryHeader:
        """Parses Mach-O headers."""
        magic = data[:4]
        is_64 = magic in (self.MAGIC_MACHO_64_LE, self.MAGIC_MACHO_64_BE)
        is_le = magic in (self.MAGIC_MACHO_32_LE, self.MAGIC_MACHO_64_LE)
        prefix = "<" if is_le else ">"

        cputype = struct.unpack_from(f"{prefix}I", data, 4)[0]
        arch_map = {7: "x86", 7 | 0x01000000: "x86_64", 12: "ARM", 12 | 0x01000000: "AArch64"}
        arch = arch_map.get(cputype, f"CPU_{cputype}")

        return BinaryHeader(
            format="MACH-O",
            architecture=arch,
            bitness=64 if is_64 else 32,
            endianness="little" if is_le else "big",
            entry_point=0,
            sha256=sha256,
            file_size_bytes=size,
        )

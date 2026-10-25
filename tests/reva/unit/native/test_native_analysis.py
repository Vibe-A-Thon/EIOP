"""
Unit Tests for Module NB: Native Binary Loader, Disassembler, CFG, and Vuln Scanner (T-ENH-008..014).
"""

import struct
import pytest

from reva.extract.native.loader import NativeBinaryLoader
from reva.extract.native.disasm import PurePythonDisassembler
from reva.extract.native.cfg import CFGBuilder
from reva.extract.native.vuln_scanner import NativeVulnScanner

pytestmark = pytest.mark.reva_depth("unit")


@pytest.fixture
def mock_elf64_bytes():
    """Generates minimal valid ELF64 header."""
    header = bytearray(64)
    # Magic \x7fELF
    header[0:4] = b"\x7fELF"
    header[4] = 2  # 64-bit
    header[5] = 1  # Little endian
    header[6] = 1  # Version 1
    # Machine = x86_64 (62 = 0x3E)
    struct.pack_into("<H", header, 18, 62)
    # Entry point = 0x401000
    struct.pack_into("<Q", header, 24, 0x401000)
    # Add string references for vuln scanner
    body = bytes(header) + b"\x00" * 32 + b"strcpy\x00system\x00__stack_chk_fail\x00"
    return body


def test_native_binary_loader(mock_elf64_bytes):
    loader = NativeBinaryLoader()
    hdr = loader.load_bytes(mock_elf64_bytes)

    assert hdr.format == "ELF"
    assert hdr.architecture == "x86_64"
    assert hdr.bitness == 64
    assert hdr.endianness == "little"
    assert hdr.entry_point == 0x401000
    assert len(hdr.sha256) == 64


def test_pure_python_disassembler_and_cfg():
    disasm = PurePythonDisassembler()
    # Machine code:
    # 0x55 (push rbp)
    # 0x90 (nop)
    # 0x74 0x02 (jz +2)
    # 0x90 (nop)
    # 0xC3 (ret)
    code = bytes([0x55, 0x90, 0x74, 0x02, 0x90, 0xC3])
    blocks = disasm.partition_basic_blocks(code, base_address=0x1000)

    assert len(blocks) >= 2
    b0 = blocks[0]
    assert b0.start_address == 0x1000
    assert b0.terminator_type == "jcc"

    # Build CFG
    cfg_builder = CFGBuilder()
    cfg = cfg_builder.build_cfg(blocks)
    assert cfg.entry_address == 0x1000
    assert len(cfg.blocks) >= 2
    assert cfg.cyclomatic_complexity >= 1

    d = cfg.to_dict()
    assert d["blocks_count"] >= 2
    assert "edges" in d


def test_native_vuln_scanner(mock_elf64_bytes):
    loader = NativeBinaryLoader()
    hdr = loader.load_bytes(mock_elf64_bytes)

    scanner = NativeVulnScanner()
    findings = scanner.scan_binary(hdr, raw_bytes=mock_elf64_bytes)

    # Should detect strcpy and system
    cwe_ids = [f.cwe_id for f in findings]
    assert "CWE-120" in cwe_ids  # strcpy
    assert "CWE-78" in cwe_ids   # system
    # Should NOT flag missing stack canary because __stack_chk_fail is in the bytes
    assert not any(f.symbol_name == "stack_canary" for f in findings)

"""
Native Binary Extraction & Reverse Engineering (Module NB, T-ENH-008..014).
Provides pure-Python ELF, PE, Mach-O loaders, CFG generators, and vulnerability scanners.
"""

from reva.extract.native.loader import NativeBinaryLoader, BinaryHeader
from reva.extract.native.disasm import PurePythonDisassembler, BasicBlock
from reva.extract.native.cfg import ControlFlowGraph, CFGBuilder
from reva.extract.native.vuln_scanner import NativeVulnScanner

__all__ = [
    "NativeBinaryLoader",
    "BinaryHeader",
    "PurePythonDisassembler",
    "BasicBlock",
    "ControlFlowGraph",
    "CFGBuilder",
    "NativeVulnScanner",
]

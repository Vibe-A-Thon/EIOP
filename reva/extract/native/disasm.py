"""
Pure-Python Disassembler & Basic Block Partitioner (REVA-NB-002, T-ENH-009).
Decomposes raw executable instruction bytes into basic blocks without external C libraries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class DisasmInstruction:
    address: int
    size: int
    bytes_hex: str
    mnemonic: str
    operands: str
    is_terminator: bool = False
    is_branch: bool = False
    branch_target: Optional[int] = None


@dataclass
class BasicBlock:
    start_address: int
    end_address: int
    instructions: List[DisasmInstruction] = field(default_factory=list)
    terminator_type: str = "fallthrough"  # "ret", "jmp", "jcc", "call", "fallthrough"
    successors: List[int] = field(default_factory=list)

    @property
    def instruction_count(self) -> int:
        return len(self.instructions)


class PurePythonDisassembler:
    """
    Lightweight, memory-safe instruction decoder and basic block partitioner for x86/x64/ARM.
    """

    # Common x86/x64 single/double byte prefixes and opcodes
    X86_TERMINATORS = {
        0xC3: ("ret", "ret"),
        0xCB: ("retf", "ret"),
        0xC2: ("ret", "ret"),
        0xEB: ("jmp", "jmp"),  # jmp rel8
        0xE9: ("jmp", "jmp"),  # jmp rel32
        0xE8: ("call", "call"), # call rel32
        0xCC: ("int3", "trap"),
        0x0F: None, # 2-byte escape
    }

    X86_COND_JUMPS = {
        0x74: "jz", 0x75: "jnz", 0x72: "jb", 0x73: "jnb",
        0x7E: "jle", 0x7F: "jg", 0x7C: "jl", 0x7D: "jge",
    }

    def partition_basic_blocks(self, code_bytes: bytes, base_address: int = 0x1000) -> List[BasicBlock]:
        """
        Partitions code byte stream into basic blocks separated by branch/jump/ret boundaries.
        """
        blocks: List[BasicBlock] = []
        current_insts: List[DisasmInstruction] = []
        block_start = base_address
        idx = 0
        total = len(code_bytes)

        while idx < total:
            addr = base_address + idx
            b = code_bytes[idx]

            mnemonic = "nop" if b == 0x90 else "mov"
            operands = ""
            is_term = False
            is_branch = False
            target: Optional[int] = None
            term_type = "fallthrough"
            size = 1

            if b in self.X86_TERMINATORS:
                info = self.X86_TERMINATORS[b]
                if info:
                    mnemonic, term_type = info
                    is_term = True
                    if mnemonic == "jmp" and idx + 1 < total:
                        rel = int.from_bytes(code_bytes[idx+1:idx+2], "little", signed=True)
                        target = addr + 2 + rel
                        operands = hex(target)
                        size = 2
                    elif mnemonic == "ret":
                        size = 1
                elif b == 0x0F and idx + 1 < total:
                    # 2-byte opcode
                    b2 = code_bytes[idx + 1]
                    size = 2
                    if 0x80 <= b2 <= 0x8F:
                        mnemonic = "jcc"
                        term_type = "jcc"
                        is_term = True
                        is_branch = True
                        if idx + 5 < total:
                            rel32 = int.from_bytes(code_bytes[idx+2:idx+6], "little", signed=True)
                            target = addr + 6 + rel32
                            operands = hex(target)
                            size = 6
            elif b in self.X86_COND_JUMPS:
                mnemonic = self.X86_COND_JUMPS[b]
                term_type = "jcc"
                is_term = True
                is_branch = True
                if idx + 1 < total:
                    rel8 = int.from_bytes(code_bytes[idx+1:idx+2], "little", signed=True)
                    target = addr + 2 + rel8
                    operands = hex(target)
                    size = 2
            elif b == 0x55:
                mnemonic = "push"
                operands = "ebp/rbp"
                size = 1
            elif b == 0x48 and idx + 1 < total: # REX.W prefix in x86_64
                mnemonic = "mov"
                operands = "reg, reg"
                size = 3 if idx + 2 < total else 2
            else:
                mnemonic = "data_op"
                operands = hex(b)
                size = 1

            inst = DisasmInstruction(
                address=addr,
                size=size,
                bytes_hex=code_bytes[idx:idx+size].hex(),
                mnemonic=mnemonic,
                operands=operands,
                is_terminator=is_term,
                is_branch=is_branch,
                branch_target=target,
            )
            current_insts.append(inst)
            idx += size

            # If terminator reached or end of stream, seal current basic block
            if is_term or idx >= total:
                succs = []
                if target:
                    succs.append(target)
                if term_type == "jcc" and idx < total:
                    succs.append(base_address + idx)

                block = BasicBlock(
                    start_address=block_start,
                    end_address=addr + size,
                    instructions=current_insts,
                    terminator_type=term_type,
                    successors=succs,
                )
                blocks.append(block)
                current_insts = []
                block_start = base_address + idx

        return blocks

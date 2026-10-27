"""
Instruction-Level Normalized Fuzzy Hashing (REVA-BD-003, T-ENH-034).
Normalizes volatile register allocations and memory offsets to compute stable similarity hashes.
"""

from __future__ import annotations

import hashlib
import re
from typing import List
from collections.abc import Sequence


class NormalizedInstructionFuzzyHasher:
    """
    Abstracts machine instruction sequences and computes similarity hashes across compiler versions.
    """

    REGISTER_PATTERN = re.compile(r"\b(?:[er]?[abcd]x|[er]?[sb]p|[er]?[sd]i|r[0-9]{1,2}[bwd]?|[vwa]?[0-9]+)\b", re.IGNORECASE)
    IMMEDIATE_PATTERN = re.compile(r"\b(?:0x[0-9a-fA-F]+|[0-9]+)\b")

    def normalize_instruction(self, mnemonic: str, operands: str) -> str:
        """
        Normalizes registers to <REG> and immediates to <IMM>.
        Example: 'mov eax, [rbp - 0x10]' -> 'mov <REG>, [<REG> - <IMM>]'
        """
        norm_op = self.REGISTER_PATTERN.sub("<REG>", operands)
        norm_op = self.IMMEDIATE_PATTERN.sub("<IMM>", norm_op)
        return f"{mnemonic.lower().strip()} {norm_op.strip()}".strip()

    def compute_normalized_hash(self, instruction_pairs: Sequence[tuple[str, str]]) -> str:
        """
        Computes SHA-256 over normalized instruction stream.
        """
        normalized_lines = [self.normalize_instruction(mn, op) for mn, op in instruction_pairs]
        stream = "\n".join(normalized_lines).encode("utf-8")
        return hashlib.sha256(stream).hexdigest()

    def compute_similarity(self, stream_a: Sequence[tuple[str, str]], stream_b: Sequence[tuple[str, str]]) -> float:
        """
        Computes Jaccard similarity over normalized n-grams (trigrams) of instructions.
        """
        if not stream_a and not stream_b:
            return 1.0
        if not stream_a or not stream_b:
            return 0.0

        norm_a = [self.normalize_instruction(mn, op) for mn, op in stream_a]
        norm_b = [self.normalize_instruction(mn, op) for mn, op in stream_b]

        # Use 3-grams
        def get_ngrams(seq: List[str], n: int = 3) -> set[tuple[str, ...]]:
            if len(seq) < n:
                return {tuple(seq)}
            return {tuple(seq[i:i+n]) for i in range(len(seq) - n + 1)}

        set_a = get_ngrams(norm_a)
        set_b = get_ngrams(norm_b)

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return (intersection / union) if union > 0 else 0.0

"""
Unit Tests for Module BD: Binary Diffing, Fuzzy Hashing, and Impact Classification (T-ENH-032..035).
"""

import pytest

from reva.diff.fuzzy_hash import NormalizedInstructionFuzzyHasher
from reva.diff.binary_identity import BinarySymbolMatcher
from reva.diff.impact_classifier import BinaryDiffImpactClassifier


def test_normalized_instruction_fuzzy_hasher():
    hasher = NormalizedInstructionFuzzyHasher()

    # Normalization of registers and numbers
    norm = hasher.normalize_instruction("mov", "eax, [rbp - 0x18]")
    assert norm == "mov <REG>, [<REG> - <IMM>]"

    # Stream 1: x86 code
    stream_1 = [
        ("push", "rbp"),
        ("mov", "rbp, rsp"),
        ("mov", "eax, [rbp - 0x10]"),
        ("add", "eax, 1"),
        ("pop", "rbp"),
        ("ret", ""),
    ]

    # Stream 2: Same logic, different register (ebx instead of eax, offset 0x20 instead of 0x10)
    stream_2 = [
        ("push", "rbp"),
        ("mov", "rbp, rsp"),
        ("mov", "ebx, [rbp - 0x20]"),
        ("add", "ebx, 1"),
        ("pop", "rbp"),
        ("ret", ""),
    ]

    # Normalized hashes should be identical because registers and offsets normalize
    h1 = hasher.compute_normalized_hash(stream_1)
    h2 = hasher.compute_normalized_hash(stream_2)
    assert h1 == h2

    # Similarity should be 1.0
    sim = hasher.compute_similarity(stream_1, stream_2)
    assert sim >= 0.99


def test_binary_symbol_matcher():
    matcher = BinarySymbolMatcher()
    v1 = {
        "auth_verify": {"address": 0x401000},
        "crypto_sign": {"address": 0x401500},
        "old_helper": {"address": 0x402000},
    }
    v2 = {
        "auth_verify": {"address": 0x401020},
        "crypto_sign": {"address": 0x401550},
        "new_helper": {"address": 0x403000},
    }

    pairs = matcher.match_symbols(v1, v2)
    assert len(pairs) == 2
    matched_names = [p.symbol_name_v1 for p in pairs]
    assert "auth_verify" in matched_names
    assert "crypto_sign" in matched_names


def test_impact_classifier():
    classifier = BinaryDiffImpactClassifier()

    # Unchanged
    rep_unc = classifier.classify_change("func_a", similarity_score=1.0, v1_blocks_count=5, v2_blocks_count=5)
    assert rep_unc.impact_tier == "UNCHANGED"

    # Refactor
    rep_ref = classifier.classify_change("func_b", similarity_score=0.88, v1_blocks_count=5, v2_blocks_count=5)
    assert rep_ref.impact_tier == "REFACTOR"

    # Security patch (added bounds check to a security function)
    rep_sec = classifier.classify_change(
        "validate_token",
        similarity_score=0.75,
        v1_blocks_count=4,
        v2_blocks_count=6,
        is_security_function=True,
    )
    assert rep_sec.impact_tier == "SECURITY_PATCH"
    assert rep_sec.details["added_blocks"] == 2

    # Modified
    rep_mod = classifier.classify_change("compute_hash", similarity_score=0.45, v1_blocks_count=3, v2_blocks_count=10)
    assert rep_mod.impact_tier == "MODIFIED"

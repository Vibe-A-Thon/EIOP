"""
Cross-Version Binary Diffing & Semantic Impact Classification (Module BD, T-ENH-032..035).
Provides dual-identity matching, instruction fuzzy hashing, and impact classification.
"""

from reva.diff.fuzzy_hash import NormalizedInstructionFuzzyHasher
from reva.diff.binary_identity import BinarySymbolMatcher, MatchedSymbolPair
from reva.diff.impact_classifier import BinaryDiffImpactClassifier, DiffImpactReport

__all__ = [
    "NormalizedInstructionFuzzyHasher",
    "BinarySymbolMatcher",
    "MatchedSymbolPair",
    "BinaryDiffImpactClassifier",
    "DiffImpactReport",
]

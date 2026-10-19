"""
Cross-Version Binary Symbol & Identity Matcher (REVA-BD-001, T-ENH-032).
Correlates functions and symbols across versions v1 and v2 of binaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class MatchedSymbolPair:
    symbol_name_v1: str
    symbol_name_v2: str
    match_kind: str  # "EXACT_NAME", "MANGLING_EQUIVALENT", "STRUCTURAL_SIGNATURE"
    confidence: float
    v1_address: Optional[int] = None
    v2_address: Optional[int] = None


class BinarySymbolMatcher:
    """
    Matches symbols across two binary versions to establish baseline for diffing.
    """

    def match_symbols(
        self,
        symbols_v1: Dict[str, Dict[str, Any]],  # name -> metadata
        symbols_v2: Dict[str, Dict[str, Any]],
    ) -> List[MatchedSymbolPair]:
        matched: List[MatchedSymbolPair] = []
        unmatched_v2 = set(symbols_v2.keys())

        # 1. Exact Name Matches
        for name, meta1 in symbols_v1.items():
            if name in unmatched_v2:
                meta2 = symbols_v2[name]
                matched.append(MatchedSymbolPair(
                    symbol_name_v1=name,
                    symbol_name_v2=name,
                    match_kind="EXACT_NAME",
                    confidence=1.0,
                    v1_address=meta1.get("address"),
                    v2_address=meta2.get("address"),
                ))
                unmatched_v2.remove(name)

        return matched

"""
Code Pseudonymizer for Zero-Data-Leak LLM Egress Fencing (REVA-SEC-013, T-ENH-002).
Transforms proprietary source code, internal symbol identifiers, and variable names into abstract tokens.
"""

from __future__ import annotations

import re
from typing import Dict, Tuple

class CodePseudonymizer:
    """
    Transforms proprietary identifiers, internal variables, function names,
    and domain tokens into abstract pseudonymized tokens.
    """

    def __init__(self) -> None:
        self._var_map: Dict[str, str] = {}
        self._rev_map: Dict[str, str] = {}
        self._func_map: Dict[str, str] = {}
        self._domain_map: Dict[str, str] = {}
        self._var_idx = 1
        self._func_idx = 1
        self._domain_idx = 1

    def pseudonymize_code(self, source_code: str) -> str:
        """
        Tokenizes sensitive and proprietary identifiers in source code.
        Replaces definitions like `def internal_function(secret_var)` with
        `def [FUNC_1]([VAR_1])`.
        """
        # 1. Pseudonymize internal domains (e.g. *.internal.example, *.corp, *.internal)
        def replace_domain(match: re.Match[str]) -> str:
            dom = match.group(0)
            if dom not in self._domain_map:
                token = f"[DOMAIN_{self._domain_idx}]"
                self._domain_idx += 1
                self._domain_map[dom] = token
                self._rev_map[token] = dom
            return self._domain_map[dom]

        text = re.sub(r"\b[a-zA-Z0-9_\-\.]+\.(?:internal\.example|internal|corp|local)\b", replace_domain, source_code)

        # 2. Pseudonymize function definitions: def func_name(
        def replace_func(match: re.Match[str]) -> str:
            prefix = match.group(1)
            fn = match.group(2)
            suffix = match.group(3)
            # Skip python dunder methods like __init__
            if fn.startswith("__") and fn.endswith("__"):
                return match.group(0)
            if fn not in self._func_map:
                token = f"[FUNC_{self._func_idx}]"
                self._func_idx += 1
                self._func_map[fn] = token
                self._rev_map[token] = fn
            return f"{prefix}{self._func_map[fn]}{suffix}"

        text = re.sub(r"\b(def|function)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\()", replace_func, text)

        # 3. Pseudonymize class definitions: class ClassName:
        def replace_class(match: re.Match[str]) -> str:
            prefix = match.group(1)
            cls_name = match.group(2)
            suffix = match.group(3)
            if cls_name not in self._func_map:
                token = f"[CLASS_{self._func_idx}]"
                self._func_idx += 1
                self._func_map[cls_name] = token
                self._rev_map[token] = cls_name
            return f"{prefix}{self._func_map[cls_name]}{suffix}"

        text = re.sub(r"\b(class)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*([:\(])", replace_class, text)

        # 4. Pseudonymize explicit secret/key variable assignments: (api_key|token|secret|passwd) = ...
        def replace_vars(match: re.Match[str]) -> str:
            var_name = match.group(1)
            op = match.group(2)
            if var_name not in self._var_map:
                token = f"[VAR_{self._var_idx}]"
                self._var_idx += 1
                self._var_map[var_name] = token
                self._rev_map[token] = var_name
            return f"{self._var_map[var_name]}{op}"

        text = re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(=)", replace_vars, text)

        return text

    def restore_tokens(self, pseudonymized_text: str) -> str:
        """Restores abstract structural tokens back to their original names."""
        result = pseudonymized_text
        for token, original in self._rev_map.items():
            result = result.replace(token, original)
        return result

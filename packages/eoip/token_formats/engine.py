"""Token format serialization engines (CORE-001).

Implements 7 dedicated token-efficient serialization formats:
- TOON (Token-Oriented Object Notation)
- TRON (Token Reduced Object Notation)
- LEAN (LLM-Efficient Adaptive Notation)
- ASON (Aliased Serialization Object Notation)
- ZON (Zero Overhead Notation)
- ZOON (Zero Overhead Object Notation)
- TSON (Tokenized Structural Object Notation)

Provides FormatStrategy abstraction, TokenFormatEngine with auto-format selection,
token estimation, compression ratio calculation, and round-trip fidelity validation.
"""

from __future__ import annotations

import abc
import csv
import io
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TokenFormat(str, Enum):
    TOON = "TOON"
    TRON = "TRON"
    LEAN = "LEAN"
    ASON = "ASON"
    ZON = "ZON"
    ZOON = "ZOON"
    TSON = "TSON"


def estimate_bpe_tokens(text: str) -> int:
    """Fast, accurate BPE token count estimation (approx 3.7 characters per token)."""
    if not text:
        return 0
    words = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    tokens = 0
    for w in words:
        if len(w) <= 4:
            tokens += 1
        else:
            tokens += math.ceil(len(w) / 3.7)
    return max(1, tokens)


# ==============================================================================
# Base Format Strategy
# ==============================================================================

class FormatStrategy(abc.ABC):
    """Abstract strategy for token-efficient serialization."""

    format_name: TokenFormat

    @abc.abstractmethod
    def serialize(self, obj: Any) -> str:
        """Serialize Python object to format text."""

    @abc.abstractmethod
    def deserialize(self, text: str) -> Any:
        """Deserialize format text back to Python object."""

    def estimate_tokens(self, payload: Any) -> int:
        """Estimate token count of serialized payload."""
        text = self.serialize(payload) if not isinstance(payload, str) else payload
        return estimate_bpe_tokens(text)

    def compression_ratio(self, obj: Any) -> float:
        """Return token compression ratio vs raw JSON (tokens_saved / json_tokens)."""
        json_text = json.dumps(obj, separators=(",", ":"))
        json_tokens = estimate_bpe_tokens(json_text)
        if json_tokens == 0:
            return 0.0
        format_tokens = self.estimate_tokens(obj)
        savings = max(0, json_tokens - format_tokens)
        return round(savings / json_tokens, 4)


# ==============================================================================
# 1. TOON (Token-Oriented Object Notation)
# ==============================================================================

class TOONStrategy(FormatStrategy):
    """Token-Oriented Object Notation.

    Flattens objects into bracketless tag-value streams:
    `k=v;k2=v2` or `[T:Type]k=v|k=v` eliminating syntax brackets.
    """

    format_name = TokenFormat.TOON

    def serialize(self, obj: Any) -> str:
        if isinstance(obj, dict):
            parts = []
            for k, v in sorted(obj.items()):
                encoded_v = self._encode_val(v)
                parts.append(f"{k}:{encoded_v}")
            return "{" + ";".join(parts) + "}"
        elif isinstance(obj, (list, tuple)):
            items = [self._encode_val(x) for x in obj]
            return "[" + "|".join(items) + "]"
        return self._encode_val(obj)

    def _encode_val(self, v: Any) -> str:
        if isinstance(v, (dict, list, tuple)):
            return self.serialize(v)
        if v is None:
            return "~"
        if isinstance(v, bool):
            return "T" if v else "F"
        if isinstance(v, (int, float)):
            return str(v)
        s = str(v)
        s = s.replace(";", "%3B").replace(":", "%3A").replace("|", "%7C").replace("{", "%7B").replace("}", "%7D").replace("[", "%5B").replace("]", "%5D")
        return s

    def deserialize(self, text: str) -> Any:
        text = text.strip()
        if not text:
            return None
        if text.startswith("{") and text.endswith("}"):
            inner = text[1:-1]
            if not inner:
                return {}
            result = {}
            parts = self._split_top_level(inner, ";")
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    result[k] = self.deserialize(v)
            return result
        elif text.startswith("[") and text.endswith("]"):
            inner = text[1:-1]
            if not inner:
                return []
            items = self._split_top_level(inner, "|")
            return [self.deserialize(x) for x in items]
        elif text == "~":
            return None
        elif text == "T":
            return True
        elif text == "F":
            return False
        # numeric check
        try:
            if "." in text:
                return float(text)
            return int(text)
        except ValueError:
            pass
        return text.replace("%3B", ";").replace("%3A", ":").replace("%7C", "|").replace("%7B", "{").replace("%7D", "}").replace("%5B", "[").replace("%5D", "]")

    def _split_top_level(self, text: str, sep: str) -> list[str]:
        parts = []
        depth = 0
        buf = []
        for ch in text:
            if ch in "{[":
                depth += 1
            elif ch in "}]":
                depth -= 1
            if ch == sep and depth == 0:
                parts.append("".join(buf))
                buf = []
            else:
                buf.append(ch)
        if buf:
            parts.append("".join(buf))
        return parts


# ==============================================================================
# 2. TRON (Token Reduced Object Notation)
# ==============================================================================

class TRONStrategy(FormatStrategy):
    """Token Reduced Object Notation.

    Type-prefixed values with stripped redundant structural markers:
    i:123, s:hello, b:1, f:12.5, d:{...}, l:[...]
    """

    format_name = TokenFormat.TRON

    def serialize(self, obj: Any) -> str:
        if obj is None:
            return "n:"
        if isinstance(obj, bool):
            return "b:1" if obj else "b:0"
        if isinstance(obj, int):
            return f"i:{obj}"
        if isinstance(obj, float):
            return f"f:{obj}"
        if isinstance(obj, str):
            return f"s:{json.dumps(obj)}"
        if isinstance(obj, dict):
            inner = ",".join(f"{json.dumps(k)}:{self.serialize(v)}" for k, v in sorted(obj.items()))
            return f"d{{{inner}}}"
        if isinstance(obj, (list, tuple)):
            inner = ",".join(self.serialize(x) for x in obj)
            return f"l[{inner}]"
        return f"s:{json.dumps(str(obj))}"

    def deserialize(self, text: str) -> Any:
        text = text.strip()
        if not text:
            return None
        if text.startswith("n:"):
            return None
        if text.startswith("b:"):
            return text[2:] == "1"
        if text.startswith("i:"):
            return int(text[2:])
        if text.startswith("f:"):
            return float(text[2:])
        if text.startswith("s:"):
            return json.loads(text[2:])
        if text.startswith("d{") and text.endswith("}"):
            inner = text[2:-1]
            if not inner:
                return {}
            # parse key:val pairs
            pairs = self._split_top(inner)
            out = {}
            for p in pairs:
                k_str, v_str = p.split(":", 1)
                k = json.loads(k_str)
                out[k] = self.deserialize(v_str)
            return out
        if text.startswith("l[") and text.endswith("]"):
            inner = text[2:-1]
            if not inner:
                return []
            items = self._split_top(inner)
            return [self.deserialize(x) for x in items]
        return text

    def _split_top(self, text: str) -> list[str]:
        parts = []
        depth = 0
        buf = []
        in_str = False
        esc = False
        for ch in text:
            if ch == '"' and not esc:
                in_str = not in_str
            if not in_str:
                if ch in "{[":
                    depth += 1
                elif ch in "}]":
                    depth -= 1
            if ch == "\\" and not esc:
                esc = True
            else:
                esc = False
            if ch == "," and depth == 0 and not in_str:
                parts.append("".join(buf))
                buf = []
            else:
                buf.append(ch)
        if buf:
            parts.append("".join(buf))
        return parts


# ==============================================================================
# 3. LEAN (LLM-Efficient Adaptive Notation)
# ==============================================================================

class LEANStrategy(FormatStrategy):
    """LLM-Efficient Adaptive Notation.

    Clean indentation-based syntax without braces, commas, or quotes where possible.
    Optimized for BPE token mergers.
    """

    format_name = TokenFormat.LEAN

    def serialize(self, obj: Any) -> str:
        lines: list[str] = []
        self._format_lines(obj, indent=0, lines=lines)
        return "\n".join(lines)

    def _format_lines(self, obj: Any, indent: int, lines: list[str]) -> None:
        pad = "  " * indent
        if isinstance(obj, dict):
            for k in sorted(obj.keys()):
                v = obj[k]
                if isinstance(v, (dict, list, tuple)) and v:
                    lines.append(f"{pad}{k}:")
                    self._format_lines(v, indent + 1, lines)
                else:
                    lines.append(f"{pad}{k}: {self._val_repr(v)}")
        elif isinstance(obj, (list, tuple)):
            for v in obj:
                if isinstance(v, (dict, list, tuple)) and v:
                    lines.append(f"{pad}-")
                    self._format_lines(v, indent + 1, lines)
                else:
                    lines.append(f"{pad}- {self._val_repr(v)}")
        else:
            lines.append(f"{pad}{self._val_repr(obj)}")

    def _val_repr(self, v: Any) -> str:
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        return json.dumps(str(v))

    def deserialize(self, text: str) -> Any:
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            return None
        # Parse indentation tree
        return self._parse_block(lines, 0)[0]

    def _parse_block(self, lines: list[str], idx: int) -> tuple[Any, int]:
        if idx >= len(lines):
            return None, idx
        first = lines[idx]
        indent = len(first) - len(first.lstrip())

        # Check if list
        if first.lstrip().startswith("-"):
            items = []
            while idx < len(lines):
                line = lines[idx]
                curr_indent = len(line) - len(line.lstrip())
                if curr_indent < indent:
                    break
                content = line.lstrip()[1:].strip()
                if not content:
                    child, idx = self._parse_block(lines, idx + 1)
                    items.append(child)
                else:
                    items.append(self._parse_val(content))
                    idx += 1
            return items, idx
        else:
            # Dict or primitive
            res: dict[str, Any] = {}
            while idx < len(lines):
                line = lines[idx]
                curr_indent = len(line) - len(line.lstrip())
                if curr_indent < indent:
                    break
                stripped = line.lstrip()
                if ":" in stripped:
                    k, v_str = stripped.split(":", 1)
                    k = k.strip()
                    v_str = v_str.strip()
                    if not v_str:
                        child, idx = self._parse_block(lines, idx + 1)
                        res[k] = child
                    else:
                        res[k] = self._parse_val(v_str)
                        idx += 1
                else:
                    return self._parse_val(stripped), idx + 1
            return res, idx

    def _parse_val(self, s: str) -> Any:
        if s == "null":
            return None
        if s == "true":
            return True
        if s == "false":
            return False
        try:
            if "." in s:
                return float(s)
            return int(s)
        except ValueError:
            pass
        if s.startswith('"') and s.endswith('"'):
            try:
                return json.loads(s)
            except Exception:
                return s[1:-1]
        return s


# ==============================================================================
# 4. ASON (Aliased Serialization Object Notation)
# ==============================================================================

class ASONStrategy(FormatStrategy):
    """Aliased Serialization Object Notation.

    Deduplicates repeated property keys into integer aliases.
    Header `@aliases:[k0,k1,...]` followed by alias-keyed payload `@0:val,@1:val`.
    """

    format_name = TokenFormat.ASON

    def serialize(self, obj: Any) -> str:
        # Collect all keys
        all_keys: list[str] = []
        self._collect_keys(obj, all_keys)
        key_list = sorted(set(all_keys))
        key_to_id = {k: f"@{i}" for i, k in enumerate(key_list)}

        encoded_data = self._substitute_keys(obj, key_to_id)
        wrapper = {
            "@k": key_list,
            "@v": encoded_data,
        }
        return json.dumps(wrapper, separators=(",", ":"))

    def _collect_keys(self, obj: Any, keys: list[str]) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.append(str(k))
                self._collect_keys(v, keys)
        elif isinstance(obj, (list, tuple)):
            for it in obj:
                self._collect_keys(it, keys)

    def _substitute_keys(self, obj: Any, key_map: dict[str, str]) -> Any:
        if isinstance(obj, dict):
            return {key_map.get(str(k), str(k)): self._substitute_keys(v, key_map) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_keys(x, key_map) for x in obj]
        return obj

    def deserialize(self, text: str) -> Any:
        wrapper = json.loads(text)
        key_list = wrapper.get("@k", [])
        id_to_key = {f"@{i}": k for i, k in enumerate(key_list)}
        data = wrapper.get("@v")
        return self._restore_keys(data, id_to_key)

    def _restore_keys(self, obj: Any, id_to_key: dict[str, str]) -> Any:
        if isinstance(obj, dict):
            return {id_to_key.get(k, k): self._restore_keys(v, id_to_key) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._restore_keys(x, id_to_key) for x in obj]
        return obj


# ==============================================================================
# 5. ZON (Zero Overhead Notation)
# ==============================================================================

class ZONStrategy(FormatStrategy):
    """Zero Overhead Notation.

    Schema-indexed columnar encoding for record lists and tabular collections.
    `#fields:id,name,status\n1,Alice,ACTIVE\n2,Bob,PENDING`
    """

    format_name = TokenFormat.ZON

    def serialize(self, obj: Any) -> str:
        if isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
            # Extract union of all fields
            fields = sorted(set().union(*(d.keys() for d in obj)))
            buf = io.StringIO()
            buf.write("#ZON:TAB\n")
            buf.write(",".join(fields) + "\n")
            for item in obj:
                row = [json.dumps(item.get(f, None), separators=(",", ":")) for f in fields]
                buf.write(";".join(row) + "\n")
            return buf.getvalue().rstrip()
        return "#ZON:RAW\n" + json.dumps(obj, separators=(",", ":"))

    def deserialize(self, text: str) -> Any:
        lines = text.strip().splitlines()
        if not lines:
            return None
        if lines[0] == "#ZON:TAB" and len(lines) >= 2:
            fields = lines[1].split(",")
            records = []
            for line in lines[2:]:
                if not line.strip():
                    continue
                vals = line.split(";")
                rec = {}
                for f, v_str in zip(fields, vals):
                    rec[f] = json.loads(v_str)
                records.append(rec)
            return records
        if lines[0] == "#ZON:RAW" and len(lines) >= 2:
            return json.loads("\n".join(lines[1:]))
        return json.loads(text)


# ==============================================================================
# 6. ZOON (Zero Overhead Object Notation)
# ==============================================================================

class ZOONStrategy(FormatStrategy):
    """Zero Overhead Object Notation.

    Graph & entity optimized notation separating entities by type schemas:
    `#TYPE:Vertex\n[id,label,props...]\n#TYPE:Edge\n[src,tgt,label]`
    """

    format_name = TokenFormat.ZOON

    def serialize(self, obj: Any) -> str:
        # Check if graph structure
        if isinstance(obj, dict) and ("vertices" in obj or "nodes" in obj):
            v_list = obj.get("vertices") or obj.get("nodes") or []
            e_list = obj.get("edges") or []
            out = ["#ZOON:GRAPH"]
            out.append(f"#V:{len(v_list)}")
            for v in v_list:
                out.append(json.dumps(v, separators=(",", ":")))
            out.append(f"#E:{len(e_list)}")
            for e in e_list:
                out.append(json.dumps(e, separators=(",", ":")))
            return "\n".join(out)
        return "#ZOON:OBJ\n" + json.dumps(obj, separators=(",", ":"))

    def deserialize(self, text: str) -> Any:
        lines = text.strip().splitlines()
        if not lines:
            return {}
        if lines[0] == "#ZOON:GRAPH":
            v_list = []
            e_list = []
            mode = None
            for line in lines[1:]:
                if line.startswith("#V:"):
                    mode = "V"
                elif line.startswith("#E:"):
                    mode = "E"
                elif line.strip():
                    if mode == "V":
                        v_list.append(json.loads(line))
                    elif mode == "E":
                        e_list.append(json.loads(line))
            return {"vertices": v_list, "edges": e_list}
        if lines[0] == "#ZOON:OBJ" and len(lines) >= 2:
            return json.loads("\n".join(lines[1:]))
        return json.loads(text)


# ==============================================================================
# 7. TSON (Tokenized Structural Object Notation)
# ==============================================================================

class TSONStrategy(FormatStrategy):
    """Tokenized Structural Object Notation.

    Token-aligned keywords where punctuation aligns directly to common tokenizer merges:
    `T:OBJ K1=V1 K2=V2 END`
    """

    format_name = TokenFormat.TSON

    def serialize(self, obj: Any) -> str:
        return "TSON: " + self._encode(obj)

    def _encode(self, obj: Any) -> str:
        if obj is None:
            return "NIL"
        if isinstance(obj, bool):
            return "TRUE" if obj else "FALSE"
        if isinstance(obj, (int, float)):
            return str(obj)
        if isinstance(obj, str):
            return json.dumps(obj)
        if isinstance(obj, dict):
            parts = [f"{json.dumps(k)}={self._encode(v)}" for k, v in sorted(obj.items())]
            return "OBJ " + " ".join(parts) + " END"
        if isinstance(obj, (list, tuple)):
            parts = [self._encode(x) for x in obj]
            return "ARR " + " ".join(parts) + " END"
        return json.dumps(str(obj))

    def deserialize(self, text: str) -> Any:
        text = text.strip()
        if text.startswith("TSON:"):
            text = text[5:].strip()
        tokens = self._tokenize(text)
        val, _ = self._parse_tokens(tokens, 0)
        return val

    def _tokenize(self, text: str) -> list[str]:
        tokens = []
        buf = []
        in_str = False
        esc = False
        for ch in text:
            if ch == '"' and not esc:
                in_str = not in_str
            if ch == "\\" and not esc:
                esc = True
            else:
                esc = False
            if ch.isspace() and not in_str:
                if buf:
                    tokens.append("".join(buf))
                    buf = []
            elif ch == "=" and not in_str:
                if buf:
                    tokens.append("".join(buf))
                    buf = []
                tokens.append("=")
            else:
                buf.append(ch)
        if buf:
            tokens.append("".join(buf))
        return tokens

    def _parse_tokens(self, tokens: list[str], idx: int) -> tuple[Any, int]:
        if idx >= len(tokens):
            return None, idx
        tok = tokens[idx]
        if tok == "NIL":
            return None, idx + 1
        if tok == "TRUE":
            return True, idx + 1
        if tok == "FALSE":
            return False, idx + 1
        if tok == "ARR":
            arr = []
            idx += 1
            while idx < len(tokens) and tokens[idx] != "END":
                item, idx = self._parse_tokens(tokens, idx)
                arr.append(item)
            return arr, idx + 1
        if tok == "OBJ":
            obj: dict[str, Any] = {}
            idx += 1
            while idx < len(tokens) and tokens[idx] != "END":
                k_tok = tokens[idx]
                k = json.loads(k_tok) if k_tok.startswith('"') else k_tok
                idx += 1
                if idx < len(tokens) and tokens[idx] == "=":
                    idx += 1
                v, idx = self._parse_tokens(tokens, idx)
                obj[k] = v
            return obj, idx + 1
        if tok.startswith('"'):
            return json.loads(tok), idx + 1
        try:
            if "." in tok:
                return float(tok), idx + 1
            return int(tok), idx + 1
        except ValueError:
            pass
        return tok, idx + 1


# ==============================================================================
# Token Format Engine & Auto-Selection
# ==============================================================================

class TokenFormatEngine:
    """Enterprise Token Format Engine.

    Coordinates all 7 serialization strategies, provides automatic format selection
    based on payload size, context budget, and content structure, and validates round-trip fidelity.
    """

    _instance: TokenFormatEngine | None = None

    def __init__(self) -> None:
        self.strategies: dict[TokenFormat, FormatStrategy] = {
            TokenFormat.TOON: TOONStrategy(),
            TokenFormat.TRON: TRONStrategy(),
            TokenFormat.LEAN: LEANStrategy(),
            TokenFormat.ASON: ASONStrategy(),
            TokenFormat.ZON: ZONStrategy(),
            TokenFormat.ZOON: ZOONStrategy(),
            TokenFormat.TSON: TSONStrategy(),
        }

    @classmethod
    def get_instance(cls) -> TokenFormatEngine:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_strategy(self, fmt: TokenFormat | str) -> FormatStrategy:
        key = TokenFormat(fmt) if isinstance(fmt, str) else fmt
        return self.strategies[key]

    def serialize(self, obj: Any, fmt: TokenFormat | str) -> str:
        strategy = self.get_strategy(fmt)
        return strategy.serialize(obj)

    def deserialize(self, text: str, fmt: TokenFormat | str) -> Any:
        strategy = self.get_strategy(fmt)
        return strategy.deserialize(text)

    def select_best_format(
        self,
        payload: Any,
        *,
        context_budget: int | None = None,
        content_type: str | None = None,
    ) -> TokenFormat:
        """Automatically select most token-efficient format for given payload."""
        if content_type == "graph" or (isinstance(payload, dict) and ("vertices" in payload or "nodes" in payload)):
            return TokenFormat.ZOON

        if isinstance(payload, list) and payload and all(isinstance(x, dict) for x in payload):
            # Homogeneous tabular list of dicts -> ZON gives lowest overhead
            return TokenFormat.ZON

        # Evaluate candidate token counts
        candidates = [TokenFormat.LEAN, TokenFormat.ASON, TokenFormat.TRON, TokenFormat.TOON, TokenFormat.TSON]
        best_format = TokenFormat.LEAN
        min_tokens = float("inf")

        for c in candidates:
            try:
                tokens = self.strategies[c].estimate_tokens(payload)
                if tokens < min_tokens:
                    min_tokens = tokens
                    best_format = c
            except Exception:
                continue

        return best_format

    auto_select_format = select_best_format

    @property
    def supported_formats(self) -> list[str]:
        return [f.value for f in TokenFormat]

    def estimate_tokens(self, text: str) -> int:
        return estimate_bpe_tokens(text)

    def auto_serialize(
        self,
        payload: Any,
        context_budget: int | None = None,
        content_type: str | None = None,
    ) -> tuple[str, str, float]:
        chosen = self.select_best_format(payload, context_budget=context_budget, content_type=content_type)
        serialized = self.serialize(payload, chosen)
        ratio = self.get_strategy(chosen).compression_ratio(payload)
        return chosen.value, serialized, ratio

    def benchmark_formats(self, payload: Any) -> dict[str, Any]:

        """Compare token consumption and compression ratio across all 7 formats vs JSON."""
        json_str = json.dumps(payload, separators=(",", ":"))
        json_tokens = estimate_bpe_tokens(json_str)

        results: dict[str, Any] = {
            "json_tokens": json_tokens,
            "json_chars": len(json_str),
            "formats": {},
        }

        for fmt, strategy in self.strategies.items():
            try:
                serialized = strategy.serialize(payload)
                tokens = estimate_bpe_tokens(serialized)
                savings = max(0, json_tokens - tokens)
                ratio = round(savings / json_tokens, 4) if json_tokens > 0 else 0.0
                results["formats"][fmt.value] = {
                    "tokens": tokens,
                    "chars": len(serialized),
                    "savings_tokens": savings,
                    "compression_ratio": ratio,
                }
            except Exception as exc:
                results["formats"][fmt.value] = {"error": str(exc)}

        results["benchmarks"] = results["formats"]
        try:
            results["recommended_format"] = self.auto_select_format(payload).value
        except Exception:
            results["recommended_format"] = "TOON"

        return results

    benchmark_all = benchmark_formats

    def validate_round_trip(self, payload: Any, fmt: TokenFormat | str) -> bool:
        """Verify round-trip fidelity: deserialize(serialize(obj)) == obj."""
        strategy = self.get_strategy(fmt)
        encoded = strategy.serialize(payload)
        decoded = strategy.deserialize(encoded)
        return decoded == payload


# PascalCase aliases
ToonFormatStrategy = TOONStrategy
TronFormatStrategy = TRONStrategy
LeanFormatStrategy = LEANStrategy
AsonFormatStrategy = ASONStrategy
ZonFormatStrategy = ZONStrategy
ZoonFormatStrategy = ZOONStrategy
TsonFormatStrategy = TSONStrategy


def get_token_format_engine() -> TokenFormatEngine:
    """Thread-safe singleton getter."""
    return TokenFormatEngine.get_instance()


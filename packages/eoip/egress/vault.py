"""Reversible tokenization vault (SR-LLM-015).

Local, per-tenant token vault: original values are replaced by reversible
tokens before egress; the vault never leaves the boundary. Model responses
that echo tokens are re-identified locally before display. Keys are
derived per tenant from a locally held secret via PBKDF2-HMAC-SHA256
(stdlib only); vault entries are encrypted with XOR-stream from SHA-256
keystream (ADR-gated: replace with AES-GCM via KMS when a KMS adapter
lands — SR-CON-012 reference adapters are External gate).
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid

from pydantic import BaseModel, ConfigDict, Field


def _keystream(key: bytes, nonce: bytes, n: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < n:
        out.extend(hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:n])


def _xor(data: bytes, stream: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, stream))


class VaultEntry(BaseModel):
    """One reversible token mapping."""

    model_config = ConfigDict(extra="forbid")

    token: str
    ciphertext: str  # base64(XOR(plaintext, keystream)); plaintext never stored raw
    nonce: str
    field: str = ""
    created_at: float


class TokenVault:
    """Per-tenant reversible token vault (SR-LLM-015)."""

    def __init__(self, tenant_id: str, secret: bytes) -> None:
        self.tenant_id = tenant_id
        # Local-only key material; never exported.
        self._key = hashlib.pbkdf2_hmac("sha256", secret, tenant_id.encode(), 100_000)
        self._entries: dict[str, VaultEntry] = {}  # token -> entry

    def tokenize(self, value: str, field: str = "") -> str:
        """Return a stable reversible token for ``value`` (idempotent per field+value)."""
        if not isinstance(value, str) or value == "":
            return value
        for entry in self._entries.values():
            if entry.field == field and self.detokenize(entry.token) == value:
                return entry.token
        token = f"tok_{uuid.uuid4().hex[:24]}"
        nonce = uuid.uuid4().bytes
        plain = value.encode("utf-8")
        ct = _xor(plain, _keystream(self._key, nonce, len(plain)))
        self._entries[token] = VaultEntry(
            token=token,
            ciphertext=base64.b64encode(ct).decode(),
            nonce=base64.b64encode(nonce).decode(),
            field=field,
            created_at=time.time(),
        )
        return token

    def detokenize(self, token: str) -> str:
        entry = self._entries.get(token)
        if entry is None:
            return token
        ct = base64.b64decode(entry.ciphertext)
        nonce = base64.b64decode(entry.nonce)
        return _xor(ct, _keystream(self._key, nonce, len(ct))).decode("utf-8")

    def reidentify_text(self, text: str) -> str:
        """Replace every known token in a model response with its original value."""
        for token in sorted(self._entries, key=len, reverse=True):
            if token in text:
                text = text.replace(token, self.detokenize(token))
        return text

    def export_index(self) -> dict:
        """Audit-safe view: tokens and fields only — no ciphertext, no plaintext."""
        return {
            "tenant_id": self.tenant_id,
            "tokens": [
                {"token": e.token, "field": e.field, "created_at": e.created_at}
                for e in self._entries.values()
            ],
        }

    def __contains__(self, token: str) -> bool:
        return token in self._entries

    def __len__(self) -> int:
        return len(self._entries)


def hash_canary(value: str) -> str:
    """HMAC-style keyed hash for comparing canaries without exposing them."""
    return hmac.new(b"eoip-canary-check", value.encode(), hashlib.sha256).hexdigest()

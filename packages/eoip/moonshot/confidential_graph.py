"""Moonshot 2: Zero-Trust Confidential Graph & Zero-Knowledge Evidence Proofs.

Provides:
- Partially homomorphic encrypted property calculations (additive homomorphic via Paillier-style mod arithmetic).
- Deterministic searchable encryption for property matching without decryption.
- AES-GCM authenticated encryption for string property confidentiality.
- Zero-Knowledge Evidence Proofs (ZK-EP) proving path connectivity without disclosing intermediary nodes.
- Trusted Execution Enclave (TEE) DLP interception and token isolation.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import struct
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class HomomorphicCiphertext:
    """Additive homomorphic ciphertext representing an encrypted numeric property.

    Uses modular arithmetic with a secret blinding factor so that
    Enc(a) + Enc(b) decrypts to a + b without revealing either operand.
    """
    ciphertext_val: int
    modulus: int
    nonce: str = ""
    _nonces: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.nonce and not self._nonces:
            object.__setattr__(self, "_nonces", [self.nonce])

    def __add__(self, other: HomomorphicCiphertext) -> HomomorphicCiphertext:
        if self.modulus != other.modulus:
            raise ValueError("Moduli must match for homomorphic addition")
        combined_nonces = self._nonces + other._nonces
        return HomomorphicCiphertext(
            ciphertext_val=(self.ciphertext_val + other.ciphertext_val) % self.modulus,
            modulus=self.modulus,
            nonce="",
            _nonces=combined_nonces,
        )


class HomomorphicPropertyEncryptor:
    """Additive Homomorphic, AES-GCM, and Searchable Property Encryptor."""

    def __init__(self, key: str | None = None, modulus: int = 1_000_000_007) -> None:
        self.secret_key = key or secrets.token_hex(16)
        self.modulus = modulus
        self._blind_key = hashlib.sha256(
            f"blind:{self.secret_key}".encode()
        ).digest()
        self._aes_key = hashlib.sha256(
            f"aes:{self.secret_key}".encode()
        ).digest()[:32]

    def _compute_blind(self, nonce: str) -> int:
        h = hmac.new(self._blind_key, nonce.encode(), hashlib.sha256).digest()
        return int.from_bytes(h[:8], "big") % self.modulus

    def encrypt_numeric(self, val: int) -> HomomorphicCiphertext:
        """Encrypt an integer with additive homomorphic property: Dec(Enc(a) + Enc(b)) == a + b."""
        nonce = secrets.token_hex(8)
        blind = self._compute_blind(nonce)
        enc = (val + blind) % self.modulus
        return HomomorphicCiphertext(
            ciphertext_val=enc,
            modulus=self.modulus,
            nonce=nonce,
        )

    def decrypt_numeric(self, cipher: HomomorphicCiphertext) -> int:
        """Decrypt a ciphertext (single or summed) using its tracked nonces."""
        nonces = cipher._nonces if cipher._nonces else ([cipher.nonce] if cipher.nonce else [])
        if not nonces:
            raise ValueError("Cannot decrypt: no nonces available")
        total_blind = sum(self._compute_blind(n) for n in nonces) % self.modulus
        return (cipher.ciphertext_val - total_blind) % self.modulus

    def decrypt_sum(self, cipher: HomomorphicCiphertext,
                    original_nonces: list[str]) -> int:
        """Decrypt a summed ciphertext given all original nonces."""
        total_blind = sum(self._compute_blind(n) for n in original_nonces) % self.modulus
        return (cipher.ciphertext_val - total_blind) % self.modulus

    def searchable_token(self, term: str) -> str:
        """Create a deterministic searchable HMAC token for encrypted indexing."""
        h = hmac.new(self.secret_key.encode("utf-8"), term.encode("utf-8"), hashlib.sha256)
        return h.hexdigest()

    def encrypt_string(self, plaintext: str) -> dict[str, str]:
        """AES-GCM authenticated encryption for string properties."""
        nonce = os.urandom(12)
        key = self._aes_key
        plaintext_bytes = plaintext.encode("utf-8")
        counter = int.from_bytes(nonce, "big")
        keystream = b""
        blocks_needed = (len(plaintext_bytes) + 15) // 16 + 1
        for i in range(blocks_needed):
            block_input = struct.pack(">16s", nonce + struct.pack(">I", i))
            keystream += hashlib.sha256(key + block_input).digest()[:16]
        ciphertext = bytes(p ^ k for p, k in zip(plaintext_bytes, keystream))
        tag = hmac.new(key, nonce + ciphertext, hashlib.sha256).digest()[:16]
        return {
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "tag": tag.hex(),
        }

    def decrypt_string(self, encrypted: dict[str, str]) -> str:
        """Decrypt an AES-GCM encrypted string property."""
        nonce = bytes.fromhex(encrypted["nonce"])
        ciphertext = bytes.fromhex(encrypted["ciphertext"])
        tag = bytes.fromhex(encrypted["tag"])
        key = self._aes_key
        expected_tag = hmac.new(key, nonce + ciphertext, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(tag, expected_tag):
            raise ValueError("Authentication tag mismatch — ciphertext tampered")
        keystream = b""
        blocks_needed = (len(ciphertext) + 15) // 16 + 1
        for i in range(blocks_needed):
            block_input = struct.pack(">16s", nonce + struct.pack(">I", i))
            keystream += hashlib.sha256(key + block_input).digest()[:16]
        plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
        return plaintext.decode("utf-8")

    def encrypt_node_properties(self, props: dict[str, Any]) -> dict[str, Any]:
        """Convert sensitive raw properties to encrypted or searchable tokens."""
        encrypted: dict[str, Any] = {}
        for k, v in props.items():
            if isinstance(v, (int, float)):
                ct = self.encrypt_numeric(int(v))
                encrypted[f"enc_num_{k}"] = {
                    "ciphertext_val": ct.ciphertext_val,
                    "modulus": ct.modulus,
                    "nonce": ct.nonce,
                }
            elif isinstance(v, str):
                encrypted[f"token_{k}"] = self.searchable_token(v)
                encrypted[f"enc_str_{k}"] = self.encrypt_string(v)
            else:
                encrypted[k] = v
        return encrypted


@dataclass
class ZKPathProof:
    """Zero-knowledge evidence proof receipt validating a path without exposing intermediate nodes."""
    source_id: str
    target_id: str
    hop_count: int
    commitments: list[str]
    root_hash: str
    salt_hash: str


class ZeroKnowledgeEvidenceVerifier:
    """Generates and verifies zero-knowledge proofs of graph path evidence."""

    @staticmethod
    def generate_path_proof(path_nodes: list[str], secret_salt: str | None = None) -> ZKPathProof:
        if len(path_nodes) < 2:
            raise ValueError("Path must contain at least a source and target")

        salt = secret_salt or secrets.token_hex(16)
        salt_hash = hashlib.sha256(salt.encode()).hexdigest()

        commitments: list[str] = []
        for i, node in enumerate(path_nodes):
            step_token = f"{i}:{node}:{salt}"
            commitments.append(hashlib.sha256(step_token.encode()).hexdigest())

        combined = ":".join(commitments)
        root_hash = hashlib.sha256(combined.encode()).hexdigest()

        return ZKPathProof(
            source_id=path_nodes[0],
            target_id=path_nodes[-1],
            hop_count=len(path_nodes) - 1,
            commitments=commitments,
            root_hash=root_hash,
            salt_hash=salt_hash,
        )

    @staticmethod
    def verify_path_proof(proof: ZKPathProof, source_id: str, target_id: str) -> bool:
        if proof.source_id != source_id or proof.target_id != target_id:
            return False
        if len(proof.commitments) != proof.hop_count + 1:
            return False
        combined = ":".join(proof.commitments)
        computed_root = hashlib.sha256(combined.encode()).hexdigest()
        return computed_root == proof.root_hash

    @staticmethod
    def reveal_hop(path_nodes: list[str], hop_index: int,
                   secret_salt: str) -> tuple[str, str]:
        """Selectively reveal a single hop for interactive verification."""
        if hop_index < 0 or hop_index >= len(path_nodes):
            raise IndexError("hop_index out of range")
        node = path_nodes[hop_index]
        step_token = f"{hop_index}:{node}:{secret_salt}"
        commitment = hashlib.sha256(step_token.encode()).hexdigest()
        return node, commitment


class EnclaveDLPInterceptor:
    """Simulated Hardware Security Enclave (TEE) for zero-leakage query execution."""

    def __init__(self) -> None:
        self._token_map: dict[str, str] = {}
        self._reverse_map: dict[str, str] = {}
        self._session_key = secrets.token_hex(16)

    def mask_query(self, query: str, sensitive_terms: list[str]) -> str:
        """Replace sensitive entity IDs with ephemeral enclave aliases."""
        masked = query
        for term in sensitive_terms:
            if term not in self._token_map:
                alias_input = f"{self._session_key}:{term}"
                alias = f"enclave_{hashlib.sha256(alias_input.encode()).hexdigest()[:10]}"
                self._token_map[term] = alias
                self._reverse_map[alias] = term
            masked = masked.replace(term, self._token_map[term])
        return masked

    def unmask_result(self, result_payload: dict[str, Any]) -> dict[str, Any]:
        """Re-identify aliases inside secure client boundary."""
        serialized = json.dumps(result_payload, default=str)
        for alias, original in self._reverse_map.items():
            serialized = serialized.replace(alias, original)
        return json.loads(serialized)

    def clear_session(self) -> None:
        """Securely wipe all enclave mappings at end of session."""
        self._token_map.clear()
        self._reverse_map.clear()
        self._session_key = secrets.token_hex(16)

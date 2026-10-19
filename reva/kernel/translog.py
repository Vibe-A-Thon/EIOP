"""Merkle transparency log with RFC 6962 / RFC 9162 proofs (T-110 / REVA-TL-001 / REVA-TL-003 / §6.9)."""

from __future__ import annotations

import hashlib
from typing import List, Optional, Tuple

from reva.core.digest import sha256_hex
from reva.core.errors import RevaIntegrityError
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.store import RevaStore

# Domain separation prefixes per RFC 6962 §2.1
LEAF_PREFIX = b"\x00"
NODE_PREFIX = b"\x01"


def leaf_hash(data: bytes) -> bytes:
    """Compute leaf hash: SHA-256(0x00 || data)."""
    return hashlib.sha256(LEAF_PREFIX + data).digest()


def node_hash(left: bytes, right: bytes) -> bytes:
    """Compute interior node hash: SHA-256(0x01 || left || right)."""
    return hashlib.sha256(NODE_PREFIX + left + right).digest()


def empty_tree_root() -> bytes:
    """RFC 6962 empty tree root: SHA-256("")."""
    return hashlib.sha256(b"").digest()


def largest_power_of_two_less_than(n: int) -> int:
    """Return largest power of 2 strictly less than n (for n >= 2)."""
    if n < 2:
        raise ValueError(f"n must be >= 2, got {n}")
    return 1 << ((n - 1).bit_length() - 1)


def mth(leaf_hashes: List[bytes]) -> bytes:
    """Compute Merkle Tree Hash (MTH) over an ordered list of leaf hashes per RFC 6962 §2.1."""
    n = len(leaf_hashes)
    if n == 0:
        return empty_tree_root()
    if n == 1:
        return leaf_hashes[0]

    k = largest_power_of_two_less_than(n)
    left = mth(leaf_hashes[:k])
    right = mth(leaf_hashes[k:])
    return node_hash(left, right)


def compute_path(m: int, leaf_hashes: List[bytes]) -> List[bytes]:
    """RFC 6962 PATH(m, D[n]) inclusion proof for leaf m in leaf_hashes."""
    n = len(leaf_hashes)
    if n <= 1:
        return []

    k = largest_power_of_two_less_than(n)
    if m < k:
        return compute_path(m, leaf_hashes[:k]) + [mth(leaf_hashes[k:])]
    else:
        return compute_path(m - k, leaf_hashes[k:]) + [mth(leaf_hashes[:k])]


def compute_subproof(m: int, leaf_hashes: List[bytes], b: bool) -> List[bytes]:
    """RFC 6962 SUBPROOF(m, D[n], b) consistency proof."""
    n = len(leaf_hashes)
    if m == n:
        return [] if b else [mth(leaf_hashes)]

    k = largest_power_of_two_less_than(n)
    if m <= k:
        return compute_subproof(m, leaf_hashes[:k], b) + [mth(leaf_hashes[k:])]
    else:
        return compute_subproof(m - k, leaf_hashes[k:], False) + [mth(leaf_hashes[:k])]


def compute_consistency_proof(m: int, n: int, leaf_hashes: List[bytes]) -> List[bytes]:
    """RFC 6962 PROOF(m, D[n]) consistency proof between size m and n (m <= n)."""
    if m < 0 or m > n or n > len(leaf_hashes):
        raise ValueError(f"Invalid range m={m}, n={n} for {len(leaf_hashes)} leaves")
    if m == 0 or m == n:
        return []
    return compute_subproof(m, leaf_hashes[:n], True)


def verify_inclusion(leaf_hash_bytes: bytes, index: int, tree_size: int, proof: List[bytes], expected_root: bytes) -> bool:
    """Verify an inclusion proof per RFC 6962 / RFC 9162 semantics."""
    if tree_size == 0 or index < 0 or index >= tree_size:
        return False
    if tree_size == 1:
        return index == 0 and len(proof) == 0 and leaf_hash_bytes == expected_root

    # Determine tree splits from top down
    splits: List[Tuple[bool, int]] = []  # (is_left_child, subtree_size)
    curr_idx = index
    curr_size = tree_size

    while curr_size > 1:
        k = largest_power_of_two_less_than(curr_size)
        if curr_idx < k:
            splits.append((True, curr_size))
            curr_size = k
        else:
            splits.append((False, curr_size))
            curr_idx -= k
            curr_size = curr_size - k

    if len(proof) != len(splits):
        return False

    # Bottom-up evaluation using proof elements
    curr_hash = leaf_hash_bytes
    # splits were collected top-down, while proof is ordered bottom-up
    for i, (is_left, _) in enumerate(reversed(splits)):
        sibling = proof[i]
        if is_left:
            curr_hash = node_hash(curr_hash, sibling)
        else:
            curr_hash = node_hash(sibling, curr_hash)

    return curr_hash == expected_root


def verify_consistency(size_m: int, size_n: int, root_m: bytes, root_n: bytes, proof: List[bytes]) -> bool:
    """Verify consistency proof between tree size m and n (RFC 9162 §2.1.4.2)."""
    if size_m < 0 or size_m > size_n:
        return False
    if size_m == size_n:
        return len(proof) == 0 and root_m == root_n
    if size_m == 0:
        return len(proof) == 0

    path = list(proof)
    if not path:
        return False

    # If first is an exact power of 2, prepend first_hash to the consistency_path
    if (size_m & (size_m - 1)) == 0:
        path = [root_m] + path

    fn = size_m - 1
    sn = size_n - 1

    # If LSB(fn) is set, right-shift both fn and sn equally until LSB(fn) is not set
    while fn & 1:
        fn >>= 1
        sn >>= 1

    fr = path[0]
    sr = path[0]

    for c in path[1:]:
        if sn == 0:
            return False
        if (fn & 1) or (fn == sn):
            fr = node_hash(c, fr)
            sr = node_hash(c, sr)
            if not (fn & 1):
                while not (fn & 1) and fn != 0:
                    fn >>= 1
                    sn >>= 1
        else:
            sr = node_hash(sr, c)

        fn >>= 1
        sn >>= 1

    return fr == root_m and sr == root_n and sn == 0




class TransparencyLog:
    """Tenant-scoped Merkle transparency log backed by RevaStore."""

    def __init__(self, store: RevaStore, log_id: str) -> None:
        self.store = store
        self.log_id = log_id

    def append(self, leaf_data: str) -> int:
        """Append leaf data into log and return zero-based leaf index."""
        cur = self.store.conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM reva_log_leaves WHERE log_id = ?", (self.log_id,))
        index = cur.fetchone()["cnt"]

        l_hash = leaf_hash(leaf_data.encode("utf-8"))
        now = format_ts(utc_now_ms())
        cur.execute(
            """
            INSERT INTO reva_log_leaves (log_id, leaf_index, leaf_data, leaf_hash, appended_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.log_id, index, leaf_data, l_hash, now),
        )
        self.store.conn.commit()
        return index

    def get_leaves(self, limit: Optional[int] = None) -> List[bytes]:
        """Fetch all or up to limit leaf hashes in index order."""
        cur = self.store.conn.cursor()
        if limit is not None:
            cur.execute(
                "SELECT leaf_hash FROM reva_log_leaves WHERE log_id = ? AND leaf_index < ? ORDER BY leaf_index ASC",
                (self.log_id, limit),
            )
        else:
            cur.execute(
                "SELECT leaf_hash FROM reva_log_leaves WHERE log_id = ? ORDER BY leaf_index ASC",
                (self.log_id,),
            )
        return [row["leaf_hash"] for row in cur.fetchall()]

    def size(self) -> int:
        cur = self.store.conn.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM reva_log_leaves WHERE log_id = ?", (self.log_id,))
        return cur.fetchone()["cnt"]

    def root(self, size: Optional[int] = None) -> bytes:
        """Compute MTH over leaves up to size."""
        leaves = self.get_leaves(limit=size)
        return mth(leaves)

    def inclusion_proof(self, leaf_index: int, tree_size: Optional[int] = None) -> List[str]:
        """Return inclusion proof as list of hex strings."""
        sz = self.size() if tree_size is None else tree_size
        if leaf_index < 0 or leaf_index >= sz:
            raise ValueError(f"Leaf index {leaf_index} out of range for tree size {sz}")
        leaves = self.get_leaves(limit=sz)
        proof_bytes = compute_path(leaf_index, leaves)
        return [b.hex() for b in proof_bytes]

    def consistency_proof(self, size_m: int, size_n: Optional[int] = None) -> List[str]:
        """Return consistency proof between size m and n as list of hex strings."""
        sz_n = self.size() if size_n is None else size_n
        leaves = self.get_leaves(limit=sz_n)
        proof_bytes = compute_consistency_proof(size_m, sz_n, leaves)
        return [b.hex() for b in proof_bytes]


# Ergonomic alias
MerkleLog = TransparencyLog


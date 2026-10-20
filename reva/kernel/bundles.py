"""Portable warrant bundle export, cryptographic packaging, and atomic import (T-117 / REVA-WK-012 / REVA-SEC-010)."""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from reva.core.digest import sha256_canonical, sha256_hex
from reva.core.errors import RevaIntegrityError, RevaValidationError
from reva.core.ids import bundle_id as compute_bundle_id, warrant_id as compute_warrant_id
from reva.core.jcs import canonical_digest, canonicalize
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.acl import Principal, is_authorized
from reva.kernel.blobs import BlobStore
from reva.kernel.signing import b64url_encode, verify_warrant_signature
from reva.kernel.sth import SignedTreeHead, verify_sth
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog, leaf_hash, verify_inclusion
from reva.kernel.warrant import SealedWarrant, WarrantBody, WarrantEnvelope


class BundleManifest(BaseModel):
    schema_name: str = Field(default="reva.bundle/1", alias="schema")
    tenant_origin: str
    created_at: str
    warrant_ids: List[str]
    blob_ids: List[str]
    key_ids: List[str]
    sth: Dict[str, Any]
    bundle_id: Optional[str] = None


class ImportReport(BaseModel):
    success: bool
    bundle_id: str
    warrants_imported: int
    blobs_imported: int
    issues: List[str] = Field(default_factory=list)


def export_bundle(
    store: RevaStore,
    blobs: BlobStore,
    log: TransparencyLog,
    tenant_id: str,
    principal: Principal,
    warrant_ids: List[str],
    destination_zip_path: str,
    sth_record: Optional[SignedTreeHead] = None,
) -> str:
    """Export selected warrants and their transitive artifacts into an authenticated zip bundle."""
    # 1. Collect warrants visible to principal
    warrants: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
    blob_ids: Set[str] = set()
    key_ids: Set[str] = set()

    for wid in sorted(list(set(warrant_ids))):
        row = store.get_warrant(tenant_id, wid)
        if not row:
            continue
        body_dict, env_dict = row
        if not is_authorized(env_dict, principal):
            continue

        warrants.append((body_dict, env_dict))

        # Collect blobs
        raw_ref = body_dict.get("raw_ref")
        if raw_ref and raw_ref.get("blob_id"):
            blob_ids.add(raw_ref["blob_id"])

        # Collect keys
        sig_obj = env_dict.get("signature")
        kid = sig_obj.get("key_id") if isinstance(sig_obj, dict) else env_dict.get("key_id")
        if kid:
            key_ids.add(kid)

    # 2. Get STH for log inclusion proofs
    cur = store.conn.cursor()
    if sth_record is None:
        row = cur.execute(
            "SELECT * FROM reva_sths WHERE log_id = ? ORDER BY tree_size DESC LIMIT 1",
            (log.log_id,),
        ).fetchone()
        if not row:
            raise RevaValidationError("Cannot export bundle without at least one signed tree head (STH)")
        sth_dict = {
            "sth_id": row["sth_id"],
            "log_id": row["log_id"],
            "tree_size": row["tree_size"],
            "root_hash": row["root_hash"].hex() if isinstance(row["root_hash"], bytes) else row["root_hash"],
            "issued_at": row["issued_at"],
            "key_id": row["key_id"],
            "signature": b64url_encode(row["signature"]) if isinstance(row["signature"], bytes) else row["signature"],
        }
    else:
        sth_dict = sth_record.model_dump()

    key_ids.add(sth_dict["key_id"])

    # 3. Inclusion proofs for each warrant
    proofs: Dict[str, List[str]] = {}
    sth_tree_size = sth_dict["tree_size"]
    for body_dict, env_dict in warrants:
        wid = env_dict["warrant_id"]
        log_meta = env_dict.get("log", {})
        leaf_idx = log_meta.get("leaf_index", 0)
        if leaf_idx < sth_tree_size:
            proofs[wid] = log.inclusion_proof(leaf_idx, sth_tree_size)

    # 4. Public keys dictionary
    keys: Dict[str, str] = {}
    for kid in key_ids:
        k_row = store.get_key(kid)
        if k_row:
            keys[kid] = k_row["public_key"].hex() if isinstance(k_row["public_key"], bytes) else k_row["public_key"]

    # 5. Manifest & Bundle ID
    now_ts = format_ts(utc_now_ms())
    manifest_data = {
        "blob_ids": sorted(list(blob_ids)),
        "created_at": now_ts,
        "key_ids": sorted(list(key_ids)),
        "schema": "reva.bundle/1",
        "sth": sth_dict,
        "tenant_origin": tenant_id,
        "warrant_ids": [env["warrant_id"] for _, env in warrants],
    }
    bid = compute_bundle_id(manifest_data)
    manifest_data["bundle_id"] = bid

    # 6. Write ZIP archive
    dest_path = Path(destination_zip_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(dest_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        # manifest.json
        zf.writestr("manifest.json", canonicalize(manifest_data))
        # keys.json
        zf.writestr("keys.json", canonicalize(keys))
        # proofs.json
        zf.writestr("proofs.json", canonicalize(proofs))

        # warrants.jsonl
        lines = []
        for body_dict, env_dict in warrants:
            item = {"body": body_dict, "envelope": env_dict, "warrant_id": env_dict["warrant_id"]}
            lines.append(canonicalize(item).decode("utf-8"))
        zf.writestr("warrants.jsonl", "\n".join(lines) + "\n")

        # blobs
        for b_id in sorted(list(blob_ids)):
            clean_hash = b_id.removeprefix("blb1_")
            if blobs.exists(tenant_id, b_id):
                blob_bytes = blobs.get_bytes(tenant_id, b_id)
                zf.writestr(f"blobs/{clean_hash}", blob_bytes)

    return bid


def import_bundle(
    store: RevaStore,
    blobs: BlobStore,
    log: TransparencyLog,
    target_tenant_id: str,
    zip_path: str,
) -> ImportReport:
    """Verify and atomically import an authenticated warrant bundle."""
    issues: List[str] = []
    path = Path(zip_path)
    if not path.is_file():
        return ImportReport(success=False, bundle_id="unknown", warrants_imported=0, blobs_imported=0, issues=[f"Bundle file not found: {zip_path}"])

    with zipfile.ZipFile(path, mode="r") as zf:
        namelist = set(zf.namelist())
        if "manifest.json" not in namelist:
            return ImportReport(success=False, bundle_id="unknown", warrants_imported=0, blobs_imported=0, issues=["Missing manifest.json"])

        # 1. Parse and verify manifest
        manifest_raw = zf.read("manifest.json")
        manifest_dict = json.loads(manifest_raw)
        claimed_bid = manifest_dict.get("bundle_id")

        manifest_no_bid = dict(manifest_dict)
        manifest_no_bid.pop("bundle_id", None)
        expected_bid = compute_bundle_id(manifest_no_bid)

        if claimed_bid != expected_bid:
            return ImportReport(success=False, bundle_id=claimed_bid or "unknown", warrants_imported=0, blobs_imported=0, issues=[f"Manifest bundle_id mismatch: expected {expected_bid}, got {claimed_bid}"])

        # 2. Parse keys
        keys_dict: Dict[str, str] = {}
        if "keys.json" in namelist:
            keys_dict = json.loads(zf.read("keys.json"))

        # 3. Verify STH
        sth_dict = manifest_dict.get("sth", {})
        sth_key_id = sth_dict.get("key_id")
        if not sth_key_id or sth_key_id not in keys_dict:
            issues.append(f"STH key {sth_key_id} missing from bundled keys")
        else:
            pub_bytes = bytes.fromhex(keys_dict[sth_key_id])
            sth_obj = SignedTreeHead(
                sth_id=sth_dict["sth_id"],
                log_id=sth_dict["log_id"],
                tree_size=sth_dict["tree_size"],
                root_hash=sth_dict["root_hash"],
                issued_at=sth_dict["issued_at"],
                key_id=sth_key_id,
                signature=sth_dict["signature"],
            )
            if not verify_sth(sth_obj, pub_bytes):
                issues.append(f"STH signature verification failed for bundle {claimed_bid}")

        # 4. Parse proofs
        proofs_dict: Dict[str, List[str]] = {}
        if "proofs.json" in namelist:
            proofs_dict = json.loads(zf.read("proofs.json"))

        # 5. Verify warrants & inclusion proofs
        parsed_warrants: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
        if "warrants.jsonl" in namelist:
            content = zf.read("warrants.jsonl").decode("utf-8")
            sth_root_bytes = bytes.fromhex(sth_dict.get("root_hash", "00" * 32))
            sth_size = sth_dict.get("tree_size", 0)

            for line in content.splitlines():
                if not line.strip():
                    continue
                w_item = json.loads(line)
                b_dict = w_item["body"]
                e_dict = w_item["envelope"]
                wid = w_item["warrant_id"]

                # Digest verify
                if compute_warrant_id(b_dict) != wid:
                    issues.append(f"Warrant {wid} body digest mismatch")

                # Signature verify
                sig_obj = e_dict.get("signature")
                kid = sig_obj.get("key_id") if isinstance(sig_obj, dict) else e_dict.get("key_id")
                sig = sig_obj.get("sig") if isinstance(sig_obj, dict) else e_dict.get("sig")
                if not kid or kid not in keys_dict:
                    issues.append(f"Warrant {wid} signed by unbundled key {kid}")
                else:
                    k_bytes = bytes.fromhex(keys_dict[kid])
                    if not verify_warrant_signature(wid, sig or "", k_bytes):
                        issues.append(f"Warrant {wid} signature invalid")

                # Inclusion proof verify
                if wid in proofs_dict:
                    p_hex_list = proofs_dict[wid]
                    p_bytes = [bytes.fromhex(p) for p in p_hex_list]
                    leaf_idx = e_dict.get("log", {}).get("leaf_index", 0)
                    lh = leaf_hash(wid.encode("utf-8"))
                    if not verify_inclusion(lh, leaf_idx, sth_size, p_bytes, sth_root_bytes):
                        issues.append(f"Warrant {wid} inclusion proof verification failed")

                parsed_warrants.append((b_dict, e_dict))

        # 6. Verify blobs
        blob_contents: Dict[str, bytes] = {}
        for fname in namelist:
            if fname.startswith("blobs/"):
                sha = fname.removeprefix("blobs/")
                data = zf.read(fname)
                if sha256_hex(data) != sha.lower():
                    issues.append(f"Corrupted bundled blob: {fname}")
                blob_contents[f"blb1_{sha}"] = data

        # If any validation failed, abort atomically
        if issues:
            return ImportReport(
                success=False,
                bundle_id=claimed_bid,
                warrants_imported=0,
                blobs_imported=0,
                issues=issues,
            )

        # 7. Write blobs to CAS store
        blobs_imported = 0
        for bid, b_data in blob_contents.items():
            blobs.put(target_tenant_id, b_data)
            blobs_imported += 1

        # 8. Save keys
        now = format_ts(utc_now_ms())
        for kid, hex_pub in keys_dict.items():
            pub_b = bytes.fromhex(hex_pub)
            store.save_key(
                key_id=kid,
                tenant_id=target_tenant_id,
                owner_kind="bundle_import",
                owner_id=claimed_bid,
                public_key=pub_b,
                private_key_enc=b"",
                status="verify_only",
                activated_at=now,
            )

        # 9. Insert warrants and append to target log
        warrants_imported = 0
        for b_dict, e_dict in parsed_warrants:
            wid = e_dict["warrant_id"]
            new_leaf = log.append(wid)
            # Update envelope with imported display marker
            e_dict["display"] = e_dict.get("display") or {}
            e_dict["display"]["imported_from"] = claimed_bid
            e_dict["log"]["imported_leaf_index"] = new_leaf

            subject_key = "unknown"
            subj = b_dict.get("subject", {})
            if "sha256" in subj:
                subject_key = f"artifact:{subj['sha256']}"
            elif "record_key" in subj:
                subject_key = f"source_record:{subj.get('system_instance_id')}:{subj['record_key']}"

            store.save_warrant(
                tenant_id=target_tenant_id,
                warrant_id=wid,
                body=b_dict,
                envelope=e_dict,
                subject_key=subject_key,
                predicate=b_dict.get("predicate", ""),
                producer_id=b_dict.get("producer", {}).get("producer_id", ""),
                authority=b_dict.get("authority", "shipped_artifact"),
                epistemic=b_dict.get("epistemic_state", "observed"),
                confidence_bp=b_dict.get("confidence", {}).get("score_bp", 10000),
                observed_at=b_dict.get("observed_at", now),
                valid_from=b_dict.get("valid_time", {}).get("from", now),
                valid_to=b_dict.get("valid_time", {}).get("to"),
                recorded_at=now,
                status=e_dict.get("status", "active"),
                log_index=new_leaf,
                acl_tokens=e_dict.get("acl", {}).get("source_acl_refs", []),
                classification=e_dict.get("classification", {}).get("level", "internal"),
                links=b_dict.get("links", []),
            )
            warrants_imported += 1

        return ImportReport(
            success=True,
            bundle_id=claimed_bid,
            warrants_imported=warrants_imported,
            blobs_imported=blobs_imported,
            issues=[],
        )

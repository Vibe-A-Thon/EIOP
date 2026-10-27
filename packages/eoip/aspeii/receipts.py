"""Ed25519 signing and verification for ASPEII action certificates."""

from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass
from datetime import datetime, timezone
from collections.abc import Mapping

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from eoip.contracts.aspeii import (
    ASPEIIActionCertificate,
    ASPEIIActionCertificatePayload,
    ASPEIIActionIntent,
    canonical_action_digest,
)

CERTIFICATE_DOMAIN_SEPARATOR = b"EOIP-ASPEII-CERTIFICATE-v1\n"


@dataclass(frozen=True)
class CertificateVerification:
    """Signature/integrity outcome; this does not establish truth or authority."""

    valid: bool
    reason_code: str
    key_id: str
    action_digest: str


class ASPEIIReceiptSigner:
    """Signs verified certificate payloads using an injected protected key."""

    def __init__(self, *, key_id: str, private_key_bytes: bytes) -> None:
        if not key_id:
            raise ValueError("A configured signing key id is required")
        if len(private_key_bytes) != 32:
            raise ValueError("Ed25519 private key material must be exactly 32 bytes")
        self._key_id = key_id
        self._private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)

    @classmethod
    def from_private_key(cls, *, key_id: str, private_key: Ed25519PrivateKey) -> ASPEIIReceiptSigner:
        raw = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return cls(key_id=key_id, private_key_bytes=raw)

    @property
    def public_key_bytes(self) -> bytes:
        return self._private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

    def sign(
        self,
        payload: ASPEIIActionCertificatePayload,
        *,
        action: ASPEIIActionIntent,
    ) -> ASPEIIActionCertificate:
        if payload.key_id != self._key_id:
            raise ValueError("Certificate key id does not match the configured signer")
        expected_action_digest = canonical_action_digest(action)
        if payload.action_digest != expected_action_digest:
            raise ValueError("Certificate is not bound to the supplied action")
        if (
            payload.action_ref.kind != "action"
            or payload.action_ref.id != action.action_id
            or payload.action_ref.revision != action.revision
        ):
            raise ValueError("Certificate action reference does not match the supplied action identity")
        if payload.action_ref.digest != expected_action_digest:
            raise ValueError("Certificate action reference does not match its canonical digest")
        if payload.expires_at <= datetime.now(timezone.utc):
            raise ValueError("Expired certificate payload cannot be signed")
        message = _certificate_message(payload)
        signature = base64.b64encode(self._private_key.sign(message)).decode("ascii")
        return ASPEIIActionCertificate.model_validate(
            payload.model_dump(mode="python") | {"signature": signature}
        )


def _certificate_message(payload: ASPEIIActionCertificatePayload) -> bytes:
    try:
        canonical = rfc8785.dumps(payload.model_dump(mode="json"))
    except (rfc8785.CanonicalizationError, ValueError, TypeError) as exc:
        raise ValueError("Certificate payload cannot be serialized as RFC 8785 JSON") from exc
    return CERTIFICATE_DOMAIN_SEPARATOR + canonical


def verify_action_certificate(
    certificate: ASPEIIActionCertificate,
    *,
    action: ASPEIIActionIntent,
    trusted_public_keys: Mapping[str, bytes],
    now: datetime | None = None,
) -> CertificateVerification:
    """Verify signature, action binding, and time bounds under supplied trust keys."""

    action_digest = canonical_action_digest(action)
    if certificate.action_digest != action_digest or certificate.action_ref.digest != action_digest:
        return CertificateVerification(False, "ACTION_DIGEST_MISMATCH", certificate.key_id, action_digest)
    if (
        certificate.action_ref.kind != "action"
        or certificate.action_ref.id != action.action_id
        or certificate.action_ref.revision != action.revision
    ):
        return CertificateVerification(False, "ACTION_REFERENCE_MISMATCH", certificate.key_id, action_digest)
    checked_at = now or datetime.now(timezone.utc)
    if checked_at.tzinfo is None or checked_at.utcoffset() is None:
        raise ValueError("Verification time must include a timezone")
    checked_at = checked_at.astimezone(timezone.utc)
    if checked_at < certificate.issued_at or checked_at >= certificate.expires_at:
        return CertificateVerification(False, "CERTIFICATE_EXPIRED_OR_NOT_YET_VALID", certificate.key_id, action_digest)
    raw_public_key = trusted_public_keys.get(certificate.key_id)
    if raw_public_key is None:
        return CertificateVerification(False, "UNTRUSTED_KEY_ID", certificate.key_id, action_digest)
    if len(raw_public_key) != 32:
        return CertificateVerification(False, "INVALID_TRUSTED_KEY", certificate.key_id, action_digest)
    try:
        signature = base64.b64decode(certificate.signature, validate=True)
        key = Ed25519PublicKey.from_public_bytes(raw_public_key)
        payload = ASPEIIActionCertificatePayload.model_validate(
            certificate.model_dump(mode="python", exclude={"signature"})
        )
        key.verify(signature, _certificate_message(payload))
    except (InvalidSignature, ValueError, binascii.Error, rfc8785.CanonicalizationError):
        return CertificateVerification(False, "SIGNATURE_INVALID", certificate.key_id, action_digest)
    return CertificateVerification(True, "SIGNATURE_VALID", certificate.key_id, action_digest)
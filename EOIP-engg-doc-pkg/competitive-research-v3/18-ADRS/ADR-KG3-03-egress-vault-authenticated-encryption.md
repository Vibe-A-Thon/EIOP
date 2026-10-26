# ADR-KG3-03: Egress Vault — Authenticated Encryption, Not XOR

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-03 |
| Gap | GAP-08 (`07-GAP-REGISTER.md`, forced P0, High severity) |
| Capability | CAP-51 (LLM egress control) |

## Context

`egress/gateway.py` is, on the whole, a strong and real control: default sharing level S0 (none), a platform kill switch, per-endpoint contract-term amendment that disables an endpoint until re-approved, a sealed immutable manifest per call, response DLP scanning and re-identification, and an `EgressOutage` fallback (BL-45, "Implemented (strengthened)" at HEAD). But the reversible tokenisation vault behind it, `egress/vault.py:24-33,68,84`, encrypts with an XOR keystream derived from a SHA-256 counter, keyed by PBKDF2 — and has no authentication tag. This is not a hardening gap, it is a cryptographic defect: XOR-with-keystream ciphers are malleable (an attacker who can flip bits in the ciphertext predictably flips bits in the plaintext) and catastrophically broken if the keystream ever repeats or is partially known. The module's own docstring already says "ADR-gated: replace with AES-GCM via KMS" — this ADR is that gate. Notably, the same codebase already uses a correct primitive elsewhere: `tenancy/layers.py` uses AES-256-GCM (HKDF-derived, AAD-bound) for per-tenant data keys, and `cryptography 50.0.2` is already an installed, lock-pinned dependency. Two crypto standards coexist in one repository today for no technical reason.

## Options considered

1. **Quick integration** — swap `egress/vault.py` to AES-GCM using the already-installed `cryptography` package, matching the pattern `tenancy/layers.py` already uses.
2. **Pragmatic native enhancement** — add key rotation and envelope encryption on top of the AES-GCM swap, so a compromised data-encryption key can be rotated without re-encrypting the whole vault.
3. **Long-term** — an optional OpenBao (MPL-2.0) Transit integration for customers who want a managed KMS, with the native AEAD path remaining the default for air-gapped deployments that cannot or will not run a separate KMS service. (HashiCorp Vault itself is BUSL-licensed and is excluded from bundling under the licence allow-list, GAP-19/ADR-KG3-11 — OpenBao is the community fork used instead, per `02-TECHNOLOGY-REGISTRY.md` §3.)

## Options rejected and why

Keeping the XOR cipher under any configuration is rejected outright — there is no deployment scenario (air-gapped or cloud-connected, single-tenant or multi-tenant) where an unauthenticated, malleable stream cipher is an acceptable default for a vault that exists specifically to protect tokenised values before they leave the egress boundary. This is the one self-inversion card where "when the alternative would be worse" does not apply: AEAD is strictly better with negligible added latency, full stop.

## Decision

Adopt option 1 immediately — replace the XOR/PBKDF2 scheme with AES-GCM (or ChaCha20-Poly1305) from the `cryptography` package already in the lock, matching the proven pattern in `tenancy/layers.py` rather than inventing a new one. Adopt option 3 as an optional, not default, integration for customers who already run OpenBao or an equivalent KMS; this is additive and does not change the default air-gapped path. Option 2 (key rotation) is folded into the option 1 implementation as a requirement, not deferred, because shipping AEAD without a key-rotation story just relocates the "quick integration" label onto a second, later ADR.

## Consequences

**Positive:** closes a Critical-adjacent, High-severity forced P0 (score 4.25, the second-highest-scoring forced item in the register) with a fix that reuses an in-house pattern rather than adding a new dependency or external service. Removes a genuine liability: an unauthenticated cipher in a security-labelled vault is the kind of defect that, if found externally rather than by this research, would be a credible, embarrassing vulnerability report.

**Negative:** every value currently tokenised under the old cipher must be migrated (re-encrypted) under the new one, which requires a one-time migration pass with no window where both old and new ciphertext formats are ambiguous on read — the migration plan, not the cipher swap itself, is the implementation risk. Key-management (where keys are stored, how they are rotated, who can access them) must be decided before rollout per the self-inversion card's own dependency note; shipping AEAD without that story solves the algorithm problem while leaving the custody problem open.

## Reversibility

High at the code level (the vault's call sites are internal to `egress/vault.py`) but low in practice once customer data has been tokenised under the new scheme in a live deployment — reverting to XOR after migration would mean either a second migration back or maintaining dual-format support indefinitely, neither of which should ever be exercised. This is a one-way door by design: there is no scenario under which reverting to XOR is the correct choice.

# C19 — HashiCorp Vault and OpenBao

| Field | Value |
|---|---|
| Registry ID | T-C19-vault-openbao |
| Tier | B (secrets; licence to verify) |
| Versions examined | Vault v2.2.1 (22 Oct 2026); OpenBao v2.7.1 (1 Oct, year not shown) |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
| Member | Owner / governance | Licence | Status |
|---|---|---|---|
| Vault | HashiCorp, now IBM (acquisition closed early 2025); LICENSE licensor reportedly changed to International Business Machines Corporation 2026-03-26 [CLAIM-vo-02] | **BUSL 1.1** since Aug 2023 (before: MPL-2.0); converts to MPL-2.0 four years after each version's publication | active; Vault 2.0 GA April 2026 (secondary sources: 04-13 vs 04-14) |
| OpenBao | Linux Foundation / OpenSSF (sandbox, joined June 2025 per secondary source); open governance, TSC | **MPL-2.0** [CLAIM-vo-03] | active; 8.7k stars; forked from Vault 1.14.0 (last MPL release) |
Legal-review triggers: BSL 1.1 additional-use grant (no hosted/embedded competitive offering) and white-label/OEM distribution; MPL-2.0 file-level copyleft (OpenBao). Record only, not conclusions.

## 2. Problem and workflows
Central secrets (static KV, dynamic DB/cloud credentials with leases), PKI, transit encryption-as-a-service, auth methods (OIDC, K8s), audit devices. EOIP workflow: replace env-injected tokens (`EOIP_API_TOKEN`, `runtime.api_token()`), connector credentials, and the tokenisation-vault key with leased secrets and Transit keys.

## 3. Feature inventory
| Capability | Vault | OpenBao |
|---|---|---|
| KV, dynamic secrets with leases/revocation | present | present [CLAIM-vo-03] |
| Transit (encrypt/decrypt without storing) | present | present ("data encryption and decryption without storing") |
| PKI, auth methods, audit devices | present | present (detail not re-verified) |
| Namespaces | Enterprise (historically) | OSS; GA from 2.3.1 per secondary source (UNVERIFIED) |
| Storage | integrated Raft, others | local disk, PostgreSQL, more [CLAIM-vo-03] |
| Performance/DR replication, Sentinel, FIPS 140-3 builds, managed HCP | Enterprise | absent (per comparison blog, 0.5) |

## 4. Architecture
```
Client --TLS+token--> [Vault/OpenBao active node] --seal/unseal (Shamir or auto-unseal KMS)--> barrier-encrypted storage (Raft/PG)
                         |-- audit device (file/socket)   |-- standby nodes (forward/serve reads)
Apps --lease renew--> secrets engines (KV, DB, PKI, Transit)
```

## 5. Under-the-hood reconstruction
- Barrier model: all persistent data is encrypted by a data key held in memory; the key is protected by a master key split via Shamir or wrapped by an auto-unseal KMS; sealed server answers only unseal/health. (Public architecture knowledge; docs not re-fetched, 0.7.)
- Request pipeline: token -> policy check (path-based ACL policies, deny by default) -> secrets engine -> lease manager -> audit log before response. Dynamic secrets are created per request with TTL and revoked by the expiry manager.
- Transit: keys never leave; versioned keys with rewrap. This is the primitive EOIP's `egress/vault.py` lacks: that vault derives keys via PBKDF2 and encrypts entries with an XOR keystream from SHA-256 (self-documented, "replace with AES-GCM via KMS when a KMS adapter lands"; reference KMS adapters are an "External gate").
- Consistency/HA: leader plus standbys (Raft in Vault; storage-dependent); OpenBao standby nodes serve reads from 2.5 per secondary source (UNVERIFIED).
- Licence mechanism: BSL "Change Date" four years; additional use grant permits production use except offering a competing hosted/embedded product to third parties; internal use not competitive [CLAIM-vo-01].

## 6. Requirements inferred
FR: lease TTLs, audit device, Transit AEAD, policy per path, unseal without cloud. NFR: sealed-at-rest, no plaintext in logs, rotation without downtime, single-node boot with Raft or file storage.

## 7. Performance and resource model
No throughput/latency figures were fetched for either: **UNVERIFIED**. Qualitative: Go single binary; storage backend dominates latency; auto-unseal depends on KMS (air-gap needs transit-seal or Shamir). Failure modes: sealed cluster after restart, lease storm on mass revocation, audit-device failure blocks requests (documented Vault behaviour, 0.6).

## 8. Strengths
Mature secret lifecycle; dynamic credentials remove long-lived secrets; Transit AEAD for field-level encryption; OpenBao gives a permissive-copyleft (MPL) route with community governance. Match: EOIP already fails closed on missing/short/revoked token (`runtime.py` `api_token`), but has no rotation/lease.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | Vault BUSL 1.1 and IBM licensor; OpenBao MPL-2.0 file-level copyleft |
| Operational | unseal ceremony, storage HA, audit-device availability; heavy for tiny deployments |
| Governance | OpenBao maintainer overlap with IBM engineers reported (secondary) |
| Friction | policy language (HCL), agent/sidecar injection |
| Gaps | OpenBao lacks Enterprise replication/FIPS builds (per comparison blog) |

## 10. Deployment, licensing, viability
Both self-host, container/binary, air-gap viable with Shamir unseal. For a redistributed, white-labelled EOIP: **do not embed Vault (BUSL)**; treat OpenBao as an optional integration deployed by the customer (not bundled) until legal review of MPL-2.0 file-level obligations. Interface by HTTP API (Vault-compatible), keeping both swappable.

## 11. Delta vs EOIP baseline
BL-45 egress vault: self-built reversible tokenisation with stdlib keystream (non-standard cipher) and local secret; BL-22 offline licensing; `runtime.api_token()` env injection. No secret leasing, rotation, Transit, or KMS adapter (SR-CON-012 reference adapters flagged External gate in the code docstring). Not a BL-18/BL-20 item, but tenant key isolation depends on it.

## 12. Cards
**STR-vo-01** | OpenBao/Vault | Transit encryption-as-a-service | CLAIM-vo-03 | replaces custom keystream cipher; per-tenant keys | integrate | `SecretsPort` with Transit adapter; fallback AES-GCM via `cryptography` | tokenised value round-trips; key rotation re-wraps without plaintext exposure.
**STR-vo-02** | OpenBao | dynamic leased credentials | CLAIM-vo-03 | no static connector credentials | integrate | connector auth fetches leased DB/API creds | credential expires and connector fails closed.
**INV-vo-01** (BSL 1.1, licensing, proven) | Vault not embeddable for competing OEM use; options: (1) OpenBao only; (2) `SecretsPort` with env/file default plus both; (3) native KMS lite. Selected 2. Benchmark: n/a, legal gate. Decision ADOPT (abstraction). Defensibility: customer choice.
**INV-vo-02** (unseal/ops weight, deployment hypothesis) | single-node dev mode risks (in-memory, unsealed): ban in production profile. Decision EXPERIMENT: 1-node Raft footprint measurement.

## 13. Decisions
| Capability | Decision |
|---|---|
| Secrets backend | INTEGRATE OpenBao (optional, customer-deployed) via `SecretsPort` |
| Vault (BUSL) | REJECT bundling; REFERENCE |
| Replace XOR-keystream cipher | BUILD (AES-GCM) now, independent of vault |
| Dynamic creds / leases | EXPERIMENT |

## 14. Tests
Sealed-server boot in air-gap; token revoke -> API refuses start; Transit round-trip and rotation; licence scan of shipped artefacts (no BUSL components); secret never appears in logs/manifest (`egress/manifest.py`).

## 15. Risks
BSL interpretation; OpenBao bus factor/IBM overlap; sandbox maturity; Vault 2.x feature divergence (secondary source).

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | owners, licences |
| D2,D3 | 2,4 | secrets, barrier |
| D8 | 5,7 | HA, storage |
| D18 | 5,9,11 | seal, policies, audit |
| D19 | 11 | per-tenant keys |
| D20 | 7 | UNVERIFIED |
| D21 | 1,10 | BUSL vs MPL |
| D22 | 10 | API-compatible swap |
| D23 | N/A | none found |
| D24 | App C | mixed sources |
| D4-D7,D9-D17 | N/A | not a data system |

## Appendix B — Capabilities
| CAP | Vault / OpenBao | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-50 | native | 03 | BL-45 | INTEGRATE | P2 |
| CAP-48 | audit devices | 03 | BL-19 | REFERENCE | P3 |
| CAP-77 | licence cost | 01,02 | BL-22 | INTEGRATE OpenBao | P1 |
| CAP-52 | OEM terms | 01 | BL-21 | REJECT Vault bundling | P1 |

## Appendix C — Evidence
| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-vo-01 | BSL 1.1 text | additional use grant, competitive offering definition, internal use not competitive, 4-year change to MPL-2.0 | Officially documented | https://www.hashicorp.com/en/bsl | updated 2023-10-17 / 2026-10-26 | 0.9 | page did not mention Vault explicitly |
| CLAIM-vo-02 | Vault 2.x | Vault 2.0 GA Apr 2026 under IBM; BUSL still applies; licensor now IBM; v2.2.1 released 22 Oct 2026 | Third-party report + release page | https://infoq.com/news/2026/04/vault-2-0-ibm-identity/ ; https://github.com/hashicorp/vault/releases/latest | 2026-04 / 2026-10-26 | 0.6 | secondary sources differ by a day; one source claims 2.2.0 on 15 Oct |
| CLAIM-vo-03 | OpenBao v2.7.1 | MPL-2.0; OpenSSF/LF open governance; 8.7k stars; KV, dynamic secrets, encrypt/decrypt without storing; PG/disk storage | Officially documented | https://github.com/openbao/openbao | 1 Oct / 2026-10-26 | 0.85 | OpenSSF join date from secondary source |
| CLAIM-vo-04 | Fork history | OpenBao forked from Vault 1.14.0, last MPL release | Third-party report | https://techtarget.com/searchitoperations/news/366563095/IBM-engineers-hatch-Linux-Foundation-HashiCorp-Vault-fork | 2024 / 2026-10-26 | 0.7 | none |

## Appendix D — Assumptions
Barrier/seal description from public architecture knowledge, flagged 0.7. No legal conclusions drawn.

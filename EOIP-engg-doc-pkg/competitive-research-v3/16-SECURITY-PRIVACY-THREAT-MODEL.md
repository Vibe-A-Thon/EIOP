# 16 — Security & Privacy Threat Model (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 16-SECURITY-PRIVACY-THREAT-MODEL.md |
| Methodology | STRIDE + OWASP Top 10 for LLMs / MITRE ATLAS |
| Security Paradigm | Zero-Trust Derivation ACLs + Zero-Data-Leak Egress Fencing |
| Verification Cutoff | 2026-10-18 UTC |

---

## 1. STRIDE Threat Analysis

| Threat (STRIDE) | Attack Vector | Impact on KG / Agent | Mitigating Defense & Control |
|---|---|---|---|
| **Spoofing** | Attacker impersonates tenant or user identity in query API | Cross-tenant access, unauthorized graph read | Signed HMAC / OIDC JWT tokens verified on every hop; strict in-memory tokens only |
| **Tampering** | Malicious injection modifies graph edges or changes claims | Corrupted business logic, poisoned digital thread | Mutation Validation Gate; RFC 8785 Merkle Warrants (`wr1_...`); immutable WAL |
| **Repudiation** | Operator denies executing destructive action | Unaccountable configuration drift | Comprehensive audit log signed with Merkle roots; dual-key approval on mutations |
| **Information Disclosure** | Graph traversal or RAG surfaces facts derived from private sources | Secret leakage, insider trading data spill | Derivation-Aware ACL Composition: Inferred facts inherit premise ACLs; policy epochs |
| **Denial of Service** | Deep recursive traversal or supernode explosion exhausts RAM | Out-of-memory crash, service outage | Bounded QueryPlans; degree limits (max 1000 edges/hop); query timeout (10s) |
| **Elevation of Privilege** | Cypher/Gremlin injection escapes parameterized boundaries | Root shell / arbitrary database execution | Parameterized Query Gateway; raw query endpoints restricted to platform admin |

---

## 2. LLM & Agentic AI Specific Safeguards

### 2.1 Prompt Injection & Jailbreak Defense
- All user-supplied prompts are wrapped in cryptographic boundary fences:
  `<<<UNTRUSTED_CONTENT_START:canary_hash>>> ... <<<UNTRUSTED_CONTENT_END:canary_hash>>>`.
- Models are instructed systemically to treat enclosed text as inert semantic data.

### 2.2 Exfiltration & Tripwire Canaries
- `EgressSecurityGate` inserts synthetic cryptographic canary tokens (`egress_canary_...`).
- An egress honeypot monitor detects if canary tokens appear in unauthorized outbound network buffers, triggering an instantaneous automated kill-switch.

### 2.3 Data Poisoning Defense
- Ingested external assertions are quarantined in the **Prediction Plane** (`PROPOSED_UNTIL_VALIDATED`).
- No external uncorroborated claim can overwrite verified institutional knowledge without human steward approval.

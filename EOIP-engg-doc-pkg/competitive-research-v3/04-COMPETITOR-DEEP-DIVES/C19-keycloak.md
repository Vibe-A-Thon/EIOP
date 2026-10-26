# C19 — Keycloak / OIDC / SAML

| Field | Value |
|---|---|
| Registry ID | T-C19-keycloak |
| Tier | B (self-hosted IdP; EOIP has its own OIDC/SAML adapter, BL-19) |
| Versions examined | Keycloak 26.8.1 (release page dated 13 Oct, year not shown, 2026 inferred); docs 26.8.1 |
| Verified on | 2026-10-26 (brief says 2026-10-18; batch run date used) |
| Worker | V11 |

## 1. Identity, status, tier, sources
Keycloak: open-source identity and access management server (OIDC, OAuth 2.0, SAML 2.0, identity brokering, user federation). CNCF **Incubating** (accepted 2023-04-10) [CLAIM-keycloak-01]. Licence Apache-2.0 (project-level; not re-fetched from LICENSE file this run, confidence 0.8). Very active: 26.8.1 is a security-fix release (token exchange accepting bearer tokens without required mTLS cert, admin permission bypasses, SAML/OIDC broker issues) [CLAIM-keycloak-02]. OIDC/SAML are protocols, not products; this entry covers Keycloak as the reference self-hosted IdP. Sources: keycloak.org documentation, keycloak.org HA intro, CNCF project list, GitHub releases.

## 2. Problem, workloads, workflows
Central login/SSO for many apps, brokering enterprise IdPs (Entra, Okta, LDAP/AD), and token issuance. Flow: user -> EOIP web -> redirect to Keycloak realm (PKCE) -> ID/access token with `sub`, roles, groups -> EOIP/MCP resource server validates JWT and maps to principal. White-label: realm per tenant, themes.

## 3. Feature inventory
| Capability | Status |
|---|---|
| OIDC, SAML 2.0 IdP and broker | present [CLAIM-keycloak-01] |
| Authorization Services (UMA 2.0, policy enforcer) | present |
| Token exchange | present (security-sensitive, see -02) |
| Organizations (multi-org inside realm) | present |
| Fine-grained admin permissions | present |
| User federation LDAP/Kerberos, MFA, WebAuthn | present (docs index; details not re-verified) |
| Clustering via Infinispan; external RDBMS | present [CLAIM-keycloak-03] |
| Admin REST API, SPIs/themes/providers (Java) | present |
| Per-document / per-fact ACL filtering | absent (not an authorization-for-search system) |

## 4. Architecture
```
Browser/Service --OIDC/SAML--> [Keycloak node(s) : realms, clients, flows, SPIs]
                                   | Infinispan (sessions, caches, cross-node)
                                   v
                              RDBMS (users, clients, config)  <-- LDAP/AD/upstream IdP federation
EOIP API / MCP (resource server) --JWKS fetch--> validate JWT locally
```

## 5. Under-the-hood reconstruction
- Data model: realm -> clients, users, groups, roles (realm/client), protocol mappers that shape token claims. State in RDBMS (config, users, offline sessions) plus Infinispan caches (user/session/auth sessions). Hypothesis (from public architecture knowledge, not re-read at source): Quarkus runtime since v17.
- Token path: authorization-code + PKCE; signing keys published at JWKS; resource servers verify offline; refresh and revocation require Keycloak round trips (introspection).
- Authorization Services: resources, scopes, permissions evaluated by policy types (role, group, JS, time, aggregate); UMA permission tickets; a policy-enforcer library on the resource server.
- Multi-tenancy: realm-per-tenant (strong separation of users/keys, heavier) or Organizations in one realm (lighter). Scale limits for thousands of realms: NOT PUBLICLY VERIFIED here.
- Security hardening: strict redirect URI matching, mTLS-bound tokens (DPoP/mTLS), brute-force detection; the 26.8.1 advisory shows the IdP itself is a high-value target.

## 6. Requirements inferred
FR: OIDC discovery, PKCE, SAML metadata, group/role claims, tenant claim, logout/revocation. NFR: HA with sub-10 ms node RTT and synchronous multi-AZ DB [CLAIM-keycloak-03]; prompt patching cadence.

## 7. Performance and resource model
Vendor docs: regularly tested 1,000,000 users and 300 requests/s; scaled to 30,000,000 users, 1,000 logins/s and 20,000 token refreshes/s on six pods (40 vCPU, 8 GB each) with Aurora PostgreSQL `db.r8g.16xlarge`; CPU grows linearly with load [CLAIM-keycloak-03]. Single-node footprint for EOIP one-node-first: JVM + RDBMS; no vendor figure fetched (UNVERIFIED; plan 1-2 GB RAM, hypothesis). Failure modes: Infinispan split-brain, DB latency, key rotation misconfig.

## 8. Strengths
Mature standards coverage; broker to enterprise IdPs; admin console; large community; CNCF governance. Matching: EOIP already has OIDC/PKCE/SAML adapter code; the strength to adopt is the **operational IdP** (sessions, MFA, federation) rather than reimplementation.

## 9. Limitations
| Class | Item |
|---|---|
| Operational | JVM + DB + cache cluster; heavy for tiny one-node deploys |
| Security | frequent security releases (26.8.1) [CLAIM-keycloak-02] |
| Friction | custom SPIs in Java; realm-per-tenant at scale unclear |
| Scope | issues identity, not per-document ACLs; group claims bloat tokens |

## 10. Deployment, licensing, viability
Apache-2.0 permissive, redistributable; container image, Helm/operator; air-gap viable (no mandatory cloud; verify theme/font CDN use). Red Hat build (RHBK) is a commercial variant, not required. No legal trigger from licence.

## 11. Competitive delta vs EOIP
BL-19: EOIP has `authn/oauth_sso.py` (PKCE, OIDC discovery, SAML adapter, IdPFederation) marked "SSO live-unverified". No Keycloak interoperability test exists in what was inspected. MCP server authenticates one static bearer token (`apps/mcp/main.py:220-223`; see C09-mcp INV-mcp-02), so no per-user identity reaches retrieval (BL-18).

## 12. Cards
**STR-keycloak-01** | Keycloak | Operational IdP with brokering and MFA | CLAIM-01 | removes need for EOIP to own credential lifecycle | integrate | ship Keycloak as optional reference IdP in compose; validate JWT `sub`/groups into `TrustedScope` | live OIDC login + MCP call carries `sub`.
**STR-keycloak-02** | Keycloak | Standards-based token exchange/audience restriction | CLAIM-02 | MCP resource-server mode | integrate | RFC 8693 exchange for downstream REST with caution | test with mTLS-bound tokens.
**INV-keycloak-01** (heavy footprint, hypothesis/deployment) | JVM+DB+Infinispan vs one-node-first | Option 1: optional compose profile (selected); 2: lightweight built-in OIDC only (exists); 3: pluggable IdP SPI. Falsifiable POC: cold start RAM and p95 login latency on 4 GB node vs built-in adapter. Defensibility low (commodity); decision EXPERIMENT. Failure case: stale group claims after revocation -> require short token TTL plus `policy_epoch` bump (authz/pdp.py).
**INV-keycloak-02** (IdP as attack surface, proven by 26.8.1 advisory) | Option: pin versions, subscribe to advisories, contract-test token exchange off by default. Decision ADOPT as operational policy.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-44 SSO/OIDC/SAML IdP | INTEGRATE (Keycloak optional reference IdP; any OIDC IdP) |
| CAP-45 roles to scopes mapping | REUSE EOIP `authz/core.py` fed by token claims |
| Keycloak Authorization Services for doc ACLs | REJECT (wrong granularity) |
| Per-tenant realm provisioning | EXPERIMENT |

## 14. Tests / acceptance
1. Keycloak container in CI; OIDC code+PKCE login end-to-end against `oauth_sso.py`. 2. MCP resource-server test: user A token cannot read user B-only doc (J5). 3. Revoked user denied within TTL. 4. Air-gapped boot with no external fetch.

## 15. Risks / open questions
Realm-per-tenant limits; token-claim size for large group sets (ReBAC should instead hold groups); advisory cadence; DPoP support status UNVERIFIED.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | identity, CNCF incubating, Apache-2.0 |
| D2 | 2 | SSO/brokering |
| D3 | 4,5 | Quarkus/Infinispan/RDBMS (hypothesis) |
| D4-D7,D9-D12,D14 | N/A | not a data/query/reasoning system |
| D8 | 5,7 | HA, scale figures |
| D13 | 11 | token-to-retrieval identity gap |
| D15-D17 | 3 | admin console, SPIs |
| D18 | 5,9 | AuthN, token binding, advisories |
| D19 | 5 | realms/Organizations |
| D20 | 7 | vendor figures |
| D21 | 10 | permissive; Red Hat variant |
| D22 | 8 | standards portability |
| D23 | N/A | no prior-art concern found |
| D24 | App C | docs-based, no benchmark rerun |

## Appendix B — Capability mapping
| CAP | Keycloak | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-44 | native | 01 | BL-19 Implemented/Partial | INTEGRATE | P1 |
| CAP-45 | partial | 01 | BL-19 | REUSE own | P2 |
| CAP-47 | partial (realms) | 01 | BL-20 Partial | EXPERIMENT | P2 |
| CAP-46 | absent | - | BL-18 | REJECT here | P0 via ReBAC |
| CAP-50 | native self-host | 03 | - | INTEGRATE | P2 |

## Appendix C — Evidence
| CLAIM | product/version/date | claim | class | source | dates | confidence | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-keycloak-01 | 26.8.1 | OIDC+SAML 2.0, Authorization Services UMA2, token exchange, Organizations, fine-grained admin perms, Infinispan; CNCF incubating (accepted 2023-04-10) | Officially documented | Keycloak docs https://www.keycloak.org/documentation ; CNCF https://www.cncf.io/projects/ | n/a / 2026-10-26 | 0.9 | none |
| CLAIM-keycloak-02 | 26.8.1 | release is mostly security fixes incl. token-exchange/mTLS, admin bypass, SAML/OIDC broker | Officially documented | https://github.com/keycloak/keycloak/releases/latest | 13 Oct (year not shown) / 2026-10-26 | 0.8 | summary via page fetch |
| CLAIM-keycloak-03 | 26.8.1 docs | tested 1M users/300 rps; scaled 30M users, 1,000 logins/s, 20,000 refreshes/s; 6 pods 40 vCPU 8 GB; node RTT <10 ms | Officially documented (vendor) | https://www.keycloak.org/high-availability/single-cluster/introduction | n/a / 2026-10-26 | 0.85 | vendor workload |

## Appendix D — Assumptions
Licence taken as Apache-2.0 from project knowledge; access date is batch date 2026-10-26; release year inferred; no LICENSE file fetched.

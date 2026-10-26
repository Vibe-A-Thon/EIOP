# ADR-KG3-11: Licence Allow-List as a CI Gate

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-11 |
| Gap | GAP-19 (`07-GAP-REGISTER.md`, forced P0, High severity, score 4.5 — the highest score in the register) |
| Capability | CAP-52 (White-label / OEM packaging), CAP-77 (Licensing and TCO) |

## Context

EOIP is sold and white-labelled (Master Prompt §4.3 item 12), which means every reused or integrated component must be checked for redistribution, OEM, SaaS and embedding terms before adoption — not after. The research package itself, across its own registry and deep dives, documents numerous AGPL/SSPL/BSL/ELv2/commercial-only components that would block a white-label OEM product if adopted without review: Zingg (AGPL-3.0), FalkorDB (SSPL), HashiCorp Vault (BUSL), Grafana (AGPL-3.0), Elasticsearch (mixed AGPL/SSPL/ELv2 depending on version), Airbyte (mixed ELv2/MIT), Redpanda (BUSL), TruffleHog (AGPL-3.0), PM4Py (AGPL-3.0), igraph (GPL-2.0), Raphtory (GPL-3.0), Logseq (AGPL-3.0), and several OWL reasoners under LGPL/AGPL terms. No automated check exists today to catch a future dependency addition that would silently reintroduce one of these — licence review has been manual and ad hoc, scattered across per-feature decisions in the registry rather than enforced anywhere in CI. This is the root cause the self-inversion card names: operational/governance, not technical.

## Options considered

1. **Quick integration** — a licence-checker CI step scanning `requirements.lock` and `package-lock.json` (and equivalent manifests) against an explicit allow-list derived from `02-TECHNOLOGY-REGISTRY.md` §3, failing the build on any licence not on the list.
2. **Pragmatic native enhancement** — extend the allow-list check to container images and bundled binaries, not just language-package manifests, since several of the named risks (FalkorDB, Redpanda, Vault/OpenBao) are typically consumed as container images rather than as a language dependency.
3. **Long-term** — an automated SBOM (shares infrastructure with GAP-44/CAP-79) cross-checked against the allow-list on every release, so the licence gate and the supply-chain-integrity gate are one pipeline rather than two.

## Options rejected and why

Relying on manual review alone, even if formalized as a checklist rather than ad hoc, is rejected: the research package's own evidence is that this has already failed to prevent multiple attractive-but-blocked components from being seriously considered (the researcher-decision tallies in the capability matrix, e.g. CAP-52's `REJECT×7, REUSE×3, BUILD×1`, show these components were evaluated and rejected by researchers manually, which worked this time but is not a durable control against a future addition made under schedule pressure).

## Decision

Adopt option 1 immediately as a CI gate — this is the item the self-inversion card itself marks P0 (forced), distinct from the other ten self-inversion cards' plain ADOPT. Adopt options 2 and 3 as the target, explicitly sharing infrastructure with GAP-44 (SBOM/signing, a separate P1 gap) since both require the same component inventory. Legal review retains final say on any exception the automated gate flags — this ADR builds the gate, it does not replace legal judgement on edge cases.

## Consequences

**Positive:** closes the highest-scoring gap in the entire register (4.5, forced P0) with an S-effort (2–4 week) fix. Converts licence risk management from "a researcher noticed this time" to "the build fails automatically" — directly protecting the OEM/white-label business model (CAP-52) that is itself one of this platform's named differentiators (no researched competitor offers an OEM-ready self-host product, per CAP-52's evidence row).

**Negative:** not a market differentiator by itself — it is risk management, and the self-inversion card is explicit that this should not be oversold as a feature. An allow-list that is too strict can block a genuinely useful dependency pending legal review, creating friction; one that is too permissive defeats the purpose. Getting the initial allow-list right, derived correctly from `02-TECHNOLOGY-REGISTRY.md` §3, is itself a one-time research task this ADR depends on being accurate.

## Reversibility

High. A CI gate is easy to add, tune or temporarily disable (with an audit trail of the disable, not silently) without touching production code. The risk is not reversibility but drift — an allow-list that is not kept current with new licensing terms (e.g., a project changing from Apache-2.0 to BSL between versions, which several components in the researched set have done) requires ongoing maintenance, not a one-time setup.

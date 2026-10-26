# ADR-KG3-10: Local Model Runtime Hardening

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic — the prior version of this file claimed "smooth 60 FPS rendering on 100,000+ nodes" for Sigma.js with no benchmark; see `10-TARGET-REFERENCE-ARCHITECTURE.md` §8 for the correction) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-10 |
| Gap | GAP-36 (`07-GAP-REGISTER.md`, forced P0, High severity) |
| Capability | CAP-61 (Local model serving) |

## Context

`deploy/docker-compose.yml` pins `ollama/ollama:0.12.3`, runs it as root, and provides no authentication in front of it. As of this research (2026-10), that pin is roughly a year old, and research into Ollama (C09-ollama) documents a path-traversal CVE (CVE-2026-103663) affecting versions in this range. Running as root inside a container is a standard hardening violation independent of any specific CVE: a container compromise via any vulnerability in that range escalates further than it would with a non-root user. The lack of authentication means any service on the same network segment as the Ollama container can issue inference requests or, depending on the CVE, worse. This is a straightforward operational-hygiene gap, not a design flaw — the pin was simply never revisited after initial setup.

## Options considered

1. **Quick integration** — bump the pin past the patched version, add a non-root user in the container definition, and add a network policy restricting access to internal services only (not exposed beyond the compose network).
2. **Pragmatic native enhancement** — an authenticating reverse proxy in front of the model port, so even internal callers must present a credential, consistent with the "least privilege" posture Master Prompt §4.3 item 8 asks for everywhere else.
3. **Long-term** — a `ModelPort` abstraction (already partially present as `models/port.py`, NB-10) supporting both Ollama and llama.cpp (STR-llcpp-01: a dependency-free, CPU-only server with embeddings, rerank and JSON-schema output), selected per deployment, so a customer uncomfortable with Ollama's operational history has a credible alternative without an application-code change.

## Options rejected and why

Treating this as low-priority because it is "just an operational pin" is rejected — the gap register's own severity classification (High, forced P0) reflects that an unauthenticated, outdated, root-running service in the default deployment compose file is a live risk in every default install, not a theoretical one. No alternative design trade-off applies here in the way it does for, say, tenant isolation (ADR-KG3-02) where SILO deployments legitimately need less enforcement — every deployment benefits from this fix with no downside.

## Decision

Adopt option 1 immediately — this is a same-day fix with no architectural dependency. Adopt option 2 soon after, as defence-in-depth. Adopt option 3 as the target architecture, both because it gives customers a choice and because llama.cpp's dependency-free CPU profile fits the platform's CPU-first principle (§1 principle 4) more tightly than a general-purpose model server does.

## Consequences

**Positive:** closes a High-severity forced P0 (score 4.25, tied for second-highest in the register) with the lowest-effort fix of any item in this set — S-effort per the capability matrix. BM-14 (a CVE/vulnerability scan of the pinned image, re-checked on every release) makes "zero known-exploitable CVEs at release time" a standing, automatable gate rather than a one-time check.

**Negative:** none specific to this fix beyond the standard cost of re-validating model behaviour against a new Ollama version (a version bump can change default parameters or API surface in ways that need re-testing against the existing retrieval/synthesis pipeline, `ai/graphrag.py`).

## Reversibility

High. This is an isolated, independently revertible operational change (an image tag, a container user directive, a network policy) with no coupling to any other ADR in this set. It is explicitly called out in the self-inversion card as "not a differentiator — a hygiene fix every self-hosted competitor needs," which is also why it has no meaningful reversibility risk: there is no scenario where reverting to the old pin is correct.

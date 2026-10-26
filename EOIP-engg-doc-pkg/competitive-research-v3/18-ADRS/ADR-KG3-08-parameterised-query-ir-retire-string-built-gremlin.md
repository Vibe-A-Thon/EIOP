# ADR-KG3-08: Parameterised Query IR; Retire String-Built Gremlin

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-08 |
| Gap | GAP-05 (`07-GAP-REGISTER.md`, forced P0, High severity), ties to GAP-04 (ADR-KG3-12) |
| Capability | CAP-13 (Gremlin), CAP-49 (Query and prompt-injection defence) |

## Context

Two backend adapters build Gremlin/Groovy scripts by splicing property keys and labels into strings: `adapters/janusgraph.py:192,276` and `graph/hugegraph.py:525-551`. This is a proven injection surface by code reading — if a key or label value ever originates from untrusted input without independent sanitisation, the adapter executes attacker-controlled script fragments. Separately, the agent firewall (`agents/firewall.py`) that is supposed to catch malicious input relies on regex patterns only (C09-guardrails INV-grd-01), which is a known-weak defence class against adversarial text, not a backstop that makes the string-building safe. These are two distinct problems that happen to share one fix: removing hand-built query strings removes the injection surface regardless of what the firewall does or does not catch.

## Options considered

1. **Quick integration** — parameterise the two named call sites directly, so property keys and labels are bound as typed parameters rather than spliced into the script text.
2. **Pragmatic native enhancement** — route every backend call through the QueryPlan→AST compiler (`query/ast_compiler.py`, BL-09) so that no hand-built script ever reaches a backend adapter in the first place; this is the same compiler ADR-KG3-12 makes the production path for a different reason (backend portability), applied here for its security benefit.
3. **Long-term** — adopt gremlin-lang with typed parameters as the only wire format to Gremlin-speaking backends once TinkerPop 4.0 is stable (currently beta per C12-tinkerpop, `STR-tinkerpop-01`); not yet actionable.

## Options rejected and why

Treating the regex firewall as the primary mitigation is rejected: a classifier or regex layer is a reasonable supplement for untrusted free text reaching an LLM-driven query-suggestion path, but it is not a substitute for parameterisation at the two adapters, which is a construction-level fix, not a detection-level one. Detection can be evaded; construction cannot be bypassed by input it was never asked to interpret as code.

## Decision

Adopt option 1 immediately — parameterise the two named call sites as an independent, scoped patch that does not wait on the compiler work. Adopt option 2 as the structural fix, sharing its delivery with ADR-KG3-12 (GAP-04) since both call for the same QueryPlan→AST path to be the only route to a backend. Track option 3 for later: TinkerPop 4.0's gremlin-lang direction is the right long-term wire format, but its beta status means committing to it now would be premature.

## Consequences

**Positive:** closes a High-severity forced P0 (score 3.4). Removes a real vulnerability by construction once option 2 lands, rather than leaving two patched-but-still-string-built call sites as the only defence. Shares its benchmark and its delivery vehicle with GAP-01's adapter-defect fixes (ADR-KG3-05) and GAP-04's structural compiler (ADR-KG3-12), so this is not three separate initiatives competing for the same engineering time — it is one initiative with three justifications.

**Negative:** this closes a real vulnerability but is explicitly not a market differentiator on its own (per the self-inversion card's own defensibility note) — it is a correctness bar, and framing it as more than that would overstate its competitive value. The structural fix (option 2) depends on GAP-04's compiler being built, which is L-effort; until then, option 1's point patches are the only mitigation in production.

## Reversibility

High for the two point patches (parameterising a call site is a local, independently revertible change). The structural fix's reversibility matches ADR-KG3-12's: once adapters no longer build scripts at all, reverting to string-building would mean deliberately reintroducing the vulnerability this ADR exists to close, which should never be the correct direction.

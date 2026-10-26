# EPIC-LIVINGAIAGGGRA-NOTEST: living-AI-agg-Graffin-requirements.md · code_no_test

*Code references the ID but no test is mapped.* 2 tasks, ~7.2 h, priorities {'P0': 2}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-GRF-SEC-001 [P0] GRF-SEC-001: Cryptographic Constitution Verification Engine

- **Source:** `living-AI-agg-Graffin-requirements.md:256-262` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 3 other site(s): see duplicate task DUP-GRF-SEC-001; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 3.0 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### `GRF-SEC-001`: Cryptographic Constitution Verification Engine
- **Description**: Before Graffin executes any task, the runtime **MUST** verify the cryptographic hash of its constitution against WORM storage.
- **Specification**: If `sha256(constitution.json) != EXPECTED_WORM_HASH`, Graffin enters locked state `STATE_TAMPER_DETECTED` and shuts down.
- **Done-When**:
  - `GRF-SEC-001.D01`: Tampering with any byte in `constitution.json` blocks Graffin startup with exit code 65.
  - `GRF-SEC-001.D02`: Valid constitution initializes Graffin in authorized state.
```
</details>

**Next steps**
1. Read the referenced code: reva/agents/graffin/constitution.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GRF-SEC-001') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-GRF-SEC-001

**Acceptance criteria**
- [ ] Before Graffin executes any task, the runtime MUST verify the cryptographic hash of its constitution against WORM storage.
- [ ] Description: Before Graffin executes any task, the runtime MUST verify the cryptographic hash of its constitution against WORM storage
- [ ] Specification: If sha256(constitution.json) != EXPECTEDWORMHASH, Graffin enters locked state STATETAMPERDETECTED and shuts down
- [ ] GRF-SEC-001.D01: Tampering with any byte in constitution.json blocks Graffin startup with exit code 65
- [ ] GRF-SEC-001.D02: Valid constitution initializes Graffin in authorized state
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/agents/graffin/constitution.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/agents/graffin/constitution.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GRF-SEC-002 [P0] GRF-SEC-002: Kill Switch Implementation & Verification

- **Source:** `living-AI-agg-Graffin-requirements.md:263-272` (heading) · **Type:** Security · **Severity:** High
- **Now:** Not Verified / L1 (tests passed 0, failed 0)
- **Gaps:** Code references the ID but no test is mapped; ID defined at 3 other site(s): see duplicate task DUP-GRF-SEC-002; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 4.2 h (M, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
### `GRF-SEC-002`: Kill Switch Implementation & Verification
- **Description**: The platform **MUST** implement multi-channel kill switch handlers terminating Graffin within $\le 500\text{ ms}$.
- **Specification**:
  * OS Signal Handler: Traps `SIGTERM`, `SIGINT`.
  * REST API Handler: `POST /api/graffin/v1/kill` requiring bearer token.
  * Heartbeat Monitor: Checks `.data/graffin_heartbeat` every $100\text{ ms}$.
- **Done-When**:
  - `GRF-SEC-002.D01`: Triggering kill switch terminates process in $< 500\text{ ms}$ verified by timer tests.
  - `GRF-SEC-002.D02`: All uncommitted database transactions and leases are cleanly released.
```
</details>

**Next steps**
1. Read the referenced code: reva/agents/graffin/kill_switch.py:2
2. Write one test per acceptance criterion; mark with @pytest.mark.req('GRF-SEC-002') and add to requirements-test-map.json
3. Run locally (L2), then via CI (L3)
4. Resolve duplicate definition first: DUP-GRF-SEC-002

**Acceptance criteria**
- [ ] The platform MUST implement multi-channel kill switch handlers terminating Graffin within $\le 500\text{ ms}$.
- [ ] Description: The platform MUST implement multi-channel kill switch handlers terminating Graffin within $\le 500\text{ ms}$
- [ ] OS Signal Handler: Traps SIGTERM, SIGINT
- [ ] REST API Handler: POST /api/graffin/v1/kill requiring bearer token
- [ ] Heartbeat Monitor: Checks .data/graffinheartbeat every $100\text{ ms}$
- [ ] GRF-SEC-002.D01: Triggering kill switch terminates process in $< 500\text{ ms}$ verified by timer tests
- [ ] GRF-SEC-002.D02: All uncommitted database transactions and leases are cleanly released
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`reva/agents/graffin/kill_switch.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/reva/agents/graffin/kill_switch.py#L2-L2)

**Proof plan (1.1):** have ['L1']; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']


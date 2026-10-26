# EPIC-REVA-UNTR-03: reva-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 60 tasks, ~363.5 h, priorities {'P2': 60}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-RC-28 [P2] RC-28: Doctor / setup / update (per-client registration diagnosis, dry-run plans, backups, approval) for ~20 agent clients

- **Source:** `reva-requirements.md:140-140` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-28; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-28 | Doctor / setup / update (per-client registration diagnosis, dry-run plans, backups, approval) for ~20 agent clients | `src/application/Doctor*.ts`, `Setup*.ts`, `Update*.ts`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-28' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-28') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-28

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-28 | Doctor / setup / update (per-client registration diagnosis, dry-run plans, backups, approval) for ~20 agent clients | src/application/Doctor.ts, Setup.ts, Update*.ts»
- [ ] Doctor / setup / update (per-client registration diagnosis, dry-run plans, backups, approval) for ~20 agent clients
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-29 [P2] RC-29: Behavioural test depth taxonomy (module, composition, boundary, MCP boundary, acceptance, conformance, evaluation; "paths and suite names do not establish depth")

- **Source:** `reva-requirements.md:141-141` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-29; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-29 | Behavioural test depth taxonomy (module, composition, boundary, MCP boundary, acceptance, conformance, evaluation; "paths and suite names do not establish depth") | `docs/testing.md`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-29' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-29') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-29

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-29 | Behavioural test depth taxonomy (module, composition, boundary, MCP boundary, acceptance, conformance, evaluation; "paths and suite names do not establish depth") | docs/testing.md»
- [ ] Behavioural test depth taxonomy (module, composition, boundary, MCP boundary, acceptance, conformance, evaluation; "paths and suite names do not establish depth")
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-30 [P2] RC-30: Native analysis via Hopper/Ghidra/IDA/Kuna/Rizin/objdump (pseudocode, assembly, xrefs, CFG, call paths, byte search)

- **Source:** `reva-requirements.md:142-142` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-30; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-30 | Native analysis via Hopper/Ghidra/IDA/Kuna/Rizin/objdump (pseudocode, assembly, xrefs, CFG, call paths, byte search) | `src/hopper`, `src/ghidra`, `src/ida`, `src/kuna`, `src/rizin`, `src/objdump`, `bridge/*`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-30' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-30') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-30

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-30 | Native analysis via Hopper/Ghidra/IDA/Kuna/Rizin/objdump (pseudocode, assembly, xrefs, CFG, call paths, byte search) | src/hopper, src/ghidra, src/ida, src/kuna, src/rizin, src/objdump, bridge/*»
- [ ] Native analysis via Hopper/Ghidra/IDA/Kuna/Rizin/objdump (pseudocode, assembly, xrefs, CFG, call paths, byte search)
- [ ] src/hopper, src/ghidra, src/ida, src/kuna, src/rizin, src/objdump, bridge/*
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-31 [P2] RC-31: Debugging and instrumentation (GDB/MI, pwndbg, Rizin debug, Frida, LLDB tracer)

- **Source:** `reva-requirements.md:143-143` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-31; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-31 | Debugging and instrumentation (GDB/MI, pwndbg, Rizin debug, Frida, LLDB tracer) | `src/gdb`, `src/frida`, `bridge/native/rea_lldb_tracer.py`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-31' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-31') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-31

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-31 | Debugging and instrumentation (GDB/MI, pwndbg, Rizin debug, Frida, LLDB tracer) | src/gdb, src/frida, bridge/native/rea_lldb_tracer.py»
- [ ] Debugging and instrumentation (GDB/MI, pwndbg, Rizin debug, Frida, LLDB tracer)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-32 [P2] RC-32: Android/ADB/JADX/Apktool/JEB/Flutter/Harmony analysis: src/adb, src/android, src/apktool, src/jeb, src/flutter, src/domain/harmony

- **Source:** `reva-requirements.md:144-144` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-32; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-32 | Android/ADB/JADX/Apktool/JEB/Flutter/Harmony analysis | `src/adb`, `src/android`, `src/apktool`, `src/jeb`, `src/flutter`, `src/domain/harmony`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-32' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-32') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-32

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-32 | Android/ADB/JADX/Apktool/JEB/Flutter/Harmony analysis | src/adb, src/android, src/apktool, src/jeb, src/flutter, src/domain/harmony»
- [ ] src/adb, src/android, src/apktool, src/jeb, src/flutter, src/domain/harmony
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-33 [P2] RC-33: Firmware (Binwalk/Unblob), pcap/TShark, sigrok signal decoding, EVM, WASM, DOS/PSP/MIPS/PPC/RISC-V profiles, Apple bundles, PE resources, recorded crashes

- **Source:** `reva-requirements.md:145-145` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-33; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-33 | Firmware (Binwalk/Unblob), pcap/TShark, sigrok signal decoding, EVM, WASM, DOS/PSP/MIPS/PPC/RISC-V profiles, Apple bundles, PE resources, recorded crashes | `src/firmware`, `src/pcap`, `src/signals`, `src/evm`, `src/wasm`, `src/ghidra/*Profile.ts`, `src/domain/apple`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-33' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-33') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-33

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-33 | Firmware (Binwalk/Unblob), pcap/TShark, sigrok signal decoding, EVM, WASM, DOS/PSP/MIPS/PPC/RISC-V profiles, Apple bundles, PE resources, recorded crashes | src/firmware, src/pcap, src/signals, src/evm, src/wasm, src/ghidra/*Profile.ts, src/domain/apple»
- [ ] Firmware (Binwalk/Unblob), pcap/TShark, sigrok signal decoding, EVM, WASM, DOS/PSP/MIPS/PPC/RISC-V profiles, Apple bundles, PE resources, recorded crashes
- [ ] src/firmware, src/pcap, src/signals, src/evm, src/wasm, src/ghidra/*Profile.ts, src/domain/apple
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RC-34 [P2] RC-34: Runtime observation: browser/Electron CDP capture and scenarios, V8 Inspector, process PTY capture, native UI capture

- **Source:** `reva-requirements.md:146-146` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; ID defined at 2 other site(s): see duplicate task DUP-RC-34; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 6.5 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RC-34 | Runtime observation: browser/Electron CDP capture and scenarios, V8 Inspector, process PTY capture, native UI capture | `src/browser`, `src/inspector`, `src/process/capture`, `bridge/native`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RC-34' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RC-34') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)
5. Resolve duplicate definition first: DUP-RC-34

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RC-34 | Runtime observation: browser/Electron CDP capture and scenarios, V8 Inspector, process PTY capture, native UI capture | src/browser, src/inspector, src/process/capture, bridge/native»
- [ ] Runtime observation: browser/Electron CDP capture and scenarios, V8 Inspector, process PTY capture, native UI capture
- [ ] src/browser, src/inspector, src/process/capture, bridge/native
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-003 [P2] REVA-AB-003: Outbound HTTP calls — JS/TS: fetch, axios(.get/.post/…/request), axios.create({baseURL}) instances, got, node:http(s).request, ky. Java: RestTemplate.*, WebClient…uri(…), `@FeignClient(name\ · url) in

- **Source:** `reva-requirements.md:877-877` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-003 | **Outbound HTTP calls** — JS/TS: `fetch`, `axios(.get/.post/…/request)`, `axios.create({baseURL})` instances, `got`, `node:http(s).request`, `ky`. Java: `RestTemplate.*`, `WebClient…uri(…)`, `@FeignClient(name\|url)` interfaces with mapping annotations, `HttpClient` (`java.net.http`). Python: `requests.*`, `httpx.*` (sync/async clients with `base_url`), `aiohttp.ClientSession.*`. | Golden outbound sets per fixture, including base-URL composition. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Golden outbound sets per fixture, including base-URL composition
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-004 [P2] REVA-AB-004: Messaging and RPC: Kafka (kafkajs producer.send({topic}), consumer.subscribe({topic}); Spring KafkaTemplate.send(topic, …), @KafkaListener(topics=…); confluent-kafka/kafka-python produce(topic)/subscr

- **Source:** `reva-requirements.md:878-878` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-004 | **Messaging and RPC**: Kafka (kafkajs `producer.send({topic})`, `consumer.subscribe({topic})`; Spring `KafkaTemplate.send(topic, …)`, `@KafkaListener(topics=…)`; confluent-kafka/kafka-python `produce(topic)`/`subscribe([...])`), RabbitMQ/AMQP (`sendToQueue`, `publish(exchange, routingKey)`, `@RabbitListener(queues=…)`), GraphQL client operations (`gql`/`graphql` tagged templates: operation type and name), gRPC service/method definitions from `.proto` files and client stub calls (by generated method names), Electron IPC (`ipcMain.handle/on`, `ipcRenderer.invoke/send`, `contextBridge.exposeInMainWorld`), scheduled jobs (`@Scheduled`, node-cron, Celery beat), CLI commands (argparse/click/typer/commander/picocli). | Golden sets per fixture; IPC pairing produces `invokes→handles` links only for literal channel matches; dynamic channels are kept unpaired with a gap. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Golden sets per fixture; IPC pairing produces invokes→handles links only for literal channel matches; dynamic channels are kept unpaired with a gap
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-005 [P2] REVA-AB-005: Constant and template resolution: resolve string literals, same-file constants, simple cross-file imported constants (depth ≤ 2), Spring @Value("${prop}") and @ConfigurationProperties against applicat

- **Source:** `reva-requirements.md:879-879` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-005 | **Constant and template resolution**: resolve string literals, same-file constants, simple cross-file imported constants (depth ≤ 2), Spring `@Value("${prop}")` and `@ConfigurationProperties` against `application*.yml/properties` (profile-aware: default + each named profile listed), `process.env.X` / `os.environ["X"]` against `.env*`, Compose and Helm values files present in the repo. Templates (`${id}`, f-strings, `String.format`, concatenation, `{id}` in annotations, `:id` Express params, `<int:id>` Flask converters) normalize to canonical `{}` segments. Unresolvable parts make the boundary `resolution: partial`, keeping the expression text and source span. | Fixture with each resolution style yields the expected canonical templates; unresolved parts keep the original expression. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with each resolution style yields the expected canonical templates; unresolved parts keep the original expression
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-007 [P2] REVA-AB-007: Service identity: a service = a deployable unit determined by, in order, (1) an explicit reva-service.yaml in the repo, (2) build descriptors (Maven/Gradle module, package.json with start script, pypr

- **Source:** `reva-requirements.md:881-881` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-007 | **Service identity**: a service = a deployable unit determined by, in order, (1) an explicit `reva-service.yaml` in the repo, (2) build descriptors (Maven/Gradle module, `package.json` with `start` script, `pyproject.toml`), (3) Dockerfile/Compose/Helm service names. Logical key = `svc:<repo_id>/<service_name>`. | Mono-repo fixture with three services is split correctly. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Mono-repo fixture with three services is split correctly
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-011 [P2] REVA-AB-011: Coverage and limitations: per repo and per file: files examined/skipped (by language, size limit REVA_AB_MAX_FILE_BYTES default 2 MiB, generated-code patterns, vendored dirs), parse errors, unresolved

- **Source:** `reva-requirements.md:885-885` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-011 | **Coverage and limitations**: per repo and per file: files examined/skipped (by language, size limit `REVA_AB_MAX_FILE_BYTES` default 2 MiB, generated-code patterns, vendored dirs), parse errors, unresolved dynamic dispatch, reflection, runtime registration. Statements never claim runtime reachability. | Coverage counts equal the fixture's file counts; limitation codes match §10.3. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Coverage counts equal the fixture's file counts; limitation codes match §10.3
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-012 [P2] REVA-AB-012: Incremental extraction: given the previous run's per-file digests, re-extract only changed files plus files whose resolved constants depend on changed files (dependency index); results equal a full re

- **Source:** `reva-requirements.md:886-886` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-012 | **Incremental extraction**: given the previous run's per-file digests, re-extract only changed files plus files whose resolved constants depend on changed files (dependency index); results equal a full re-extraction. | Property test on random edit sequences: incremental result == full result. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Property test on random edit sequences: incremental result == full result
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AB-013 [P2] REVA-AB-013: Projection: reva_Service, reva_Boundary, reva_Resource vertices; reva_EXPOSES, reva_CALLS, reva_ACCESSES edges; links to KGF's code-graph symbol vertices (by repo/path/symbol) when they exist (reva_DE

- **Source:** `reva-requirements.md:887-887` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AB-013 | **Projection**: `reva_Service`, `reva_Boundary`, `reva_Resource` vertices; `reva_EXPOSES`, `reva_CALLS`, `reva_ACCESSES` edges; links to KGF's code-graph symbol vertices (by repo/path/symbol) when they exist (`reva_DEFINED_IN` property `symbol_ref`). | Graph queries on each backend return the expected subgraph for the fixture (conformance suite across HugeGraph, Neo4j, Neptune-compatible Gremlin). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AB-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AB-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Graph queries on each backend return the expected subgraph for the fixture (conformance suite across HugeGraph, Neo4j, Neptune-compatible Gremlin)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-002 [P2] REVA-AI-002: Safety limits (configurable): max total uncompressed bytes (default 8 GiB), max member count (500,000), max nesting depth (6), max compression ratio per member (200:1) and overall (100:1), max path le

- **Source:** `reva-requirements.md:843-843` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-002 | Safety limits (configurable): max total uncompressed bytes (default 8 GiB), max member count (500,000), max nesting depth (6), max compression ratio per member (200:1) and overall (100:1), max path length (4,096), max single member (2 GiB). Breaches stop expansion of that subtree, record the limit, and set coverage `partial`. | Zip-bomb (42.zip-style, generated by the test suite) and deep-nesting fixtures are contained with correct limits recorded. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AI-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AI-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Zip-bomb (42.zip-style, generated by the test suite) and deep-nesting fixtures are contained with correct limits recorded
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-003 [P2] REVA-AI-003: Path safety: reject absolute paths, .. traversal, drive letters, NUL bytes and device files; symlinks and hard links are recorded as link entries and never followed or materialized outside the extract

- **Source:** `reva-requirements.md:844-844` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-003 | Path safety: reject absolute paths, `..` traversal, drive letters, NUL bytes and device files; symlinks and hard links are recorded as link entries and **never followed or materialized outside the extraction root**. Case-colliding names are kept as distinct members. | Traversal and symlink-escape fixtures produce rejections recorded as limitations; nothing is written outside the root. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AI-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AI-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Traversal and symlink-escape fixtures produce rejections recorded as limitations; nothing is written outside the root
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-004 [P2] REVA-AI-004: Member identity: every member gets {member_path (normalized POSIX), size, sha256, media_type, format, mode, mtime (recorded but non-semantic)}; nested containers recurse within limits. Duplicate conte

- **Source:** `reva-requirements.md:845-845` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-004 | Member identity: every member gets `{member_path (normalized POSIX), size, sha256, media_type, format, mode, mtime (recorded but non-semantic)}`; nested containers recurse within limits. Duplicate content is stored once per tenant blob namespace. | Inventory of a JAR containing nested JARs lists all levels with digests; re-inventory yields identical warrant IDs. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AI-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AI-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Inventory of a JAR containing nested JARs lists all levels with digests; re-inventory yields identical warrant IDs
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-006 [P2] REVA-AI-006: Output: one reva.pred.artifact_inventory warrant per container (statement = member table digest + counts + nested container list; the full member table stored as a blob), reva_Artifact vertices and re

- **Source:** `reva-requirements.md:847-847` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-006 | Output: one `reva.pred.artifact_inventory` warrant per container (statement = member table digest + counts + nested container list; the full member table stored as a blob), `reva_Artifact` vertices and `reva_CONTAINS` edges (projection batched). | A 10,000-member archive produces one warrant and 10,001 projected vertices; the view API pages the member table. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AI-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AI-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A 10,000-member archive produces one warrant and 10,001 projected vertices; the view API pages the member table
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AI-007 [P2] REVA-AI-007: Safe extraction API (extract(artifact_id, members[], dest)) for downstream extractors only: writes into a REVA-owned temp root, applies the same safety rules, and returns digests verified after write.

- **Source:** `reva-requirements.md:848-848` (table_row) · **Type:** AI · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AI-007 | Safe extraction API (`extract(artifact_id, members[], dest)`) for downstream extractors only: writes into a REVA-owned temp root, applies the same safety rules, and returns digests verified after write. | Extracted file digests equal inventory digests. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AI-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AI-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Extracted file digests equal inventory digests
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-002 [P2] REVA-AS-002: Streaming processing with bounded memory (≤ 512 MiB for 10 M records) using per-group accumulators; inputs up to 50 GiB per job. · Performance test meets REVA-NFR-006. · integration

- **Source:** `reva-requirements.md:898-898` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-002 | Streaming processing with bounded memory (≤ 512 MiB for 10 M records) using per-group accumulators; inputs up to 50 GiB per job. | Performance test meets REVA-NFR-006. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AS-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AS-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Performance test meets REVA-NFR-006
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-005 [P2] REVA-AS-005: Per operation: methods, statuses histogram, content types, request/response JSON key-shapes (key paths with types and presence ratios, no values), query parameter names, first/last seen, call count, p

- **Source:** `reva-requirements.md:901-901` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-005 | Per operation: methods, statuses histogram, content types, request/response JSON key-shapes (key paths with types and presence ratios, no values), query parameter names, first/last seen, call count, p50/p95 latency when timings exist, callers. | Golden summary per fixture. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AS-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AS-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Golden summary per fixture
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-006 [P2] REVA-AS-006: Caller attribution: OTel client spans (service.name → peer.service/server.address); access logs via REVA_AS_CALLER_MAP (source CIDR/user-agent → service); HAR via a capture-level caller_service parame

- **Source:** `reva-requirements.md:902-902` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-006 | Caller attribution: OTel client spans (`service.name` → `peer.service`/`server.address`); access logs via `REVA_AS_CALLER_MAP` (source CIDR/user-agent → service); HAR via a capture-level `caller_service` parameter. Unattributable calls keep `caller: unknown`. | Fixture with mixed attribution yields correct callers and an explicit unknown bucket. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AS-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AS-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with mixed attribution yields correct callers and an explicit unknown bucket
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-007 [P2] REVA-AS-007: Output: reva_ApiOperation vertices, runtime-observed reva_CALLS edges (caller service → operation), and links from operations to static routes (via RR). Coverage records the time window, sampling (OTe

- **Source:** `reva-requirements.md:903-903` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-007 | Output: `reva_ApiOperation` vertices, runtime-observed `reva_CALLS` edges (caller service → operation), and links from operations to static routes (via RR). Coverage records the time window, sampling (OTel sampled flag or configured rate) and dropped/malformed counts; sampled data always yields `partial`. | Coverage fields present and correct; sampled fixture reports partial. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AS-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AS-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Coverage fields present and correct; sampled fixture reports partial
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-AS-008 [P2] REVA-AS-008: OpenAPI alignment report: operations observed but not in the spec (undocumented), in the spec but never observed in the window (unobserved, not "dead"), and parameter mismatches. · Fixture spec vs tra

- **Source:** `reva-requirements.md:904-904` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-AS-008 | OpenAPI alignment report: operations observed but not in the spec (undocumented), in the spec but never observed in the window (unobserved, not "dead"), and parameter mismatches. | Fixture spec vs traffic yields all three categories. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-AS-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-AS-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture spec vs traffic yields all three categories
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-BD-002 [P2] REVA-BD-002: Control Flow Graph (CFG) isomorphism & Graph Edit Distance (GED) scoring. Computes CFG structural similarity between candidate function pairs across versions; scores similarity in $[0, 1]$ based on ba

- **Source:** `reva-requirements.md:1171-1171` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-BD-002 | Control Flow Graph (CFG) isomorphism & Graph Edit Distance (GED) scoring. Computes CFG structural similarity between candidate function pairs across versions; scores similarity in $[0, 1]$ based on basic-block topology and control flow transitions. | Correctly matches modified functions with 90%+ GED similarity when minor instruction tweaks occur; distinguishes true changes from completely rewritten functions. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-BD-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-BD-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Correctly matches modified functions with 90%+ GED similarity when minor instruction tweaks occur; distinguishes true changes from completely rewritten functions
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CV-003 [P2] REVA-CV-003: Presentation rule: API, MCP and UI render an empty set with non-complete coverage as "Unknown — not proven empty" and show the reasons. · Acceptance test on the Impact Trace screen and the REST respon

- **Source:** `reva-requirements.md:708-708` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CV-003 | Presentation rule: API, MCP and UI render an empty set with non-complete coverage as **"Unknown — not proven empty"** and show the reasons. | Acceptance test on the Impact Trace screen and the REST response for a partial trace. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CV-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CV-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Acceptance test on the Impact Trace screen and the REST response for a partial trace
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CV-004 [P2] REVA-CV-004: Connector coverage: KGF connectors report sync watermarks and gaps (failed pages, rate-limited windows) through SourcePort.coverage(source_id). REVA stores them and composes them into per_source cover

- **Source:** `reva-requirements.md:709-709` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CV-004 | Connector coverage: KGF connectors report sync watermarks and gaps (failed pages, rate-limited windows) through `SourcePort.coverage(source_id)`. REVA stores them and composes them into `per_source` coverage for any query touching data from that source. | A trace touching Jira data during a simulated rate-limit outage reports `partial` with the Jira watermark. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CV-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CV-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A trace touching Jira data during a simulated rate-limit outage reports partial with the Jira watermark
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CV-005 [P2] REVA-CV-005: Coverage-aware absence assertions: the helper assert_absent(query) -> AbsenceResult returns proven_absent only under complete coverage of the relevant scope; otherwise not_found_unknown. · Used by the

- **Source:** `reva-requirements.md:710-710` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CV-005 | Coverage-aware absence assertions: the helper `assert_absent(query) -> AbsenceResult` returns `proven_absent` only under complete coverage of the relevant scope; otherwise `not_found_unknown`. | Used by the trace engine and the answer contract; unit tests for both branches. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CV-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CV-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Used by the trace engine and the answer contract; unit tests for both branches
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CX-004 [P2] REVA-CX-004: Propagation: open contradictions set reva_has_contradiction=true on affected graph elements, block closure of linked obligations (CLOSURE_BLOCKED_CONTRADICTION), and appear in grounded answers that us

- **Source:** `reva-requirements.md:736-736` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CX-004 | Propagation: open contradictions set `reva_has_contradiction=true` on affected graph elements, block closure of linked obligations (`CLOSURE_BLOCKED_CONTRADICTION`), and appear in grounded answers that use any member warrant. | Acceptance check through RJ-02. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CX-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CX-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Acceptance check through RJ-02
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-CX-005 [P2] REVA-CX-005: Record-and-continue policy for extractors: integrity_policy ∈ {fail_closed (default), record_and_continue}. Under record_and_continue, verified siblings continue, contradicted items are quarantined, a

- **Source:** `reva-requirements.md:737-737` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-CX-005 | Record-and-continue policy for extractors: `integrity_policy ∈ {fail_closed (default), record_and_continue}`. Under `record_and_continue`, verified siblings continue, contradicted items are quarantined, and result coverage becomes `partial`. | Inventory of an archive with one corrupted member under both policies behaves as specified. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-CX-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-CX-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Inventory of an archive with one corrupted member under both policies behaves as specified
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DB-004 [P2] REVA-DB-004: Linking: reva_DbObject vertices; FK edges; reva_Resource(db_table) from AB matched to DbObjects by (db_instance mapping, schema, name), case-normalized per dialect; ambiguous matches → gap. · Fixture 

- **Source:** `reva-requirements.md:915-915` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DB-004 | Linking: `reva_DbObject` vertices; FK edges; `reva_Resource(db_table)` from AB matched to DbObjects by `(db_instance mapping, schema, name)`, case-normalized per dialect; ambiguous matches → gap. | Fixture links code tables to DB tables; an ambiguous same-name table in two schemas produces a gap. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DB-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DB-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture links code tables to DB tables; an ambiguous same-name table in two schemas produces a gap
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DB-005 [P2] REVA-DB-005: Schema diff over time through GD (tables/columns added, removed, changed) with valid-time history. · Two snapshots yield the correct diff. · integration

- **Source:** `reva-requirements.md:916-916` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DB-005 | Schema diff over time through GD (tables/columns added, removed, changed) with valid-time history. | Two snapshots yield the correct diff. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DB-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DB-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Two snapshots yield the correct diff
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DI-005 [P2] REVA-DI-005: Core dump & crash artifact analyzer. Parses ELF core dumps and Windows minidumps; reconstructs crashed thread registers, faulting instruction address, stack backtrace, and loaded shared library maps. 

- **Source:** `reva-requirements.md:1140-1140` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DI-005 | Core dump & crash artifact analyzer. Parses ELF core dumps and Windows minidumps; reconstructs crashed thread registers, faulting instruction address, stack backtrace, and loaded shared library maps. | Analyzes Linux ELF core dump fixture; identifies faulting signal (e.g. SIGSEGV), faulting address, and backtrace; links crash address to corresponding `reva_BinaryFunction`. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DI-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DI-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Analyzes Linux ELF core dump fixture; identifies faulting signal (e.g. SIGSEGV), faulting address, and backtrace; links crash address to corresponding revaBinaryFunction
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DR-003 [P2] REVA-DR-003: Doctor results are exposed at GET /doctor (admin only) and summarized in KGF's health endpoint (IP-10) as `reva: ok\ · degraded\ · down`.

- **Source:** `reva-requirements.md:1017-1017` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DR-003 | Doctor results are exposed at `GET /doctor` (admin only) and summarized in KGF's health endpoint (IP-10) as `reva: ok\|degraded\|down`. | Health endpoint shows degraded when the blob store is read-only. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Health endpoint shows degraded when the blob store is read-only
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-DV-001 [P2] REVA-DV-001: Claim inputs: an artifact (or image) plus an expected commit (from a deployment record, Jira release, or user input). · API accepts all three sources. · integration

- **Source:** `reva-requirements.md:963-963` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-DV-001 | Claim inputs: an artifact (or image) plus an expected commit (from a deployment record, Jira release, or user input). | API accepts all three sources. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-DV-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-DV-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] API accepts all three sources
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-001 [P2] REVA-FT-001: Seeds (typed): entity_id, string, service_account, config_key, env_var, route, topic, table, file_path, symbol, rule_id, jira_key, commit, api_operation, artifact. Match modes exact (default for all b

- **Source:** `reva-requirements.md:935-935` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-001 | Seeds (typed): `entity_id`, `string`, `service_account`, `config_key`, `env_var`, `route`, `topic`, `table`, `file_path`, `symbol`, `rule_id`, `jira_key`, `commit`, `api_operation`, `artifact`. Match modes `exact` (default for all but `string`) and `contains`; case sensitivity flag; an empty value is only allowed with `exact`. Seed resolution returns matches with a basis (`id, logical_key, label, property, alias`). | Each seed kind has a fixture; an empty `contains` seed is rejected. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each seed kind has a fixture; an empty contains seed is rejected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-002 [P2] REVA-FT-002: Traversal policies per question template, each a set of allowed edge labels with directions: impact.downstream (dependents), impact.upstream (dependencies), impact.both, plus named templates impact.se

- **Source:** `reva-requirements.md:936-936` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-002 | Traversal policies per question template, each a set of allowed edge labels with directions: `impact.downstream` (dependents), `impact.upstream` (dependencies), `impact.both`, plus named templates `impact.service_account`, `impact.rule_change`, `impact.feature_change`, `who_changed.symbol`, `incident.root_candidates`, `test_scope.change`. Templates are data (YAML in `reva/workflows/trace_templates/`), versioned, and listed by API. | Each template returns the golden result on the reference fixture graph (§13 RJ-03/RJ-04). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each template returns the golden result on the reference fixture graph (§13 RJ-03/RJ-04)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-005 [P2] REVA-FT-005: Output groups: impacted services, boundaries, resources, deployments/builds, repositories/files/symbols, Jira stories/epics, owners/teams, tests (REVA-FT-006), open gaps and contradictions in the subg

- **Source:** `reva-requirements.md:939-939` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-005 | Output groups: impacted services, boundaries, resources, deployments/builds, repositories/files/symbols, Jira stories/epics, owners/teams, tests (REVA-FT-006), open gaps and contradictions in the subgraph; each item lists supporting paths and warrant IDs. | Group counts match the fixture expectations. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Group counts match the fixture expectations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-006 [P2] REVA-FT-006: Test-scope recommendation: tests whose per-test coverage contexts (from REVA verifier runs) touched any impacted symbol, ranked by number of impacted symbols hit; tests with stale coverage data (older

- **Source:** `reva-requirements.md:940-940` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-006 | Test-scope recommendation: tests whose per-test coverage contexts (from REVA verifier runs) touched any impacted symbol, ranked by number of impacted symbols hit; tests with stale coverage data (older than the symbol's current version) are flagged; when no coverage data exists, say so (gap), never "no tests needed". | Fixture with coverage maps recommends the expected tests; missing data produces a gap. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with coverage maps recommends the expected tests; missing data produces a gap
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-007 [P2] REVA-FT-007: As-of traversal: as_of_valid and as_of_recorded parameters restrict the graph to elements valid / known at those instants. · Fixture with time-varying ownership returns different owners for two as-of 

- **Source:** `reva-requirements.md:941-941` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-007 | As-of traversal: `as_of_valid` and `as_of_recorded` parameters restrict the graph to elements valid / known at those instants. | Fixture with time-varying ownership returns different owners for two as-of dates. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture with time-varying ownership returns different owners for two as-of dates
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-008 [P2] REVA-FT-008: Every trace result is itself a warrant (reva.pred.trace_result, derived, links to all edge warrants used, coverage composed) with a trc1_ ID, so answers can cite it. · Re-running on unchanged data yie

- **Source:** `reva-requirements.md:942-942` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-008 | Every trace result is itself a warrant (`reva.pred.trace_result`, `derived`, links to all edge warrants used, coverage composed) with a `trc1_` ID, so answers can cite it. | Re-running on unchanged data yields the same trace ID. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Re-running on unchanged data yields the same trace ID
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-FT-009 [P2] REVA-FT-009: Performance: REVA-NFR-004. Traversal pushes filters down to the backend where the GraphPort reports capability; otherwise it runs in REVA with batched neighbour fetches. · Benchmark passes on each bac

- **Source:** `reva-requirements.md:943-943` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-FT-009 | Performance: REVA-NFR-004. Traversal pushes filters down to the backend where the GraphPort reports capability; otherwise it runs in REVA with batched neighbour fetches. | Benchmark passes on each backend in CI (Neptune via a Gremlin-compatible lane, or named skip). | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-FT-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-FT-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Benchmark passes on each backend in CI (Neptune via a Gremlin-compatible lane, or named skip)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GA-001 [P2] REVA-GA-001: Answer contract: `{answer_id, question, mode: deterministic\ · llm_synthesized, claims:[{claim_id, text, kind: observed\ · derived\

- **Source:** `reva-requirements.md:1001-1001` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-001 | Answer contract: `{answer_id, question, mode: deterministic\|llm_synthesized, claims:[{claim_id, text, kind: observed\|derived\|inferred\|unknown, warrant_ids[], confidence{band,score_bp}, coverage}], unknowns[], contradictions[], limitations[], coverage, trace_ids[]}`. Rendering groups claims under **Observed / Derived / Inferred / Unknown** and shows contradictions prominently. | Answer view acceptance test; schema test. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Answer view acceptance test; schema test
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GA-004 [P2] REVA-GA-004: Citation verification: after synthesis, every claim must cite ≥ 1 warrant from the supplied context. The claim's kind must not exceed the weakest cited epistemic state (an inferred warrant cannot back

- **Source:** `reva-requirements.md:1004-1004` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-004 | Citation verification: after synthesis, every claim must cite ≥ 1 warrant from the supplied context. The claim's kind must not exceed the weakest cited epistemic state (an inferred warrant cannot back an "observed" claim). Uncited claims are dropped or downgraded to `inferred` with limitation `UNCITED_CLAIM`, per `REVA_GA_UNCITED_POLICY` (default `drop`). | Fixture LLM outputs with uncited, mis-graded and correct claims are handled per policy. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture LLM outputs with uncited, mis-graded and correct claims are handled per policy
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GA-005 [P2] REVA-GA-005: Absence questions ("is X used anywhere?", "which systems call Y?") use coverage-aware absence (REVA-CV-005); answers never say "none/no" unless proven absent under complete coverage. · Partial-coverag

- **Source:** `reva-requirements.md:1005-1005` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GA-005 | Absence questions ("is X used anywhere?", "which systems call Y?") use coverage-aware absence (REVA-CV-005); answers never say "none/no" unless proven absent under complete coverage. | Partial-coverage fixture yields "Unknown — not proven" phrasing. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GA-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GA-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Partial-coverage fixture yields "Unknown — not proven" phrasing
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GD-001 [P2] REVA-GD-001: Inputs: two snapshot selectors ({scope, commit} or {scope, as_of}) or two warrant-backed graph exports. · Each selector type works on fixtures. · integration

- **Source:** `reva-requirements.md:951-951` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GD-001 | Inputs: two snapshot selectors (`{scope, commit}` or `{scope, as_of}`) or two warrant-backed graph exports. | Each selector type works on fixtures. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GD-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GD-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each selector type works on fixtures
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GD-003 [P2] REVA-GD-003: Statuses: unchanged, changed, added, removed, moved, renamed, ambiguous; changed items list dimensions (content, location, properties, relationships, coverage) and property-level deltas. · E-06 regres

- **Source:** `reva-requirements.md:953-953` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GD-003 | Statuses: `unchanged, changed, added, removed, moved, renamed, ambiguous`; changed items list dimensions (`content, location, properties, relationships, coverage`) and property-level deltas. | **E-06 regression:** the v1→v2 fixture from §2.5 reports the 9 modules and the `accounts:rotate` handler as `changed`/`unchanged`, not removed+added; the new handler is `added`; the endpoint template change is `changed` with a property delta. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GD-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GD-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] E-06 regression: the v1→v2 fixture from §2.5 reports the 9 modules and the accounts:rotate handler as changed/unchanged, not removed+added; the new handler is added; the endpoint template change is changed with a property delta
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GD-004 [P2] REVA-GD-004: Change graph projection: reva_CHANGED_FROM edges new→old with match basis and confidence; diff result warrant reva.pred.graph_diff with coverage (min of both sides). · Projection and warrant verified.

- **Source:** `reva-requirements.md:954-954` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GD-004 | Change graph projection: `reva_CHANGED_FROM` edges new→old with match basis and confidence; diff result warrant `reva.pred.graph_diff` with coverage (min of both sides). | Projection and warrant verified. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GD-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GD-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Projection and warrant verified
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-GD-005 [P2] REVA-GD-005: Ontology/schema diff mode: classes, properties, constraints and DB schema objects compared with semantic categories (breaking / non-breaking / additive). · Fixture ontology pair yields correct categor

- **Source:** `reva-requirements.md:955-955` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-GD-005 | Ontology/schema diff mode: classes, properties, constraints and DB schema objects compared with semantic categories (breaking / non-breaking / additive). | Fixture ontology pair yields correct categories. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-GD-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-GD-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture ontology pair yields correct categories
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-002 [P2] REVA-IF-002: GET /warrants/{warrant_id} · Get warrant (verified) · viewer

- **Source:** `reva-requirements.md:1223-1223` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-002 | `GET /warrants/{warrant_id}` | Get warrant (verified) | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-002 | GET /warrants/{warrant_id} | Get warrant (verified) | viewer»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-004 [P2] REVA-IF-004: `GET /warrants/{id}/links?direction=in\ · out&rel=` · Link neighbourhood

- **Source:** `reva-requirements.md:1225-1225` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-004 | `GET /warrants/{id}/links?direction=in\|out&rel=` | Link neighbourhood | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-004 | `GET /warrants/{id}/links?direction=in\ | out&rel=` | Link neighbourhood | viewer»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-005 [P2] REVA-IF-005: POST /warrants/{id}/supersede, POST /warrants/{id}/retract · Supersede/retract · reviewer

- **Source:** `reva-requirements.md:1226-1226` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-005 | `POST /warrants/{id}/supersede`, `POST /warrants/{id}/retract` | Supersede/retract | reviewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-005 | POST /warrants/{id}/supersede, POST /warrants/{id}/retract | Supersede/retract | reviewer»
- [ ] POST /warrants/{id}/supersede, POST /warrants/{id}/retract
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-006 [P2] REVA-IF-006: POST /bundles/export, POST /bundles/import, GET /bundles/{id} · Bundles · analyst / admin (import)

- **Source:** `reva-requirements.md:1227-1227` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-006 | `POST /bundles/export`, `POST /bundles/import`, `GET /bundles/{id}` | Bundles | analyst / admin (import)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-006 | POST /bundles/export, POST /bundles/import, GET /bundles/{id} | Bundles | analyst / admin (import)»
- [ ] POST /bundles/export, POST /bundles/import, GET /bundles/{id}
- [ ] analyst / admin (import)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-007 [P2] REVA-IF-007: GET /predicates, GET /operations · Registries · viewer

- **Source:** `reva-requirements.md:1228-1228` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-007 | `GET /predicates`, `GET /operations` | Registries | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-007 | GET /predicates, GET /operations | Registries | viewer»
- [ ] GET /predicates, GET /operations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-008 [P2] REVA-IF-008: GET /producers, POST /producers, POST /producers/{id}/keys/rotate, POST /keys/{key_id}/revoke, GET /keys/public · Producers and keys · admin

- **Source:** `reva-requirements.md:1229-1229` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-008 | `GET /producers`, `POST /producers`, `POST /producers/{id}/keys/rotate`, `POST /keys/{key_id}/revoke`, `GET /keys/public` | Producers and keys | admin
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-008 | GET /producers, POST /producers, POST /producers/{id}/keys/rotate, POST /keys/{key_id}/revoke, GET /keys/public | Producers and keys | admin»
- [ ] GET /producers, POST /producers, POST /producers/{id}/keys/rotate, POST /keys/{key_id}/revoke, GET /keys/public
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-010 [P2] REVA-IF-010: GET /gaps, POST /gaps, GET /gaps/{gap_id}, PATCH /gaps/{gap_id} (with expected_revision), GET /gaps/{gap_id}/revisions, POST /gaps/{gap_id}/probes/{n}/run · Knowledge gaps · viewer / analyst

- **Source:** `reva-requirements.md:1230-1230` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-010 | `GET /gaps`, `POST /gaps`, `GET /gaps/{gap_id}`, `PATCH /gaps/{gap_id}` (with `expected_revision`), `GET /gaps/{gap_id}/revisions`, `POST /gaps/{gap_id}/probes/{n}/run` | Knowledge gaps | viewer / analyst
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-010 | GET /gaps, POST /gaps, GET /gaps/{gap_id}, PATCH /gaps/{gap_id} (with expected_revision), GET /gaps/{gap_id}/revisions, POST /gaps/{gap_id}/probes/{n}/run | Knowledge gaps | viewer / analyst»
- [ ] GET /gaps, POST /gaps, GET /gaps/{gap_id}, PATCH /gaps/{gap_id} (with expected_revision), GET /gaps/{gap_id}/revisions, POST /gaps/{gap_id}/probes/{n}/run
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-015 [P2] REVA-IF-015: GET /contradictions, GET /contradictions/{id}, POST /contradictions/{id}/resolve · Contradictions · viewer / reviewer

- **Source:** `reva-requirements.md:1231-1231` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-015 | `GET /contradictions`, `GET /contradictions/{id}`, `POST /contradictions/{id}/resolve` | Contradictions | viewer / reviewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-015 | GET /contradictions, GET /contradictions/{id}, POST /contradictions/{id}/resolve | Contradictions | viewer / reviewer»
- [ ] GET /contradictions, GET /contradictions/{id}, POST /contradictions/{id}/resolve
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-021 [P2] REVA-IF-021: GET /bindings, PUT /bindings/{obligation_key} · Bindings · reviewer

- **Source:** `reva-requirements.md:1233-1233` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-021 | `GET /bindings`, `PUT /bindings/{obligation_key}` | Bindings | reviewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-021' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-021') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-021 | GET /bindings, PUT /bindings/{obligation_key} | Bindings | reviewer»
- [ ] GET /bindings, PUT /bindings/{obligation_key}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-022 [P2] REVA-IF-022: POST /runs (start verifier run for binding(s)), GET /runs/{run_id}, POST /runs/{run_id}/cancel, GET /runs/{run_id}/artifacts/{kind} · Verifier runs · verifier

- **Source:** `reva-requirements.md:1234-1234` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-022 | `POST /runs` (start verifier run for binding(s)), `GET /runs/{run_id}`, `POST /runs/{run_id}/cancel`, `GET /runs/{run_id}/artifacts/{kind}` | Verifier runs | verifier
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-022' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-022') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-022 | POST /runs (start verifier run for binding(s)), GET /runs/{run_id}, POST /runs/{run_id}/cancel, GET /runs/{run_id}/artifacts/{kind} | Verifier runs | verifier»
- [ ] POST /runs (start verifier run for binding(s)), GET /runs/{run_id}, POST /runs/{run_id}/cancel, GET /runs/{run_id}/artifacts/{kind}
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-IF-023 [P2] REVA-IF-023: POST /closure/evaluate (scope), GET /ledgers/{ledger_id}, `GET /ledgers/{id}/export?format=json\ · md\ · html`

- **Source:** `reva-requirements.md:1235-1235` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-IF-023 | `POST /closure/evaluate` (scope), `GET /ledgers/{ledger_id}`, `GET /ledgers/{id}/export?format=json\|md\|html` | Closure and ledgers | viewer
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-IF-023' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-IF-023') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-IF-023 | POST /closure/evaluate (scope), GET /ledgers/{ledger_id}, `GET /ledgers/{id}/export?format=json\ | md\ | html` | Closure and ledgers | viewer»
- [ ] POST /closure/evaluate (scope), GET /ledgers/{ledger_id}, `GET /ledgers/{id}/export?format=json\
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']


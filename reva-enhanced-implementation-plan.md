# REVA — Enhanced Capabilities Implementation Plan
**Native Binary Decompilation, Mobile Package Triage, Firmware Carving, Controlled Dynamic Tracing, Runtime Observation, Cross-Version Binary Diffing, Repository URL Ingestion & Wisdom Graph Integration**

| Field | Value |
|---|---|
| Document | `reva-enhanced-implementation-plan.md` |
| Companion Specification | `reva-requirements.md` (normative requirements, identifier scheme, canonical data model) |
| System Target | EOIP / KnowGridFlow (KGF): Python/FastAPI backend, React frontend, multi-backend graph (Apache HugeGraph, Neo4j, Amazon Neptune), local-first, multi-tenant |
| Core Philosophy | Pure-Python First, Local-First, Zero Commercial License Lock-in, Cryptographic Warrant Provenance, Zero LLM Data Leaks |
| Status | Approved for implementation |

---

## 0. Foundational Operating Rule (Read Before Any Code is Written)

### 0.1 The Proof-of-Done Imperative
**A code file path, a function name, a test file reference, a commit message, a green test report count, or a coverage percentage is NEVER, on its own, proof that a requirement is implemented.**

In REVA, completion is strictly determined by the **Proof-of-Done Engine** (Module `PD`, §7.6, §14):
1. Every requirement MUST have a declared, reviewed **Obligation** (`OBL-REVA-...`) with mandatory case kinds (`positive`, `negative`, `boundary`, `malformed`, `concurrency`, `tamper`) and an explicit `required_depth` (`unit` < `component` < `integration` < `acceptance` < `deployed` < `production-observed`).
2. Verification commands MUST execute inside the REVA Sandboxed Runner from a pristine git checkout at a recorded commit hash, capturing full process lineage, environment fingerprints, and content-addressed outputs.
3. Tests MUST execute the owning code under **per-test coverage contexts** (`--cov-context=test`) and MUST kill injected AST mutants above the mandatory threshold ($\ge 0.75$).
4. Verification authority MUST be comparable to the requirement's claim (e.g. a unit test cannot close an end-to-end integration or acceptance journey claim).
5. For user-visible capabilities (`api`, `mcp`, `cli`, `ui`), runtime evidence (signed HTTP exchange traces, DOM snapshots, video recordings) MUST be captured against the running stack in acceptance journeys `RJ-13`, `RJ-14`, `RJ-15`.
6. Zero open contradictions and zero blocking knowledge gaps may be linked to the obligation.
7. An AI coding agent claiming completion MUST provide the unique Merkle-anchored **Ledger ID** and signed attestation hash. Any report stating "implemented and tested" without this cryptographic proof is unproven and invalid.

### 0.2 Pure-Python First & Zero-Data-Leak LLM Egress Policy
1. **Deterministic Python Dominance:** $\ge 95\%$ of all reverse-engineering, AST generation, binary loading, basic block decomposition, CFG building, opcode analysis, format parsing, and graph projection MUST be implemented in deterministic, memory-safe, pure Python.
2. **Minimal LLM Invocations:** LLMs are reserved strictly for high-level semantic summarization, natural language answering, and ambiguous architectural precedent queries.
3. **Zero Data Leakage:** Under `REVA-SEC-013`, all data destined for an LLM MUST pass through `reva/core/egress_gate.py`:
   - Proprietary source code is never transmitted raw; it is abstracted into pseudonymized AST token graphs (`[ENTITY_1]`, `[CALL_2]`).
   - Automated RFC 6901 pointer redaction scrubs all tokens, keys, passwords, database URLs, internal IPs, and PII.
   - Local offline LLMs (via Ollama or vLLM) are the mandatory default; external LLM egress is blocked unless explicitly authorized by signed tenant policy.
   - All untrusted repository content is strictly wrapped in prompt-injection defense delimiters (`_meta.provenance.untrusted_content`).

---

## 1. Plan Overview & Phase Architecture

```mermaid
graph TD
    P0[Phase P-ENH-0: Baseline & Egress Safety] --> P1[Phase P-ENH-1: Repo Ingestion & Wisdom Graph]
    P0 --> P2[Phase P-ENH-2: Native Binary Disassembly & CFG]
    P1 --> P3[Phase P-ENH-3: Mobile Package Triage & JNI]
    P2 --> P4[Phase P-ENH-4: Firmware & Bytecode Carving]
    P2 --> P5[Phase P-ENH-5: Safe Controlled Tracing]
    P1 --> P6[Phase P-ENH-6: Headless Browser CDP Observation]
    P2 --> P7[Phase P-ENH-7: Cross-Version Binary Diffing]
    P3 --> P8[Phase P-ENH-8: Surface Integration & Release Gate G3b]
    P4 --> P8
    P5 --> P8
    P6 --> P8
    P7 --> P8
```

| Phase | Focus Modules | Key Deliverables |
|---|---|---|
| **Phase P-ENH-0** | Baseline, Safety, Sandboxes | Egress Security Gate, Reverse Engineering Sandbox Profiles, Ports |
| **Phase P-ENH-1** | `REVA-AB-014/015`, Wisdom Graph | Git Remote Ingestion (GitHub/GitLab), ADR & Commit Precedent Miner |
| **Phase P-ENH-2** | `Module NB` (Native Binaries) | ELF/PE/Mach-O Loader, Capstone/Rizin Disassembler, CFG, Ghidra Batch Worker |
| **Phase P-ENH-3** | `Module MB` (Mobile Packages) | Pure-Python APK/DEX/AAB Parser, iOS IPA Parser, JNI `.so` Bridge Mapper |
| **Phase P-ENH-4** | `Module FM` (Firmware & Containers)| SquashFS/Ext4 Carver, Secret Harvester, WASM/EVM Bytecode Decoder |
| **Phase P-ENH-5** | `Module DI` (Controlled Tracing) | Dual-Key Authorization, Ephemeral GDB/LLDB Controller, Crash Triage |
| **Phase P-ENH-6** | `Module RO` (Runtime Observation) | Supervised Chromium CDP, Real-Time Redaction, DOM/Interaction Attestation |
| **Phase P-ENH-7** | `Module BD` (Binary Diffing) | Dual-Identity Matching, CFG Isomorphism (GED), Instruction Fuzzy Hash |
| **Phase P-ENH-8** | Integration, MCP/REST/CLI, Journeys | Unified Endpoints, Tools, CLI, Journeys RJ-13..RJ-15, Release Gate G3b |

---

## 2. Phase P-ENH-0 — Baseline Discovery, Configuration, Sandbox Profiles & Egress Safety

### T-ENH-001 Configuration Parameters & Feature Flags
- **Obligation:** `OBL-REVA-ENH-CONFIG` (layer: `core`, depth: `unit`)
- **Requirements Covered:** §11, `REVA-NB-*`, `REVA-MB-*`, `REVA-FM-*`, `REVA-DI-*`, `REVA-RO-*`, `REVA-BD-*`
- **Depends On:** `T-003` (`reva/config.py`)
- **Target Files:**
  - `reva/config.py` (extend `RevaSettings`)
  - `tests/reva/unit/config/test_enhanced_settings.py`
- **Implementation Instructions:**
  1. Add configuration parameters to `RevaSettings` with safe defaults:
     ```python
     # Native Binary Worker Settings
     reva_nb_disasm_timeout_s: int = Field(default=300, description="Max disassembly time per binary")
     reva_nb_ghidra_timeout_s: int = Field(default=600, description="Max Ghidra decompile time per binary")
     reva_nb_max_binary_bytes: int = Field(default=256 * 1024 * 1024, description="Max binary file size (256 MiB)")
     reva_nb_max_instructions: int = Field(default=500_000, description="Max instructions to disassemble per function")
     
     # Mobile Package Settings
     reva_mb_max_apk_bytes: int = Field(default=500 * 1024 * 1024, description="Max mobile package size (500 MiB)")
     reva_mb_decompression_ratio_limit: float = Field(default=200.0, description="Zip-bomb protection ratio")
     reva_mb_adb_loopback_only: bool = Field(default=True, description="Enforce loopback emulator ADB connection only")
     
     # Firmware Carving Settings
     reva_fm_max_carve_depth: int = Field(default=6, description="Max recursive filesystem carving depth")
     reva_fm_max_decompressed_bytes: int = Field(default=10 * 1024 * 1024 * 1024, description="Max disk budget (10 GiB)")
     
     # Controlled Dynamic Tracing Settings
     reva_di_dual_key_required: bool = Field(default=True, description="Require analyst + sec-admin signatures")
     reva_di_max_trace_instructions: int = Field(default=100_000, description="Max ring-buffer instruction trace size")
     reva_di_max_memory_read_bytes: int = Field(default=64 * 1024, description="Max memory dump slice (64 KiB)")
     
     # Headless Browser CDP Settings
     reva_ro_browser_headless: bool = Field(default=True, description="Strict headless mode")
     reva_ro_allowed_domains: list[str] = Field(default_factory=lambda: ["127.0.0.1", "localhost", "testapp.local"])
     
     # LLM Egress Gate Settings
     reva_egress_allow_external_llm: bool = Field(default=False, description="Strict local-only LLM default")
     reva_egress_redaction_strict: bool = Field(default=True, description="Drop raw source code from egress")
     ```
  2. Implement validation: ensure timeouts are $> 0$ and ratio limits $\ge 10.0$.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/config/test_enhanced_settings.py -v
  ```
- **Expected Output:**
  - All default fields initialized; environment override parsing verified; invalid configurations raise `ValidationError`.
- **Done When:** Settings load cleanly from environment variables and `.env` with strict type validation.

---

### T-ENH-002 Zero-Data-Leak LLM Egress Security Gate
- **Obligation:** `OBL-REVA-SEC-EGRESS-GATE` (layer: `security`, depth: `component`)
- **Requirements Covered:** `REVA-SEC-013`, `REVA-SEC-005`, `REVA-SEC-006`
- **Depends On:** `T-ENH-001`, `T-602` (`reva/core/redact.py`)
- **Target Files:**
  - `reva/core/egress_gate.py`
  - `reva/core/pseudonymizer.py`
  - `tests/reva/component/security/test_egress_gate.py`
- **Implementation Instructions:**
  1. Create `EgressSecurityGate` class:
     ```python
     class EgressSecurityGate:
         def __init__(self, settings: RevaSettings, redactor: RedactionEngine):
             self.settings = settings
             self.redactor = redactor
             self.pseudonymizer = CodePseudonymizer()

         def sanitize_prompt_payload(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
             """
             Applies RFC 6901 redaction, scrubs credentials, replaces raw proprietary code
             with abstract structural tokens, and wraps untrusted input in security fences.
             """
     ```
  2. Implement `CodePseudonymizer`: parses raw code with Python AST or generic regex; transforms variable names, internal function names, internal domains, and customer IDs into tokens like `[VAR_1]`, `[FUNC_1]`, `[DOMAIN_1]`. Stores a local ephemeral bidirectional mapping in memory only.
  3. Enforce the **Zero-Raw-Code Rule**: If payload contains file bodies $\ge 500$ bytes without AST tokenization, raise `RevaEgressViolationError("Raw code egress is strictly forbidden")`.
  4. Implement Prompt Fencing: Wrap all user or repository strings in:
     `<<<UNTRUSTED_CONTENT_START:SHA256_HASH>>>\n...\n<<<UNTRUSTED_CONTENT_END>>>`
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/security/test_egress_gate.py -v
  ```
- **Expected Output:**
  - All test payloads containing AWS keys, JWTs, proprietary code blocks, and passwords have zero leaks; `RevaEgressViolationError` raised on untokenized raw code attempts.
- **Done When:** Automated byte-scan confirms 0 bytes of sensitive data or raw code pass through the gate unredacted.

---

### T-ENH-003 Ephemeral Container Sandbox Profiles for Reverse Engineering
- **Obligation:** `OBL-REVA-SANDBOX-RE-PROFILES` (layer: `sandbox`, depth: `component`)
- **Requirements Covered:** `REVA-VS-003`, `REVA-VS-004`, `REVA-NB-002`, `REVA-DI-002`
- **Depends On:** `T-204` (`reva/sandbox/profiles.py`)
- **Target Files:**
  - `reva/sandbox/profiles.py` (add `RE_DISASM`, `RE_GHIDRA`, `RE_DYNAMIC_TRACING`, `RE_BROWSER_CDP`)
  - `tests/reva/component/sandbox/test_re_profiles.py`
- **Implementation Instructions:**
  1. Define sandbox security profiles:
     - `ProfileKind.RE_DISASM`: CPU limit 600s, RAM 4 GiB, `network: "none"`, read-only root, `/tmp` tmpfs 512 MiB, capabilities: `ALL` dropped.
     - `ProfileKind.RE_GHIDRA`: CPU limit 900s, RAM 8 GiB, `network: "none"`, read-only root, headless JVM options `-XX:+UseG1GC -Xmx6G`, capabilities: `ALL` dropped.
     - `ProfileKind.RE_DYNAMIC_TRACING`: CPU limit 300s, RAM 2 GiB, `network: "none"`, ephemeral PID namespace, `ptrace` allowed inside container only (`--cap-add=SYS_PTRACE`), `--security-opt=seccomp=unconfined` restricted strictly to isolated ephemeral container.
     - `ProfileKind.RE_BROWSER_CDP`: CPU limit 180s, RAM 2 GiB, network isolated to loopback interface only (`127.0.0.1`), chromium flags: `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage --headless=new`.
  2. Implement capability validation: If host cannot support containerization, fall back to process sandbox with `ENVIRONMENT_DEGRADED_SANDBOX` warrant limitation.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/sandbox/test_re_profiles.py -v
  ```
- **Done When:** Profile configurations emit compliant Docker/Podman run arguments and process limit constraints.

---

## 3. Phase P-ENH-1 — Remote Repository URL Ingestion & Wisdom Graph Extractor

### T-ENH-004 Git Repository Ingestion Engine
- **Obligation:** `OBL-REVA-REPO-INGEST-GIT` (layer: `extractor`, depth: `integration`)
- **Requirements Covered:** `REVA-AB-014`, `REVA-AI-001`
- **Depends On:** `T-ENH-001`, `T-ENH-003`
- **Target Files:**
  - `reva/extract/repo/git_cloner.py`
  - `reva/extract/repo/model.py`
  - `tests/reva/integration/extract/test_git_cloner.py`
- **Implementation Instructions:**
  1. Implement `GitRepositoryCloner`:
     ```python
     class GitRepositoryCloner:
         def __init__(self, sandbox: ProcessSandboxRunner, settings: RevaSettings):
             self.sandbox = sandbox
             self.settings = settings

         async def clone_or_fetch(
             self, 
             repo_url: str, 
             ref: str = "HEAD", 
             depth: int = 1,
             credentials: RepoCredentials | None = None
         ) -> ClonedRepoContext:
             """
             Safely clones a remote Git repo (GitHub, GitLab, Bitbucket, Git-over-HTTPS)
             into an isolated sandbox workspace. Validates URL against SSRF rules.
             """
     ```
  2. Implement URL Validation: Reject non-git schemes, `file://` URLs, local network IPs (`10.0.0.0/8`, `192.168.0.0/16`, `127.0.0.1`), AWS metadata endpoints (`169.254.169.254`).
  3. Execute `git clone --depth <depth> --single-branch --branch <ref> <url> <dest>` under process sandbox with timeout $\le 300\text{s}$ and quota $\le 5\text{ GiB}$.
  4. Compute tree root SHA-256 and commit hash; generate `reva_Artifact` warrant.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/test_git_cloner.py -v
  ```
- **Done When:** Clones a local bare git repo fixture, extracts commit hash and file tree, and rejects malicious SSRF repository URLs.

---

### T-ENH-005 Multi-Repo Workspace Orchestrator
- **Obligation:** `OBL-REVA-REPO-WORKSPACE` (layer: `extractor`, depth: `integration`)
- **Requirements Covered:** `REVA-AB-007`, `REVA-AB-014`
- **Depends On:** `T-ENH-004`, `T-501`
- **Target Files:**
  - `reva/extract/repo/workspace.py`
  - `tests/reva/integration/extract/test_workspace_orchestrator.py`
- **Implementation Instructions:**
  1. Implement `WorkspaceOrchestrator`: Coordinates multi-repo analysis (e.g. backend service repo + frontend web repo + native SDK repo).
  2. Discovers services across ingested repositories; builds unified service topology map (`svc:<org>/<repo>/<service>`).
  3. Triggers parallel extraction pipelines: Tree-sitter boundary parser (`T-503..T-505`), native binary scanner (`T-ENH-008`), and mobile package triage (`T-ENH-015`).
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/test_workspace_orchestrator.py -v
  ```
- **Done When:** Ingests two concurrent repo fixtures, identifies services, and triggers unified boundary extraction.

---

### T-ENH-006 Wisdom Graph Precedent & ADR Extractor
- **Obligation:** `OBL-REVA-WISDOM-ADR` (layer: `extractor`, depth: `component`)
- **Requirements Covered:** `REVA-AB-015`, `WG-DEC-*`, `WG-PREC-*`
- **Depends On:** `T-ENH-004`
- **Target Files:**
  - `reva/extract/wisdom/adr_extractor.py`
  - `reva/extract/wisdom/model.py`
  - `tests/reva/component/extract/test_adr_extractor.py`
- **Implementation Instructions:**
  1. Implement `AdrExtractor`: Scans workspace for Architecture Decision Records in standard paths (`docs/adr/*.md`, `doc/decisions/*.md`, `rfc/*.md`, `architecture/decisions/*.md`).
  2. Parse standard ADR sections: `Status`, `Context`, `Decision`, `Consequences`, `Alternatives Considered`.
  3. Extract referenced code symbols, service names, and architectural boundaries mentioned in the ADR text.
  4. Project `wg_Decision` and `wg_Precedent` vertices into the Wisdom Graph via `GraphPort`, connecting them to corresponding `reva_Service` vertices with `reva_JUSTIFIED_BY` edges.
  5. Issue signed warrant (`wr1_...`) with `Authority.SOURCE_SYSTEM_RECORD`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/test_adr_extractor.py -v
  ```
- **Done When:** Parses fixture ADR markdown files, extracts decisions and consequences, and connects them to graph nodes.

---

### T-ENH-007 Commit Semantics & PR Discussion Miner
- **Obligation:** `OBL-REVA-WISDOM-COMMITS` (layer: `extractor`, depth: `component`)
- **Requirements Covered:** `REVA-AB-015`, `WG-LESSON-*`
- **Depends On:** `T-ENH-004`, `T-ENH-006`
- **Target Files:**
  - `reva/extract/wisdom/commit_miner.py`
  - `tests/reva/component/extract/test_commit_miner.py`
- **Implementation Instructions:**
  1. Implement `CommitSemanticMiner`: Walks git log from cloned repo; analyzes commit message headers following Conventional Commits (`feat(auth):`, `fix(db):`, `refactor(core):`, `BREAKING CHANGE:`).
  2. Extracts ticket references (`Fixes #123`, `Jira: PROJ-456`), co-authors (`Co-authored-by:`), and sign-offs.
  3. Maps code diff file paths to modified boundaries; generates architectural evolution trails.
  4. If breaking changes or architectural trade-offs are identified, emit `wg_Lesson` vertices into the Wisdom Graph.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/test_commit_miner.py -v
  ```
- **Done When:** Parses fixture git history, categorizes conventional commits, and projects architectural evolution links.

---

## 4. Phase P-ENH-2 — Module NB — Native Binary Disassembly & Decompilation Core

### T-ENH-008 Multi-Format Binary Loader
- **Obligation:** `OBL-REVA-NB-LOADER` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-NB-001`, `REVA-NB-007`
- **Depends On:** `T-ENH-001`, `T-402`
- **Target Files:**
  - `reva/extract/native/loader.py`
  - `reva/extract/native/model.py`
  - `tests/reva/unit/extract/native/test_binary_loader.py`
- **Implementation Instructions:**
  1. Implement `BinaryLoader` using pure-Python libraries (`pyelftools` for ELF, `pefile` for PE/COFF, `macholib` for Mach-O):
     ```python
     class BinaryFormat(str, Enum):
         ELF = "elf"
         PE = "pe"
         MACHO = "macho"
         UNKNOWN = "unknown"

     class BinaryArchitecture(str, Enum):
         X86_64 = "x86_64"
         AARCH64 = "aarch64"
         ARMV7 = "armv7"
         RISCV64 = "riscv64"
         X86 = "x86"

     @dataclass(frozen=True)
     class BinaryMetadata:
         format: BinaryFormat
         architecture: BinaryArchitecture
         entry_point: int
         image_base: int
         is_pie: bool
         is_stripped: bool
         sections: list[SectionHeader]
         imported_libraries: list[str]
     ```
  2. Implement magic-byte format detection (`\x7fELF`, `MZ`, `\xfe\xed\xfa\xce`, `\xcf\xfa\xed\xfe`).
  3. Parse section headers: name, virtual address, virtual size, raw data offset, raw data size, flags (`READ`, `WRITE`, `EXECUTE`).
  4. Parse dynamic link dependencies: `DT_NEEDED` in ELF, Import Directory in PE, `LC_LOAD_DYLIB` in Mach-O.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/extract/native/test_binary_loader.py -v
  ```
- **Done When:** Correctly extracts metadata from ELF, PE, and Mach-O fixtures without crashing on malformed binaries.

---

### T-ENH-009 Headless Disassembly Engine with Capstone / Rizin
- **Obligation:** `OBL-REVA-NB-DISASM` (layer: `extractor`, depth: `integration`)
- **Requirements Covered:** `REVA-NB-002`
- **Depends On:** `T-ENH-008`, `T-ENH-003`
- **Target Files:**
  - `reva/extract/native/disasm.py`
  - `tests/reva/integration/extract/native/test_disasm_engine.py`
- **Implementation Instructions:**
  1. Implement `HeadlessDisassembler` with Capstone Python bindings inside the `RE_DISASM` sandbox runner:
     ```python
     @dataclass(frozen=True)
     class Instruction:
         address: int
         size: int
         mnemonic: str
         op_str: str
         bytes: bytes
         is_branch: bool
         is_call: bool
         is_return: bool
         jump_target: int | None
     ```
  2. Configure Capstone disassembler mode based on detected architecture (`CS_ARCH_X86`, `CS_ARCH_ARM64`, etc.).
  3. Disassemble executable segments; track linear and recursive descent paths.
  4. Handle disassembly timeouts: If instruction count exceeds `reva_nb_max_instructions` or execution exceeds timeout, halt gracefully, record partial coverage, and issue limitation `REVA_LIM_DISASM_TRUNCATED`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/native/test_disasm_engine.py -v
  ```
- **Done When:** Disassembles test functions accurately, matching expected objdump instruction sequences.

---

### T-ENH-010 Control Flow Graph (CFG) & Basic Block Analyzer
- **Obligation:** `OBL-REVA-NB-CFG` (layer: `extractor`, depth: `component`)
- **Requirements Covered:** `REVA-NB-004`
- **Depends On:** `T-ENH-009`
- **Target Files:**
  - `reva/extract/native/cfg.py`
  - `tests/reva/component/extract/native/test_cfg_analyzer.py`
- **Implementation Instructions:**
  1. Implement `ControlFlowGraphBuilder`:
     - Identifies basic block leaders: function entry points, branch targets, and instructions immediately following a branch/call.
     - Constructs `BasicBlock`: start address, end address, list of instructions, terminator instruction.
     - Adds directed edges: unconditional jump, conditional branch (true/false branches), fallthrough, call, return.
  2. Compute Cyclomatic Complexity:
     $$M = E - N + 2P$$
     where $E$ is number of CFG edges, $N$ is number of basic blocks, $P = 1$ for a single function.
  3. Detect loop headers and back-edges using Tarjan's strongly connected components algorithm.
  4. Export CFG to deterministic JSON and networkx / GraphPort graph formats.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/native/test_cfg_analyzer.py -v
  ```
- **Done When:** CFG builder accurately decomposes complex functions (loops, if/else, switch tables) and computes ground-truth cyclomatic complexity.

---

### T-ENH-011 Function Boundary & Symbol Resolution Engine
- **Obligation:** `OBL-REVA-NB-SYMBOLS` (layer: `extractor`, depth: `component`)
- **Requirements Covered:** `REVA-NB-005`, `REVA-NB-007`
- **Depends On:** `T-ENH-010`
- **Target Files:**
  - `reva/extract/native/symbols.py`
  - `tests/reva/component/extract/native/test_symbol_resolver.py`
- **Implementation Instructions:**
  1. Implement `SymbolResolver`:
     - In non-stripped binaries: extracts symbols from `.symtab`, `.dynsym`, export directories, and DWARF debug info.
     - In stripped binaries: uses recursive descent entry points, `.eh_frame` exception handler landing pads, prologue signatures (`push rbp; mov rbp, rsp` or `stp x29, x30, [sp, -... ]!`), and call-site targets.
  2. Compute stable function logical keys: `nb:<binary_sha256>:func:<start_offset>`.
  3. Map function calls to external symbols (PLT/GOT imports) such as `malloc`, `recv`, `SSL_read`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/native/test_symbol_resolver.py -v
  ```
- **Done When:** Detects 100% of internal function boundaries in non-stripped binaries and recovers $\ge 90\%$ in stripped test binary fixtures.

---

### T-ENH-012 String Literal & Cross-Reference Extractor
- **Obligation:** `OBL-REVA-NB-XREFS` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-NB-006`
- **Depends On:** `T-ENH-008`, `T-ENH-009`
- **Target Files:**
  - `reva/extract/native/xrefs.py`
  - `tests/reva/unit/extract/native/test_xrefs_extractor.py`
- **Implementation Instructions:**
  1. Implement `XRefExtractor`:
     - Scans read-only data sections (`.rodata`, `.rdata`, `.cstring`) for null-terminated strings (ASCII, UTF-8, UTF-16LE).
     - Identifies high-value patterns: URLs (`https?://.*`), IP addresses, SQL query fragments (`SELECT.*FROM`), format strings (`%s:%d`), file paths (`/etc/.*`).
     - Traces code cross-references: detects PC-relative addressing (`lea rdi, [rip + offset]`, `adrp + add` in ARM64) and absolute relocations that reference string addresses.
  2. Associates each string with referencing function IDs and basic block IDs.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/extract/native/test_xrefs_extractor.py -v
  ```
- **Done When:** Discovers embedded strings and traces references from call sites to string offsets.

---

### T-ENH-013 Headless Ghidra Decompiler Batch Bridge
- **Obligation:** `OBL-REVA-NB-GHIDRA` (layer: `extractor`, depth: `integration`)
- **Requirements Covered:** `REVA-NB-003`
- **Depends On:** `T-ENH-003`, `T-ENH-011`
- **Target Files:**
  - `reva/extract/native/ghidra_bridge.py`
  - `reva/extract/native/decomp/ghidra_headless_script.py`
  - `tests/reva/integration/extract/native/test_ghidra_bridge.py`
- **Implementation Instructions:**
  1. Implement `GhidraBatchDecompiler`:
     - Prepares headless Ghidra batch invocation command using `analyzeHeadless`.
     - Injects Python/Jython decompiler worker script (`ghidra_headless_script.py`).
     - Decompiles target functions into structured JSON AST: functions, parameters, return types, local variables, statement nodes, call sites.
  2. Runs exclusively inside `RE_GHIDRA` container profile under strict timeout and memory limits.
  3. If Ghidra is not installed or container fails, trigger automatic graceful fallback to Capstone disassembly CFG with limitation `REVA_LIM_DECOMPILER_FALLBACK`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/native/test_ghidra_bridge.py -v
  ```
- **Done When:** Emits structured C AST for test binary functions when Ghidra is present, and falls back cleanly when disabled.

---

### T-ENH-014 Native Binary Knowledge Graph Projection
- **Obligation:** `OBL-REVA-NB-PROJECTION` (layer: `graph`, depth: `integration`)
- **Requirements Covered:** `REVA-NB-008`, `REVA-WK-001`
- **Depends On:** `T-ENH-010`, `T-ENH-011`, `T-119`
- **Target Files:**
  - `reva/extract/native/projection.py`
  - `tests/reva/integration/extract/native/test_native_projection.py`
- **Implementation Instructions:**
  1. Implement `NativeGraphProjector`:
     - Writes `reva_BinaryFunction`, `reva_BasicBlock`, and `reva_NativeExport` vertices through `GraphPort`.
     - Writes `reva_CONTAINS_BLOCK`, `reva_BRANCHES_TO`, and `reva_CALLS_NATIVE` edges.
     - Emits signed Ed25519 warrants (`wr1_...`) for every binary function and export, binding them to the parent `reva_Artifact` digest.
  2. Idempotency test: Re-projecting the same binary must update timestamps without duplicating vertices or creating dangling edges.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/native/test_native_projection.py -v
  ```
- **Done When:** Graph queries return full binary callgraph and CFG topology across all supported backends.

---

## 5. Phase P-ENH-3 — Module MB — Mobile Application Package Triage

### T-ENH-015 Pure-Python APK & Binary AXML Manifest Parser
- **Obligation:** `OBL-REVA-MB-APK` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-MB-001`, `REVA-MB-003`
- **Depends On:** `T-ENH-001`
- **Target Files:**
  - `reva/extract/mobile/apk_parser.py`
  - `reva/extract/mobile/axml.py`
  - `reva/extract/mobile/model.py`
  - `tests/reva/unit/extract/mobile/test_apk_parser.py`
- **Implementation Instructions:**
  1. Implement streaming ZIP extraction with zip-bomb protection: track cumulative decompressed bytes; if ratio $> 200:1$ or total bytes $> 500\text{ MiB}$, abort immediately with `RevaZipBombError`.
  2. Implement pure-Python Android Binary XML (AXML) chunk decoder (`axml.py`):
     - Decodes String Pool Chunk, Resource ID Chunk, XML Start/End Namespace Chunks, XML Start/End Element Chunks.
     - Reconstructs standard UTF-8 XML document for `AndroidManifest.xml`.
  3. Extract core package metadata: `package`, `versionCode`, `versionName`, `minSdkVersion`, `targetSdkVersion`, `debuggable`.
  4. Extract all components: Activities, Services, Receivers, Providers, permissions, and Intent Filters (actions, categories, data schemes).
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/extract/mobile/test_apk_parser.py -v
  ```
- **Done When:** Decodes standard and obfuscated AXML manifests accurately and safely rejects synthetic zip bomb APKs.

---

### T-ENH-016 Dalvik DEX / Multi-DEX Bytecode Analyzer
- **Obligation:** `OBL-REVA-MB-DEX` (layer: `extractor`, depth: `component`)
- **Requirements Covered:** `REVA-MB-002`
- **Depends On:** `T-ENH-015`
- **Target Files:**
  - `reva/extract/mobile/dex_parser.py`
  - `tests/reva/component/extract/mobile/test_dex_parser.py`
- **Implementation Instructions:**
  1. Implement `DexParser` to parse `classes.dex`, `classes2.dex`, etc. without running Dalvik VM:
     - Parses DEX Header: magic (`dex\n035`), checksum, SHA-1 signature, string IDs, type IDs, proto IDs, field IDs, method IDs, class defs.
     - Indexes class hierarchies, implemented interfaces, method prototypes, and bytecode instructions.
  2. Identify `native` method declarations (methods with access flag `ACC_NATIVE = 0x0100`).
  3. Extract string pool literals: search for hardcoded backend API endpoints, auth endpoints, and crypto keys.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/mobile/test_dex_parser.py -v
  ```
- **Done When:** Ingests multi-DEX fixture APKs, identifies all classes and native methods, and extracts string literals.

---

### T-ENH-017 iOS IPA Bundle & Plist Analyzer
- **Obligation:** `OBL-REVA-MB-IPA` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-MB-004`
- **Depends On:** `T-ENH-008`
- **Target Files:**
  - `reva/extract/mobile/ipa_parser.py`
  - `tests/reva/unit/extract/mobile/test_ipa_parser.py`
- **Implementation Instructions:**
  1. Implement `IpaParser`: Unzips `.ipa` archive under `Payload/<AppName>.app/`.
  2. Parses `Info.plist` (both XML and binary plist formats via Python's `plistlib`):
     - `CFBundleIdentifier`, `CFBundleShortVersionString`, `CFBundleVersion`, `MinimumOSVersion`.
     - Custom URL schemes (`CFBundleURLTypes`).
  3. Parses `embedded.mobileprovision`: extracts entitlements (push notifications, app groups, keychain access groups, iCloud containers).
  4. Dispatches the main Mach-O executable to `BinaryLoader` (`T-ENH-008`) to inspect architecture slices (arm64, arm64e).
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/extract/mobile/test_ipa_parser.py -v
  ```
- **Done When:** Extracts iOS bundle details, entitlements, custom URL schemes, and Mach-O slices without macOS host dependency.

---

### T-ENH-018 JNI Bridge & Native Cross-Layer Call Mapper
- **Obligation:** `OBL-REVA-MB-JNI` (layer: `extractor`, depth: `integration`)
- **Requirements Covered:** `REVA-MB-005`
- **Depends On:** `T-ENH-016`, `T-ENH-011`
- **Target Files:**
  - `reva/extract/mobile/jni_bridge.py`
  - `tests/reva/integration/extract/mobile/test_jni_bridge.py`
- **Implementation Instructions:**
  1. Implement `JniBridgeMapper`:
     - Collects all `native` methods found by `DexParser` in format `package.Class.methodName`.
     - Generates canonical JNI symbol names according to JNI spec:
       `Java_package_Class_methodName` (handling escaped characters like `_` $\to$ `_1`).
     - Inspects embedded `.so` libraries in `lib/<abi>/` (e.g. `lib/arm64-v8a/libnative.so`) using `BinaryLoader` export tables.
  2. Matches JNI symbols to native function addresses and disassembles them via `T-ENH-009`.
  3. Emits `reva_CALLS_NATIVE` edges connecting Java boundary entities to `reva_BinaryFunction` entities with signed warrants.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/mobile/test_jni_bridge.py -v
  ```
- **Done When:** Links Java native method declaration in Dalvik DEX to disassembled C function in embedded `.so` library.

---

### T-ENH-019 Safe Read-Only ADB Triage Client
- **Obligation:** `OBL-REVA-MB-ADB` (layer: `extractor`, depth: `integration`)
- **Requirements Covered:** `REVA-MB-006`
- **Depends On:** `T-ENH-001`
- **Target Files:**
  - `reva/extract/mobile/adb_client.py`
  - `tests/reva/integration/extract/mobile/test_adb_client.py`
- **Implementation Instructions:**
  1. Implement `SafeAdbClient`: Connects to ADB server on local loopback interface (`127.0.0.1:5037`).
  2. Whitelist read-only commands: `host:devices`, `shell:pm list packages`, `shell:pm dump <package>`, `shell:dumpsys package <package>`.
  3. Rejection Guard: Any command matching `install`, `uninstall`, `rm`, `push`, `pull`, `chmod`, `setprop` MUST be rejected with `RevaSecurityViolationError`.
  4. Parse package dump into runtime mobile package state; reconcile with static APK warrant.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/mobile/test_adb_client.py -v
  ```
- **Done When:** Queries local mock ADB server for package status and strictly rejects any mutating ADB command.

---

## 6. Phase P-ENH-4 — Module FM — Firmware & Embedded Container Carver

### T-ENH-020 Signature-Based Partition Carver & Header Parser
- **Obligation:** `OBL-REVA-FM-CARVER` (layer: `extractor`, depth: `component`)
- **Requirements Covered:** `REVA-FM-001`, `REVA-FM-002`
- **Depends On:** `T-ENH-001`, `T-ENH-003`
- **Target Files:**
  - `reva/extract/firmware/carver.py`
  - `reva/extract/firmware/signatures.py`
  - `tests/reva/component/extract/firmware/test_firmware_carver.py`
- **Implementation Instructions:**
  1. Implement `FirmwareCarver`:
     - Scans binary streams for known filesystem magic signatures:
       * SquashFS (`hsqs`, `sqsh`)
       * CramFS (`0x28cd3d45`)
       * JFFS2 (`0x85 0x19`)
       * Ext2/3/4 (`0x53 0xef` at superblock offset 1080)
       * U-Boot Image header (`0x27 0x05 0x19 0x56`)
       * Device Tree Blob DTB (`0xd0 0x0d 0xfe 0xed`)
  2. Implement recursive extraction pipeline:
     - Enforces recursion depth $\le 6$, maximum compression ratio $\le 200:1$, and total size budget $\le 10\text{ GiB}$.
     - Runs extraction tools inside isolated container sandboxes.
  3. Yields carved filesystem trees as `reva_FirmwarePartition` entities.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/firmware/test_firmware_carver.py -v
  ```
- **Done When:** Successfully identifies and extracts SquashFS and U-Boot partitions from synthetic flash dump fixtures.

---

### T-ENH-021 Embedded Credential & Key Harvester
- **Obligation:** `OBL-REVA-FM-SECRETS` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-FM-003`
- **Depends On:** `T-ENH-020`, `T-602`
- **Target Files:**
  - `reva/extract/firmware/secrets.py`
  - `tests/reva/unit/extract/firmware/test_secrets_harvester.py`
- **Implementation Instructions:**
  1. Implement `SecretHarvester`:
     - Scans carved filesystem trees for cryptographic private keys (`-----BEGIN RSA PRIVATE KEY-----`, OpenSSH private keys).
     - Scans for X.509 certificates and CA bundles.
     - Scans configuration files (`/etc/shadow`, `/etc/passwd`, `/etc/network/interfaces`, `.env`, `wpa_supplicant.conf`) for default passwords and API tokens.
  2. Apply redaction: Redact actual secret strings; compute SHA-256 fingerprint commitment.
  3. Project `reva_Resource(secret)` with fingerprint warrants in the Knowledge Graph.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/extract/firmware/test_secrets_harvester.py -v
  ```
- **Done When:** Identifies private keys and hardcoded passwords in test firmware filesystems and redacts them in public warrants.

---

### T-ENH-022 Pure-Python WASM & EVM Bytecode Decoder
- **Obligation:** `OBL-REVA-FM-BYTECODE` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-FM-004`
- **Depends On:** `T-ENH-001`
- **Target Files:**
  - `reva/extract/firmware/bytecode.py`
  - `tests/reva/unit/extract/firmware/test_bytecode_decoder.py`
- **Implementation Instructions:**
  1. Implement `WasmDecoder`:
     - Parses WebAssembly binary format magic (`\x00asm`) and version.
     - Decodes sections: Type (0x01), Import (0x02), Function (0x03), Table (0x04), Memory (0x05), Global (0x06), Export (0x07), Code (0x0a), Custom (0x00).
     - Disassembles bytecode instructions into structured opcodes without running a WASM runtime.
  2. Implement `EvmBytecodeDecoder`:
     - Scans EVM runtime bytecode for function selector dispatchers (`PUSH4 <selector>`, `EQ`, `JUMPI`).
     - Reconstructs 4-byte method selectors and basic control flow blocks.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/extract/firmware/test_bytecode_decoder.py -v
  ```
- **Done When:** Emits function inventories and section tables for WASM and EVM fixtures.

---

### T-ENH-023 Firmware Merkle Tree & Warrant Bundle Generator
- **Obligation:** `OBL-REVA-FM-BUNDLES` (layer: `kernel`, depth: `integration`)
- **Requirements Covered:** `REVA-FM-005`, `REVA-WK-012`
- **Depends On:** `T-ENH-020`, `T-117`
- **Target Files:**
  - `reva/extract/firmware/bundles.py`
  - `tests/reva/integration/extract/firmware/test_firmware_bundles.py`
- **Implementation Instructions:**
  1. Implement `FirmwareBundleGenerator`:
     - Computes leaf hashes for every carved file, binary, and partition.
     - Builds RFC 6962 Merkle tree binding root firmware image digest to all carved children.
     - Emits signed warrant bundle with inclusion proofs proving full provenance.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/firmware/test_firmware_bundles.py -v
  ```
- **Done When:** Generates a valid warrant bundle with verified Merkle inclusion proofs for extracted partitions.

---

## 7. Phase P-ENH-5 — Module DI — Safe Dynamic Instrumentation & Controlled Tracing

### T-ENH-024 Dual-Key Cryptographic Authorization Protocol
- **Obligation:** `OBL-REVA-DI-AUTH` (layer: `security`, depth: `component`)
- **Requirements Covered:** `REVA-DI-001`, `REVA-SEC-007`
- **Depends On:** `T-107` (`reva/kernel/signing.py`), `T-ENH-001`
- **Target Files:**
  - `reva/sandbox/tracing/auth.py`
  - `tests/reva/component/sandbox/tracing/test_tracing_auth.py`
- **Implementation Instructions:**
  1. Implement `DualKeyAuthorizationToken`:
     ```python
     @dataclass(frozen=True)
     class DynamicExecutionWarrant:
         target_binary_sha256: str
         analyst_key_id: str
         analyst_signature: str
         sec_admin_key_id: str
         sec_admin_signature: str
         max_duration_s: int
         issued_at: str
         expires_at: str
     ```
  2. Verify that both signatures are valid Ed25519 signatures under the tenant's registered public keys.
  3. Enforce expiration window: Token must not be older than `REVA_DI_TOKEN_MAX_AGE_S` (default 300s).
  4. Reject any single-signature or unsigned tracing request with `RevaUnauthorizedExecutionError`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/sandbox/tracing/test_tracing_auth.py -v
  ```
- **Done When:** Validates dual signatures and rejects expired, forged, or single-signed authorization tokens.

---

### T-ENH-025 Ephemeral Containerized GDB/MI2 & LLDB Controller
- **Obligation:** `OBL-REVA-DI-CONTROLLER` (layer: `sandbox`, depth: `integration`)
- **Requirements Covered:** `REVA-DI-002`, `REVA-DI-003`
- **Depends On:** `T-ENH-024`, `T-ENH-003`
- **Target Files:**
  - `reva/sandbox/tracing/controller.py`
  - `tests/reva/integration/sandbox/tracing/test_debugger_controller.py`
- **Implementation Instructions:**
  1. Implement `DebuggerController` communicating via GDB/MI2 protocol:
     - Spawns GDB/MI2 inside `RE_DYNAMIC_TRACING` container sandbox.
     - Issues commands: `-file-exec-and-symbols`, `-break-insert`, `-exec-run`, `-exec-continue`, `-data-read-memory-bytes`, `-data-list-register-values`.
  2. Implement strict bounds:
     - Memory read size capped at $\le 64\text{ KiB}$ (`reva_di_max_memory_read_bytes`).
     - Session execution timeout strictly enforced.
  3. Ensure container termination and cleanup on normal exit, error, or cancellation.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/sandbox/tracing/test_debugger_controller.py -v
  ```
- **Done When:** Hits breakpoints, reads bounded memory slices, and terminates cleanly without host orphan processes.

---

### T-ENH-026 Execution Call-Path & Bounded Ring-Buffer Tracer
- **Obligation:** `OBL-REVA-DI-TRACER` (layer: `sandbox`, depth: `integration`)
- **Requirements Covered:** `REVA-DI-004`
- **Depends On:** `T-ENH-025`
- **Target Files:**
  - `reva/sandbox/tracing/tracer.py`
  - `tests/reva/integration/sandbox/tracing/test_execution_tracer.py`
- **Implementation Instructions:**
  1. Implement `ExecutionTracer`:
     - Instruments function calls and basic block entries.
     - Streams trace events into a bounded in-memory ring-buffer (capacity $100,000$ events).
     - If buffer capacity is exceeded, drop oldest non-branch events and record limitation `REVA_LIM_TRACE_TRUNCATED`.
  2. Project `reva_RuntimeTrace` vertex into knowledge graph, linking executed functions to observed runtime performance.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/sandbox/tracing/test_execution_tracer.py -v
  ```
- **Done When:** Records complete instruction execution path into bounded ring-buffer without memory exhaustion.

---

### T-ENH-027 Core Dump & Minidump Crash Analyzer
- **Obligation:** `OBL-REVA-DI-CRASH` (layer: `extractor`, depth: `unit`)
- **Requirements Covered:** `REVA-DI-005`
- **Depends On:** `T-ENH-008`
- **Target Files:**
  - `reva/sandbox/tracing/crash_triage.py`
  - `tests/reva/unit/sandbox/tracing/test_crash_triage.py`
- **Implementation Instructions:**
  1. Implement `CrashTriageAnalyzer`:
     - Parses ELF Core Dumps (`PT_NOTE` segments: `NT_PRSTATUS`, `NT_PRPSINFO`, `NT_SIGINFO`).
     - Parses Windows Minidumps (`MDMP` stream directories: `ThreadListStream`, `ExceptionStream`, `ModuleListStream`).
  2. Extracts faulting signal (e.g. `SIGSEGV`, `STATUS_ACCESS_VIOLATION`), faulting virtual address, register states, and thread stack backtrace.
  3. Resolves faulting address to `reva_BinaryFunction` offset; generates crash warrant.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/sandbox/tracing/test_crash_triage.py -v
  ```
- **Done When:** Parses Linux ELF core dump fixture, recovers crashed thread stack frames, and identifies faulting function.

---

## 8. Phase P-ENH-6 — Module RO — Runtime Observation & Headless Browser CDP

### T-ENH-028 Supervised Headless Chromium / Playwright Controller
- **Obligation:** `OBL-REVA-RO-CONTROLLER` (layer: `runtime`, depth: `integration`)
- **Requirements Covered:** `REVA-RO-001`
- **Depends On:** `T-ENH-003`
- **Target Files:**
  - `reva/extract/runtime/browser.py`
  - `tests/reva/integration/extract/runtime/test_browser_controller.py`
- **Implementation Instructions:**
  1. Implement `BrowserSupervisor` using Playwright or Chromium CDP:
     - Spawns headless browser inside isolated network namespace restricted to loopback (`127.0.0.1`) or explicit domain allowlist.
     - Controls navigation, viewport sizing, timeouts, and page lifecycle.
     - Guarantees automated browser context teardown on completion or error.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/extract/runtime/test_browser_controller.py -v
  ```
- **Done When:** Spawns headless browser, navigates to local test server, and exits cleanly without hanging processes.

---

### T-ENH-029 Real-Time RFC 6901 CDP Network Harvester
- **Obligation:** `OBL-REVA-RO-NETWORK` (layer: `runtime`, depth: `component`)
- **Requirements Covered:** `REVA-RO-002`, `REVA-SEC-005`
- **Depends On:** `T-ENH-028`, `T-602`
- **Target Files:**
  - `reva/extract/runtime/cdp_network.py`
  - `tests/reva/component/extract/runtime/test_cdp_network.py`
- **Implementation Instructions:**
  1. Implement `CdpNetworkHarvester`:
     - Subscribes to CDP `Network.requestWillBeSent`, `Network.responseReceived`, and `Network.loadingFinished`.
     - Reconstructs HTTP requests and responses into structured HAR.
     - Applies real-time RFC 6901 redaction to all cookies, `Authorization` headers, bearer tokens, and configured secrets.
  2. Forwards sanitized network exchanges directly to `reva/extract/apisurface/accumulate.py`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/extract/runtime/test_cdp_network.py -v
  ```
- **Done When:** Captures network traffic from test web app and asserts 100% of credentials and sensitive tokens are redacted.

---

### T-ENH-030 Deterministic DOM Snapshot & Journey Attestation Engine
- **Obligation:** `OBL-REVA-RO-DOM-ATTEST` (layer: `runtime`, depth: `acceptance`)
- **Requirements Covered:** `REVA-RO-003`, `REVA-RO-004`, `REVA-RO-005`
- **Depends On:** `T-ENH-029`, `T-207`
- **Target Files:**
  - `reva/extract/runtime/dom_attest.py`
  - `tests/reva/acceptance/runtime/test_dom_attestation.py`
- **Implementation Instructions:**
  1. Implement `DomAttestationEngine`:
     - Captures DOM tree snapshots and accessibility trees at milestone interaction steps.
     - Synthesizes deterministic, resilient CSS and XPath locators for clicked and submitted elements.
     - Links interactive UI elements to backend API boundaries (`reva_BrowserInteraction` -> `reva_Boundary`).
  2. Collects console errors (`Runtime.exceptionThrown`) and associates them with source maps.
  3. Records video and screenshot evidence; signs in-toto style attestation warrant proving journey completion.
- **Verification Command:**
  ```powershell
  pytest tests/reva/acceptance/runtime/test_dom_attestation.py -v
  ```
- **Done When:** Drives automated login journey against fixture SPA, produces signed attestation, and links UI buttons to API routes.

---

## 9. Phase P-ENH-7 — Module BD — Cross-Version Binary & Logic Diffing

### T-ENH-031 Dual-Identity Function Matching
- **Obligation:** `OBL-REVA-BD-MATCHER` (layer: `workflow`, depth: `unit`)
- **Requirements Covered:** `REVA-BD-001`
- **Depends On:** `T-ENH-011`
- **Target Files:**
  - `reva/workflows/bindiff/matcher.py`
  - `tests/reva/unit/workflows/bindiff/test_binary_matcher.py`
- **Implementation Instructions:**
  1. Implement `DualIdentityMatcher`:
     - Compares binary v1 and binary v2 without suffering from address relocation churn.
     - First pass: Matches by exported symbol name and logical key.
     - Second pass: Matches by normalized instruction content digest.
     - Third pass: Matches by callgraph neighborhood and basic block count.
  2. Categorizes functions into: `unchanged`, `modified`, `added`, `removed`, `renamed`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/workflows/bindiff/test_binary_matcher.py -v
  ```
- **Done When:** Accurately recognizes relocated and reordered functions as unchanged between recompiled versions.

---

### T-ENH-032 CFG Isomorphism & Graph Edit Distance (GED) Calculator
- **Obligation:** `OBL-REVA-BD-GED` (layer: `workflow`, depth: `component`)
- **Requirements Covered:** `REVA-BD-002`
- **Depends On:** `T-ENH-010`, `T-ENH-031`
- **Target Files:**
  - `reva/workflows/bindiff/ged.py`
  - `tests/reva/component/workflows/bindiff/test_cfg_ged.py`
- **Implementation Instructions:**
  1. Implement `CfgIsomorphismScorer`:
     - Computes Graph Edit Distance (GED) between two Control Flow Graphs:
       Cost of node insertion, deletion, and substitution (based on basic block opcode similarity);
       Cost of edge insertion, deletion, and condition changes.
     - Computes normalized similarity score:
       $$\text{Similarity}(G_1, G_2) = 1.0 - \frac{\text{GED}(G_1, G_2)}{|V_1| + |V_2| + |E_1| + |E_2|}$$
  2. Classifies matches: Identical ($\ge 0.98$), Minor Modification ($0.80 \le s < 0.98$), Substantial Rewrite ($s < 0.80$).
- **Verification Command:**
  ```powershell
  pytest tests/reva/component/workflows/bindiff/test_cfg_ged.py -v
  ```
- **Done When:** Scores CFG similarity accurately on modified control-flow fixtures (added branch, modified loop).

---

### T-ENH-033 Normalized Instruction Fuzzy Hashing
- **Obligation:** `OBL-REVA-BD-FUZZY` (layer: `workflow`, depth: `unit`)
- **Requirements Covered:** `REVA-BD-003`
- **Depends On:** `T-ENH-009`
- **Target Files:**
  - `reva/workflows/bindiff/fuzzy_hash.py`
  - `tests/reva/unit/workflows/bindiff/test_fuzzy_hash.py`
- **Implementation Instructions:**
  1. Implement `InstructionNormalizer`:
     - Normalizes disassembled instruction stream: abstracts specific register names (e.g. `eax`, `ebx` $\to$ `REG`), strips immediate memory offsets (`[rbp - 0x10]` $\to$ `[REG - IMM]`), abstracts jump target addresses.
  2. Computes TLSH / SSDEEP fuzzy hashes over the normalized mnemonic stream.
  3. Detects refactored logic across different compiler optimization levels (`-O2` vs `-O3`).
- **Verification Command:**
  ```powershell
  pytest tests/reva/unit/workflows/bindiff/test_fuzzy_hash.py -v
  ```
- **Done When:** Matches identical logic compiled at different optimization levels with high fuzzy similarity.

---

### T-ENH-034 Binary Change Impact Propagation Engine
- **Obligation:** `OBL-REVA-BD-IMPACT` (layer: `workflow`, depth: `integration`)
- **Requirements Covered:** `REVA-BD-004`, `REVA-BD-005`, `REVA-FT-001`
- **Depends On:** `T-ENH-031`, `T-701` (`reva/workflows/trace.py`)
- **Target Files:**
  - `reva/workflows/bindiff/impact.py`
  - `tests/reva/integration/workflows/bindiff/test_binary_impact.py`
- **Implementation Instructions:**
  1. Implement `BinaryImpactPropagator`:
     - Takes list of modified binary functions from `matcher.py`.
     - Traverses knowledge graph upwards along `reva_CALLS_NATIVE` and `reva_CALLS` edges.
     - Identifies all impacted high-level HTTP routes, background jobs, database resources, and Jira user stories.
  2. Emits signed binary diff warrant citing base binary digest, target binary digest, and list of affected graph entities.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/workflows/bindiff/test_binary_impact.py -v
  ```
- **Done When:** Traversal from changed native function in `.so` identifies impacted API endpoint and Jira story.

---

## 10. Phase P-ENH-8 — Surface Integration, REST, MCP, CLI & Release Gate G3b

### T-ENH-035 Reverse Engineering REST API Endpoints
- **Obligation:** `OBL-REVA-IF-REST-RE` (layer: `api`, depth: `integration`)
- **Requirements Covered:** `REVA-IF-046`..`REVA-IF-049`, `REVA-IF-053`, `REVA-IF-054`
- **Depends On:** `T-301`, `T-ENH-008..034`
- **Target Files:**
  - `reva/api/routers/reverse_eng.py`
  - `tests/reva/integration/api/test_reverse_eng_api.py`
- **Implementation Instructions:**
  1. Implement FastAPI routes under `/api/reva/v1`:
     - `POST /binaries/analyze` -> triggers binary analysis job
     - `GET /binaries/{digest}/functions` -> lists functions
     - `GET /binaries/{digest}/functions/{offset}/cfg` -> returns CFG JSON
     - `GET /binaries/{digest}/functions/{offset}/decompiled` -> returns C AST
     - `POST /mobile/analyze` -> triggers APK/IPA triage
     - `POST /firmware/carve` -> triggers firmware carver
     - `POST /tracing/sessions` -> starts dual-key authorized trace session
     - `POST /browser/observe` -> executes supervised headless browser scenario
     - `POST /diff/binaries` -> executes binary diff between two digests
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/api/test_reverse_eng_api.py -v
  ```
- **Done When:** All REST endpoints return valid JSON responses with appropriate HTTP status codes and error handling.

---

### T-ENH-036 Reverse Engineering MCP Tools
- **Obligation:** `OBL-REVA-IF-MCP-RE` (layer: `mcp`, depth: `integration`)
- **Requirements Covered:** §9.2 (`reva_analyze_binary`, `reva_decompile_function`, `reva_get_binary_cfg`, `reva_triage_mobile_package`, `reva_carve_firmware`, `reva_trace_execution`, `reva_analyze_crash_dump`, `reva_observe_runtime`, `reva_diff_binaries`)
- **Depends On:** `T-307`, `T-ENH-035`
- **Target Files:**
  - `reva/mcp/tools/reverse_eng.py`
  - `tests/reva/integration/mcp/test_reverse_eng_mcp.py`
- **Implementation Instructions:**
  1. Register reverse engineering MCP tools conforming to §9.2 schema.
  2. Implement response budgeting: large CFG graphs or decompiled ASTs exceeding 10 MiB budget are stored as retained views and return summary with continuation token.
  3. Mark untrusted binary strings with `_meta.provenance.untrusted_content`.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/mcp/test_reverse_eng_mcp.py -v
  ```
- **Done When:** MCP client can invoke tools, receive structured results, and handle budget continuations.

---

### T-ENH-037 Reverse Engineering CLI Commands
- **Obligation:** `OBL-REVA-IF-CLI-RE` (layer: `cli`, depth: `integration`)
- **Requirements Covered:** §9.3 (`kgf reva binary`, `kgf reva mobile`, `kgf reva firmware`, `kgf reva trace`, `kgf reva browser`, `kgf reva bindiff`)
- **Depends On:** `T-308`, `T-ENH-035`
- **Target Files:**
  - `reva/cli/commands/reverse_eng.py`
  - `tests/reva/integration/cli/test_reverse_eng_cli.py`
- **Implementation Instructions:**
  1. Implement CLI subcommands under `kgf reva`:
     - `kgf reva binary analyze <file>`
     - `kgf reva binary cfg <file> <func_offset>`
     - `kgf reva mobile triage <package>`
     - `kgf reva firmware carve <image>`
     - `kgf reva trace execute <binary> --token <token>`
     - `kgf reva browser observe <url>`
     - `kgf reva bindiff compare <bin1> <bin2>`
  2. Support `--json`, `--tenant`, and `--quiet` flags.
- **Verification Command:**
  ```powershell
  pytest tests/reva/integration/cli/test_reverse_eng_cli.py -v
  ```
- **Done When:** CLI subcommands execute and print formatted terminal outputs or clean JSON streams.

---

### T-ENH-038 Acceptance Journeys RJ-13, RJ-14, RJ-15 Execution & Release Gate G3b
- **Obligation:** `OBL-REVA-GATE-G3B` (layer: `acceptance`, depth: `acceptance`)
- **Requirements Covered:** `RJ-13`, `RJ-14`, `RJ-15`, §14.3
- **Depends On:** `T-ENH-001` through `T-ENH-037`
- **Target Files:**
  - `tests/reva/acceptance/journeys/test_rj13_native_binary.py`
  - `tests/reva/acceptance/journeys/test_rj14_mobile_triage.py`
  - `tests/reva/acceptance/journeys/test_rj15_tracing_and_diff.py`
  - `scripts/reva/build_reva_ledger.py`
- **Implementation Instructions:**
  1. Execute `RJ-13`: Upload stripped Linux ELF and Windows PE executables; analyze CFGs and decompile functions; verify graph projection and Merkle tree inclusion proofs.
  2. Execute `RJ-14`: Ingest mobile APK and iOS IPA fixtures; verify component topology and the cross-layer `reva_CALLS_NATIVE` edge linking Java Activity to native `.so` C function.
  3. Execute `RJ-15`: Issue dual-key authorized dynamic tracing session; record bounded instruction ring-buffer; run supervised headless browser with RFC 6901 redaction; execute cross-version binary diff matching reordered functions without false churn.
  4. Run `python scripts/reva/build_reva_ledger.py` to evaluate Stage G3b closure in the REVA Proof-of-Done ledger.
- **Verification Commands:**
  ```powershell
  pytest tests/reva/acceptance/journeys/test_rj13_native_binary.py -v
  pytest tests/reva/acceptance/journeys/test_rj14_mobile_triage.py -v
  pytest tests/reva/acceptance/journeys/test_rj15_tracing_and_diff.py -v
  python scripts/reva/build_reva_ledger.py --stage G3b
  ```
- **Done When:** All 3 acceptance journeys pass against the running Compose stack, and Stage G3b is certified `CLOSED` in the signed REVA ledger.

---

## 11. 7-Level Verification Hierarchy & Proof-of-Done Protocol

To enforce the foundational rule that **code and test-file references alone are NOT considered proof of completion**, any AI coding agent working on REVA must satisfy all 7 levels of verification for every obligation before claiming done:

```
+-------------------------------------------------------------------------+
| Level 7: Merkle Transparency Log Anchoring & Signed Ledger Attestation  |
+-------------------------------------------------------------------------+
| Level 6: Mutation Testing & Fault Injection (Probe Score >= 0.75)        |
+-------------------------------------------------------------------------+
| Level 5: Acceptance Journey Execution against Live Compose Stack        |
+-------------------------------------------------------------------------+
| Level 4: Multi-Backend Graph Conformance (HugeGraph, Neo4j, Neptune)   |
+-------------------------------------------------------------------------+
| Level 3: Per-Test Coverage Context Mapping (--cov-context=test)         |
+-------------------------------------------------------------------------+
| Level 2: Sandboxed Process Execution with Recorded Process Lineage      |
+-------------------------------------------------------------------------+
| Level 1: Static Type Checking, AST Anti-Gaming & Guardrail Scans        |
+-------------------------------------------------------------------------+
```

1. **Level 1 (Static Analysis & Type Checking):**
   - AST scanner `scripts/reva/forbid_placeholders.py` must find 0 violations (no `pass`-only, `...`, `TODO`, `FIXME`).
   - Depth marker checker `scripts/reva/check_depth_markers.py` must pass 100%.
   - Strict `mypy` and `ruff` checks must pass with zero errors.
2. **Level 2 (Sandboxed Process Lineage):**
   - Tests must run inside the REVA sandboxed runner (`reva/sandbox/runner.py`) from a clean git checkout at a recorded commit.
   - PIDs, process groups, and resource usage must be logged in the execution manifest.
3. **Level 3 (Per-Test Coverage Contexts):**
   - Code coverage must be recorded using `--cov-context=test`.
   - The test asserting an obligation MUST execute the owning source lines directly; incidental coverage does not count.
4. **Level 4 (Multi-Backend Conformance):**
   - Graph projection must be verified against Apache HugeGraph, Neo4j, and TinkerPop Gremlin conformant backends.
5. **Level 5 (Acceptance Journey Execution):**
   - For all user-facing layers, full acceptance journeys (`RJ-01`..`RJ-15`) must run with captured runtime evidence (HTTP exchanges, screenshots, video).
6. **Level 6 (Mutation Testing & Anti-Gaming):**
   - AST mutants generated by REVA's mutation probe must be killed with a score $\ge 0.75$.
   - Anti-gaming checks (AG-01..AG-14) must pass (rejecting tautological assertions, mock shortcuts, and empty test bodies).
7. **Level 7 (Transparency Log Anchoring):**
   - Closing attestations must be signed with the tenant Ed25519 key, inserted into the tenant Merkle transparency log, and validated via `kgf reva log verify`.
   - The resulting signed Ledger ID must be exported in JSON, Markdown, and HTML formats.

---

## 12. Final Completion Checklist for AI Coding Agents

Before declaring completion of any task or phase, verify:
- [ ] No placeholder tokens (`TODO`, `FIXME`, `XXX`, `HACK`, `pass`, `...`) exist in any file.
- [ ] `reva_obligation`, `reva_case`, and `reva_depth` pytest markers are present on every test.
- [ ] Pure-Python implementation handles $\ge 95\%$ of parsing and processing logic.
- [ ] Zero secrets, PII, or raw source code files leak through the LLM Egress Security Gate.
- [ ] All binary, mobile, and firmware extractions enforce strict decompression quotas and memory limits.
- [ ] Ephemeral container sandboxes enforce `network: "none"` and drop-all Linux capabilities.
- [ ] Every graph vertex and edge carries signed warrants and bitemporal timestamps.
- [ ] Proof-of-Done ledger reflects `closed` status for the corresponding obligation ID.

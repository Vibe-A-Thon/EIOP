# EPIC-REVA-UNTR-05: reva-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 36 tasks, ~216.0 h, priorities {'P2': 36}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-REVA-RR-002 [P2] REVA-RR-002: Categories: matched, static_only_unobserved (never "dead" unless REVA-RR-003 holds), runtime_only (creates gap GAP_RUNTIME_WITHOUT_SOURCE), ambiguous (gap with candidates). · Each category is present 

- **Source:** `reva-requirements.md:925-925` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RR-002 | Categories: `matched`, `static_only_unobserved` (never "dead" unless REVA-RR-003 holds), `runtime_only` (creates gap `GAP_RUNTIME_WITHOUT_SOURCE`), `ambiguous` (gap with candidates). | Each category is present in the fixture output. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-RR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-RR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Each category is present in the fixture output
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RR-003 [P2] REVA-RR-003: "Unused" claims: a static boundary may be labelled unobserved_with_complete_coverage only when runtime coverage for that service is complete for a window ≥ REVA_RR_MIN_WINDOW_DAYS (default 30) and uns

- **Source:** `reva-requirements.md:926-926` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RR-003 | "Unused" claims: a static boundary may be labelled `unobserved_with_complete_coverage` only when runtime coverage for that service is `complete` for a window ≥ `REVA_RR_MIN_WINDOW_DAYS` (default 30) and unsampled. Otherwise it stays `static_only_unobserved`. | Partial-coverage fixture never yields the stronger label. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-RR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-RR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Partial-coverage fixture never yields the stronger label
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-RR-004 [P2] REVA-RR-004: Results project reva_OBSERVED_AS edges and update static elements with observed_count, last_observed_at. · Projection verified on each backend. · integration

- **Source:** `reva-requirements.md:927-927` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-RR-004 | Results project `reva_OBSERVED_AS` edges and update static elements with `observed_count`, `last_observed_at`. | Projection verified on each backend. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-RR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-RR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Projection verified on each backend
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-002 [P2] REVA-SP-002: Rust cargo-auditable: read the .dep-v0 section (ELF, PE, Mach-O __DATA), zlib-decompress with a 64 MiB output cap, parse packages (name, version, source, kind, dependency indices, root flag) and build

- **Source:** `reva-requirements.md:857-857` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-002 | **Rust cargo-auditable**: read the `.dep-v0` section (ELF, PE, Mach-O `__DATA`), zlib-decompress with a 64 MiB output cap, parse packages (name, version, source, kind, dependency indices, root flag) and build the dependency DAG; detect invalid indices as a malformed-input error. | Fixture built with `cargo auditable build` parses; a stripped binary yields `unavailable`. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture built with cargo auditable build parses; a stripped binary yields unavailable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-004 [P2] REVA-SP-004: JVM archives (JAR/WAR/EAR, Spring Boot fat JARs): parse META-INF/MANIFEST.MF (Implementation-, Build-Jdk-Spec, Created-By, Main-Class, Start-Class, Spring-Boot-Version), every META-INF/maven//pom.prop

- **Source:** `reva-requirements.md:859-859` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-004 | **JVM archives** (JAR/WAR/EAR, Spring Boot fat JARs): parse `META-INF/MANIFEST.MF` (Implementation-*, Build-Jdk-Spec, Created-By, Main-Class, Start-Class, Spring-Boot-Version), every `META-INF/maven/**/pom.properties` (+ `pom.xml` coordinates), `BOOT-INF/lib/*.jar` and `WEB-INF/lib/*.jar` recursively, `git.properties` (`git.commit.id`, `git.commit.id.abbrev`, `git.branch`, `git.commit.time`, `git.dirty`, `git.build.version`), and `META-INF/build-info.properties`; class-file major version → Java release; package inventory. | Fixture Spring Boot JAR (built in CI from a minimal project with git-commit-id plugin) yields components, the commit and the Java release; a JAR without metadata yields components from embedded pom.properties only, with limitations. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture Spring Boot JAR (built in CI from a minimal project with git-commit-id plugin) yields components, the commit and the Java release; a JAR without metadata yields components from embedded pom.properties only, with limitations
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-007 [P2] REVA-SP-007: OCI images: image config (created, architecture, os, labels incl. org.opencontainers.image.revision, .source, .version, .created), history, layer digests verification, per-layer inventory, then recurs

- **Source:** `reva-requirements.md:862-862` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-007 | **OCI images**: image config (`created`, `architecture`, `os`, labels incl. `org.opencontainers.image.revision`, `.source`, `.version`, `.created`), history, layer digests verification, per-layer inventory, then recursive detection of the ecosystems above inside layers (respecting whiteout files for the final filesystem view). | Fixture image (built in CI with `docker buildx --output type=oci`) yields the revision label, OS packages are listed as `unavailable` unless a dpkg/apk/rpm database is present, and its embedded JAR/venv is detected. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Fixture image (built in CI with docker buildx --output type=oci) yields the revision label, OS packages are listed as unavailable unless a dpkg/apk/rpm database is present, and its embedded JAR/venv is detected
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-008 [P2] REVA-SP-008: OS packages inside images: parse /var/lib/dpkg/status, /lib/apk/db/installed and (if present) the RPM sqlite DB (/var/lib/rpm/rpmdb.sqlite) read-only for name/version/arch. · Debian- and Alpine-based 

- **Source:** `reva-requirements.md:863-863` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-008 | OS packages inside images: parse `/var/lib/dpkg/status`, `/lib/apk/db/installed` and (if present) the RPM sqlite DB (`/var/lib/rpm/rpmdb.sqlite`) read-only for name/version/arch. | Debian- and Alpine-based fixture images list packages. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Debian- and Alpine-based fixture images list packages
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-009 [P2] REVA-SP-009: SBOM export: CycloneDX 1.5 JSON and SPDX 2.3 JSON for any artifact or image, with component PURLs, hashes, dependency relationships and REVA warrant IDs as external references. Outputs validate agains

- **Source:** `reva-requirements.md:864-864` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-009 | SBOM export: CycloneDX 1.5 JSON and SPDX 2.3 JSON for any artifact or image, with component PURLs, hashes, dependency relationships and REVA warrant IDs as external references. Outputs validate against the official JSON Schemas (vendored in the repo under `tests/reva/fixtures/schemas/`). | Schema validation passes for all fixtures. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Schema validation passes for all fixtures
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-010 [P2] REVA-SP-010: Commit linking: when a revision is found (vcs.revision, git.commit.id, PEP 610 commit, gitHead, OCI revision label, .NET +sha), issue reva.pred.built_from_commit and, if KGF's git graph contains that 

- **Source:** `reva-requirements.md:865-865` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-010 | Commit linking: when a revision is found (`vcs.revision`, `git.commit.id`, PEP 610 commit, `gitHead`, OCI revision label, .NET `+sha`), issue `reva.pred.built_from_commit` and, if KGF's git graph contains that commit, project `reva_BUILT_FROM` to it. Otherwise create a gap from template `GAP_COMMIT_NOT_INGESTED` with probe "sync repo X". Abbreviated SHAs match only if unique in the tenant's repos; otherwise the link is ambiguous (candidates listed, no edge). | Three-fixture test: full SHA linked, unique short SHA linked with `derived`, ambiguous short SHA produces a gap with candidates. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Three-fixture test: full SHA linked, unique short SHA linked with derived, ambiguous short SHA produces a gap with candidates
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-011 [P2] REVA-SP-011: Dirty-build flag: vcs.modified=true, git.dirty=true or equivalent creates a reva.pred.dirty_build warrant and marks the build vertex; drift verification (DV) treats dirty builds as unverifiable_dirty.

- **Source:** `reva-requirements.md:866-866` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-011 | Dirty-build flag: `vcs.modified=true`, `git.dirty=true` or equivalent creates a `reva.pred.dirty_build` warrant and marks the build vertex; drift verification (DV) treats dirty builds as `unverifiable_dirty`. | Dirty fixture is flagged in graph and UI. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Dirty fixture is flagged in graph and UI
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-SP-012 [P2] REVA-SP-012: Optional vulnerability matching (off by default, REVA_VULN_MATCH=false): match PURLs against a locally mirrored OSV dataset directory (tenant-supplied, no network calls); results are external_service 

- **Source:** `reva-requirements.md:867-867` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-SP-012 | Optional vulnerability matching (off by default, `REVA_VULN_MATCH=false`): match PURLs against a locally mirrored OSV dataset directory (tenant-supplied, no network calls); results are `external_service` warrants with the mirror snapshot date in limitations. | With a fixture mirror, a known vulnerable version is matched; with matching disabled no lookup happens. | integration
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-SP-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-SP-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] With a fixture mirror, a known vulnerable version is matched; with matching disabled no lookup happens
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-002 [P2] REVA-TST-002: Unit tests may not touch the filesystem (beyond tmppath for pure parsers), network, subprocesses or databases; integration tests cross exactly the boundary they name; acceptance tests run against the 

- **Source:** `reva-requirements.md:1395-1395` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-002 | Unit tests may not touch the filesystem (beyond `tmp_path` for pure parsers), network, subprocesses or databases; integration tests cross exactly the boundary they name; acceptance tests run against the Compose stack via REST/MCP/CLI/UI only.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-002 | Unit tests may not touch the filesystem (beyond tmp_path for pure parsers), network, subprocesses or databases; integration tests cross exactly the boundary they name; acceptance tests run against the Compose stack via REST/MCP/CLI/UI only.»
- [ ] Unit tests may not touch the filesystem (beyond tmp_path for pure parsers), network, subprocesses or databases; integration tests cross exactly the boundary they name; acceptance tests run against the Compose stack via REST/MCP/CLI/UI only.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-004 [P2] REVA-TST-004: Golden files (expected warrant IDs, route sets, SBOMs, diffs, traces) are committed and regenerated only by kgf reva fixtures regen, which prints a diff that requires review

- **Source:** `reva-requirements.md:1397-1397` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-004 | Golden files (expected warrant IDs, route sets, SBOMs, diffs, traces) are committed and regenerated only by `kgf reva fixtures regen`, which prints a diff that requires review.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-004 | Golden files (expected warrant IDs, route sets, SBOMs, diffs, traces) are committed and regenerated only by kgf reva fixtures regen, which prints a diff that requires review.»
- [ ] Golden files (expected warrant IDs, route sets, SBOMs, diffs, traces) are committed and regenerated only by kgf reva fixtures regen, which prints a diff that requires review.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-005 [P2] REVA-TST-005: Property-based tests (Hypothesis) for JCS, IDs, coverage composition, Merkle proofs, templating, incremental extraction equivalence and closure monotonicity (adding a failing check can never turn a no

- **Source:** `reva-requirements.md:1398-1398` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-005 | Property-based tests (Hypothesis) for JCS, IDs, coverage composition, Merkle proofs, templating, incremental extraction equivalence and closure monotonicity (adding a failing check can never turn a non-closed outcome into closed).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-005 | Property-based tests (Hypothesis) for JCS, IDs, coverage composition, Merkle proofs, templating, incremental extraction equivalence and closure monotonicity (adding a failing check can never turn a non-closed outcome into closed).»
- [ ] Property-based tests (Hypothesis) for JCS, IDs, coverage composition, Merkle proofs, templating, incremental extraction equivalence and closure monotonicity (adding a failing check can never turn a non-closed outcome into closed).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-007 [P2] REVA-TST-007: Every requirement in this document has ≥ 1 obligation in docs/reva/obligations/reva.yaml with marker-tagged tests, per §14. CI computes the REVA ledger on every main-branch build

- **Source:** `reva-requirements.md:1400-1400` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-007 | Every requirement in this document has ≥ 1 obligation in `docs/reva/obligations/reva.yaml` with marker-tagged tests, per §14. CI computes the REVA ledger on every main-branch build.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-007 | Every requirement in this document has ≥ 1 obligation in docs/reva/obligations/reva.yaml with marker-tagged tests, per §14. CI computes the REVA ledger on every main-branch build.»
- [ ] Every requirement in this document has ≥ 1 obligation in docs/reva/obligations/reva.yaml with marker-tagged tests, per §14. CI computes the REVA ledger on every main-branch build.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-008 [P2] REVA-TST-008: Negative-path coverage: each requirement's obligation lists negative and malformed case kinds unless it is pure presentation

- **Source:** `reva-requirements.md:1401-1401` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-008 | Negative-path coverage: each requirement's obligation lists `negative` and `malformed` case kinds unless it is pure presentation.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-008' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-008') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-008 | Negative-path coverage: each requirement's obligation lists negative and malformed case kinds unless it is pure presentation.»
- [ ] Negative-path coverage: each requirement's obligation lists negative and malformed case kinds unless it is pure presentation.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-TST-009 [P2] REVA-TST-009: Unavailable environments (no Docker, no Oracle) are named skips with reasons; skipped tests never count as passes (AG-01)

- **Source:** `reva-requirements.md:1402-1402` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-TST-009 | Unavailable environments (no Docker, no Oracle) are named skips with reasons; skipped tests never count as passes (AG-01).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-TST-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-TST-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-TST-009 | Unavailable environments (no Docker, no Oracle) are named skips with reasons; skipped tests never count as passes (AG-01).»
- [ ] Unavailable environments (no Docker, no Oracle) are named skips with reasons; skipped tests never count as passes (AG-01).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-003 [P2] REVA-UI-003: Transparency Log: STH timeline, tree size, auditor status, proof verifier tool (paste a warrant ID → inclusion proof result). · Proof verification on a fixture warrant. · acceptance

- **Source:** `reva-requirements.md:1043-1043` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-003 | **Transparency Log**: STH timeline, tree size, auditor status, proof verifier tool (paste a warrant ID → inclusion proof result). | Proof verification on a fixture warrant. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-003 | Transparency Log: STH timeline, tree size, auditor status, proof verifier tool (paste a warrant ID → inclusion proof result). | Proof verification on a fixture warrant. | acceptance»
- [ ] Transparency Log: STH timeline, tree size, auditor status, proof verifier tool (paste a warrant ID → inclusion proof result).
- [ ] Proof verification on a fixture warrant.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-004 [P2] REVA-UI-004: Proof-of-Done Board: obligations matrix (rows = obligations, columns = case kinds × status), filters (requirement, layer, owner, status), per-obligation detail with the ordered closure checks and reas

- **Source:** `reva-requirements.md:1044-1044` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-004 | **Proof-of-Done Board**: obligations matrix (rows = obligations, columns = case kinds × status), filters (requirement, layer, owner, status), per-obligation detail with the ordered closure checks and reason codes, linked verifier runs, attestations, coverage hits and mutation scores; "Asserted done — unproven" lane for board items without closure; export buttons (JSON/MD/HTML). | RJ-06. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-004 | Proof-of-Done Board: obligations matrix (rows = obligations, columns = case kinds × status), filters (requirement, layer, owner, status), per-obligation detail with the ordered closure checks and reason codes, linked verifier runs, attestations, coverage hits and mutation scores; "Asserted done — unproven" lane for board items without closure; export buttons (JSON»
- [ ] Proof-of-Done Board: obligations matrix (rows = obligations, columns = case kinds × status), filters (requirement, layer, owner, status), per-obligation detail with the ordered closure checks and reason codes, linked verifier runs, attestations, coverage hits and mutation scores; "Asserted done — unproven" lane for board items without closure; export buttons (JSON/MD/HTML).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-005 [P2] REVA-UI-005: Verifier Run Detail: lineage tree, environment fingerprint, test outcomes, rerun matrix, per-owner coverage, mutation results, artifacts (download), attestation verification. · RJ-06. · acceptance

- **Source:** `reva-requirements.md:1045-1045` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-005 | **Verifier Run Detail**: lineage tree, environment fingerprint, test outcomes, rerun matrix, per-owner coverage, mutation results, artifacts (download), attestation verification. | RJ-06. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-005 | Verifier Run Detail: lineage tree, environment fingerprint, test outcomes, rerun matrix, per-owner coverage, mutation results, artifacts (download), attestation verification. | RJ-06. | acceptance»
- [ ] Verifier Run Detail: lineage tree, environment fingerprint, test outcomes, rerun matrix, per-owner coverage, mutation results, artifacts (download), attestation verification.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-006 [P2] REVA-UI-006: Knowledge-Gap Board (kanban by status; sort by impact; owner/due date; probes with "Run probe" action; revision history diff). · RJ-05. · acceptance

- **Source:** `reva-requirements.md:1046-1046` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-006 | **Knowledge-Gap Board** (kanban by status; sort by impact; owner/due date; probes with "Run probe" action; revision history diff). | RJ-05. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-006 | Knowledge-Gap Board (kanban by status; sort by impact; owner/due date; probes with "Run probe" action; revision history diff). | RJ-05. | acceptance»
- [ ] Knowledge-Gap Board (kanban by status; sort by impact; owner/due date; probes with "Run probe" action; revision history diff).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-009 [P2] REVA-UI-009: Service Boundary Map: services, routes, calls (static inferred vs runtime observed styled distinctly), resources; filter by service/repo; click-through to source spans. Large graphs use server-side ag

- **Source:** `reva-requirements.md:1049-1049` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-009 | **Service Boundary Map**: services, routes, calls (static inferred vs runtime observed styled distinctly), resources; filter by service/repo; click-through to source spans. Large graphs use server-side aggregation and progressive disclosure (≤ 2,000 rendered elements at once). | RJ-03. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-009' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-009') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-009 | Service Boundary Map: services, routes, calls (static inferred vs runtime observed styled distinctly), resources; filter by service/repo; click-through to source spans. Large graphs use server-side aggregation and progressive disclosure (≤ 2,000 rendered elements at once). | RJ-03. | acceptance»
- [ ] Service Boundary Map: services, routes, calls (static inferred vs runtime observed styled distinctly), resources; filter by service/repo; click-through to source spans. Large graphs use server-side aggregation and progressive disclosure (≤ 2,000 rendered elements at once).
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-010 [P2] REVA-UI-010: API Surface Explorer: operations with templates (basis badge), statuses, callers, key-shapes, OpenAPI alignment categories. · RJ-10. · acceptance

- **Source:** `reva-requirements.md:1050-1050` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-010 | **API Surface Explorer**: operations with templates (basis badge), statuses, callers, key-shapes, OpenAPI alignment categories. | RJ-10. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-010' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-010') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-010 | API Surface Explorer: operations with templates (basis badge), statuses, callers, key-shapes, OpenAPI alignment categories. | RJ-10. | acceptance»
- [ ] API Surface Explorer: operations with templates (basis badge), statuses, callers, key-shapes, OpenAPI alignment categories.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-011 [P2] REVA-UI-011: Reconciliation View: matched / static-only / runtime-only / ambiguous lists with counts and window/coverage banner. · RJ-10. · acceptance

- **Source:** `reva-requirements.md:1051-1051` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-011 | **Reconciliation View**: matched / static-only / runtime-only / ambiguous lists with counts and window/coverage banner. | RJ-10. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-011' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-011') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-011 | Reconciliation View: matched / static-only / runtime-only / ambiguous lists with counts and window/coverage banner. | RJ-10. | acceptance»
- [ ] Reconciliation View: matched / static-only / runtime-only / ambiguous lists with counts and window/coverage banner.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-012 [P2] REVA-UI-012: Impact Trace Studio: seed picker (typed), template picker, as-of pickers, results grouped (§7.14 FT-005), path viewer with per-edge warrants and epistemic styling, frontier panel with reasons, test-sc

- **Source:** `reva-requirements.md:1052-1052` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-012 | **Impact Trace Studio**: seed picker (typed), template picker, as-of pickers, results grouped (§7.14 FT-005), path viewer with per-edge warrants and epistemic styling, frontier panel with reasons, test-scope list, "Create gap" from frontier, export as answer. | RJ-03, RJ-04. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-012' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-012') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-012 | Impact Trace Studio: seed picker (typed), template picker, as-of pickers, results grouped (§7.14 FT-005), path viewer with per-edge warrants and epistemic styling, frontier panel with reasons, test-scope list, "Create gap" from frontier, export as answer. | RJ-03, RJ-04. | acceptance»
- [ ] Impact Trace Studio: seed picker (typed), template picker, as-of pickers, results grouped (§7.14 FT-005), path viewer with per-edge warrants and epistemic styling, frontier panel with reasons, test-scope list, "Create gap" from frontier, export as answer.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-013 [P2] REVA-UI-013: Graph Diff Viewer: side-by-side and change list with statuses and match bases; ambiguous items queue. · RJ-11. · acceptance

- **Source:** `reva-requirements.md:1053-1053` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-013 | **Graph Diff Viewer**: side-by-side and change list with statuses and match bases; ambiguous items queue. | RJ-11. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-013' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-013') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-013 | Graph Diff Viewer: side-by-side and change list with statuses and match bases; ambiguous items queue. | RJ-11. | acceptance»
- [ ] Graph Diff Viewer: side-by-side and change list with statuses and match bases; ambiguous items queue.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-015 [P2] REVA-UI-015: Answer View integration in KGF's NL query screen: claims grouped by kind with badges, citations open the WarrantDrawer, contradictions and unknowns sections. · RJ-08. · acceptance

- **Source:** `reva-requirements.md:1055-1055` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-015 | **Answer View integration** in KGF's NL query screen: claims grouped by kind with badges, citations open the WarrantDrawer, contradictions and unknowns sections. | RJ-08. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-015' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-015') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-015 | Answer View integration in KGF's NL query screen: claims grouped by kind with badges, citations open the WarrantDrawer, contradictions and unknowns sections. | RJ-08. | acceptance»
- [ ] Answer View integration in KGF's NL query screen: claims grouped by kind with badges, citations open the WarrantDrawer, contradictions and unknowns sections.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-UI-016 [P2] REVA-UI-016: Evaluation Dashboard: suite runs, metrics over time, failing cases with diffs. · RJ-08. · acceptance

- **Source:** `reva-requirements.md:1056-1056` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-UI-016 | **Evaluation Dashboard**: suite runs, metrics over time, failing cases with diffs. | RJ-08. | acceptance
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-UI-016' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-UI-016') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-UI-016 | Evaluation Dashboard: suite runs, metrics over time, failing cases with diffs. | RJ-08. | acceptance»
- [ ] Evaluation Dashboard: suite runs, metrics over time, failing cases with diffs.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-VW-004 [P2] REVA-VW-004: Stable ordering: collections are ordered by a documented key (default: canonical ID). · Two identical requests return identical pages. · unit

- **Source:** `reva-requirements.md:977-977` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-VW-004 | Stable ordering: collections are ordered by a documented key (default: canonical ID). | Two identical requests return identical pages. | unit
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-VW-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-VW-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Two identical requests return identical pages
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-REVA-XP-002 [P2] REVA-XP-002: Legacy hardware probe and signal decoder bridge (TShark, Sigrok). Connects to pre-recorded hardware signal logic captures. · Disabled by default (REVA_XP_SIGNAL_DECODE=false); consumes pre-recorded of

- **Source:** `reva-requirements.md:1182-1182` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
REVA-XP-002 | Legacy hardware probe and signal decoder bridge (TShark, Sigrok). Connects to pre-recorded hardware signal logic captures. | Disabled by default (`REVA_XP_SIGNAL_DECODE=false`); consumes pre-recorded offline captures only. | component
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'REVA-XP-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('REVA-XP-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «REVA-XP-002 | Legacy hardware probe and signal decoder bridge (TShark, Sigrok). Connects to pre-recorded hardware signal logic captures. | Disabled by default (REVA_XP_SIGNAL_DECODE=false); consumes pre-recorded offline captures only. | component»
- [ ] Legacy hardware probe and signal decoder bridge (TShark, Sigrok). Connects to pre-recorded hardware signal logic captures.
- [ ] Disabled by default (REVA_XP_SIGNAL_DECODE=false); consumes pre-recorded offline captures only.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-02 [P2] RJ-02: Contradiction governance. Confluence says service billing is owned by Team A; ServiceNow CMDB says Team B, with overlapping validity

- **Source:** `reva-requirements.md:1411-1411` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-02 | **Contradiction governance.** Confluence says service `billing` is owned by Team A; ServiceNow CMDB says Team B, with overlapping validity. | One `value_conflict` opens; affected entities show the banner; an answer about ownership shows both claims and the contradiction; a reviewer resolves by human decision; history keeps both; as-of queries before and after the decision behave correctly.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-02 | Contradiction governance. Confluence says service billing is owned by Team A; ServiceNow CMDB says Team B, with overlapping validity. | One value_conflict opens; affected entities show the banner; an answer about ownership shows both claims and the contradiction; a reviewer resolves by human decision; history keeps both; as-of queries before and after the decision behav»
- [ ] Contradiction governance. Confluence says service billing is owned by Team A; ServiceNow CMDB says Team B, with overlapping validity.
- [ ] One value_conflict opens; affected entities show the banner; an answer about ownership shows both claims and the contradiction; a reviewer resolves by human decision; history keeps both; as-of queries before and after the decision behave correctly.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-03 [P2] RJ-03: Service-account blast radius. Fixture estate: 3 repos (Spring Boot billing service, FastAPI notifications service, Electron admin app), Helm values, OTel export, DB schemas. Seed serviceaccount = svc-

- **Source:** `reva-requirements.md:1412-1412` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-03 | **Service-account blast radius.** Fixture estate: 3 repos (Spring Boot billing service, FastAPI notifications service, Electron admin app), Helm values, OTel export, DB schemas. Seed `service_account = svc-billing-rotator`, template `impact.service_account`. | Results list the services, routes, resources, deployments, Jira stories and owners in the golden file; paths show weakest-link epistemic states; coverage is complete for the fixture scope; a deliberately unindexed repo produces a frontier gap and the UI shows "Unknown — not proven empty" for that branch.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-03 | Service-account blast radius. Fixture estate: 3 repos (Spring Boot billing service, FastAPI notifications service, Electron admin app), Helm values, OTel export, DB schemas. Seed service_account = svc-billing-rotator, template impact.service_account. | Results list the services, routes, resources, deployments, Jira stories and owners in the golden file; paths show weake»
- [ ] Service-account blast radius. Fixture estate: 3 repos (Spring Boot billing service, FastAPI notifications service, Electron admin app), Helm values, OTel export, DB schemas. Seed service_account = svc-billing-rotator, template impact.service_account.
- [ ] Results list the services, routes, resources, deployments, Jira stories and owners in the golden file; paths show weakest-link epistemic states; coverage is complete for the fixture scope; a deliberately unindexed repo produces a frontier gap and the UI shows "Unknown — not proven empty" for that branch.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-04 [P2] RJ-04: Rule-change test scope. Seed ruleid = DISCOUNTRULE7, template impact.rulechange, after verifier runs have collected coverage data

- **Source:** `reva-requirements.md:1413-1413` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-04 | **Rule-change test scope.** Seed `rule_id = DISCOUNT_RULE_7`, template `impact.rule_change`, after verifier runs have collected coverage data. | Impacted symbols match golden; recommended tests include exactly the tests whose coverage contexts hit them; stale coverage is flagged; removing coverage data yields a gap instead of an empty list.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-04 | Rule-change test scope. Seed rule_id = DISCOUNT_RULE_7, template impact.rule_change, after verifier runs have collected coverage data. | Impacted symbols match golden; recommended tests include exactly the tests whose coverage contexts hit them; stale coverage is flagged; removing coverage data yields a gap instead of an empty list.»
- [ ] Rule-change test scope. Seed rule_id = DISCOUNT_RULE_7, template impact.rule_change, after verifier runs have collected coverage data.
- [ ] Impacted symbols match golden; recommended tests include exactly the tests whose coverage contexts hit them; stale coverage is flagged; removing coverage data yields a gap instead of an empty list.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-06 [P2] RJ-06: Proof-of-Done. For a fixture KGF feature with 6 obligations: (a) only test files exist → nothing closes; (b) tests exist but one is assert True → AG-05; (c) one mocks the owner → AG-06; (d) all good →

- **Source:** `reva-requirements.md:1415-1415` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-06 | **Proof-of-Done.** For a fixture KGF feature with 6 obligations: (a) only test files exist → nothing closes; (b) tests exist but one is `assert True` → AG-05; (c) one mocks the owner → AG-06; (d) all good → closed with attestation; (e) commit changes an owner → `stale`; (f) a board item manually set to Done appears as "Asserted done — unproven". Export the HTML ledger. | Each sub-step shows the exact expected reason codes in UI and API; ledger IDs are stable; the HTML export works offline.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-06 | Proof-of-Done. For a fixture KGF feature with 6 obligations: (a) only test files exist → nothing closes; (b) tests exist but one is assert True → AG-05; (c) one mocks the owner → AG-06; (d) all good → closed with attestation; (e) commit changes an owner → stale; (f) a board item manually set to Done appears as "Asserted done — unproven". Export the HTML ledger. | Each s»
- [ ] Proof-of-Done. For a fixture KGF feature with 6 obligations: (a) only test files exist → nothing closes; (b) tests exist but one is assert True → AG-05; (c) one mocks the owner → AG-06; (d) all good → closed with attestation; (e) commit changes an owner → stale; (f) a board item manually set to Done appears as "Asserted done — unproven". Export the HTML ledger.
- [ ] Each sub-step shows the exact expected reason codes in UI and API; ledger IDs are stable; the HTML export works offline.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-09 [P2] RJ-09: Shipped-artifact provenance and drift. Upload the CI-built Spring Boot JAR, Go binary and OCI image for commit C; then a JAR built from a dirty tree; then a JAR whose embedded commit is not ingested

- **Source:** `reva-requirements.md:1418-1418` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-09 | **Shipped-artifact provenance and drift.** Upload the CI-built Spring Boot JAR, Go binary and OCI image for commit C; then a JAR built from a dirty tree; then a JAR whose embedded commit is not ingested. | Components, SBOM (valid CycloneDX/SPDX), `BUILT_FROM` edges to C; drift verdicts `verified_match` (with reference build), `unverifiable_dirty`, and `unknown` + `GAP_COMMIT_NOT_INGESTED` respectively.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-09 | Shipped-artifact provenance and drift. Upload the CI-built Spring Boot JAR, Go binary and OCI image for commit C; then a JAR built from a dirty tree; then a JAR whose embedded commit is not ingested. | Components, SBOM (valid CycloneDX/SPDX), BUILT_FROM edges to C; drift verdicts verified_match (with reference build), unverifiable_dirty, and unknown + GAP_COMMIT_NOT_ING»
- [ ] Shipped-artifact provenance and drift. Upload the CI-built Spring Boot JAR, Go binary and OCI image for commit C; then a JAR built from a dirty tree; then a JAR whose embedded commit is not ingested.
- [ ] Components, SBOM (valid CycloneDX/SPDX), BUILT_FROM edges to C; drift verdicts verified_match (with reference build), unverifiable_dirty, and unknown + GAP_COMMIT_NOT_INGESTED respectively.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-RJ-11 [P2] RJ-11: Graph diff without churn. Extract boundaries at commits A and B of the Electron fixture (E-06 changes) and of the Spring fixture (controller moved to a new package + one route added)

- **Source:** `reva-requirements.md:1420-1420` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
RJ-11 | **Graph diff without churn.** Extract boundaries at commits A and B of the Electron fixture (E-06 changes) and of the Spring fixture (controller moved to a new package + one route added). | E-06 regression passes; moved controller shows `moved` with routes `unchanged`; added route `added`; the diff warrant cites both snapshots.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'RJ-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('RJ-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «RJ-11 | Graph diff without churn. Extract boundaries at commits A and B of the Electron fixture (E-06 changes) and of the Spring fixture (controller moved to a new package + one route added). | E-06 regression passes; moved controller shows moved with routes unchanged; added route added; the diff warrant cites both snapshots.»
- [ ] Graph diff without churn. Extract boundaries at commits A and B of the Electron fixture (E-06 changes) and of the Spring fixture (controller moved to a new package + one route added).
- [ ] E-06 regression passes; moved controller shows moved with routes unchanged; added route added; the diff warrant cites both snapshots.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']


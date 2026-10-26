# EPIC-GUICCGHCP-UNTR: GUI-cc-ghcp-requirements.md · untraced

*No code, test or infra reference to the ID anywhere.* 59 tasks, ~354.0 h, priorities {'P0': 6, 'P1': 31, 'P2': 22}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-COMP-02 [P0] COMP-02: TextField, NumberField, SecretField (reveal toggle, never autocompletes, paste allowed), TextArea, Select, AsyncCombobox (debounced server search, keyboard APG combobox), ChipMultiSelect, DateTimeFiel

- **Source:** `GUI-cc-ghcp-requirements.md:708-708` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-02 | `TextField`, `NumberField`, `SecretField` (reveal toggle, never autocompletes, paste allowed), `TextArea`, `Select`, `AsyncCombobox` (debounced server search, keyboard APG combobox), `ChipMultiSelect`, `DateTimeField`/`DateRangeField` (UTC on wire, user zone shown, zone label visible), `Slider`/`RangeSlider` (time), `Toggle`, `Checkbox`, `SegmentedControl` | visible label, help text, error text linked by `aria-describedby`; validate on blur + submit; server pointer→field mapping
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-02 | TextField, NumberField, SecretField (reveal toggle, never autocompletes, paste allowed), TextArea, Select, AsyncCombobox (debounced server search, keyboard APG combobox), ChipMultiSelect, DateTimeField/DateRangeField (UTC on wire, user zone shown, zone label visible), Slider/RangeSlider (time), Toggle, Checkbox, SegmentedControl | visible label, help text, error text »
- [ ] TextField, NumberField, SecretField (reveal toggle, never autocompletes, paste allowed), TextArea, Select, AsyncCombobox (debounced server search, keyboard APG combobox), ChipMultiSelect, DateTimeField/DateRangeField (UTC on wire, user zone shown, zone label visible), Slider/RangeSlider (time), Toggle, Checkbox, SegmentedControl
- [ ] visible label, help text, error text linked by aria-describedby; validate on blur + submit; server pointer→field mapping
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-04 [P0] COMP-04: DataGrid (TanStack Table + Virtual): sort, filter, group, pin columns, column chooser (persisted per scope), row selection, inline edit (where endpoint exists), density, export CSV (respects filters +

- **Source:** `GUI-cc-ghcp-requirements.md:710-710` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-04 | `DataGrid` (TanStack Table + Virtual): sort, filter, group, pin columns, column chooser (persisted per scope), row selection, inline edit (where endpoint exists), density, export CSV (respects filters + permission), ARIA grid, row count/position announced, > 100 rows virtualized | empty/error rows inside grid; sticky identity/status/actions columns
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-04 | DataGrid (TanStack Table + Virtual): sort, filter, group, pin columns, column chooser (persisted per scope), row selection, inline edit (where endpoint exists), density, export CSV (respects filters + permission), ARIA grid, row count/position announced, > 100 rows virtualized | empty/error rows inside grid; sticky identity/status/actions columns»
- [ ] DataGrid (TanStack Table + Virtual): sort, filter, group, pin columns, column chooser (persisted per scope), row selection, inline edit (where endpoint exists), density, export CSV (respects filters + permission), ARIA grid, row count/position announced, > 100 rows virtualized
- [ ] empty/error rows inside grid; sticky identity/status/actions columns
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-11 [P0] COMP-11: StreamingAnswer (token append, caret, Stop/Regenerate, mode badge, boundary badge, aria-live=polite with 1 s batching), CitationChip ([n] → evidence; hover/focus highlights graph node/edge & source sp

- **Source:** `GUI-cc-ghcp-requirements.md:717-717` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-11 | `StreamingAnswer` (token append, caret, Stop/Regenerate, mode badge, boundary badge, `aria-live=polite` with 1 s batching), `CitationChip` (`[n]` → evidence; hover/focus highlights graph node/edge & source span), `ConfidenceMeter` (shows value + `inputs` list; never shown without inputs; `confidence_score < .7` shows `uncertainty_reason`), `SuggestionCard` (§11.2), `EvidenceManifestPanel`, `AbstainNotice` |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-11 | StreamingAnswer (token append, caret, Stop/Regenerate, mode badge, boundary badge, aria-live=polite with 1 s batching), CitationChip ([n] → evidence; hover/focus highlights graph node/edge & source span), ConfidenceMeter (shows value + inputs list; never shown without inputs; confidence_score < .7 shows uncertainty_reason), SuggestionCard (§11.2), EvidenceManifestPane»
- [ ] StreamingAnswer (token append, caret, Stop/Regenerate, mode badge, boundary badge, aria-live=polite with 1 s batching), CitationChip ([n] → evidence; hover/focus highlights graph node/edge & source span), ConfidenceMeter (shows value + inputs list; never shown without inputs; confidence_score < .7 shows uncertainty_reason), SuggestionCard (§11.2), EvidenceManifestPanel, AbstainNotice
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-002 [P0] GUI-SCR-002: A01 Given the catalog loads, when a connector is chosen and the form submitted with a raw secret in config, then the server 422 is shown on the field and nothing is saved; with a env:// ref, POST /sou

- **Source:** `GUI-cc-ghcp-requirements.md:851-855` (list_item) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-002-A01` Given the catalog loads, when a connector is chosen and the form submitted with a raw secret in `config`, then the server 422 is shown on the field and nothing is saved; with a `env://` ref, `POST /sources` returns 201 and step 3 opens.
  - `A02` Given a dry-run job returns `PARTIAL`, when the step renders, then rejected counts and reasons are shown and the step is not marked complete.
  - `A03` Given a browser refresh mid-wizard, when the route reopens, then the same step and non-secret values are restored with a `Draft restored` banner; secrets are empty.
  - `A04` Given baseline FAILED, when viewed, then the trail shows Failed, the error with correlation ID is visible and Complete is disabled.
  - `A05` Given baseline SUCCEEDED, when step 8 runs a question, then the answer shows evidence from the newly ingested entities (assert at least one citation canonical_id belongs to the new source's run).
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-002' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-002') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A02 Given a dry-run job returns PARTIAL, when the step renders, then rejected counts and reasons are shown and the step is not marked complete.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-02 [P0] GUI-VSC-02: Status bar item: EOIP: Connected · <tenant> / EOIP: Offline / EOIP: Not configured; click opens Set Access Token; token stored in SecretStorage only

- **Source:** `GUI-cc-ghcp-requirements.md:1322-1322` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-02 | Status bar item: `EOIP: Connected · <tenant>` / `EOIP: Offline` / `EOIP: Not configured`; click opens Set Access Token; token stored in `SecretStorage` only
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-02 | Status bar item: EOIP: Connected · <tenant> / EOIP: Offline / EOIP: Not configured; click opens Set Access Token; token stored in SecretStorage only»
- [ ] Status bar item: EOIP: Connected · <tenant> / EOIP: Offline / EOIP: Not configured; click opens Set Access Token; token stored in SecretStorage only
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-03 [P0] JRN-03: Search → expand → filter → inspect entity → provenance → save view → restart → restore → authorized export

- **Source:** `GUI-cc-ghcp-requirements.md:114-114` (table_row) · **Type:** Security · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-03 | Search → expand → filter → inspect entity → provenance → save view → restart → restore → authorized export | SCR-005, 006
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-03 | Search → expand → filter → inspect entity → provenance → save view → restart → restore → authorized export | SCR-005, 006»
- [ ] Search → expand → filter → inspect entity → provenance → save view → restart → restore → authorized export
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-01 [P1] COMP-01: Button / IconButton / SplitButton

- **Source:** `GUI-cc-ghcp-requirements.md:707-707` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-01 | `Button` / `IconButton` / `SplitButton` | variants primary/secondary/quiet/danger; sizes 28/32/36/40; `loading` keeps width and shows inline spinner + `aria-busy`; icon-only requires `aria-label` and renders `Tooltip`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-01 | Button / IconButton / SplitButton | variants primary/secondary/quiet/danger; sizes 28/32/36/40; loading keeps width and shows inline spinner + aria-busy; icon-only requires aria-label and renders Tooltip»
- [ ] Button / IconButton / SplitButton
- [ ] variants primary/secondary/quiet/danger; sizes 28/32/36/40; loading keeps width and shows inline spinner + aria-busy; icon-only requires aria-label and renders Tooltip
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-03 [P1] COMP-03: Tabs (APG tabs; lazy panels), Accordion, Breadcrumbs, LazyTree (virtual, APG treeview, async children), Pagination/LoadMore (shows server cap), CommandPalette, RecentsList

- **Source:** `GUI-cc-ghcp-requirements.md:709-709` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-03 | `Tabs` (APG tabs; lazy panels), `Accordion`, `Breadcrumbs`, `LazyTree` (virtual, APG treeview, async children), `Pagination`/`LoadMore` (shows server cap), `CommandPalette`, `RecentsList` |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-03 | Tabs (APG tabs; lazy panels), Accordion, Breadcrumbs, LazyTree (virtual, APG treeview, async children), Pagination/LoadMore (shows server cap), CommandPalette, RecentsList»
- [ ] Tabs (APG tabs; lazy panels), Accordion, Breadcrumbs, LazyTree (virtual, APG treeview, async children), Pagination/LoadMore (shows server cap), CommandPalette, RecentsList
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-05 [P1] COMP-05: EntityCard (icon, label chip, name, ID ellipsis, trust ladder, freshness, fact badge), EntityHoverCard (300 ms delay; fetches GET /entities/{id} once; keyboard reachable via Enter on focused chip), Re

- **Source:** `GUI-cc-ghcp-requirements.md:711-711` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-05 | `EntityCard` (icon, label chip, name, ID ellipsis, trust ladder, freshness, fact badge), `EntityHoverCard` (300 ms delay; fetches `GET /entities/{id}` once; keyboard reachable via `Enter` on focused chip), `RelationshipChip` (type, direction arrow, fact-class style), `PropertyList` (type-aware: ISO dates → localized with raw on hover; URLs → safe links (http/https only, rel noopener); code refs → mono; long text → expandable) | masked fields render `••••` with lock icon and reveal only if server returns value
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-05 | EntityCard (icon, label chip, name, ID ellipsis, trust ladder, freshness, fact badge), EntityHoverCard (300 ms delay; fetches GET /entities/{id} once; keyboard reachable via Enter on focused chip), RelationshipChip (type, direction arrow, fact-class style), PropertyList (type-aware: ISO dates → localized with raw on hover; URLs → safe links (http/https only, rel noope»
- [ ] EntityCard (icon, label chip, name, ID ellipsis, trust ladder, freshness, fact badge), EntityHoverCard (300 ms delay; fetches GET /entities/{id} once; keyboard reachable via Enter on focused chip), RelationshipChip (type, direction arrow, fact-class style), PropertyList (type-aware: ISO dates → localized with raw on hover; URLs → safe links (http/https only, rel noopener); code refs → mono; long t
- [ ] masked fields render •••• with lock icon and reveal only if server returns value
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-06 [P1] COMP-06: JsonViewer (collapsible, copy, search, never executes), DiffViewer (side-by-side/inline, added/removed/changed with +/−/Δ symbols and colours)

- **Source:** `GUI-cc-ghcp-requirements.md:712-712` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-06 | `JsonViewer` (collapsible, copy, search, never executes), `DiffViewer` (side-by-side/inline, added/removed/changed with +/−/Δ symbols and colours) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-06 | JsonViewer (collapsible, copy, search, never executes), DiffViewer (side-by-side/inline, added/removed/changed with +/−/Δ symbols and colours)»
- [ ] JsonViewer (collapsible, copy, search, never executes), DiffViewer (side-by-side/inline, added/removed/changed with +/−/Δ symbols and colours)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-07 [P1] COMP-07: StatusPill (maps §2.1/§2.7 enums → colour+icon+label; unknown → neutral with raw text), FactBadge (§2.2), TrustLadder (§2.3), FreshnessStamp (as of 12:04 · 6 min ago, warns > SLO), ModeBadge (§2.4), B

- **Source:** `GUI-cc-ghcp-requirements.md:713-713` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-07 | `StatusPill` (maps §2.1/§2.7 enums → colour+icon+label; unknown → neutral with raw text), `FactBadge` (§2.2), `TrustLadder` (§2.3), `FreshnessStamp` (`as of 12:04 · 6 min ago`, warns > SLO), `ModeBadge` (§2.4), `BoundaryBadge` (§2.5), `RiskTierBadge` (§2.6), `AbstainBadge` | never colour-only
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-07 | StatusPill (maps §2.1/§2.7 enums → colour+icon+label; unknown → neutral with raw text), FactBadge (§2.2), TrustLadder (§2.3), FreshnessStamp (as of 12:04 · 6 min ago, warns > SLO), ModeBadge (§2.4), BoundaryBadge (§2.5), RiskTierBadge (§2.6), AbstainBadge | never colour-only»
- [ ] StatusPill (maps §2.1/§2.7 enums → colour+icon+label; unknown → neutral with raw text), FactBadge (§2.2), TrustLadder (§2.3), FreshnessStamp (as of 12:04 · 6 min ago, warns > SLO), ModeBadge (§2.4), BoundaryBadge (§2.5), RiskTierBadge (§2.6), AbstainBadge
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-08 [P1] COMP-08: Skeleton (structure-shaped, 120 ms dissolve), Spinner (only for < 400 ms indeterminate), Progress (determinate/indeterminate/job with ETA only when server provides timings), Toast (80 z, 6 s, pause on

- **Source:** `GUI-cc-ghcp-requirements.md:714-714` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-08 | `Skeleton` (structure-shaped, 120 ms dissolve), `Spinner` (only for < 400 ms indeterminate), `Progress` (determinate/indeterminate/job with ETA only when server provides timings), `Toast` (80 z, 6 s, pause on hover, action button, `role=status`), `InlineAlert`/`Banner` (info/warning/danger/success with icon + title + detail + correlation ID copy), `EmptyState`, `ErrorState` (problem → §8.3), `OfflineState` (capture age), `DeniedState` (needed capability, no object disclosure), `StaleState` (refresh action), `MissingBackendState` (contract ID, "Not available in this deployment") |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-08 | Skeleton (structure-shaped, 120 ms dissolve), Spinner (only for < 400 ms indeterminate), Progress (determinate/indeterminate/job with ETA only when server provides timings), Toast (80 z, 6 s, pause on hover, action button, role=status), InlineAlert/Banner (info/warning/danger/success with icon + title + detail + correlation ID copy), EmptyState, ErrorState (problem → »
- [ ] Skeleton (structure-shaped, 120 ms dissolve), Spinner (only for < 400 ms indeterminate), Progress (determinate/indeterminate/job with ETA only when server provides timings), Toast (80 z, 6 s, pause on hover, action button, role=status), InlineAlert/Banner (info/warning/danger/success with icon + title + detail + correlation ID copy), EmptyState, ErrorState (problem → §8.3), OfflineState (capture a
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-09 [P1] COMP-09: Tooltip (portal, 300 ms hover / 0 ms focus, aria-describedby, Esc closes), Popover, Dialog (focus trap/restore, inert background, Esc, aria-modal), Drawer (right/bottom), Sheet (tablet/mobile), Confir

- **Source:** `GUI-cc-ghcp-requirements.md:715-715` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-09 | `Tooltip` (portal, 300 ms hover / 0 ms focus, `aria-describedby`, Esc closes), `Popover`, `Dialog` (focus trap/restore, inert background, Esc, `aria-modal`), `Drawer` (right/bottom), `Sheet` (tablet/mobile), `ConfirmDialog` (impact summary + typed confirmation when `severity='high'`), `ContextMenu` (APG menu; keyboard `Shift+F10`) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-09 | Tooltip (portal, 300 ms hover / 0 ms focus, aria-describedby, Esc closes), Popover, Dialog (focus trap/restore, inert background, Esc, aria-modal), Drawer (right/bottom), Sheet (tablet/mobile), ConfirmDialog (impact summary + typed confirmation when severity='high'), ContextMenu (APG menu; keyboard Shift+F10)»
- [ ] Tooltip (portal, 300 ms hover / 0 ms focus, aria-describedby, Esc closes), Popover, Dialog (focus trap/restore, inert background, Esc, aria-modal), Drawer (right/bottom), Sheet (tablet/mobile), ConfirmDialog (impact summary + typed confirmation when severity='high'), ContextMenu (APG menu; keyboard Shift+F10)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-10 [P1] COMP-10: Stepper (linear/non-linear, current step only visible + compact trail, resumable from XState snapshot), Uploader (drag/drop, file list, accept from GET /connectors/files/formats, 3 MB client cap with 

- **Source:** `GUI-cc-ghcp-requirements.md:716-716` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-10 | `Stepper` (linear/non-linear, current step only visible + compact trail, resumable from XState snapshot), `Uploader` (drag/drop, file list, accept from `GET /connectors/files/formats`, 3 MB client cap with message, octet-stream POST, progress, cancel; chunked/resumable is `BACKEND-MISSING-011` → shown as disabled "Resumable upload not available"), `FilterBuilder` (AND/OR groups; field from schema; operators = ≠ > < contains regex in; produces `QueryPlan.filters`), `CodeEditor` (Monaco lazy; read-only mode; dialect syntax), `RichTextEditor` (Tiptap lazy; sanitized HTML output; no raw HTML paste), `FlowEditor` (React Flow wrapper with keyboard alternatives: node palette list, "Connect A → B" command) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-10 | Stepper (linear/non-linear, current step only visible + compact trail, resumable from XState snapshot), Uploader (drag/drop, file list, accept from GET /connectors/files/formats, 3 MB client cap with message, octet-stream POST, progress, cancel; chunked/resumable is BACKEND-MISSING-011 → shown as disabled "Resumable upload not available"), FilterBuilder (AND/OR groups»
- [ ] Stepper (linear/non-linear, current step only visible + compact trail, resumable from XState snapshot), Uploader (drag/drop, file list, accept from GET /connectors/files/formats, 3 MB client cap with message, octet-stream POST, progress, cancel; chunked/resumable is BACKEND-MISSING-011 → shown as disabled "Resumable upload not available"), FilterBuilder (AND/OR groups; field from schema; operators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-12 [P1] COMP-12: GraphCanvas, GraphToolbar, LayoutPicker, Legend (schema-driven; click toggles label; shows counts), Minimap (200×150, viewport rect, click-to-navigate), TimelineScrubber (dual handle + histogram), Len

- **Source:** `GUI-cc-ghcp-requirements.md:718-718` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-12 | `GraphCanvas`, `GraphToolbar`, `LayoutPicker`, `Legend` (schema-driven; click toggles label; shows counts), `Minimap` (200×150, viewport rect, click-to-navigate), `TimelineScrubber` (dual handle + histogram), `LensSwitcher`, `PathBreadcrumb`, `GraphTableView`, `GraphTreeView`, `ClusterHull`, `ImpactRings` | §10
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-12' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-12') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-12 | GraphCanvas, GraphToolbar, LayoutPicker, Legend (schema-driven; click toggles label; shows counts), Minimap (200×150, viewport rect, click-to-navigate), TimelineScrubber (dual handle + histogram), LensSwitcher, PathBreadcrumb, GraphTableView, GraphTreeView, ClusterHull, ImpactRings | §10»
- [ ] GraphCanvas, GraphToolbar, LayoutPicker, Legend (schema-driven; click toggles label; shows counts), Minimap (200×150, viewport rect, click-to-navigate), TimelineScrubber (dual handle + histogram), LensSwitcher, PathBreadcrumb, GraphTableView, GraphTreeView, ClusterHull, ImpactRings
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-13 [P1] COMP-13: NotificationItem, PresenceAvatars (only when BACKEND-MISSING-016 exists; else hidden), CommentThread (hidden until backend), ApprovalCard (exact target, changed fields, risk tier, expiry, approve/reje

- **Source:** `GUI-cc-ghcp-requirements.md:719-719` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-13 | `NotificationItem`, `PresenceAvatars` (only when `BACKEND-MISSING-016` exists; else hidden), `CommentThread` (hidden until backend), `ApprovalCard` (exact target, changed fields, risk tier, expiry, approve/reject with reason), `RemediationBoard` (Kanban via dnd-kit with keyboard move), `JobLog` (virtualized, bounded 5 000 lines, copy, filter), `ActivityTray` |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-13 | NotificationItem, PresenceAvatars (only when BACKEND-MISSING-016 exists; else hidden), CommentThread (hidden until backend), ApprovalCard (exact target, changed fields, risk tier, expiry, approve/reject with reason), RemediationBoard (Kanban via dnd-kit with keyboard move), JobLog (virtualized, bounded 5 000 lines, copy, filter), ActivityTray»
- [ ] NotificationItem, PresenceAvatars (only when BACKEND-MISSING-016 exists; else hidden), CommentThread (hidden until backend), ApprovalCard (exact target, changed fields, risk tier, expiry, approve/reject with reason), RemediationBoard (Kanban via dnd-kit with keyboard move), JobLog (virtualized, bounded 5 000 lines, copy, filter), ActivityTray
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-14 [P1] COMP-14: ScopeSwitcher (tenant/workspace; shows lock when principal is tenant-bound; search; recent)

- **Source:** `GUI-cc-ghcp-requirements.md:720-720` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-14 | `ScopeSwitcher` (tenant/workspace; shows lock when principal is tenant-bound; search; recent) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-14 | ScopeSwitcher (tenant/workspace; shows lock when principal is tenant-bound; search; recent)»
- [ ] ScopeSwitcher (tenant/workspace; shows lock when principal is tenant-bound; search; recent)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-15 [P1] COMP-15: KnowledgeAgeStamp (SR-ING-051: every answer/result header shows Knowledge as of <time> · source lag <n> when freshness/lastseen/asof present; else Knowledge age unknown)

- **Source:** `GUI-cc-ghcp-requirements.md:721-721` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-15 | `KnowledgeAgeStamp` (SR-ING-051: every answer/result header shows `Knowledge as of <time> · source lag <n>` when `freshness`/`last_seen`/`as_of` present; else `Knowledge age unknown`) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-15' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-15') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-15 | KnowledgeAgeStamp (SR-ING-051: every answer/result header shows Knowledge as of <time> · source lag <n> when freshness/last_seen/as_of present; else Knowledge age unknown)»
- [ ] KnowledgeAgeStamp (SR-ING-051: every answer/result header shows Knowledge as of <time> · source lag <n> when freshness/last_seen/as_of present; else Knowledge age unknown)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-16 [P1] COMP-16: ResultBanner (renders partial:true → "Partial result: <warnings>"; warnings[] list; truncated)

- **Source:** `GUI-cc-ghcp-requirements.md:722-722` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-16 | `ResultBanner` (renders `partial:true` → "Partial result: <warnings>"; `warnings[]` list; `truncated_*`) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-16' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-16') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-16 | ResultBanner (renders partial:true → "Partial result: <warnings>"; warnings[] list; truncated_*)»
- [ ] ResultBanner (renders partial:true → "Partial result: <warnings>"; warnings[] list; truncated_*)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-17 [P1] COMP-17: CorrelationId (mono, middle ellipsis, copy; present in every error, every job row, every answer footer)

- **Source:** `GUI-cc-ghcp-requirements.md:723-723` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-17 | `CorrelationId` (mono, middle ellipsis, copy; present in every error, every job row, every answer footer) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-17' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-17') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-17 | CorrelationId (mono, middle ellipsis, copy; present in every error, every job row, every answer footer)»
- [ ] CorrelationId (mono, middle ellipsis, copy; present in every error, every job row, every answer footer)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-18 [P1] COMP-18: KpiTile (value with tabular nums, unit, as-of stamp, trend sparkline only with ≥ 3 points, N/A state; never a coloured ring without denominator)

- **Source:** `GUI-cc-ghcp-requirements.md:724-724` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-18 | `KpiTile` (value with tabular nums, unit, as-of stamp, trend sparkline only with ≥ 3 points, `N/A` state; never a coloured ring without denominator) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-18' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-18') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-18 | KpiTile (value with tabular nums, unit, as-of stamp, trend sparkline only with ≥ 3 points, N/A state; never a coloured ring without denominator)»
- [ ] KpiTile (value with tabular nums, unit, as-of stamp, trend sparkline only with ≥ 3 points, N/A state; never a coloured ring without denominator)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-19 [P1] COMP-19: DimensionGauges (five separate 0–100 gauges; refuses to render an aggregate)

- **Source:** `GUI-cc-ghcp-requirements.md:725-725` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-19 | `DimensionGauges` (five separate 0–100 gauges; refuses to render an aggregate) | R9
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-19' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-19') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-19 | DimensionGauges (five separate 0–100 gauges; refuses to render an aggregate) | R9»
- [ ] DimensionGauges (five separate 0–100 gauges; refuses to render an aggregate)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-20 [P1] COMP-20: MiddleEllipsis (CSS + measured; full value in tooltip and copy)

- **Source:** `GUI-cc-ghcp-requirements.md:726-726` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-20 | `MiddleEllipsis` (CSS + measured; full value in tooltip and copy) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-20' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-20') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-20 | MiddleEllipsis (CSS + measured; full value in tooltip and copy)»
- [ ] MiddleEllipsis (CSS + measured; full value in tooltip and copy)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-21 [P1] COMP-21: OperatorMenu (WHY / WHY NOT / WHAT IF / WHAT CHANGED / WHEN / WHO / WHERE / HOW → mapped endpoints §3.3; disabled with reason when unavailable)

- **Source:** `GUI-cc-ghcp-requirements.md:727-727` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-21 | `OperatorMenu` (WHY / WHY NOT / WHAT IF / WHAT CHANGED / WHEN / WHO / WHERE / HOW → mapped endpoints §3.3; disabled with reason when unavailable) |
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-21' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-21') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-21 | OperatorMenu (WHY / WHY NOT / WHAT IF / WHAT CHANGED / WHEN / WHO / WHERE / HOW → mapped endpoints §3.3; disabled with reason when unavailable)»
- [ ] OperatorMenu (WHY / WHY NOT / WHAT IF / WHAT CHANGED / WHEN / WHO / WHERE / HOW → mapped endpoints §3.3; disabled with reason when unavailable)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-COMP-22 [P1] COMP-22: CapabilityGate (wraps any control; props `requires: {role?, backend?: 'INT-xxx' · 'BACKEND-MISSING-xxx', capability?}`; renders disabled + reason tooltip; never hides discoverable controls, hides only

- **Source:** `GUI-cc-ghcp-requirements.md:728-728` (table_row) · **Type:** Compliance · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
COMP-22 | `CapabilityGate` (wraps any control; props `requires: {role?, backend?: 'INT-xxx' | 'BACKEND-MISSING-xxx', capability?}`; renders disabled + reason tooltip; never hides discoverable controls, hides only undiscoverable objects) | R2/R3
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'COMP-22' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('COMP-22') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «COMP-22 | CapabilityGate (wraps any control; props `requires: {role?, backend?: 'INT-xxx' | 'BACKEND-MISSING-xxx', capability?}`; renders disabled + reason tooltip; never hides discoverable controls, hides only undiscoverable objects) | R2/R3»
- [ ] CapabilityGate (wraps any control; props `requires: {role?, backend?: 'INT-xxx'
- [ ] 'BACKEND-MISSING-xxx', capability?}`; renders disabled + reason tooltip; never hides discoverable controls, hides only undiscoverable objects)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-BE-029 [P1] GUI-BE-029: One-use WebSocket connection ticket (POST /api/v1/realtime/ticket → short-lived token usable only in the WS handshake)

- **Source:** `GUI-cc-ghcp-requirements.md:439-439` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GUI-BE-029` | One-use WebSocket connection ticket (`POST /api/v1/realtime/ticket` → short-lived token usable only in the WS handshake) | Poll `GET /api/v1/graph/events`; tray label `polling`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-BE-029' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-BE-029') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-BE-029 | One-use WebSocket connection ticket (POST /api/v1/realtime/ticket → short-lived token usable only in the WS handshake) | Poll GET /api/v1/graph/events; tray label polling»
- [ ] One-use WebSocket connection ticket (POST /api/v1/realtime/ticket → short-lived token usable only in the WS handshake)
- [ ] Poll GET /api/v1/graph/events; tray label polling
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-BE-033 [P1] GUI-BE-033: RateLimit-, ETag, Idempotency-Key

- **Source:** `GUI-cc-ghcp-requirements.md:443-443` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GUI-BE-033` | `RateLimit-*`, `ETag`, `Idempotency-Key` | §3.1 fallbacks
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-BE-033' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-BE-033') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-BE-033 | RateLimit-*, ETag, Idempotency-Key | §3.1 fallbacks»
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-001 [P1] GUI-SCR-001: A01 Given a valid local credential, when submitted, then POST /auth/login is called, the token is held in memory only (assert localStorage/sessionStorage/IndexedDB contain no token), and the user land

- **Source:** `GUI-cc-ghcp-requirements.md:824-830` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-001-A01` Given a valid local credential, when submitted, then `POST /auth/login` is called, the token is held in memory only (assert `localStorage`/`sessionStorage`/IndexedDB contain no token), and the user lands on Overview with tenant/workspace visible in the context bar.
  - `A02` Given an invalid credential, when submitted, then an inline error with correlation ID appears and no navigation occurs.
  - `A03` Given a tenant-bound token, when the scope step renders, then the tenant is pre-selected, locked, and switching to another tenant is impossible in the UI and returns 403 if forced via URL.
  - `A04` Given an unbound admin token and a tenant ID input, when an invalid ID is entered, then `GET /tenancy/context` 403 is shown inline.
  - `A05` Given an expiring token, when 2 minutes remain, then a warning is shown; when expired, then all in-flight requests abort, caches clear, and `/auth/expired` is shown with the return URL preserved.
  - `A06` Given sign-out, when confirmed, then token, Query cache, Dexie scoped caches and polling are cleared and the WS/poll loop stops.
  - `A07` Given `GET /health/ready` 503, when the page loads, then `Server not ready` with retry is shown and no login POST is attempted.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-001' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-001') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): A01 Given a valid local credential, when submitted, then POST /auth/login is called, the token is held in memory only (assert localStorage/sessionStorage/IndexedDB contain no token), and the user lands on Overview with tenant/workspace visible in the context bar. - A02 Given an invalid credential, when submitted, then an inline error with correlation ID appears and no navigatio
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-004 [P1] GUI-SCR-004: A01 Given a question, when submitted in Advanced mode, then suggestion cards render each with paraphrase, intent, depth/limit, estimated rows (from /query/cost when a plan exists; else Cost unknown), 

- **Source:** `GUI-cc-ghcp-requirements.md:917-923` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-004-A01` Given a question, when submitted in Advanced mode, then suggestion cards render each with paraphrase, intent, depth/limit, estimated rows (from `/query/cost` when a plan exists; else `Cost unknown`), confidence and a Preview that shows the exact `QueryPlan` JSON before any execution.
  - `A02` Given a deterministic result, when rendered, then the mode badge is `Deterministic`, the knowledge-age stamp is present, and every factual sentence has ≥ 1 citation chip resolving to a node/edge/evidence id present in the result (test asserts no orphan citations).
  - `A03` Given the local model is `ready`, when Narrate is on, then the first SSE delta renders before `[DONE]` (assert ≥ 2 paint frames between first and last chunk) and Stop aborts the fetch (assert request aborted and partial text retained with `Stopped` state).
  - `A04` Given the model is `unavailable`, when asked, then no `/brain/llm/*` request is made and the notice is shown.
  - `A05` Given `partial:true` with no nodes, when rendered, then `AbstainBadge` appears and no narration is requested.
  - `A06` Given a source snippet containing prompt-injection text, when displayed, then it renders as inert text inside an `Untrusted source content` frame and no tool/action is triggered.
  - `A07` Given Save, when the page reloads, then the answer, plan and manifest reappear from local storage with `Saved on this device` label.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-004' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-004') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): A01 Given a question, when submitted in Advanced mode, then suggestion cards render each with paraphrase, intent, depth/limit, estimated rows (from /query/cost when a plan exists; else Cost unknown), confidence and a Preview that shows the exact QueryPlan JSON before any execution. - A02 Given a deterministic result, when rendered, then the mode badge is Deterministic, the know
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-005 [P1] GUI-SCR-005: A01 Given a focus id in the URL, when loaded, then the entity and its 1-hop neighbourhood render, the entity is selected and the inspector shows it; refresh restores identical selection/camera (±1 px)

- **Source:** `GUI-cc-ghcp-requirements.md:945-951` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-005-A01` Given a `focus` id in the URL, when loaded, then the entity and its 1-hop neighbourhood render, the entity is selected and the inspector shows it; refresh restores identical selection/camera (±1 px).
  - `A02` Given a `partial:true` neighbourhood, when rendered, then the status strip and `ResultBanner` state partial and the warnings text.
  - `A03` Given 2 000 visible edges, when a layout runs, then the main thread never blocks > 50 ms (perf trace) because layout runs in the worker; cancelling via scope change discards the result.
  - `A04` Given a saved view, when the API restarts and the view is restored, then stale ids are reported (`3 entities no longer found`) rather than silently dropped.
  - `A05` Given the Table toggle, when pressed, then the same nodes/edges appear in `GraphTableView` with identical selection, and every toolbar action is available via the table's row/context menu.
  - `A06` Given an export (GraphML/GEXF/JSON-LD/CSV), when generated, then it parses with an independent parser in the test and preserves ids, direction, labels, properties, Unicode and fact class.
  - `A07` Given a cross-tenant saved-view import, when applied, then the ids are validated against the current scope and foreign ids are rejected with a count.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-005' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-005') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A03 Given 2 000 visible edges, when a layout runs, then the main thread never blocks > 50 ms (perf trace) because layout runs in the worker;
- [ ] A07 Given a cross-tenant saved-view import, when applied, then the ids are validated against the current scope and foreign ids are rejected with a count.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-03 [P1] GUI-VSC-03: Commands (existing names): Set Access Token, Context for Active File, Trace Requirement to Code, Explore Impact, Trace Provenance / Lineage, GraphRAG Retrieval, Search Knowledge Graph, Natural Languag

- **Source:** `GUI-cc-ghcp-requirements.md:1323-1323` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-03 | Commands (existing names): Set Access Token, Context for Active File, Trace Requirement to Code, Explore Impact, Trace Provenance / Lineage, GraphRAG Retrieval, Search Knowledge Graph, Natural Language Query (`POST /api/v1/query/nl`), Read-only MCP Tool; add quick actions `WHY`, `WHAT CHANGED`, `IMPACT`, `WHERE USED` mapped to §3.3 operators (G2-VSC-007)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-03' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-03') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-03 | Commands (existing names): Set Access Token, Context for Active File, Trace Requirement to Code, Explore Impact, Trace Provenance / Lineage, GraphRAG Retrieval, Search Knowledge Graph, Natural Language Query (POST /api/v1/query/nl), Read-only MCP Tool; add quick actions WHY, WHAT CHANGED, IMPACT, WHERE USED mapped to §3.3 operators (G2-VSC-007)»
- [ ] Commands (existing names): Set Access Token, Context for Active File, Trace Requirement to Code, Explore Impact, Trace Provenance / Lineage, GraphRAG Retrieval, Search Knowledge Graph, Natural Language Query (POST /api/v1/query/nl), Read-only MCP Tool; add quick actions WHY, WHAT CHANGED, IMPACT, WHERE USED mapped to §3.3 operators (G2-VSC-007)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-04 [P1] GUI-VSC-04: Webview results: same tokens (VS Code theme-aware CSS variables mapped to §5.2 semantics), mode badge, knowledge-age stamp, evidence list with Open source range actions constrained to eoip.repositoryR

- **Source:** `GUI-cc-ghcp-requirements.md:1324-1324` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-04 | Webview results: same tokens (VS Code theme-aware CSS variables mapped to §5.2 semantics), mode badge, knowledge-age stamp, evidence list with `Open source range` actions constrained to `eoip.repositoryRoot` (reject absolute/traversal/symlink); CSP `default-src 'none'` with nonce
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-04 | Webview results: same tokens (VS Code theme-aware CSS variables mapped to §5.2 semantics), mode badge, knowledge-age stamp, evidence list with Open source range actions constrained to eoip.repositoryRoot (reject absolute/traversal/symlink); CSP default-src 'none' with nonce»
- [ ] Webview results: same tokens (VS Code theme-aware CSS variables mapped to §5.2 semantics), mode badge, knowledge-age stamp, evidence list with Open source range actions constrained to eoip.repositoryRoot (reject absolute/traversal/symlink); CSP default-src 'none' with nonce
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-07 [P1] JRN-07: Ontology draft → validate → diff/impact → review → publish → rollback

- **Source:** `GUI-cc-ghcp-requirements.md:118-118` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-07 | Ontology draft → validate → diff/impact → review → publish → rollback | SCR-012, 013
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-07 | Ontology draft → validate → diff/impact → review → publish → rollback | SCR-012, 013»
- [ ] Ontology draft → validate → diff/impact → review → publish → rollback
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-10 [P1] JRN-10: Query validate/explain/run → cancel/timeout → save template → paged/exported result

- **Source:** `GUI-cc-ghcp-requirements.md:121-121` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-10 | Query validate/explain/run → cancel/timeout → save template → paged/exported result | SCR-011
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-10' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-10') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-10 | Query validate/explain/run → cancel/timeout → save template → paged/exported result | SCR-011»
- [ ] Query validate/explain/run → cancel/timeout → save template → paged/exported result
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-14 [P1] JRN-14: Governance policy edit (replace) → evaluate → denied egress → revoke token

- **Source:** `GUI-cc-ghcp-requirements.md:125-125` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-14 | Governance policy edit (replace) → evaluate → denied egress → revoke token | SCR-021
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-14' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-14') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-14 | Governance policy edit (replace) → evaluate → denied egress → revoke token | SCR-021»
- [ ] Governance policy edit (replace) → evaluate → denied egress → revoke token
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-15 [P1] JRN-15: Tenant quotas/placement → suspend/resume → backup/restore view

- **Source:** `GUI-cc-ghcp-requirements.md:126-126` (table_row) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-15 | Tenant quotas/placement → suspend/resume → backup/restore view | SCR-022
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-15' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-15') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-15 | Tenant quotas/placement → suspend/resume → backup/restore view | SCR-022»
- [ ] Tenant quotas/placement → suspend/resume → backup/restore view
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-16 [P1] JRN-16: Brand draft → contrast failure → fix → preview all 4 themes → publish → rollback (publish blocked until BACKEND-MISSING-018)

- **Source:** `GUI-cc-ghcp-requirements.md:127-127` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-16 | Brand draft → contrast failure → fix → preview all 4 themes → publish → rollback (publish blocked until `BACKEND-MISSING-018`) | SCR-023
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-16' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-16') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-16 | Brand draft → contrast failure → fix → preview all 4 themes → publish → rollback (publish blocked until BACKEND-MISSING-018) | SCR-023»
- [ ] Brand draft → contrast failure → fix → preview all 4 themes → publish → rollback (publish blocked until BACKEND-MISSING-018)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-BE-030 [P2] GUI-BE-030: Saved graph views server CRUD (BACKEND-MISSING-004 broadened to list/get/update/delete/share)

- **Source:** `GUI-cc-ghcp-requirements.md:440-440` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GUI-BE-030` | Saved graph views server CRUD (`BACKEND-MISSING-004` broadened to list/get/update/delete/share) | Store views in Dexie namespaced `{principal, tenant, workspace, schema_version}` with export/import JSON; label `Saved locally on this device`
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-BE-030' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-BE-030') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-BE-030 | Saved graph views server CRUD (BACKEND-MISSING-004 broadened to list/get/update/delete/share) | Store views in Dexie namespaced {principal, tenant, workspace, schema_version} with export/import JSON; label Saved locally on this device»
- [ ] Saved graph views server CRUD (BACKEND-MISSING-004 broadened to list/get/update/delete/share)
- [ ] Store views in Dexie namespaced {principal, tenant, workspace, schema_version} with export/import JSON; label Saved locally on this device
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-BE-031 [P2] GUI-BE-031: Entity 360 aggregate (BACKEND-MISSING-006)

- **Source:** `GUI-cc-ghcp-requirements.md:441-441` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GUI-BE-031` | Entity 360 aggregate (`BACKEND-MISSING-006`) | Compose client-side from `GET /entities/{id}` + `/neighborhood` + `/lineage` + `/enterprise/diff/timeline/{id}` + `/graph/metrics` + `/identity/candidates`, each section independently loadable and failable
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-BE-031' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-BE-031') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-BE-031 | Entity 360 aggregate (BACKEND-MISSING-006) | Compose client-side from GET /entities/{id} + /neighborhood + /lineage + /enterprise/diff/timeline/{id} + /graph/metrics + /identity/candidates, each section independently loadable and failable»
- [ ] Entity 360 aggregate (BACKEND-MISSING-006)
- [ ] Compose client-side from GET /entities/{id} + /neighborhood + /lineage + /enterprise/diff/timeline/{id} + /graph/metrics + /identity/candidates, each section independently loadable and failable
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-BE-032 [P2] GUI-BE-032: Cursor pagination on list endpoints

- **Source:** `GUI-cc-ghcp-requirements.md:442-442` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
`GUI-BE-032` | Cursor pagination on list endpoints | Use `limit` with "server cap" notice; never fabricate totals
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-BE-032' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-BE-032') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-BE-032 | Cursor pagination on list endpoints | Use limit with "server cap" notice; never fabricate totals»
- [ ] Cursor pagination on list endpoints
- [ ] Use limit with "server cap" notice; never fabricate totals
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-003 [P2] GUI-SCR-003: A01 Given /admin/system fails, when Overview renders, then the Health card shows an error with correlation ID while other cards render data

- **Source:** `GUI-cc-ghcp-requirements.md:877-881` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-003-A01` Given `/admin/system` fails, when Overview renders, then the Health card shows an error with correlation ID while other cards render data.
  - `A02` Given a non-admin principal, when Overview renders, then no `/admin/*` request is issued and admin-only cards are absent (not errored).
  - `A03` Given two tenants with different graphs, when switching scope, then all tiles update and no stale value from the previous tenant is visible at any frame (snapshot after switch shows skeletons then new values).
  - `A04` Given the jobs list contains a `HELD` job, when its chip is clicked, then SCR-017 opens pre-filtered and the row is focused.
  - `A05` Given validation summary has `0` findings, then the card reads `0 findings in last run (as of …)`; given no run exists, then `No validation run yet`.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-003' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-003') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Statement holds (verbatim requirement is the criterion): A01 Given /admin/system fails, when Overview renders, then the Health card shows an error with correlation ID while other cards render data. - A02 Given a non-admin principal, when Overview renders, then no /admin/* request is issued and admin-only cards are absent (not errored). - A03 Given two tenants with different graphs, when switching scope, then all tiles update and no s
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-006 [P2] GUI-SCR-006: A01 Given a valid id, when opened, then header, Overview and Relationships render from GET /entities/{id}; a failing Impact call shows an error only inside the Impact tab

- **Source:** `GUI-cc-ghcp-requirements.md:977-982` (list_item) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-006-A01` Given a valid id, when opened, then header, Overview and Relationships render from `GET /entities/{id}`; a failing Impact call shows an error only inside the Impact tab.
  - `A02` Given `deleted_at` set and `include_deleted=false`, when opened, then 404 is shown with a `Show deleted` action that retries with `include_deleted=true` and renders the tombstone banner.
  - `A03` Given 300 outgoing edges, when Relationships renders, then groups are virtualized and counts are exact to the response; `Load more` calls neighborhood with explicit limit and shows server cap.
  - `A04` Given the Delete action, when the typed id mismatches, then Confirm is disabled; when it matches and the server returns `DELETED`, then the page re-fetches and shows the tombstone.
  - `A05` Given navigation Graph → Entity → back, when returning, then the graph camera/selection/filters are unchanged (store snapshot restored).
  - `A06` Given a masked/absent property, when rendered, then `Not provided` vs `Masked` are distinguished by the server response shape (absent key vs masked marker), never guessed.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-006' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-006') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A06 Given a masked/absent property, when rendered, then Not provided vs Masked are distinguished by the server response shape (absent key vs masked marker), never guessed.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-SCR-007 [P2] GUI-SCR-007: A01 Given anchor and depth 4, when Run, then rings = bydepth keys, totals equal totalaffected, and risk badge equals risk

- **Source:** `GUI-cc-ghcp-requirements.md:993-998` (list_item) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
- `GUI-SCR-007-A01` Given anchor and depth 4, when Run, then rings = `by_depth` keys, totals equal `total_affected`, and risk badge equals `risk`.
  - `A02` Given a result with cycles/truncation (`partial:true`), when rendered, then the banner shows and ring counts are labelled `≥`.
  - `A03` Given an affected node selected, when the inspector opens, then it lists ≥ 1 supporting path from `paths[]` with edge classes and evidence counts.
  - `A04` Given Scenario mode, when run, then no mutation endpoint is called (network assertion) and the banner is visible.
  - `A05` Given Export checklist, when generated, then the CSV contains one row per affected entity with depth/risk/owner/tests and the header stamp.
  - `A06` Given Cancel during a long run, when pressed, then the request aborts and the previous result stays visible with `Cancelled` state.
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-SCR-007' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-SCR-007') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] A03 Given an affected node selected, when the inspector opens, then it lists ≥ 1 supporting path from paths[] with edge classes and evidence counts.
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-01 [P2] GUI-VSC-01: Sidebar EOIP Context TreeView: sections Current symbol (name, kind, range), Related entities grouped by label (icons from the same registry rendered as codicons mapping table), Relationships, Provenan

- **Source:** `GUI-cc-ghcp-requirements.md:1321-1321` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-01 | Sidebar `EOIP Context` TreeView: sections Current symbol (name, kind, range), Related entities grouped by label (icons from the same registry rendered as codicons mapping table), Relationships, Provenance, Evidence; each item has a tooltip with canonical id and fact class; unresolved → `Not indexed` item (never empty tree without explanation)
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-01 | Sidebar EOIP Context TreeView: sections Current symbol (name, kind, range), Related entities grouped by label (icons from the same registry rendered as codicons mapping table), Relationships, Provenance, Evidence; each item has a tooltip with canonical id and fact class; unresolved → Not indexed item (never empty tree without explanation)»
- [ ] Sidebar EOIP Context TreeView: sections Current symbol (name, kind, range), Related entities grouped by label (icons from the same registry rendered as codicons mapping table), Relationships, Provenance, Evidence; each item has a tooltip with canonical id and fact class; unresolved → Not indexed item (never empty tree without explanation)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-05 [P2] GUI-VSC-05: Failure to reach EOIP never blocks editing; last successful context retained with as of stamp

- **Source:** `GUI-cc-ghcp-requirements.md:1325-1325` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-05 | Failure to reach EOIP never blocks editing; last successful context retained with `as of` stamp
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-05 | Failure to reach EOIP never blocks editing; last successful context retained with as of stamp»
- [ ] Failure to reach EOIP never blocks editing; last successful context retained with as of stamp
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-06 [P2] GUI-VSC-06: No write/admin tools; MCP tool list filtered to read-only; hidden chain-of-thought never shown

- **Source:** `GUI-cc-ghcp-requirements.md:1326-1326` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-06 | No write/admin tools; MCP tool list filtered to read-only; hidden chain-of-thought never shown
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-06 | No write/admin tools; MCP tool list filtered to read-only; hidden chain-of-thought never shown»
- [ ] No write/admin tools; MCP tool list filtered to read-only; hidden chain-of-thought never shown
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-GUI-VSC-07 [P2] GUI-VSC-07: Extension host tests per command against the real API (fixture repo), plus offline test

- **Source:** `GUI-cc-ghcp-requirements.md:1327-1327` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
GUI-VSC-07 | Extension host tests per command against the real API (fixture repo), plus offline test
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'GUI-VSC-07' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('GUI-VSC-07') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «GUI-VSC-07 | Extension host tests per command against the real API (fixture repo), plus offline test»
- [ ] Extension host tests per command against the real API (fixture repo), plus offline test
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-01 [P2] JRN-01: Sign in → choose tenant/workspace → deep-link refresh → switch scope → sign out

- **Source:** `GUI-cc-ghcp-requirements.md:112-112` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-01 | Sign in → choose tenant/workspace → deep-link refresh → switch scope → sign out | SCR-001, shell
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-01' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-01') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-01 | Sign in → choose tenant/workspace → deep-link refresh → switch scope → sign out | SCR-001, shell»
- [ ] Sign in → choose tenant/workspace → deep-link refresh → switch scope → sign out
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-02 [P2] JRN-02: Connect source → test → baseline/ingest → review inferred graph (dry-run) → publish → first question

- **Source:** `GUI-cc-ghcp-requirements.md:113-113` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-02 | Connect source → test → baseline/ingest → review inferred graph (dry-run) → publish → first question | SCR-002, 014, 015, 017, 004
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-02' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-02') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-02 | Connect source → test → baseline/ingest → review inferred graph (dry-run) → publish → first question | SCR-002, 014, 015, 017, 004»
- [ ] Connect source → test → baseline/ingest → review inferred graph (dry-run) → publish → first question
- [ ] SCR-002, 014, 015, 017, 004
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-04 [P2] JRN-04: Ask → suggestion cards (QueryPlan preview + cost) → run → streamed/narrated answer → hover citations → stop/regenerate → save/report

- **Source:** `GUI-cc-ghcp-requirements.md:115-115` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-04 | Ask → suggestion cards (QueryPlan preview + cost) → run → streamed/narrated answer → hover citations → stop/regenerate → save/report | SCR-004, 019
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-04' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-04') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-04 | Ask → suggestion cards (QueryPlan preview + cost) → run → streamed/narrated answer → hover citations → stop/regenerate → save/report | SCR-004, 019»
- [ ] Ask → suggestion cards (QueryPlan preview + cost) → run → streamed/narrated answer → hover citations → stop/regenerate → save/report
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-05 [P2] JRN-05: Select entity → blast radius (hop/severity) → paths → owners/tests checklist → export plan

- **Source:** `GUI-cc-ghcp-requirements.md:116-116` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-05 | Select entity → blast radius (hop/severity) → paths → owners/tests checklist → export plan | SCR-007
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-05' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-05') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-05 | Select entity → blast radius (hop/severity) → paths → owners/tests checklist → export plan | SCR-007»
- [ ] Select entity → blast radius (hop/severity) → paths → owners/tests checklist → export plan
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-06 [P2] JRN-06: Incident → ranked hypotheses → evidence traversal → record finding

- **Source:** `GUI-cc-ghcp-requirements.md:117-117` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-06 | Incident → ranked hypotheses → evidence traversal → record finding | SCR-009
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-06' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-06') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-06 | Incident → ranked hypotheses → evidence traversal → record finding | SCR-009»
- [ ] Incident → ranked hypotheses → evidence traversal → record finding
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-08 [P2] JRN-08: Upload (interrupted) → resume → mapping conflict → job retry → verified graph

- **Source:** `GUI-cc-ghcp-requirements.md:119-119` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-08 | Upload (interrupted) → resume → mapping conflict → job retry → verified graph | SCR-015, 017
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-08' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-08') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-08 | Upload (interrupted) → resume → mapping conflict → job retry → verified graph | SCR-015, 017»
- [ ] Upload (interrupted) → resume → mapping conflict → job retry → verified graph
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-09 [P2] JRN-09: Duplicate candidates → compare → decide (accept/reject) → undo/revert where supported

- **Source:** `GUI-cc-ghcp-requirements.md:120-120` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-09 | Duplicate candidates → compare → decide (accept/reject) → undo/revert where supported | SCR-016, 006
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-09' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-09') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-09 | Duplicate candidates → compare → decide (accept/reject) → undo/revert where supported | SCR-016, 006»
- [ ] Duplicate candidates → compare → decide (accept/reject) → undo/revert where supported
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-11 [P2] JRN-11: Agent run → scoped approval → denied/replayed action → audited result

- **Source:** `GUI-cc-ghcp-requirements.md:122-122` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-11 | Agent run → scoped approval → denied/replayed action → audited result | SCR-018
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-11' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-11') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-11 | Agent run → scoped approval → denied/replayed action → audited result | SCR-018»
- [ ] Agent run → scoped approval → denied/replayed action → audited result
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-12 [P2] JRN-12: Report template → params → render → schedule → download/revoke

- **Source:** `GUI-cc-ghcp-requirements.md:123-123` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-12 | Report template → params → render → schedule → download/revoke | SCR-019
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-12' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-12') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-12 | Report template → params → render → schedule → download/revoke | SCR-019»
- [ ] Report template → params → render → schedule → download/revoke
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-13 [P2] JRN-13: Two browsers → presence/comments → disconnect/rejoin → membership revoked (blocked until BACKEND-MISSING-016)

- **Source:** `GUI-cc-ghcp-requirements.md:124-124` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-13 | Two browsers → presence/comments → disconnect/rejoin → membership revoked (blocked until `BACKEND-MISSING-016`) | SCR-020
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-13' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-13') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-13 | Two browsers → presence/comments → disconnect/rejoin → membership revoked (blocked until BACKEND-MISSING-016) | SCR-020»
- [ ] Two browsers → presence/comments → disconnect/rejoin → membership revoked (blocked until BACKEND-MISSING-016)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-17 [P2] JRN-17: Settings (theme/density/locale/motion) → notifications → help → about/licences

- **Source:** `GUI-cc-ghcp-requirements.md:128-128` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-17 | Settings (theme/density/locale/motion) → notifications → help → about/licences | SCR-025, 026
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-17' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-17') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-17 | Settings (theme/density/locale/motion) → notifications → help → about/licences | SCR-025, 026»
- [ ] Settings (theme/density/locale/motion) → notifications → help → about/licences
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']

## RT-JRN-18 [P2] JRN-18: Induced 401/403/404/offline/version-mismatch/chunk-failure → safe recovery with retained draft

- **Source:** `GUI-cc-ghcp-requirements.md:129-129` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Not Verified / L0 (tests passed 0, failed 0)
- **Gaps:** No code, test or infra reference to the ID anywhere; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04 · **Effort:** 6.0 h (M, low confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
JRN-18 | Induced 401/403/404/offline/version-mismatch/chunk-failure → safe recovery with retained draft | SCR-027
```
</details>

**Next steps**
1. Discovery: search for an implementation under another name: git grep -n -w 'JRN-18' -- packages apps reva scripts tests deploy; then search by key terms from the requirement text
2. If an implementation exists: add a trace (pytest.mark.req('JRN-18') on tests; ID in docstring of the implementing module) and a test per acceptance criterion
3. If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently
4. If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «JRN-18 | Induced 401/403/404/offline/version-mismatch/chunk-failure → safe recovery with retained draft | SCR-027»
- [ ] Induced 401/403/404/offline/version-mismatch/chunk-failure → safe recovery with retained draft
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Proof plan (1.1):** have nothing; needs ['L2', 'L3 (same commit) or L4']; missing ['L2', 'L3 (same commit) or L4']


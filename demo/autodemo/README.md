# EOIP client demonstrations

Double-click the respective Windows launcher. It starts the repository Docker
stack with bounded health checks, authenticates privately, opens a visible Chrome
browser and presents user-paced steps in the application and a separate
live-results window. The console remains open at the end, including on failure.
No in-memory fixture runner is used as evidence for the live application.

| Launcher | Sequence |
|---|---|
| `run-demo.bat` | Enterprise application, administration/manual ingestion, administration/pipeline ingestion, then separate VS Code NLQ/MCP |
| `run-demo-manual.bat` | Enterprise application plus live manual JSON ingestion and administration |
| `run-demo-pipeline.bat` | Enterprise application plus live pipeline-fixture JSON ingestion and administration |
| `run-demo-admin.bat` | Separate administration, manual ingestion, format exports and governance |
| `run-demo-vscode.bat` | Separate isolated VS Code extension demonstration |
| `run-demo-hubble.bat` | Additive corpus loading and 13 named, color-coded live Hubble graph scenarios |

## Prerequisites and safe operation

- Node.js (22+), Docker Desktop running, and dependencies installed for the web
  application and VS Code extension using their existing package managers.
- Google Chrome installed. `PLAYWRIGHT_CHANNEL` or
  `PLAYWRIGHT_EXECUTABLE_PATH` can select another already-installed browser.
  The launcher does not silently install dependencies or browser binaries.
- `EOIP_API_TOKEN` in the process environment or `deploy/.env`. Tokens are never
  printed or put in demo receipts. Use a **dedicated local demo deployment**:
  ingestion writes demo entities and captures to the configured persistent store.
- All enterprise scenarios must be ready in the live scenario catalog. The
  existing Docker bootstrap seeds them when `EOIP_LOAD_DEMO=true`. If an older
  local environment disabled seeding, explicitly enable it in `deploy/.env`
  and restart the stack. There is no fixture fallback on missing live data.
- The extension demo uses the updated **0.1.0 source extension** in an isolated
  VS Code host, not an assertion that an older installed VSIX is updated.
  Cached VS Code and the extension's test-electron dependency are required.

No reset, restore, arbitrary deletion, arbitrary DLQ replay, cancellation, proposal
approval, external connector credential acquisition or production mutation is
automated. These require a separately approved, disposable scenario.
The expanded application demo creates isolated synthetic truth claims, taxonomy
concepts and a persisted knowledge product. It deletes only the query template
created by that run, including on a failed template step.

## Visible sequences and coverage boundaries

The application walks all ready Northstar Commerce stories: business intent to
runtime, incident correlation, API blast radius, release governance, test
intelligence, design to delivery, knowledge provenance, graph analytics,
business objectives/capabilities, decision trade-offs, process deviations,
failed qualification gates and verified permanent remediation.
Each story executes its declared path through the real UI and asserts the
returned endpoints, then runs impact, lineage, neighborhood and traceability
requests against the live API. Empty graph results fail.
Cross-domain paths explicitly select the scenario corpus's ontology relationship
labels through the policy-validated path request. The default traversal allowlist
for other clients is unchanged. Startup checks authenticated schema access, not
merely the HugeGraph metadata/version endpoint.

The separate Hubble launcher uses the normal persistent Docker deployment and
opens `http://localhost:8088/enterprise.html?tour=1` in the default browser.
It queries Hubble's saved connection for real vertices and edges, then advances
every 15 seconds. Use Stop walkthrough for manual exploration. Named seed search,
domain colors, directional relationship labels, node/edge provenance and
inspectable Gremlin expose the same Northstar entities as the application.
This sequence has no fixture-rendering fallback and does not delete volumes.

It also demonstrates NLQ with nonempty graph results, navigation through seven
explorer lenses and ten KGR graph views, every advertised RAG routing pattern
and agent-routing type, eight engineering disciplines, and graph analytics
(blast radius, reverse impact, centrality, communities, similarity, k-core,
components, degree distribution, non-mutating what-if, anomalies, link
prediction and surprises). Results are shown as real API JSON, not fabricated
browser responses. **Routing is not model inference**. UI navigation is
explicitly distinguished from executing every control in a view.
RAG steps display the actual delegated execution pattern, evidence manifest and
abstention decision; a corrective/adaptive route may legitimately execute a
simple/hybrid stage. An explicit, reasoned abstention is shown as such, not as a
generated answer.
Agent steps likewise show the requested type separately from the executed
implementation and validate its answer, category, confidence, actions and
reasoning. Many advertised types are aliases or supervisor delegations to
shared implementations; this is not a demonstration of distinct autonomous
behavior for each catalog entry.

Additional multi-step journeys execute local federation planning, conflicting
truth claims with authority resolution and read-back explanations, query-template
binding/explanation/cost, faceted search, keyword retrieval evidence, graph
assertions with an explicitly expected read-only violation, synthetic SKOS
scheme/concept mapping and validation, and a Draft-to-Certified knowledge-product
lifecycle with persisted read-back and lineage. EOQL and OSQL expose the same
identified enterprise data and ontology. Truth/SKOS state is process-local and
does not survive API restart or appear in Hubble. Products are persisted, but
their source/consumer lineage entries are properties, not graph relationship
edges. `Certified` is an application lifecycle state, not external certification.
Federation uses local adapters; query cost is an estimate, not measured latency.

The separate administration sequence demonstrates source/job inspection,
validation, ontology schema, JSON-LD context, audit and DLQ inspection; real
single-file and batch ingestion of 13 JSON source fixtures; all eight graph
export formats; knowledge-firewall inspection; an evidence manifest; and
governance/health catalogs. The Meridian PAY/FRD ingestion fixtures are separate
from the Northstar scenario corpus. Pipeline mode ingests its pipeline JSON
fixtures; it does not claim to run authenticated upstream polling/webhooks.

Each browser receipt inventories **every operation in the live OpenAPI schema**
as `DEMONSTRATED` or `NOT_DEMONSTRATED`. The latter remain visible at the end
and are **not counted as completed**. Planned lenses, destructive recovery,
stateful simulation/proposal lifecycles, every KGR control, external connectors,
binary file-format samples/OCR/optional converters and model inference still
require dedicated scenarios and prerequisites. Consequently the receipt is
`PARTIAL` when those operations remain; successful selected steps do not certify
the user's entire application-wide acceptance criterion.

## Running and pacing

```powershell
.\demo\autodemo\run-demo.bat
.\demo\autodemo\run-demo-admin.bat --delay 5000
.\demo\autodemo\run-demo-pipeline.bat --delay 1000 --no-pause
.\demo\autodemo\run-demo.bat --dry-run
node .\demo\autodemo\application-demo.js --headless --delay 0 --no-pause
node .\demo\autodemo\administration-demo.js --dataset pipelines --headless --delay 0 --no-pause
node --test .\demo\autodemo\tests\*.test.js
```

Direct JavaScript commands use an already-running stack. Default pacing waits
for **Next Step**, Enter, Space or ArrowRight. `--headless` is for
validation, not client presentations. `--no-pause` advances automatically using
`--delay` (default 2.5 seconds) and suppresses the launcher's
final console pause. `--dry-run` does not start services, access secrets, open
windows, ingest data or write receipts. `--help` documents supported arguments.
Legacy `--data-dir` / administration `--skip-ingest` are deliberately rejected:
captures now use the service configuration, and ingestion is part of this demo.

Receipts are unique JSON files under `test-results`. `--output FILE` sets the
browser receipt path; full mode writes numbered phase files to avoid overwrites.
The extension writes its own receipt. Failures retain completed/failed step
counts and a redacted error, exit nonzero, close automation-owned browsers and
stop the remaining sequence. Docker services remain running for manual review.
Exit zero means selected sequences executed, **not** universal feature coverage.

The historical Python `runner.py` and `admin_runner.py` are not invoked by these
launchers. The former remains a fixture test utility, not live ingestion.
The latter is a legacy console helper, not the supported administration demo.

## Validation strategy

Existing UI tests are retained without rewriting their journeys. New Node
tests cover argument validation, dry-run isolation, strict path/graph assertions,
launcher failure propagation and honest operation coverage; the existing
Windows validation workflow runs them. Live acceptance runs the same browser
scripts with zero delay against Docker services and validates all selected
steps. There are no intercepted responses in the demonstration.

Manual review: launch headful with default pacing; verify both windows are
readable, each story appears in order, administration is visibly separate,
the console remains open, and full mode transitions to isolated VS Code with
NLQ/MCP results. Check the final receipts' uncovered-operation lists rather
than inferring complete coverage from a successful console exit.

"""Generate the Pass-9 SR status table rows (290 SR IDs) -> .tmp/sr_table.json."""
import json
import re
from collections import Counter

texts = json.load(open('.tmp/sr_texts.json', encoding='utf-8'))
ids = sorted(texts)

T = 'tests/unit/test_sr_wave_api_routes.py'
EV = {
    'tenancy': ('packages/eoip/tenancy/', 'tests/unit/test_tenancy.py'),
    'licensing': ('packages/eoip/licensing/', 'tests/unit/test_licensing.py'),
    'config': ('packages/eoip/config/', 'tests/unit/test_layered_config.py'),
    'egress': ('packages/eoip/egress/', 'tests/unit/test_egress_gateway.py'),
    'branding': ('packages/eoip/branding/', 'tests/unit/test_branding.py'),
    'privacy': ('packages/eoip/privacy/', 'tests/unit/test_privacy.py'),
    'compliance': ('packages/eoip/compliance/', 'tests/unit/test_compliance_packs.py'),
    'reports': ('packages/eoip/reports/', 'tests/unit/test_reports.py'),
    'qa': ('packages/eoip/qa/', 'tests/unit/test_qa_gate_integrity.py'),
    'suggest': ('packages/eoip/suggest/', 'tests/unit/test_suggestion_engine.py'),
    'ingestprof': ('packages/eoip/ingest/profile.py', 'tests/unit/test_schema_profiler.py'),
    'packs': ('packages/eoip/marketplace/ + config/domain-packs/',
              'tests/unit/test_marketplace.py + test_domain_packs*.py'),
}


def done(key, note=''):
    pkg, tst = EV[key]
    return ('Done-behavioral', pkg + '; ' + tst + '; ' + T, note)


def exists(ev, note=''):
    return ('Exists', ev, note)


def partial(ev, note=''):
    return ('Exists-partial', ev, note)


def ext(note):
    return ('External gate', '', note)


def adr(note):
    return ('ADR-gated', '', note)


C = {}
# --- implemented this pass ---
for i in ('001', '002', '003', '006', '007', '009'):
    C['SR-TEN-' + i] = done('tenancy')
C['SR-DEP-007'] = done('licensing')
C['SR-COM-001'] = done('licensing')
for i in ('001', '002', '003', '004', '005', '006'):
    C['SR-CFG-' + i] = done('config')
for i in range(10, 21):
    C['SR-LLM-%03d' % i] = done('egress')
C['SR-LLM-018'] = partial(
    EV['egress'][0],
    'gateway covers model egress; embedding/OCR/speech routing is per-endpoint, not enforced for all pipeline stages')
C['SR-CON-010'] = done('egress')
C['SR-CON-011'] = done('egress')
for i in ('001', '003', '006', '007'):
    C['SR-WL-' + i] = done('branding')
C['SR-WL-002'] = partial('packages/eoip/branding/ (identity) + deploy/nginx',
                         'branded login/identity content exists; custom CNAME/TLS automation needs ingress infra')
C['SR-WL-005'] = ext('OEM re-signed appliance images deferred (build pipeline)')
C['SR-WL-008'] = adr('partner console needs fleet-management design decision')
C['SR-WL-009'] = adr('embeddable iframe/web-component widgets need an embedding-auth design decision')
C['SR-WL-004'] = partial(
    EV['branding'][0] + '; packages/eoip/branding/devendoring.py',
    'devendoring helpers exist; full vendor-identifier sweep (image/binary names) remains')
C['SR-ONT-007'] = done('branding')
for i in ('001', '002', '003', '004'):
    C['SR-PRV-' + i] = done('privacy')
C['SR-PRV-006'] = partial(
    EV['privacy'][0],
    'residency validator + egress region pinning exist; storage-region pinning is policy-checked, not backend-enforced')
for i in ('001', '002', '003', '004', '005'):
    C['SR-GOV-' + i] = done('compliance')
C['SR-NLQ-008'] = done('reports', 'HTML/MD/JSON in-product; PDF/DOCX/PPTX export is an External gate')
for i in ('010', '011', '012', '013', '014'):
    C['SR-QA-' + i] = done('qa')
C['SR-NLQ-002'] = done('suggest')
C['SR-NLQ-003'] = done('suggest')
C['SR-NLQ-004'] = partial(
    EV['suggest'][0],
    'deterministic mode is behavioral; narrated/exploratory LLM modes are External-gate (local LLM adapter)')
C['SR-ING-010'] = done('ingestprof')
C['SR-ING-012'] = done('ingestprof')
C['SR-ING-013'] = done('ingestprof')
C['SR-ING-016'] = done('ingestprof',
                       'edge-class honesty hook in profiler; ASSERTED/DERIVED classes predate this pass')
C['SR-COM-020'] = done('packs')
C['SR-COM-021'] = done('packs')

# --- AGT ---
C['SR-AGT-001'] = exists('packages/eoip/contracts/agent.py')
C['SR-AGT-002'] = exists('packages/eoip/agents/runtime.py')
C['SR-AGT-003'] = partial('packages/eoip/agents/governed.py',
                          'HITL approval flow exists; HOTL/HIC monitoring modes partial')
C['SR-AGT-004'] = exists('packages/eoip/agents/runtime.py (READ_TOOLS enforcement)')
C['SR-AGT-005'] = exists('apps/mcp/ (read-only MCP server)')
C['SR-AGT-006'] = exists('packages/eoip/agents/memory.py')
C['SR-AGT-007'] = partial('packages/eoip/marketplace/',
                          'signed packages + installer exist; agent certification workflow partial')
C['SR-AGT-008'] = exists('packages/eoip/agents/orchestration.py')
C['SR-AGT-009'] = exists('packages/eoip/agents/proposals.py (PROPOSE_ONLY)')
C['SR-AGT-010'] = exists('packages/eoip/agents/ catalog (20+ agents)')
C['SR-AGT-011'] = ext('RPA/workflow outbound hooks (tickets, PR comments) deferred - needs target-system contracts')
C['SR-AGT-020'] = partial('packages/eoip/connectors/ (poll/webhook)',
                          'watch-an-entity push UX partial')
C['SR-AGT-021'] = exists('packages/eoip/graph/conformance.py + knowledge_debt.py')
C['SR-AGT-022'] = exists('packages/eoip/graph/expertise.py freshness_report')
C['SR-AGT-023'] = exists('packages/eoip/graph/knowledge_debt.py')
C['SR-AGT-024'] = exists('packages/eoip/graph/expertise.py find_experts')
C['SR-AGT-025'] = partial('blast radius + incident correlation',
                          'fragility x coverage composite risk score partial')
C['SR-AGT-026'] = exists('packages/eoip/graph/anomaly.py')
C['SR-AGT-027'] = adr('scheduled personalized digest generation needs a scheduler + template decision')
C['SR-AGT-028'] = adr('auto-generated onboarding tours need UX/ADR decision')
C['SR-AGT-029'] = partial('packages/eoip/graph/simulation.py',
                          'simulation workspace exists; full digital-twin scenario planning partial')

# --- ARC ---
C['SR-ARC-001'] = exists('packages/eoip/* modular monolith')
C['SR-ARC-002'] = exists('packages/eoip/graph/backends.py + adapters')
C['SR-ARC-003'] = partial('packages/eoip/events/',
                          'embedded append-only log exists; NATS/Kafka adapters ADR-gated')
C['SR-ARC-004'] = exists('schemas/ (versioned contract registry)')
C['SR-ARC-005'] = partial('deploy/helm + apps/worker',
                          'stateless tiers deployable; horizontal-scale validation is External (cluster)')
C['SR-ARC-006'] = adr('consistency-model conformance needs clustered-backend certification')
C['SR-ARC-007'] = partial('idempotent upserts + deterministic IDs',
                          'replay-safe mutation proofs partial')
C['SR-ARC-008'] = exists('packages/eoip/graph/bitemporal.py')
C['SR-ARC-009'] = exists('packages/eoip/federation/')
C['SR-ARC-010'] = adr('WASM/container sandboxed extension runtime not selected yet')
C['SR-ARC-011'] = exists('packages/eoip/gaps/g2_architecture.py (CI guardrails)')
C['SR-ARC-012'] = exists('docs/adr-001-*.md + ADR process')

# --- COM ---
C['SR-COM-002'] = partial('demo/ + examples/eval + licensing evaluation model',
                          'demo datasets + eval license exist; ROI calculator/sizing tool are sales tooling (External)')
C['SR-COM-003'] = partial('packages/eoip/branding/content.py (legal registry)',
                          'legal content hosting exists; full procurement kit (MSA/DPA/BAA templates) is commercial tooling')
C['SR-COM-004'] = ext('support tiers with SLAs require a support organization, not product code')
C['SR-COM-005'] = ext('professional services are an offering, not product behavior')
C['SR-COM-006'] = ext('partner program is a business function')
C['SR-COM-007'] = exists('docs/ (api-reference, agents, runbooks, 60+ docs)')
C['SR-COM-008'] = ext('sales artifacts (battlecards, datasheets) are marketing deliverables')
C['SR-COM-009'] = exists('docs/adr-001-g2-contract-and-revision-model.md (LTS/revision policy)')
C['SR-COM-010'] = adr('open-core/licensing strategy recorded via ADR process; final business decision pending')

# --- CON ---
C['SR-CON-001'] = exists('deploy/docker-compose.yml (self-contained DP-0)')
C['SR-CON-002'] = exists('local hashing embedder + local model provider')
C['SR-CON-003'] = exists('no default transports; egress kill switch (reinforced this pass by packages/eoip/egress)')
C['SR-CON-004'] = done('config', 'typed layered config shipped this pass (SR-CFG-001..006)')
C['SR-CON-005'] = exists('deterministic query/impact/lineage paths run without LLM')
C['SR-CON-006'] = exists('evidence manifests + provenance trust states')
C['SR-CON-007'] = exists('clean-room policy documented in docs/')
C['SR-CON-008'] = exists('adapter-based backends (graph, embeddings, models)')
C['SR-CON-009'] = exists('export formats (RDF, GraphML, JSON, openCypher, ...)')
C['SR-CON-012'] = ext('hyperscaler reference adapters need cloud accounts for certification')
C['SR-CON-013'] = partial('deploy/helm/', 'Helm modules exist; Terraform/OpenTofu modules partial')
C['SR-CON-014'] = adr('local<->cloud capability migration tooling needs provider-selection ADR')

# --- DEP ---
C['SR-DEP-001'] = exists('deploy/docker-compose.yml + scripts/demo_reset.py')
C['SR-DEP-002'] = exists('deploy/helm/ (HA topology, PDBs)')
C['SR-DEP-003'] = partial('scripts/backup.py + offline license/pack files',
                          'signed OCI archive pipeline partial')
C['SR-DEP-004'] = ext('appliance images (hardware+software) require a hardware build pipeline')
C['SR-DEP-005'] = ext('RPM/DEB native packages require packaging infra')
C['SR-DEP-006'] = partial('docs/ + deploy/', 'platform matrix documented; continuous certification External')
C['SR-DEP-008'] = adr('DP-6 edge package needs sync/conflict-policy ADR')
C['SR-DEP-009'] = exists('docs/ (hardening guides, reference architectures)')

# --- EXT ---
C['SR-EXT-001'] = exists('apps/api (REST/OpenAPI)')
C['SR-EXT-002'] = partial('apps/api + schemas/',
                          'idempotency + pagination on select routes; 12-month deprecation program partial')
C['SR-EXT-003'] = exists('admin APIs across apps/api/extended.py (extended this pass: tenancy/config/branding/licensing admin)')
C['SR-EXT-004'] = partial('packages/eoip (Python SDK)',
                          'Python SDK is the product package; TS/Java/Go/.NET SDKs External')
C['SR-EXT-005'] = partial('examples/ (jira, gitlab, servicenow, confluence)',
                          'reference integrations exist; Slack/Teams bots External')
C['SR-EXT-010'] = exists('connector/parser extension points + marketplace')
C['SR-EXT-011'] = adr('plugin process isolation (container vs WASM) not decided')
C['SR-EXT-012'] = exists('packages/eoip/marketplace (signed, manifest, SBOM fields)')
C['SR-EXT-013'] = partial('packages/eoip/graphtest + marketplace',
                          'contract-test scaffolding exists; full plugin test kit partial')
C['SR-EXT-014'] = partial('packages/eoip/marketplace/ (registry, search)',
                          'online catalog exists; ratings/review workflow partial')
C['SR-EXT-015'] = adr('low-code Studio builders need a UI/ADR decision')

# --- GDB ---
C['SR-GDB-001'] = exists('packages/eoip/graph/store.py (GraphStore port)')
C['SR-GDB-002'] = partial('packages/eoip/graph/backends.py capability flags',
                          'capability manifest publishing partial')
C['SR-GDB-003'] = partial('tests/integration + contract tests',
                          'conformance suite exists for memory backend; per-backend certification External')
C['SR-GDB-004'] = ext('Tier A/B/C certification requires vendor collaboration and HA clusters')
C['SR-GDB-005'] = adr('polyglot per-domain backend split needs deployment ADR')
C['SR-GDB-006'] = adr('online migration (dual-write) not implemented')
C['SR-GDB-007'] = adr('virtual/zero-ETL graph views not implemented')
C['SR-GDB-008'] = partial('RDF/OWL export; LPG primary', 'RDF-star/reification partial')
C['SR-GDB-009'] = partial('packages/eoip/graph/bitemporal.py',
                          'EntityRevision on mutations; full as-of query surface partial')
C['SR-GDB-010'] = exists('packages/eoip/graph/memory.py (embedded + in-memory)')
C['SR-GDB-011'] = partial('config/graph-store.yaml (SQLite single-node)',
                          'PostgreSQL clustered metadata path partial')
C['SR-GDB-012'] = exists('packages/eoip/fileparse + raw capture storage')
C['SR-GDB-013'] = partial('packages/eoip/events/ (embedded log)',
                          'NATS/Kafka/RabbitMQ adapters External')
C['SR-GDB-014'] = exists('packages/eoip/query/cache.py + in-process cache; tenant-scoped keys')
C['SR-GDB-015'] = partial('packages/eoip/jobs.py (retry, timers)',
                          'saga/human-approval workflow engine partial')
C['SR-GDB-016'] = exists('docs/ (component license matrix)')

# --- ING ---
C['SR-ING-001'] = exists('packages/eoip/connectors/ (connector SDK)')
C['SR-ING-002'] = exists('connectors: pagination, retry+jitter, circuit breaker, checkpoints')
C['SR-ING-003'] = exists('poll + webhook change capture in connectors')
C['SR-ING-004'] = exists('credential isolation via secret store/vault')
C['SR-ING-005'] = partial('marketplace packaging for connectors',
                          'data-flow manifest now wired via SR-CON-011')
C['SR-ING-006'] = exists('shared pipeline stages for streaming and batch')
C['SR-ING-007'] = partial('streaming JSON parse + archive support', 'gz/zstd coverage partial')
C['SR-ING-011'] = exists('packages/eoip/ingestion/ entity detection')
C['SR-ING-014'] = partial('packages/eoip/ingest/profile.py value-overlap',
                          'inclusion-dependency discovery partial')
C['SR-ING-015'] = partial('config-reference edge extraction',
                          'trace/log-derived edges need observability sources')
C['SR-ING-017'] = adr('ontology induction (proposed classes from data) not implemented')
C['SR-ING-018'] = exists('packages/eoip/graph/similarity.py link_prediction')
C['SR-ING-019'] = exists('config/mappings/ (declarative mapping DSL)')
C['SR-ING-020'] = partial('packages/eoip/ingest/profile.py drift endpoint',
                          'auto-compatible mapping updates partial')
C['SR-ING-030'] = exists('identity resolution: deterministic then probabilistic')
C['SR-ING-031'] = partial('collective resolution via graph context',
                          'graph-neighbor evidence partial')
C['SR-ING-032'] = exists('explainable, reversible merges with audit bands')
C['SR-ING-033'] = exists('SAME_AS crosswalk with confidence')
C['SR-ING-040'] = partial('derived graphs from mutation events',
                          'incremental maintenance partial; full rebuild exists')
C['SR-ING-041'] = partial('graph.json / HTML export artifacts',
                          'interactive HTML artifact partial')
C['SR-ING-042'] = exists('traversal-first retrieval baseline (no embeddings required)')
C['SR-ING-043'] = partial('pre-aggregation of degree/centrality',
                          'per-domain reachability buckets partial')
C['SR-ING-050'] = exists('validation engine severities + quarantine')
C['SR-ING-051'] = exists('freshness SLOs + knowledge-age surfacing')
C['SR-ING-052'] = exists('ingestion idempotency tests')
C['SR-ING-053'] = partial('reconciliation reports', 'scheduled report automation partial')
C['SR-ING-060'] = exists('hostile-input defenses (zip-bomb, traversal, XXE tests)')
C['SR-ING-061'] = partial('prompt-injection posture: ingestion firewall',
                          'indirect-injection test corpus partial')
C['SR-ING-070'] = exists('export formats (JSON/CSV/GraphML/GEXF/RDF/...)')
C['SR-ING-071'] = ext('JDBC/ODBC/OData/Arrow Flight endpoints need driver certification')

# --- LLM (001-009 pre-existing, 010-020 this pass) ---
C['SR-LLM-001'] = partial('packages/eoip/models/ (Model Provider Port)',
                          'chat/completion + structured-output port exists; tool-calling surface partial')
C['SR-LLM-002'] = exists('local Ollama adapter (eoip.models providers)')
C['SR-LLM-003'] = exists('packages/eoip/models/governance.py ModelRegistry')
C['SR-LLM-004'] = partial('task-based routing between local models',
                          'model routing table exists; multi-model deployment partial')
C['SR-LLM-005'] = exists('docs/ (hardware reference configurations)')
C['SR-LLM-006'] = exists('PromptTemplateRegistry (versioned prompts, A/B hooks)')
C['SR-LLM-007'] = exists('embedding service with model versioning + re-embedding')
C['SR-LLM-008'] = partial('LLM observability metrics', 'per-call cost/quality telemetry partial')
C['SR-LLM-009'] = exists('guardrails: KnowledgeFirewall + output schema validation')

# --- NFR ---
C['SR-NFR-001'] = partial('apps/worker + stateless API tiers',
                          'horizontal scale deployable; multi-node validation External')
C['SR-NFR-002'] = exists('shard-plan + read-replica topology docs')
C['SR-NFR-003'] = exists('query policy: admission control, concurrency, kill-runaway')
C['SR-NFR-004'] = partial('degradation fallbacks (hashing embedder, no-model mode)',
                          'full degradation matrix testing partial')
C['SR-NFR-005'] = exists('scripts/backup.py checksummed archives')
C['SR-NFR-006'] = exists('ops upgrade-plan + signed bundle path')
C['SR-NFR-007'] = ext('chaos/soak testing needs a live cluster')
C['SR-NFR-008'] = partial('sizing guidance in docs', 'in-product capacity forecasting partial')

# --- NLQ (rest) ---
C['SR-NLQ-001'] = exists('packages/eoip/query/nlq.py deterministic template tier')
C['SR-NLQ-005'] = exists('explanation envelope + evidence panel depth')
C['SR-NLQ-006'] = exists('why/why-not/what-changed operators + what-if')
C['SR-NLQ-007'] = partial('conversation follow-ups in NLQProcessor',
                          'session memory across turns partial')
C['SR-NLQ-009'] = ext('multilingual NL needs local multilingual models (External model dependency)')
C['SR-NLQ-010'] = exists('examples/eval golden sets + evaluation agent')
C['SR-NLQ-011'] = exists('authz-constrained NLQ (hidden entities never revealed)')
C['SR-NLQ-012'] = partial('feedback/curation queue', 'thumbs-to-curation loop partial')
C['SR-NLQ-013'] = ext('voice and chat-app surfaces (Teams/Slack/IDE) deferred')
C['SR-NLQ-014'] = exists('simulation overlay copy-on-write what-if')
C['SR-NLQ-015'] = partial('follow-up suggestions in NL responses',
                          'usage-graph proactive suggestions partial')

# --- ONT ---
C['SR-ONT-001'] = exists('ontology packs as versioned artifacts')
C['SR-ONT-002'] = exists('SKOS/RDF/OWL/JSON-LD import-export')
C['SR-ONT-003'] = partial('apps/web ontology views', 'full visual ontology studio partial')
C['SR-ONT-004'] = exists('SHACL-class validation + severity gates')
C['SR-ONT-005'] = exists('SKOS glossary/taxonomy (schemes, synonyms)')
C['SR-ONT-006'] = partial('lexical/structural alignment',
                          'embedding-assisted matching needs vector backends')
C['SR-ONT-008'] = adr('ontology-driven code generation not implemented')
C['SR-ONT-009'] = exists('governed evolution via change governance (SR-GOV-003)')
C['SR-ONT-010'] = ext('DataHub/OpenMetadata/Atlas sync needs those systems for certification')
C['SR-ONT-020'] = partial('graph-native derivations (transitive closure, paths)',
                          'Datalog/SWRL-class rule tier partial')
C['SR-ONT-021'] = exists('truth store retraction surfaces contradictions')
C['SR-ONT-022'] = partial('bitemporal edges', 'defeasible role semantics partial')

# --- OPS ---
C['SR-OPS-001'] = exists('metrics registry + /metrics exposition')
C['SR-OPS-002'] = exists('health/readiness endpoints + dependency roll-up')
C['SR-OPS-003'] = exists('ops support-bundle (redacted)')
C['SR-OPS-004'] = exists('telemetry off by default')
C['SR-OPS-005'] = exists('docs/agent_runbook.md + runbooks')
C['SR-OPS-006'] = partial('usage meter export supports cost views',
                          'cloud FinOps dashboards partial')

# --- PRV (rest) ---
C['SR-PRV-005'] = partial('compliance packs auto-generate records of processing',
                          'data-flow diagram generation partial')
C['SR-PRV-007'] = adr('pseudonymization/tokenization services beyond the egress vault not implemented')

# --- QA (001/002 deferred) ---
C['SR-QA-001'] = ext('synthetic dataset generation per industry pack deferred (generator tooling)')
C['SR-QA-002'] = ext('synthetic scale knobs depend on SR-QA-001 generators')

# --- QRY ---
C['SR-QRY-001'] = exists('6 query languages (EOQL, Gremlin, openCypher, GQL, SPARQL, SQL)')
C['SR-QRY-002'] = exists('schema-aware validation + policy before execution')
C['SR-QRY-003'] = exists('query explain (plan, backends, pushdowns, cost)')
C['SR-QRY-004'] = partial('dialect round-trip golden corpus',
                          'corpus growing; 500-per-backend target partial')
C['SR-QRY-005'] = exists('parameterized plans only (no string-built queries)')
C['SR-QRY-006'] = exists('saved templates + question catalog (query intelligence)')
C['SR-QRY-007'] = exists('result envelope with evidence IDs + freshness')
C['SR-QRY-008'] = exists('30+ graph algorithms callable from plans')
C['SR-QRY-009'] = partial('reachability accelerators', 'transitive-closure indexes partial')
C['SR-QRY-010'] = exists('federated query with per-source policy')
C['SR-QRY-011'] = exists('AS OF / bitemporal reads')
C['SR-QRY-012'] = adr('multilingual query front-ends deferred with SR-NLQ-009')

# --- RAG ---
C['SR-RAG-001'] = exists('retrieval router with logged rationale')
C['SR-RAG-002'] = partial('local/global GraphRAG patterns',
                          'community-summary mode needs embedding backend')
C['SR-RAG-003'] = exists('hybrid BM25+dense with RRF')
C['SR-RAG-004'] = partial('plugin strategy slots exist',
                          'HyDE/step-back/RAG-Fusion implementations partial')
C['SR-RAG-005'] = partial('graph-aware chunking in fileparse',
                          'chunk-entity linking partial')
C['SR-RAG-006'] = partial('corrective verification',
                          'entity verification before LLM assertions partial')
C['SR-RAG-007'] = partial('token-aware context assembly',
                          'per-model budget tables partial')
C['SR-RAG-008'] = exists('model-down deterministic fallback')
C['SR-RAG-009'] = exists('semantic + exact cache keyed by tenant/policy/revision')
C['SR-RAG-010'] = exists('RAG evaluation harness (precision/recall, groundedness)')

# --- SEC ---
C['SR-SEC-001'] = partial('local identity provider + tokens',
                          'OIDC/SAML/LDAP/SCIM need external identity infrastructure')
C['SR-SEC-002'] = exists('RBAC + ABAC policy enforcer')
C['SR-SEC-003'] = partial('element-level policies on labels/classes',
                          'property-level and derived-structure policies partial')
C['SR-SEC-004'] = partial('source-ACL capture in connectors (select sources)',
                          'universal permission mirroring partial')
C['SR-SEC-005'] = ext('access-review certification campaigns are an enterprise process')
C['SR-SEC-006'] = partial('agent identities with budgets', 'least-privilege agent roles partial')
C['SR-SEC-010'] = partial('TLS in deploy configs', 'internal mTLS needs clustered deployment')
C['SR-SEC-011'] = exists('secrets via files/vault; no secrets in graph or logs')
C['SR-SEC-012'] = exists('hash-chained audit sink, exportable')
C['SR-SEC-013'] = exists('non-root, read-only root FS, dropped capabilities in deploy/')
C['SR-SEC-014'] = partial('SBOM generation in CI', 'VEX + Sigstore signing partial')
C['SR-SEC-015'] = ext('SAST/DAST/fuzzing + penetration tests are External certification gates')
C['SR-SEC-016'] = partial('CSP/CSRF/XSS/SSRF guards', 'full web-hardening audit partial')
C['SR-SEC-017'] = exists('knowledge firewall + prompt-injection corpus')

# --- TEN (rest) ---
C['SR-TEN-004'] = ext('automated cross-tenant penetration suite requires an independent security environment')
C['SR-TEN-005'] = ext('BYOK/HYOK key management requires customer KMS integrations')
C['SR-TEN-008'] = partial('tenant-scoped settings/config exist (this pass)',
                          'per-tenant connectors/model allowlists partial')
C['SR-TEN-010'] = adr('cross-tenant sharing needs an explicit sharing-policy design decision')

# --- UX ---
for i in ('001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012'):
    C.setdefault('SR-UX-' + i,
                 partial('apps/web (live-API screens)',
                         'web UI exists; full UX acceptance (scale rendering, WCAG audit) partial'))

# --- VDB ---
C['SR-VDB-001'] = exists('packages/eoip/retrieval/vectors.py vector port')
C['SR-VDB-002'] = partial('hashing embedder (embedded)',
                          'FAISS/pgvector/Qdrant adapters need those backends deployed')
C['SR-VDB-003'] = adr('index-strategy configurability awaits adapter selection (SR-VDB-002)')
C['SR-VDB-004'] = adr('multimodal embeddings need model selection ADR')
C['SR-VDB-005'] = exists('embeddings inherit classification/access policy (privacy + firewall)')
C['SR-VDB-006'] = exists('faceted BM25 search with highlighting')
C['SR-VDB-007'] = exists('no-vector-store deterministic NL acceptance path')

DEFAULT = partial('packages/eoip/ (pre-pass implementation)', 'see prior audit passes')

rows = []
counts = Counter()
for rid in ids:
    status, ev, note = C.get(rid, DEFAULT)
    counts[status] += 1
    pri = texts[rid]['priority'].replace('|', '/')
    evnote = (ev + (' - ' + note if note else '')).replace('|', '/')
    rows.append((rid, pri, status, evnote))

print(counts)
json.dump({'rows': rows, 'counts': dict(counts)},
          open('.tmp/sr_table.json', 'w', encoding='utf-8'), ensure_ascii=False)

defaulted = [r[0] for r in rows if r[3].startswith('packages/eoip/ (pre-pass')]
print('defaulted:', len(defaulted), defaulted)

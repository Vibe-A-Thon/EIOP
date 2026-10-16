# Comprehensive Enterprise Knowledge Graph & Ontology System Requirements Specification (Master Engineering Specification)

**Document Version:** 2.0-AGGREGATED-MASTER  
**Tracking Identifier:** `CRAragg.md`  
**Companion Research Dossier:** [`competitive-research-analysis-agg.md`](competitive-research-analysis-agg.md)  
**Target Platform:** EOIP / KnowGridFlow (Enterprise Ontology & Intelligence Platform)  
**Date:** 2026-10-16  
**Status:** Canonical Implementation Authority & Execution Contract  

---

## 1. Objective, Authority & Autonomous Agent Mandate

### 1.1 Core Mission
This document is the **authoritative, self-explaining, and fully detailed engineering requirements specification** for building the Enterprise Ontology & Intelligence Platform (EOIP / KnowGridFlow). It translates all architectural gaps, competitor limitations, and inversion strategies documented in [`competitive-research-analysis-agg.md`](competitive-research-analysis-agg.md) into concrete, actionable, and testable engineering specifications.

The target system is a **Unified Neuro-Symbolic Enterprise Living Brain** designed to:
1. Connect seamlessly to existing enterprise systems (**Jira, Confluence, Wiki, Rally, ServiceNow, Snowflake, GitLab, GitHub, qTest, API Portal, Artifactory, Splunk, Slack, Kibana, Fortuna, Grafana, Documentum**, and custom systems) via an extensible **Universal Connection Factory**.
2. Support both **Push** (webhooks, event streams, CDC) and **Pull** (permission-preserving crawling, polling) modes.
3. Ingest and decode **16+ file and media formats** (TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX, EML, MSG, Scanned Images/OCR, Audio/Video transcripts, and Engineering Diagrams).
4. Construct and maintain **8 interconnected graph planes** (Raw Resource Graph, Canonical Domain Knowledge Graph, Schema/Meta-Graph, Provenance & Derivation Graph, Lineage Graph, Policy/Security Graph, Temporal/Event Graph, and Vector Similarity Projections).
5. Seamlessly unify **Deterministic Semantics** (W3C RDF 1.1, OWL 2, strict SHACL Core 2017 validation, formal DL inference, and transactional ACID consistency) with **Probabilistic AI** (dense/sparse vector embeddings, GraphRAG, LLM context projection, and tool-calling operational outbox actions).
6. Enforce strict **Zero-Trust Corporate Governance** with source-authoritative Attribute-Based Access Control (ABAC), derivation ACL composition, and strict no-egress boundaries.

---

### 1.2 Mandatory Completion Contract: The "No-Assumption" Rule

> [!CRITICAL]
> ### NON-NEGOTIABLE COMPLETION CONTRACT
> **CODE AND TEST-FILE REFERENCES ALONE ARE NEVER PROOF OF COMPLETION.**
> 
> No autonomous AI agent, developer, or reviewer may claim a requirement is satisfied simply because:
> - A Python file, class, method, or FastAPI route exists.
> - A test file or mock test exists in the repository.
> - A UI component or button renders on screen.
> - A requirement ID is mentioned in a commit message or markdown checklist.
> - A mock provider returns simulated or hardcoded success.
> 
> **A requirement clause is ONLY considered complete when it is backed by an Immutable Verification Receipt.**

#### The 5-State Requirement Lifecycle:
```
[ OPEN ] ---> [ DESIGNED ] ---> [ IMPLEMENTED ] ---> [ VERIFIED ] ---> [ ACCEPTED ]
                   |                   |                    |
                   v                   v                    v
              [ BLOCKED ]         [ FAILED ]           [ DEFERRED ]
```

1. **OPEN:** Requirement specified; no production code written.
2. **DESIGNED:** Pydantic contracts, database schemas, and state machine algorithms reviewed.
3. **IMPLEMENTED:** Real production code written in `packages/eoip/` or `apps/api/` (no mocks, no hardcoded stubs).
4. **VERIFIED:** Automated unit, integration, and negative tests pass against real backends, producing a machine-verifiable execution receipt.
5. **ACCEPTED:** Peer-reviewed audit confirms the code satisfies all acceptance criteria, handles all failure modes, enforces multi-tenant boundaries, and exhibits zero regressions.

---

### 1.3 Machine-Verifiable Execution Receipt Schema

Every verified clause must emit an immutable JSON receipt matching the following schema into `.audit-scratch/receipts/{clause_id}.json`:

```json
{
  "$schema": "https://eoip.enterprise.internal/schemas/verification-receipt-v2.json",
  "requirement_clause": "CRA-020.2",
  "state": "ACCEPTED",
  "execution_timestamp": "2026-10-16T15:30:00Z",
  "git_commit_sha": "3a8b4f129c9e88d7f3e1a0b5c4d6e8f7a9b0c2d3",
  "source_tree_dirty": false,
  "artifact_digest_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "runtime_environment": {
    "os": "Linux / Windows-x64",
    "python_version": "3.11.9",
    "storage_backend": "RocksDB / MemoryHarness",
    "semantic_engine": "SHACL-Core-2017-Validator"
  },
  "execution_command": "pytest tests/unit/test_shacl_strict.py -k test_cardinality_rejection -v --json-report",
  "exit_code": 0,
  "results": {
    "tests_total": 8,
    "tests_passed": 8,
    "tests_failed": 0,
    "tests_skipped": 0,
    "duration_ms": 1420
  },
  "verified_invariants": [
    "MinCount violations reject invalid instances with HTTP 422",
    "Unknown datatypes raise explicit UNSUPPORTED_DATATYPE error code",
    "Zero data mutations committed to canonical store upon validation failure",
    "Tenant A cannot inspect or validate Tenant B shapes"
  ],
  "negative_test_evidence": {
    "attack_payload": "{\"min_counts\": {\"name\": 2}, \"instances\": [{\"name\": \"single\"}]}",
    "expected_status": 422,
    "actual_status": 422,
    "response_error_code": "SHACL_CARDINALITY_VIOLATION"
  },
  "sign_off_agent": "Antigravity-Enterprise-Architect"
}
```

---

## 2. Canonical Cross-Module Data Contracts

All subsystems must interact via strongly typed Pydantic v2 data models. Re-implementing ad-hoc dictionaries or untyped JSON objects is strictly forbidden.

```python
# packages/eoip/contracts/canonical.py
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, HttpUrl

class PrincipalType(str, Enum):
    USER = "user"
    SERVICE_ACCOUNT = "service_account"
    AGENT = "agent"

class TrustedScope(BaseModel):
    """Derived strictly server-side from authenticated JWT/mTLS tokens."""
    tenant_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    principal_id: str = Field(..., min_length=1)
    principal_type: PrincipalType
    roles: List[str] = Field(default_factory=list)
    effective_acls: List[str] = Field(..., description="Groups and direct ACL IDs the principal possesses")
    policy_epoch: int = Field(default=1, description="Current global security epoch for tenant")
    delegation_chain: List[str] = Field(default_factory=list)
    expires_at: datetime

class SourceOperation(str, Enum):
    UPSERT = "upsert"
    DELETE = "delete"
    ACL_UPDATE = "acl_update"
    RENAME = "rename"
    RECONCILE = "reconcile"

class SourceEvent(BaseModel):
    """Immutable record of an event ingested from an enterprise source."""
    event_id: str = Field(..., description="Source-instance scoped unique event ID")
    source_instance_id: str = Field(..., description="e.g., 'jira-prod-us'")
    source_system_type: str = Field(..., description="e.g., 'jira', 'confluence', 'servicenow'")
    operation: SourceOperation
    resource_id: str = Field(..., description="Source system native ID (e.g., 'PROJ-1234')")
    resource_revision: str
    observed_at: datetime
    content_sha256: str = Field(..., min_length=64, max_length=64)
    acl_vector: List[str] = Field(..., description="Source-authoritative user/group permission IDs")
    raw_payload_ref: str = Field(..., description="CAS URI: 'cas://sha256/...'")
    cursor_watermark: str
    tenant_id: str

class EvidenceLocator(BaseModel):
    """Exact byte/spatial/temporal anchor linking an assertion to raw source data."""
    document_id: str
    source_system: str
    source_revision: str
    page_number: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    bounding_box: Optional[List[float]] = None  # [ymin, xmin, ymax, xmax] normalized 0.0-1.0
    media_timestamp_ms: Optional[int] = None
    snippet_text: Optional[str] = None

class TermKind(str, Enum):
    IRI = "iri"
    BLANK_NODE = "blank_node"
    LITERAL = "literal"

class RDFTerm(BaseModel):
    kind: TermKind
    value: str
    datatype: Optional[str] = None
    language: Optional[str] = None

class CanonicalAssertion(BaseModel):
    """An asserted or inferred triple/quad in the Knowledge Graph."""
    assertion_id: str = Field(..., description="'urn:eoip:assertion:<uuid4>'")
    graph_iri: str = Field(default="urn:eoip:graph:domain")
    subject: RDFTerm
    predicate: RDFTerm
    object: RDFTerm
    
    # Semantic Lineage
    is_inferred: bool = False
    supporting_assertion_ids: List[str] = Field(default_factory=list)
    evidence: Optional[EvidenceLocator] = None
    extraction_model: Optional[str] = None
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    
    # Zero-Trust Security Vector
    tenant_id: str
    source_acl_vector: List[str] = Field(..., description="Composed ACLs required to read this fact")
    security_classification: str = Field(default="INTERNAL")
    policy_epoch: int = 1
    
    # Bitemporal Tracking
    valid_from: datetime
    valid_to: Optional[datetime] = None
    tx_timestamp: datetime = Field(default_factory=datetime.utcnow)

class ActionStatus(str, Enum):
    PROPOSED = "proposed"
    STAGED = "staged"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"

class ActionIntent(BaseModel):
    """Governed operational action ready for two-phase dispatch to an external system."""
    action_id: str = Field(..., description="'urn:eoip:action:<uuid4>'")
    action_shape_iri: str = Field(..., description="SHACL Action Shape URI defining argument schema")
    target_system_id: str = Field(..., description="e.g., 'servicenow-prod'")
    idempotency_key: str = Field(..., min_length=16, max_length=128)
    parameters: Dict[str, Any]
    parameters_sha256: str
    
    # Governance & Approval Chain
    status: ActionStatus = ActionStatus.PROPOSED
    requested_by_principal: str
    approved_by_principal: Optional[str] = None
    approval_timestamp: Optional[datetime] = None
    approval_signature: Optional[str] = None
    dry_run: bool = False
    
    # Source Verification & Compensation
    read_back_verification_query: Optional[str] = None
    compensation_action_id: Optional[str] = None
    tenant_id: str
```

---

## 3. Atomic Engineering Requirements Catalog (CRA-001 through CRA-040)

```
====================================================================================================
MODULE 1: PLATFORM FOUNDATIONS, CAPABILITIES & ZERO-TRUST SECURITY
====================================================================================================
```

### CRA-001. Truthful Capabilities Registry, Baseline & Audit Ledger
- **Priority:** P0 (Foundational Blocker)
- **Direct Dependencies:** None
- **Inversion Traceability:** INV-05, INV-08, INV-21, INV-23, INV-39, INV-55; G06, G18
- **Detailed Specification:**
  1. Maintain a dynamic, machine-verifiable `CapabilityRegistry`. Every backend adapter (HugeGraph, Neo4j, Memory, pySHACL, HermiT) must register its verified feature matrix at startup.
  2. If a client queries an unsupported feature (e.g., attempting a recursive SPARQL property path on an adapter supporting only basic triple matches), the engine must return HTTP 422 with status `UNSUPPORTED_CAPABILITY`. It must NEVER silently fall back, fake success, or return empty sets without diagnostics.
  3. Generate and maintain the immutable requirement ledger in `.audit-scratch/ledger.json`, mapping all 40+ CRA requirements to active code, test suites, and cryptographic receipts.
- **Verification Receipts & Acceptance Criteria:**
  - `pytest tests/unit/test_capability_registry.py` passes 100%.
  - Triggering an uncertified capability returns `{ "status": "ERROR", "code": "UNSUPPORTED_CAPABILITY", "unsupported_construct": "PropertyPath" }`.
  - The ledger parses cleanly and validates that no clause is marked `ACCEPTED` without an existing `.audit-scratch/receipts/{clause_id}.json` file.

---

### CRA-002. Sandboxed Micro-Worker Runtime & Resource Fencing
- **Priority:** P0 (Foundational Blocker)
- **Direct Dependencies:** CRA-001
- **Inversion Traceability:** INV-02, INV-08, INV-30, INV-47, INV-55; G11
- **Detailed Specification:**
  1. All resource-intensive and potentially vulnerable tasks (deep document parsing, OCR, video decode, JVM Description Logic reasoning, SHACL validation) must execute inside **isolated worker processes**.
  2. Workers must enforce strict OS-level cgroup/process limits: Maximum 2GB RAM, maximum 2 CPU cores, maximum 30-second execution deadline per item.
  3. If a worker exceeds limits (e.g., a zip bomb, infinite loop in regex, or memory explosion in HermiT reasoner), the orchestrator immediately terminates the worker process, releases file descriptors, returns HTTP 504 / Job Failure, and respawns a healthy worker. Core FastAPI API threads must NEVER block, crash, or run out of memory.
- **Verification Receipts & Acceptance Criteria:**
  - Execute a simulated fork-bomb / memory-spike script inside a worker; verify that the worker is killed within 1,000ms and the main API server remains 100% responsive.
  - Receipt recorded in `.audit-scratch/receipts/CRA-002.json`.

---

### CRA-003. Zero-Trust Principal, Tenancy & Derivation ACL Authorization
- **Priority:** P0 (Security Blocker)
- **Direct Dependencies:** CRA-001, CRA-002
- **Inversion Traceability:** INV-03, INV-19, INV-20, INV-24, INV-39, INV-43; G15, G16
- **Detailed Specification:**
  1. Implement strict multi-tenant database partitioning. Every vertex, edge, assertion, and vector embedding must be tagged with an immutable `tenant_id`.
  2. Implement **Derivation ACL Composition:** When an inference engine derives a new fact $F$ from premises $P_1, P_2, \dots, P_n$, the resulting assertion $F$ automatically inherits the **intersection of the ACL vectors** of all supporting premises:
     $$\text{ACL}(F) = \bigcap_{i=1}^n \text{ACL}(P_i)$$
  3. Dynamic Query Pruning: During SPARQL, SQL, or Vector retrieval, the query engine automatically rewrites execution plans to append security filters matching the caller's `TrustedScope.effective_acls`. If a user does not have permission for $P_1$, they are mathematically prevented from discovering $F$.
  4. Real-time Policy Invalidation: When source permissions are modified (e.g., a user is removed from a private Confluence space), the tenant's `policy_epoch` is incremented. All cached queries, vector search indices, and derived inferences tagged with older epochs are dynamically evicted or re-filtered upon access.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/security/test_tenancy_and_derivation_acls.py`.
  - Assert Tenant A cannot read Tenant B data even when guessing internal URIs.
  - Assert User X (authorized for premise A, but denied premise B) cannot see Inferred Fact C derived from A and B.

---

```
====================================================================================================
MODULE 2: UNIVERSAL CONNECTION FACTORY & ENTERPRISE SYSTEM ADAPTERS
====================================================================================================
```

### CRA-004. Universal Connection Factory & Conformance SDK
- **Priority:** P0
- **Direct Dependencies:** CRA-002, CRA-003
- **Inversion Traceability:** INV-04, INV-27, INV-31, INV-42, INV-43, INV-45; G07, G08
- **Detailed Specification:**
  1. Provide the canonical `ConnectionFactory` interface supporting both Push (webhooks, streaming) and Pull (polling, crawling) across enterprise systems.
  2. Implement automated configuration validation: verify credentials, network endpoints, TLS certificates, and OAuth2 scopes before activating any connector.
  3. Include a built-in Rate Limiter and Token Bucket algorithm per connection instance, guaranteeing that crawling never overloads enterprise source systems or triggers HTTP 429 backoff penalties.
  4. Implement an open SDK allowing third-party developers to implement new enterprise connectors by subclassing `BaseConnector` and implementing standard discovery, sync, and ACL extraction methods.
- **Verification Receipts & Acceptance Criteria:**
  - `tests/unit/test_connection_factory.py` passes 100%.
  - Pluggable custom connector successfully loads via Python entry-points and executes a dry-run sync.

---

### CRA-005. Issue Tracking & Agile Connectors (Jira & Rally)
- **Priority:** P1
- **Direct Dependencies:** CRA-004, CRA-010
- **Inversion Traceability:** INV-05, INV-33, INV-38, INV-42
- **Detailed Specification:**
  1. **Jira Connector (Cloud & Data Center):**
     - Supports Jira REST API v3 and Webhooks.
     - Maps Issues, Projects, Sprints, Components, Worklogs, and Issue Links (`blocks`, `is blocked by`, `relates to`, `duplicates`).
     - Extracts Jira Security Levels and Project Role permissions into the `acl_vector`.
     - Ingests attachment binaries into the Raw Artifact Vault.
  2. **Rally (Broadcom) Connector:**
     - Supports WSAPI v2.0.
     - Maps User Stories, Defects, Tasks, Iterations, and Milestones.
     - Preserves parent-child epic hierarchies and defect association graphs.
- **Verification Receipts & Acceptance Criteria:**
  - Live sandbox / mock fixture integration tests in `tests/integration/connectors/test_jira_rally.py`.
  - Proves incremental sync retrieves only issues updated after the last high-watermark cursor.

---

### CRA-006. Knowledge & Content Repository Connectors (Confluence, Wiki & Documentum)
- **Priority:** P1
- **Direct Dependencies:** CRA-004, CRA-010, CRA-012
- **Inversion Traceability:** INV-06, INV-11, INV-12, INV-40
- **Detailed Specification:**
  1. **Confluence & Generic Wiki Connector:**
     - Ingests Spaces, Pages, BlogPosts, and Comments via CQL and REST APIs.
     - Preserves page hierarchical trees (`wiki:parentPage`, `wiki:childPage`).
     - Extracts Confluence space permissions and page-level restrictions (`view` and `edit` constraints) into `acl_vector`.
     - Downloads embedded attachments and macros for multiformat decoding.
  2. **Documentum (OpenText) Connector:**
     - Connects via Documentum REST Services and CMIS endpoints.
     - Ingests Cabinets, Folders, sysobjects, and renditions.
     - Preserves Documentum Access Control Lists (ACLs), user domain groups, and retention/legal-hold flags.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/connectors/test_confluence_documentum.py`.
  - Proves that restricted Confluence pages are stripped from unauthorized user search results.

---

### CRA-007. Code, Pipeline & Artifact Connectors (GitHub, GitLab & Artifactory)
- **Priority:** P1
- **Direct Dependencies:** CRA-004, CRA-010
- **Inversion Traceability:** INV-07, INV-38, INV-44
- **Detailed Specification:**
  1. **GitHub & GitLab Connectors:**
     - Ingests Repositories, Branches, Commits, Pull/Merge Requests, Issues, and CI/CD Pipeline statuses.
     - Maps commit hashes to author identities and modified file paths.
     - Links PR descriptions to Jira tickets (e.g., regex extraction of `PROJ-\d+` linking commit to issue graph).
     - Captures repository visibility (Public, Internal, Private) in ACL vectors.
  2. **Artifactory (JFrog) Connector:**
     - Uses AQL (Artifactory Query Language) to index repositories, published artifacts, Docker image layers, and build info.
     - Maps build provenance (linking binary artifacts back to the exact Git commit SHA and CI pipeline run).
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/connectors/test_git_artifactory.py`.
  - Verifies multi-hop graph traversal from a compiled binary in Artifactory -> Git Commit -> Jira Feature Ticket.

---

### CRA-008. ITSM, Operational & Monitoring Connectors (ServiceNow, Splunk & Grafana)
- **Priority:** P1
- **Direct Dependencies:** CRA-004, CRA-010, CRA-027
- **Inversion Traceability:** INV-08, INV-33, INV-35, INV-36
- **Detailed Specification:**
  1. **ServiceNow Connector:**
     - Ingests Configuration Items (CIs) from the CMDB (`cmdb_ci`), Incident records, Change Requests, and Problem tickets.
     - Maps CI dependency relationships (`cmdb_rel_ci`: `Depends on::Used by`, `Runs on::Hosts`).
     - Supports two-way operational write-backs (e.g., creating a Change Request or updating Incident status via CRA-027).
  2. **Splunk & Grafana Connectors:**
     - Ingests saved searches, alert definitions, and dashboard metadata.
     - Links dashboard metric panels to corresponding CMDB services and microservices.
     - PII & Secret Redaction: Automatically strips passwords, API keys, and private tokens from ingested log queries.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/connectors/test_servicenow_splunk.py`.
  - Proves operational CI dependencies form a queryable directed acyclic graph (DAG).

---

### CRA-009. Data Warehouse, Messaging & Custom Connectors (Snowflake, Slack, Kibana & Fortuna)
- **Priority:** P1
- **Direct Dependencies:** CRA-004, CRA-010, CRA-024
- **Inversion Traceability:** INV-09, INV-27, INV-28, INV-42
- **Detailed Specification:**
  1. **Snowflake Connector:**
     - Extracts metadata dictionaries (`INFORMATION_SCHEMA`, `ACCOUNT_USAGE`).
     - Ingests SQL query history to infer automated column-level data lineage.
     - Enables live data virtualization via JDBC/Arrow-Flight (querying Snowflake tables without data duplication).
  2. **Slack Connector:**
     - Ingests public channel messages and thread conversations via Slack Events API.
     - Automatically filters out private channels and direct messages (DMs) unless explicit compliance approval is granted.
     - Extracts entity mentions and resolves them against the knowledge graph.
  3. **Fortuna & Generic Custom Connectors:**
     - Configurable REST/OpenAPI, GraphQL, and JDBC adapters for proprietary internal business applications.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/connectors/test_snowflake_slack.py`.
  - Proves Snowflake tables are queryable via standard SPARQL OBDA queries.

---

```
====================================================================================================
MODULE 3: MULTIFORMAT INGESTION & DOCUMENT INTELLIGENCE
====================================================================================================
```

### CRA-010. Bitemporal Event Journal & Resumable Checkpoint Engine
- **Priority:** P0
- **Direct Dependencies:** CRA-002, CRA-003
- **Inversion Traceability:** INV-10, INV-25, INV-31, INV-37; G16
- **Detailed Specification:**
  1. Every event received via push or pull is appended to an immutable, append-only **Event Journal**.
  2. Maintain a persistent checkpoint high-watermark per connector instance. If a worker crashes mid-ingestion, it resumes from the exact high-watermark cursor upon restart with zero data loss and zero duplicate triple emissions.
  3. Support bitemporal indexing: record both `observed_at` (when the platform saw the change) and `source_timestamp` (when the source system recorded the change).
- **Verification Receipts & Acceptance Criteria:**
  - Crash-injection test: Kill ingestion worker process at 50% completion; restart worker and verify 100% data integrity with zero duplicates.

---

### CRA-011. Push Webhook Gateway & Sandboxed Crawler Engine
- **Priority:** P0
- **Direct Dependencies:** CRA-003, CRA-004
- **Inversion Traceability:** INV-11, INV-39, INV-43
- **Detailed Specification:**
  1. **Webhook Gateway:** Authenticates inbound webhook signatures (HMAC-SHA256 for GitHub, Jira, Slack). Rejects unverified or expired payloads with HTTP 401. Enforces a sliding-window rate limiter.
  2. **Sandboxed Crawler Engine:** Bounded recursive crawler for intranet wikis and documentation portals. Enforces maximum depth (default: 5), maximum pages (default: 10,000), domain allowlists, and robots.txt compliance. Egress firewall blocks internal metadata IPs (SSRF prevention).
- **Verification Receipts & Acceptance Criteria:**
  - Submit forged HMAC webhook payload -> Assert HTTP 401 rejection.
  - Submit URL with loopback IP (`127.0.0.1` or `169.254.169.254`) -> Assert crawler immediate block and security audit log emission.

---

### CRA-012. Structured Data & Rich Office Document Decoders
- **Priority:** P0
- **Direct Dependencies:** CRA-002, CRA-010
- **Inversion Traceability:** INV-12, INV-30; G09, G11
- **Detailed Specification:**
  1. Implement decoders for: **TXT, JSON, CSV, TSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX**.
  2. Text chunking must implement safe progress invariants: `0 <= overlap < chunk_size`, guaranteed termination, and safe handling of multi-byte UTF-8 boundaries (resolving gap G11).
  3. Preserve structural locators: every extracted text chunk must record its exact document ID, page number, slide number, sheet name, cell coordinate, or paragraph index in `EvidenceLocator`.
  4. Formula Security: In spreadsheets (XLS/XLSX), extract evaluated cached values and raw formula strings; NEVER execute external DDE macros or embedded scripts.
- **Verification Receipts & Acceptance Criteria:**
  - `pytest tests/unit/test_multiformat_office.py` passes 100%.
  - Verify that a 10MB DOCX and 50-sheet XLSX extract complete text and structural locators within 5 seconds.

---

### CRA-013. Email, Mailbox Container & Archive Parsers
- **Priority:** P0
- **Direct Dependencies:** CRA-002, CRA-012
- **Inversion Traceability:** INV-13, INV-24, INV-40
- **Detailed Specification:**
  1. Implement decoders for **EML, MSG, MBOX, and MIME email threads**.
  2. Extract message headers (`From`, `To`, `Cc`, `Bcc`, `Subject`, `Date`, `Message-ID`, `In-Reply-To`), plain-text body, sanitized HTML body, and nested attachments.
  3. Archive Decoders: Support **ZIP, TAR, GZ, 7Z, BZ2**. Enforce safe streaming decompression: maximum archive size 2GB, maximum nested depth of 3 levels, and path-traversal prevention (rejecting `../` malicious paths).
  4. Nested Attachments: Extracted attachments automatically inherit the parent email's ACLs and are recursively queued for multiformat decoding.
- **Verification Receipts & Acceptance Criteria:**
  - Ingest an EML file with an attached password-free ZIP containing a PDF and an XLSX; verify that all three levels are indexed and queryable with correct parent-child provenance.

---

### CRA-014. Multimedia, Speech-to-Text & Computer Vision OCR Engine
- **Priority:** P1
- **Direct Dependencies:** CRA-002, CRA-012
- **Inversion Traceability:** INV-14, INV-51, INV-52
- **Detailed Specification:**
  1. **OCR Engine (Images & Scanned PDFs):**
     - Extracts text from PNG, JPG, JPEG, TIFF, and scanned PDF documents using Tesseract / PaddleOCR.
     - Preserves normalized spatial bounding boxes `[ymin, xmin, ymax, xmax]` for every detected line and paragraph.
  2. **Audio/Video Transcription Engine:**
     - Extracts audio tracks from MP4, MKV, MP3, WAV, and M4A containers via FFmpeg.
     - Transcribes speech to text using an isolated Whisper model runner.
     - Emits timestamped text segments (preserving start and end milliseconds) in `EvidenceLocator`.
  3. No-Egress Enforcement: All OCR and Whisper models must execute locally on-premises or within the sovereign VPC with ZERO external cloud API calls.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/test_ocr_multimedia.py`.
  - Verifies that querying a spoken phrase returns the exact video file and millisecond timestamp.

---

### CRA-015. Engineering Diagram & Architecture Visual Parser
- **Priority:** P1
- **Direct Dependencies:** CRA-002, CRA-012
- **Inversion Traceability:** INV-07, INV-15, INV-32; G10
- **Detailed Specification:**
  1. Support structured technical diagram formats: **Draw.io (XML), PlantUML, Mermaid, and Visio (VSDX)**.
  2. Compile diagram shapes, labels, connectors, and arrowheads into an abstract syntax tree (AST).
  3. Map diagram components to formal ontology classes (e.g., a cylinder shape maps to `ex:Database`, a rectangle to `ex:Service`) and connectors to formal relationships (`ex:calls`, `ex:readsFrom`).
  4. Never execute naive fallback remapping: resolve gap G10 by preserving unrecognized relations as generic directed edges (`ex:connectsTo`) with full visual attributes rather than coercing all shapes to `Service` and arrows to `CALLS`.
- **Verification Receipts & Acceptance Criteria:**
  - Parse a microservice architecture diagram; verify that extracted services, databases, and dependencies compile into valid OWL 2 triples with 100% graph fidelity.

---

```
====================================================================================================
MODULE 4: CANONICAL STORAGE, DETERMINISTIC REASONING & SHACL ENFORCEMENT
====================================================================================================
```

### CRA-016. RDF 1.1 / RDF-Star Terms & Lexical Fidelity Engine
- **Priority:** P0 (Core Semantic Blocker)
- **Direct Dependencies:** CRA-001
- **Inversion Traceability:** INV-16, INV-20, INV-26, INV-55; G03, G05
- **Detailed Specification:**
  1. Implement a 100% compliant W3C RDF 1.1 and RDF-star term model.
  2. Strict IRI Lexical Preservation: IRIs must be treated as exact, case-sensitive Unicode strings. Fix gap G03: lowercase folding is strictly prohibited (`urn:example:A` and `urn:example:a` must remain distinct non-equal terms).
  3. Maintain full distinction between Datatype Literals (`"123"^^xsd:integer`) and Language-Tagged Strings (`"Chat"@fr` vs. `"Chat"@en`).
  4. Full RDF-star (RDF*) support: Allow statements about statements (nested quoted triples: `<< :john :worksFor :acme >> :since 2021`), enabling rich edge properties without cumbersome RDF reification.
  5. JSON-LD 1.1 Standard Processing: Fix gap G05 by supporting standard JSON-LD 1.1 compaction, expansion, and context resolution rather than relying on proprietary compact formats.
- **Verification Receipts & Acceptance Criteria:**
  - `pytest tests/unit/test_rdf_terms.py` passes 100%.
  - Verify that case-distinct IRIs are never equated without an explicit `owl:sameAs` axiom.

---

### CRA-017. Declarative Mapping IR & Relational OBDA Virtualization
- **Priority:** P0
- **Direct Dependencies:** CRA-016
- **Inversion Traceability:** INV-17, INV-27, INV-28, INV-30
- **Detailed Specification:**
  1. Define a versioned, engine-neutral **Mapping Intermediate Representation (Mapping IR)** supporting W3C R2RML, RML, and RML-star.
  2. Virtualization Pushdown: Compile SPARQL queries over mapped relational databases (Snowflake, PostgreSQL, Oracle) into optimized ANSI SQL queries via Ontop-style semantic query rewriting.
  3. Materialization Engine: For batch datasets (CSV, JSON), execute high-speed vectorized materialization via Morph-KGC / Polars workers, generating over 100,000 triples/second.
- **Verification Receipts & Acceptance Criteria:**
  - Execute a SPARQL query over a 10M-row virtualized PostgreSQL table; verify query executes in <50ms via direct SQL pushdown without copying table data into the triplestore.

---

### CRA-018. Immutable Ontology Package Registry & Semantic Versioning
- **Priority:** P0
- **Direct Dependencies:** CRA-016
- **Inversion Traceability:** INV-01, INV-02, INV-08, INV-18, INV-25
- **Detailed Specification:**
  1. Maintain an immutable, content-addressable **Ontology Package Registry**.
  2. Every ontology release is packaged as a signed bundle containing:
     - The primary OWL 2 ontology document (Turtle / RDF/XML).
     - Pinned transitive import closure with SHA-256 digests (preventing unexpected remote import drift).
     - Associated SHACL constraint shapes package.
     - Associated R2RML / RML mapping definitions.
     - Cryptographic signature and release manifest.
  3. Enforce Semantic Versioning (SemVer 2.0): Breaking axiom changes (e.g., removing a property or tightening a domain constraint) require a major version bump; additive extensions require a minor version bump.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_ontology_registry.py`.
  - Proves that tampering with an import file triggers an immediate signature mismatch and halts activation.

---

### CRA-019. Hybrid Tiered Reasoning Engine (HTRE) & Dependency Retraction
- **Priority:** P0 (Core Semantic Blocker)
- **Direct Dependencies:** CRA-002, CRA-016, CRA-018
- **Inversion Traceability:** INV-17, INV-18, INV-19, INV-20, INV-55; G04
- **Detailed Specification:**
  1. Fix gap G04: Replace hardcoded toy reasoning with the **Hybrid Tiered Reasoning Engine (HTRE)**.
  2. **Tier 1 (Forward Materialization):** Materialize deterministic taxonomic closures (RDFS `subClassOf`, `subPropertyOf`, domain, and range) into memory-mapped prefix tries during write transactions.
  3. **Tier 2 (Query-Time Datalog Evaluation):** Evaluate complex OWL 2 DL axioms, SWRL rules, and transitive property chains via query-time graph rewriting.
  4. **Dependency Provenance Vector:** Every inferred triple stores an array of `supporting_assertion_ids`. If a supporting premise is deleted, an O(1) dependency sweep immediately retracts all dependent inferred triples from the graph.
  5. Consistency Validation: Prior to committing inferred facts, the engine validates disjoint class axioms (`owl:disjointWith`). If a contradiction is detected, the transaction aborts with an `InconsistentOntologyException` detailing the minimal conflicting sub-axiom set.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_htre_reasoner.py`.
  - Assert multi-hop transitive closure computes correctly.
  - Assert deleting a single supporting fact immediately purges the derived inference.

---

### CRA-020. Strict Transactional W3C SHACL Core 2017 Validator
- **Priority:** P0 (Core Correctness Blocker)
- **Direct Dependencies:** CRA-002, CRA-016, CRA-018
- **Inversion Traceability:** INV-08, INV-20, INV-22, INV-47, INV-48; G01, G02
- **Detailed Specification:**
  1. Fix gaps G01 and G02: Implement complete, strict **W3C SHACL Core 2017** validation.
  2. Cardinality & Datatype Enforcement: Enforce `sh:minCount`, `sh:maxCount`, `sh:datatype`, `sh:class`, `sh:nodeKind`, `sh:in`, `sh:pattern`, and property paths.
  3. **Strict Fail-Closed Semantics:** If an unrecognized datatype (G02) or unsupported SHACL construct is encountered, the validator must NEVER return `conforms=true`. It must raise an explicit validation error and reject the data.
  4. Transaction Commit Boundary: Data mutations submitted via API must pass SHACL validation prior to database commit. If any violation is detected, zero triples are committed, and a formal W3C `sh:ValidationReport` is returned with HTTP 422.
- **Verification Receipts & Acceptance Criteria:**
  - Run the reproduction probe from research section 19:
    ```powershell
    python -m pytest tests/unit/test_shacl_strict.py
    ```
  - Confirm: G01 minCount/maxCount violations are strictly caught; G02 unknown datatypes fail validation; invalid mutations are rejected.

---

```
====================================================================================================
MODULE 5: TAXONOMY GOVERNANCE, IDENTITY ALIGNMENT & QUERY FEDERATION
====================================================================================================
```

### CRA-021. Multilingual Taxonomy & Controlled Vocabulary Stewardship (SKOS / SKOS-XL)
- **Priority:** P1
- **Direct Dependencies:** CRA-018, CRA-020
- **Inversion Traceability:** INV-06, INV-09, INV-10, INV-11, INV-12, INV-13, INV-14
- **Detailed Specification:**
  1. Full support for **SKOS and SKOS-XL** concept schemes, broader/narrower hierarchies, related links, and polyhierarchies.
  2. Multilingual Label Management: Store preferred (`skos:prefLabel`), alternative (`skos:altLabel`), and hidden (`skos:hiddenLabel`) labels across multiple BCP-47 language tags (e.g., `en`, `es`, `de`, `fr`, `ja`, `zh`).
  3. Term Deprecation Lifecycle: Support marking concepts as deprecated (`owl:deprecated true`), providing replacement pointers (`dct:isReplacedBy`), and recording change history with audited editorial notes.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_skos_governance.py`.
  - Ingest an ISO 25964 thesaurus; verify multilingual concept search and polyhierarchical traversals.

---

### CRA-022. Ontology Change Governance, Visual Diffs & Pull-Request Workflows
- **Priority:** P1
- **Direct Dependencies:** CRA-003, CRA-018, CRA-020
- **Inversion Traceability:** INV-01, INV-08, INV-22, INV-25, INV-41
- **Detailed Specification:**
  1. Implement GitOps-style branch, merge, and review workflows for enterprise ontologies.
  2. Semantic Diffs: When an engineer modifies an ontology, the engine calculates a **semantic AST diff** (identifying added/removed classes, modified cardinalities, and altered subsumption hierarchies) rather than a raw text line diff.
  3. Automated Pull Request Gates: Every proposed change runs automated CI checks (consistency verification via HermiT, pitfall scanning via OOPS!, and instance regression validation via SHACL).
  4. Multi-Stage Approval: Enforce mandatory dual-steward approval before merging schema changes into the production branch.
- **Verification Receipts & Acceptance Criteria:**
  - Create a branch, introduce an unsatisfiable class, and submit a PR; verify CI automated gate blocks merge with an explanation report.

---

### CRA-023. Canonical Identity Resolution & Reversible Entity Merging
- **Priority:** P1
- **Direct Dependencies:** CRA-003, CRA-016, CRA-019
- **Inversion Traceability:** INV-13, INV-16, INV-23, INV-37, INV-53, INV-54
- **Detailed Specification:**
  1. Entity Resolution Engine: Reconcile duplicate entities originating across different systems (e.g., resolving a Jira user, a GitHub committer, and a Slack handle to a single canonical `ex:Person`).
  2. Multi-Metric Similarity: Combines deterministic exact-key matches (email, employee ID) with probabilistic similarity (Jaro-Winkler on names, graph neighborhood structural similarity).
  3. **Reversible Merging & Audit Ledger:** Merged entities do not destroy original identifiers. Maintain an immutable `IdentityMergeLedger`. If two entities are merged in error, an administrator can execute an atomic **Split Operation**, instantly restoring the original disjoint nodes, their respective edges, and dependent inference vectors without data corruption.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_identity_resolution.py`.
  - Merge two entities, query unified properties, execute split, and verify original state is 100% restored.

---

### CRA-024. Cost-Based Federated Query Engine (SPARQL 1.1, ANSI SQL & openCypher)
- **Priority:** P1
- **Direct Dependencies:** CRA-003, CRA-016, CRA-017, CRA-019
- **Inversion Traceability:** INV-18, INV-19, INV-21, INV-24, INV-27, INV-28; G06, G13
- **Detailed Specification:**
  1. Unified Query Interface: Provide a cost-based federated query planner supporting:
     - **SPARQL 1.1** (full Query and Update specification).
     - **ANSI SQL** (translating SQL table queries into underlying graph traversals via Timbr-style views).
     - **openCypher / GQL** (property graph pattern matching over RDF-star graphs).
  2. Cost-Based Optimizer (CBO): Estimates join cardinality, pushdown selectivity, and network transfer costs across local triplestores, remote Snowflake databases, and virtualized SQL endpoints.
  3. Query Budget Guards: Enforce strict execution deadlines (default: 30 seconds), maximum memory allocation (default: 4GB), and maximum result row limits to prevent runaway queries from degrading cluster performance.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/test_federated_query.py`.
  - Execute a federated query joining local Jira graph nodes with virtualized Snowflake customer tables; verify sub-second execution.

---

```
====================================================================================================
MODULE 6: PROBABILISTIC AI, GRAPHRAG & OPERATIONAL WRITE-BACK OUTBOX
====================================================================================================
```

### CRA-025. Tenant-Scoped Vector Similarity & Hybrid Search Projections
- **Priority:** P1
- **Direct Dependencies:** CRA-002, CRA-003, CRA-012
- **Inversion Traceability:** INV-10, INV-19, INV-25, INV-39, INV-44, INV-54; G12
- **Detailed Specification:**
  1. Fix gap G12: Replace deterministic hashing stubs with production-grade dense vector embeddings (e.g., `text-embedding-3-large`, `bge-large-en-v1.5`) and BM25 sparse keyword indices.
  2. Store embeddings inside a dedicated vector index (Qdrant / pgvector) strictly partitioned by `tenant_id`.
  3. Hybrid Retrieval: Combine dense semantic similarity scores with BM25 sparse keyword scores and PageRank graph centrality scores using Reciprocal Rank Fusion (RRF).
  4. Real-time ACL Filtering: Vector search results must be filtered against the caller's verified `TrustedScope` during vector candidate scanning, preventing unauthorized document chunks from appearing in search results.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_hybrid_vector_search.py`.
  - Assert vector search returns relevant text chunks with exact document citations.

---

### CRA-026. Evidence-Bound GraphRAG & Calibrated Context Assembly
- **Priority:** P1
- **Direct Dependencies:** CRA-003, CRA-019, CRA-020, CRA-025
- **Inversion Traceability:** INV-04, INV-10, INV-11, INV-14, INV-26, INV-51, INV-52
- **Detailed Specification:**
  1. Implement **Grounded GraphRAG**: When generating answers to complex natural language questions, the system retrieves both semantic text chunks and the surrounding multi-hop ontological subgraph.
  2. Strict Evidence Binding: Every sentence generated by the LLM must be accompanied by an explicit citation linking to a verified `CanonicalAssertion` and raw `EvidenceLocator`.
  3. **Calibrated Abstention:** If the retrieved evidence does not support answering the question or if confidence is below 0.85, the model must explicitly state: *"I cannot answer this based on authorized corporate knowledge"*, eliminating hallucinations.
  4. No-Egress Protection: In air-gapped deployments, route LLM inference exclusively to local self-hosted models (vLLM, Ollama, TGI) with zero external internet traffic.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/test_graphrag_grounding.py`.
  - Verify prompt injection attempts in source documents fail to hijack the model or leak unauthorized facts.

---

### CRA-027. Two-Phase Operational Write-Back Outbox & Action Engine
- **Priority:** P1
- **Direct Dependencies:** CRA-003, CRA-004, CRA-020
- **Inversion Traceability:** INV-33, INV-36, INV-41, INV-43
- **Detailed Specification:**
  1. Deliver the Palantir Foundry-style **Operational Action Layer**. Define action types as formal SHACL Action Shapes (e.g., `RestartServiceAction`, `CreateJiraBugAction`).
  2. Two-Phase Transactional Outbox:
     - *Phase 1 (Staging & Validation):* Action parameters are validated against the SHACL shape. If valid, an immutable `ActionIntent` is recorded in the database outbox with status `STAGED`. High-risk actions trigger human-in-the-loop approval workflows.
     - *Phase 2 (Idempotent Execution & Read-Back):* Upon approval, an outbound worker dispatches the action to the remote target system (e.g., ServiceNow REST API) with a unique `Idempotency-Key`.
  3. Read-Back Verification: Following remote execution, the worker queries the target system to independently confirm the change succeeded before updating the action status to `COMPLETED`.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/integration/test_action_outbox.py`.
  - Trigger an action, approve it, simulate remote network timeout, verify automatic idempotent retry and successful read-back.

---

### CRA-028. Bitemporal Graph Navigation, Blast-Radius Simulation & Time Travel
- **Priority:** P1
- **Direct Dependencies:** CRA-010, CRA-016, CRA-019
- **Inversion Traceability:** INV-25, INV-36, INV-37, INV-38, INV-40; G14
- **Detailed Specification:**
  1. Fix gap G14: Replace heuristic random walks with formal graph traversal algorithms (Dijkstra, BFS, PageRank, Tarjan's strongly connected components).
  2. Bitemporal Time Travel: Allow users to execute SPARQL queries with `AS OF` clauses (e.g., `SELECT * WHERE { ... } AS OF "2024-01-15T00:00:00Z"`), returning the exact historical state of the knowledge graph at that moment in time.
  3. Blast-Radius Simulation: When planning a change (e.g., deprecating a database or changing an API endpoint), the simulation engine traverses upstream dependency edges, returning the exact list of impacted microservices, teams, and business processes with risk severity scores.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_temporal_simulation.py`.
  - Execute a point-in-time historical query and verify deleted nodes correctly appear in historical views.

---

```
====================================================================================================
MODULE 7: CATALOG INTEGRATION, ENTERPRISE METADATA & UI WORKBENCH
====================================================================================================
```

### CRA-029. Enterprise Context Layer & Data Catalog Projections
- **Priority:** P1
- **Direct Dependencies:** CRA-003, CRA-016, CRA-018, CRA-024
- **Inversion Traceability:** INV-18, INV-24, INV-28, INV-38, INV-39, INV-40, INV-42, INV-44, INV-45
- **Detailed Specification:**
  1. Maintain active metadata projections compatible with OpenMetadata, DataHub, and Apache Atlas.
  2. Multi-Layer Catalog Graph: Implement data.world-style layered metadata:
     - *Layer 1 (Raw Automated Metadata):* Extracted automatically by crawlers.
     - *Layer 2 (Curated Human Edits):* Business steward descriptions, ownership assignments, and custom tags.
     - *Layer 3 (Effective Merged View):* Deterministic precedence rules ensuring human edits take priority over crawler scans without overwriting raw crawler history.
  3. End-to-End Lineage: Construct automated cross-system lineage linking raw database tables -> transformation scripts -> BI dashboards -> business metrics.
- **Verification Receipts & Acceptance Criteria:**
  - Test Suite: `tests/unit/test_catalog_projections.py`.
  - Verify that updating a human description in Layer 2 does not get erased on subsequent crawler runs.

---

### CRA-030. Accessible Multi-View Enterprise UI Workbench (WCAG 2.2 AA)
- **Priority:** P1
- **Direct Dependencies:** CRA-001, CRA-003, CRA-022, CRA-026
- **Inversion Traceability:** INV-01, INV-05, INV-06, INV-09, INV-16, INV-28, INV-30, INV-50; G15
- **Detailed Specification:**
  1. Deliver a responsive React 19 / Vite single-page application providing specialized operational workbenches:
     - *Source Management:* Configure connectors, monitor crawler health, view error logs.
     - *Ontology Modeler:* Visual force-directed graph canvas + expert Manchester Syntax editor.
     - *Knowledge Explorer:* Interactive entity search, multi-hop neighborhood traversal, and evidence inspection.
     - *Ask AI (GraphRAG):* Natural language question-and-answer interface with side-by-side cryptographic citation panels.
     - *Action Governance:* Approval queues, dry-run impact diffs, and execution audit timelines.
  2. **Accessibility (WCAG 2.2 AA):** Complete keyboard navigation, visible focus indicators, screen-reader ARIA labeling, high-contrast dark/light themes, and reduced-motion animations.
  3. No Fake Data: Replace all placeholder stubs and mock records with real live API data bindings.
- **Verification Receipts & Acceptance Criteria:**
  - Run Playwright E2E and Axe accessibility audits: `npm run test:e2e` and `npm run test:a11y`.
  - 100% automated accessibility checks pass with zero WCAG 2.2 AA violations.

---

```
====================================================================================================
MODULE 8: OPERATIONAL DURABILITY, DEPLOYMENT & COMPLETE QUALIFICATION
====================================================================================================
```

### CRA-031. Durable Distributed Jobs & Dead-Letter Queue (DLQ)
- **Priority:** P0
- **Direct Dependencies:** CRA-002, CRA-003
- **Inversion Traceability:** INV-12, INV-25, INV-29, INV-30, INV-31, INV-36, INV-39, INV-41, INV-44, INV-45; G16
- **Detailed Specification:**
  1. Re-engineer the background job engine for distributed enterprise execution. All jobs (crawl runs, batch ingestions, validation runs, report generations) must be stored in a durable database queue with distributed heartbeat leasing.
  2. Workers acquire leases with heartbeats every 10 seconds. If a worker dies, its lease expires, and another worker automatically picks up the job from the last valid checkpoint.
  3. Dead-Letter Queue (DLQ): If a specific document or payload repeatedly fails processing (e.g., malformed file causing worker crash), it is routed to an isolated DLQ with full diagnostic stack traces, allowing administrators to inspect and replay without stalling the pipeline.
- **Verification Receipts & Acceptance Criteria:**
  - `tests/unit/test_job_queue_tenancy.py` and `tests/integration/test_durable_jobs.py` pass 100%.

---

### CRA-032. OpenTelemetry Tracing, Prometheus Metrics & Audit Observability
- **Priority:** P0
- **Direct Dependencies:** CRA-001, CRA-003, CRA-031
- **Inversion Traceability:** INV-39, INV-44, INV-45
- **Detailed Specification:**
  1. Instrument all API endpoints, background jobs, SPARQL queries, and database transactions with **OpenTelemetry (OTel)** distributed traces.
  2. Export Prometheus metrics: track request latencies (p50/p95/p99), ingestion throughput, SHACL validation durations, and inference amplification ratios.
  3. Structured Audit Logging: Every security-relevant event (login, permission modification, ontology merge, write-back action execution) is emitted as a structured JSON log containing caller principal, timestamp, action, and cryptographic digest.
- **Verification Receipts & Acceptance Criteria:**
  - Verify `/metrics` endpoint exports Prometheus metrics conforming to the Prometheus text format.
  - Verify every API request returns a `traceparent` header linking to an active OTel trace span.

---

### CRA-033. Enterprise Backup, Point-In-Time Recovery (PITR) & Disaster Recovery
- **Priority:** P0
- **Direct Dependencies:** CRA-010, CRA-018, CRA-031
- **Inversion Traceability:** INV-12, INV-20, INV-23, INV-25, INV-37, INV-45
- **Detailed Specification:**
  1. Implement non-blocking, online snapshot backups of the canonical graph, ontology package registry, and relational metadata.
  2. Point-In-Time Recovery (PITR): Combine base snapshots with the bitemporal transaction journal, allowing administrators to restore the entire enterprise knowledge graph to any specific second in time over the preceding 30 days.
  3. Disaster Recovery SLOs:
     - **Recovery Point Objective (RPO):** $\le 15$ minutes.
     - **Recovery Time Objective (RTO):** $\le 4$ hours for a complete 500M-triple restore.
- **Verification Receipts & Acceptance Criteria:**
  - Execute a automated restore drill: take snapshot, simulate database corruption, execute automated restore, and verify 100% graph and query consistency.

---

### CRA-034. Migration CLI & Zero-Downtime Cutover Tooling
- **Priority:** P1
- **Direct Dependencies:** CRA-016, CRA-017, CRA-018, CRA-033
- **Inversion Traceability:** INV-01, INV-15, INV-16, INV-25, INV-26, INV-32, INV-34, INV-35, INV-40
- **Detailed Specification:**
  1. Implement a dedicated command-line utility: `eoip-migrate`.
  2. Commands:
     - `eoip-migrate discover --source <uri>`: Analyzes legacy triplestores (GraphDB, Stardog, Jena) and outputs an extraction plan.
     - `eoip-migrate export --output <path>`: Generates clean, canonical Turtle/N-Quads dumps with SHA-256 manifests.
     - `eoip-migrate validate --input <path>`: Runs pre-migration SHACL and OWL consistency checks.
     - `eoip-migrate cutover`: Atomically switches traffic with automated rollback capability.
- **Verification Receipts & Acceptance Criteria:**
  - Execute complete synthetic migration of a 50M-triple GraphDB repository using `eoip-migrate`; verify zero dropped triples and zero query divergence.

---

### CRA-035. Supply-Chain Compliance, SBOM & Licensing Isolation
- **Priority:** P0
- **Direct Dependencies:** CRA-001, CRA-002
- **Inversion Traceability:** INV-02, INV-05, INV-13, INV-15, INV-21, INV-32, INV-35, INV-46, INV-49, INV-50, INV-54, INV-55; G17
- **Detailed Specification:**
  1. Fix gap G17: Maintain an automated **Software Bill of Materials (SBOM)** conforming to CycloneDX / SPDX for all Python, Node.js, and container dependencies.
  2. Licensing Isolation: Ensure zero viral copyleft contamination (GPLv3 / AGPLv3) enters the proprietary first-party codebase. All GPL/AGPL tools (e.g., standalone CLI utilities) must execute strictly across process network boundaries.
  3. Resolve all legacy dependency issues (e.g., verifying `extract-msg` commercial distribution terms).
- **Verification Receipts & Acceptance Criteria:**
  - Run automated license compliance scan: `syft` and `license-checker`; verify 100% approved licenses.

---

### CRA-036. Performance, Scale & 500M Triple Scale Qualification
- **Priority:** P0
- **Direct Dependencies:** CRA-001, CRA-019, CRA-020, CRA-024, CRA-032
- **Inversion Traceability:** INV-17, INV-18, INV-19, INV-20, INV-21, INV-22, INV-23, INV-26, INV-27, INV-28, INV-29, INV-30, INV-31; G18
- **Detailed Specification:**
  1. Qualify the platform against the **P2 Massive Scale Target**:
     - 500 Million Asserted Triples.
     - 20,000 Classes, 150,000 Axioms.
     - 500 Concurrent Active Users.
  2. Performance Targets:
     - Point Read Latency: $p95 < 20\text{ms}$.
     - Bounded 2-hop Subgraph Page: $p95 < 250\text{ms}$.
     - Batch Ingestion Rate: $> 50,000\text{ triples/second}$.
  3. Execute automated load tests using `wrk` and Locust over a sustained 4-hour window, measuring memory stability and zero heap exhaustion.
- **Verification Receipts & Acceptance Criteria:**
  - Machine-readable benchmark report saved to `.audit-scratch/receipts/CRA-036.json` confirming all latency and throughput targets are achieved.

---

### CRA-037. Independent Test Oracles & Regression Prevention
- **Priority:** P0 (Quality Blocker)
- **Direct Dependencies:** CRA-001 through CRA-036
- **Inversion Traceability:** All INV IDs (01 through 55)
- **Detailed Specification:**
  1. Implement **Independent Test Oracles**: Tests must never share buggy helper functions or mock assumptions with the production code. Expected query results and validation reports must be authored independently.
  2. Automated Mutation & Fuzz Testing: Execute property-based fuzz tests (via Hypothesis) on all parsers, serializers, and SPARQL query planners to detect edge-case panics, memory leaks, and Unicode vulnerabilities.
  3. Zero-Skipped Policy: CI builds must fail if any required test is skipped, marked xfail without an open bug tracker ID, or times out.
- **Verification Receipts & Acceptance Criteria:**
  - Complete test suite passes: `pytest tests/ --cov=packages/eoip --cov-fail-under=85`.
  - Mutation testing score $> 80\%$.

---

### CRA-038. Support Runbooks, SLA Enforcement & Disaster Drills
- **Priority:** P1
- **Direct Dependencies:** CRA-032, CRA-033
- **Inversion Traceability:** INV-10, INV-23, INV-35, INV-41
- **Detailed Specification:**
  1. Publish operational runbooks for all high-severity failure scenarios:
     - Ingestion pipeline backlog / Kafka lag remediation.
     - Triplestore memory exhaustion / query-kill procedures.
     - Compromised source credentials / token rotation.
     - Inconsistent ontology rollback.
  2. Automated Diagnostic Bundles: Implement an administrative CLI (`eoip-admin support-bundle`) that compiles anonymized logs, system metrics, and configuration states into an encrypted diagnostic bundle for enterprise support engineers.
- **Verification Receipts & Acceptance Criteria:**
  - Operator dry-run: An engineer follows the runbook to recover from a simulated database split-brain scenario within 30 minutes.

---

### CRA-039. Developer Platform: Python & TypeScript SDKs, OpenAPI & MCP Server
- **Priority:** P1
- **Direct Dependencies:** CRA-001, CRA-003, CRA-016, CRA-027
- **Inversion Traceability:** INV-05, INV-08, INV-10, INV-33, INV-39, INV-44
- **Detailed Specification:**
  1. Automatically generate and publish client SDKs:
     - `@eoip/sdk-typescript` for frontend and Node.js microservices.
     - `eoip-python` for data scientists and AI pipeline developers.
  2. **Model Context Protocol (MCP) Server:** Expose an enterprise-governed MCP server conforming to the Anthropic / open MCP specification. Allows external AI coding agents (Claude, Cursor, Antigravity) to safely query the knowledge graph, inspect ontology schemas, and propose actions under strict ABAC policy enforcement.
- **Verification Receipts & Acceptance Criteria:**
  - Execute a multi-turn conversation where an AI agent interacts with the knowledge graph via the EOIP MCP server to answer a business query.

---

### CRA-040. Data Privacy, Right-to-be-Forgotten & Strict No-Egress Firewalls
- **Priority:** P0 (Legal & Compliance Blocker)
- **Direct Dependencies:** CRA-003, CRA-010, CRA-025, CRA-031
- **Inversion Traceability:** INV-13, INV-24, INV-25, INV-37, INV-40, INV-42, INV-43, INV-52, INV-54
- **Detailed Specification:**
  1. **Right-to-be-Forgotten (GDPR / CCPA):** Provide an automated deletion cascade. When a data deletion request is submitted for a specific subject (e.g., `ex:Customer123`), the engine locates and purges all instances across all 8 graph planes (Canonical Graph, Derived Inferences, Raw Blobs, Search Indices, Vector Embeddings, and Cache Layers).
  2. **Strict No-Egress Mode:** Provide a cryptographic network boundary. In sovereign/air-gapped deployments, all outbound internet traffic is blocked. Ingress and egress are restricted strictly to configured enterprise systems, verified by network socket monitors.
- **Verification Receipts & Acceptance Criteria:**
  - Execute GDPR purge request; run deep verification sweep across graph indices, vector databases, and cache layers; assert zero remaining records.
  - Run network socket analyzer during full ingestion and RAG cycle; verify 0 external bytes sent.

---

## 4. Complete Verification Protocol for Autonomous AI Agents

When an autonomous AI agent implements requirements from this specification, it must adhere to the following sequence:

```
+---------------------------------------------------------------------------------------------------+
|                            AUTONOMOUS IMPLEMENTATION PROTOCOL                                     |
|                                                                                                   |
|  1. Read Requirement Clause (e.g., CRA-020.2: Cardinality Enforcement).                           |
|  2. Inspect Existing Code in `packages/eoip/` and Identify Canonical Owner.                       |
|  3. Write Pydantic / SQLAlchemy / Database Schema Models.                                         |
|  4. Write Production Business Logic (Clean, Robust, Fully Commented).                             |
|  5. Write Unit Tests (Positive Cases) and Adversarial Tests (Negative / Tamper Cases).             |
|  6. Run Execution Command (pytest, wrk, curl) and Capture Exit Code.                              |
|  7. Verify Machine Invariants (Zero Leaks, Strict Rejection of Invalid Data).                     |
|  8. Emit Machine-Readable Verification Receipt to `.audit-scratch/receipts/{clause_id}.json`.      |
|  9. Update Ledger in `.audit-scratch/ledger.json` from IMPLEMENTED to VERIFIED.                   |
+---------------------------------------------------------------------------------------------------+
```

### Mandate on Code Reviews and Sign-Off:
Under no circumstances may an agent mark a requirement complete by simply referencing a filename or test function name. The existence of code proves only that text was written; only **the execution of that code producing a verifiable, cryptographic receipt** constitutes proof of completion.

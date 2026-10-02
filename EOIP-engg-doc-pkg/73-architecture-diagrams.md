# Architecture Diagram Catalog

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** All Mermaid diagrams requested by the master specification

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## 01-system-context

```mermaid
graph LR
  Sources[Jira JSON / Git / GitLab metadata / docs] --> Ingest[EOIP ingestion]
  Dev[Developer] --> Web[Web app]
  Dev --> VS[VS Code extension]
  Admin[Platform engineer] --> AdminUI[Admin UI]
  Web --> API[FastAPI application]
  AdminUI --> API
  VS --> API
  MCPClient[MCP client] --> MCP[MCP adapter]
  MCP --> API
  API --> HG[(Apache HugeGraph)]
  Ingest --> HG
  API --> LM[Local model adapter]
  API --> Raw[(Local raw/evidence volumes)]
```

## 02-container-architecture

```mermaid
graph TB
  subgraph Host[On-prem / local Docker host]
    Edge[eoip-web : React static UI + reverse proxy]
    API[eoip-api : FastAPI]
    Worker[eoip-worker : ingestion/parser jobs]
    MCP[eoip-mcp : MCP server]
    HG[hugegraph-server : RocksDB]
    Model[local-model : optional runtime profile]
    Obs[Prometheus/Grafana : optional observability profile]
    Vol[(raw/state/backup/model volumes)]
  end
  Edge --> API
  API --> HG
  Worker --> HG
  Worker --> Vol
  API --> Vol
  MCP --> API
  API --> Model
  Obs -. scrape .-> API
  HG --> Vol
```

## 03-ingestion-pipeline

```mermaid
flowchart LR
 S[Source] --> C[Connector] --> R[Raw Capture] --> N[Canonicalize]
 N --> P[Parse / Extract] --> I[Identity Resolution] --> L[Relationship / Semantic Link]
 L --> V[Validate] --> M[Idempotent Graph Mutation] --> X[Index / Meta / Provenance]
 X --> Q[Quality Metrics]
 V -->|rejected| D[DLQ]
```

## 04-enterprise-graph-architecture

```mermaid
graph TB
 M[Meta Graph] --> J[Jira / Work domain]
 M --> C[Code domain]
 M --> D[Documentation domain]
 M --> CI[CI/CD domain]
 M --> P[Provenance domain]
 M --> T[Temporal/Identity domain]
 J <-->|IMPLEMENTS / REFERENCES| C
 C <-->|PRODUCED_BY| CI
 C <-->|DOCUMENTS / REFERENCES| D
 J -. evidence .-> P
 C -. evidence .-> P
 D -. evidence .-> P
```

## 05-meta-graph

```mermaid
graph LR
 DS[DataSource] --> IR[IngestionRun]
 IR --> GD[GraphDomain]
 IR --> OV[OntologyVersion]
 IR --> SV[SchemaVersion]
 IR --> VR[ValidationRun]
 VR --> VF[ValidationFinding]
 VR --> QS[QualitySnapshot]
 IR --> EV[Evidence]
 EV --> FACT[Business Fact]
```

## 06-code-graph

```mermaid
graph LR
 R[Repository] --> B[Branch]
 R --> C[Commit]
 C -->|MODIFIES| F[File]
 F -->|DECLARES| S[CodeSymbol]
 S -->|CALLS| S2[CodeSymbol]
 S -->|IMPORTS| M[Module/Dependency]
 S -->|DEPENDS_ON| D[Dependency]
```

## 07-cross-domain-relationship-graph

```mermaid
flowchart LR
 J[Jira Story] --> MR[Merge Request]
 MR --> C[Commit]
 C --> F[Source File]
 F --> FN[Function]
 FN --> D[Dependency]
 D --> P[Pipeline/Build]
 P --> DOC[Documentation]
 J -. evidence .-> E[Provenance]
 FN -. evidence .-> E
 DOC -. evidence .-> E
```

## 08-query-execution

```mermaid
flowchart LR
 U[NL / structured request] --> I[Intent extraction]
 I --> P[Typed QueryPlan]
 P --> S[Schema + policy validation]
 S --> C[Cost / bounds validation]
 C --> G[Named Gremlin template]
 G --> H[(HugeGraph)]
 H --> E[GraphResult + Evidence]
 E --> A[UI / MCP / RAG / Agent]
 S -->|deny| D[Policy error + audit]
```

## 09-graphrag

```mermaid
flowchart LR
 Q[Question] --> R[Retrieval Router]
 R --> G[Graph query]
 R --> D[Linked docs/code retrieval]
 G --> C[Evidence context]
 D --> C
 C --> L[Local model, if available]
 C --> F[Deterministic formatter/fallback]
 L --> O[Answer + citations]
 F --> O
```

## 10-agent-runtime

```mermaid
stateDiagram-v2
 [*] --> Route
 Route --> Context
 Context --> Plan
 Plan --> Validate
 Validate --> Execute: allowed
 Validate --> Stop: denied/budget
 Execute --> Observe
 Observe --> Evaluate
 Evaluate --> Plan: bounded replan
 Evaluate --> Result: sufficient
 Result --> Explain
 Explain --> Audit
 Audit --> [*]
```

## 11-multi-agent-orchestration

```mermaid
flowchart TB
 R[Request] --> S[Supervisor]
 S --> P[Planner]
 P --> V[Plan Validator]
 V --> W1[Worker A]
 V --> W2[Worker B]
 W1 --> C[Critic/Reviewer]
 W2 --> C
 C --> S
 S --> O[Bounded Result + Evidence]
 G[Budgets/Circuit Breaker] -. constrains .-> S
 G -. constrains .-> W1
 G -. constrains .-> W2
```

## 12-mcp-architecture

```mermaid
graph LR
 Client[MCP Client] --> Server[EOIP MCP Server]
 Server --> Policy[Tool Registry + Policy]
 Policy --> Services[Application Services]
 Services --> Q[Query / Retrieval]
 Q --> HG[(HugeGraph)]
 Services --> Ev[Evidence]
 W[Write/Action Registry] -. disabled in MVP .-> Policy
```

## 13-human-control-architecture

```mermaid
flowchart LR
 Req[Requested Action] --> Risk[Risk + Reversibility]
 Risk --> P[Human-Control Policy]
 P -->|read/low risk| Exec[Execute]
 P -->|approval required| H[Human Approval]
 H -->|approve| Exec
 H -->|reject/timeout| Stop[Stop + Audit]
 Exec --> Verify[Verify Outcome]
 Verify --> Audit[Evidence + Audit]
```

## 14-web-ui-architecture

```mermaid
graph LR
 Browser[React SPA] --> Search[Search/Query]
 Browser --> Graph[Graph Explorer]
 Browser --> Impact[Trace/Impact]
 Browser --> Admin[Admin Screens]
 Search --> API[FastAPI]
 Graph --> API
 Impact --> API
 Admin --> API
 API --> Services[Application Services]
```

## 15-vscode-architecture

```mermaid
graph LR
 VS[VS Code] --> Ext[EOIP Extension]
 Ext --> Ctx[Workspace/File/Symbol Resolver]
 Ext --> API[EOIP REST API]
 API --> Graph[Graph/Query Services]
 Graph --> HG[(HugeGraph)]
 API --> Ev[Evidence]
 Ext --> View[Sidebar/Webview]
```

## 16-deployment

```mermaid
graph TB
 User[Browser/VS Code/MCP client] --> Host[On-prem Docker Host]
 subgraph Host
   Web[Web/API edge]
   Worker[Worker]
   MCP[MCP]
   HG[HugeGraph + RocksDB]
   LM[Local Model]
   V[(Persistent Volumes)]
 end
 Web --> HG
 Worker --> HG
 MCP --> Web
 Web --> LM
 HG --> V
 Worker --> V
 Internet[(External Internet)] -. denied by default .- Host
```

## 17-mvp-e2e-flow

```mermaid
sequenceDiagram
 participant O as Operator
 participant W as Worker
 participant H as HugeGraph
 participant U as Web/VSCode
 participant A as Query/RAG Agent
 participant M as MCP
 O->>W: import Jira + Git + code + docs
 W->>H: canonical vertices/edges + evidence
 W->>H: validation/meta/quality
 O->>U: select Jira issue / current symbol
 U->>A: trace or impact request
 A->>H: bounded QueryPlan/Gremlin template
 H-->>A: path/subgraph/evidence
 A-->>U: result + references
 O->>M: same context request
 M->>A: application service call
 A-->>M: same evidence semantics
```

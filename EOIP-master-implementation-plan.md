# EOIP Master Implementation Plan

Snapshot: 2026-10-19T19:22:09+00:00
Source revision: `76f8e8bb93000e604f88aba1bf07a6ad594cf519`
Status: work programme and acceptance contract; no phase is declared complete by its presence here.

## Operating instructions for a coding agent

Read `EOIP-master-requirements.md` and the linked original source for each assigned ID. Recheck the current branch; this snapshot can become stale. Preserve unrelated working-tree changes. Turn one requirement into explicit authorized entrypoints, inputs, outputs, errors, limits, security controls, tests and independent runtime observations. Report blocked work rather than inventing proof.

### One requirement at a time

1. Pin the source ID, SHA-256 and exact source lines. Resolve duplicate or conflicting text through an ADR. Do not silently choose the easier wording.
2. Identify the owning service/repository in the suite plan. Trace API, worker, storage, UI and external channels. Record code and test paths as leads.
3. Specify the success and denial journey, deployment profile, fixture, expected output, quality measure, resource envelope and applicable security boundary.
4. Implement at the owning boundary, keeping one authority for auth, jobs, graph writes, evidence and artifacts. Add migrations and compatibility where necessary.
5. Run tests plus a real entrypoint through the packaged product. Observe persisted outputs, exact backend placement, authorization and negative cases outside the component under test.
6. Retain a reproducible bundle with source/build/model/config hashes, environment, raw results, failures, reviewer identity, verifier output and expiry. A hash or populated reviewer field is not an independent signature.
7. Promote only the exact accepted profile. Revoke or requalify after code, dependency, model, policy or driver changes. Update this dashboard from source evidence, not manual count edits.

## Delivery order

| Wave | Ownership | Prerequisites | Required exit observation |
|---|---|---|---|
| W00 | Inventory, lineage and disagreement resolution | none | All Markdown files accounted for; stable IDs, line sources and conflicts reviewed |
| W01 | Evidence and capability truth | 00 | Forged/changed/missing receipts rejected by independent verifier; no file-path promotion |
| W02 | Identity, tenancy, source ACL and privacy | 00-01 | Cross-tenant and revoked-access end-to-end denials with derived data |
| W03 | Durable jobs, artifact authority and recovery | 01-02 | Concurrent claims, stale fences, persisted results and restart reconciliation |
| W04 | Graph acquisition, connectors, mappings and data quality | 02-03 | Real source-to-graph counts, provenance, rejected rows and reconciliation |
| W05 | Ontology, SHACL, bitemporal graph and governed writes | 02-04 | Actual validation, approved mutation, read-after-write and rollback effects |
| W06 | Query dialects, graph traversal and explorer | 02, 05 | Known-answer queries against each advertised backend plus unsupported cases |
| W07 | Optional numerical and processing profiles | 02-06 | All ten logical profiles run scoped CPU tasks; accelerators only with physical traces |
| W08 | Local models, retrieval, grounded answers and agents | 02-07 | Qualified model tasks, citations, no-egress and delegated action boundaries |
| W09 | Reports, analytics and export lifecycle | 02-08 | Snapshot/provenance, scheduled jobs, revocation and downloaded artifact controls |
| W10 | Suite portals, MCP, CLI and VS Code | 02-09 | Real user journeys across selected deployed frontend and same APIs |
| W11 | Install, license, migration, operations and scale | 00-10 | Clean offline package, restore drills, benchmark and supported topology matrix |
| W12 | Independent release acceptance | all | All scoped requirements have independently checked current evidence or are visibly blocked/excluded |

## Priority audit repairs

- **AUD-001 Legacy master status promoted paths and editable claims** (high): Use independently observed, profile-bound acceptance evidence and reviewer verification. Reproduce against [scripts/build_master_suite.py](scripts/build_master_suite.py); retain positive and negative runtime observations.
- **AUD-002 Result references are not persisted by durable commit** (high): Persist result and receipt references transactionally, reconcile staged artifacts and test restart. Reproduce against [packages/eoip/jobs.py:279](packages/eoip/jobs.py); retain positive and negative runtime observations.
- **AUD-003 Lease expiry needs a direct stale-worker gate** (high): Reject stale operations immediately at lease expiry and test before and after reclamation. Reproduce against [packages/eoip/jobs.py:231](packages/eoip/jobs.py); retain positive and negative runtime observations.
- **AUD-004 Cross-tenant pending-claim predicate has been corrected in the working tree** (medium): Retain regression coverage and qualify tenant scope across queue operations and deployments. Reproduce against [packages/eoip/jobs.py:166](packages/eoip/jobs.py); retain positive and negative runtime observations.
- **AUD-005 Logical operator catalog is broader than runtime integration** (high): Run each operator through the real end-to-end processing contract and preserve receipts. Reproduce against [packages/eoip/processing/catalog.py](packages/eoip/processing/catalog.py); retain positive and negative runtime observations.
- **AUD-006 Classical quantum simulator diverges from the planned bounded library path** (high): Enforce caps before allocation and use Qiskit Aer or document an approved revised design with analytic acceptance. Reproduce against [packages/eoip/processing/backends/quantum_sim.py:206](packages/eoip/processing/backends/quantum_sim.py); retain positive and negative runtime observations.
- **AUD-007 Query proposals interpolate schema class names** (high): Use an authorized schema registry and structured query AST, then validate through the existing parser. Reproduce against [packages/eoip/processing/backends/text_local.py:184](packages/eoip/processing/backends/text_local.py); retain positive and negative runtime observations.
- **AUD-008 Grounded status is based on produced citations** (medium): Verify source authorization and cited span support independently; evaluate abstention. Reproduce against [packages/eoip/processing/backends/text_local.py:124](packages/eoip/processing/backends/text_local.py); retain positive and negative runtime observations.
- **AUD-009 Application egress checks are not a network boundary** (high): Deny compute-worker egress at the OS/deployment boundary and observe hostile probes externally. Reproduce against [packages/eoip/egress/gateway.py:260](packages/eoip/egress/gateway.py); retain positive and negative runtime observations.
- **AUD-010 Editable ledger state can qualify a capability** (high): Bind verified receipts to exact profile and make production admission fail on unqualified state. Reproduce against [packages/eoip/capabilities/registry.py:110](packages/eoip/capabilities/registry.py); retain positive and negative runtime observations.
- **AUD-011 Alternate frontend supplies a bootstrap principal on whoami failure** (medium): Remove the synthesized identity before adopting this frontend into the suite. Reproduce against [frontend/src/lib/auth.tsx:56](frontend/src/lib/auth.tsx); retain positive and negative runtime observations.
- **AUD-012 Two frontend implementations need a release decision** (medium): Reconcile routes, auth, tests and deployment before publishing a unified help claim. Reproduce against [docs/EOIP-suite-architecture-plan.md](docs/EOIP-suite-architecture-plan.md); retain positive and negative runtime observations.
- **AUD-013 Graph service label contradicts the active memory backend** (medium): Bind the service name and health to authoritative backend metadata, remove optimistic READY fallback, and verify the memory and HugeGraph profiles through browser journeys. Reproduce against [apps/web/src/App.jsx:718](apps/web/src/App.jsx); retain positive and negative runtime observations.

## Requirement work queue

This queue retains one row per unique requirement and gives a first owning wave. The wave is a planning aid, not a guarantee of implementation status. Each row inherits the seven-step acceptance procedure above and the original source's detailed constraints.

| ID | Area | Lead wave | Audit state | Reported state | Source | Next proof |
|---|---|---|---|---|---|---|
| `AC-01` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1032](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-02` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1033](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-03` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1034](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-04` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1035](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-05` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1036](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-06` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1037](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-07` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1038](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-08` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1039](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-09` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1040](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-10` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1041](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-11` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1042](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-12` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1043](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-13` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1044](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-14` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1045](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-15` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1046](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-16` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1047](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-17` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1048](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-18` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1049](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-19` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1050](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-20` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1051](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-21` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1052](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-22` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1053](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-23` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1054](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-24` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1055](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-25` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1056](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-26` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1057](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-27` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1058](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-28` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1059](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-29` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1060](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-30` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1061](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-31` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1062](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-32` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1063](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-33` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1064](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-34` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1065](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-35` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1066](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-36` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1067](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-37` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1068](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-38` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1069](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-39` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1070](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-40` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1071](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-41` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1072](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-42` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1073](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-43` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1074](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-44` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1075](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-45` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1076](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-46` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1077](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-47` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1078](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-48` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:1079](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `AC-FR-ADMIN-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:78](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-ADMIN-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:79](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-AGENT-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:68](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-AGENT-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:69](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-AGENT-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:70](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-AGENT-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:71](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-AGENT-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:72](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CODE-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:46](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CODE-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:47](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CODE-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:48](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CODE-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:49](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CODE-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:50](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONF-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:22](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:15](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:16](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:17](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:18](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:19](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-006` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:20](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-CONN-007` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:21](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:29](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:30](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:31](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:32](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:33](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-006` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:34](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-007` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:35](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-008` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:36](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-009` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:37](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-GRAPH-010` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:38](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-ID-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:43](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-ID-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:44](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-INGEST-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:24](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-INGEST-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:25](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-INGEST-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:26](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-INGEST-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:27](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-INGEST-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:28](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-MCP-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:74](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-MCP-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:75](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-MEM-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:73](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-ONTO-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:39](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-ONTO-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:40](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-PROV-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:41](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-PROV-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:42](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:51](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:52](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:53](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:54](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:55](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-006` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:56](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-007` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:57](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-QUERY-008` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:58](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-RAG-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:62](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-RAG-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:63](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-RAG-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:64](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-RAG-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:65](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-RAG-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:66](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-RAG-006` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:67](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-SNOW-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:23](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-TEMP-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:45](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-UI-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:76](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-UI-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:77](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-VALID-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:59](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-VALID-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:60](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-VALID-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:61](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-VSCODE-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:80](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-FR-VSCODE-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:81](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-MAINT-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:94](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-OPS-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:91](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-OPS-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:92](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-PERF-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:93](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-PRIV-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:95](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-REL-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:89](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-REL-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:90](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-001` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:82](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-002` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:83](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-003` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:84](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-004` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:85](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-005` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:86](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-006` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:87](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AC-NFR-SEC-007` | AC | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:88](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `AGENT-001` | AGENT | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:175](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AGENT-001.1` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:406` | reconcile source and design real acceptance |
| `AGENT-001.2` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:407` | reconcile source and design real acceptance |
| `AGENT-001.3` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:408` | reconcile source and design real acceptance |
| `AGENT-001.4` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:409` | reconcile source and design real acceptance |
| `AGENT-001.5` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:410` | reconcile source and design real acceptance |
| `AGENT-002` | AGENT | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:194](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AGENT-002.1` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:432` | reconcile source and design real acceptance |
| `AGENT-002.2` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:433` | reconcile source and design real acceptance |
| `AGENT-002.3` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:434` | reconcile source and design real acceptance |
| `AGENT-002.4` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:435` | reconcile source and design real acceptance |
| `AGENT-002.5` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:436` | reconcile source and design real acceptance |
| `AGENT-002.6` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:437` | reconcile source and design real acceptance |
| `AGENT-002.7` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:438` | reconcile source and design real acceptance |
| `AGENT-002.8` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:439` | reconcile source and design real acceptance |
| `AGENT-003` | AGENT | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:220](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AGENT-003.1` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:460` | reconcile source and design real acceptance |
| `AGENT-003.2` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:461` | reconcile source and design real acceptance |
| `AGENT-003.3` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:462` | reconcile source and design real acceptance |
| `AGENT-003.4` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:463` | reconcile source and design real acceptance |
| `AGENT-003.5` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:464` | reconcile source and design real acceptance |
| `AGENT-004` | AGENT | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:241](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AGENT-004.1` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:481` | reconcile source and design real acceptance |
| `AGENT-004.2` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:482` | reconcile source and design real acceptance |
| `AGENT-004.3` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:483` | reconcile source and design real acceptance |
| `AGENT-004.4` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:484` | reconcile source and design real acceptance |
| `AGENT-004.5` | AGENT | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:485` | reconcile source and design real acceptance |
| `CRA-001.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-001.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-002.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-002.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-002.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-003.10` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-003.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-003.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-004.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-004.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-004.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-005.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-005.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-005.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-006.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-006.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-006.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-007.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-007.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-007.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-008.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-008.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-008.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-009.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-009.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-010.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-010.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-010.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-011.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-011.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-011.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-012.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-012.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-012.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-013.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-013.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-013.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-014.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-014.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-014.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-015.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-015.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-015.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-016.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-017.11` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-018.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-019.10` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-019.12` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-020.10` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-021.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-022.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-022.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-023.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-023.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-024.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-024.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-025.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-026.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-026.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-027.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-027.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-028.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-028.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-028.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-029.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-029.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-029.8` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-030.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-030.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-031.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-031.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-032.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-032.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-033.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-034.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-034.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-035.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-036.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-037.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-037.9` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-038.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-038.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-039.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-040.6` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `CRA-040.7` | AGG | W00 | claimed_accepted | `ACCEPTED` | `AGG` | independently verify claim and runtime |
| `AI-001` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:390](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-001.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:650` | reconcile source and design real acceptance |
| `AI-001.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:651` | reconcile source and design real acceptance |
| `AI-001.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:652` | reconcile source and design real acceptance |
| `AI-001.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:653` | reconcile source and design real acceptance |
| `AI-001.5` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:654` | reconcile source and design real acceptance |
| `AI-001.6` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:655` | reconcile source and design real acceptance |
| `AI-001.7` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:656` | reconcile source and design real acceptance |
| `AI-002` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:414](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-002.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:675` | reconcile source and design real acceptance |
| `AI-002.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:676` | reconcile source and design real acceptance |
| `AI-002.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:677` | reconcile source and design real acceptance |
| `AI-002.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:678` | reconcile source and design real acceptance |
| `AI-002.5` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:679` | reconcile source and design real acceptance |
| `AI-003` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:435](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-003.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:698` | reconcile source and design real acceptance |
| `AI-003.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:699` | reconcile source and design real acceptance |
| `AI-003.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:700` | reconcile source and design real acceptance |
| `AI-003.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:701` | reconcile source and design real acceptance |
| `AI-003.5` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:702` | reconcile source and design real acceptance |
| `AI-004` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:456](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-004.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:719` | reconcile source and design real acceptance |
| `AI-004.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:720` | reconcile source and design real acceptance |
| `AI-004.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:721` | reconcile source and design real acceptance |
| `AI-004.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:722` | reconcile source and design real acceptance |
| `AI-004.5` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:723` | reconcile source and design real acceptance |
| `AI-005` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:475](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-005.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:741` | reconcile source and design real acceptance |
| `AI-005.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:742` | reconcile source and design real acceptance |
| `AI-005.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:743` | reconcile source and design real acceptance |
| `AI-005.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:744` | reconcile source and design real acceptance |
| `AI-005.5` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:745` | reconcile source and design real acceptance |
| `AI-006` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:495](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-006.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:763` | reconcile source and design real acceptance |
| `AI-006.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:764` | reconcile source and design real acceptance |
| `AI-006.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:765` | reconcile source and design real acceptance |
| `AI-006.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:766` | reconcile source and design real acceptance |
| `AI-006.5` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:767` | reconcile source and design real acceptance |
| `AI-007` | AI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:515](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `AI-007.1` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:784` | reconcile source and design real acceptance |
| `AI-007.2` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:785` | reconcile source and design real acceptance |
| `AI-007.3` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:786` | reconcile source and design real acceptance |
| `AI-007.4` | AI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:787` | reconcile source and design real acceptance |
| `AI-ACT-ART-13` | AI | W00 | untriaged | `UNTRIAGED` | [docs/audit-2026-10-06/assessed-gap-report.md:750](docs/audit-2026-10-06/assessed-gap-report.md) | reconcile source and design real acceptance |
| `AIDLC-001` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:177` | reconcile source and design real acceptance |
| `AIDLC-001.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2052` | reconcile source and design real acceptance |
| `AIDLC-001.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2053` | reconcile source and design real acceptance |
| `AIDLC-001.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2054` | reconcile source and design real acceptance |
| `AIDLC-001.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2055` | reconcile source and design real acceptance |
| `AIDLC-002` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:177` | reconcile source and design real acceptance |
| `AIDLC-002.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2070` | reconcile source and design real acceptance |
| `AIDLC-002.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2071` | reconcile source and design real acceptance |
| `AIDLC-002.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2072` | reconcile source and design real acceptance |
| `AIDLC-002.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2073` | reconcile source and design real acceptance |
| `AIDLC-003` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:139` | reconcile source and design real acceptance |
| `AIDLC-003.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2089` | reconcile source and design real acceptance |
| `AIDLC-003.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2090` | reconcile source and design real acceptance |
| `AIDLC-003.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2091` | reconcile source and design real acceptance |
| `AIDLC-003.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2092` | reconcile source and design real acceptance |
| `AIDLC-004` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:139` | reconcile source and design real acceptance |
| `AIDLC-004.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2165` | reconcile source and design real acceptance |
| `AIDLC-004.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2166` | reconcile source and design real acceptance |
| `AIDLC-004.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2167` | reconcile source and design real acceptance |
| `AIDLC-004.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2168` | reconcile source and design real acceptance |
| `AIDLC-005` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:143` | reconcile source and design real acceptance |
| `AIDLC-005.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2183` | reconcile source and design real acceptance |
| `AIDLC-005.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2184` | reconcile source and design real acceptance |
| `AIDLC-005.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2185` | reconcile source and design real acceptance |
| `AIDLC-005.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2186` | reconcile source and design real acceptance |
| `AIDLC-006` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:176` | reconcile source and design real acceptance |
| `AIDLC-006.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2200` | reconcile source and design real acceptance |
| `AIDLC-006.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2201` | reconcile source and design real acceptance |
| `AIDLC-006.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2202` | reconcile source and design real acceptance |
| `AIDLC-006.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2203` | reconcile source and design real acceptance |
| `AIDLC-007` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:747` | reconcile source and design real acceptance |
| `AIDLC-007.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2109` | reconcile source and design real acceptance |
| `AIDLC-007.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2110` | reconcile source and design real acceptance |
| `AIDLC-007.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2111` | reconcile source and design real acceptance |
| `AIDLC-007.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2112` | reconcile source and design real acceptance |
| `AIDLC-008` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:79` | reconcile source and design real acceptance |
| `AIDLC-008.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2127` | reconcile source and design real acceptance |
| `AIDLC-008.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2128` | reconcile source and design real acceptance |
| `AIDLC-008.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2129` | reconcile source and design real acceptance |
| `AIDLC-008.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2130` | reconcile source and design real acceptance |
| `AIDLC-009` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:178` | reconcile source and design real acceptance |
| `AIDLC-009.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2314` | reconcile source and design real acceptance |
| `AIDLC-009.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2315` | reconcile source and design real acceptance |
| `AIDLC-009.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2316` | reconcile source and design real acceptance |
| `AIDLC-009.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2317` | reconcile source and design real acceptance |
| `AIDLC-010` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:181` | reconcile source and design real acceptance |
| `AIDLC-010.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2144` | reconcile source and design real acceptance |
| `AIDLC-010.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2145` | reconcile source and design real acceptance |
| `AIDLC-010.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2146` | reconcile source and design real acceptance |
| `AIDLC-010.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2147` | reconcile source and design real acceptance |
| `AIDLC-011` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:143` | reconcile source and design real acceptance |
| `AIDLC-011.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2220` | reconcile source and design real acceptance |
| `AIDLC-011.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2221` | reconcile source and design real acceptance |
| `AIDLC-011.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2222` | reconcile source and design real acceptance |
| `AIDLC-011.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2223` | reconcile source and design real acceptance |
| `AIDLC-012` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:175` | reconcile source and design real acceptance |
| `AIDLC-012.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2239` | reconcile source and design real acceptance |
| `AIDLC-012.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2240` | reconcile source and design real acceptance |
| `AIDLC-012.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2241` | reconcile source and design real acceptance |
| `AIDLC-012.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2242` | reconcile source and design real acceptance |
| `AIDLC-013` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2244` | reconcile source and design real acceptance |
| `AIDLC-013.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2257` | reconcile source and design real acceptance |
| `AIDLC-013.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2258` | reconcile source and design real acceptance |
| `AIDLC-013.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2259` | reconcile source and design real acceptance |
| `AIDLC-013.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2260` | reconcile source and design real acceptance |
| `AIDLC-014` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2262` | reconcile source and design real acceptance |
| `AIDLC-014.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2276` | reconcile source and design real acceptance |
| `AIDLC-014.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2277` | reconcile source and design real acceptance |
| `AIDLC-014.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2278` | reconcile source and design real acceptance |
| `AIDLC-014.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2279` | reconcile source and design real acceptance |
| `AIDLC-015` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:180` | reconcile source and design real acceptance |
| `AIDLC-015.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2334` | reconcile source and design real acceptance |
| `AIDLC-015.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2335` | reconcile source and design real acceptance |
| `AIDLC-015.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2336` | reconcile source and design real acceptance |
| `AIDLC-015.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2337` | reconcile source and design real acceptance |
| `AIDLC-016` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:178` | reconcile source and design real acceptance |
| `AIDLC-016.1` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2294` | reconcile source and design real acceptance |
| `AIDLC-016.2` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2295` | reconcile source and design real acceptance |
| `AIDLC-016.3` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2296` | reconcile source and design real acceptance |
| `AIDLC-016.4` | AIDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2297` | reconcile source and design real acceptance |
| `PUR-APU-001` | APU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:356](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-APU-002` | APU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:357](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-APU-003` | APU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:358](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-APU-004` | APU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:359](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-APU-005` | APU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:360](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `ASPEII-E2E-01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:736](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:737](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:738](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:739](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:740](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:741](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-07` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:742](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-08` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:743](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-09` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:744](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-10` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:745](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-11` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:746](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-12` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:747](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-13` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:748](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-14` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:749](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-15` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:750](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-E2E-16` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:751](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:653](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:654](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:655](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:656](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:657](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:658](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-07` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:659](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-08` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:660](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-PROF-09` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:661](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:200](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:193](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:194](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:195](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:196](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:197](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-001.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:198](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:213](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:206](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:207](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:208](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:209](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:210](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-002.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:211](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:226](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:219](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:220](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:221](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:222](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:223](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-003.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:224](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:239](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:232](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:233](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:234](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:235](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:236](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-004.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:237](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:252](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:245](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:246](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:247](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:248](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:249](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-005.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:250](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:265](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:258](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:259](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:260](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:261](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:262](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-006.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:263](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:278](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:271](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:272](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:273](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:274](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:275](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-007.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:276](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:291](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:284](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:285](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:286](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:287](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:288](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-008.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:289](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:304](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:297](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:298](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:299](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:300](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:301](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-009.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:302](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:317](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:310](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:311](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:312](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:313](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:314](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-010.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:315](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:330](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:323](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:324](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:325](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:326](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:327](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-011.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:328](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:343](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:336](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:337](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:338](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:339](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:340](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-012.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:341](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:356](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:349](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:350](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:351](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:352](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:353](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-013.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:354](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:369](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:362](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:363](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:364](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:365](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:366](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-014.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:367](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:382](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:375](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:376](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:377](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:378](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:379](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-015.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:380](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:395](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:388](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:389](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:390](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:391](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:392](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-016.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:393](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:408](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:401](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:402](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:403](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:404](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:405](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-017.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:406](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:421](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:414](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:415](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:416](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:417](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:418](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-018.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:419](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:434](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:427](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:428](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:429](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:430](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:431](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-019.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:432](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:447](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:440](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:441](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:442](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:443](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:444](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-020.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:445](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:460](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:453](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:454](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:455](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:456](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:457](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-021.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:458](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:473](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:466](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:467](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:468](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:469](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:470](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-022.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:471](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:486](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:479](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:480](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:481](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:482](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:483](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-023.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:484](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:499](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:492](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:493](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:494](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:495](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:496](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-024.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:497](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:512](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:505](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:506](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:507](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:508](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:509](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-025.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:510](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:525](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:518](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:519](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:520](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:521](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:522](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-026.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:523](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:538](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:531](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:532](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:533](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:534](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:535](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-027.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:536](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:551](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:544](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:545](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:546](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:547](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:548](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-028.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:549](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:564](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:557](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:558](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:559](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:560](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:561](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-029.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:562](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:577](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:570](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:571](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:572](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:573](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:574](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-030.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:575](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:590](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:583](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:584](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:585](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:586](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:587](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-031.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:588](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:603](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:596](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:597](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:598](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:599](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:600](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-032.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:601](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:616](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:609](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:610](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:611](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:612](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:613](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-033.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:614](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:629](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:622](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:623](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:624](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:625](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:626](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-034.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:627](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:642](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:635](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:636](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:637](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:638](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:639](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-035.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:640](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.ACC` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:655](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.C01` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:648](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.C02` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:649](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.C03` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:650](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.C04` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:651](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.C05` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:652](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-RQ-036.C06` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-reqirements.md:653](aspeii-reqirements.md) | reconcile source and design real acceptance |
| `ASPEII-WP01.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:154](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP02.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:167](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP03.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:181](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP04.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:195](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP05.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:208](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP06.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:222](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP07.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:235](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP08.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:249](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP09.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:262](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP10.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:277](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP11.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:290](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP12.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:305](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP13.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:319](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP14.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:332](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP15.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:346](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP16.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:360](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP17.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:374](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `ASPEII-WP18.GATE` | ASPEII | W02 | untriaged | `UNTRIAGED` | [aspeii-implementation-plan.md:387](aspeii-implementation-plan.md) | reconcile source and design real acceptance |
| `BASE-01` | BASE | W00 | untriaged | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:33` | reconcile source and design real acceptance |
| `BASE-02` | BASE | W00 | untriaged | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:215` | reconcile source and design real acceptance |
| `BASE-03` | BASE | W00 | untriaged | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:218` | reconcile source and design real acceptance |
| `BASE-04` | BASE | W00 | untriaged | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:160` | reconcile source and design real acceptance |
| `CG-CODE-01` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/17-code-graph.md:18](EOIP-engg-doc-pkg/17-code-graph.md) | reconcile source and design real acceptance |
| `CG-CODE-02` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/17-code-graph.md:28](EOIP-engg-doc-pkg/17-code-graph.md) | reconcile source and design real acceptance |
| `CG-DEV-2026-10-11` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:3](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-DOC-01` | CG | W00 | untriaged | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:238` | reconcile source and design real acceptance |
| `CG-GAP-001` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:62](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-002` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:63](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-003` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:64](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-004` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:65](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-005` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:66](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-006` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:67](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-007` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:68](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CG-GAP-008` | CG | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:69](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | execute complete entrypoint and negative cases |
| `CG-GAP-009` | CG | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md:70](EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md) | reconcile source and design real acceptance |
| `CIP-E2E-01` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:338](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-E2E-02` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:342](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-E2E-03` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:346](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-E2E-04` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:350](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-E2E-05` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:354](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-NEG-01` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:331](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-02` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:332](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-03` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:333](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-04` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:334](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-05` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:335](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-06` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:336](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-07` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:337](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-08` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:338](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-09` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:339](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-10` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:340](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-11` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:341](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-12` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:342](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-NEG-13` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:343](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P0.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:108](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P0.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:108](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P0.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:108](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P0.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:108](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P0.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:108](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P0.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:117](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P1.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:122](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P1.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:122](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P1.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:122](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P1.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:122](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P1.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:130](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P2.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:135](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P2.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:135](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P2.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:135](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P2.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:135](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P2.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:135](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P2.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:143](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P3.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:148](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P3.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:148](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P3.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:148](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P3.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:148](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P3.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:148](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P3.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:157](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:162](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:162](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:162](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:162](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:162](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.6` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:162](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P4.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:171](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P5.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:176](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P5.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:176](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P5.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:176](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P5.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:176](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P5.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:176](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P5.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:185](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P6.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:190](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P6.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:190](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P6.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:190](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P6.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:190](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P6.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:190](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P6.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:199](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P7.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:204](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P7.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:204](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P7.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:204](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P7.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:204](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P7.5` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:204](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P7.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:213](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P8.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:218](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P8.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:218](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P8.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:218](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P8.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:218](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-P8.GATE` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:226](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-01` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:351](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-02` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:352](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-03` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:353](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-04` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:354](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-05` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:355](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-06` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:356](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-07` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:357](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-08` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:358](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-09` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:359](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-REL-10` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-implementation-plan.md:360](community-ip-implementation-plan.md) | reconcile source and design real acceptance |
| `CIP-RQ-001.AC-001.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:126](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-001.AC-001.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:126](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-001.AC-001.3` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:126](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-001.AC-001.4` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:126](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-002.AC-002.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:132](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-002.AC-002.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:132](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-003.AC-003.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:138](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-003.AC-003.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:138](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-004.AC-004.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:144](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-004.AC-004.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:144](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-005.AC-005.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:150](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-005.AC-005.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:150](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-006.AC-006.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:156](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-006.AC-006.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:156](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-007.AC-007.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:162](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-007.AC-007.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:162](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-008.AC-008.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:168](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-008.AC-008.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:168](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-009.AC-009.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:174](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-009.AC-009.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:174](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-010.AC-010.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:180](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-010.AC-010.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:180](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-011.AC-011.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:186](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-011.AC-011.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:186](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-012.AC-012.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:192](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-012.AC-012.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:192](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-013.AC-013.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:198](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-013.AC-013.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:198](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-014.AC-014.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:204](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-014.AC-014.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:204](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-015.AC-015.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:210](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-015.AC-015.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:210](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-016.AC-016.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:216](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-016.AC-016.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:216](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-017.AC-017.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:222](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-017.AC-017.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:222](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-018.AC-018.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:228](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-018.AC-018.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:228](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-019.AC-019.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:234](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-019.AC-019.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:234](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-020.AC-020.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:240](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-020.AC-020.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:240](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-021.AC-021.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:246](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-021.AC-021.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:246](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-022.AC-022.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:252](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-022.AC-022.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:252](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-023.AC-023.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:258](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-023.AC-023.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:258](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-024.AC-024.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:283](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-024.AC-024.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:283](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-025.AC-025.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:289](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-025.AC-025.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:289](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-026.AC-026.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:295](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-026.AC-026.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:295](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-027.AC-027.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:301](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-027.AC-027.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:301](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-028.AC-028.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:307](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-028.AC-028.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:307](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-029.AC-029.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:313](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-029.AC-029.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:313](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-030.AC-030.1` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:321](community-ip-requirements.md) | reconcile source and design real acceptance |
| `CIP-RQ-030.AC-030.2` | CIP | W00 | untriaged | `UNTRIAGED` | [community-ip-requirements.md:321](community-ip-requirements.md) | reconcile source and design real acceptance |
| `COMPLY-001` | COMPLY | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:836](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `COMPLY-001.1` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1166` | reconcile source and design real acceptance |
| `COMPLY-001.2` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1167` | reconcile source and design real acceptance |
| `COMPLY-001.3` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1168` | reconcile source and design real acceptance |
| `COMPLY-001.4` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1169` | reconcile source and design real acceptance |
| `COMPLY-001.5` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1170` | reconcile source and design real acceptance |
| `COMPLY-002` | COMPLY | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:854](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `COMPLY-002.1` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1190` | reconcile source and design real acceptance |
| `COMPLY-002.2` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1191` | reconcile source and design real acceptance |
| `COMPLY-002.3` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1192` | reconcile source and design real acceptance |
| `COMPLY-002.4` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1193` | reconcile source and design real acceptance |
| `COMPLY-002.5` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1194` | reconcile source and design real acceptance |
| `COMPLY-003` | COMPLY | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:872](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `COMPLY-003.1` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1212` | reconcile source and design real acceptance |
| `COMPLY-003.2` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1213` | reconcile source and design real acceptance |
| `COMPLY-003.3` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1214` | reconcile source and design real acceptance |
| `COMPLY-003.4` | COMPLY | W11 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1215` | reconcile source and design real acceptance |
| `PUR-CON-001` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:132](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-002` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:133](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-003` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:134](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-004` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:135](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-005` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:136](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-006` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:137](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-007` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:138](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-008` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:139](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-009` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:140](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CON-010` | CON | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:141](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `CONN-01` | CONN | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:493` | execute complete entrypoint and negative cases |
| `CONN-02` | CONN | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:496` | execute complete entrypoint and negative cases |
| `CONN-03` | CONN | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:499` | execute complete entrypoint and negative cases |
| `CORE-001` | CORE | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:20](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `CORE-001.1` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:235` | reconcile source and design real acceptance |
| `CORE-001.2` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:236` | reconcile source and design real acceptance |
| `CORE-001.3` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:237` | reconcile source and design real acceptance |
| `CORE-001.4` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:238` | reconcile source and design real acceptance |
| `CORE-001.5` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:239` | reconcile source and design real acceptance |
| `CORE-001.6` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:240` | reconcile source and design real acceptance |
| `CORE-001.7` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:241` | reconcile source and design real acceptance |
| `CORE-002` | CORE | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:45](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `CORE-002.1` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:265` | reconcile source and design real acceptance |
| `CORE-002.2` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:266` | reconcile source and design real acceptance |
| `CORE-002.3` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:267` | reconcile source and design real acceptance |
| `CORE-002.4` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:268` | reconcile source and design real acceptance |
| `CORE-002.5` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:269` | reconcile source and design real acceptance |
| `CORE-002.6` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:270` | reconcile source and design real acceptance |
| `CORE-002.7` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:271` | reconcile source and design real acceptance |
| `CORE-002.8` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:272` | reconcile source and design real acceptance |
| `CORE-003` | CORE | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:72](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `CORE-003.1` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:296` | reconcile source and design real acceptance |
| `CORE-003.2` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:297` | reconcile source and design real acceptance |
| `CORE-003.3` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:298` | reconcile source and design real acceptance |
| `CORE-003.4` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:299` | reconcile source and design real acceptance |
| `CORE-003.5` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:300` | reconcile source and design real acceptance |
| `CORE-003.6` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:301` | reconcile source and design real acceptance |
| `CORE-003.7` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:302` | reconcile source and design real acceptance |
| `CORE-003.8` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:303` | reconcile source and design real acceptance |
| `CORE-004` | CORE | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:99](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `CORE-004.1` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:327` | reconcile source and design real acceptance |
| `CORE-004.2` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:328` | reconcile source and design real acceptance |
| `CORE-004.3` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:329` | reconcile source and design real acceptance |
| `CORE-004.4` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:330` | reconcile source and design real acceptance |
| `CORE-004.5` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:331` | reconcile source and design real acceptance |
| `CORE-004.6` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:332` | reconcile source and design real acceptance |
| `CORE-004.7` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:333` | reconcile source and design real acceptance |
| `CORE-004.8` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:334` | reconcile source and design real acceptance |
| `CORE-005` | CORE | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:126](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `CORE-005.1` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:352` | reconcile source and design real acceptance |
| `CORE-005.2` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:353` | reconcile source and design real acceptance |
| `CORE-005.3` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:354` | reconcile source and design real acceptance |
| `CORE-005.4` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:355` | reconcile source and design real acceptance |
| `CORE-005.5` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:356` | reconcile source and design real acceptance |
| `CORE-006` | CORE | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:146](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `CORE-006.1` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:377` | reconcile source and design real acceptance |
| `CORE-006.2` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:378` | reconcile source and design real acceptance |
| `CORE-006.3` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:379` | reconcile source and design real acceptance |
| `CORE-006.4` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:380` | reconcile source and design real acceptance |
| `CORE-006.5` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:381` | reconcile source and design real acceptance |
| `CORE-006.6` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:382` | reconcile source and design real acceptance |
| `CORE-006.7` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:383` | reconcile source and design real acceptance |
| `CORE-006.8` | CORE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:384` | reconcile source and design real acceptance |
| `PUR-CPU-001` | CPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:295](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CPU-002` | CPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:296](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CPU-003` | CPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:297](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CPU-004` | CPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:298](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-CPU-005` | CPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:299](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `CRA-001.12` | CRA | W01 | claimed_accepted | `ACCEPTED` | `CRA` | independently verify claim and runtime |
| `CRA-004.11` | CRA | W01 | claimed_accepted | `ACCEPTED` | `CRA` | independently verify claim and runtime |
| `CRA-001.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-001.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-001.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-001.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-001.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-002.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-002.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-002.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-002.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-002.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-002.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-003.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-003.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-003.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-003.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-003.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-003.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-004.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-004.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-004.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-004.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-004.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-004.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-005.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-005.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-005.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-005.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-005.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-006.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-006.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-006.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-006.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-006.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-007.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-007.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-007.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-007.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-007.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-008.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-008.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-008.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-008.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-008.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-009.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-009.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-009.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-009.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-009.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-010.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-010.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-010.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-010.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-010.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-011.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-011.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-011.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-011.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-011.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-012.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-012.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-012.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-012.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-012.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-013.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-013.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-013.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-013.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-013.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-014.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-014.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-014.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-014.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-014.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-015.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-015.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-015.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-015.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-015.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-016.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-016.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-016.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-016.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-016.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-017.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-017.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-017.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-017.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-017.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-018.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-018.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-018.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-018.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-018.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-019.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-019.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-019.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-019.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-019.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-019.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-020.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-020.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-020.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-020.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-020.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-020.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-021.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-021.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-021.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-021.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-021.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-022.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-022.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-022.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-022.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-022.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-023.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-023.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-023.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-023.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-023.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-024.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-024.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-024.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-024.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-024.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-024.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-025.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-025.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-025.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-025.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-025.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-026.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-026.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-026.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-026.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-026.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-026.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-027.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-027.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-027.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-027.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-027.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-028.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-028.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-028.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-028.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-028.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-029.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-029.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-029.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-029.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-029.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-030.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-030.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-030.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-030.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-030.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-030.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-031.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-031.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-031.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-031.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-031.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-032.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-032.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-032.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-032.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-032.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-033.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-033.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-033.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-033.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-033.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-034.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-034.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-034.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-034.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-034.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-035.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-035.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-035.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-035.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-035.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-036.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-036.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-036.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-036.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-036.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-036.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-037.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-037.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-037.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-037.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-037.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-037.6` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-038.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-038.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-038.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-038.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-038.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-039.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-039.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-039.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-039.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-039.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-040.1` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-040.2` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-040.3` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-040.4` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `CRA-040.5` | CRAr | W00 | claimed_accepted | `ACCEPTED` | `CRAr` | independently verify claim and runtime |
| `PUR-DAT-001` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:274](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-002` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:275](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-003` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:276](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-004` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:277](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-005` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:278](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-006` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:279](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-007` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:280](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DAT-008` | DAT | W04 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:281](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `DERIVED-LLM-SELF-001` | DERIVED | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/todo-status.md:20](EOIP-engg-doc-pkg/todo-status.md) | reconcile source and design real acceptance |
| `PUR-DPU-001` | DPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:335](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DPU-002` | DPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:336](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DPU-003` | DPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:337](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DPU-004` | DPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:338](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-DPU-005` | DPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:339](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-001` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:100](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-002` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:101](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-003` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:102](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-004` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:103](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-005` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:104](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-006` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:105](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-007` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:106](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-FND-008` | FND | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:107](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `FR-001` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:847](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-002` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:848](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-003` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:849](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:850](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-005` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:851](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-006` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:852](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-007` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:853](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-008` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:854](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-009` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:855](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-01` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:70](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `FR-010` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:856](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-011` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:857](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-012` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:858](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-013` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:859](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-014` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:860](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-015` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:861](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-016` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:862](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-017` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:863](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-018` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:864](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-019` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:865](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-02` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1081](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-020` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:866](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-021` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:867](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-022` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:868](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-023` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:869](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-024` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:870](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-025` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:871](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-026` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:872](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-027` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:873](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-028` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:874](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `FR-03` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1082](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-04` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1083](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-05` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1084](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-06` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1085](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-07` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1086](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-08` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1087](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FR-67` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:70](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `FR-ADMIN-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:645](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-ADMIN-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:655](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-AGENT-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:545](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-AGENT-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:555](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-AGENT-003` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/02-scope-and-objectives.md:26](EOIP-engg-doc-pkg/02-scope-and-objectives.md) | execute complete entrypoint and negative cases |
| `FR-AGENT-004` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:575](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-AGENT-005` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:585](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-CODE-001` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:325](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-CODE-002` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/02-scope-and-objectives.md:24](EOIP-engg-doc-pkg/02-scope-and-objectives.md) | reconcile source and design real acceptance |
| `FR-CODE-003` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:345](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-CODE-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:355](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-CODE-005` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:365](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-CONF-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:81](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-CONN-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:11](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-CONN-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/02-scope-and-objectives.md:22](EOIP-engg-doc-pkg/02-scope-and-objectives.md) | execute complete entrypoint and negative cases |
| `FR-CONN-003` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/02-scope-and-objectives.md:23](EOIP-engg-doc-pkg/02-scope-and-objectives.md) | reconcile source and design real acceptance |
| `FR-CONN-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:41](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-CONN-005` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:51](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-CONN-006` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:61](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-CONN-007` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:71](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-GRAPH-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/01-project-vision.md:22](EOIP-engg-doc-pkg/01-project-vision.md) | execute complete entrypoint and negative cases |
| `FR-GRAPH-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:161](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-GRAPH-003` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:171](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-GRAPH-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:181](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-GRAPH-005` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:191](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-GRAPH-006` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/01-project-vision.md:23](EOIP-engg-doc-pkg/01-project-vision.md) | reconcile source and design real acceptance |
| `FR-GRAPH-007` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:211](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-GRAPH-008` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:221](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-GRAPH-009` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:231](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-GRAPH-010` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:241](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-GRAPH-011` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/06-architecture.md:307](EOIP-engg-doc-pkg/06-architecture.md) | reconcile source and design real acceptance |
| `FR-GRAPH-012` | FR | W04 | untriaged | `UNTRIAGED` | [docs/audit-2026-10-06/assessed-gap-report.md:171](docs/audit-2026-10-06/assessed-gap-report.md) | reconcile source and design real acceptance |
| `FR-ID-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:295](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-ID-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:305](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-INGEST-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:101](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-INGEST-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:111](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-INGEST-003` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:121](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-INGEST-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:131](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-INGEST-005` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:141](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-KGR-001` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:99](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-002` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:171](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-003` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:232](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:244](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-005` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:306](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-006` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:344](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-007` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:354](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-008` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:373](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-009` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:384](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-010` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1298](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-011` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1495](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-012` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1329](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-013` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1403](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-014` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1434](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-015` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1464](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-016` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-implementation-plan.md:1520](EOIP-engg-doc-pkg/KGR-implementation-plan.md) | reconcile source and design real acceptance |
| `FR-KGR-017` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:492](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-018` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:504](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-019` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:519](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-020` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:530](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-021` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:542](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-022` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:553](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-023` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:564](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-024` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:575](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-025` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:589](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-026` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:600](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-027` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:611](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-028` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:642](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-029` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:666](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-KGR-030` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:685](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `FR-MCP-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:605](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-MCP-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:615](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-MEM-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:595](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-ONTO-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:255](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-ONTO-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:265](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-PROV-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/01-project-vision.md:24](EOIP-engg-doc-pkg/01-project-vision.md) | execute complete entrypoint and negative cases |
| `FR-PROV-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:285](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:375](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:385](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-003` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/01-project-vision.md:25](EOIP-engg-doc-pkg/01-project-vision.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:405](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-QUERY-005` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:415](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-006` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:425](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-007` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:435](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-008` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:445](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-QUERY-009` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/25-query-engine-requirements.md:30](EOIP-engg-doc-pkg/25-query-engine-requirements.md) | reconcile source and design real acceptance |
| `FR-RAG-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:485](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-RAG-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/01-project-vision.md:26](EOIP-engg-doc-pkg/01-project-vision.md) | execute complete entrypoint and negative cases |
| `FR-RAG-003` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:505](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-RAG-004` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/02-scope-and-objectives.md:25](EOIP-engg-doc-pkg/02-scope-and-objectives.md) | reconcile source and design real acceptance |
| `FR-RAG-005` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:525](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-RAG-006` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:535](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-SNOW-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:91](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-TEMP-001` | FR | W04 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:315](EOIP-engg-doc-pkg/03-functional-requirements.md) | reconcile source and design real acceptance |
| `FR-UI-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:625](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-UI-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:635](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-VALID-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:455](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-VALID-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:465](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-VALID-003` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:475](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-VSCODE-001` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:665](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FR-VSCODE-002` | FR | W04 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/03-functional-requirements.md:675](EOIP-engg-doc-pkg/03-functional-requirements.md) | execute complete entrypoint and negative cases |
| `FRD-001` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-001-008` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2078](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-002` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-003` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-004` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-005` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-006` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-007` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-100` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-101` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-102` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-103` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-200` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-201` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-202` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-300` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-301` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-302` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `FRD-321` | FRD | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:2054](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `G2-ADMIN-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1090](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1554](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1557](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1560](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1563](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1566](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1569](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1572](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1575](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1578](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-011` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1581](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-012` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1584](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-013` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1587](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-014` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1590](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-015` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1593](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-016` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1596](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ADMIN-017` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1599](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:57](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:56](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:68](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:72](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:76](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:80](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:84](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:88](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:92](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:96](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-011` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:100](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-012` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:104](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-013` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:108](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-014` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:112](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCH-015` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:116](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCHC-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:821](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-ARCHC-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1113](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-ARCHC-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1116](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-ARCHC-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1123](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-ARCHC-005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1126](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-ARCHC-006` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1129](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-ARCHC-007` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1132](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-ARCHC-008` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1135](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-ARCHC-009` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1138](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-CAP-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:944](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-CAP-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1289](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAP-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1292](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAP-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1295](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAP-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1298](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAP-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1308](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAUSE-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1017](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-CAUSE-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1150](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAUSE-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1157](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAUSE-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1160](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAUSE-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1168](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-CAUSE-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1171](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:139](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:175](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:58](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:204](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:207](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-006` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:215](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-007` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:218](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-008` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:221](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-009` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:224](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:227](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-011` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:230](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-012` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:238](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-013` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:241](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-014` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:250](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-015` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:259](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-016` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:262](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-017` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:265](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-018` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:272](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-019` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:275](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-020` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:287](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-021` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:290](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-022` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:301](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-023` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:304](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-024` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:307](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-025` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:310](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-026` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:319](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EKAF-027` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:322](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-028` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:334](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-029` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:337](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EKAF-030` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:340](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-EVENT-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:60](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-EVENT-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:835](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVENT-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:838](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVENT-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:841](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVENT-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:844](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVENT-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:855](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVENT-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:858](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:268](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:706](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:711](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:714](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:717](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:720](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:723](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:726](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:59](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:743](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-011` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:746](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-012` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:749](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-013` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:752](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-014` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:755](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-015` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:758](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-EVOL-016` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:761](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-API-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:524](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-API-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:870](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-API-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:879](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-BIZ-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:984](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-BIZ-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:994](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-BIZ-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:997](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-DEC-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:949](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-DEC-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:961](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-DEC-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:964](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-OBS-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:618](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-OBS-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:899](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-OBS-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:902](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-PROC-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:971](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-PROC-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:974](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-PROC-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:977](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-RUNTIME-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:619](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-RUNTIME-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:912](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-RUNTIME-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:915](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-SEC-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:620](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-SEC-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:925](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-SEC-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:928](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-TEST-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:935](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-TEST-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:939](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-GRAPH-TEST-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:942](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-I2R-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:748](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-I2R-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1352](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-I2R-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1355](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-I2R-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1358](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-I2R-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1361](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:942](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1183](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1186](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1189](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1192](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1195](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1198](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1201](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1204](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1207](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-011` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1210](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-012` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1213](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-IMMUNE-013` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1216](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-JOURNAL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:269](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-JOURNAL-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:776](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-JOURNAL-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:789](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-JOURNAL-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:797](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-JOURNAL-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:800](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-JOURNAL-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:803](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-KD-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:823](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-KD-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1371](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-KD-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1386](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-KD-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1395](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-KD-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1398](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-KD-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1401](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OBS-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:141](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-OBS-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1705](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OBS-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1714](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OBS-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1720](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OBS-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1723](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OBS-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1726](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OEVO-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:943](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-OEVO-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1226](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OEVO-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1229](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OEVO-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1238](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OEVO-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1241](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-OEVO-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1244](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-P0` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:35](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P0-001` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:74](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `G2-P1` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:36](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P10` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:45](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P10-040` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:74](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `G2-P2` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:37](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P3` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:38](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P4` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:39](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P5` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:40](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P6` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:41](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P7` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:42](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P8` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:43](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-P9` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:44](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-PERF-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1735](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1738](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1741](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1744](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1747](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1750](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1753](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PERF-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1756](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PM-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:822](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-PM-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1254](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PM-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1257](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PM-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1266](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-PM-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1269](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:825](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-QOP-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1320](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1018](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-QOP-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1326](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1329](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1332](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1335](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1338](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-QOP-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1341](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:271](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-REL-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1766](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1769](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1772](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1775](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1778](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1781](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REL-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1784](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-REQ-34` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/reference/g2-traceability.md:63](EOIP-engg-doc-pkg/reference/g2-traceability.md) | reconcile source and design real acceptance |
| `G2-SEC-CRAWL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:140](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1665](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1668](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1671](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1674](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1677](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1680](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1683](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1686](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1689](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-011` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1692](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SEC-CRAWL-012` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1695](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SIM-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1016](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SIM-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1070](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SIM-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1073](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SIM-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1083](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SIM-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1091](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SIM-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1094](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SIM-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1097](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SLO-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:824](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SLO-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1418](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SLO-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1421](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SLO-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1424](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SLO-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1427](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-API-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:523](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-API-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:480](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-API-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:483](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-API-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:487](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-API-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:490](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-API-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:493](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CICD-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:611](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CICD-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:578](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CICD-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:582](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CICD-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:585](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CODE-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:419](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CODE-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:461](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-CODE-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:464](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-CODE-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:467](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-CODE-005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:470](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-CONF-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:520](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CONF-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:375](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CONF-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:378](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CONF-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:381](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-CONF-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:384](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-DD-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:613](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-DD-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:529](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-DD-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:532](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-DD-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:535](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GH-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:418](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-GH-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:429](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GH-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:432](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GH-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:435](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:417](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-GL-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:445](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GL-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:448](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GL-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:451](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GRAF-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:614](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-GRAF-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:545](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-GRAF-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:549](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-JIRA-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:416](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-JIRA-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:353](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-JIRA-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:356](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-JIRA-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:359](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-JIRA-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:362](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-JIRA-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:365](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-KIB-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:612](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-KIB-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:503](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-KIB-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:506](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-KIB-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:509](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-KIB-005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:519](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-SRC-OTEL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:615](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-OTEL-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:559](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-OTEL-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:562](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-OTEL-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:565](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-OTEL-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:568](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-RUNTIME-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:616](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-RUNTIME-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:595](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-RUNTIME-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:598](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SBOM-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:617](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SBOM-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:608](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SBOM-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:612](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SBOM-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:615](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNKB-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:521](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNKB-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:394](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNKB-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:397](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNOW-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:522](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNOW-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:407](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNOW-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:410](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNOW-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:413](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNOW-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:416](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-SNOW-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:419](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-WEB-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:420](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SRC-WEB-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:626](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-WEB-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:629](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-WEB-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:632](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SRC-WEB-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:635](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:267](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:645](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:655](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:658](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:661](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:664](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:667](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:670](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-009` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:673](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-010` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:676](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-011` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:679](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-012` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:682](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-013` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:685](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-SYNC-014` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:688](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-T0001` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:64](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:78](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:90](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:102](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:105](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0006` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:119](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0101` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:145](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0102` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:148](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0103` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:151](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0104` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:154](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0110` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:161](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0111` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:170](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0112` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:173](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0120` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:180](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0121` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:183](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0122` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:186](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0123` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:189](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0130` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:196](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0131` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:205](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0132` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:208](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0133` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:216](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0134` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:219](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0135` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:222](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0140` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:229](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0141` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:232](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0142` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:235](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0150` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:242](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0151` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:245](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0152` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:248](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0153` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:251](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0201` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:277](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0202` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:282](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0203` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:291](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0210` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:298](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0211` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:301](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0212` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:304](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0213` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:312](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0220` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:319](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0221` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:322](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0222` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:330](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0223` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:333](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0224` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:336](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0225` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:339](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0230` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:346](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0231` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:349](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0232` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:352](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0240` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:359](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0241` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:362](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0242` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:365](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0243` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:371](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0250` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:378](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0251` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:381](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0252` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:384](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0253` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:387](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0301` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:426](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0302` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:433](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0303` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:436](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0304` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:439](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0310` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:446](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0311` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:449](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0312` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:452](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0313` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:455](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0320` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:462](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0321` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:465](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0322` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:468](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0323` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:471](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0330` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:478](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0331` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:481](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0332` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:484](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0333` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:487](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0340` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:494](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0341` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:497](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0342` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:500](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0401` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:530](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0402` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:533](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0403` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:536](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0404` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:539](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0405` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:542](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0410` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:551](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0411` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:554](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0412` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:557](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0413` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:560](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0414` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:563](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0415` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:566](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0416` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:569](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0420` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:576](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0421` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:579](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0422` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:582](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0423` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:585](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0424` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:588](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0425` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:591](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0426` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:594](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0501` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:627](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0502` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:630](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0503` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:633](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0504` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:636](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0510` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:643](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0511` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:646](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0512` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:649](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0513` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:652](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0520` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:659](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0521` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:662](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0522` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:665](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0523` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:668](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0530` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:675](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0531` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:678](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0532` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:681](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0540` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:688](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0541` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:691](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0542` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:694](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0543` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:697](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0550` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:704](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0551` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:707](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0560` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:714](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0561` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:717](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0562` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:720](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0563` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:723](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0601` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:754](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0602` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:757](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0603` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:760](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0610` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:767](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0611` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:770](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0612` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:773](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0620` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:780](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0621` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:783](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0622` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:786](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0630` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:793](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0631` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:800](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0632` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:803](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0701` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:831](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0702` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:834](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0703` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:837](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0704` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:840](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0705` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:843](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0710` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:850](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0711` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:853](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0712` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:856](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0713` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:859](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0714` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:862](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0715` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:865](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0720` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:872](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0721` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:875](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0722` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:878](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0723` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:881](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0730` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:888](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0731` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:891](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0732` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:894](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0733` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:897](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0740` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:904](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0741` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:907](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0742` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:910](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0743` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:913](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0750` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:920](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0751` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:923](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0752` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:926](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0753` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:929](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0801` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:950](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0802` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:953](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0803` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:956](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0804` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:959](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0805` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:962](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0810` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:969](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0811` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:972](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0812` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:975](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0813` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:978](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0814` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:981](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0820` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:988](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0821` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:991](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0822` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:994](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0823` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:997](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0824` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1000](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0901` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1024](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0902` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1027](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0903` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1030](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0904` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1033](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0905` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1036](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0906` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1039](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0910` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1046](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0911` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1049](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0912` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1052](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0920` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1059](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0921` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1062](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0922` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1065](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0923` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1068](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T0924` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1071](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1030` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1154](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1031` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1157](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1032` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1160](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1033` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1163](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1040` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1170](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1041` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1173](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1042` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1176](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1043` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1179](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1044` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1182](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1045` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1185](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-T1046` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1188](EOIP-engg-doc-pkg/gaps2-implementation.md) | reconcile source and design real acceptance |
| `G2-TEL-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:621](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-TEL-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1637](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TEL-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1640](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TEL-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1643](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TEL-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1646](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TEL-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1649](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TEL-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1652](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TEL-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1655](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TIME-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:820](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-TIME-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1045](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TIME-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1048](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TIME-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1051](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TIME-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1054](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TIME-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1057](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TIME-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1060](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TWIN-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:747](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-TWIN-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1008](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TWIN-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1025](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TWIN-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1028](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-TWIN-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1031](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-UX-GRAPH-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1088](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-UX-GRAPH-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1477](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1480](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1483](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1486](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-006` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1489](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-007` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1492](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-008` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1495](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-009` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1498](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-010` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1501](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-011` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1504](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-012` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1507](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-013` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1510](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-014` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1513](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-015` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1516](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-GRAPH-016` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1519](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-LENS-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1087](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-UX-LENS-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1464](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-UX-LENS-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1467](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-UX-PLAY-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1089](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-UX-PLAY-002` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1529](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-PLAY-003` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1538](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-PLAY-004` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1541](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-UX-PLAY-005` | G2 | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1544](EOIP-engg-doc-pkg/gaps2-requirements.md) | reconcile source and design real acceptance |
| `G2-VSC-001` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-implementation.md:1091](EOIP-engg-doc-pkg/gaps2-implementation.md) | execute complete entrypoint and negative cases |
| `G2-VSC-002` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1609](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-VSC-003` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1612](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-VSC-004` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1615](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-VSC-005` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1618](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-VSC-006` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1621](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-VSC-007` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1624](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `G2-VSC-008` | G2 | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps2-requirements.md:1627](EOIP-engg-doc-pkg/gaps2-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-001` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:73](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `GAP-002` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1342](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-003` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1343](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-004` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1344](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-005` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1345](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-006` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1346](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-007` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1347](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-008` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1348](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-009` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1349](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `GAP-296` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:73](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `GAP-AGOV-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:55](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:715](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:716](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:717](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:718](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:719](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:720](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:721](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:722](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:723](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-011` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:724](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AGOV-012` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:725](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AI` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-AI-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:147](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:601](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:696](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:697](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:698](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:699](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:700](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:701](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:702](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:703](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-AKO-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:704](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-APP` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-APP-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:783](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-APP-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:274](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ARCH-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:382](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-ARCH-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:535](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ARCH-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:536](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ARCH-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:537](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ARCH-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:538](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ARCH-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:539](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CACHE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:462](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-CACHE-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:889](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CACHE-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:890](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CACHE-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:891](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CACHE-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:892](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CATALOG` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-CATALOG-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:538](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-CATALOG-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:297](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CATALOG-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:298](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CATALOG-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:299](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CATALOG-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:300](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CDC-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:803](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CDC-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:804](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CDC-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:805](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CDC-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:806](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CDC-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:807](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CDC-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:808](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CHANGE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:383](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-CHANGE-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:548](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CHANGE-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:549](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CHANGE-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:550](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CHANGE-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:559](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CHANGE-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:560](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CONTRACT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:292](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-CONTRACT-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:440](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CONTRACT-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:441](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CONTRACT-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:442](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CONTRACT-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:443](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CONTRACT-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:444](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:50](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-CP-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:400](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:401](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:402](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:403](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:404](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:405](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:406](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-CP-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:407](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DATAOPS-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:542](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-DBAGNOSTIC-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:53](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:513](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:514](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:515](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:516](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:517](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:518](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DRIFT-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:519](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DUAL` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-DUAL-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:142](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-DUAL-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:143](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ENG-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:121](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:621](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:622](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:623](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:624](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:625](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:626](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:627](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:628](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:629](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-ER-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:630](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-EXPORT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:339](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-EXT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:785](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/06-architecture.md:125](EOIP-engg-doc-pkg/06-architecture.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:639](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:640](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:641](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:642](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:643](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:644](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FABRIC-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:645](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FED` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-FED-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:536](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-FED-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:118](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FED-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:119](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FED-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:120](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FRESH-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:384](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-FRESH-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1002](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FRESH-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1003](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FRESH-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1004](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-FRESH-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1005](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GDS` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-GDS-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:731](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-GDS-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:145](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:291](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:418](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:419](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:427](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:428](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:429](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:430](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GITOPS-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:431](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GOV` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-GOV-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:298](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-GOV-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:198](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GOV-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:199](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GRAG-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:461](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-GRAG-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:359](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GRAG-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:360](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GRAG-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:361](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GRAG-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:362](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GRAG-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:363](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-GRAPHTEST-001` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/reference/g2-traceability.md:74](EOIP-engg-doc-pkg/reference/g2-traceability.md) | reconcile source and design real acceptance |
| `GAP-HA` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-HA-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:664](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-HG-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:51](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-HG-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:168](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-HG-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1076](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1077](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1078](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1079](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1080](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1081](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1082](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-HG-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:1083](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-IDE` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-IDE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:173](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:603](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:736](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:737](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:738](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:739](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:740](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:741](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KFW-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:742](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KGCI-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:820](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KGCI-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:821](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KGCI-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:822](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KGCI-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:823](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KP-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:539](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-KP-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:582](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KP-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:593](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KP-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:594](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KP-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:595](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KQ-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:293](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-KQ-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:490](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KQ-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:502](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KQ-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:503](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KQ-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:504](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KQ-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:505](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:170](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:677](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:678](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:679](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:680](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:681](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:682](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:683](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:684](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-KRAG-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:685](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LAYER-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:540](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-LAYER-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:252](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIFE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:900](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIFE-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:901](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIFE-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:902](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIFE-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:903](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIFE-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:904](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIFE-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:905](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIN-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:541](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-LIN-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:792](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIN-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:793](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIN-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:794](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LIN-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:795](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-LITE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:665](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-LITE-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:254](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MIGRATION-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:340](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:782](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:916](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:917](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:918](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:919](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:920](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:921](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-MKT-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:922](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-NLP` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-NLP-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:222](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-NOCODE` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-NOCODE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:194](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-NOCODE-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:195](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-NOCODE-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:196](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-OBS-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:54](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-OBS-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:856](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-OBS-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:857](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-OBS-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:858](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-OBS-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:859](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-OFFLINE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:172](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-OPS-001` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/06-architecture.md:126](EOIP-engg-doc-pkg/06-architecture.md) | reconcile source and design real acceptance |
| `GAP-PACK-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:224](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PERF-001` | GAP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/reference/deployment-ha.md:126](EOIP-engg-doc-pkg/reference/deployment-ha.md) | reconcile source and design real acceptance |
| `GAP-PERF-002` | GAP | W00 | untriaged | `UNTRIAGED` | [docs/audit-2026-10-06/assessed-gap-report.md:452](docs/audit-2026-10-06/assessed-gap-report.md) | reconcile source and design real acceptance |
| `GAP-PORT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:52](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:167](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:455](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:456](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:457](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:458](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:459](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:460](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:461](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-PROV-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:462](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QI-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:463](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-QI-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:874](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QI-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:875](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QI-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:876](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QI-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:877](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QI-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:878](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QI-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:169](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-QI-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:880](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-QUERY` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-QUERY-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:321](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-REC` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-REC-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:223](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RET-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:458](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-RET-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:656](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RET-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:665](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RET-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:666](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RET-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:667](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RET-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:668](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RULE` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-RULE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:170](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RULE-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:171](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-RULE-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:172](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:166](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:382](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:383](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:384](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:381](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:386](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:387](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SDT-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:388](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SEARCH-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:459](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-SEARCH-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:169](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:783](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1603](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1604](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1605](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1606](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1607](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1608](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | execute complete entrypoint and negative cases |
| `GAP-SEC-008` | GAP | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:997` | execute complete entrypoint and negative cases |
| `GAP-SEC-009` | GAP | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1008` | execute complete entrypoint and negative cases |
| `GAP-SEC-010` | GAP | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1009` | execute complete entrypoint and negative cases |
| `GAP-SEC-011` | GAP | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1010` | execute complete entrypoint and negative cases |
| `GAP-SEC-012` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:783](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-SEM-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:146](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:296](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:604](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:605](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:606](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:607](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:608](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:609](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:610](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:611](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:612](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-STUDIO-011` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:613](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TAX-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:297](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-TCO-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:225](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMP-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:568](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMP-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:569](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMP-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:570](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMP-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:571](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMP-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:572](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMP-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:573](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TEMPLATE` | GAP | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `GAP-TEMPLATE-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:784](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-TRUST-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:295](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-TRUST-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:751](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUST-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:752](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUST-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:760](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUST-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:761](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-implementation.md:294](EOIP-engg-doc-pkg/gaps-implementation.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-002` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:471](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-003` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:472](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-004` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:473](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-005` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:474](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-006` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:475](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-007` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:476](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-008` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:477](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-009` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:478](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-TRUTH-010` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:479](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `GAP-UX-001` | GAP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/gaps-requirements.md:200](EOIP-engg-doc-pkg/gaps-requirements.md) | execute complete entrypoint and negative cases |
| `CRA-001.13` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-014.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-023.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-025.8` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-025.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-028.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-035.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-036.10` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-037.11` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.1` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.2` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.3` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.4` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.5` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.6` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.7` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.8` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-043.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.1` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.10` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.11` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.2` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.3` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.4` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.5` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.6` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.7` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.8` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `CRA-044.9` | GN | W00 | claimed_accepted | `ACCEPTED` | `GN` | independently verify claim and runtime |
| `GN-001` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:535](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:595](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:596](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:597](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:598](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:599](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:600](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-001.D07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:601](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:605](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:657](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:658](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:659](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:660](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:661](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-002.D06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:662](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-003` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:666](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-003.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:692](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-003.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:693](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-003.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:694](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-004` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:698](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-004.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:724](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-004.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:725](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-004.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:726](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-004.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:727](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-004.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:728](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-005` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:732](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-005.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:764](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-005.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:765](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-005.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:766](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-005.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:767](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-006` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:771](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-006.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:795](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-006.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:796](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-006.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:797](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-006.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:798](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-007` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:802](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-007.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:819](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-007.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:820](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-007.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:821](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:302](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:337](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:338](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:339](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:340](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:341](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-010.D06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:342](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-011` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:346](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-011.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:385](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-011.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:386](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-011.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:387](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-011.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:388](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-011.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:389](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-012` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:393](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-012.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:428](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-012.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:429](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-012.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:430](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-012.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:431](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-012.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:432](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-013` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:436](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-013.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:458](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-013.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:459](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-013.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:460](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-013.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:461](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-013.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:462](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-014` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:466](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-014.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:474](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-014.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:475](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-014.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:476](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-014.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:477](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-014.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:478](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-015` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:482](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-015.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:501](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-015.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:502](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-015.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:503](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-015.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:504](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-015.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:505](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-016` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:509](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-016.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:524](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-016.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:525](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-016.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:526](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-016.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:527](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:827](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:868](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:869](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:870](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:871](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:872](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:873](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:874](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:875](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-101.D09` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:876](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-102` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:880](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-102.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:888](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-102.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:889](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-102.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:890](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-102.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:891](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-103` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:895](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-103.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:903](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-103.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:904](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-103.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:905](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-103.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:906](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-104` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:910](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-104.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:917](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-104.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:918](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-104.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:919](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-104.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:920](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-201` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:926](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-201.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:934](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-201.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:935](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-201.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:936](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-202` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:940](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-202.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:945](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-202.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:946](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-202.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:947](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-203` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:951](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-203.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:968](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-203.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:969](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-203.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:970](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-203.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:971](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-301` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:977](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-301.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:981](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-301.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:982](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-301.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:983](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-302` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:985](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-302.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:989](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-302.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:990](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-302.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:991](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-303` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:993](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-303.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:997](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-303.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:998](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-401` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1004](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-401.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1010](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-401.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1011](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-401.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1012](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-402` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1014](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-402.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1021](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-402.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1022](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-402.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1023](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-403` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1025](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-403.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1032](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-403.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1033](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-403.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1034](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-501` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1044](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-501.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1051](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-501.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1052](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-501.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1053](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-501.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1054](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-502` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1056](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-502.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1063](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-502.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1064](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-502.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1065](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-502.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1066](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-601` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1072](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-601.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1085](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-601.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1086](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-601.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1087](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-601.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1088](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-701` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1094](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-701.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1101](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-701.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1102](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-701.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1103](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-702` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1105](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-702.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1112](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-702.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1113](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-702.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1114](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-703` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1116](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-703.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1129](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-703.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1130](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-703.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1131](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-703.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1132](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-704` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1134](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-704.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1160](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-704.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1161](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-704.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1162](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-704.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1163](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1165](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1170](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1171](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1172](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1173](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1174](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1175](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1176](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-705.D08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1177](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1183](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1188](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1189](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1190](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1191](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1192](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1193](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-706.D07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1194](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1204](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1205](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1206](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1207](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1208](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1209](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1210](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1211](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-09` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1212](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-CD-10` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-requirements.md:1213](Graph-Neurons-requirements.md) | reconcile source and design real acceptance |
| `GN-FX-01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:288](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:289](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:290](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:291](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:292](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:293](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:294](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-FX-08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:295](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:175](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:176](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:177](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:178](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:179](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:180](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:181](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:182](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G09` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:183](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G10` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:184](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.G11` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:185](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0a.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:168](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:199](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:200](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:201](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:202](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:204](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:205](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:206](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:207](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G09` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:208](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.G10` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:209](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH0b.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:191](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH1.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:215](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH1.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:216](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH1.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:217](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH1.G04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:218](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH1.G05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:219](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH1.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:211](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:232](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:233](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:234](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:235](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:236](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:237](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:238](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:239](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G09` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:240](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.G10` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:241](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH2.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:225](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH3.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:247](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH3.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:248](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH3.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:249](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH3.G04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:250](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH3.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:243](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH4.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:258](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH4.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:259](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH4.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:260](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH4.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:252](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH5.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:263](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH5.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:263](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH5.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:263](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH5.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:262](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH6.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:269](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH6.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:269](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH6.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:269](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH6.G04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:269](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH6.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:268](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH7.G01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:275](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH7.G02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:275](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH7.G03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:275](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-PH7.GATE` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:274](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-01` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:437](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-02` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:438](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-03` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:439](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-04` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:440](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-05` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:441](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-06` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:442](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-07` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:443](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-08` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:444](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-09` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:445](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-10` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:446](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-11` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:447](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-12` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:448](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-13` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:449](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-14` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:450](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-15` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:451](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `GN-SO-16` | GN | W00 | untriaged | `UNTRIAGED` | [Graph-Neurons-implementation-plan.md:452](Graph-Neurons-implementation-plan.md) | reconcile source and design real acceptance |
| `PUR-GPU-001` | GPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:305](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-GPU-002` | GPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:306](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-GPU-003` | GPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:307](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-GPU-004` | GPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:308](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-GPU-005` | GPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:309](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `GRAPH-001` | GRAPH | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:260](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `GRAPH-001.1` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:505` | reconcile source and design real acceptance |
| `GRAPH-001.2` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:506` | reconcile source and design real acceptance |
| `GRAPH-001.3` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:507` | reconcile source and design real acceptance |
| `GRAPH-001.4` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:508` | reconcile source and design real acceptance |
| `GRAPH-001.5` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:509` | reconcile source and design real acceptance |
| `GRAPH-001.6` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:510` | reconcile source and design real acceptance |
| `GRAPH-001.7` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:511` | reconcile source and design real acceptance |
| `GRAPH-002` | GRAPH | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:284](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `GRAPH-002.1` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:532` | reconcile source and design real acceptance |
| `GRAPH-002.2` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:533` | reconcile source and design real acceptance |
| `GRAPH-002.3` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:534` | reconcile source and design real acceptance |
| `GRAPH-002.4` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:535` | reconcile source and design real acceptance |
| `GRAPH-002.5` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:536` | reconcile source and design real acceptance |
| `GRAPH-003` | GRAPH | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:305](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `GRAPH-003.1` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:555` | reconcile source and design real acceptance |
| `GRAPH-003.2` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:556` | reconcile source and design real acceptance |
| `GRAPH-003.3` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:557` | reconcile source and design real acceptance |
| `GRAPH-003.4` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:558` | reconcile source and design real acceptance |
| `GRAPH-003.5` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:559` | reconcile source and design real acceptance |
| `GRAPH-004` | GRAPH | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:325](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `GRAPH-004.1` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:578` | reconcile source and design real acceptance |
| `GRAPH-004.2` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:579` | reconcile source and design real acceptance |
| `GRAPH-004.3` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:580` | reconcile source and design real acceptance |
| `GRAPH-004.4` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:581` | reconcile source and design real acceptance |
| `GRAPH-004.5` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:582` | reconcile source and design real acceptance |
| `GRAPH-005` | GRAPH | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:346](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `GRAPH-005.1` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:600` | reconcile source and design real acceptance |
| `GRAPH-005.2` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:601` | reconcile source and design real acceptance |
| `GRAPH-005.3` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:602` | reconcile source and design real acceptance |
| `GRAPH-005.4` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:603` | reconcile source and design real acceptance |
| `GRAPH-005.5` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:604` | reconcile source and design real acceptance |
| `GRAPH-006` | GRAPH | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:366](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `GRAPH-006.1` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:622` | reconcile source and design real acceptance |
| `GRAPH-006.2` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:623` | reconcile source and design real acceptance |
| `GRAPH-006.3` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:624` | reconcile source and design real acceptance |
| `GRAPH-006.4` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:625` | reconcile source and design real acceptance |
| `GRAPH-006.5` | GRAPH | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:626` | reconcile source and design real acceptance |
| `GRF-OPS-001` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-requirements.md:273](living-AI-agg-Graffin-requirements.md) | reconcile source and design real acceptance |
| `GRF-OPS-002` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-requirements.md:280](living-AI-agg-Graffin-requirements.md) | reconcile source and design real acceptance |
| `GRF-OPS-003` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-requirements.md:287](living-AI-agg-Graffin-requirements.md) | reconcile source and design real acceptance |
| `GRF-OPS-004` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-requirements.md:294](living-AI-agg-Graffin-requirements.md) | reconcile source and design real acceptance |
| `GRF-P0.GATE` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:1](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `GRF-P1.GATE` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:1](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `GRF-P2.GATE` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:1](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `GRF-P3.GATE` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:1](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `GRF-P4.GATE` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:1](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `GRF-P5.GATE` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:1](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `GRF-SEC-001` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-requirements.md:256](living-AI-agg-Graffin-requirements.md) | reconcile source and design real acceptance |
| `GRF-SEC-002` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-requirements.md:263](living-AI-agg-Graffin-requirements.md) | reconcile source and design real acceptance |
| `T-GRF-001` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:77](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-002` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:90](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-003` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:113](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-004` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:125](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-005` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:138](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-006` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:154](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-007` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:167](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-008` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:184](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-009` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:195](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-010` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:212](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-011` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:224](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-011B` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:236](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-012` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:255](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-013` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:266](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-014` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:280](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `T-GRF-015` | GRF | W00 | untriaged | `UNTRIAGED` | [living-AI-agg-Graffin-implementation-plan.md:291](living-AI-agg-Graffin-implementation-plan.md) | reconcile source and design real acceptance |
| `H-01` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:267` | independently verify claim and runtime |
| `H-02` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:270` | independently verify claim and runtime |
| `H-03` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:272` | independently verify claim and runtime |
| `H-04` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:274` | independently verify claim and runtime |
| `H-05` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:277` | independently verify claim and runtime |
| `H-06` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:279` | independently verify claim and runtime |
| `H-07` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:281` | independently verify claim and runtime |
| `H-08` | H | W00 | claimed_accepted | `ACCEPTED` | `KGF-MASTER-BACKLOG.md:283` | independently verify claim and runtime |
| `INFRA-001` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:537](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-001.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:810` | reconcile source and design real acceptance |
| `INFRA-001.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:811` | reconcile source and design real acceptance |
| `INFRA-001.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:812` | reconcile source and design real acceptance |
| `INFRA-001.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:813` | reconcile source and design real acceptance |
| `INFRA-001.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:814` | reconcile source and design real acceptance |
| `INFRA-002` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:558](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-002.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:834` | reconcile source and design real acceptance |
| `INFRA-002.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:835` | reconcile source and design real acceptance |
| `INFRA-002.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:836` | reconcile source and design real acceptance |
| `INFRA-002.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:837` | reconcile source and design real acceptance |
| `INFRA-002.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:838` | reconcile source and design real acceptance |
| `INFRA-003` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:579](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-003.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:858` | reconcile source and design real acceptance |
| `INFRA-003.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:859` | reconcile source and design real acceptance |
| `INFRA-003.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:860` | reconcile source and design real acceptance |
| `INFRA-003.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:861` | reconcile source and design real acceptance |
| `INFRA-003.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:862` | reconcile source and design real acceptance |
| `INFRA-004` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:599](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-004.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:881` | reconcile source and design real acceptance |
| `INFRA-004.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:882` | reconcile source and design real acceptance |
| `INFRA-004.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:883` | reconcile source and design real acceptance |
| `INFRA-004.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:884` | reconcile source and design real acceptance |
| `INFRA-004.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:885` | reconcile source and design real acceptance |
| `INFRA-005` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:619](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-005.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:904` | reconcile source and design real acceptance |
| `INFRA-005.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:905` | reconcile source and design real acceptance |
| `INFRA-005.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:906` | reconcile source and design real acceptance |
| `INFRA-005.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:907` | reconcile source and design real acceptance |
| `INFRA-005.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:908` | reconcile source and design real acceptance |
| `INFRA-006` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:639](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-006.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:925` | reconcile source and design real acceptance |
| `INFRA-006.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:926` | reconcile source and design real acceptance |
| `INFRA-006.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:927` | reconcile source and design real acceptance |
| `INFRA-006.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:928` | reconcile source and design real acceptance |
| `INFRA-006.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:929` | reconcile source and design real acceptance |
| `INFRA-007` | INFRA | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:658](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `INFRA-007.1` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:948` | reconcile source and design real acceptance |
| `INFRA-007.2` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:949` | reconcile source and design real acceptance |
| `INFRA-007.3` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:950` | reconcile source and design real acceptance |
| `INFRA-007.4` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:951` | reconcile source and design real acceptance |
| `INFRA-007.5` | INFRA | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:952` | reconcile source and design real acceptance |
| `PUR-INT-001` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:398](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-002` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:399](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-003` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:400](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-004` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:401](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-005` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:402](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-006` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:403](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-007` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:404](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-008` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:405](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-009` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:406](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-INT-010` | INT | W10 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:407](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `E2E-IP-001.S01` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:821](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S02` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:822](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S03` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:823](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S04` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:824](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S05` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:825](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S06` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:826](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S07` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:827](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S08` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:828](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S09` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:829](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S10` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:830](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S11` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:831](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S12` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:832](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S13` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:833](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S14` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:834](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S15` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:835](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S16` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:836](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-IP-001.S17` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:837](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-DOD-1` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1262](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-DOD-2` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1263](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-DOD-3` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1264](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-DOD-4` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1265](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-DOD-5` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1266](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-DOD-6` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1267](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-DOD-7` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1268](ip-requirements.md) | reconcile source and design real acceptance |
| `IP-WP-00.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:365](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-01.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:391](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-02.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:413](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-03.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:436](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-04.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:454](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-05.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:474](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-06.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:494](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-06b.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:512](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-07.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:534](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-08.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:553](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-09.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:573](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-10.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:589](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-11.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:608](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-12.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:628](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-13.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:638](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-14.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:646](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-15.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:654](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-16.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:662](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-17.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:670](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-18.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:678](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-19.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:686](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-20.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:694](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-21.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:702](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-22.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:710](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-23.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:718](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-24.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:726](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-25.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:841](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-26.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:744](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-27.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:766](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-28.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:787](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `IP-WP-29.GATE` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements-implementation-plan.md:805](ip-requirements-implementation-plan.md) | reconcile source and design real acceptance |
| `REQ-BRB-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:658](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-BRB-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:659](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-BRB-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:660](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-BRB-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:661](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-BRB-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:662](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-BRB-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:663](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CHK-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:464](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CHK-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:465](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CHK-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:480](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CHK-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:481](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CHK-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:482](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CHK-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:483](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1334](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1335](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1336](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1337](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1338](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1339](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1340](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1341](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-009` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1342](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1343](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1344](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1345](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-013` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1346](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-CMT-014` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1347](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:673](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:674](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:698](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:699](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:700](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-013` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:701](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DCG-014` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:702](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1382](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1383](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1384](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1385](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1386](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1387](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1388](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1389](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-009` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1390](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1391](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DIS-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1392](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DSC-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1287](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DSC-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1288](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DSC-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1289](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DSC-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1290](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-DSC-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1291](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-EXP-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:513](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-EXP-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:514](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-EXP-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:515](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-EXP-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:516](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-HLF-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:598](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-HLF-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:599](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-HLF-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:600](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-HLF-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:601](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IMP-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:633](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IMP-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:634](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IMP-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:635](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IMP-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:636](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IMP-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:637](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IMP-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:638](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:829](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:830](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:831](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:832](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:833](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:834](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:835](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:836](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV1-009` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:837](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV11-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:922](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV11-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:923](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV11-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:924](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV11-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:925](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV11-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:926](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV11-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:927](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV12-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:933](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV12-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:934](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV12-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:935](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV12-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:936](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV12-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:937](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:843](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:844](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:845](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:846](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:847](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:848](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:849](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:850](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV3-009` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:851](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV4-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:857](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV4-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:858](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV4-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:859](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV4-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:860](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV4-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:861](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV4-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:862](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV5-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:868](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV5-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:869](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV5-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:870](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV5-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:871](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV5-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:872](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV5-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:873](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV6-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:879](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV6-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:880](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV6-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:881](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV6-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:882](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV6-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:883](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV6-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:884](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV7-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:890](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV7-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:891](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV7-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:892](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV7-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:893](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV7-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:894](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV7-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:895](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV8-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:901](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV8-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:902](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV8-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:903](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV8-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:904](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV8-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:905](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV8-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:906](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV9-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:912](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV9-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:913](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV9-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:914](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV9-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:915](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-INV9-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:916](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IPH-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:159](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IPH-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:160](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IPH-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:161](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IPH-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:162](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-IPH-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:163](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LIN-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:506](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LIN-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:507](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LSE-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:526](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LSE-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:527](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LSE-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:528](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LSE-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:550](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LSE-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:551](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LSE-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:552](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LVC-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:571](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LVC-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:572](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LVC-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:573](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LVC-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:574](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-LVC-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:575](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MET-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:753](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MET-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:754](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MET-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:755](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MET-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:770](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MET-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:771](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MET-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:772](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:712](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:713](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:714](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:738](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:739](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:740](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-013` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:741](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-014` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:742](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-MMG-015` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:743](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:797](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:798](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:799](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:805](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:806](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:807](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-013` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:808](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-020` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:814](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-021` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:815](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-030` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:821](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-031` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:822](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-NEU-032` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:823](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-OPR-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:389](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-OPR-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:390](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-OPR-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:391](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-OPR-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:392](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:142](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:143](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:144](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:145](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:146](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:147](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:148](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:149](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-009` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:150](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PLT-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:151](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:947](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:948](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:949](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:950](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:951](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:952](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:953](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:954](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-PRC-009` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:955](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1402](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1403](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1404](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1405](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1406](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1407](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-007` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1408](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-RFX-008` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:1409](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SAS-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:445](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SAS-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:446](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SAS-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:447](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SAS-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:448](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SAS-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:449](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SAS-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:450](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SDK-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:489](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SDK-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:490](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SDK-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:491](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SDK-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:492](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SHB-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:780](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SHB-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:781](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SHB-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:782](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SHB-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:783](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SHB-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:784](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-SHB-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:785](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-VER-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:498](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-VER-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:499](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-VER-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:500](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:243](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:244](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-010` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:343](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-011` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:344](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-012` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:345](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-013` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:346](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-014` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:347](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-020` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:376](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-021` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:377](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-022` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:378](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WAR-023` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:379](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WCA-001` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:423](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WCA-002` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:424](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WCA-003` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:425](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WCA-004` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:426](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WCA-005` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:427](ip-requirements.md) | reconcile source and design real acceptance |
| `REQ-WCA-006` | IP | W00 | untriaged | `UNTRIAGED` | [ip-requirements.md:428](ip-requirements.md) | reconcile source and design real acceptance |
| `PUR-IPU-001` | IPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:377](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-IPU-002` | IPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:378](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-IPU-003` | IPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:379](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-IPU-004` | IPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:380](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-IPU-005` | IPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:381](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `KGR-G-PLAN-V1.0` | KGR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:3](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-REQ-V2.0` | KGR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:3](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `KGR-G-001` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:27](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-002` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:28](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-003` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:29](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-004` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:33](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-005` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:34](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-006` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:38](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-007` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:43](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-008` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:39](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-009` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:44](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-010` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:48](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-011` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:251](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-012` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:251](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-013` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:283](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-014` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-015` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-016` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:283](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-017` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:251](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-018` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-019` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:314](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-020` | KGR-G | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:283](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | execute complete entrypoint and negative cases |
| `KGR-G-021` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:169](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-022` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:226](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-023` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:227](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-024` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:228](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-025` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:229](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-026` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:230](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `KGR-G-027` | KGR-G | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:169](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `PUR-LPU-001` | LPU | W08 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:366](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-LPU-002` | LPU | W08 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:367](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-LPU-003` | LPU | W08 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:368](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-LPU-004` | LPU | W08 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:369](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-LPU-005` | LPU | W08 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:370](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-LPU-006` | LPU | W08 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:371](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `CRA-001.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-002.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-003.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-004.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-005.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-006.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-007.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-008.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-009.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-010.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-011.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-012.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-013.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-014.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-015.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-016.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-017.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-018.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-019.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-020.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-021.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-022.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-023.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-024.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-025.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-026.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-027.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-028.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-029.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-030.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-031.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-032.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-033.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-034.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-035.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-036.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-037.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-038.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-039.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-040.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-041.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-042.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-043.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-044.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `CRA-045.A` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E01` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E02` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E03` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E04` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E05` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E06` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E07` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E08` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E09` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E10` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E11` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E12` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E13` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `E14` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-09` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-10` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-11` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-12` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-13` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-14` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-15` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-16` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `H-17` | Ledger | W00 | challenged | `BLOCKED` | `unresolved` | reproduce blocked scope or approve disposition |
| `R-C01` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C02` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C03` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C04` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C05` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C06` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C07` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C08` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C09` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C10` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C11` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C12` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C13` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C14` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C15` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C16` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C17` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C18` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C19` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C20` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C21` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C22` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C23` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C24` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C25` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C26` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C27` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C28` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C29` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C30` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C31` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C32` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C33` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C34` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C35` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C36` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C37` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C38` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C39` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C40` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C41` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C42` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C43` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C44` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C45` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C46` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C47` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C48` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C49` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C50` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C51` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C52` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C53` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C54` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `R-C55` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-01` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-02` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-03` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-04` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-05` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-06` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-07` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-08` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-09` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-10` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-11` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-12` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-13` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-14` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-15` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-16` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-17` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-18` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-19` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-20` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-21` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-22` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-23` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-24` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-25` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-26` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-27` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-28` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-29` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-30` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-31` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-32` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-33` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-34` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-35` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-36` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-37` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-38` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-39` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-40` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-41` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `X-42` | Ledger | W00 | claimed_accepted | `ACCEPTED` | `unresolved` | independently verify claim and runtime |
| `MS-1` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:377](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `MS-10` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:325](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `MS-11` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:8](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-12` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:68](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-13` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:96](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-14` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:33](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | reconcile source and design real acceptance |
| `MS-15` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:24](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-16` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:183](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-17` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:210](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-18` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:151](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-19` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:25](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-2` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:66](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `MS-20` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:300](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | reconcile source and design real acceptance |
| `MS-21` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:267](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-22` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:26](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-23` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:384](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-24` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:353](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-25` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:27](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-26` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:472](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-27` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:436](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-28` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:28](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | reconcile source and design real acceptance |
| `MS-29` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:551](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-3` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:66](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `MS-30` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:8](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | execute complete entrypoint and negative cases |
| `MS-4` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:383](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `MS-5` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:66](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `MS-6` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:174](EOIP-engg-doc-pkg/KGR-g-requirements.md) | execute complete entrypoint and negative cases |
| `MS-7` | MS | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:175](EOIP-engg-doc-pkg/KGR-g-requirements.md) | execute complete entrypoint and negative cases |
| `MS-8` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:317](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `MS-9` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-implementation-plan.md:383](EOIP-engg-doc-pkg/KGR-g-implementation-plan.md) | reconcile source and design real acceptance |
| `MS-KGR-020` | MS | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:424](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | reconcile source and design real acceptance |
| `MULTI-001` | MULTI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:970](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `MULTI-001.1` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1334` | reconcile source and design real acceptance |
| `MULTI-001.2` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1335` | reconcile source and design real acceptance |
| `MULTI-001.3` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1336` | reconcile source and design real acceptance |
| `MULTI-002` | MULTI | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:984](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `MULTI-002.1` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1353` | reconcile source and design real acceptance |
| `MULTI-002.2` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1354` | reconcile source and design real acceptance |
| `MULTI-002.3` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1355` | reconcile source and design real acceptance |
| `MULTI-002.4` | MULTI | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1356` | reconcile source and design real acceptance |
| `MVP-FR-001` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:99](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-002` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:100](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-003` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:101](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-004` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:102](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-005` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:103](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-006` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:104](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-007` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:105](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-008` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:106](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-009` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:107](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-01` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:72](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `MVP-FR-010` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:108](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-011` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:109](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-012` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:110](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-013` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:111](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-014` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:112](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-015` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:113](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-016` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:114](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-017` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:115](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-018` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:116](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-019` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:117](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-020` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:118](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-021` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:119](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-022` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:120](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-023` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:121](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-024` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:122](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-025` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:123](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-026` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:124](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-027` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:125](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | reconcile source and design real acceptance |
| `MVP-FR-028` | MVP | W00 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/70-acceptance-criteria.md:126](EOIP-engg-doc-pkg/70-acceptance-criteria.md) | execute complete entrypoint and negative cases |
| `MVP-FR-28` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:72](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `MVP-P0` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:44](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P1` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:45](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P2` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:46](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P3` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:47](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P4` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:48](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P5` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:49](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P6` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:50](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `MVP-P7` | MVP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md:51](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md) | reconcile source and design real acceptance |
| `NFR-001` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1679](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-002` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1680](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-003` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1681](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-004` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1682](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-005` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1683](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-006` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1684](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-007` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1685](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-008` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/generated/current-gap-report.md:1686](EOIP-engg-doc-pkg/audits/generated/current-gap-report.md) | reconcile source and design real acceptance |
| `NFR-01` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:71](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `NFR-02` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1094](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `NFR-03` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1095](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `NFR-04` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1096](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `NFR-05` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1097](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `NFR-06` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:1098](EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md) | reconcile source and design real acceptance |
| `NFR-14` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-g-requirements.md:71](EOIP-engg-doc-pkg/KGR-g-requirements.md) | reconcile source and design real acceptance |
| `NFR-KGR-001` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:704](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `NFR-KGR-002` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:713](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `NFR-KGR-003` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:718](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `NFR-KGR-004` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:726](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `NFR-KGR-005` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/KGR-requirements.md:732](EOIP-engg-doc-pkg/KGR-requirements.md) | reconcile source and design real acceptance |
| `NFR-MAINT-001` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:131](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `NFR-OPS-001` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:101](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `NFR-OPS-002` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:111](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `NFR-PERF-001` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:121](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `NFR-PRIV-001` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:141](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-REL-001` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:81](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `NFR-REL-002` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:91](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `NFR-SEC-001` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:11](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-SEC-002` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:21](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-SEC-003` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:31](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-SEC-004` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:41](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-SEC-005` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:51](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-SEC-006` | NFR | W11 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:61](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | reconcile source and design real acceptance |
| `NFR-SEC-007` | NFR | W11 | code_observed | `UNTRIAGED` | [EOIP-engg-doc-pkg/04-non-functional-requirements.md:71](EOIP-engg-doc-pkg/04-non-functional-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-NPU-001` | NPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:325](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-NPU-002` | NPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:326](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-NPU-003` | NPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:327](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-NPU-004` | NPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:328](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-NPU-005` | NPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:329](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `NS-AGENT-001` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:187](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-AGENT-002` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:201](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-AGENT-003` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:228](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-CORE-001` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:103](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-CORE-002` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:138](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-CORE-003` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:159](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-CORE-004` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:170](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-KG-001` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:242](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-KG-002` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:254](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-KG-003` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:275](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-P0.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-P1.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-P2.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-P3.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-P4.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-P5.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-P6.GATE` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:1](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `NS-REVA-001` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:307](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-REVA-002` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:319](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `NS-WG-001` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-agg-requirements.md:289](neural-schema-agg-requirements.md) | reconcile source and design real acceptance |
| `T-NS-001` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:84](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-002` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:95](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-003` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:108](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-004` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:120](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-005` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:136](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-006` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:148](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-007` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:163](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-008` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:175](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-009` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:187](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-009B` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:198](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-010` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:215](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-011` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:227](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-012` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:238](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-013` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:252](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-014` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:263](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-015` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:278](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-016` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:291](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `T-NS-017` | NS | W00 | untriaged | `UNTRIAGED` | [neural-schema-implementation-plan.md:302](neural-schema-implementation-plan.md) | reconcile source and design real acceptance |
| `CRA-001.11` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-002.10` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-002.11` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-003.12` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-004.10` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-004.12` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-005.9` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-016.6` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-016.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-016.9` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-017.10` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-017.6` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-017.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-017.9` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-018.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-018.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-019.13` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-019.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-019.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-019.9` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-020.11` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-020.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-020.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-020.9` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-021.6` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-021.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-022.6` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-022.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-023.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-024.10` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-024.11` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-024.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-027.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-030.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-032.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-034.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-035.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-035.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-036.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-037.10` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-039.7` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `CRA-039.8` | OCA | W00 | claimed_accepted | `ACCEPTED` | `OCA` | independently verify claim and runtime |
| `PUR-OPS-001` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:419](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-002` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:420](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-003` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:421](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-004` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:422](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-005` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:423](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-006` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:424](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-007` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:425](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-OPS-008` | OPS | W11 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:426](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PERF-01` | PERF | W00 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:177` | execute complete entrypoint and negative cases |
| `PRE-001` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:18` | reconcile source and design real acceptance |
| `PRE-001.1` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:196` | reconcile source and design real acceptance |
| `PRE-001.2` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:197` | reconcile source and design real acceptance |
| `PRE-001.3` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:198` | reconcile source and design real acceptance |
| `PRE-001.4` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:199` | reconcile source and design real acceptance |
| `PRE-001.5` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:200` | reconcile source and design real acceptance |
| `PRE-002` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:18` | reconcile source and design real acceptance |
| `PRE-002.1` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:209` | reconcile source and design real acceptance |
| `PRE-002.2` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:210` | reconcile source and design real acceptance |
| `PRE-002.3` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:211` | reconcile source and design real acceptance |
| `PRE-002.4` | PRE | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:212` | reconcile source and design real acceptance |
| `CRA-026.10` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-026.11` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-026.12` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.1` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.2` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.3` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.4` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.5` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.6` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `CRA-045.7` | PRM | W00 | claimed_accepted | `ACCEPTED` | `PRM` | independently verify claim and runtime |
| `PUR-QPU-001` | QPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:345](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-QPU-002` | QPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:346](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-QPU-003` | QPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:347](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-QPU-004` | QPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:348](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-QPU-005` | QPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:349](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-QPU-006` | QPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:350](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `REL-01` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1212` | execute complete entrypoint and negative cases |
| `REL-02` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1216` | execute complete entrypoint and negative cases |
| `REL-03` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1218` | execute complete entrypoint and negative cases |
| `REL-04` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:292` | execute complete entrypoint and negative cases |
| `REL-05` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:245` | execute complete entrypoint and negative cases |
| `REL-06` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:175` | execute complete entrypoint and negative cases |
| `REL-07` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:175` | execute complete entrypoint and negative cases |
| `REL-08` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1213` | execute complete entrypoint and negative cases |
| `REL-09` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:161` | execute complete entrypoint and negative cases |
| `REL-10` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:175` | execute complete entrypoint and negative cases |
| `REL-11` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1213` | execute complete entrypoint and negative cases |
| `REL-12` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:162` | execute complete entrypoint and negative cases |
| `REL-13` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:247` | execute complete entrypoint and negative cases |
| `REL-14` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1249` | execute complete entrypoint and negative cases |
| `REL-15` | REL | W12 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:1252` | execute complete entrypoint and negative cases |
| `REQ-USER-IMPORT-001` | REQ | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/tickets/requirements-map.md:15](EOIP-engg-doc-pkg/tickets/requirements-map.md) | reconcile source and design real acceptance |
| `CRA-001.10` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-001.7` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-001.9` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-003.11` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-003.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-007.9` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-008.9` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-009.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-012.6` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-016.10` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-017.7` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-019.11` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-025.7` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-026.13` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-026.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-027.9` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-033.7` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-036.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-037.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-038.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.1` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.2` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.3` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.4` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.5` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.6` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-041.7` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.1` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.2` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.3` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.4` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.5` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.6` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-042.7` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-043.10` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-043.11` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-044.12` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-044.13` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `CRA-045.8` | RES | W00 | claimed_accepted | `ACCEPTED` | `RES` | independently verify claim and runtime |
| `REVA-AB-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:875](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:876](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:877](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:878](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:879](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:880](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:881](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:882](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:883](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:884](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:885](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:886](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-013` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:887](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-014` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:888](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AB-015` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:889](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:842](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:843](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:844](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:845](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:846](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:847](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AI-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:848](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:897](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:898](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:899](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:900](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:901](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:902](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:903](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-AS-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:904](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-BD-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1170](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-BD-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1171](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-BD-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1172](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-BD-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1173](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-BD-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1174](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CV-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:706](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CV-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:707](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CV-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:708](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CV-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:709](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CV-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:710](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CX-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:733](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CX-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:734](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CX-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:735](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CX-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:736](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-CX-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:737](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DB-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:912](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DB-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:913](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DB-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:914](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DB-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:915](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DB-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:916](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DI-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1136](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DI-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1137](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DI-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1138](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DI-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1139](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DI-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1140](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DR-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1015](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DR-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1016](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DR-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1017](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DV-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:963](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DV-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:964](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DV-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:965](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-DV-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:966](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FM-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1119](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FM-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1120](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FM-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1121](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FM-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1122](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FM-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1123](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:935](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:936](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:937](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:938](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:939](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:940](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:941](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:942](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-FT-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:943](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1001](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1002](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1003](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1004](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1005](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1006](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GA-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1007](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GD-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:951](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GD-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:952](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GD-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:953](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GD-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:954](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-GD-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:955](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1222](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1223](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1224](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1225](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1226](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1227](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1228](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1229](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1230](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-015` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1231](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-020` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1232](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-021` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1233](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-022` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1234](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-023` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1235](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-024` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1236](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-025` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1237](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-026` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1238](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-030` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1239](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-031` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1240](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-040` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1241](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-041` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1242](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-042` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1243](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-043` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1244](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-044` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1245](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-045` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1246](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-046` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1247](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-047` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1248](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-048` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1249](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-049` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1250](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-050` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1251](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-051` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1252](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-052` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1253](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-053` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1254](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-054` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1255](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-060` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1256](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-061` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1257](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-070` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1258](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-071` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1259](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-080` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1260](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-IF-081` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1261](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:718](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:719](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:720](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:721](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:722](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:723](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:724](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-KG-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:725](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MB-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1101](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MB-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1102](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MB-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1103](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MB-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1104](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MB-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1105](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MB-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1106](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:985](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:986](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:987](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:988](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:989](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:990](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:991](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:992](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-MC-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:993](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1081](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1082](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1083](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1084](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1085](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1086](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1087](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NB-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1088](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1191](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1192](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1193](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1194](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1195](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1196](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1197](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1198](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1199](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1200](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1201](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1202](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-013` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1203](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-014` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1204](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-015` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1205](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-016` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1206](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-017` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1207](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-018` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1208](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-019` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1209](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-020` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1210](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-NFR-030` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1211](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-OB-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1062](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-OB-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1063](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-OB-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1064](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-OB-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1065](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-OB-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1066](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-OB-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1067](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-0.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-1.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-2.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-3.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-4.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-5.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-6.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-7.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-P-ENH-8.GATE` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `REVA-PD-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:784](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:785](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:786](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:787](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:788](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:789](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:790](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:791](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:792](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:793](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:794](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-PD-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:795](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RO-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1153](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RO-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1154](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RO-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1155](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RO-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1156](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RO-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1157](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RR-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:924](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RR-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:925](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RR-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:926](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-RR-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:927](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1022](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1023](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1024](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1025](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1026](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1027](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1028](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1029](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1030](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1031](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1032](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1033](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SEC-013` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1034](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:856](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:857](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:858](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:859](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:860](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:861](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:862](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:863](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:864](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:865](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:866](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-SP-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:867](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-TL-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:694](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-TL-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:695](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-TL-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:696](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-TL-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:697](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-TL-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:698](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1041](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1042](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1043](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1044](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1045](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1046](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1047](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1048](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1049](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1050](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1051](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1052](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-013` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1053](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-014` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1054](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-015` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1055](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-016` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1056](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-UI-017` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1057](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:825](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:826](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:827](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:828](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:829](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:830](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:831](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:832](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:833](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VS-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:834](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VW-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:974](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VW-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:975](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VW-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:976](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-VW-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:977](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:672](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:673](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:674](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:675](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:676](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:677](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:678](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:679](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:680](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:681](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:682](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:683](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-013` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:684](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-014` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:685](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-WK-015` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:686](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-XP-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1181](reva-requirements.md) | reconcile source and design real acceptance |
| `REVA-XP-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-requirements.md:1182](reva-requirements.md) | reconcile source and design real acceptance |
| `T-ENH-001` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:73](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-002` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:122](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-003` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:159](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-004` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:183](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-005` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:222](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-006` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:241](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-007` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:263](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-008` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:285](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-009` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:331](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-010` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:364](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-011` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:389](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-012` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:410](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-013` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:431](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-014` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:454](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-015` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:477](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-016` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:501](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-017` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:522](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-018` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:544](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-019` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:567](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-020` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:589](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-021` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:618](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-022` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:640](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-023` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:663](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-024` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:685](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-025` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:717](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-026` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:740](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-027` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:761](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-028` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:784](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-029` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:804](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-030` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:825](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-031` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:849](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-032` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:871](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-033` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:894](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-034` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:914](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-035` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:937](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-036` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:963](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-037` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:982](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `T-ENH-038` | REVA | W00 | untriaged | `UNTRIAGED` | [reva-enhanced-implementation-plan.md:1007](reva-enhanced-implementation-plan.md) | reconcile source and design real acceptance |
| `PUR-RUN-001` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:187](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-002` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:188](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-003` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:189](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-004` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:190](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-005` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:191](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-006` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:192](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-007` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:193](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-008` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:194](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-009` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:195](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-010` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:196](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-011` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:197](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-RUN-012` | RUN | W03 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:198](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `S-01` | S | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `S-02` | S | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `S-03` | S | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `S-04` | S | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `S-05` | S | W00 | code_observed | `UNTRIAGED` | [requirements-registry.json:1](requirements-registry.json) | execute complete entrypoint and negative cases |
| `SDLC-001` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:174` | reconcile source and design real acceptance |
| `SDLC-001.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1409` | reconcile source and design real acceptance |
| `SDLC-001.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1410` | reconcile source and design real acceptance |
| `SDLC-001.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1411` | reconcile source and design real acceptance |
| `SDLC-001.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1412` | reconcile source and design real acceptance |
| `SDLC-002` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1414` | reconcile source and design real acceptance |
| `SDLC-002.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1428` | reconcile source and design real acceptance |
| `SDLC-002.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1429` | reconcile source and design real acceptance |
| `SDLC-002.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1430` | reconcile source and design real acceptance |
| `SDLC-002.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1431` | reconcile source and design real acceptance |
| `SDLC-003` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1433` | reconcile source and design real acceptance |
| `SDLC-003.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1447` | reconcile source and design real acceptance |
| `SDLC-003.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1448` | reconcile source and design real acceptance |
| `SDLC-003.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1449` | reconcile source and design real acceptance |
| `SDLC-003.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1450` | reconcile source and design real acceptance |
| `SDLC-004` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:35` | reconcile source and design real acceptance |
| `SDLC-004.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1468` | reconcile source and design real acceptance |
| `SDLC-004.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1469` | reconcile source and design real acceptance |
| `SDLC-004.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1470` | reconcile source and design real acceptance |
| `SDLC-004.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1471` | reconcile source and design real acceptance |
| `SDLC-005` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:144` | reconcile source and design real acceptance |
| `SDLC-005.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1487` | reconcile source and design real acceptance |
| `SDLC-005.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1488` | reconcile source and design real acceptance |
| `SDLC-005.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1489` | reconcile source and design real acceptance |
| `SDLC-005.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1490` | reconcile source and design real acceptance |
| `SDLC-006` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1492` | reconcile source and design real acceptance |
| `SDLC-006.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1506` | reconcile source and design real acceptance |
| `SDLC-006.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1507` | reconcile source and design real acceptance |
| `SDLC-006.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1508` | reconcile source and design real acceptance |
| `SDLC-006.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1509` | reconcile source and design real acceptance |
| `SDLC-007` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:864` | reconcile source and design real acceptance |
| `SDLC-007.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1525` | reconcile source and design real acceptance |
| `SDLC-007.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1526` | reconcile source and design real acceptance |
| `SDLC-007.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1527` | reconcile source and design real acceptance |
| `SDLC-007.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1528` | reconcile source and design real acceptance |
| `SDLC-008` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:141` | reconcile source and design real acceptance |
| `SDLC-008.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1544` | reconcile source and design real acceptance |
| `SDLC-008.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1545` | reconcile source and design real acceptance |
| `SDLC-008.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1546` | reconcile source and design real acceptance |
| `SDLC-008.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1547` | reconcile source and design real acceptance |
| `SDLC-009` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1549` | reconcile source and design real acceptance |
| `SDLC-009.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1563` | reconcile source and design real acceptance |
| `SDLC-009.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1564` | reconcile source and design real acceptance |
| `SDLC-009.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1565` | reconcile source and design real acceptance |
| `SDLC-009.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1566` | reconcile source and design real acceptance |
| `SDLC-010` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1371` | reconcile source and design real acceptance |
| `SDLC-010.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1584` | reconcile source and design real acceptance |
| `SDLC-010.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1585` | reconcile source and design real acceptance |
| `SDLC-010.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1586` | reconcile source and design real acceptance |
| `SDLC-010.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1587` | reconcile source and design real acceptance |
| `SDLC-011` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1589` | reconcile source and design real acceptance |
| `SDLC-011.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1602` | reconcile source and design real acceptance |
| `SDLC-011.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1603` | reconcile source and design real acceptance |
| `SDLC-011.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1604` | reconcile source and design real acceptance |
| `SDLC-011.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1605` | reconcile source and design real acceptance |
| `SDLC-012` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1258` | reconcile source and design real acceptance |
| `SDLC-012.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1621` | reconcile source and design real acceptance |
| `SDLC-012.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1622` | reconcile source and design real acceptance |
| `SDLC-012.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1623` | reconcile source and design real acceptance |
| `SDLC-012.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1624` | reconcile source and design real acceptance |
| `SDLC-013` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1626` | reconcile source and design real acceptance |
| `SDLC-013.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1640` | reconcile source and design real acceptance |
| `SDLC-013.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1641` | reconcile source and design real acceptance |
| `SDLC-013.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1642` | reconcile source and design real acceptance |
| `SDLC-013.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1643` | reconcile source and design real acceptance |
| `SDLC-014` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1645` | reconcile source and design real acceptance |
| `SDLC-014.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1657` | reconcile source and design real acceptance |
| `SDLC-014.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1658` | reconcile source and design real acceptance |
| `SDLC-014.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1659` | reconcile source and design real acceptance |
| `SDLC-014.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1660` | reconcile source and design real acceptance |
| `SDLC-015` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:174` | reconcile source and design real acceptance |
| `SDLC-015.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1676` | reconcile source and design real acceptance |
| `SDLC-015.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1677` | reconcile source and design real acceptance |
| `SDLC-015.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1678` | reconcile source and design real acceptance |
| `SDLC-015.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1679` | reconcile source and design real acceptance |
| `SDLC-016` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1681` | reconcile source and design real acceptance |
| `SDLC-016.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1694` | reconcile source and design real acceptance |
| `SDLC-016.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1695` | reconcile source and design real acceptance |
| `SDLC-016.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1696` | reconcile source and design real acceptance |
| `SDLC-016.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1697` | reconcile source and design real acceptance |
| `SDLC-017` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:931` | reconcile source and design real acceptance |
| `SDLC-017.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1714` | reconcile source and design real acceptance |
| `SDLC-017.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1715` | reconcile source and design real acceptance |
| `SDLC-017.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1716` | reconcile source and design real acceptance |
| `SDLC-017.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1717` | reconcile source and design real acceptance |
| `SDLC-018` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1719` | reconcile source and design real acceptance |
| `SDLC-018.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1732` | reconcile source and design real acceptance |
| `SDLC-018.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1733` | reconcile source and design real acceptance |
| `SDLC-018.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1734` | reconcile source and design real acceptance |
| `SDLC-018.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1735` | reconcile source and design real acceptance |
| `SDLC-019` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1737` | reconcile source and design real acceptance |
| `SDLC-019.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1749` | reconcile source and design real acceptance |
| `SDLC-019.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1750` | reconcile source and design real acceptance |
| `SDLC-019.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1751` | reconcile source and design real acceptance |
| `SDLC-019.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1752` | reconcile source and design real acceptance |
| `SDLC-020` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1754` | reconcile source and design real acceptance |
| `SDLC-020.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1766` | reconcile source and design real acceptance |
| `SDLC-020.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1767` | reconcile source and design real acceptance |
| `SDLC-020.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1768` | reconcile source and design real acceptance |
| `SDLC-020.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1769` | reconcile source and design real acceptance |
| `SDLC-021` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1771` | reconcile source and design real acceptance |
| `SDLC-021.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1784` | reconcile source and design real acceptance |
| `SDLC-021.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1785` | reconcile source and design real acceptance |
| `SDLC-021.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1786` | reconcile source and design real acceptance |
| `SDLC-021.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1787` | reconcile source and design real acceptance |
| `SDLC-022` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1373` | reconcile source and design real acceptance |
| `SDLC-022.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1805` | reconcile source and design real acceptance |
| `SDLC-022.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1806` | reconcile source and design real acceptance |
| `SDLC-022.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1807` | reconcile source and design real acceptance |
| `SDLC-022.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1808` | reconcile source and design real acceptance |
| `SDLC-023` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1810` | reconcile source and design real acceptance |
| `SDLC-023.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1824` | reconcile source and design real acceptance |
| `SDLC-023.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1825` | reconcile source and design real acceptance |
| `SDLC-023.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1826` | reconcile source and design real acceptance |
| `SDLC-023.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1827` | reconcile source and design real acceptance |
| `SDLC-024` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1829` | reconcile source and design real acceptance |
| `SDLC-024.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1842` | reconcile source and design real acceptance |
| `SDLC-024.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1843` | reconcile source and design real acceptance |
| `SDLC-024.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1844` | reconcile source and design real acceptance |
| `SDLC-024.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1845` | reconcile source and design real acceptance |
| `SDLC-025` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:176` | reconcile source and design real acceptance |
| `SDLC-025.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1863` | reconcile source and design real acceptance |
| `SDLC-025.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1864` | reconcile source and design real acceptance |
| `SDLC-025.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1865` | reconcile source and design real acceptance |
| `SDLC-025.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1866` | reconcile source and design real acceptance |
| `SDLC-026` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1238` | reconcile source and design real acceptance |
| `SDLC-026.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1881` | reconcile source and design real acceptance |
| `SDLC-026.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1882` | reconcile source and design real acceptance |
| `SDLC-026.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1883` | reconcile source and design real acceptance |
| `SDLC-026.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1884` | reconcile source and design real acceptance |
| `SDLC-027` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:140` | reconcile source and design real acceptance |
| `SDLC-027.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1900` | reconcile source and design real acceptance |
| `SDLC-027.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1901` | reconcile source and design real acceptance |
| `SDLC-027.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1902` | reconcile source and design real acceptance |
| `SDLC-027.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1903` | reconcile source and design real acceptance |
| `SDLC-028` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:142` | reconcile source and design real acceptance |
| `SDLC-028.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1919` | reconcile source and design real acceptance |
| `SDLC-028.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1920` | reconcile source and design real acceptance |
| `SDLC-028.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1921` | reconcile source and design real acceptance |
| `SDLC-028.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1922` | reconcile source and design real acceptance |
| `SDLC-029` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:142` | reconcile source and design real acceptance |
| `SDLC-029.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1937` | reconcile source and design real acceptance |
| `SDLC-029.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1938` | reconcile source and design real acceptance |
| `SDLC-029.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1939` | reconcile source and design real acceptance |
| `SDLC-029.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1940` | reconcile source and design real acceptance |
| `SDLC-030` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:144` | reconcile source and design real acceptance |
| `SDLC-030.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1955` | reconcile source and design real acceptance |
| `SDLC-030.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1956` | reconcile source and design real acceptance |
| `SDLC-030.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1957` | reconcile source and design real acceptance |
| `SDLC-030.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1958` | reconcile source and design real acceptance |
| `SDLC-031` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1297` | reconcile source and design real acceptance |
| `SDLC-031.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1974` | reconcile source and design real acceptance |
| `SDLC-031.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1975` | reconcile source and design real acceptance |
| `SDLC-031.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1976` | reconcile source and design real acceptance |
| `SDLC-031.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1977` | reconcile source and design real acceptance |
| `SDLC-032` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1375` | reconcile source and design real acceptance |
| `SDLC-032.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1994` | reconcile source and design real acceptance |
| `SDLC-032.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1995` | reconcile source and design real acceptance |
| `SDLC-032.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1996` | reconcile source and design real acceptance |
| `SDLC-032.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1997` | reconcile source and design real acceptance |
| `SDLC-033` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1999` | reconcile source and design real acceptance |
| `SDLC-033.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2012` | reconcile source and design real acceptance |
| `SDLC-033.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2013` | reconcile source and design real acceptance |
| `SDLC-033.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2014` | reconcile source and design real acceptance |
| `SDLC-033.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2015` | reconcile source and design real acceptance |
| `SDLC-034` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1316` | reconcile source and design real acceptance |
| `SDLC-034.1` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2029` | reconcile source and design real acceptance |
| `SDLC-034.2` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2030` | reconcile source and design real acceptance |
| `SDLC-034.3` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2031` | reconcile source and design real acceptance |
| `SDLC-034.4` | SDLC | W00 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:2032` | reconcile source and design real acceptance |
| `PUR-SEC-001` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:232](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-002` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:233](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-003` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:234](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-004` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:235](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-005` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:236](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-006` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:237](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-007` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:238](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-008` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:239](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-009` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:240](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-010` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:241](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-011` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:242](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-012` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:243](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-013` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:244](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-014` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:245](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-015` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:246](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-SEC-016` | SEC | W02 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:247](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `SR-AGT-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:681](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:682](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:683](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:684](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:685](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:686](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:687](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:688](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:689](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:690](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:691](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-020` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:697](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-021` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:698](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-022` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:699](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-023` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:700](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-024` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:701](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-025` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:702](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-026` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:703](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-027` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:704](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-028` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:705](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-AGT-029` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:706](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:162](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:163](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:164](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:165](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:166](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:167](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:168](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:169](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:170](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:43](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | reconcile source and design real acceptance |
| `SR-ARC-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:172](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ARC-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:173](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CFG-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:747](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CFG-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:748](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CFG-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:749](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CFG-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:750](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CFG-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:751](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CFG-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:752](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1000](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1001](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1002](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1003](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1004](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1005](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1006](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1007](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1008](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1009](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-020` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1034](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-COM-021` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:1035](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:98](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:99](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:100](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:101](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:102](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:103](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:104](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:105](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:106](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:124](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:125](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:126](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-CON-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/diamond-moonshots-advanced.md:99](EOIP-engg-doc-pkg/diamond-moonshots-advanced.md) | reconcile source and design real acceptance |
| `SR-CON-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:128](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:922](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:923](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:924](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:925](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:926](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:927](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:928](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:929](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-DEP-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:930](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:776](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:777](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:778](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:779](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:780](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:786](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:787](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:788](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:789](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:790](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-EXT-015` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:791](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:183](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:184](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:185](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:186](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:187](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:188](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:189](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:190](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:191](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:192](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:216](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:217](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:218](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:219](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-015` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:220](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GDB-016` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:221](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GOV-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:868](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GOV-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:869](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GOV-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:870](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GOV-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:871](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-GOV-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:872](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:345](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:346](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:347](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:348](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:349](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:350](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:351](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:379](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:380](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:381](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:382](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:383](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-015` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:384](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-016` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:385](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-017` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:386](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-018` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:387](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-019` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:388](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-020` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:389](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-030` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:414](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-031` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:415](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-032` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:416](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-033` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:417](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-040` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:440](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-041` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:441](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-042` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:442](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-043` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:443](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-050` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:449](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-051` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:450](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-052` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:451](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-053` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:452](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-060` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:467](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-061` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:468](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-070` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:474](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ING-071` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:475](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:604](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:605](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:606](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:607](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:608](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:609](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:610](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:611](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:612](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:661](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:662](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:663](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:664](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:665](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-015` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:666](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-016` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:667](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-017` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:668](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-018` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:669](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-019` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:670](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-LLM-020` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:671](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:896](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:897](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:898](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:899](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:900](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:901](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:902](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NFR-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:903](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:580](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:581](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:582](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:583](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:584](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:585](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:586](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:587](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:588](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:584](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:590](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:591](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:592](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:593](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-NLQ-015` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:594](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:495](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:496](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:497](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:498](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:499](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:500](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:501](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:502](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:503](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:504](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-020` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:522](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-021` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:523](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-ONT-022` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:524](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-OPS-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:909](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-OPS-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:910](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-OPS-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:911](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-OPS-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:912](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-OPS-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:913](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-OPS-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:914](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:848](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:849](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:850](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:851](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:852](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:853](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-PRV-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:854](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:955](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:956](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:962](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:963](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:964](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:965](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QA-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:966](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:312](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:313](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:314](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:315](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:316](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:317](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:318](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:319](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:320](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:321](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:322](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-QRY-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:323](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:563](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:564](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:565](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:566](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:567](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:568](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:569](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:570](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:571](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-RAG-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:572](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:824](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:825](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:826](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:827](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:828](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:829](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:835](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:836](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:837](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-013` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:838](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-014` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:839](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-015` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:840](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-016` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:841](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-SEC-017` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:842](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:718](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:719](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:720](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:721](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:722](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:723](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:724](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:725](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:726](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-TEN-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:727](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:803](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:804](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:805](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:806](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:807](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:808](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:809](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:810](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:811](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-010` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:812](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-011` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:813](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-UX-012` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:814](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:227](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:228](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:229](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:230](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:231](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:232](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-VDB-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:233](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-001` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:733](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-002` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:734](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-003` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:735](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-004` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:736](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-005` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:737](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-006` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:738](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-007` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:739](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-008` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:740](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `SR-WL-009` | SR | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/super-requirements.md:741](EOIP-engg-doc-pkg/super-requirements.md) | reconcile source and design real acceptance |
| `TASK-AIE-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:11](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:18](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:23](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:28](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:32](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:37](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:41](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:45](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:49](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:53](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:58](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:62](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-AIE-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md:66](EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:11](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:17](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:21](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:25](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:29](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:34](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:38](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:42](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:47](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:51](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:55](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:60](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:65](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:69](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:74](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-016` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:78](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-ARCH-017` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Architect_tasks.md:82](EOIP-engg-doc-pkg/roles/Architect_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:12](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:18](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:25](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:31](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:40](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:47](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:53](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:59](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:65](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:70](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:76](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:82](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CEO-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CEO_tasks.md:90](EOIP-engg-doc-pkg/roles/CEO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:11](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:17](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:24](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:30](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:37](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:44](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:50](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:56](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:63](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:70](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:75](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:80](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:88](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:94](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:99](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-016` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:106](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-017` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:112](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-CTO-018` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/CTO_tasks.md:117](EOIP-engg-doc-pkg/roles/CTO_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:21](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:27](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:32](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:37](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:42](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:46](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:52](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:56](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:60](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:63](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:66](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:69](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:73](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-030` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:73](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-031` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:76](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DEV-032` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/Developer_tasks.md:80](EOIP-engg-doc-pkg/roles/Developer_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:11](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:18](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:23](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:28](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:36](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:41](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:46](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:52](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:57](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:63](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:68](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:73](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:79](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-DM-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md:86](EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:11](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:16](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:22](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:26](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:32](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:37](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:41](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:46](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:51](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:56](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:61](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:65](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:69](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:74](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:79](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LAI-016` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md:83](EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:11](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:16](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:21](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:26](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:30](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:35](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:41](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:47](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:52](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:56](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:61](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:65](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:69](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:74](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:78](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LD-016` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md:83](EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:11](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:22](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:26](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:31](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:38](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:42](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:48](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:53](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:57](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:61](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:66](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:71](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:75](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:82](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LEGAL-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md:86](EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:11](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:17](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:22](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:27](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:32](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:38](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:42](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:46](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:50](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:54](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:59](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:64](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-LIC-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md:68](EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:11](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:17](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:21](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:25](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:29](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:34](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:38](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:41](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:46](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:49](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:53](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKE-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md:58](EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:11](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:17](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:22](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:26](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:32](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:40](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:45](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:50](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:54](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:58](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:63](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:68](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:73](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-MKT-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md:78](EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:11](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:15](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:19](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:23](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:27](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:33](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:33](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-016` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:36](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-017` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:40](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-018` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:44](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-019` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:48](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-020` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:52](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QA-021` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md:56](EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:11](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:17](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:22](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:28](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:34](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:38](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:41](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:46](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:51](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:56](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:61](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:66](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-QAL-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/QALead_tasks.md:71](EOIP-engg-doc-pkg/roles/QALead_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-001` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:11](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-002` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:16](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-003` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:22](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-004` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:26](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-005` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:30](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-006` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:35](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-007` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:41](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-008` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:46](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-009` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:50](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-010` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:54](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-011` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:59](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-012` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:64](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-013` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:68](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-014` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:73](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-015` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:77](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-016` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:81](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TASK-SEC-017` | TASK | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md:85](EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md) | reconcile source and design real acceptance |
| `TEST-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:888](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `TEST-001.1` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1233` | reconcile source and design real acceptance |
| `TEST-001.2` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1234` | reconcile source and design real acceptance |
| `TEST-001.3` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1235` | reconcile source and design real acceptance |
| `TEST-001.4` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1236` | reconcile source and design real acceptance |
| `TEST-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:904](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `TEST-002.1` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1253` | reconcile source and design real acceptance |
| `TEST-002.2` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1254` | reconcile source and design real acceptance |
| `TEST-002.3` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1255` | reconcile source and design real acceptance |
| `TEST-002.4` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1256` | reconcile source and design real acceptance |
| `TEST-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:920](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `TEST-003.1` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1272` | reconcile source and design real acceptance |
| `TEST-003.2` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1273` | reconcile source and design real acceptance |
| `TEST-003.3` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1274` | reconcile source and design real acceptance |
| `TEST-003.4` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1275` | reconcile source and design real acceptance |
| `TEST-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:935](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `TEST-004.1` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1292` | reconcile source and design real acceptance |
| `TEST-004.2` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1293` | reconcile source and design real acceptance |
| `TEST-004.3` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1294` | reconcile source and design real acceptance |
| `TEST-004.4` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1295` | reconcile source and design real acceptance |
| `TEST-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:951](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `TEST-005.1` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1312` | reconcile source and design real acceptance |
| `TEST-005.2` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1313` | reconcile source and design real acceptance |
| `TEST-005.3` | TEST | W12 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1314` | reconcile source and design real acceptance |
| `TEST-FR-ADMIN-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:78](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-ADMIN-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:79](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-AGENT-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:68](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-AGENT-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:69](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-AGENT-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:70](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-AGENT-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:71](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-AGENT-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:72](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CODE-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:46](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CODE-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:47](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CODE-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:48](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CODE-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:49](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CODE-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:50](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONF-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:22](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:15](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:16](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:17](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:18](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:19](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-006` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:20](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-CONN-007` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:21](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:29](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:30](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:31](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:32](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:33](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-006` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:34](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-007` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:35](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-008` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:36](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-009` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:37](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-GRAPH-010` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:38](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-ID-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:43](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-ID-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:44](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-INGEST-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:24](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-INGEST-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:25](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-INGEST-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:26](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-INGEST-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:27](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-INGEST-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:28](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-MCP-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:74](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-MCP-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:75](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-MEM-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:73](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-ONTO-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:39](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-ONTO-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:40](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-PROV-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:41](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-PROV-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:42](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:51](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:52](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:53](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:54](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:55](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-006` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:56](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-007` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:57](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-QUERY-008` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:58](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-RAG-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:62](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-RAG-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:63](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-RAG-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:64](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-RAG-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:65](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-RAG-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:66](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-RAG-006` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:67](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-SNOW-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:23](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-TEMP-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:45](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-UI-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:76](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-UI-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:77](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-VALID-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:59](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-VALID-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:60](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-VALID-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:61](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-VSCODE-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:80](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-FR-VSCODE-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:81](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-MAINT-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:94](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-OPS-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:91](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-OPS-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:92](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-PERF-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:93](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-PRIV-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:95](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-REL-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:89](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-REL-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:90](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-001` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:82](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-002` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:83](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-003` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:84](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-004` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:85](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-005` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:86](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-006` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:87](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `TEST-NFR-SEC-007` | TEST | W12 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/72-requirement-traceability.md:88](EOIP-engg-doc-pkg/72-requirement-traceability.md) | reconcile source and design real acceptance |
| `PUR-TPU-001` | TPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:315](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-TPU-002` | TPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:316](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-TPU-003` | TPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:317](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-TPU-004` | TPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:318](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-TPU-005` | TPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:319](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `UI-001` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:682](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-001.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:976` | reconcile source and design real acceptance |
| `UI-001.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:977` | reconcile source and design real acceptance |
| `UI-001.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:978` | reconcile source and design real acceptance |
| `UI-001.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:979` | reconcile source and design real acceptance |
| `UI-001.5` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:980` | reconcile source and design real acceptance |
| `UI-002` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:700](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-002.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:999` | reconcile source and design real acceptance |
| `UI-002.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1000` | reconcile source and design real acceptance |
| `UI-002.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1001` | reconcile source and design real acceptance |
| `UI-002.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1002` | reconcile source and design real acceptance |
| `UI-002.5` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1003` | reconcile source and design real acceptance |
| `UI-003` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:718](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-003.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1020` | reconcile source and design real acceptance |
| `UI-003.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1021` | reconcile source and design real acceptance |
| `UI-003.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1022` | reconcile source and design real acceptance |
| `UI-003.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1023` | reconcile source and design real acceptance |
| `UI-004` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:734](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-004.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1040` | reconcile source and design real acceptance |
| `UI-004.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1041` | reconcile source and design real acceptance |
| `UI-004.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1042` | reconcile source and design real acceptance |
| `UI-004.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1043` | reconcile source and design real acceptance |
| `UI-005` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:750](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-005.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1059` | reconcile source and design real acceptance |
| `UI-005.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1060` | reconcile source and design real acceptance |
| `UI-005.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1061` | reconcile source and design real acceptance |
| `UI-005.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1062` | reconcile source and design real acceptance |
| `UI-006` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:766](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-006.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1079` | reconcile source and design real acceptance |
| `UI-006.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1080` | reconcile source and design real acceptance |
| `UI-006.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1081` | reconcile source and design real acceptance |
| `UI-006.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1082` | reconcile source and design real acceptance |
| `UI-007` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:782](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-007.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1101` | reconcile source and design real acceptance |
| `UI-007.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1102` | reconcile source and design real acceptance |
| `UI-007.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1103` | reconcile source and design real acceptance |
| `UI-007.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1104` | reconcile source and design real acceptance |
| `UI-008` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:800](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-008.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1121` | reconcile source and design real acceptance |
| `UI-008.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1122` | reconcile source and design real acceptance |
| `UI-008.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1123` | reconcile source and design real acceptance |
| `UI-008.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1124` | reconcile source and design real acceptance |
| `UI-009` | UI | W10 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/eoip-phase4-requirements.md:816](EOIP-engg-doc-pkg/eoip-phase4-requirements.md) | reconcile source and design real acceptance |
| `UI-009.1` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1141` | reconcile source and design real acceptance |
| `UI-009.2` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1142` | reconcile source and design real acceptance |
| `UI-009.3` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1143` | reconcile source and design real acceptance |
| `UI-009.4` | UI | W10 | untriaged | `UNTRIAGED` | `eoip-phase4-2-requirements.md:1144` | reconcile source and design real acceptance |
| `UI-01` | UI | W10 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:917` | execute complete entrypoint and negative cases |
| `UI-02` | UI | W10 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:919` | execute complete entrypoint and negative cases |
| `UI-03` | UI | W10 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:921` | execute complete entrypoint and negative cases |
| `UI-04` | UI | W10 | code_observed | `UNTRIAGED` | `KGF-MASTER-BACKLOG.md:923` | execute complete entrypoint and negative cases |
| `PUR-VER-001` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:447](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-002` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:448](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-003` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:449](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-004` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:450](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-005` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:451](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-006` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:452](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-007` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:453](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-008` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:454](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-009` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:455](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-010` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:456](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-011` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:457](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VER-012` | VER | W12 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:458](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VPU-001` | VPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:387](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VPU-002` | VPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:388](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VPU-003` | VPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:389](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VPU-004` | VPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:390](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VPU-005` | VPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:391](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `PUR-VPU-006` | VPU | W07 | code_observed | `UNTRIAGED` | [processing-units-requirements.md:392](processing-units-requirements.md) | execute complete entrypoint and negative cases |
| `E2E-WG-001.S01` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:613](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S02` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:614](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S03` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:615](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S04` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:616](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S05` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:617](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S06` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:618](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S07` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:619](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S08` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:620](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S09` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:621](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S10` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:622](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S11` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:623](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S12` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:624](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S13` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:625](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S14` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:626](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S15` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:627](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S16` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:628](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S17` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:629](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `E2E-WG-001.S18` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:630](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-ASK-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:970](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ASK-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:971](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ASK-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:972](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ASK-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:973](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ASK-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:974](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ASK-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:975](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:791](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:792](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:793](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:794](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:795](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:796](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:797](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAL-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:798](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:514](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:515](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:516](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:517](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:518](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:519](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:520](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:521](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:522](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:523](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-011` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:524](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-012` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:525](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-013` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:526](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CAP-014` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:527](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:830](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:831](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:832](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:833](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:834](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:835](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:836](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:837](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:838](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:839](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-011` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:840](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CNS-012` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:841](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-COH-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:957](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-COH-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:958](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-COH-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:959](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-COH-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:960](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-COH-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:961](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-COH-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:962](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:537](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:538](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:539](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:540](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:541](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:542](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:543](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:544](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:545](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-CTX-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:546](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-1` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1322](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-2` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1323](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-3` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1324](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-4` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1325](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-5` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1326](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-6` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1327](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-DOD-7` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1328](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-EMG-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:891](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-EMG-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:892](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-EMG-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:893](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-EMG-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:894](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-EMG-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:895](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-EMG-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:896](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ENT-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:564](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ENT-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:565](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ENT-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:566](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ENT-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:567](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ENT-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:568](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ENT-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:569](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-IPH-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:187](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-IPH-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:188](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-IPH-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:189](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-IPH-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:190](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:713](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:714](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:715](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:716](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:717](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:718](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:719](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:720](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:721](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:722](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-011` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:723](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-012` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:724](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-013` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:725](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-LES-014` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:726](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:928](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:929](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:930](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:931](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:932](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:933](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MEM-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:934](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MET-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1022](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MET-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1023](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MET-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1024](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MET-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1025](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MET-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1026](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-MET-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1027](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:942](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:943](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:944](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:945](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:946](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:947](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:948](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OBS-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:949](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ONT-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:291](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ONT-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:292](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ONT-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:293](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ONT-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:294](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ONT-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:295](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-ONT-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:296](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:648](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:649](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:650](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:651](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:652](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:653](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:654](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:655](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:656](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-OUT-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:657](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:168](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:169](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:170](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:171](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:172](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:173](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:174](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:175](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:176](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:177](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-011` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:178](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PLT-012` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:179](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:750](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:751](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:752](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:753](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:754](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:755](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-POL-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:756](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRC-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1037](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRC-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1038](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRC-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1039](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRC-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1040](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRC-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1041](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:617](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:618](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:619](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:620](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:621](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:622](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:623](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:624](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:625](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-PRE-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:626](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-SEC-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1049](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-SEC-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1050](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-SEC-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1051](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-SEC-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1052](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-SEC-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1053](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-SEC-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1054](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-TLS-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:983](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-TLS-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:984](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-TLS-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:985](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-TLS-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:986](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-TLS-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:987](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-TLS-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:988](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1064](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1065](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1066](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1067](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1068](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1069](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1070](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1071](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1072](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-010` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1073](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-011` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1074](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-012` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1075](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-013` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1076](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-014` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1077](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-UI-015` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:1078](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:764](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:765](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:766](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:767](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:768](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:769](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-VAL-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:770](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-001` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:873](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-002` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:874](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-003` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:875](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-004` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:876](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-005` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:877](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-006` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:878](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-007` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:879](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-008` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:880](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WLD-009` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-requirements.md:881](wisdom-graph-requirements.md) | reconcile source and design real acceptance |
| `WG-WP-00.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:387](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-01.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:408](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-02.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:426](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-03.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:442](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-04.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:459](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-05.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:469](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-06.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:484](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-07.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:494](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-08.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:510](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-09.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:520](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-10.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:530](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-11.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:547](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-12.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:557](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-13.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:567](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-14.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:577](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-15.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:587](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-16.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:597](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WG-WP-17.GATE` | WG | W00 | untriaged | `UNTRIAGED` | [wisdom-graph-implementation-plan.md:634](wisdom-graph-implementation-plan.md) | reconcile source and design real acceptance |
| `WP-AGENT-MEMORY-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:24](EOIP-engg-doc-pkg/implementation/wp-agent-memory.md) | reconcile source and design real acceptance |
| `WP-AGENT-MEMORY-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:33](EOIP-engg-doc-pkg/implementation/wp-agent-memory.md) | reconcile source and design real acceptance |
| `WP-AGENT-MEMORY-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:42](EOIP-engg-doc-pkg/implementation/wp-agent-memory.md) | reconcile source and design real acceptance |
| `WP-AGENT-MEMORY-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:51](EOIP-engg-doc-pkg/implementation/wp-agent-memory.md) | reconcile source and design real acceptance |
| `WP-AGENT-MEMORY-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:60](EOIP-engg-doc-pkg/implementation/wp-agent-memory.md) | reconcile source and design real acceptance |
| `WP-AGENT-MEMORY-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-agent-memory.md:69](EOIP-engg-doc-pkg/implementation/wp-agent-memory.md) | reconcile source and design real acceptance |
| `WP-CODEGRAPH-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-codegraph.md:23](EOIP-engg-doc-pkg/implementation/wp-codegraph.md) | reconcile source and design real acceptance |
| `WP-CODEGRAPH-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-codegraph.md:32](EOIP-engg-doc-pkg/implementation/wp-codegraph.md) | reconcile source and design real acceptance |
| `WP-CODEGRAPH-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-codegraph.md:41](EOIP-engg-doc-pkg/implementation/wp-codegraph.md) | reconcile source and design real acceptance |
| `WP-CODEGRAPH-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-codegraph.md:50](EOIP-engg-doc-pkg/implementation/wp-codegraph.md) | reconcile source and design real acceptance |
| `WP-CODEGRAPH-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-codegraph.md:59](EOIP-engg-doc-pkg/implementation/wp-codegraph.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:27](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:36](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:45](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:54](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:63](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:72](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-07` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:81](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-08` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:90](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-CONNECTORS-09` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-connectors.md:99](EOIP-engg-doc-pkg/implementation/wp-connectors.md) | reconcile source and design real acceptance |
| `WP-EXPERIENCE-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-experience.md:24](EOIP-engg-doc-pkg/implementation/wp-experience.md) | reconcile source and design real acceptance |
| `WP-EXPERIENCE-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-experience.md:33](EOIP-engg-doc-pkg/implementation/wp-experience.md) | reconcile source and design real acceptance |
| `WP-EXPERIENCE-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-experience.md:42](EOIP-engg-doc-pkg/implementation/wp-experience.md) | reconcile source and design real acceptance |
| `WP-EXPERIENCE-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-experience.md:51](EOIP-engg-doc-pkg/implementation/wp-experience.md) | reconcile source and design real acceptance |
| `WP-EXPERIENCE-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-experience.md:60](EOIP-engg-doc-pkg/implementation/wp-experience.md) | reconcile source and design real acceptance |
| `WP-EXPERIENCE-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-experience.md:69](EOIP-engg-doc-pkg/implementation/wp-experience.md) | reconcile source and design real acceptance |
| `WP-FOUNDATION-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-foundation.md:23](EOIP-engg-doc-pkg/implementation/wp-foundation.md) | reconcile source and design real acceptance |
| `WP-FOUNDATION-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-foundation.md:32](EOIP-engg-doc-pkg/implementation/wp-foundation.md) | reconcile source and design real acceptance |
| `WP-FOUNDATION-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-foundation.md:41](EOIP-engg-doc-pkg/implementation/wp-foundation.md) | reconcile source and design real acceptance |
| `WP-FOUNDATION-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-foundation.md:50](EOIP-engg-doc-pkg/implementation/wp-foundation.md) | reconcile source and design real acceptance |
| `WP-FOUNDATION-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-foundation.md:59](EOIP-engg-doc-pkg/implementation/wp-foundation.md) | reconcile source and design real acceptance |
| `WP-INGESTION-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ingestion.md:23](EOIP-engg-doc-pkg/implementation/wp-ingestion.md) | reconcile source and design real acceptance |
| `WP-INGESTION-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ingestion.md:32](EOIP-engg-doc-pkg/implementation/wp-ingestion.md) | reconcile source and design real acceptance |
| `WP-INGESTION-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ingestion.md:41](EOIP-engg-doc-pkg/implementation/wp-ingestion.md) | reconcile source and design real acceptance |
| `WP-INGESTION-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ingestion.md:50](EOIP-engg-doc-pkg/implementation/wp-ingestion.md) | reconcile source and design real acceptance |
| `WP-INGESTION-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ingestion.md:59](EOIP-engg-doc-pkg/implementation/wp-ingestion.md) | reconcile source and design real acceptance |
| `WP-MCP-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-mcp.md:20](EOIP-engg-doc-pkg/implementation/wp-mcp.md) | reconcile source and design real acceptance |
| `WP-MCP-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-mcp.md:29](EOIP-engg-doc-pkg/implementation/wp-mcp.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:30](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:39](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:48](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:57](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:66](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:75](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-07` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:84](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-08` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:93](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-09` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:102](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-10` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:111](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-11` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:120](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-ONTOLOGY-GRAPH-12` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md:129](EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md) | reconcile source and design real acceptance |
| `WP-QUERY-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:27](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:36](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:45](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:54](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:63](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:72](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-07` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:81](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-08` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:90](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-QUERY-09` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-query.md:99](EOIP-engg-doc-pkg/implementation/wp-query.md) | reconcile source and design real acceptance |
| `WP-RAG-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-rag.md:24](EOIP-engg-doc-pkg/implementation/wp-rag.md) | reconcile source and design real acceptance |
| `WP-RAG-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-rag.md:33](EOIP-engg-doc-pkg/implementation/wp-rag.md) | reconcile source and design real acceptance |
| `WP-RAG-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-rag.md:42](EOIP-engg-doc-pkg/implementation/wp-rag.md) | reconcile source and design real acceptance |
| `WP-RAG-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-rag.md:51](EOIP-engg-doc-pkg/implementation/wp-rag.md) | reconcile source and design real acceptance |
| `WP-RAG-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-rag.md:60](EOIP-engg-doc-pkg/implementation/wp-rag.md) | reconcile source and design real acceptance |
| `WP-RAG-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-rag.md:69](EOIP-engg-doc-pkg/implementation/wp-rag.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:32](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:41](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:50](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-04` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:59](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-05` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:68](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-06` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:77](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-07` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:86](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-08` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:95](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-09` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:104](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-10` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:113](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-11` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:122](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-12` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:131](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-13` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:140](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-SECURITY-OPS-14` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-security-ops.md:149](EOIP-engg-doc-pkg/implementation/wp-security-ops.md) | reconcile source and design real acceptance |
| `WP-VALIDATION-01` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-validation.md:21](EOIP-engg-doc-pkg/implementation/wp-validation.md) | reconcile source and design real acceptance |
| `WP-VALIDATION-02` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-validation.md:30](EOIP-engg-doc-pkg/implementation/wp-validation.md) | reconcile source and design real acceptance |
| `WP-VALIDATION-03` | WP | W00 | untriaged | `UNTRIAGED` | [EOIP-engg-doc-pkg/implementation/wp-validation.md:39](EOIP-engg-doc-pkg/implementation/wp-validation.md) | reconcile source and design real acceptance |

## Independent acceptance matrix

Run API-to-worker-to-store tests, UI/CLI/MCP/VS Code journeys, tenant revocation, crash/retry/cancel races, model task quality, no-egress probes, package/offline install, backup/restore and hardware placement only where advertised. Record observed outcomes and raw artifacts for every supported OS, backend, tenancy and model profile.

A focused passing test is evidence for that tested behavior only. Skipped hardware, missing customer integrations, unrun scale targets, unavailable vendor credentials and missing task datasets remain BLOCKED. Performance numbers require equal work, precision, environment and raw samples. A `not needed` decision requires an authorized rationale, alternative and impact record.

## Source reconciliation and change control

The source inventory in the master requirements lists every readable Markdown file with line count and hash. For each `requirement` document and any guide/research file containing normative signals, review every line against registry IDs. Add orphan clauses, resolve collisions and record deliberate dispositions. Compare file hashes on every rebuild; changed sources invalidate the previous mapping until reviewed. Historic files stay discoverable and unmodified.

The existing `requirements-registry.json` and `EOIP-programme-registry.json` remain machine input records. This plan and the master requirements are the only maintained consolidated Markdown pair. The HTML dashboard is the single project tracker. Neither the generated documents nor the dashboard should be used to edit an acceptance ledger directly.

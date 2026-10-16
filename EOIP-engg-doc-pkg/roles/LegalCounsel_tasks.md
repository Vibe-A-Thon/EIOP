# Legal Counsel — IP Protection, Licensing & Regulatory

> **Role**: Legal Counsel / General Counsel
> **Scope**: IP protection, licensing, contracts, data privacy regulations, terms of service, open-source compliance

---

## Legal Responsibilities

### 1. Intellectual Property
- **TASK-LEGAL-001**: Patent strategy — identify patentable innovations and file provisional patents
  - Status: Not Started | Priority: P0
  - Patentable candidates:
    - Token Format Engines (TOON/TRON/LEAN/ASON/ZON/ZOON/TSON) — novel token-efficient serialization
    - Graph-over-Graph — multi-layer graph query architecture
    - Intent Router — cost-optimized query classification
    - Cognitive Boundary Telemetry — agent autonomy handoff
    - Intelligence Engineering — cognitive pipeline orchestration
  - Risk: Public disclosure without patent filing loses patent rights
  - Mitigation: File provisional patents BEFORE any public demo, blog, or conference talk

- **TASK-LEGAL-002**: Trademark registration — "EOIP", "KnowGridFlow", "Enterprise Cognitive Intelligence Platform"
  - Status: Not Started | Priority: P1
  - Deliverable: Trademark applications filed

- **TASK-LEGAL-003**: Trade secret identification — classify proprietary algorithms not suitable for patenting
  - Status: Not Started | Priority: P1
  - Deliverable: Trade secret inventory with access controls

### 2. Open Source Compliance
- **TASK-LEGAL-004**: Audit all dependencies for license compatibility (GPL, LGPL, Apache, MIT, BSD)
  - Status: Not Started | Priority: P0
  - Deliverable: License audit report
  - Risk: GPL-licensed dependency contaminates proprietary code
  - Mitigation: Automated license scanning in CI (FOSSA, Snyk)
  - Current deps: FastAPI (MIT), Pydantic (MIT), Starlette (BSD), React (MIT) — generally safe

- **TASK-LEGAL-005**: Define open-source contribution policy — what can be open-sourced (Community edition) vs. proprietary
  - Status: Not Started | Priority: P1
  - Deliverable: Open-source policy document

- **TASK-LEGAL-006**: Review license implications of graph database connectors (Neo4j Community GPL, TigerGraph proprietary)
  - Status: Not Started | Priority: P1
  - Risk: Neo4j Community Edition is GPL — connector code may need isolation
  - Mitigation: Clean-room adapter pattern, dynamic loading

### 3. Customer Agreements
- **TASK-LEGAL-007**: Draft Enterprise License Agreement (ELA) for Professional/Enterprise/OEM tiers
  - Status: Not Started | Priority: P1
  - Deliverable: ELA template
  - Include: Usage rights, SLA commitments, data processing terms, liability caps

- **TASK-LEGAL-008**: Draft Terms of Service for Community edition (SaaS)
  - Status: Not Started | Priority: P1
  - Deliverable: ToS document

- **TASK-LEGAL-009**: Draft Data Processing Agreement (DPA) for GDPR compliance
  - Status: Not Started | Priority: P0
  - Deliverable: DPA template aligned with GDPR Article 28

- **TASK-LEGAL-010**: Draft Business Associate Agreement (BAA) for HIPAA-regulated customers
  - Status: Not Started | Priority: P1
  - Deliverable: BAA template

### 4. Regulatory & Privacy
- **TASK-LEGAL-011**: EU AI Act compliance assessment — classify system risk level, documentation requirements
  - Status: Not Started | Priority: P1
  - Risk: AI systems used for decision-making may be classified as high-risk under EU AI Act
  - Mitigation: Maintain XAI documentation, human oversight mechanisms, risk assessment

- **TASK-LEGAL-012**: India DPDP Act compliance — data localization requirements, consent management
  - Status: Not Started | Priority: P2
  - Current: India DPDP compliance pack exists (skeleton-only)

- **TASK-LEGAL-013**: Review AI agent actions for liability — who is responsible when an agent makes a harmful decision?
  - Status: Not Started | Priority: P1
  - Deliverable: AI liability framework
  - Risk: Agent autonomous decisions could create legal liability
  - Mitigation: Human-in-the-loop controls, audit trails, verification gates

### 5. Partnership & Employment
- **TASK-LEGAL-014**: Draft partnership agreement template for system integrators and cloud providers
  - Status: Not Started | Priority: P2
  - Dependencies: CEO partnership pipeline

- **TASK-LEGAL-015**: Employee/contractor IP assignment agreements
  - Status: Not Started | Priority: P0
  - Deliverable: IP assignment clause in all employment/contractor agreements

---

## Handoffs

| From Legal | To Role | What |
|---|---|---|
| Patent filings | CEO | IP portfolio strategy |
| License audit | CTO | Dependency decisions |
| DPA/BAA templates | Security Officer | Compliance alignment |
| ToS/ELA drafts | Licensing Manager | Enforcement |
| AI liability framework | Lead AI Engineer | Guardrail requirements |
| Open-source policy | Lead Developer | Code contribution guidelines |

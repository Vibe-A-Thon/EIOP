# Sample EOIP Requirements (fixture)

## REQ-FUNC-0001 — Document ingest pipeline

**Type:** Functional  
**Priority:** P0  
**Owner:** owner-hash-a11  

Ingest PDF and DOCX documents, emit normalized JSON, reject malware MIME types.

### Acceptance Criteria
1. Valid PDF produces JSON with fields title, pages, text.
2. Executable uploads return HTTP 415.
3. Processing completes under 30s for files ≤ 10MB.

### Related files
- src/ingest/
- tests/unit/test_ingest.py

---

ID: REQ-SEC-0002
Title: Role-based authorization on write APIs
Type: Security
Priority: P0
Description: Viewer role cannot mutate resources; Admin can. Denied calls return 403 and audit log entry.
Acceptance Criteria:
1. Viewer POST returns 403
2. Admin POST returns 201
3. Denial is logged with actor id (hashed)
Security Controls: JWT authn, RBAC authz
Estimated Effort: 24 hours

---

## REQ-AI-0003 LLM egress redaction

Type: AI

All prompts sent to external LLMs must pass through redaction middleware that strips emails and SSNs.

Acceptance Criteria:
- Redaction log entry REDACT_OK for each call
- Call aborted if redaction fails

---

## Architecture notes (not a requirement)

This paragraph should not become a requirement.

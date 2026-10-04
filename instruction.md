# Agent Orchestration Instructions and Contracts

**Purpose**  
Establish a one‑time canonical contract that every agent and LLM must follow when working on this repository. This file defines roles, handoff rules, tracking files, ticketing conventions, and the minimal runtime obligations required before any agent session ends.

**Scope**  
Applies to all agents and LLMs interacting with this repo (Kimi Code, VSCode Chat, Codex, Kimi, Automode, GPT5.5, and others). Covers reading docs, auditing, implementing, testing, demo data generation, ticketing, and handoffs.

---

## Core Contracts Agents Must Follow
- **Read Contract**: Before any work, read `instruction.md`, `context.md`, `memory.md`, `todo-status.md`, and `checklist.md`.  
- **Tracking Contract**: All progress must be recorded in the root MD files and `tickets/` as specified.  
- **Ticket Contract**: Every gap, bug, or task must be a ticket file in `tickets/` using the ticket template.  
- **Handoff Contract**: Before session end or token limits, update `memory.md` and `context.md` with exact next steps and reproduction commands.  
- **Persona Contract**: Use the persona line in `context.md` for the active role. If multiple agents collaborate, each agent must adopt the role assigned to them for that session.  
- **Commit Contract**: Commit all tracking files and ticket changes to the repo before ending the session.  
- **Ignore List**: Do not audit or act on the two files in the ignore list:  
  `f:/code/EOIP/EIOP/EOIP-engg-doc-pkg/KGR-requirements.md` and  
  `f:/code/EOIP/EIOP/EOIP-engg-doc-pkg/KGR-implementation-plan.md`.

---

## Pointers to supporting orchestration files
Agents must consult these files in addition to this document:

- **`onboarding_prompts.md`** — exact one‑time onboarding prompt and the short resume prompt `continue from left over`.  
- **`handoff_template.md`** — canonical Handoff block template to append to `memory.md` and `context.md`.  
- **`roles.md`** — persona lines for each role (CTO, Senior Engineer, QA Lead, Data Engineer, DevOps, Demo Producer, LLM Orchestrator).  
- **`onboarding_checklist.md`** — step‑by‑step checklist for the first onboarding run.  
- **`agent_runbook.md`** — operational runbook: branch/commit naming, ticket naming, update rules.  
- **`tickets/architecture-ticket.md`** — architecture notes and P0 architectural decisions.

Agents must not modify `instruction.md` enforcement rules or remove these pointers.

---

## Minimal Runtime Obligations per Session
1. **Start**: Log session start in `memory.md` with timestamp and active ticket ID.  
2. **During**: Update ticket change logs and `todo-status.md` on every ticket status change.  
3. **Before End**: Write a handoff block in `memory.md` and `context.md` containing:
   - **Current ticket ID** and status.  
   - **Branch name** and **last commit hash**.  
   - **Exact shell commands** to reproduce tests and run demo.  
   - **Next three actions** with file paths and line references.  
   - **Blockers** and required approvals.  
4. **Finish**: Commit and push the updated MD files and ticket files.

---

## Enforcement Rules
- Noncompliant agents that fail to update required tracking files must be considered invalid; their outputs must not be merged.  
- Ticket status changes without corresponding updates to `todo-status.md` and `checklist.md` are invalid.  
- Handoffs missing exact commands are incomplete.

---

## Where to Place Persona Line
Place the active persona line at the top of `context.md` as a single bold line. Example:  
**Persona**: You are the Senior Engineer. Implement tickets to acceptance criteria with clean commits and tests.

---

## Short Prompt Mechanism
After the one‑time onboarding using `instruction.md`, use this **Simple Prompt** for all subsequent agent sessions:

**Simple Prompt**  
**Resume work on ticket**: `<ticket-ID>`  
**Role**: `<role>`  
**Goal**: `<short goal, 8–12 words>`  
**Max work for this session**: `<list of 1–3 tasks>`

Example:  
`Resume work on ticket-20261004-001 Role: Senior Engineer Goal: Implement API endpoint for user import Max work for this session: update endpoint, add unit tests, update ticket status`

Every agent must prepend that simple prompt with the persona line from `context.md` and must follow the contracts in `instruction.md`.

---

## Quick links (for convenience)
- `onboarding_prompts.md`  
- `handoff_template.md`  
- `roles.md`  
- `onboarding_checklist.md`  
- `agent_runbook.md`  
- `tickets/requirements-map.md`
- `tickets/architecture-ticket.md`
- `memory.md`
- `context.md`

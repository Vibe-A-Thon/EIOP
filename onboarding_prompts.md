# Agent Prompts
One‑time onboarding prompt: 
ONBOARD-AND-POPULATE (one-time)

1. Read and accept contracts
   - Open and read these files now: instruction.md, context.md, memory.md, todo-status.md, checklist.md, agent_prompts.md, handoff_template.md, roles.md, onboarding_checklist.md, agent_runbook.md, tickets/requirements-map.md, tickets/*.md.
   - Respect the Ignore List: do NOT read or act on:
     f:/code/EOIP/EIOP/EOIP-engg-doc-pkg/KGR-requirements.md
     f:/code/EOIP/EIOP/EOIP-engg-doc-pkg/KGR-implementation-plan.md

2. Set your persona
   - Choose one persona from roles.md that matches your role for this session (CTO, Senior Engineer, QA Lead, Data Engineer, DevOps, Demo Producer, LLM Orchestrator).
   - Replace the **Persona** line at the top of context.md with that exact persona line.

3. Populate templates only if empty
   - For each root template file (context.md, memory.md, todo-status.md, checklist.md, tickets/requirements-map.md) replace placeholder fields with actual repo values **only if the field is empty or contains a placeholder**. Do not overwrite existing real data.
   - Required fields to populate when empty:
     - context.md: **Repo root**, **Active ticket** (none), **Branch** (main), **Onboarding branch**, **Test commands**, **CI commands**, **Primary services**.
     - memory.md: **Last session timestamp** (now), **Last processed ticket** (none), **Last commit hash** (`git rev-parse --short HEAD`), **Open PRs**, **Failing tests** (run tests), **Next steps** (3 shell commands), **Blockers**.
     - todo-status.md & checklist.md: add discovered tickets, priorities, owners, ETAs.
     - tickets/requirements-map.md: add first 3 requirements discovered with source file references.

4. Discover and create initial tickets
   - Scan the repo for the top 3 highest‑impact gaps (missing features, failing tests, missing demo data).
   - For each gap create a ticket file in tickets/ named `ticket-<YYYYMMDD>-<NNN>.md` using the ticket template exactly.
   - Populate ticket fields: **ID**, **Title**, **Priority**, **Status** (Open), **Reporter**, **Assignee** (temporary), **Description**, **Doc code reference**, **Acceptance criteria**, **Test plan**, **Files to modify**, **Estimated effort**, **Change log** (initial entry).
   - Add corresponding rows to tickets/requirements-map.md and update todo-status.md and checklist.md.

5. Commit, branch, push
   - Create branch: `onboarding/<role>-<YYYYMMDD>` (replace role and date).
   - Stage and commit all modified template files and new tickets with messages referencing ticket IDs, for example:
     `git add . && git commit -m "onboarding: populate templates; add ticket-2026XXXX-001"`
   - Push branch to remote: `git push -u origin onboarding/<role>-<YYYYMMDD>`

6. Write session summary and handoff
   - Append a one‑paragraph session summary to memory.md describing what you did.
   - Append a Handoff block (use the exact format from handoff_template.md) to both memory.md and context.md.
   - The Handoff block must include:
     - **Timestamp** (ISO)
     - **Active role** (persona)
     - **Branch** and **Last commit** (short hash)
     - **Current ticket** (ticket-ID or none)
     - **Next actions**: three exact shell commands with file paths and line refs
     - **Blockers** (list or none)
     - **Reproduction commands**: exact commands to run unit, integration, and demo

   **Handoff block format (copy verbatim from handoff_template.md)**

7. Finalize
   - If any required field could not be populated (missing environment info, secrets, or access), create a P0 ticket describing the missing item with reproduction steps.
   - Ensure all tracking files (context.md, memory.md, todo-status.md, checklist.md, tickets/*) are committed.
   - Push branch and end session.

IMPORTANT
- If templates already contain real data, skip population and start working on the highest priority Open tickets instead.
- Do not change enforcement rules in instruction.md.
- After this onboarding run, future sessions will use the single short prompt: `continue from left over`.

Short resume prompt: `continue from left over`
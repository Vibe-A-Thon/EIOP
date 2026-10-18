# Slack Connector API Research & Qualification Specification

*Researched per CRA-006.2, CRA-006.8. Complies with Decision H-13 and ONT-006.*

## Official API Specifications & Pinned Versions
- **Slack Web API & Events API**:
  - Pinned API endpoints: `https://slack.com/api`
  - Core Methods: `conversations.list`, `conversations.history`, `conversations.replies`
  - Event Subscriptions: `message.channels`, `message_changed`, `message_deleted`, `file_shared`
  - Rate Limiting: Tiered per method (Tier 2/3: 20-50 requests/min; Tier 4: 100+ requests/min) with HTTP 429 backoff.

## Boundary Enforcement & Decision H-13
- **Private Channels & Direct Messages (DMs)**:
  - Strict deny-by-default posture.
  - Enabling private channels (`enable_private_channels=True`) or DMs (`enable_direct_messages=True`) is strictly refused unless accompanied by an explicit, non-empty `compliance_approval_ref`.
  - Violations raise immediate configuration errors.

## Message Lifecycles, Threads, and Deletions
- Full message history preserved with microsecond timestamp pointers (`ts`).
- Thread replies linked to parent message via `repliesTo` edge.
- Deletions and edits captured as explicit `DELETE` and `UPSERT` source events.

## Mentions & Proposed Knowledge
- Slack user mentions `<@USERID>` and channel mentions are extracted into `metadata["proposed_mentions"]`.
- In accordance with CRA-023, mentions from unverified chat sources remain in `proposed` state until corroborated by authoritative identity records.

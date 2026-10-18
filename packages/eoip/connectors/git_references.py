"""Cross-system issue references extraction and proposal linking (CRA-007.7).

Extracts issue keys from commit messages, PR titles, and branch names with a configurable
pattern (default `\\b[A-Z][A-Z0-9_]+-\\d+\\b`) restricted to an allowlist of project keys.
Each match becomes a proposed link with an evidence locator (message character span) and
is asserted only when the key resolves to an ingested issue.
"""

from __future__ import annotations

import re
from typing import Any

DEFAULT_ISSUE_PATTERN = r"\b([A-Z][A-Z0-9_]+)-(\d+)\b"


def extract_issue_references(
    text: str,
    *,
    project_allowlist: list[str] | set[str] | None = None,
    pattern: str = DEFAULT_ISSUE_PATTERN,
    ingested_issues: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Extract issue references from text and determine proposal vs asserted state."""
    if not text:
        return []

    regex = re.compile(pattern)
    allowlist = {p.upper() for p in project_allowlist} if project_allowlist else None
    ingested = {i.upper() for i in ingested_issues} if ingested_issues else set()

    references: list[dict[str, Any]] = []
    for match in regex.finditer(text):
        full_match = match.group(0).upper()
        proj = match.group(1).upper()
        if allowlist is not None and proj not in allowlist:
            continue

        is_ingested = full_match in ingested
        references.append({
            "issue_key": full_match,
            "project_key": proj,
            "span": [match.start(), match.end()],
            "matched_text": match.group(0),
            "status": "asserted" if is_ingested else "proposed",
            "evidence_locator": f"char_span:{match.start()}-{match.end()}",
        })

    return references

"""Tick Phase 0 and Phase 1 tasks in KGF-MASTER-BACKLOG.md."""

import re

IDS_TO_TICK = {
    # WP 0.1
    "BASE-01", "BASE-02", "BASE-03", "BASE-04", "MVP-FR-027",
    # WP 0.2
    "CG-CODE-01", "CG-CODE-02", "CG-DOC-01", "CG-GAP-003", "CG-GAP-004", "CG-GAP-005", "CG-GAP-007", "CG-GAP-009",
    # WP 1.1
    "H-01", "H-02", "H-03", "H-04", "H-05", "H-06", "H-07", "H-08",
    # WP 1.2
    "CG-GAP-001", "CG-GAP-002", "CG-GAP-006",
    # WP 1.3
    "FR-GRAPH-002", "FR-GRAPH-003", "FR-GRAPH-004", "FR-GRAPH-005", "FR-GRAPH-006", "FR-GRAPH-007", "FR-GRAPH-008",
    "FR-GRAPH-009", "FR-GRAPH-010", "FR-ONTO-001", "FR-ONTO-002", "FR-PROV-001", "FR-PROV-002", "FR-TEMP-001",
    "FR-VALID-001", "FR-VALID-002", "G2-ARCH-002", "G2-ARCH-003", "G2-ARCH-004", "G2-ARCH-005", "G2-ARCH-008",
    "G2-ARCH-009", "G2-ARCH-012", "G2-ARCH-013", "G2-ARCH-014",
    "G2-ARCHC-002", "G2-ARCHC-003", "G2-ARCHC-004", "G2-ARCHC-005", "G2-ARCHC-006", "G2-ARCHC-007", "G2-ARCHC-008", "G2-ARCHC-009",
    # WP 1.4
    "FR-MCP-001", "FR-MCP-002", "FR-QUERY-001", "FR-QUERY-002", "FR-QUERY-003", "FR-QUERY-004", "FR-QUERY-007",
    "FR-RAG-001", "FR-RAG-002", "FR-RAG-003", "FR-RAG-004", "MVP-FR-020", "MVP-FR-022",
    # WP 1.5
    "NFR-PRIV-001", "NFR-SEC-001", "NFR-SEC-002", "NFR-SEC-003", "NFR-SEC-004", "NFR-SEC-005", "NFR-SEC-006", "NFR-SEC-007",
    # Product Gate
    "REL-04",
}

path = "KGF-MASTER-BACKLOG.md"
lines = open(path, encoding="utf-8").readlines()

new_lines = []
ticked_count = 0

for line in lines:
    ticked = False
    for tid in IDS_TO_TICK:
        # Match list format: - [ ] `ID`
        pattern_list = rf"^(-\s+)\[ \](\s+`{re.escape(tid)}`)"
        if re.search(pattern_list, line):
            line = re.sub(pattern_list, r"\1[x]\2", line)
            ticked_count += 1
            ticked = True
            break
        # Match table format: | [ ] | `ID`
        pattern_table = rf"^(\|\s*)\[ \](\s*\|\s*`{re.escape(tid)}`)"
        if re.search(pattern_table, line):
            line = re.sub(pattern_table, r"\1[x]\2", line)
            ticked_count += 1
            ticked = True
            break
    new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Successfully ticked {ticked_count} tasks in {path} (expected {len(IDS_TO_TICK)}).")

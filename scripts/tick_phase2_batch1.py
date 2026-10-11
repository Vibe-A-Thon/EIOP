"""Tick newly verified Phase 2 tasks in KGF-MASTER-BACKLOG.md."""

import re

PHASE2_TICK_IDS = {
    # WP 2.1
    "FR-CONN-001", "FR-CONN-003", "FR-CONN-004", "FR-CONN-005",
    "FR-INGEST-002", "FR-INGEST-004",
    "G2-EKAF-002", "G2-EKAF-004", "G2-EKAF-005", "G2-EKAF-006", "G2-EKAF-007",
    "G2-EKAF-008", "G2-EKAF-009", "G2-EKAF-011", "G2-EKAF-012", "G2-EKAF-013",
    "G2-EKAF-015", "G2-EKAF-019", "G2-EKAF-020", "G2-EKAF-021",
    "G2-EKAF-027", "G2-EKAF-028", "G2-EKAF-029", "G2-EKAF-030",
    # WP 2.3
    "G2-SRC-DD-002", "G2-SRC-DD-003", "G2-SRC-DD-004",
    "G2-SRC-GH-001", "G2-SRC-GH-002", "G2-SRC-GH-003", "G2-SRC-GH-004",
    "G2-SRC-GL-001", "G2-SRC-GL-002", "G2-SRC-GL-003", "G2-SRC-GL-004",
    "G2-SRC-GRAF-002", "G2-SRC-GRAF-003",
    "G2-SRC-KIB-002", "G2-SRC-KIB-003", "G2-SRC-KIB-004", "G2-SRC-KIB-005",
    # WP 2.4
    "FR-CODE-001", "FR-CODE-002", "FR-CODE-004", "FR-CODE-005",
    "G2-SRC-CODE-002", "G2-SRC-CODE-003", "G2-SRC-CODE-004", "G2-SRC-CODE-005",
}

path = "KGF-MASTER-BACKLOG.md"
lines = open(path, encoding="utf-8").readlines()

new_lines = []
ticked_count = 0

for line in lines:
    ticked = False
    for tid in PHASE2_TICK_IDS:
        pattern_list = rf"^(-\s+)\[ \](\s+`{re.escape(tid)}`)"
        if re.search(pattern_list, line):
            line = re.sub(pattern_list, r"\1[x]\2", line)
            ticked_count += 1
            ticked = True
            break
        pattern_table = rf"^(\|\s*)\[ \](\s*\|\s*`{re.escape(tid)}`)"
        if re.search(pattern_table, line):
            line = re.sub(pattern_table, r"\1[x]\2", line)
            ticked_count += 1
            ticked = True
            break
    new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Successfully ticked {ticked_count} Phase 2 tasks in {path} (expected {len(PHASE2_TICK_IDS)}).")

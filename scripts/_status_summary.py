import json
import re

with open("kgf-progress-2026-10-12.json", encoding="utf-8") as f:
    prog = json.load(f)

done = sum(1 for v in prog["s"].values() if v == "done")
in_progress = sum(1 for v in prog["s"].values() if v == "in_progress")
blocked = sum(1 for v in prog["s"].values() if v == "blocked")
not_started = sum(1 for v in prog["s"].values() if v in ("not_started", "todo", "open"))

print(f"Progress JSON total keys: {len(prog['s'])}, Done: {done}, In progress: {in_progress}, Blocked: {blocked}, Not started: {not_started}")

with open("KGF-MASTER-BACKLOG.md", encoding="utf-8") as f:
    text = f.read()

# Let's count tasks per phase in KGF-MASTER-BACKLOG.md
phase_headers = list(re.finditer(r"### Phase (\d+)\.\s*([^\n]+)", text))
for i, m in enumerate(phase_headers):
    phase_num = m.group(1)
    phase_title = m.group(2).strip()
    start_pos = m.start()
    end_pos = phase_headers[i + 1].start() if i + 1 < len(phase_headers) else len(text)
    section = text[start_pos:end_pos]

    # match both table rows and list items
    ticked = len(re.findall(r"(?:\|\s*\[x\]\s*\||-\s*\[x\])\s*`([^`]+)`", section))
    unticked = len(re.findall(r"(?:\|\s*\[\s*\]\s*\||-\s*\[\s*\])\s*`([^`]+)`", section))
    total = ticked + unticked
    print(f"- Phase {phase_num} {phase_title}: {ticked}/{total} done (unticked: {unticked})")

# Check unticked in Phase 4
m4 = re.search(r"### Phase 4\..*?(?=### Phase 5|\Z)", text, re.DOTALL)
if m4:
    unticked_p4 = re.findall(r"\|\s*\[\s*\]\s*\|\s*`([^`]+)`", m4.group(0))
    print(f"Unticked in Phase 4: {unticked_p4}")

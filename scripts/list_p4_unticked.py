import json
import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
prog = json.load(open('kgf-progress-2026-10-12.json', encoding='utf-8'))['s']

in_p4 = False
p4_tasks = []
curr_wp = ""

for line in lines:
    if '## Phase 4' in line or '### Phase 4' in line:
        in_p4 = True
    elif in_p4 and (line.startswith(("## Phase 5", "### Phase 5"))):
        break
    if in_p4:
        if line.startswith('#### '):
            curr_wp = line.strip()
        m = re.search(r'\[([ x])\]\s*\|\s*`([^`]+)`|[-*]\s*\[([ x])\]\s*`([^`]+)`', line)
        if m:
            chk_str = m.group(1) or m.group(3)
            is_checked = chk_str == 'x'
            t_id = m.group(2) or m.group(4)
            done = prog.get(t_id) == 'done'
            p4_tasks.append((curr_wp, t_id, is_checked, done, line.strip()))

print(f"Total Phase 4 backlog tasks found: {len(p4_tasks)}")
unticked = [t for t in p4_tasks if not t[3]]
print(f"Unticked in Phase 4: {len(unticked)}")

by_wp = {}
for wp, tid, chk, done, raw in unticked:
    by_wp.setdefault(wp, []).append((tid, raw))

for wp, items in by_wp.items():
    print(f"\n{wp} ({len(items)} remaining):")
    for tid, raw in items:
        print(f"  {tid}")

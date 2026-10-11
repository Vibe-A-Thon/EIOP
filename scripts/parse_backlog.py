import re
from collections import defaultdict

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = 'Header'
cur_wp = ''
phase_counts = defaultdict(lambda: {'total': 0, 'done': 0})
all_tasks = []

for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    m = re.match(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?", line)
    if m:
        st, tid, title = m.groups()
        all_tasks.append((cur_phase, st, tid, title.strip() if title else ''))
        phase_counts[cur_phase]['total'] += 1
        if st == 'x':
            phase_counts[cur_phase]['done'] += 1

print("=== Backlog Status by Phase ===")
for p, counts in phase_counts.items():
    done = counts['done']
    total = counts['total']
    pct = (done / total * 100) if total else 0
    print(f"{p}: {done}/{total} completed ({pct:.1f}%)")

total_done = sum(c['done'] for c in phase_counts.values())
total_all = sum(c['total'] for c in phase_counts.values())
print(f"\nTOTAL: {total_done}/{total_all} tasks ticked ({total_done/total_all*100:.1f}%)")


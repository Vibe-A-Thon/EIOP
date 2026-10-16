import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = 'Header'
cur_wp = ''
p2_tasks = []

for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    m = re.match(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?", line)
    if m:
        st, tid, title = m.groups()
        if 'Phase 2' in cur_phase:
            p2_tasks.append((cur_wp, st, tid, title.strip() if title else ''))

print(f"Total Phase 2 tasks: {len(p2_tasks)}")
unticked = [t for t in p2_tasks if t[1] != 'x']
print(f"Unticked Phase 2 tasks: {len(unticked)}")
for wp, st, tid, title in unticked:
    print(f"{wp} | [{st}] {tid}: {title}")

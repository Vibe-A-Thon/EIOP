import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = ''
cur_wp = ''
p4_tasks = []

pattern = re.compile(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?")

for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip()
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    m = pattern.match(line)
    if m:
        st, tid, title = m.groups()
        if 'Phase 4' in cur_phase:
            p4_tasks.append((cur_wp, st, tid, title.strip() if title else ''))

print(f'Total Phase 4 tasks: {len(p4_tasks)}')
wp_groups = {}
for wp, st, tid, title in p4_tasks:
    wp_groups.setdefault(wp, []).append((st, tid, title))

for wp, tasks in wp_groups.items():
    print(f"\n{wp} ({len(tasks)} tasks):")
    for st, tid, title in tasks[:4]:
        print(f"  [{st}] {tid}: {title}")
    if len(tasks) > 4:
        print(f"  ... and {len(tasks) - 4} more")

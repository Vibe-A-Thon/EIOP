import json
import re

progress = json.load(open('kgf-progress-2026-10-11.json', encoding='utf-8'))['s']
lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()

cur_phase = ''
cur_wp = ''
p3_tasks = []

for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    m = re.match(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?", line)
    if m and 'Phase 3' in cur_phase:
        st, tid, title = m.groups()
        p3_tasks.append((cur_wp, st, tid, title.strip() if title else ''))

print(f"Total Phase 3 tasks in backlog: {len(p3_tasks)}")
done_in_backlog = [t for t in p3_tasks if t[1] == 'x']
print(f"Marked [x] in backlog: {len(done_in_backlog)}")
for wp, st, tid, title in done_in_backlog:
    print(f"  Backlog [x]: {tid} - {title}")

done_in_json = [t for t in p3_tasks if progress.get(t[2]) == 'done']
print(f"Marked done in kgf-progress-2026-10-11.json: {len(done_in_json)}")
for wp, st, tid, title in done_in_json:
    print(f"  JSON done: {tid} - {title}")

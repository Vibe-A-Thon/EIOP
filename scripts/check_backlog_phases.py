import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = ''
stats = {}
for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
        if cur_phase not in stats: stats[cur_phase] = {'total': 0, 'unticked': 0}
    m = re.match(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?", line)
    if m:
        st, tid, title = m.groups()
        if cur_phase:
            stats[cur_phase]['total'] += 1
            if st != 'x':
                stats[cur_phase]['unticked'] += 1

print(f"{'Phase':<15} | {'Unticked':<8} | {'Total':<8}")
print("-" * 35)
total_unticked = 0
total_all = 0
for phase, s in sorted(stats.items()):
    print(f"{phase:<15} | {s['unticked']:<8} | {s['total']:<8}")
    total_unticked += s['unticked']
    total_all += s['total']
print("-" * 35)
print(f"{'TOTAL':<15} | {total_unticked:<8} | {total_all:<8}")

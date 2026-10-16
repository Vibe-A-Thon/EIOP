import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = ''
cur_wp = ''
for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    if 'Phase 2' in cur_phase:
        if line.strip().startswith('| [ ]') or line.strip().startswith('- [ ]'):
            cols = [c.strip() for c in line.split('|')]
            print(f"{cur_wp} | {line.strip()}")

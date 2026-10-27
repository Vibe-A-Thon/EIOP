import re
import glob

# Get unticked tasks from list_phase2_unticked.py
lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = 'Header'
cur_wp = ''
unticked = []
for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    m = re.match(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?", line)
    if m:
        st, tid, title = m.groups()
        if 'Phase 2' in cur_phase and st != 'x':
            unticked.append((tid, title.strip() if title else ''))

# Find all @pytest.mark.req across tests/
all_tests = glob.glob('tests/**/*.py', recursive=True)
req_to_files = {}
for tf in all_tests:
    try:
        content = open(tf, encoding='utf-8').read()
        for m in re.finditer(r"@pytest\.mark\.req\(([^)]+)\)", content):
            args = [a.strip(' "\' \n\t') for a in m.group(1).split(',')]
            for a in args:
                if a not in req_to_files:
                    req_to_files[a] = set()
                req_to_files[a].add(tf.replace('\\', '/'))
    except Exception:
        pass

import json
with open('requirements-registry.json', encoding='utf-8') as f:
    reg = json.load(f)
reg_by_id = {x['id']: x for x in reg}

print(f"Total unticked: {len(unticked)}")
for tid, title in unticked:
    found = req_to_files.get(tid, set())
    item = reg_by_id.get(tid, {})
    reg_title = item.get('title', '')
    print(f"{tid:18} | found: {len(found):2} | {reg_title}")

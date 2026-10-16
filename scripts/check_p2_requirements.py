import json

with open('requirements-registry.json', encoding='utf-8') as f:
    reg = json.load(f)

print(f"reg type: {type(reg)}, len: {len(reg)}")
if isinstance(reg, list):
    print("Sample reg item:", reg[0] if reg else None)
    all_reg_ids = {r.get('id') for r in reg if isinstance(r, dict)}
elif isinstance(reg, dict):
    print("reg keys:", list(reg.keys())[:10])
    all_reg_ids = set(reg.keys())

with open('requirements-test-map.json', encoding='utf-8') as f:
    tmap = json.load(f)

import re
lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = ''
unticked_ids = []
for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    m = re.match(r"^(?:-\s+|\s*\|\s*)\[([ x~!])\]\s*(?:\|\s*)?`([^`]+)`(?:\s*\|\s*([^|]+))?", line)
    if m:
        st, tid, title = m.groups()
        if 'Phase 2' in cur_phase and st != 'x':
            unticked_ids.append((tid, title.strip() if title else ''))

print(f"Unticked Phase 2 IDs: {len(unticked_ids)}")
in_reg_count = 0
in_tmap_count = 0
for tid, title in unticked_ids:
    has_reg = tid in all_reg_ids
    has_test = tid in tmap
    if has_reg: in_reg_count += 1
    if has_test: in_tmap_count += 1
    print(f"{tid:20} | in_reg={has_reg!s:5} | in_tmap={has_test!s:5} | tests={tmap.get(tid, [])}")

print(f"\nSummary: {in_reg_count}/{len(unticked_ids)} in registry, {in_tmap_count}/{len(unticked_ids)} in test-map")

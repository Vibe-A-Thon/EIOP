import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
cur_phase = 'Header'
cur_wp = ''
target_ids = ['G2-EKAF-003', 'G2-EKAF-010', 'G2-EKAF-014', 'G2-EKAF-016', 'G2-EKAF-023', 'G2-EKAF-024', 'G2-EKAF-025', 'G2-EKAF-026', 'CONN-01', 'CONN-02', 'CONN-03', 'FR-CONF-001', 'FR-SNOW-001']

for line in lines:
    if line.startswith('### Phase'):
        cur_phase = line.strip().split('.')[0].replace('### ', '')
    elif line.startswith('#### WP'):
        cur_wp = line.strip()
    for tid in target_ids:
        if f"`{tid}`" in line:
            print(f"{cur_phase} | {cur_wp} | {line.strip()}")

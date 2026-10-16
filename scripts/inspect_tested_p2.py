import re

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
check_ids = ['G2-EKAF-003', 'FR-CONF-001', 'FR-SNOW-001', 'G2-SRC-CONF-002', 'G2-SRC-CONF-003', 'G2-SRC-CONF-004', 'G2-SRC-CONF-005', 'G2-SRC-WEB-002', 'G2-SEC-CRAWL-002']

for idx, line in enumerate(lines):
    for cid in check_ids:
        if f"`{cid}`" in line:
            print(f"L{idx+1}: {line.strip()}")

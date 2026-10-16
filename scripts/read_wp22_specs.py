import re

with open('EOIP-engg-doc-pkg/gaps2-requirements.md', encoding='utf-8') as f:
    text = f.read()

target_ids = [
    'G2-EVENT-002', 'G2-EVENT-003', 'G2-EVENT-004', 'G2-EVENT-005', 'G2-EVENT-006', 'G2-EVENT-007',
    'G2-SYNC-002', 'G2-SYNC-003', 'G2-SYNC-004', 'G2-SYNC-005', 'G2-SYNC-006', 'G2-SYNC-007',
    'G2-SYNC-008', 'G2-SYNC-009', 'G2-SYNC-010', 'G2-SYNC-011', 'G2-SYNC-012', 'G2-SYNC-013', 'G2-SYNC-014'
]

for tid in target_ids:
    idx = text.find(tid)
    if idx != -1:
        snippet = text[idx:idx+350].split('\n\n')[0]
        print(f"=== {tid} ===")
        print(snippet.strip())
        print()
    else:
        print(f"=== {tid} NOT FOUND ===")

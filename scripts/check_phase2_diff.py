"""Check which IDs from PHASE2_TICK_IDS were not found."""

from tick_phase2_batch1 import PHASE2_TICK_IDS

lines = open('KGF-MASTER-BACKLOG.md', encoding='utf-8').readlines()
all_text = ''.join(lines)

for tid in PHASE2_TICK_IDS:
    if f"`{tid}`" not in all_text:
        print(f"Not in backlog: {tid}")
    elif f"[x] | `{tid}`" not in all_text and f"[x] `{tid}`" not in all_text:
        print(f"Not ticked: {tid}")

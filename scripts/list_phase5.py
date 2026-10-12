import re

with open("KGF-MASTER-BACKLOG.md", encoding="utf-8") as f:
    text = f.read()

m5 = re.search(r"### Phase 5\..*?(?=### Phase 6|\Z)", text, re.DOTALL)
if m5:
    phase5_text = m5.group(0)
    # find all subheadings (#### WP ...)
    wps = list(re.finditer(r"(####\s*WP\s*[^\n]+)", phase5_text))
    for i, wp in enumerate(wps):
        wp_title = wp.group(1)
        start = wp.start()
        end = wps[i + 1].start() if i + 1 < len(wps) else len(phase5_text)
        wp_sec = phase5_text[start:end]
        tasks = re.findall(r"(?:\|\s*\[([ x~]*)\]\s*\||-\s*\[([ x~]*)\])\s*`([^`]+)`\s*\|\s*([^|\n]+)", wp_sec)
        print(f"\n{wp_title} (Found: {len(tasks)})")
        for mark1, mark2, tid, desc in tasks:
            mark = (mark1 or mark2).strip()
            print(f"  [{mark}] {tid}: {desc.strip()[:60]}")

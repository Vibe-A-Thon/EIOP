import re

text = open("KGF-MASTER-BACKLOG.md", encoding="utf-8").read()
m6 = re.search(r"### Phase 6\..*?(?=### Phase 7|\Z)", text, re.DOTALL)
if m6:
    content = m6.group(0)
    wps = re.findall(r"####\s+([^\n]+)", content)
    print("Work packages in Phase 6:")
    for wp in wps:
        print("  -", wp)
    tasks = re.findall(r"\|\s*\[ \]\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)", content)
    print(f"\nTotal unticked tasks in Phase 6: {len(tasks)}")
    for tid, title in tasks[:15]:
        print(f"  {tid}: {title.strip()}")

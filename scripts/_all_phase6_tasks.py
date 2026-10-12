import re

text = open("KGF-MASTER-BACKLOG.md", encoding="utf-8").read()
m6 = re.search(r"### Phase 6\..*?(?=### Phase 7|\Z)", text, re.DOTALL)
if m6:
    sec = m6.group(0)
    tasks = re.findall(r"(?:\|\s*\[ \]\s*\||-\s*\[ \]\s*)\s*`([^`]+)`", sec)
    print(f"Total tasks in Phase 6: {len(tasks)}")
    print(tasks)

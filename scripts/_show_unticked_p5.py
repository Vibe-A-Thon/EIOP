import re

text = open("KGF-MASTER-BACKLOG.md", encoding="utf-8").read()
m5 = re.search(r"### Phase 5\..*?(?=### Phase 6|\Z)", text, re.DOTALL)
if m5:
    unticked_tables = re.findall(r"\|\s*\[ \]\s*\|\s*`([^`]+)`", m5.group(0))
    unticked_lists = re.findall(r"-\s*\[ \]\s*`([^`]+)`", m5.group(0))
    all_unticked = unticked_tables + unticked_lists
    print(f"Total unticked in Phase 5: {len(all_unticked)}")
    for u in all_unticked:
        print(u)

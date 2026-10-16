import re

with open("KGF-MASTER-BACKLOG.md", encoding="utf-8") as f:
    text = f.read()

m = re.search(r"#### WP 5\.3\..*?(?=#### WP 5\.4|\Z)", text, re.DOTALL)
if m:
    print(m.group(0))

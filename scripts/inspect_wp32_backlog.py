import re

with open("KGF-MASTER-BACKLOG.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

in_wp = False
for line in lines:
    if "#### WP 3.2." in line:
        in_wp = True
    elif in_wp and line.startswith("#### WP "):
        break
    if in_wp:
        print(line, end="")

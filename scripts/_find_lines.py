with open("KGF-MASTER-BACKLOG.md", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "GAP-SEC" in line or "WP 5." in line:
        print(f"{i+1}: {line.strip()}")

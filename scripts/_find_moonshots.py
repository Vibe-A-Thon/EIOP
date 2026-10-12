from pathlib import Path

for p in Path(".").glob("**/*moonshot*"):
    print(p)
for p in Path("EOIP-engg-doc-pkg").glob("**/*.md"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    if "MS-15" in text or "MS-22" in text:
        print(f"Found MS-15/22 in {p}")

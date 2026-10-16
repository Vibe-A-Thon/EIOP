import os
from pathlib import Path

pkg = Path("EOIP-engg-doc-pkg")
for p in pkg.glob("**/*.md"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    for term in ["G2-SIM-002", "G2-TWIN-002", "G2-IMMUNE-002"]:
        if term in text:
            print(f"Found {term} in {p}")

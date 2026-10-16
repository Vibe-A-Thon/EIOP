import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding="utf-8")
gaps2 = Path("EOIP-engg-doc-pkg/gaps2-requirements.md").read_text(encoding="utf-8")

def find_reqs(prefix):
    matches = re.findall(rf"(###?\s*`?({prefix}[^\n`]+)`?.*?(?=(?:###?\s*`?G2-|\Z)))", gaps2, re.DOTALL)
    for m in matches:
        print("="*60)
        print(m[0][:400])

print("PERF REQS:")
find_reqs("G2-PERF")

print("\nREL REQS:")
find_reqs("G2-REL")

print("\nSLO REQS:")
find_reqs("G2-SLO")

print("\nTEL REQS:")
find_reqs("G2-TEL")

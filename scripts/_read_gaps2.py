from pathlib import Path
import re

gaps2 = Path("EOIP-engg-doc-pkg/gaps2-requirements.md").read_text(encoding="utf-8")

def find_reqs(prefix):
    matches = re.findall(rf"(###?\s*`?({prefix}[^\n`]+)`?.*?(?=(?:###?\s*`?G2-|\Z)))", gaps2, re.DOTALL)
    for m in matches:
        print("="*60)
        print(m[0][:500])

print("SIMULATION REQS:")
find_reqs("G2-SIM")

print("\nDIGITAL TWIN REQS:")
find_reqs("G2-TWIN")

print("\nIMMUNE REQS:")
find_reqs("G2-IMMUNE")

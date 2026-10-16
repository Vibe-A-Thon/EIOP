import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding="utf-8")
text = Path("EOIP-engg-doc-pkg/diamond-moonshots-advanced.md").read_text(encoding="utf-8")

for ms_id in ["MS-15", "MS-18", "MS-19", "MS-21", "MS-22", "MS-23", "MS-24", "MS-29", "MS-30"]:
    print("="*60)
    print(f"SEARCHING FOR {ms_id}:")
    pattern = rf"(###?\s*`?{ms_id}[^\n`]*`?.*?(?=(?:###?\s*`?MS-|\Z)))"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        print(match.group(1)[:1200])
    else:
        idx = text.find(ms_id)
        if idx != -1:
            print(text[idx:idx+1000])
        else:
            print("NOT FOUND")

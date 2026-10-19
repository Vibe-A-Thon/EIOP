"""Audit all JavaScript property accesses against Python data dictionaries
"""
import re
import json
from pathlib import Path

dash_text = Path("EOIP-master-dashboard.html").read_text(encoding="utf-8")

# Extract datasets
for ds_name in ["CAPS_ITEMS", "TECHS_ITEMS", "ADRS_ITEMS", "WPS_ITEMS", "INVS_ITEMS", "GAPS_ITEMS", "PROC_UNITS", "PROC_OPS", "PROC_WPS", "PROC_RECEIPTS"]:
    m = re.search(rf"const\s+{ds_name}\s*=\s*(\[.*?\]);", dash_text, re.DOTALL)
    if m:
        try:
            items = json.loads(m.group(1))
            if items:
                print(f"{ds_name}: {len(items)} items. Sample keys: {list(items[0].keys())}")
            else:
                print(f"{ds_name}: 0 items")
        except Exception as e:
            print(f"Error parsing {ds_name}: {e}")
    else:
        print(f"{ds_name}: NOT FOUND in HTML")

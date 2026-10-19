import re
from pathlib import Path

text = Path("EOIP-master-dashboard.html").read_text(encoding="utf-8")
print("Length of dashboard:", len(text))

# Check REQS_ITEMS
m_reqs = re.search(r"const REQS_ITEMS = (\[.*?\]);\nconst CAPS_ITEMS", text, re.DOTALL)
if m_reqs:
    import json
    reqs = json.loads(m_reqs.group(1))
    print(f"REQS_ITEMS count: {len(reqs)}")
    print(f"Sample REQS_ITEMS[0]: {reqs[0]}")
    # Check if any have 'fam' or 'st' or 'cp' as undefined
    has_fam = all('fam' in r for r in reqs)
    has_st = all('st' in r for r in reqs)
    has_cp = all('cp' in r for r in reqs)
    print(f"All reqs have 'fam': {has_fam}, 'st': {has_st}, 'cp': {has_cp}")
else:
    print("REQS_ITEMS block not found via regex!")

# Check PROG_ITEMS
m_prog = re.search(r"const PROG_ITEMS = (\[.*?\]);\nconst REQS_ITEMS", text, re.DOTALL)
if m_prog:
    import json
    prog = json.loads(m_prog.group(1))
    print(f"PROG_ITEMS count: {len(prog)}")
    print(f"Sample PROG_ITEMS[0]: {prog[0]}")
    has_prio = all('prio' in p for p in prog)
    has_st = all('st' in p for p in prog)
    has_grp = all('grp' in p for p in prog)
    print(f"All prog items have 'prio': {has_prio}, 'st': {has_st}, 'grp': {has_grp}")

# Check TECHS_ITEMS
m_tech = re.search(r"const TECHS_ITEMS = (\[.*?\]);\nconst ADRS_ITEMS", text, re.DOTALL)
if m_tech:
    import json
    techs = json.loads(m_tech.group(1))
    print(f"TECHS_ITEMS count: {len(techs)}")
    print(f"Sample TECHS_ITEMS[0]: {techs[0]}")
    has_cat = all('cat' in t for t in techs)
    has_lic = all('lic' in t for t in techs)
    has_air = all('air_gap' in t for t in techs)
    print(f"All tech items have 'cat': {has_cat}, 'lic': {has_lic}, 'air_gap': {has_air}")

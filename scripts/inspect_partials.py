import json
from pathlib import Path

ROOT = Path(".").resolve()
with open("requirements-registry.json", "r", encoding="utf-8") as f:
    raw_reqs = json.load(f)
with open("requirements-test-map.json", "r", encoding="utf-8") as f:
    test_map = json.load(f)

partial_with_cp_no_tf = []
partial_with_tf_no_cp = []
missed_reqs = []

for r in raw_reqs:
    rid = r.get("id")
    prio = r.get("priority") or r.get("audit_baseline", {}).get("priority", "P2").replace("`", "")
    
    # Code paths
    cps = r.get("code_paths", [])
    valid_cp = [p for p in cps if (ROOT / p).exists()]
    if not valid_cp:
        ev = r.get("audit_baseline", {}).get("evidence", "")
        if ev:
            ev_clean = ev.replace("`", "").split(":")[0].strip()
            if ev_clean and (ROOT / ev_clean).exists():
                valid_cp = [ev_clean]
    if not valid_cp:
        pe = r.get("implementation", {}).get("public_entrypoints", [])
        valid_cp = [p for p in pe if (ROOT / p).exists()]

    # Test files
    tfs = r.get("test_files", [])
    valid_tf = [t for t in tfs if (ROOT / t).exists()]
    if not valid_tf:
        t_ev = r.get("audit_baseline", {}).get("tests", "")
        if t_ev:
            t_clean = t_ev.replace("`", "").split(":")[0].strip()
            if t_clean and (ROOT / t_clean).exists():
                valid_tf = [t_clean]

    mapped = test_map.get(rid, [])

    if valid_cp and not (valid_tf or mapped):
        partial_with_cp_no_tf.append((rid, r.get("title", ""), valid_cp[0]))
    elif (valid_tf or mapped) and not valid_cp:
        raw_cp = cps[0] if cps else (r.get("audit_baseline", {}).get("evidence", ""))
        partial_with_tf_no_cp.append((rid, r.get("title", ""), (valid_tf or mapped)[0], raw_cp))
    elif not valid_cp and not (valid_tf or mapped):
        if prio in ["P0", "P1", "MUST"]:
            missed_reqs.append((rid, prio, r.get("title", "")))

print(f"partial with cp but no tf: {len(partial_with_cp_no_tf)}")
for it in partial_with_cp_no_tf[:20]:
    print("  CP_NO_TF:", it)

print(f"\npartial with tf but no cp: {len(partial_with_tf_no_cp)}")
for it in partial_with_tf_no_cp[:20]:
    print("  TF_NO_CP:", it)

print(f"\nmissed reqs (P0/P1/MUST): {len(missed_reqs)}")
for it in missed_reqs[:20]:
    print("  MISSED:", it)

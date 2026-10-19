import sys
sys.stdout.reconfigure(encoding="utf-8")
import json

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("const D = ")
end = text.find(";\n", pos)
D = json.loads(text[pos + len("const D = "):end])

print("=== GAPS_V3 ===")
for g in D.get("gaps_v3", []):
    print(g)

print("\n=== WPS ===")
for w in D.get("wps", []):
    print(w)

print("\n=== GATES ===")
print(json.dumps(D.get("gates", {}), indent=2))

print("\n=== REQS (Sample 3) ===")
for r in D.get("reqs", [])[:3]:
    print(r)

print("\n=== INVS_V3 (Sample 3) ===")
for inv in D.get("invs_v3", [])[:3]:
    print(inv)

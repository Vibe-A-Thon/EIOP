import sys
sys.stdout.reconfigure(encoding="utf-8")
import json

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("const D = ")
end = text.find(";\n", pos)
D = json.loads(text[pos + len("const D = "):end])
caps = D.get("caps", [])
print(f"Total caps in ontology dashboard: {len(caps)}")
verif_count = sum(1 for c in caps if c.get("dec") == "VERIFIED")
roadmap_count = sum(1 for c in caps if c.get("dec") == "ROADMAP")
print(f"Verified: {verif_count}, Roadmap: {roadmap_count}")
for cid in ["CAP-02", "CAP-05", "CAP-07", "CAP-10", "CAP-46", "CAP-47"]:
    c = next(x for x in caps if x["id"] == cid)
    print(f"  {c['id']}: dec={c['dec']}, pri={c['pri']}, code={c.get('code_path', '')[:35]}, baseline={c['baseline'][:45]}...")

ind = D.get("ind", [])
print(f"\nTotal ind rows: {len(ind)}")
for r in ind[:4]:
    print(f"  {r['id']}: {r['tool']} -> mean={r.get('mean')}")

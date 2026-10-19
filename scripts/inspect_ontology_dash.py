import re
import json

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("const D = ")
end = text.find(";\n", pos)
D = json.loads(text[pos + len("const D = "):end])

print("=== DATA OBJECT D SUMMARY ===")
for k in D:
    v = D[k]
    if isinstance(v, list):
        print(f"  {k}: {len(v)} items")
    elif isinstance(v, dict):
        print(f"  {k}: {len(v)} keys")
    else:
        print(f"  {k}: {type(v)}")

# Check what competitors are evaluated in ind or agg
print("\n=== COMPETITOR EVALUATIONS (ind/agg) ===")
ind = D.get("ind", [])
print(f"Total individuals/competitors in 'ind': {len(ind)}")
for item in ind[:10]:
    if isinstance(item, dict):
        print(f"  {item.get('id')}: {item.get('name')} | category={item.get('cat')} | total_score={item.get('total')}")

agg = D.get("agg", [])
print(f"Total in 'agg': {len(agg)}")
if agg:
    print("  agg sample:", agg[0])

# Check what the JavaScript rendering functions do
print("\n=== JAVASCRIPT RENDERING FUNCTIONS ===")
fn_matches = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print("Functions found:", fn_matches)

# Check panel renders
for fn in ["renderScorecard", "renderCapabilities", "renderTechCensus", "renderArchitecture", "renderRequirements", "renderOntBacklog", "renderInversions", "renderGaps"]:
    p = text.find(f"function {fn}")
    if p != -1:
        print(f"\n--- {fn} ---")
        print(text[p:p+600])

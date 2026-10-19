import re
import json

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("const D = ")
end = text.find(";\n", pos)
D = json.loads(text[pos + len("const D = "):end])

print("Scorecard dimensions:", D.get("dims"))
print("\nFirst 5 items in 'ind':")
for it in D.get("ind", [])[:5]:
    print(it)

print("\nFirst 5 items in 'agg':")
for it in D.get("agg", [])[:5]:
    print(it)

# Let's find renderHeat or renderScorecard implementation
for fn in ["renderHeat", "datasetRows", "cellClass", "initScoreControls"]:
    p = text.find(f"function {fn}")
    if p != -1:
        print(f"\n--- {fn} ---")
        print(text[p:p+400])

# Check the HTML for the scorecard view
p_score = text.find('id="view-scorecard"')
if p_score == -1:
    p_score = text.find('data-view="scorecard"')
if p_score == -1:
    p_score = text.find('scorecard')
print("\nHTML around scorecard:", text[p_score:p_score+600])

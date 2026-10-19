import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find the scorecard controls
pos_controls = text.find('id="scorecard"')
if pos_controls == -1:
    pos_controls = text.find('fData')
print("=== SCORECARD CONTROLS ===")
print(text[pos_controls-200:pos_controls+800])

# Find datasetRows function
pos_fn = text.find("function datasetRows")
print("\n=== DATASET ROWS FUNCTION ===")
print(text[pos_fn:pos_fn+600])

import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("const NOTES = ")
pos_end = text.find("function renderHeat", pos)
print("=== NOTES THROUGH RENDERHEAT ===")
print(text[pos:pos_end])

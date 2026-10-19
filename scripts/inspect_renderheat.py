import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("function renderHeat()")
pos_end = text.find("function moveTip", pos)
print("=== RENDERHEAT FULL ===")
print(text[pos:pos_end])

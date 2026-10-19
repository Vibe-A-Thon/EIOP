import sys
sys.stdout.reconfigure(encoding="utf-8")
import re

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find the header, title, and summary banner
pos_body = text.find("<body")
pos_nav = text.find("<nav", pos_body)
print("=== HEADER & BANNER ===")
print(text[pos_body:pos_nav])

# Find the score controls and filters above the scorecard table
pos_main = text.find("<main")
pos_score = text.find('id="scoreHeat"', pos_main)
print("\n=== SCORE CONTROLS & KPI SUMMARY ===")
print(text[pos_main:pos_score])

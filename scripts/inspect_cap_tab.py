import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("ontology-analysis-dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find the capabilities panel HTML
pos_p_cap = text.find('id="p-capabilities"')
pos_next_p = text.find('id="p-tech_census"', pos_p_cap)
print("=== CAPABILITIES PANEL HTML ===")
print(text[pos_p_cap:pos_next_p])

# Find renderCapabilities function
pos_fn = text.find("function renderCapabilities")
pos_next_fn = text.find("function renderRegistry", pos_fn)
print("\n=== RENDERCAPABILITIES FUNCTION ===")
print(text[pos_fn:pos_next_fn])

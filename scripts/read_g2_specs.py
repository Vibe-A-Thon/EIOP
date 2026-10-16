import re

with open('EOIP-engg-doc-pkg/gaps2-requirements.md', encoding='utf-8') as f:
    text = f.read()

wp21_ids = [
    'G2-EKAF-003', 'G2-EKAF-010', 'G2-EKAF-014', 'G2-EKAF-016', 
    'G2-EKAF-023', 'G2-EKAF-024', 'G2-EKAF-025', 'G2-EKAF-026'
]

for tid in wp21_ids:
    m = re.search(rf"(###?\s*{tid}[^\n]*\n(?:(?!(?:###?\s*G2-))[^\n]*\n)*)", text)
    if m:
        print(f"==================== {tid} ====================")
        print(m.group(1).strip()[:1000])
        print()
    else:
        # try simple search
        idx = text.find(tid)
        if idx != -1:
            print(f"==================== {tid} (simple find) ====================")
            print(text[idx-50:idx+400])
            print()

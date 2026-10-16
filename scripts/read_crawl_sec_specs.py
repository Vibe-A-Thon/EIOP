with open('EOIP-engg-doc-pkg/gaps2-requirements.md', encoding='utf-8') as f:
    text = f.read()

target_ids = [f"G2-SEC-CRAWL-{i:03d}" for i in range(2, 13)]
for tid in target_ids:
    idx = text.find(tid)
    if idx != -1:
        snippet = text[idx:idx+350].split('\n\n')[0]
        print(f"=== {tid} ===")
        print(snippet.strip())
        print()
    else:
        print(f"=== {tid} NOT FOUND ===")

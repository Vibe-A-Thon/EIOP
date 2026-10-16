import re

for doc in [
    "KGF-MASTER-BACKLOG.md",
    "EOIP-engg-doc-pkg/03-functional-requirements.md",
    "EOIP-engg-doc-pkg/gaps2-requirements.md",
    "EOIP-engg-doc-pkg/MVP-requirements.md",
]:
    try:
        content = open(doc, encoding="utf-8").read()
        print(f"================ {doc} ================")
        for req in [
            "FR-VSCODE-001", "FR-VSCODE-002",
            "G2-VSC-002", "G2-VSC-003", "G2-VSC-004", "G2-VSC-005", "G2-VSC-006", "G2-VSC-007", "G2-VSC-008",
            "MVP-FR-019"
        ]:
            matches = [m.start() for m in re.finditer(re.escape(req), content)]
            if matches:
                print(f"--- {req} found {len(matches)} times ---")
                for pos in matches[:2]:
                    snippet = content[max(0, pos - 50):min(len(content), pos + 300)]
                    print(snippet.strip())
                    print("...")
    except Exception as e:
        print(f"Error reading {doc}: {e}")

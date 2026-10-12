import re

for doc in [
    "KGF-MASTER-BACKLOG.md",
    "EOIP-engg-doc-pkg/03-functional-requirements.md",
    "EOIP-engg-doc-pkg/04-non-functional-requirements.md",
    "EOIP-engg-doc-pkg/gaps2-requirements.md",
    "EOIP-engg-doc-pkg/05-gap-analysis.md",
    "EOIP-engg-doc-pkg/08-security-architecture.md",
]:
    try:
        content = open(doc, encoding="utf-8").read()
        print(f"================ {doc} ================")
        for req in ["GAP-SEC-008", "GAP-SEC-009", "GAP-SEC-010", "GAP-SEC-011", "GAP-SEC-012"]:
            matches = [m.start() for m in re.finditer(re.escape(req), content)]
            if matches:
                print(f"--- {req} found {len(matches)} times ---")
                for pos in matches[:2]:
                    snippet = content[max(0, pos - 50):min(len(content), pos + 300)]
                    print(snippet.strip())
                    print("...")
    except Exception as e:
        print(f"Error reading {doc}: {e}")

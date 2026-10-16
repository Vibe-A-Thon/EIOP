"""Markdown link checker for non-historical documentation (CG-GAP-005, REL-13)."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Excluded historical directories and legacy doc packages (CG-GAP-005, REL-13)
EXCLUDED_DIRS = {
    "historical",
    "EOIP-engg-doc-pkg",
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "dist",
    "build",
    "audits/historical",
    ".vscode-test",
}

broken_links = []
total_links = 0
checked_files = 0

for md_file in REPO_ROOT.rglob("*.md"):
    rel_path = md_file.relative_to(REPO_ROOT).as_posix()
    if any(ex in rel_path for ex in EXCLUDED_DIRS):
        continue

    checked_files += 1
    content = md_file.read_text(encoding="utf-8", errors="ignore")

    # Match markdown links: [text](target)
    for m in re.finditer(r'\[([^\]]+)\]\(([^)#]+)(?:#[^)]*)?\)', content):
        target = m.group(2).strip()
        # Skip external links and email links
        if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
            continue

        total_links += 1
        # Resolve path relative to current md file
        try:
            resolved = (md_file.parent / target).resolve()
            if not resolved.exists():
                broken_links.append({
                    "file": rel_path,
                    "target": target,
                    "link_text": m.group(1),
                })
        except Exception as e:
            broken_links.append({
                "file": rel_path,
                "target": target,
                "error": str(e),
            })

print(f"Scanned {checked_files} markdown files.")
print(f"Total local links checked: {total_links}")
print(f"Broken links found: {len(broken_links)}")
for b in broken_links[:25]:
    print(f"  {b['file']} -> {b['target']} (text: {b.get('link_text', '')})")

import sys
sys.exit(1 if broken_links else 0)

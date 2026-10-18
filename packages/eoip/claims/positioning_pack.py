"""Ontology-as-Code positioning package generator (ONT-012, CRA-041.4)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

REQUIRED_CRA_022_CLAUSES: List[str] = [
    "CRA-022.1",
    "CRA-022.2",
    "CRA-022.3",
    "CRA-022.4",
    "CRA-022.5",
    "CRA-022.6",
    "CRA-022.7",
    "CRA-022.8",
    "CRA-022.9",
    "CRA-022.A",
]


class OntologyAsCodePackGenerator:
    """Generates the ONT-012 Ontology-as-Code positioning package only when CRA-022 is ACCEPTED."""

    @classmethod
    def check_prerequisites(
        cls,
        ledger_path: Optional[Path | str] = None,
        ledger_data: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        ledger_items: Dict[str, Dict[str, Any]] = {}
        if ledger_data:
            ledger_items = {it["id"]: it for it in ledger_data.get("items", [])}
        elif ledger_path and Path(ledger_path).exists():
            try:
                raw = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
                ledger_items = {it["id"]: it for it in raw.get("items", [])}
            except Exception as e:
                return [f"Failed to read ledger from {ledger_path}: {e}"]
        else:
            return ["Ledger not provided; cannot verify CRA-022 prerequisite acceptance."]

        missing_or_unaccepted: List[str] = []
        for req in REQUIRED_CRA_022_CLAUSES:
            item = ledger_items.get(req)
            if not item or item.get("state") != "ACCEPTED":
                st = item.get("state") if item else "MISSING"
                missing_or_unaccepted.append(f"{req} is {st} (must be ACCEPTED)")

        return missing_or_unaccepted

    @classmethod
    def generate_pack(
        cls,
        ledger_path: Optional[Path | str] = None,
        ledger_data: Optional[Dict[str, Any]] = None,
        date_str: str = "2026-10-18",
    ) -> Dict[str, Any]:
        unmet = cls.check_prerequisites(ledger_path, ledger_data)
        if unmet:
            return {
                "authorized": False,
                "reasons": unmet,
                "content": None,
            }

        content = f"""# Ontology-as-Code Positioning Package (ONT-012)
**Publication Date:** {date_str}
**Governance Reference:** CRA-041.4 (Prerequisites: CRA-022 ACCEPTED)

## 1. Factual Capabilities of EOIP GitOps Layer
EOIP provides a native GitOps lifecycle engine for ontologies (`packages/eoip/ontology/gitops.py`):
- **Branching & Pull Requests:** Complete isolation of ontology branches with git-backed change tracking.
- **Review Gates:** Automated policy checks, syntactic linting, and mandatory Lead Developer approvals.
- **Semantic Diff & Impact Analysis:** Graph-aware diff identifying breaking class/property removals and dependents.
- **Migration Script Generation:** Deterministic generation of migration instructions based on ontology diffs.
- **Rollback Receipts:** Cryptographically hashed rollback records ensuring safe reversibility.
- **Semver Computation:** Automated semantic version calculation (Major/Minor/Patch) derived from diff impact.
- **Release Packaging:** Signed, canonical release manifests bundling OWL, SHACL shapes, and documentation.

## 2. Competitive Comparison Table ({date_str})
| Capability | EOIP (KnowGridFlow) | TopBraid EDG | Protégé / WebProtégé | Chowlk / OnToology |
|---|---|---|---|---|
| **Version Control Semantics** | Native Git-backed PRs & branches | EDG working copies & governance | Simple history / change tracking | GitHub webhook automations |
| **Semantic Diff & Breaking Changes** | Native graph semantic diff | Structural comparison | Textual/RDF diff plugins | Syntax validation only |
| **Automated Migration Scripts** | Deterministic diff-to-migration | Manual scripts / rules | Manual | None |
| **Semantic Versioning Automation** | Diff-driven SemVer computation | Manual version tagging | Manual | GitHub tag triggers |
| **Offline Widoco-Class Docs** | Built-in offline generation | Integrated web viewer | Plugin required | Hosted HTML via OnToology |
| **Verification Gate Receipts** | Machine-verifiable receipts | Audit logging | None | GitHub Actions logs |
| **Primary Sources** | [EOIP GitOps](file:///packages/eoip/ontology/gitops.py) | [TopBraid EDG](https://www.topquadrant.com/products/topbraid-enterprise-data-governance/) | [WebProtégé](https://webprotege.stanford.edu/) | [OnToology](https://ontoology.linkeddata.es/) |

## 3. Current Limitations
- Pure CPU execution: Deep embedding calculations operate within CPU resource boundaries (ADR-H16).
- Git repository hosting must be configured with SSH or HTTPS token access.
- Merges are evaluated against linear branch histories; complex octopus merges require rebase.
"""
        return {
            "authorized": True,
            "reasons": [],
            "content": content,
            "prerequisites": REQUIRED_CRA_022_CLAUSES,
        }


def generate_ontology_as_code_pack(
    ledger_path: Optional[Path | str] = None,
    ledger_data: Optional[Dict[str, Any]] = None,
    date_str: str = "2026-10-18",
) -> Dict[str, Any]:
    return OntologyAsCodePackGenerator.generate_pack(ledger_path, ledger_data, date_str)

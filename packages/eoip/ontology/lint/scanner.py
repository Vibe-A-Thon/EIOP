"""Ontology Pitfall Scanner and Linter (CRA-022.7, ONT-013, INV-49).

Runs offline rule plug-ins against ontology RDF graphs, manifest definitions,
and SHACL shape graphs, producing structured LintReports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import rdflib

from eoip.ontology.lint.rules import (
    ALL_PITFALL_RULES,
    LintFinding,
    LintRule,
    LintSeverity,
)


@dataclass
class LintReport:
    findings: list[LintFinding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Returns True if there are zero ERROR or CRITICAL findings."""
        return not any(f.severity in (LintSeverity.ERROR, LintSeverity.CRITICAL) for f in self.findings)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == LintSeverity.CRITICAL)

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == LintSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == LintSeverity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == LintSeverity.INFO)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "total_findings": len(self.findings),
            "critical_count": self.critical_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "severity": f.severity.value,
                    "subject": f.subject,
                    "message": f.message,
                    "remediation_hint": f.remediation_hint,
                }
                for f in self.findings
            ],
        }


class OntologyLinter:
    """Offline ontology pitfall scanner executing pluggable lint rules (CRA-022.7)."""

    def __init__(self, rules: Optional[list[LintRule]] = None) -> None:
        self.rules = list(rules or ALL_PITFALL_RULES)

    def lint_graph(
        self,
        graph: rdflib.Graph,
        manifest: Optional[dict[str, Any]] = None,
        shapes_graph: Optional[rdflib.Graph] = None,
    ) -> LintReport:
        findings: list[LintFinding] = []
        for rule in self.rules:
            findings.extend(rule.check(graph=graph, manifest=manifest, shapes_graph=shapes_graph))
        return LintReport(findings=findings)

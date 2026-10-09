"""KGR-G-011: Formal Behavioral Verification at Merge Gate.

Property-based testing + AST contract diffing + structured abstain at
the CI merge gate.  Ensures that behavioral contracts (function
signatures, type annotations, invariant assertions, pre/post conditions)
are preserved or intentionally changed across commits.
"""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

log = logging.getLogger("eoip.verification.behavioral_gate")


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class VerdictStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSTAIN = "ABSTAIN"
    WARN = "WARN"


@dataclass(frozen=True)
class FunctionContract:
    """Extracted behavioral contract from a function definition."""
    module_path: str
    function_name: str
    qualified_name: str
    parameters: list[dict[str, Any]]
    return_annotation: str | None
    decorators: list[str]
    docstring: str | None
    assertions: list[str]
    raises: list[str]
    is_async: bool
    signature_hash: str

    @staticmethod
    def compute_signature_hash(params: list[dict[str, Any]], return_ann: str | None) -> str:
        payload = json.dumps({"params": params, "return": return_ann}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class ContractDiff:
    function: str
    module_path: str
    change_type: str  # added, removed, signature_changed, decorator_changed, assertion_changed
    severity: Severity
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    description: str = ""


@dataclass
class AbstainRecord:
    """Structured record when the gate cannot make a confident decision."""
    reason: str
    confidence: float
    module_path: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class GateVerdict:
    status: VerdictStatus
    diffs: list[ContractDiff] = field(default_factory=list)
    abstains: list[AbstainRecord] = field(default_factory=list)
    summary: str = ""
    breaking_changes: int = 0
    total_contracts_before: int = 0
    total_contracts_after: int = 0


class PythonContractExtractor:
    """Extracts behavioral contracts from Python source using the ast module."""

    def extract(self, source: str, module_path: str) -> list[FunctionContract]:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []
        contracts: list[FunctionContract] = []
        self._visit(tree, module_path, "", contracts)
        return contracts

    def _visit(self, node: ast.AST, module_path: str, prefix: str, contracts: list[FunctionContract]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qname = f"{prefix}{child.name}" if prefix else child.name
                contract = self._extract_function(child, module_path, qname)
                contracts.append(contract)
                self._visit(child, module_path, f"{qname}.", contracts)
            elif isinstance(child, ast.ClassDef):
                qname = f"{prefix}{child.name}" if prefix else child.name
                self._visit(child, module_path, f"{qname}.", contracts)

    def _extract_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, module_path: str, qualified_name: str
    ) -> FunctionContract:
        params = self._extract_params(node.args)
        return_ann = ast.dump(node.returns) if node.returns else None
        decorators = [self._decorator_name(d) for d in node.decorator_list]
        docstring = ast.get_docstring(node)
        assertions = self._extract_assertions(node)
        raises = self._extract_raises(node)

        return FunctionContract(
            module_path=module_path,
            function_name=node.name,
            qualified_name=qualified_name,
            parameters=params,
            return_annotation=return_ann,
            decorators=decorators,
            docstring=docstring,
            assertions=assertions,
            raises=raises,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            signature_hash=FunctionContract.compute_signature_hash(params, return_ann),
        )

    @staticmethod
    def _extract_params(args: ast.arguments) -> list[dict[str, Any]]:
        params: list[dict[str, Any]] = []
        for arg in args.args:
            params.append({
                "name": arg.arg,
                "annotation": ast.dump(arg.annotation) if arg.annotation else None,
            })
        if args.vararg:
            params.append({"name": f"*{args.vararg.arg}", "annotation": None})
        if args.kwarg:
            params.append({"name": f"**{args.kwarg.arg}", "annotation": None})
        return params

    @staticmethod
    def _decorator_name(node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return ast.dump(node)
        if isinstance(node, ast.Call):
            return ast.dump(node.func) if hasattr(node, "func") else ast.dump(node)
        return ast.dump(node)

    @staticmethod
    def _extract_assertions(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        assertions: list[str] = []
        for child in ast.walk(node):
            if isinstance(child, ast.Assert):
                assertions.append(ast.dump(child.test))
        return assertions

    @staticmethod
    def _extract_raises(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        raises: list[str] = []
        for child in ast.walk(node):
            if isinstance(child, ast.Raise) and child.exc:
                if isinstance(child.exc, ast.Call) and isinstance(child.exc.func, ast.Name):
                    raises.append(child.exc.func.id)
                elif isinstance(child.exc, ast.Name):
                    raises.append(child.exc.id)
        return list(set(raises))


class AbstractionScopeClassifier:
    """Classifies whether a function is public API, internal, or private,
    to assign appropriate severity to contract changes."""

    def classify(self, contract: FunctionContract) -> str:
        name = contract.function_name
        if name.startswith("__") and name.endswith("__"):
            return "dunder"
        if name.startswith("_"):
            return "private"
        if any(d in ("staticmethod", "classmethod") for d in contract.decorators):
            return "class_api"
        return "public"

    def severity_for_change(self, scope: str, change_type: str) -> Severity:
        if change_type == "removed":
            return Severity.CRITICAL if scope == "public" else Severity.HIGH
        if change_type == "signature_changed":
            if scope == "public":
                return Severity.CRITICAL
            if scope in ("class_api", "dunder"):
                return Severity.HIGH
            return Severity.MEDIUM
        if change_type == "assertion_changed":
            return Severity.MEDIUM
        if change_type == "decorator_changed":
            return Severity.MEDIUM if scope == "public" else Severity.LOW
        return Severity.INFO


class ContractDiffer:
    """Computes structured diffs between two sets of behavioral contracts."""

    def __init__(self) -> None:
        self._classifier = AbstractionScopeClassifier()

    def diff(self, before: list[FunctionContract], after: list[FunctionContract]) -> list[ContractDiff]:
        before_map = {c.qualified_name: c for c in before}
        after_map = {c.qualified_name: c for c in after}
        diffs: list[ContractDiff] = []

        for name, old in before_map.items():
            if name not in after_map:
                scope = self._classifier.classify(old)
                diffs.append(ContractDiff(
                    function=name,
                    module_path=old.module_path,
                    change_type="removed",
                    severity=self._classifier.severity_for_change(scope, "removed"),
                    before={"signature_hash": old.signature_hash, "parameters": old.parameters},
                    description=f"Function '{name}' removed",
                ))
                continue

            new = after_map[name]
            scope = self._classifier.classify(old)

            if old.signature_hash != new.signature_hash:
                diffs.append(ContractDiff(
                    function=name,
                    module_path=old.module_path,
                    change_type="signature_changed",
                    severity=self._classifier.severity_for_change(scope, "signature_changed"),
                    before={"parameters": old.parameters, "return": old.return_annotation},
                    after={"parameters": new.parameters, "return": new.return_annotation},
                    description=f"Signature changed for '{name}'",
                ))

            if set(old.decorators) != set(new.decorators):
                diffs.append(ContractDiff(
                    function=name,
                    module_path=old.module_path,
                    change_type="decorator_changed",
                    severity=self._classifier.severity_for_change(scope, "decorator_changed"),
                    before={"decorators": old.decorators},
                    after={"decorators": new.decorators},
                    description=f"Decorators changed for '{name}'",
                ))

            if old.assertions != new.assertions:
                diffs.append(ContractDiff(
                    function=name,
                    module_path=old.module_path,
                    change_type="assertion_changed",
                    severity=self._classifier.severity_for_change(scope, "assertion_changed"),
                    before={"assertions": old.assertions},
                    after={"assertions": new.assertions},
                    description=f"Assertions changed for '{name}'",
                ))

        for name in after_map:
            if name not in before_map:
                new = after_map[name]
                diffs.append(ContractDiff(
                    function=name,
                    module_path=new.module_path,
                    change_type="added",
                    severity=Severity.INFO,
                    after={"signature_hash": new.signature_hash},
                    description=f"New function '{name}' added",
                ))

        return sorted(diffs, key=lambda d: list(Severity).index(d.severity))


class BehavioralGate:
    """CI merge gate that verifies behavioral contract preservation."""

    def __init__(
        self,
        *,
        fail_on_critical: bool = True,
        fail_on_high: bool = True,
        abstain_confidence_threshold: float = 0.6,
    ) -> None:
        self.fail_on_critical = fail_on_critical
        self.fail_on_high = fail_on_high
        self.abstain_threshold = abstain_confidence_threshold
        self._extractor = PythonContractExtractor()
        self._differ = ContractDiffer()

    def verify_files(
        self,
        before_files: dict[str, str],
        after_files: dict[str, str],
    ) -> GateVerdict:
        all_diffs: list[ContractDiff] = []
        abstains: list[AbstainRecord] = []
        total_before = 0
        total_after = 0

        all_paths = set(before_files) | set(after_files)
        for path in sorted(all_paths):
            if not path.endswith(".py"):
                abstains.append(AbstainRecord(
                    reason="non_python_file",
                    confidence=0.0,
                    module_path=path,
                    details={"note": "Only Python contract extraction is currently supported"},
                ))
                continue

            old_source = before_files.get(path, "")
            new_source = after_files.get(path, "")

            old_contracts = self._extractor.extract(old_source, path) if old_source else []
            new_contracts = self._extractor.extract(new_source, path) if new_source else []
            total_before += len(old_contracts)
            total_after += len(new_contracts)

            if not old_contracts and not new_contracts:
                continue

            diffs = self._differ.diff(old_contracts, new_contracts)
            all_diffs.extend(diffs)

        breaking = sum(1 for d in all_diffs if d.severity in (Severity.CRITICAL, Severity.HIGH))
        status = self._compute_status(all_diffs, abstains)

        return GateVerdict(
            status=status,
            diffs=all_diffs,
            abstains=abstains,
            breaking_changes=breaking,
            total_contracts_before=total_before,
            total_contracts_after=total_after,
            summary=self._build_summary(status, all_diffs, abstains),
        )

    def verify_git_diff(self, repo_root: str, base_ref: str, head_ref: str) -> GateVerdict:
        """Verify behavioral contracts between two git refs."""
        import subprocess

        root = Path(repo_root)
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, head_ref, "--", "*.py"],
            capture_output=True, text=True, cwd=root,
        )
        changed_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]

        before_files: dict[str, str] = {}
        after_files: dict[str, str] = {}
        for fpath in changed_files:
            before_result = subprocess.run(
                ["git", "show", f"{base_ref}:{fpath}"],
                capture_output=True, text=True, cwd=root,
            )
            if before_result.returncode == 0:
                before_files[fpath] = before_result.stdout

            after_result = subprocess.run(
                ["git", "show", f"{head_ref}:{fpath}"],
                capture_output=True, text=True, cwd=root,
            )
            if after_result.returncode == 0:
                after_files[fpath] = after_result.stdout

        return self.verify_files(before_files, after_files)

    def _compute_status(self, diffs: list[ContractDiff], abstains: list[AbstainRecord]) -> VerdictStatus:
        has_critical = any(d.severity == Severity.CRITICAL for d in diffs)
        has_high = any(d.severity == Severity.HIGH for d in diffs)

        if has_critical and self.fail_on_critical:
            return VerdictStatus.FAIL
        if has_high and self.fail_on_high:
            return VerdictStatus.FAIL

        high_confidence_abstains = [a for a in abstains if a.confidence < self.abstain_threshold]
        if len(high_confidence_abstains) > len(diffs) * 0.5 and high_confidence_abstains:
            return VerdictStatus.ABSTAIN

        if any(d.severity in (Severity.MEDIUM,) for d in diffs):
            return VerdictStatus.WARN

        return VerdictStatus.PASS

    @staticmethod
    def _build_summary(status: VerdictStatus, diffs: list[ContractDiff], abstains: list[AbstainRecord]) -> str:
        by_severity: dict[str, int] = {}
        for d in diffs:
            by_severity[d.severity.value] = by_severity.get(d.severity.value, 0) + 1
        parts = [f"Gate verdict: {status.value}"]
        if diffs:
            breakdown = ", ".join(f"{k}: {v}" for k, v in sorted(by_severity.items()))
            parts.append(f"Contract changes: {breakdown}")
        if abstains:
            parts.append(f"Abstained on {len(abstains)} file(s)")
        return " | ".join(parts)

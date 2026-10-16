"""KGR-G-011: Formal Behavioral Verification at Merge Gate.

Property-based testing + AST contract diffing + structured abstain at
the CI merge gate.  Ensures that behavioral contracts (function
signatures, type annotations, invariant assertions, pre/post conditions)
are preserved or intentionally changed across commits.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, ClassVar

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


class RiskProfile(str, Enum):
    """Merge-gate blocking policy.

    R1 is the peer-review policy and blocks on any verified high or critical
    contract failure. R0 is the autonomous policy and only blocks critical path
    failures while still reporting lower-severity evidence.
    """

    R0 = "R0"
    R1 = "R1"


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
    change_type: str  # added, removed, signature_changed, decorator_changed, assertion_changed, behavior_changed
    severity: Severity
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    description: str = ""
    scope: str = "internal"


@dataclass
class AbstainRecord:
    """Structured record when the gate cannot make a confident decision."""
    reason: str
    confidence: float
    module_path: str
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def unverified_symbols(self) -> list[str]:
        value = self.details.get("unverified_symbols", [])
        return [str(item) for item in value] if isinstance(value, list) else []


@dataclass
class PropertyCheckResult:
    function: str
    module_path: str
    status: VerdictStatus
    samples_checked: int
    reason: str = ""
    before: Any = None
    after: Any = None


@dataclass
class GateVerdict:
    status: VerdictStatus
    diffs: list[ContractDiff] = field(default_factory=list)
    abstains: list[AbstainRecord] = field(default_factory=list)
    property_checks: list[PropertyCheckResult] = field(default_factory=list)
    summary: str = ""
    breaking_changes: int = 0
    total_contracts_before: int = 0
    total_contracts_after: int = 0
    verified_symbols: list[str] = field(default_factory=list)
    unverified_symbols: list[str] = field(default_factory=list)
    coverage_percent: float = 100.0


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

    def parse(self, source: str) -> ast.Module:
        return ast.parse(source)

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
                    scope=scope,
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
                    scope=scope,
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
                    scope=scope,
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
                    scope=scope,
                ))

        for name, new in after_map.items():
            if name not in before_map:
                diffs.append(ContractDiff(
                    function=name,
                    module_path=new.module_path,
                    change_type="added",
                    severity=Severity.INFO,
                    after={"signature_hash": new.signature_hash},
                    description=f"New function '{name}' added",
                    scope=self._classifier.classify(new),
                ))

        return sorted(diffs, key=lambda d: list(Severity).index(d.severity))


class PrimitivePropertyVerifier:
    """Conservative behavioral equivalence checker for safe pure functions.

    The verifier only compiles isolated function definitions whose bodies use a
    small expression subset. When a function falls outside that scope it returns
    a structured abstain instead of guessing.
    """

    _SUPPORTED_ANNOTATIONS: ClassVar[dict[str, list[Any]]] = {
        "int": [0, 1, -1, 7],
        "float": [0.0, 1.5, -2.0],
        "str": ["", "a", "abc"],
        "bool": [False, True],
        "list": [[], [1, 2]],
        "dict": [{}, {"a": 1}],
        "tuple": [(), (1, 2)],
        "set": [set(), {1, 2}],
    }
    _SAFE_CALLS: ClassVar[dict[str, Callable[..., Any]]] = {
        "abs": abs, "all": all, "any": any, "bool": bool, "dict": dict,
        "float": float, "int": int, "len": len, "list": list, "max": max,
        "min": min, "set": set, "str": str, "sum": sum, "tuple": tuple,
    }
    _SAFE_NODES: ClassVar[tuple[type[ast.AST], ...]] = (
        ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.Return, ast.Expr, ast.Load,
        ast.Constant, ast.Name, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.IfExp,
        ast.List, ast.Tuple, ast.Dict, ast.Set, ast.Subscript, ast.Slice, ast.Call,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub, ast.UAdd,
        ast.And, ast.Or, ast.Not, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )

    def check(
        self,
        before_source: str,
        after_source: str,
        before_contracts: list[FunctionContract],
        after_contracts: list[FunctionContract],
        module_path: str,
    ) -> tuple[list[PropertyCheckResult], list[AbstainRecord]]:
        before_tree = ast.parse(before_source)
        after_tree = ast.parse(after_source)
        before_funcs = self._function_nodes(before_tree)
        after_funcs = self._function_nodes(after_tree)
        after_map = {c.qualified_name: c for c in after_contracts}
        results: list[PropertyCheckResult] = []
        abstains: list[AbstainRecord] = []

        for contract in before_contracts:
            after_contract = after_map.get(contract.qualified_name)
            if not after_contract or contract.signature_hash != after_contract.signature_hash:
                continue
            old_node = before_funcs.get(contract.qualified_name)
            new_node = after_funcs.get(contract.qualified_name)
            if old_node is None or new_node is None:
                continue
            samples = self._samples_for(contract)
            if not samples:
                abstains.append(AbstainRecord(
                    reason="unsupported_property_signature",
                    confidence=0.5,
                    module_path=module_path,
                    details={
                        "unverified_symbols": [contract.qualified_name],
                        "coverage_percent": 0.0,
                        "parameter_annotations": [p.get("annotation") for p in contract.parameters],
                    },
                ))
                continue
            if not self._safe_function(old_node) or not self._safe_function(new_node):
                abstains.append(AbstainRecord(
                    reason="unsupported_function_body",
                    confidence=0.45,
                    module_path=module_path,
                    details={"unverified_symbols": [contract.qualified_name], "coverage_percent": 0.0},
                ))
                continue

            old_func = self._compile_function(old_node)
            new_func = self._compile_function(new_node)
            checked = 0
            for checked, args in enumerate(samples, start=1):
                old_result = self._call(old_func, args)
                new_result = self._call(new_func, args)
                if old_result != new_result:
                    results.append(PropertyCheckResult(
                        function=contract.qualified_name,
                        module_path=module_path,
                        status=VerdictStatus.FAIL,
                        samples_checked=checked,
                        reason="sample_behavior_mismatch",
                        before=old_result,
                        after=new_result,
                    ))
                    break
            else:
                results.append(PropertyCheckResult(
                    function=contract.qualified_name,
                    module_path=module_path,
                    status=VerdictStatus.PASS,
                    samples_checked=checked,
                ))

        return results, abstains

    @classmethod
    def _annotation_name(cls, annotation_dump: str | None) -> str | None:
        if not annotation_dump:
            return None
        if "Name(id='" in annotation_dump:
            return annotation_dump.split("Name(id='", 1)[1].split("'", 1)[0]
        if "Subscript(value=Name(id='" in annotation_dump:
            return annotation_dump.split("Subscript(value=Name(id='", 1)[1].split("'", 1)[0]
        return None

    def _samples_for(self, contract: FunctionContract) -> list[tuple[Any, ...]]:
        choices: list[list[Any]] = []
        for param in contract.parameters:
            name = str(param.get("name", ""))
            if name in {"self", "cls"} or name.startswith("*"):
                return []
            annotation = self._annotation_name(param.get("annotation"))
            values = self._SUPPORTED_ANNOTATIONS.get(annotation or "")
            if values is None:
                return []
            choices.append(values[:3])
        if not choices:
            return [()]
        samples: list[tuple[Any, ...]] = []
        for index in range(min(3, min(len(values) for values in choices))):
            samples.append(tuple(values[index] for values in choices))
        return samples

    def _function_nodes(self, tree: ast.Module) -> dict[str, ast.FunctionDef]:
        found: dict[str, ast.FunctionDef] = {}

        def visit(node: ast.AST, prefix: str = "") -> None:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    qname = f"{prefix}{child.name}" if prefix else child.name
                    found[qname] = child
                    visit(child, f"{qname}.")
                elif isinstance(child, ast.ClassDef):
                    qname = f"{prefix}{child.name}" if prefix else child.name
                    visit(child, f"{qname}.")

        visit(tree)
        return found

    def _safe_function(self, node: ast.FunctionDef) -> bool:
        if node.decorator_list:
            return False
        for child in ast.walk(node):
            if not isinstance(child, self._SAFE_NODES):
                return False
            if (
                isinstance(child, ast.Call)
                and (not isinstance(child.func, ast.Name) or child.func.id not in self._SAFE_CALLS)
            ):
                return False
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
                return False
        return True

    def _compile_function(self, node: ast.FunctionDef) -> Callable[..., Any]:
        clone = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
        code = compile(clone, "<behavioral-gate>", "exec")
        namespace: dict[str, Any] = {"__builtins__": self._SAFE_CALLS}
        exec(code, namespace, namespace)  # noqa: S102 - AST whitelist limits executable surface.
        return namespace[node.name]

    @staticmethod
    def _call(func: Callable[..., Any], args: tuple[Any, ...]) -> dict[str, Any]:
        try:
            return {"ok": True, "value": func(*args)}
        except Exception as exc:  # noqa: BLE001 - comparing thrown behavior is the point of the check.
            return {"ok": False, "exception": type(exc).__name__, "message": str(exc)}


class BehavioralGate:
    """CI merge gate that verifies behavioral contract preservation."""

    def __init__(
        self,
        *,
        risk_profile: RiskProfile | str = RiskProfile.R1,
        fail_on_critical: bool = True,
        fail_on_high: bool | None = None,
        abstain_confidence_threshold: float = 0.6,
        enable_property_checks: bool = True,
    ) -> None:
        self.risk_profile = RiskProfile(risk_profile)
        self.fail_on_critical = fail_on_critical
        self.fail_on_high = self.risk_profile == RiskProfile.R1 if fail_on_high is None else fail_on_high
        self.abstain_threshold = abstain_confidence_threshold
        self.enable_property_checks = enable_property_checks
        self._extractor = PythonContractExtractor()
        self._differ = ContractDiffer()
        self._property_verifier = PrimitivePropertyVerifier()

    def verify_files(
        self,
        before_files: dict[str, str],
        after_files: dict[str, str],
    ) -> GateVerdict:
        all_diffs: list[ContractDiff] = []
        abstains: list[AbstainRecord] = []
        property_checks: list[PropertyCheckResult] = []
        total_before = 0
        total_after = 0
        verified_symbols: set[str] = set()
        unverified_symbols: set[str] = set()

        all_paths = set(before_files) | set(after_files)
        for path in sorted(all_paths):
            if not path.endswith(".py"):
                abstains.append(AbstainRecord(
                    reason="non_python_file",
                    confidence=0.0,
                    module_path=path,
                    details={
                        "note": "Only Python contract extraction is currently supported",
                        "unverified_symbols": [path],
                        "coverage_percent": 0.0,
                    },
                ))
                unverified_symbols.add(path)
                continue

            old_source = before_files.get(path, "")
            new_source = after_files.get(path, "")
            for label, source in (("before", old_source), ("after", new_source)):
                if not source:
                    continue
                try:
                    self._extractor.parse(source)
                except SyntaxError as exc:
                    abstains.append(AbstainRecord(
                        reason="ast_parse_error",
                        confidence=0.0,
                        module_path=path,
                        details={
                            "side": label,
                            "message": str(exc),
                            "unverified_symbols": [path],
                            "coverage_percent": 0.0,
                        },
                    ))
                    unverified_symbols.add(path)

            old_contracts = self._extractor.extract(old_source, path) if old_source else []
            new_contracts = self._extractor.extract(new_source, path) if new_source else []
            total_before += len(old_contracts)
            total_after += len(new_contracts)
            verified_symbols.update(c.qualified_name for c in old_contracts)
            verified_symbols.update(c.qualified_name for c in new_contracts)

            if not old_contracts and not new_contracts:
                continue

            diffs = self._differ.diff(old_contracts, new_contracts)
            all_diffs.extend(diffs)
            if self.enable_property_checks and old_source and new_source:
                try:
                    checks, check_abstains = self._property_verifier.check(
                        old_source, new_source, old_contracts, new_contracts, path
                    )
                    property_checks.extend(checks)
                    abstains.extend(check_abstains)
                    for record in check_abstains:
                        unverified_symbols.update(record.unverified_symbols)
                    for check in checks:
                        if check.status == VerdictStatus.FAIL:
                            scope = AbstractionScopeClassifier().classify(
                                next(c for c in old_contracts if c.qualified_name == check.function)
                            )
                            all_diffs.append(ContractDiff(
                                function=check.function,
                                module_path=path,
                                change_type="behavior_changed",
                                severity=Severity.CRITICAL if scope == "public" else Severity.HIGH,
                                before=check.before,
                                after=check.after,
                                description="Property sample changed observable behavior",
                                scope=scope,
                            ))
                except SyntaxError:
                    pass

        breaking = sum(1 for d in all_diffs if d.severity in (Severity.CRITICAL, Severity.HIGH))
        status = self._compute_status(all_diffs, abstains)
        total_symbols = len(verified_symbols | unverified_symbols)
        coverage = 100.0 if total_symbols == 0 else round(
            (len(verified_symbols - unverified_symbols) / total_symbols) * 100.0, 2
        )

        return GateVerdict(
            status=status,
            diffs=all_diffs,
            abstains=abstains,
            property_checks=property_checks,
            breaking_changes=breaking,
            total_contracts_before=total_before,
            total_contracts_after=total_after,
            verified_symbols=sorted(verified_symbols - unverified_symbols),
            unverified_symbols=sorted(unverified_symbols),
            coverage_percent=coverage,
            summary=self._build_summary(status, all_diffs, abstains, coverage),
        )

    def verify_git_diff(
        self,
        repo_root: str,
        base_ref: str,
        head_ref: str,
        *,
        include_paths: Iterable[str] | None = None,
    ) -> GateVerdict:
        """Verify behavioral contracts between two git refs."""
        root = Path(repo_root)
        pathspec = ["--", "*.py"]
        prefixes = [p.replace("\\", "/").strip("/") for p in (include_paths or []) if p]
        result = subprocess.run(
            ["git", "diff", "--name-only", base_ref, head_ref, *pathspec],
            capture_output=True, text=True, cwd=root, check=False,
        )
        if result.returncode != 0:
            return GateVerdict(
                status=VerdictStatus.ABSTAIN,
                abstains=[AbstainRecord(
                    reason="git_diff_failed",
                    confidence=0.0,
                    module_path=str(root),
                    details={"message": result.stderr.strip(), "unverified_symbols": ["git_diff"]},
                )],
                summary="Gate verdict: ABSTAIN | git diff failed",
                coverage_percent=0.0,
                unverified_symbols=["git_diff"],
            )
        changed_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        if prefixes:
            changed_files = [f for f in changed_files if any(f.replace("\\", "/").startswith(p) for p in prefixes)]

        before_files: dict[str, str] = {}
        after_files: dict[str, str] = {}
        for fpath in changed_files:
            before_result = subprocess.run(
                ["git", "show", f"{base_ref}:{fpath}"],
                capture_output=True, text=True, cwd=root, check=False,
            )
            if before_result.returncode == 0:
                before_files[fpath] = before_result.stdout

            after_result = subprocess.run(
                ["git", "show", f"{head_ref}:{fpath}"],
                capture_output=True, text=True, cwd=root, check=False,
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
    def _build_summary(
        status: VerdictStatus,
        diffs: list[ContractDiff],
        abstains: list[AbstainRecord],
        coverage_percent: float,
    ) -> str:
        by_severity: dict[str, int] = {}
        for d in diffs:
            by_severity[d.severity.value] = by_severity.get(d.severity.value, 0) + 1
        parts = [f"Gate verdict: {status.value}"]
        if diffs:
            breakdown = ", ".join(f"{k}: {v}" for k, v in sorted(by_severity.items()))
            parts.append(f"Contract changes: {breakdown}")
        if abstains:
            parts.append(f"Abstained on {len(abstains)} file(s)")
        parts.append(f"Coverage: {coverage_percent:.2f}%")
        return " | ".join(parts)


_CHANGE_TYPE_MAP = {
    "removed": "BEHAVIOR_CHANGED",
    "signature_changed": "SIGNATURE_CHANGED",
    "decorator_changed": "BEHAVIOR_CHANGED",
    "assertion_changed": "PRECONDITION_ADDED",
    "behavior_changed": "BEHAVIOR_CHANGED",
    "added": "BEHAVIOR_CHANGED",
}

_SCOPE_MAP = {
    "public": "PUBLIC_API",
    "class_api": "PUBLIC_API",
    "dunder": "INTERNAL",
    "private": "INTERNAL",
}


def gate_decision(status: VerdictStatus) -> str:
    if status == VerdictStatus.FAIL:
        return "FAIL"
    if status == VerdictStatus.ABSTAIN:
        return "ABSTAIN"
    return "PASS"


def verdict_to_report(
    verdict: GateVerdict,
    *,
    commit_sha: str,
    base_sha: str | None = None,
    duration_ms: float | None = None,
) -> dict[str, Any]:
    """Convert an in-memory verdict to the stable CI JSON contract."""

    abstain_reason = None
    if verdict.abstains:
        reasons = sorted({record.reason for record in verdict.abstains})
        abstain_reason = ", ".join(reasons)

    return {
        "schema_version": "1.0",
        "verdict_id": hashlib.sha256(
            f"{commit_sha}:{base_sha}:{verdict.summary}".encode()
        ).hexdigest()[:16],
        "commit_sha": commit_sha,
        "base_sha": base_sha,
        "decision": gate_decision(verdict.status),
        "abstain_reason": abstain_reason,
        "contracts_analyzed": verdict.total_contracts_before + verdict.total_contracts_after,
        "breaking_changes": [
            {
                "function_path": f"{diff.module_path}:{diff.function}",
                "change_type": _CHANGE_TYPE_MAP.get(diff.change_type, "BEHAVIOR_CHANGED"),
                "severity": diff.severity.value,
                "before": diff.before or {},
                "after": diff.after or {},
                "scope_classification": _SCOPE_MAP.get(diff.scope, "INTERNAL"),
            }
            for diff in verdict.diffs
            if diff.severity in {Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW}
        ],
        "files_analyzed": sorted({
            *[diff.module_path for diff in verdict.diffs],
            *[record.module_path for record in verdict.abstains],
        }),
        "duration_ms": duration_ms if duration_ms is not None else 0.0,
        "created_at": datetime.now(UTC).isoformat(),
        "metadata": {
            "requirement_id": "KGR-G-011",
            "status": verdict.status.value,
            "summary": verdict.summary,
            "risk_model": "R1 blocks HIGH/CRITICAL; R0 blocks CRITICAL only",
            "coverage_percent": verdict.coverage_percent,
            "verified_symbols": verdict.verified_symbols,
            "unverified_symbols": verdict.unverified_symbols,
            "abstains": [
                {
                    "reason": record.reason,
                    "confidence": record.confidence,
                    "module_path": record.module_path,
                    "unverified_symbols": record.unverified_symbols,
                    "details": record.details,
                }
                for record in verdict.abstains
            ],
            "property_checks": [
                {
                    "function": check.function,
                    "module_path": check.module_path,
                    "status": check.status.value,
                    "samples_checked": check.samples_checked,
                    "reason": check.reason,
                }
                for check in verdict.property_checks
            ],
        },
    }


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def _resolve_ref(root: Path, ref: str | None, fallback: str) -> str:
    value = (ref or "").strip()
    if not value:
        value = fallback
    return _git(root, "rev-parse", value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run KGR-G-011 behavioral verification gate.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", default=os.environ.get("EOIP_BEHAVIORAL_GATE_BASE_REF"))
    parser.add_argument("--head-ref", default=os.environ.get("EOIP_BEHAVIORAL_GATE_HEAD_REF", "HEAD"))
    parser.add_argument("--risk-profile", choices=[p.value for p in RiskProfile], default=os.environ.get(
        "EOIP_BEHAVIORAL_GATE_RISK", RiskProfile.R1.value
    ))
    parser.add_argument("--output", type=Path, default=Path("test-results/behavioral-gate.json"))
    parser.add_argument(
        "--include-path",
        action="append",
        default=None,
        help="Repository path prefix to gate. Defaults to ingestion, query, ontology, and schema paths.",
    )
    parser.add_argument("--fail-on-abstain", action="store_true")
    args = parser.parse_args(argv)

    root = args.repo_root.resolve()
    include_paths = args.include_path or [
        "packages/eoip/ingestion",
        "packages/eoip/query",
        "packages/eoip/ontology",
        "packages/eoip/verification",
        "schemas",
    ]
    try:
        head_sha = _resolve_ref(root, args.head_ref, "HEAD")
        base_ref = args.base_ref or "HEAD~1"
        with contextlib.suppress(subprocess.CalledProcessError):
            base_ref = _git(root, "merge-base", args.head_ref or "HEAD", args.base_ref) if args.base_ref else base_ref
        base_sha = _resolve_ref(root, base_ref, "HEAD~1")
    except (OSError, subprocess.CalledProcessError) as exc:
        verdict = GateVerdict(
            status=VerdictStatus.ABSTAIN,
            abstains=[AbstainRecord(
                reason="git_ref_resolution_failed",
                confidence=0.0,
                module_path=str(root),
                details={"message": str(exc), "unverified_symbols": ["git_refs"]},
            )],
            summary="Gate verdict: ABSTAIN | git reference resolution failed",
            coverage_percent=0.0,
            unverified_symbols=["git_refs"],
        )
        head_sha = "0" * 40
        base_sha = None
        duration_ms = 0.0
    else:
        gate = BehavioralGate(risk_profile=args.risk_profile)
        started = time.perf_counter()
        verdict = gate.verify_git_diff(str(root), base_sha, head_sha, include_paths=include_paths)
        duration_ms = (time.perf_counter() - started) * 1000.0

    report = verdict_to_report(verdict, commit_sha=head_sha, base_sha=base_sha, duration_ms=duration_ms)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(verdict.summary)
    print(f"Behavioral gate report: {output}")
    if report["decision"] == "FAIL" or (args.fail_on_abstain and report["decision"] == "ABSTAIN"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

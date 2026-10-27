"""Build a conservative requirement-to-passing-test evidence receipt.

The verifier intentionally reports test evidence, not application completion.  It
binds literal ``pytest.mark.req`` annotations to the exact JUnit outcomes and
hashes the source files that supplied those annotations.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
try:
    import defusedxml.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from pathlib import Path

from eoip.jobs import write_json

EXPECTED_MVP_REQUIREMENTS = {f"MVP-FR-{index:03d}" for index in range(1, 29)}
MAX_INPUT_BYTES = 64 * 1024**2
MAX_SOURCE_BYTES = 2 * 1024**2


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _requirement_call(node: ast.AST) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    if not isinstance(func, ast.Attribute) or func.attr != "req":
        return None
    mark = func.value
    if not isinstance(mark, ast.Attribute) or mark.attr != "mark":
        return None
    if not isinstance(mark.value, ast.Name) or mark.value.id != "pytest":
        return None
    return node


def _literal_requirements(call: ast.Call) -> set[str]:
    if call.keywords or not call.args:
        raise ValueError("requirement annotations must contain literal string arguments")
    values: set[str] = set()
    for argument in call.args:
        if not isinstance(argument, ast.Constant) or not isinstance(argument.value, str):
            raise ValueError(  # noqa: TRY004 - malformed evidence is a validation failure
                "requirement annotations must contain literal string arguments"
            )
        value = argument.value.strip()
        if not value:
            raise ValueError("requirement annotations cannot contain empty identifiers")
        values.add(value)
    return values


def _markers(nodes: list[ast.expr]) -> set[str]:
    requirements: set[str] = set()
    for node in nodes:
        call = _requirement_call(node)
        if call is not None:
            requirements.update(_literal_requirements(call))
    return requirements


def _assigned_markers(body: list[ast.stmt]) -> set[str]:
    requirements: set[str] = set()
    for statement in body:
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
        if not any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in targets):
            continue
        value = statement.value
        values = value.elts if isinstance(value, (ast.List, ast.Tuple)) else [value]
        for item in values:
            call = _requirement_call(item)
            if call is not None:
                requirements.update(_literal_requirements(call))
    return requirements


def _parse_test_sources(project_root: Path) -> tuple[dict[tuple[str, str | None, str], set[str]], dict[str, str]]:
    definitions: dict[tuple[str, str | None, str], set[str]] = {}
    hashes: dict[str, str] = {}
    test_root = project_root / "tests"
    if not test_root.is_dir():
        raise ValueError("project has no test directory")
    total = 0
    for path in sorted(test_root.rglob("test_*.py")):
        if path.is_symlink() or not path.resolve().is_relative_to(test_root.resolve()):
            raise ValueError("evidence source must remain inside the test directory")
        size = path.stat().st_size
        total += size
        if size > MAX_SOURCE_BYTES or total > MAX_INPUT_BYTES or len(hashes) >= 10_000:
            raise ValueError("test evidence sources exceed resource bounds")
        relative = path.relative_to(project_root)
        raw = path.read_bytes()
        try:
            tree = ast.parse(raw.decode("utf-8"), filename=str(relative))
        except (SyntaxError, UnicodeDecodeError) as exc:
            raise ValueError(f"cannot parse test source {relative.as_posix()}: {exc}") from exc
        # Refuse dynamic req calls even when they are not attached to a test;
        # otherwise the evidence scan could silently overlook an annotation.
        for node in ast.walk(tree):
            call = _requirement_call(node)
            if call is not None:
                _literal_requirements(call)
        module = ".".join(relative.with_suffix("").parts)
        module_markers = _assigned_markers(tree.body)
        found_test = False
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                definitions[(module, None, node.name)] = module_markers | _markers(node.decorator_list)
                found_test = True
            elif isinstance(node, ast.ClassDef):
                class_markers = module_markers | _markers(node.decorator_list) | _assigned_markers(node.body)
                for method in node.body:
                    if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name.startswith("test_"):
                        definitions[(module, node.name, method.name)] = class_markers | _markers(method.decorator_list)
                        found_test = True
        if found_test:
            hashes[relative.as_posix()] = _sha256(raw)
    return definitions, hashes


def _load_matrix(path: Path) -> list[dict[str, object]]:
    if path.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError("requirement matrix exceeds resource bound")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"mvp_requirement", "title", "parent_requirements", "implementation_task"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("requirement matrix is missing required columns")
        rows: list[dict[str, object]] = []
        seen: set[str] = set()
        for raw in reader:
            requirement = (raw.get("mvp_requirement") or "").strip()
            if not requirement or requirement in seen:
                raise ValueError("requirement matrix contains an empty or duplicate requirement")
            seen.add(requirement)
            parents = [item.strip() for item in (raw.get("parent_requirements") or "").split(",") if item.strip()]
            if (
                not parents or not (raw.get("title") or "").strip()
                or not re.fullmatch(r"MVP-FR-\d{3}", requirement)
                or raw.get("implementation_task") != f"T{int(requirement[-3:]):02d}"
            ):
                raise ValueError("requirement matrix contains an invalid row")
            rows.append({
                "mvp_requirement": requirement,
                "title": (raw.get("title") or "").strip(),
                "parent_requirements": parents,
                "implementation_task": (raw.get("implementation_task") or "").strip(),
            })
    if seen != EXPECTED_MVP_REQUIREMENTS:
        raise ValueError("requirement matrix must contain exactly MVP-FR-001 through MVP-FR-028")
    return rows


def _case_outcome(case: ET.Element) -> str:
    if case.find("failure") is not None or case.find("error") is not None:
        return "FAIL"
    if case.find("skipped") is not None:
        return "SKIPPED"
    return "PASS"


def _load_junit(path: Path) -> list[dict[str, str]]:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("JUnit evidence exceeds resource bound")
    raw = path.read_bytes()
    if b"\x00" in raw:
        raise ValueError("JUnit evidence must use UTF-8 XML")
    lowered = raw.lower()
    if b"<!doctype" in lowered or b"<!entity" in lowered:
        raise ValueError("DTD and entity declarations are not permitted in JUnit evidence")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise ValueError(f"invalid JUnit XML: {exc}") from exc
    if root.tag not in {"testsuite", "testsuites"}:
        raise ValueError("unsupported JUnit root")
    cases = list(root.iter("testcase"))
    if not cases:
        raise ValueError("JUnit evidence contains no test cases")
    declared = 0
    suites = [root] if root.tag == "testsuite" else list(root.findall(".//testsuite"))
    for suite in suites:
        value = suite.get("tests")
        if value is None or not value.isdigit():
            raise ValueError("every JUnit test suite must declare its test count")
        declared += int(value)
    if declared != len(cases):
        raise ValueError("JUnit declared test count does not match contained test cases")
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for case in cases:
        classname = (case.get("classname") or "").strip()
        name = (case.get("name") or "").strip()
        identity = (classname, name)
        if not classname or not name or identity in seen:
            raise ValueError("JUnit evidence contains an empty or duplicate test case")
        seen.add(identity)
        result.append({"classname": classname, "name": name, "outcome": _case_outcome(case)})
    return result


def _definition_for_case(
    definitions: dict[tuple[str, str | None, str], set[str]], classname: str, name: str
) -> tuple[tuple[str, str | None, str] | None, set[str]]:
    function = re.sub(r"\[.*\]$", "", name)
    modules = sorted({key[0] for key in definitions if classname == key[0] or classname.startswith(key[0] + ".")}, key=len, reverse=True)
    for module in modules:
        suffix = classname[len(module):].lstrip(".")
        class_name = suffix.split(".")[-1] if suffix else None
        key = (module, class_name, function)
        if key in definitions:
            return key, definitions[key]
        key = (module, None, function)
        if key in definitions:
            return key, definitions[key]
    return None, set()


def _identifier_status(outcomes: list[str]) -> str:
    if not outcomes:
        return "MISSING"
    if "FAIL" in outcomes:
        return "FAIL"
    if all(outcome == "PASS" for outcome in outcomes):
        return "PASS"
    return "SKIPPED"


def verify_requirement_evidence(project_root: str | Path, matrix_path: str | Path, junit_path: str | Path) -> dict:
    """Return a deterministic, JSON-serializable evidence receipt."""
    root = Path(project_root).resolve()
    matrix = _load_matrix(Path(matrix_path))
    cases = _load_junit(Path(junit_path))
    definitions, all_source_hashes = _parse_test_sources(root)
    outcomes_by_requirement: dict[str, list[str]] = {}
    bound_sources: set[str] = set()
    case_receipts: list[dict[str, object]] = []
    for case in cases:
        definition, requirements = _definition_for_case(definitions, case["classname"], case["name"])
        if definition is not None:
            bound_sources.add(definition[0].replace(".", "/") + ".py")
        for requirement in requirements:
            outcomes_by_requirement.setdefault(requirement, []).append(case["outcome"])
        case_receipts.append({**case, "requirements": sorted(requirements)})

    requirement_receipts: list[dict[str, object]] = []
    for row in matrix:
        mvp = str(row["mvp_requirement"])
        parents = list(row["parent_requirements"])
        identifiers = [mvp, *parents]
        statuses = {identifier: _identifier_status(outcomes_by_requirement.get(identifier, [])) for identifier in identifiers}
        missing_parents = [identifier for identifier in parents if statuses[identifier] != "PASS"]
        direct_status = statuses[mvp]
        parent_statuses = [statuses[identifier] for identifier in parents]
        # A test may bind directly to the derived MVP requirement, or the
        # row may be closed by passing evidence for every listed parent.
        if direct_status == "FAIL" or "FAIL" in parent_statuses:
            evidence_status = "FAIL"
        elif direct_status == "PASS" or (parent_statuses and all(status == "PASS" for status in parent_statuses)):
            evidence_status = "PASSING_TESTS"
        elif "PASS" in parent_statuses:
            evidence_status = "PARTIAL"
        elif direct_status == "SKIPPED" or "SKIPPED" in parent_statuses:
            evidence_status = "SKIPPED"
        else:
            evidence_status = "MISSING"
        requirement_receipts.append({
            **row,
            "evidence_status": evidence_status,
            "identifier_statuses": statuses,
            "missing_parent_requirements": missing_parents,
        })

    passing = sum(item["evidence_status"] == "PASSING_TESTS" for item in requirement_receipts)
    failed = sum(case["outcome"] == "FAIL" for case in cases)
    receipt: dict[str, object] = {
        "status": "MAPPED_TEST_EVIDENCE" if passing == len(requirement_receipts) and not failed else "EVIDENCE_GAPS",
        "declared_requirements": len(requirement_receipts),
        "requirements_with_passing_evidence": passing,
        "requirements": requirement_receipts,
        "test_cases": case_receipts,
        "source_hashes": {path: all_source_hashes[path] for path in sorted(bound_sources) if path in all_source_hashes},
        "junit_sha256": _sha256(Path(junit_path).read_bytes()),
        "matrix_sha256": _sha256(Path(matrix_path).read_bytes()),
        "application_completion_percent": None,
        "source_revision_bound": False,
        "failed_or_error_cases": failed,
        "annotated_evidence_coverage_percent": round(100 * passing / len(requirement_receipts), 2),
        "limitations": [
            "Passing annotated tests do not certify every acceptance criterion or live integration",
            "Source hashes describe current annotations, not the revision that produced the JUnit receipt",
            "Untagged tests are not silently credited to requirements",
        ],
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt["receipt_sha256"] = _sha256(canonical)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("matrix", type=Path)
    parser.add_argument("junit", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = verify_requirement_evidence(arguments.project_root, arguments.matrix, arguments.junit)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        write_json(arguments.output, result)
    else:
        print(rendered, end="")
    if result["status"] == "EVIDENCE_GAPS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""Datalog front-end — facts + rules with bottom-up semi-naive evaluation.

Supported subset:
  * facts: ``edge("a", "b").`` (atoms with constant arguments)
  * rules: ``reachable(X, Y) :- edge(X, Z), reachable(Z, Y).``
  * queries posed by the caller over derived predicates; evaluation is
    bottom-up with an iteration cap (default 100) to guarantee termination.

Deterministic, stdlib-only. Variables are identifiers starting with an
uppercase letter or ``_``; all other atoms are constants.
"""

from __future__ import annotations

import re
from typing import Any

from eoip.qlang.plans import QLangParseError, QLangPlan

_FACT = re.compile(r"^([a-z][\w]*)\((.*)\)\s*\.?\s*$", re.DOTALL)
_RULE = re.compile(r"^([a-z][\w]*)\((.*)\)\s*:-\s*(.+?)\s*\.?\s*$", re.DOTALL)
_TERM_SPLIT = re.compile(r",(?=(?:[^\"']|[\"'][^\"']*[\"'])*$)")

DEFAULT_ITERATION_CAP = 100


def _terms(raw: str) -> list[str]:
    return [t.strip() for t in _TERM_SPLIT.split(raw) if t.strip()]


def _is_var(term: str) -> bool:
    return bool(re.fullmatch(r"[A-Z_][A-Za-z0-9_]*", term))


def _unquote(term: str) -> str:
    if (term.startswith('"') and term.endswith('"')) or (term.startswith("'") and term.endswith("'")):
        return term[1:-1]
    return term


def parse(program: str) -> QLangPlan:
    """Parse a Datalog program (facts + rules) into a QLangPlan."""
    text = re.sub(r"%[^\n]*", "", program)  # line comments
    facts: list[dict[str, Any]] = []
    rules: list[dict[str, Any]] = []
    for stmt in re.split(r"\.\s*", text):
        stmt = stmt.strip()
        if not stmt:
            continue
        rm = _RULE.match(stmt)
        if rm:
            head = {"pred": rm.group(1), "args": [_unquote(t) for t in _terms(rm.group(2))]}
            body = []
            for lit in re.split(r",\s*(?=[a-z][\w]*\()", rm.group(3)):
                lm = re.fullmatch(r"([a-z][\w]*)\((.*)\)", lit.strip(), re.DOTALL)
                if not lm:
                    raise QLangParseError(f"Invalid Datalog body literal: {lit!r}")
                body.append({"pred": lm.group(1), "args": [_unquote(t) for t in _terms(lm.group(2))]})
            rules.append({"head": head, "body": body})
            continue
        fm = _FACT.match(stmt)
        if fm:
            facts.append({"pred": fm.group(1), "args": [_unquote(t) for t in _terms(fm.group(2))]})
            continue
        raise QLangParseError(f"Invalid Datalog statement: {stmt!r}")
    return QLangPlan(
        language="datalog",
        intent="FILTER",
        operation="Datalog",
        source=program.strip(),
        extra={"facts": facts, "rules": rules},
    )


def _match_atom(atom: dict[str, Any], fact: tuple[str, ...], env: dict[str, str]) -> dict[str, str] | None:
    """Unify one body atom against a ground fact under an environment."""
    if len(atom["args"]) != len(fact):
        return None
    env = dict(env)
    for term, value in zip(atom["args"], fact):
        if _is_var(term):
            if term in env and env[term] != value:
                return None
            env[term] = value
        elif term != value:
            return None
    return env


def evaluate(plan: QLangPlan, iteration_cap: int = DEFAULT_ITERATION_CAP) -> dict[str, list[tuple[str, ...]]]:
    """Bottom-up semi-naive evaluation; returns derived facts per predicate."""
    derived: dict[str, set[tuple[str, ...]]] = {}
    for fact in plan.extra["facts"]:
        derived.setdefault(fact["pred"], set()).add(tuple(fact["args"]))

    rules = plan.extra["rules"]
    for _ in range(iteration_cap):
        changed = False
        for rule in rules:
            envs: list[dict[str, str]] = [{}]
            for atom in rule["body"]:
                next_envs: list[dict[str, str]] = []
                for env in envs:
                    for fact in derived.get(atom["pred"], ()):
                        matched = _match_atom(atom, fact, env)
                        if matched is not None:
                            next_envs.append(matched)
                envs = next_envs
                if not envs:
                    break
            for env in envs:
                grounded = tuple(env.get(arg, arg) for arg in rule["head"]["args"])
                if any(_is_var(a) for a in grounded):
                    continue
                bucket = derived.setdefault(rule["head"]["pred"], set())
                if grounded not in bucket:
                    bucket.add(grounded)
                    changed = True
        if not changed:
            break
    else:
        raise QLangParseError(
            f"Datalog evaluation exceeded iteration cap ({iteration_cap}); "
            "program may be non-terminating under the configured cap"
        )
    return {pred: sorted(facts) for pred, facts in derived.items()}


def parse_and_evaluate(program: str, iteration_cap: int = DEFAULT_ITERATION_CAP) -> dict[str, list[tuple[str, ...]]]:
    return evaluate(parse(program), iteration_cap=iteration_cap)

"""Minimal stdlib SemVer parsing, comparison and range matching (GAP-MKT-004).

Supports exact versions and comma-separated comparator ranges over
``==, !=, >, >=, <, <=, ^, ~``. Pre-release versions compare below their
release counterpart per SemVer 2.0 rules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import total_ordering

_VERSION_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z.-]+))?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)

_RANGE_PART_RE = re.compile(r"^\s*(>=|<=|==|!=|>|<|\^|~)?\s*([0-9][0-9A-Za-z.\-]*)\s*$")


class SemVerError(ValueError):
    """Raised when a version string or range cannot be parsed."""


@total_ordering
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...] = ()

    def _key(self):
        # Pre-release sorts before the plain release.
        return (self.major, self.minor, self.patch, self.prerelease == (), self.prerelease)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other: "Version") -> bool:
        base = (self.major, self.minor, self.patch)
        other_base = (other.major, other.minor, other.patch)
        if base != other_base:
            return base < other_base
        if self.prerelease == other.prerelease:
            return False
        if not self.prerelease:
            return False  # release > prerelease
        if not other.prerelease:
            return True
        return self.prerelease < other.prerelease

    def __str__(self) -> str:
        text = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            text += "-" + ".".join(self.prerelease)
        return text


def parse_version(text: str) -> Version:
    match = _VERSION_RE.match(text.strip())
    if not match:
        raise SemVerError(f"invalid SemVer: {text!r}")
    major, minor, patch, pre = match.groups()
    prerelease = tuple(pre.split(".")) if pre else ()
    return Version(int(major), int(minor), int(patch), prerelease)


class VersionRange:
    """Parsed SemVer range; ``matches`` tests a version string."""

    def __init__(self, expression: str) -> None:
        self.expression = expression.strip()
        if not self.expression:
            raise SemVerError("empty version range")
        self._checks: list[tuple[str, Version]] = []
        for part in self.expression.split(","):
            part = part.strip()
            if not part:
                raise SemVerError(f"empty range clause in {expression!r}")
            match = _RANGE_PART_RE.match(part)
            if not match:
                raise SemVerError(f"invalid range clause: {part!r}")
            op, ver_text = match.groups()
            op = op or "=="
            version = parse_version(ver_text)
            if op == "^":
                # Caret: compatible within same major (>=v, <next major).
                upper = Version(version.major + 1, 0, 0)
                self._checks.append((">=", version))
                self._checks.append(("<", upper))
            elif op == "~":
                upper = Version(version.major, version.minor + 1, 0)
                self._checks.append((">=", version))
                self._checks.append(("<", upper))
            else:
                self._checks.append((op, version))

    def matches(self, version_text: str) -> bool:
        version = parse_version(version_text)
        for op, target in self._checks:
            if op == "==" and not (version == target):
                return False
            if op == "!=" and not (version != target):
                return False
            if op == ">" and not (version > target):
                return False
            if op == ">=" and not (version >= target):
                return False
            if op == "<" and not (version < target):
                return False
            if op == "<=" and not (version <= target):
                return False
        return True

    def __str__(self) -> str:
        return self.expression


def parse_range(expression: str) -> VersionRange:
    return VersionRange(expression)


def matches_range(version: str, expression: str) -> bool:
    return VersionRange(expression).matches(version)

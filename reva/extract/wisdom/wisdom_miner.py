"""
Wisdom Graph Extractor & Architecture Miner (REVA-AB-015, T-ENH-006, T-ENH-007).
Mines Architecture Decision Records (ADRs), commit history semantics, architectural patterns,
and system invariants to construct the Wisdom Graph (Plane GW).
100% deterministic, Python-first, zero LLM dependency for extraction.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WisdomEntity:
    id: str
    kind: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WisdomEdge:
    source_id: str
    target_id: str
    relation: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WisdomGraph:
    repo_id: str
    root_path: str
    vertices: List[WisdomEntity] = field(default_factory=list)
    edges: List[WisdomEdge] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo_id": self.repo_id,
            "root_path": self.root_path,
            "metrics": self.metrics,
            "vertices_count": len(self.vertices),
            "edges_count": len(self.edges),
            "vertices": [
                {
                    "id": v.id,
                    "kind": v.kind,
                    "name": v.name,
                    "properties": v.properties,
                }
                for v in self.vertices
            ],
            "edges": [
                {
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation": e.relation,
                    "properties": e.properties,
                }
                for e in self.edges
            ],
        }


class WisdomGraphMiner:
    """
    Synthesizes Wisdom Graphs from repository records:
    1. ADR parser: discovers architectural decisions and trade-offs.
    2. Commit miner: analyzes conventional commit logs for breaking lessons.
    3. Structural heuristics: identifies architectural patterns and complexity hotspots.
    """

    ADR_DIRECTORIES = (
        "docs/adr", "doc/decisions", "rfc", "architecture/decisions",
        "docs/decisions", "docs/rfcs"
    )

    def __init__(self, max_commits_to_scan: int = 100) -> None:
        self.max_commits_to_scan = max_commits_to_scan

    def mine_wisdom_graph(self, root_path: str, repo_id: str, knowledge_graph_dict: Optional[Dict[str, Any]] = None) -> WisdomGraph:
        """
        Extracts wisdom vertices and edges for the given repository root.
        """
        abs_root = os.path.abspath(root_path)
        wg = WisdomGraph(repo_id=repo_id, root_path=abs_root)

        # 1. Mine Architecture Decision Records (ADRs)
        self._mine_adrs(abs_root, wg)

        # 2. Mine Git Commits & Evolution Lessons
        self._mine_commits(abs_root, wg)

        # 3. Mine Architectural Patterns & Heuristic Invariants
        self._mine_architectural_patterns(abs_root, wg, knowledge_graph_dict)

        # Calculate metrics
        wg.metrics = {
            "decisions_count": len([v for v in wg.vertices if v.kind == "wg_Decision"]),
            "lessons_count": len([v for v in wg.vertices if v.kind == "wg_Lesson"]),
            "patterns_count": len([v for v in wg.vertices if v.kind == "wg_Pattern"]),
            "risks_count": len([v for v in wg.vertices if v.kind == "wg_Risk"]),
            "total_vertices": len(wg.vertices),
            "total_edges": len(wg.edges),
        }

        return wg

    def _mine_adrs(self, abs_root: str, wg: WisdomGraph) -> None:
        """Discovers and parses Architecture Decision Records."""
        discovered_adr_files = []
        for adr_dir in self.ADR_DIRECTORIES:
            target = os.path.join(abs_root, adr_dir)
            if os.path.isdir(target):
                for f in os.listdir(target):
                    if f.endswith(".md"):
                        discovered_adr_files.append(os.path.join(target, f))

        # Also search for files matching *adr* or *decision* in root/docs
        docs_dir = os.path.join(abs_root, "docs")
        if os.path.isdir(docs_dir):
            for f in os.listdir(docs_dir):
                if ("decision" in f.lower() or "adr" in f.lower()) and f.endswith(".md"):
                    p = os.path.join(docs_dir, f)
                    if p not in discovered_adr_files:
                        discovered_adr_files.append(p)

        for adr_file in discovered_adr_files:
            rel_path = os.path.relpath(adr_file, abs_root).replace("\\", "/")
            try:
                with open(adr_file, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except Exception:
                continue

            # Extract title and sections
            title = os.path.basename(adr_file).replace(".md", "").replace("-", " ").title()
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break

            # Extract Status
            status = "Accepted"
            status_match = re.search(r"(?i)\bstatus:\s*([a-zA-Z]+)", content) or re.search(r"(?i)##\s*Status\s*\n+([a-zA-Z]+)", content)
            if status_match:
                status = status_match.group(1).capitalize()

            # Extract Context and Decision summaries
            context_match = re.search(r"(?i)##\s*Context([\s\S]*?)(?=##|\Z)", content)
            context = context_match.group(1).strip()[:300] if context_match else "Architectural context recorded in ADR."

            decision_match = re.search(r"(?i)##\s*Decision([\s\S]*?)(?=##|\Z)", content)
            decision = decision_match.group(1).strip()[:300] if decision_match else "Architectural decision recorded."

            adr_id = f"dec:{rel_path}"
            wg.vertices.append(WisdomEntity(
                id=adr_id,
                kind="wg_Decision",
                name=title,
                properties={
                    "path": rel_path,
                    "status": status,
                    "context": context,
                    "decision": decision,
                }
            ))

    def _mine_commits(self, abs_root: str, wg: WisdomGraph) -> None:
        """Mines commit log for conventional commit semantics, breaking changes, and lessons."""
        git_dir = os.path.join(abs_root, ".git")
        if not os.path.isdir(git_dir):
            return

        cmd = ["git", "log", f"-n{self.max_commits_to_scan}", "--pretty=format:%H|%an|%ad|%s", "--date=short"]
        try:
            result = subprocess.run(
                cmd,
                cwd=abs_root,
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
            if result.returncode != 0:
                return

            lines = result.stdout.splitlines()
            for line in lines:
                parts = line.split("|", 3)
                if len(parts) < 4:
                    continue
                commit_hash, author, date, subject = parts
                short_hash = commit_hash[:8]

                # Check for Conventional Commit pattern: <type>(<scope>): <subject>
                conv_match = re.match(r"^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.+)$", subject)
                is_breaking = False
                category = "other"
                scope = "core"
                desc = subject

                if conv_match:
                    category = conv_match.group(1)
                    scope = conv_match.group(2) or "core"
                    is_breaking = bool(conv_match.group(3)) or ("BREAKING" in subject.upper())
                    desc = conv_match.group(4)

                if is_breaking or category in ("fix", "refactor"):
                    lesson_id = f"les:{short_hash}"
                    wg.vertices.append(WisdomEntity(
                        id=lesson_id,
                        kind="wg_Lesson",
                        name=f"[{category.upper()}] {desc[:80]}",
                        properties={
                            "commit_sha": commit_hash,
                            "author": author,
                            "date": date,
                            "category": category,
                            "scope": scope,
                            "is_breaking": is_breaking,
                        }
                    ))
        except Exception:
            pass

    def _mine_architectural_patterns(
        self,
        abs_root: str,
        wg: WisdomGraph,
        kg_dict: Optional[Dict[str, Any]] = None
    ) -> None:
        """Identifies architectural patterns and risk hotspots."""
        # 1. Pattern: Zero-Data-Leak LLM Egress Fencing
        egress_gate_path = os.path.join(abs_root, "reva", "core", "egress_gate.py")
        if os.path.exists(egress_gate_path):
            pat_id = "pat:zero-data-leak-egress-fence"
            wg.vertices.append(WisdomEntity(
                id=pat_id,
                kind="wg_Pattern",
                name="Zero-Data-Leak LLM Egress Fencing",
                properties={
                    "type": "Security Boundary / Egress Control",
                    "description": "Deterministic Python sanitization, pseudonymization, and cryptographic prompt fencing.",
                    "reference": "reva/core/egress_gate.py",
                }
            ))

        # 2. Pattern: Multi-Tier Architecture
        has_api = os.path.isdir(os.path.join(abs_root, "reva", "api")) or os.path.isdir(os.path.join(abs_root, "backend", "api"))
        has_core = os.path.isdir(os.path.join(abs_root, "reva", "core")) or os.path.isdir(os.path.join(abs_root, "backend", "core"))
        if has_api and has_core:
            pat_id = "pat:layered-clean-architecture"
            wg.vertices.append(WisdomEntity(
                id=pat_id,
                kind="wg_Pattern",
                name="Layered Clean Architecture",
                properties={
                    "type": "Structural Separation of Concerns",
                    "description": "Distinct API routing, Domain Core, and Data Persistence layers.",
                }
            ))

        # 3. Analyze KG vertices for Risk Hotspots (High cyclomatic complexity)
        if kg_dict and "vertices" in kg_dict:
            for v in kg_dict["vertices"]:
                if v.get("kind") == "kg_Function":
                    complexity = v.get("properties", {}).get("complexity", 1)
                    if complexity >= 15:
                        risk_id = f"rsk:complexity:{v['id']}"
                        wg.vertices.append(WisdomEntity(
                            id=risk_id,
                            kind="wg_Risk",
                            name=f"High Cyclomatic Complexity ({complexity}): {v['name']}",
                            properties={
                                "risk_type": "Maintainability & Defect Risk",
                                "target_function": v["id"],
                                "complexity": complexity,
                            }
                        ))
                        wg.edges.append(WisdomEdge(
                            source_id=risk_id,
                            target_id=v["id"],
                            relation="RISK_IN_COMPONENT",
                            properties={"metric": "cyclomatic_complexity", "value": complexity}
                        ))

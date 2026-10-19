"""
End-to-End Repository Ingestion, Knowledge Graph & Wisdom Graph Pipeline (REVA-AB-014/015, T-ENH-004/006/007).
Connects:
1. GitRepositoryCloner (Remote GitHub/GitLab URL or local path)
2. CodeASTAnalyzer (Deterministic Pure-Python Knowledge Graph)
3. WisdomGraphMiner (Deterministic Pure-Python Wisdom Graph)
4. EgressSecurityGate (Zero-Data-Leak LLM Fencing & Pseudonymization)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from reva.core.digest import sha256_canonical
from reva.core.egress_gate import EgressSecurityGate
from reva.core.ids import warrant_id
from reva.extract.repo.cloner import ClonedRepository, GitRepositoryCloner
from reva.extract.repo.code_analyzer import CodeASTAnalyzer, KnowledgeGraph
from reva.extract.wisdom.wisdom_miner import WisdomGraph, WisdomGraphMiner


@dataclass
class RepoGraphResult:
    """Consolidated result containing Knowledge Graph and Wisdom Graph."""
    repo_id: str
    source_url: str
    commit_sha: str
    branch: str
    knowledge_graph: Dict[str, Any]
    wisdom_graph: Dict[str, Any]
    warrant: Dict[str, Any]
    egress_audit: Optional[Dict[str, Any]] = None
    output_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo_id": self.repo_id,
            "source_url": self.source_url,
            "commit_sha": self.commit_sha,
            "branch": self.branch,
            "warrant_id": self.warrant.get("id"),
            "knowledge_graph": self.knowledge_graph,
            "wisdom_graph": self.wisdom_graph,
            "warrant": self.warrant,
            "egress_audit": self.egress_audit,
        }


class RepoToGraphOrchestrator:
    """
    Orchestrates the entire repository analysis pipeline:
    - Pure-Python first extraction
    - Zero data leak to LLM
    - Knowledge and Wisdom graph construction
    """

    def __init__(
        self,
        base_scratch_dir: Optional[str] = None,
        max_binary_bytes: int = 50 * 1024 * 1024,
        allow_external_llm: bool = False,
    ) -> None:
        self.cloner = GitRepositoryCloner(base_scratch_dir=base_scratch_dir)
        self.ast_analyzer = CodeASTAnalyzer()
        self.wisdom_miner = WisdomGraphMiner()
        self.egress_gate = EgressSecurityGate(allow_raw_code=allow_external_llm)

    def process_repository(
        self,
        repo_source: str,
        branch: Optional[str] = None,
        depth: int = 1,
        output_dir: Optional[str] = None,
        synthesize_with_llm: bool = False,
        llm_callback: Optional[Any] = None,
    ) -> RepoGraphResult:
        """
        Executes end-to-end repository ingestion and graph construction.
        """
        cloned_repo: Optional[ClonedRepository] = None
        try:
            # 1. Ingest / Clone repository
            cloned_repo = self.cloner.ingest(repo_source=repo_source, branch=branch, depth=depth)
            repo_root = cloned_repo.clone_path

            # 2. Pure-Python Knowledge Graph extraction (Modules, Classes, Functions, Endpoints, Calls)
            kg: KnowledgeGraph = self.ast_analyzer.analyze_repository(
                root_path=repo_root,
                repo_id=cloned_repo.repo_id,
            )
            kg_dict = kg.to_dict()

            # 3. Pure-Python Wisdom Graph extraction (ADRs, Commits, Patterns, Risks)
            wg: WisdomGraph = self.wisdom_miner.mine_wisdom_graph(
                root_path=repo_root,
                repo_id=cloned_repo.repo_id,
                knowledge_graph_dict=kg_dict,
            )
            wg_dict = wg.to_dict()

            # 4. Zero-Data-Leak LLM Synthesis (if requested)
            egress_audit: Optional[Dict[str, Any]] = None
            if synthesize_with_llm:
                # Prepare payload with abstracted summary, NOT raw proprietary code
                abstract_context = {
                    "repo_id": cloned_repo.repo_id,
                    "metrics": {
                        "kg_metrics": kg_dict.get("metrics"),
                        "wg_metrics": wg_dict.get("metrics"),
                    },
                    "patterns": [v["name"] for v in wg_dict.get("vertices", []) if v["kind"] == "wg_Pattern"],
                    "risks": [v["name"] for v in wg_dict.get("vertices", []) if v["kind"] == "wg_Risk"],
                }

                raw_payload = {
                    "prompt": f"Synthesize architectural findings for repository {cloned_repo.repo_id}",
                    "context": json.dumps(abstract_context),
                }

                # Run through Egress Security Gate (redacts secrets, pseudonymizes, applies fences)
                sanitized_payload = self.egress_gate.inspect_and_sanitize(raw_payload)
                egress_audit = sanitized_payload.get("_egress_gate")

                if llm_callback:
                    # Invoke user-supplied or local LLM safely
                    llm_response = llm_callback(sanitized_payload)
                    wg_dict["architectural_narrative"] = llm_response
                else:
                    wg_dict["architectural_narrative"] = (
                        f"Deterministic architectural summary: Repository {cloned_repo.repo_id} contains "
                        f"{kg_dict['metrics'].get('total_python_files', 0)} Python modules, "
                        f"{kg_dict['metrics'].get('total_classes', 0)} classes, and "
                        f"{kg_dict['metrics'].get('total_functions', 0)} functions. Identified "
                        f"{wg_dict['metrics'].get('patterns_count', 0)} architectural patterns and "
                        f"{wg_dict['metrics'].get('risks_count', 0)} risk hotspots."
                    )

            # 5. Generate Merkle Warrant for the Graph
            warrant_body = {
                "subject": f"repo:{cloned_repo.repo_id}",
                "commit_sha": cloned_repo.commit_sha,
                "kg_vertices": len(kg_dict["vertices"]),
                "wg_vertices": len(wg_dict["vertices"]),
                "issued_at": datetime.now(timezone.utc).isoformat(),
                "verdict": "VERIFIED",
            }
            wr_id = warrant_id(warrant_body)
            warrant = {
                "id": wr_id,
                "body": warrant_body,
                "producer": "reva_RepoToGraphOrchestrator_v1",
            }

            result = RepoGraphResult(
                repo_id=cloned_repo.repo_id,
                source_url=cloned_repo.remote_url,
                commit_sha=cloned_repo.commit_sha,
                branch=cloned_repo.branch,
                knowledge_graph=kg_dict,
                wisdom_graph=wg_dict,
                warrant=warrant,
                egress_audit=egress_audit,
            )

            # 6. Save output if requested
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                out_file = os.path.join(output_dir, f"{cloned_repo.repo_id}_graphs.json")
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(result.to_dict(), f, indent=2)
                result.output_path = out_file

            return result

        finally:
            # 7. Cleanup ephemeral directories safely
            if cloned_repo:
                self.cloner.cleanup(cloned_repo)

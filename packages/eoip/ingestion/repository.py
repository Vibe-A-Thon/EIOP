"""Ingest a local, tracked Git repository and optional GitLab JSON metadata."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from eoip.codegraph.parser import PARSER_VERSION, CodeParser
from eoip.contracts.source_event import SourceEvent, utc_now_iso
from eoip.identity.resolver import merge_source_aliases, person_identity
from eoip.ingestion.jira import FileEventCapture
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION

ISSUE_KEY = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


class RepositoryIngestionService:
    def __init__(self, store, capture: FileEventCapture):
        self.store, self.capture = store, capture

    def ingest(self, root: Path, repo_id="demo", metadata=None):
        root = root.resolve()
        run_id = str(uuid4())
        shared = {
            "source_system": "git",
            "repo_id": repo_id,
            "ingestion_run_id": run_id,
            "ontology_version": ONTOLOGY_VERSION,
            "schema_version": SCHEMA_VERSION,
        }

        def git(*args):
            return subprocess.check_output(["git", "-C", str(root), *args], timeout=30).decode("utf-8")

        sha = git("rev-parse", "HEAD").strip()
        branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
        message = git("log", "-1", "--format=%B").strip()
        event = self._capture(repo_id, sha, {"commit_sha": sha, "branch": branch, "message": message})
        edge_props = {
            "source_system": "git",
            "source_ref": f"git://{repo_id}/commit/{sha}",
            "evidence_key": event.event_id,
            "ingestion_run_id": run_id,
        }
        repo = self.store.upsert_vertex(
            "Repository", {**shared, "canonical_id": f"urn:eoip:code:repo:{repo_id}", "name": repo_id}
        )
        branch_node = self.store.upsert_vertex(
            "Branch",
            {**shared, "canonical_id": f"urn:eoip:code:branch:{repo_id}:{branch}", "branch_name": branch},
        )
        self._evidence(repo, event, edge_props["source_ref"])
        self._evidence(branch_node, event, edge_props["source_ref"])
        author_name = git("log", "-1", "--format=%aN").strip()
        author_email = git("log", "-1", "--format=%aE").strip()
        commit = self.store.upsert_vertex(
            "Commit",
            {
                **shared,
                "canonical_id": f"urn:eoip:code:commit:{repo_id}:{sha}",
                "commit_sha": sha,
                "message": message,
                "author_name": author_name,
                "author_email": author_email,
            },
        )
        self._evidence(commit, event, edge_props["source_ref"])
        ingested_nodes = [repo, branch_node, commit]
        self.store.upsert_edge("HAS_BRANCH", repo["vid"], branch_node["vid"], edge_props)
        self.store.upsert_edge("HAS_COMMIT", branch_node["vid"], commit["vid"], edge_props)
        self._issue_links(commit, message, "IMPLEMENTS", edge_props)

        if author_email:
            person_cid, source_alias = person_identity(author_email, "git", author_email)
            existing_person = self.store.get_vertex_by_canonical_id(person_cid)
            person = self.store.upsert_vertex(
                "Person",
                {
                    **shared,
                    "canonical_id": person_cid,
                    "display_name": author_name or author_email,
                    "email": author_email,
                    "source_aliases": (
                        merge_source_aliases(
                            existing_person["properties"].get("source_aliases"), source_alias
                        )
                        if existing_person
                        else source_alias
                    ),
                },
            )
            ingested_nodes.append(person)
            self.store.upsert_edge("AUTHORED_BY", commit["vid"], person["vid"], edge_props)
        changed = set(git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines())
        files = symbols = 0
        errors = []
        parser = CodeParser()
        file_nodes = {}
        file_imports = {}
        for name in git("ls-files", "-z").split("\0"):
            if not name:
                continue
            path = (root / name).resolve()
            if (
                not path.is_relative_to(root)
                or path.is_symlink()
                or not path.is_file()
                or path.stat().st_size > 2_000_000
            ):
                continue
            if path.suffix not in {".py", ".ts", ".tsx", ".md"}:
                continue
            source = path.read_text(encoding="utf-8")
            file_event = self._capture(repo_id, name, {"path": name, "commit_sha": sha, "content": source})
            props = {
                **edge_props,
                "evidence_key": file_event.event_id,
                "source_ref": f"git://{repo_id}/{sha}/{name}",
            }
            common = {**shared, "path": name, "content_hash": hashlib.sha256(source.encode()).hexdigest()}
            if path.suffix == ".md":
                doc = self.store.upsert_vertex(
                    "Document",
                    {
                        **common,
                        "canonical_id": f"urn:eoip:knowledge:document:{repo_id}:{name}",
                        "name": name,
                        "doc_format": "markdown",
                    },
                )
                ingested_nodes.append(doc)
                self._evidence(doc, file_event, props["source_ref"])
                self._issue_links(doc, source, "DOCUMENTS", props)
                continue
            parsed = parser.parse(repo_id, name, source)
            if parsed.parse_errors:
                errors.extend(parsed.parse_errors)
                continue
            file = self.store.upsert_vertex(
                "File",
                {
                    **common,
                    "canonical_id": f"urn:eoip:code:file:{repo_id}:{name}",
                    "language": parsed.language,
                },
            )
            ingested_nodes.append(file)
            self._evidence(file, file_event, props["source_ref"])
            self.store.upsert_edge("CONTAINS", repo["vid"], file["vid"], props)
            if name in changed:
                self.store.upsert_edge("MODIFIES", commit["vid"], file["vid"], props)
            file_nodes[name] = file
            file_imports[name] = parsed.imports
            files += 1
            symbol_nodes = {}
            for symbol in parsed.symbols:
                fields = asdict(symbol)
                fields["symbol_kind"] = fields.pop("kind")
                node = self.store.upsert_vertex(
                    "CodeSymbol",
                    {**common, **fields, "language": parsed.language, "parser_version": PARSER_VERSION},
                )
                symbol_nodes[symbol.canonical_id] = node
                ingested_nodes.append(node)
                self.store.upsert_edge("DECLARES", file["vid"], node["vid"], props)
                self._evidence(node, file_event, props["source_ref"])
                symbols += 1
            for call in parsed.calls:
                if call.caller_id in symbol_nodes and call.target_id in symbol_nodes:
                    self.store.upsert_edge(
                        "CALLS",
                        symbol_nodes[call.caller_id]["vid"],
                        symbol_nodes[call.target_id]["vid"],
                        props,
                    )
            for imported in parsed.imports:
                dependency = self.store.upsert_vertex(
                    "Dependency",
                    {
                        **shared,
                        "canonical_id": f"urn:eoip:code:dependency:{repo_id}:{imported}",
                        "name": imported,
                        "language": parsed.language,
                        "resolved": False,
                    },
                )
                ingested_nodes.append(dependency)
                self.store.upsert_edge("IMPORTS", file["vid"], dependency["vid"], props)
        path_to_file = {}
        for fname, fnode in file_nodes.items():
            mod = fname.replace("\\", "/")
            if mod.endswith(".py"):
                mod_key = mod[:-3].replace("/", ".")
                path_to_file[mod_key] = fnode
                if mod_key.endswith(".__init__"):
                    path_to_file[mod_key[: -len(".__init__")]] = fnode
        for fname, imports in file_imports.items():
            src = file_nodes[fname]
            for imp in imports:
                target = path_to_file.get(imp)
                if target and target["vid"] != src["vid"]:
                    self.store.upsert_edge("DEPENDS_ON", src["vid"], target["vid"], edge_props)
        if metadata:
            ingested_nodes.extend(self._gitlab(repo, commit, metadata, shared, sha))
        result = {
            "run_id": run_id,
            "run_status": "PARTIAL" if errors else "SUCCEEDED",
            "files": files,
            "symbols": symbols,
            "errors": errors,
            "commit_sha": sha,
        }
        run = self.store.upsert_vertex(
            "IngestionRun",
            {
                "canonical_id": f"urn:eoip:meta:ingestion-run:{run_id}",
                "run_kind": "GIT",
                "run_status": result["run_status"],
                "counts": json.dumps(result),
                "finished_at": utc_now_iso(),
            },
        )
        for node in {item["canonical_id"]: item for item in ingested_nodes}.values():
            self.store.upsert_edge(
                "INGESTED_IN",
                node["vid"],
                run["vid"],
                {
                    "fact_key": f"repository-run:{run_id}:{node['canonical_id']}",
                    "source_system": "git",
                    "ingestion_run_id": run_id,
                },
            )
        return result

    def _capture(self, repo_id, source_id, payload):
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        event = SourceEvent(
            event_id=hashlib.sha256(f"git:{repo_id}:{source_id}:{digest}".encode()).hexdigest(),
            source_system="git",
            source_record_id=f"{repo_id}:{source_id}",
            source_version=digest,
            payload_hash=digest,
            payload=payload,
        )
        self.capture.capture(event)
        return event

    def _evidence(self, node, event, ref):
        evidence = self.store.upsert_vertex(
            "Evidence",
            {
                "canonical_id": f"urn:eoip:evidence:source-event:git:{event.event_id}",
                "source_system": "git",
                "source_ref": ref,
                "method": "SOURCE_EVENT",
                "evidence_key": event.event_id,
                "content_hash": event.payload_hash,
                "captured_at": event.captured_at,
            },
        )
        self.store.upsert_edge(
            "EVIDENCED_BY",
            node["vid"],
            evidence["vid"],
            {"evidence_key": event.event_id, "source_ref": ref, "source_system": "git"},
        )

    def _issue_links(self, node, text, relation, props):
        for key in sorted(set(ISSUE_KEY.findall(text))):
            issue = self.store.get_vertex_by_canonical_id(f"urn:eoip:work:item:jira:{key}")
            if issue:
                self.store.upsert_edge(relation, node["vid"], issue["vid"], props)

    def _gitlab(self, repo, commit, metadata, shared, sha):
        event = self._capture(shared["repo_id"], "gitlab-metadata", metadata)
        ingested_nodes = []
        props = {
            "evidence_key": event.event_id,
            "source_ref": f"fixture://gitlab/{event.event_id}",
            "source_system": "gitlab",
        }
        for mr in metadata.get("merge_requests", []):
            node = self.store.upsert_vertex(
                "MergeRequest",
                {
                    **shared,
                    "canonical_id": f"urn:eoip:cicd:mr:{shared['repo_id']}:{mr['iid']}",
                    "mr_iid": mr["iid"],
                    "mr_title": mr["title"],
                    "source_branch": mr.get("source_branch"),
                    "target_branch": mr.get("target_branch"),
                },
            )
            ingested_nodes.append(node)
            self._evidence(node, event, props["source_ref"])
            self.store.upsert_edge("HAS_MERGE_REQUEST", repo["vid"], node["vid"], props)
            self._issue_links(node, mr["title"], "IMPLEMENTS", props)
            if mr.get("merge_commit_sha") in {sha, "HEAD"}:
                self.store.upsert_edge("REFERENCES", node["vid"], commit["vid"], props)
        for pipeline in metadata.get("pipelines", []):
            node = self.store.upsert_vertex(
                "PipelineRun",
                {
                    **shared,
                    "canonical_id": f"urn:eoip:cicd:pipeline:{shared['repo_id']}:{pipeline['id']}",
                    "name": pipeline.get("name", "pipeline"),
                    "pipeline_status": pipeline.get("status"),
                    "commit_sha": sha if pipeline.get("sha") == "HEAD" else pipeline.get("sha"),
                },
            )
            ingested_nodes.append(node)
            self._evidence(node, event, props["source_ref"])
            if pipeline.get("sha") in {sha, "HEAD"}:
                self.store.upsert_edge("PRODUCED_BY", node["vid"], commit["vid"], props)
        return ingested_nodes

#!/usr/bin/env python3
"""Claim / release / list task locks in audit-memory.json (multi-agent handoff, prompt §7).

  claim_tasks.py claim   --memory M --agent-id A --scope EPIC-X | RT-ID ... [--hours 8] [--tasks audit_tasks.json]
  claim_tasks.py release --memory M --agent-id A --lock-id L [--action completed|released|handoff] [--notes ...]
  claim_tasks.py list    --memory M [--expired]
  claim_tasks.py expire  --memory M --agent-id AUDIT-LEAD   (Audit Lead only: drop locks past expires_at)

Rules: a lock lasts at most 24 h; scopes are task ids, requirement ids or epic ids (expanded to
their task ids via --tasks); a claim fails if any task in scope is held by another agent's
unexpired lock. Writes atomically (tmp + rename) under an exclusive fcntl lock file.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent


def now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def expand(scope, tasks_path):
    q = json.loads(Path(tasks_path).read_text()) if tasks_path and Path(tasks_path).is_file() else {"tasks": []}
    by_epic, by_req, ids = {}, {}, set()
    for t in q.get("tasks", []):
        ids.add(t["task_id"])
        by_epic.setdefault(t.get("epic_id"), []).append(t["task_id"])
        if t.get("kind") == "requirement":
            by_req[t["requirement_id"]] = t["task_id"]
    out = []
    for s in scope:
        if s in by_epic:
            out += by_epic[s]
        elif s in ids:
            out.append(s)
        elif s in by_req:
            out.append(by_req[s])
        else:
            sys.exit(f"unknown scope item: {s}")
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["claim", "release", "list", "expire"])
    ap.add_argument("--memory", type=Path, default=KIT / "audit-output" / "audit-memory.json")
    ap.add_argument("--tasks", type=Path, default=KIT / "audit-output" / "audit_tasks.json")
    ap.add_argument("--agent-id")
    ap.add_argument("--role", default="remediation")
    ap.add_argument("--scope", nargs="*", default=[])
    ap.add_argument("--hours", type=float, default=8)
    ap.add_argument("--lock-id")
    ap.add_argument("--action", default="completed", choices=["completed", "released", "handoff"])
    ap.add_argument("--notes", default="")
    ap.add_argument("--expired", action="store_true")
    a = ap.parse_args()
    lockfile = open(str(a.memory) + ".lock", "w")
    fcntl.flock(lockfile, fcntl.LOCK_EX)
    mem = json.loads(a.memory.read_text())
    locks = mem.setdefault("open_locks", [])
    agents = mem.setdefault("agents", [])
    t = now()
    if a.cmd == "list":
        for l in locks:
            exp = parse(l["expires_at"]) < t
            if not a.expired or exp:
                print(f"{l['lock_id']}  {l['agent_id']:20}  {'EXPIRED ' if exp else ''}until {l['expires_at']}  {len(l['scope'])} tasks  {l.get('notes','')}")
        return
    if not a.agent_id:
        sys.exit("--agent-id required")
    if a.cmd == "claim":
        if a.hours > 24:
            sys.exit("locks are limited to 24 h")
        scope = expand(a.scope, a.tasks)
        held = {s: l["agent_id"] for l in locks if parse(l["expires_at"]) >= t and l["agent_id"] != a.agent_id for s in l["scope"]}
        clash = [s for s in scope if s in held]
        if clash:
            sys.exit(f"refused: {len(clash)} task(s) held by others, e.g. {clash[0]} by {held[clash[0]]}")
        lock = {"lock_id": "LOCK-" + uuid.uuid4().hex[:12], "agent_id": a.agent_id, "scope": scope,
                "claimed_at": iso(t), "expires_at": iso(t + timedelta(hours=a.hours)), "notes": a.notes or " ".join(a.scope)[:200]}
        locks.append(lock)
        agents.append({"agent_id": a.agent_id, "role": a.role, "timestamp": iso(t), "action": "claimed", "scope": scope[:500],
                       "notes": f"{lock['lock_id']} {a.notes}".strip()})
        msg = f"claimed {len(scope)} task(s) as {lock['lock_id']} until {lock['expires_at']}"
    elif a.cmd == "release":
        mine = [l for l in locks if l["lock_id"] == a.lock_id and l["agent_id"] == a.agent_id]
        if not mine:
            sys.exit("no such lock for this agent")
        locks.remove(mine[0])
        agents.append({"agent_id": a.agent_id, "role": a.role, "timestamp": iso(t), "action": a.action,
                       "scope": mine[0]["scope"][:500], "notes": f"{a.lock_id} {a.notes}".strip()})
        msg = f"released {a.lock_id} ({a.action})"
    else:
        exp = [l for l in locks if parse(l["expires_at"]) < t]
        for l in exp:
            locks.remove(l)
            agents.append({"agent_id": a.agent_id, "role": "audit_lead", "timestamp": iso(t), "action": "released",
                           "scope": l["scope"][:500], "notes": f"expired {l['lock_id']} of {l['agent_id']}"})
        msg = f"expired {len(exp)} lock(s)"
    tmp = a.memory.with_suffix(".tmp")
    tmp.write_text(json.dumps(mem, indent=2, ensure_ascii=False))
    os.replace(tmp, a.memory)
    print(msg)


if __name__ == "__main__":
    main()

/* EOIP programme rules engine — one implementation shared by EOIP-programme-tracker.html and
 * tools/tracker/verify_programme_ledger.mjs. It decides which canonical state an item may hold given
 * the evidence recorded for it. A state is never accepted because of a file path, a symbol name,
 * a test-file name or a commit hash alone.
 * Works in browsers (global ProgrammeRules) and in Node (module.exports).
 */
(function (root) {
  "use strict";
  const STATES = ["OPEN", "IN_PROGRESS", "CODE_COMPLETE", "EVIDENCED", "VERIFIED", "BLOCKED", "FAILED", "FAILED_ACCEPTED", "STALE", "DEFERRED"];
  const RANK = { OPEN: 0, IN_PROGRESS: 1, CODE_COMPLETE: 2, EVIDENCED: 3, VERIFIED: 4 };
  const DSTATES = ["OPEN", "BLOCKED", "DECIDED"];
  const HEX40 = /^[0-9a-f]{40}$/i, HEX64 = /^[0-9a-f]{64}$/i, DATE = /^\d{4}-\d{2}-\d{2}$/;
  const DECISION_REF = /^(CONFLICT-IP-\d{3}|DR-IP-\d{3}|CONFLICT-WG-\d{3}|DR-WG-\d{3}|Q-\d{3}|ADR-[A-Za-z0-9._-]+|ASPEII-DEC-\d{3}|CIP-DEC-\d{3}|LEGAL-[A-Za-z0-9._-]+|OWNER-[A-Za-z0-9._-]+)$/;
  const ASPEII_PROFILES = ["local-sqlite-windows", "local-sqlite-linux", "postgres-saas-linux", "mcp-stdio", "mcp-http", "local-model", "hosted-model", "sandbox-write-connector", "production-config"];
  const ASPEII_LEVELS = ["L2", "L3", "L4", "L5", "L6"];

  /* Native labels: every programme keeps its own vocabulary (XP-01). */
  const NATIVE = {
    ASPEII: { OPEN: "OPEN", IN_PROGRESS: "IN_PROGRESS", CODE_COMPLETE: "IN_PROGRESS", EVIDENCED: "IN_PROGRESS", VERIFIED: "VERIFIED", BLOCKED: "BLOCKED", FAILED: "FAILED", STALE: "STALE", DEFERRED: "DEFERRED" },
    CIP: { OPEN: "NOT_RUN", IN_PROGRESS: "NOT_RUN", CODE_COMPLETE: "NOT_RUN", EVIDENCED: "NOT_RUN", VERIFIED: "PASS_WITH_EVIDENCE", BLOCKED: "BLOCKED", FAILED: "FAIL", STALE: "NOT_RUN" },
    IP: { OPEN: "NOT-STARTED", IN_PROGRESS: "IN-PROGRESS", CODE_COMPLETE: "CODE-COMPLETE", EVIDENCED: "EVIDENCED", VERIFIED: "VERIFIED", BLOCKED: "BLOCKED", FAILED: "IN-PROGRESS", STALE: "IN-PROGRESS" },
    WG: { OPEN: "NOT-STARTED", IN_PROGRESS: "IN-PROGRESS", CODE_COMPLETE: "CODE-COMPLETE", EVIDENCED: "EVIDENCED", VERIFIED: "VERIFIED", BLOCKED: "BLOCKED", FAILED: "IN-PROGRESS", STALE: "IN-PROGRESS" },
    GN: { OPEN: "NOT FILED", IN_PROGRESS: "NOT FILED", CODE_COMPLETE: "NOT FILED", EVIDENCED: "DRAFT LEDGER", VERIFIED: "COMPLETE", BLOCKED: "BLOCKED", FAILED: "FAILED", FAILED_ACCEPTED: "FAILED (accepted outcome)", STALE: "NOT FILED" },
  };

  function build(D) {
    const ITEMS = D.items, BY = Object.fromEntries(ITEMS.map(i => [i.id, i]));
    const XP = Object.fromEntries((D.xp || []).map(x => [x.id, x]));
    const children = {}; ITEMS.forEach(i => { if (i.parent) (children[i.parent] = children[i.parent] || []).push(i.id); });
    const byGroup = {}; ITEMS.forEach(i => { (byGroup[i.prog + "|" + i.group] = byGroup[i.prog + "|" + i.group] || []).push(i.id); });
    const blockersOf = {}; (D.xp || []).forEach(x => x.blocks.forEach(b => (blockersOf[b] = blockersOf[b] || []).push(x.id)));
    const ipWp = Object.fromEntries((D.meta.ip_wps || []).map(w => [w.id, w]));
    const gnOrder = ["0a", "0b", "1", "2", "3", "4", "5", "6", "7"];

    function allowedStates(it) {
      if (it.kind === "conflict") return DSTATES;
      return STATES.filter(s => (s !== "DEFERRED" || it.prog === "ASPEII") && (s !== "FAILED_ACCEPTED" || (it.prog === "GN" && (it.flags || []).includes("failure_ok"))));
    }
    function native(it, s) { return it.kind === "conflict" ? s : ((NATIVE[it.prog] || {})[s] || s); }
    const safePath = p => !!p && !/^([A-Za-z]:|\/|\\)/.test(p) && !/(^|\/)\.\.(\/|$)/.test(p) && !p.includes("\\");

    /* --- dependency helpers (ctx.state(id) returns canonical state; ctx.dec(id) decision state) --- */
    function openBlockers(id, ctx) {
      const out = [];
      (blockersOf[id] || []).forEach(x => { if (ctx.dec(x) !== "DECIDED") out.push(x); });
      (ctx.log() || []).forEach(e => { if (e.blocks && (e.affects || []).includes(id) && e.state !== "DECIDED") out.push(e.id); });
      return out;
    }
    function startPrereqs(it) {
      // Gates that must be VERIFIED before work on this item may begin (IP plan §0.2; GN §3 and plan §1).
      if (it.prog === "IP") {
        const wp = it.kind === "gate" ? it.group : (it.kind === "req" ? it.group : null);
        if (wp && ipWp[wp]) return ipWp[wp].deps.map(d => `IP-${d}.GATE`);
        if (it.kind === "scenario") return it.deps || [];
        return [];
      }
      if (it.prog === "WG") {
        if (it.kind === "gate") return it.deps || [];
        if (it.kind === "req") { const g = BY[`${it.group}.GATE`]; return g ? (g.deps || []) : []; }
        if (it.kind === "scenario") return it.deps || [];
        return [];
      }
      if (it.prog === "GN" && it.group && it.group.startsWith("GN-PH")) {
        const p = it.group.slice(5);
        if (p === "X") return ["GN-PH0b.GATE"];
        const k = gnOrder.indexOf(p);
        return k > 0 ? [`GN-PH${gnOrder[k - 1]}.GATE`] : [];
      }
      return [];
    }
    function closePrereqs(it) {
      // Gates that must be VERIFIED before this item may be VERIFIED.
      if (it.kind === "gate") return it.deps || [];
      if (it.prog === "CIP") {
        const ph = it.kind === "clause" ? it.group : (it.kind === "task" ? it.group : null);
        if (ph) { const n = +ph.slice(5); return n > 0 ? [`CIP-P${n - 1}.GATE`] : []; }
      }
      return [];
    }

    /* --- evidence path rules per programme --- */
    function evidencePathError(it, p) {
      if (!safePath(p)) return "Evidence path must be a repository-relative path (no absolute path, no '..', forward slashes).";
      if (it.prog === "ASPEII" && !/^\.audit-scratch\/aspeii\/[A-Za-z0-9._-]+\/.+/.test(p)) return "ASPEII evidence must be inside a run bundle: .audit-scratch/aspeii/<run-id>/… (plan §7).";
      if (it.prog === "IP") {
        if (it.kind === "req" && !new RegExp(`^evidence/${it.id}/?$`).test(p)) return `IP evidence pack must be evidence/${it.id}/ (requirements §17.1).`;
        if (it.kind === "scenario" && !/^evidence\/E2E-IP-001\/?$/.test(p)) return "End-to-end evidence must be evidence/E2E-IP-001/ (plan WP-25 task 7).";
        if (it.kind === "gate" && !new RegExp(`^docs/ip/verification/${it.group}-report\\.md$`).test(p)) return `Gate evidence is the verification report docs/ip/verification/${it.group}-report.md (plan §5.7).`;
      }
      if (it.prog === "WG") {
        if (it.kind === "req" && !new RegExp(`^evidence/${it.id}/?$`).test(p)) return `Wisdom evidence pack must be evidence/${it.id}/ (requirements §28.1).`;
        if (it.kind === "scenario" && !/^evidence\/E2E-WG-001\/?$/.test(p)) return "End-to-end evidence must be evidence/E2E-WG-001/ (plan WG-WP-17 task 7).";
        if (it.kind === "gate" && !new RegExp(`^docs/wisdom/verification/${it.group}-report\\.md$`).test(p)) return `Gate evidence is the verification report docs/wisdom/verification/${it.group}-report.md (plan §6.7).`;
      }
      if (it.prog === "GN" && (it.kind === "check" || it.kind === "ledger")) {
        const led = it.kind === "ledger" ? it.id : it.parent;
        if (p !== `EOIP-engg-doc-pkg/evidence/${led}.md`) return `Graph Neurons evidence is the ledger file EOIP-engg-doc-pkg/evidence/${led}.md (plan §0.3).`;
      }
      return null;
    }
    function verificationRefError(it, v) {
      if (!(v || "").trim()) return "Verification reference required (independent verifier output or report).";
      if (it.prog === "ASPEII" && !/^\.audit-scratch\/aspeii\/[A-Za-z0-9._-]+\/verifier-result\.json$/.test(v)) return "ASPEII verification reference must be the independent verifier output .audit-scratch/aspeii/<run-id>/verifier-result.json (plan §7, §8).";
      if (it.prog === "IP" && it.kind === "req" && !new RegExp(`^docs/ip/verification/${it.group}-report\\.md$`).test(v)) return `IP verification reference must be docs/ip/verification/${it.group}-report.md for this requirement's work package (plan §5.7).`;
      if (it.prog === "IP" && it.kind !== "req" && !/^docs\/ip\/verification\/.+\.md$/.test(v)) return "IP verification reference must be a report under docs/ip/verification/.";
      if (it.prog === "WG" && it.kind === "req" && !new RegExp(`^docs/wisdom/verification/${it.group}-report\\.md$`).test(v)) return `Wisdom verification reference must be docs/wisdom/verification/${it.group}-report.md for this requirement's work package (plan §6.7).`;
      if (it.prog === "WG" && it.kind !== "req" && !/^docs\/wisdom\/verification\/.+\.md$/.test(v)) return "Wisdom verification reference must be a report under docs/wisdom/verification/.";
      return null;
    }

    /* --- the transition check --- */
    function errors(id, target, r, ctx) {
      const it = BY[id]; const e = []; r = r || {};
      const need = (c, m) => { if (!c) e.push(m); };
      if (!it) return ["Unknown item id."];
      if (!allowedStates(it).includes(target)) return [`${target} is not a valid state for ${it.prog} ${it.kind} items.`];
      if (target === "OPEN") return e;
      if (target === "BLOCKED") { need((r.blocked_by || "").trim(), "Name the blocking dependency, missing input or decision id."); return e; }
      if (target === "DEFERRED") { need((r.owner || "").trim(), "Owner required."); need((r.notes || "").trim(), "Reason required; DEFERRED never counts as complete."); return e; }
      if (target === "STALE") { need((r.notes || "").trim(), "Describe what changed (source, artifact, requirement text or environment)."); return e; }
      if (target === "FAILED") {
        need((r.notes || "").trim(), "Failure note with the observed numbers or error required.");
        need((r.fail_ref || r.evidence_path || "").trim(), "Reference to the failing run (receipt, log, ledger) required.");
        return e;
      }
      if (target === "FAILED_ACCEPTED") {
        need(it.kind === "ledger" && (it.flags || []).includes("failure_ok"), "Only bake-off or research requirements whose text accepts a 'not justified' outcome may close as an accepted failure (XP-18).");
        need(r.evidence_path === `EOIP-engg-doc-pkg/evidence/${id}.md`, `Ledger path EOIP-engg-doc-pkg/evidence/${id}.md required.`);
        need((r.notes || "").trim(), "Paste the real measured numbers against the named thresholds.");
        need((r.recommendation || "").trim(), "One-paragraph recommendation required (plan §0.4).");
        need((r.reviewer || "").trim() && (r.reviewer || "").trim().toLowerCase() !== (r.producer || "").trim().toLowerCase(), "Independent reviewer (different from the producer) required.");
        need(DATE.test(r.review_date || ""), "Review date (YYYY-MM-DD) required.");
        const kids = children[id] || []; const bad = kids.filter(k => !["VERIFIED", "FAILED"].includes(ctx.state(k)));
        need(bad.length === 0, `${bad.length} check(s) are neither VERIFIED nor FAILED: ${bad.slice(0, 6).join(", ")}${bad.length > 6 ? "…" : ""}`);
        return e;
      }
      const rank = RANK[target];
      if (rank >= 1) {
        need((r.owner || "").trim(), "Owner required.");
        need((r.work_ref || "").trim(), "Work reference required (task card, branch, ledger draft or DR id).");
        const pre = startPrereqs(it).filter(g => ctx.state(g) !== "VERIFIED");
        need(pre.length === 0, `Prerequisite gate(s) not VERIFIED: ${pre.join(", ")} — work may not start (IP plan §0.2 / GN phase gates).`);
      }
      if (rank >= 2) {
        need(HEX40.test(r.commit || ""), "40-hex source commit SHA required.");
        if (target === "CODE_COMPLETE") need((r.change_ref || "").trim(), "Changed paths required (recorded for navigation; never proof).");
      }
      if (rank >= 3) {
        const pe = evidencePathError(it, r.evidence_path || ""); if (pe) e.push(pe);
        need(HEX64.test(r.evidence_sha256 || ""), "64-hex SHA-256 of the evidence file or directory manifest required.");
        need((r.producer || "").trim(), "Producer identity (agent session / CI job) required.");
        need((r.command || "").trim(), "Exact command(s) executed required.");
        need(String(r.exit_code ?? "") === "0", "Exit code 0 required for passing evidence; record failures as FAILED.");
        need((r.env || "").trim(), "Environment / profile description required.");
        need(r.text_sha256 === it.text_sha256, "Evidence must be bound to the current requirement text (text_sha256 differs: requirement changed → STALE).");
        need(r.attest_run === true, "Confirm the evidence was produced by executing against the real boundary, with captured output and no skipped, xfailed or errored required case.");
        if (it.prog === "ASPEII") {
          need(ASPEII_PROFILES.includes(r.profile), "ASPEII release profile required (plan §11).");
          need(ASPEII_LEVELS.includes(r.level), "Completion level L2–L6 required; L0 (design/source references) and L1 (static checks) are not evidence (plan §1.1).");
          need((r.case_ids || "").trim(), "Executed case ID(s) from cases.jsonl required.");
        }
        if (it.prog === "CIP") {
          need((r.profile || "").trim(), "Store/worker profile required (cip-evidence-1.0 environment).");
          if (["clause", "scenario", "negative"].includes(it.kind)) need((r.junit_ids || "").trim(), "Exact JUnit case id(s) that executed required (marker without a JUnit case is rejected, plan §8 item 12).");
          if (it.kind === "clause") need((r.scenario_ref || "").trim(), "Executable scenario and observable required (CIP-RQ-030).");
        }
        if (it.prog === "IP" || it.prog === "WG") {
          if (["req", "scenario"].includes(it.kind)) need(r.pack_ok === true, "Confirm the Evidence Pack holds README.md, run.sh, transcript/, state/, negative/, metrics/, logs/, tests.md (+ ui/ for screens, benchmarks/ for numeric acceptance).");
          if (it.kind === "req") need(r.killswitch_ok === true, "Kill-switch control: tests pass with the flag on and the behaviour tests fail with it off (§17.3).");
          if (["req", "gate"].includes(it.kind)) need(r.stubscan_ok === true, "make ip-stub-scan clean or every flagged line justified in the verification report (plan §5.6).");
        }
        if (it.prog === "GN") {
          if (it.kind === "ledger") need((r.seed || "").trim(), "Seed and capture_environment() reference required in every ledger (GN-012).");
          if (it.kind === "check") {
            need((r.measured || "").trim(), "Measured / observed result pasted from real output required.");
            if (it.level === "V4") { need(r.baselines_ok === true, "All five baselines printed beside the model number (§2.2)."); need((r.snapshot_id || "").trim(), "Snapshot id (ref-2026-10 or content hash) required."); }
            if (it.level === "V5") { need(r.probes_ok === true, "All four anti-stub probes P1–P4 reported with measurements (§2.1)."); need((r.snapshot_id || "").trim(), "Snapshot id required."); }
          }
        }
      }
      if (rank >= 4) {
        need((r.reviewer || "").trim(), "Independent reviewer required.");
        need((r.reviewer || "").trim().toLowerCase() !== (r.producer || "").trim().toLowerCase(), "Reviewer must differ from the producer.");
        need(DATE.test(r.review_date || ""), "Review date (YYYY-MM-DD) required.");
        const ve = verificationRefError(it, r.verification_ref); if (ve) e.push(ve);
        need(r.attest_replay === true, "Confirm the reviewer re-ran the evidence from a fresh deployment and the observed values, decisions, counts and error codes match.");
        const pre = closePrereqs(it).filter(g => ctx.state(g) !== "VERIFIED");
        need(pre.length === 0, `Gate(s) that must close first are not VERIFIED: ${pre.join(", ")}.`);
        const ob = openBlockers(id, ctx); need(ob.length === 0, `Open decision(s) block verification: ${ob.join(", ")}.`);
        aggregateErrors(it, ctx).forEach(x => e.push(x));
      }
      return e;
    }

    function notVerified(ids, ctx, okStates) { okStates = okStates || ["VERIFIED"]; return ids.filter(x => !okStates.includes(ctx.state(x))); }
    function msgList(bad, what) { return `${bad.length} ${what} not VERIFIED (${bad.slice(0, 5).join(", ")}${bad.length > 5 ? "…" : ""}).`; }
    const of = (pred) => ITEMS.filter(pred).map(i => i.id);
    function aggregateErrors(it, ctx) {
      const out = []; const chk = (ids, what, ok) => { const b = notVerified(ids, ctx, ok); if (b.length) out.push(msgList(b, what)); };
      if (it.kind === "acceptance") chk(children[it.parent] ? children[it.parent].filter(x => BY[x].kind === "clause") : [], `clause(s) of ${it.parent}`);
      if (it.kind === "ledger") chk(children[it.id] || [], `check(s) of ${it.id}`);
      if (it.kind === "gate") {
        if (it.prog === "IP") {
          chk(it.members || [], `requirement(s) of ${it.group}`);
          if (it.group === "WP-25") { chk(of(i => i.id.startsWith("E2E-IP-001.")), "end-to-end step(s)"); chk(of(i => i.id.startsWith("IP-DOD-")), "definition-of-done item(s)"); }
        }
        if (it.prog === "CIP") {
          chk(it.members || [], `task(s) of ${it.group}`);
          if (it.group === "CIP-P7") { chk(of(i => i.prog === "CIP" && i.kind === "clause"), "acceptance clause(s)"); chk(of(i => i.prog === "CIP" && ["scenario", "negative"].includes(i.kind)), "scenario / negative item(s)"); }
        }
        if (it.prog === "GN") {
          chk(it.members || [], `gate check(s) of ${it.group}`);
          chk((it.ledgers || []).filter(l => !(BY[l].flags || []).includes("failure_ok")), `ledger(s) of ${it.group}`);
          chk((it.ledgers || []).filter(l => (BY[l].flags || []).includes("failure_ok")), `bake-off ledger(s) of ${it.group} (COMPLETE or accepted FAILED)`, ["VERIFIED", "FAILED_ACCEPTED"]);
        }
        if (it.prog === "WG") {
          chk(it.members || [], `requirement(s) of ${it.group}`);
          if (it.group === "WG-WP-17") { chk(of(i => i.id.startsWith("E2E-WG-001.")), "end-to-end step(s)"); chk(of(i => i.id.startsWith("WG-DOD-")), "definition-of-done item(s)"); }
        }
        if (it.prog === "ASPEII" && it.group === "WP18") {
          chk(of(i => i.prog === "ASPEII" && ["clause", "acceptance", "scenario", "profile"].includes(i.kind)), "ASPEII clause / acceptance / scenario / profile item(s)");
        }
      }
      if (it.id === "IP-DOD-1") chk(of(i => i.prog === "IP" && i.kind === "req"), "IP requirement(s)");
      if (it.id === "WG-DOD-1") chk(of(i => i.prog === "WG" && i.kind === "req"), "Wisdom requirement(s)");
      if (it.id === "WG-DOD-4") chk(of(i => i.id.startsWith("E2E-WG-001.")), "end-to-end step(s)");
      if (it.id === "IP-DOD-4") chk(of(i => i.id.startsWith("E2E-IP-001.")), "end-to-end step(s)");
      if (it.id === "GN-CD-01" || it.id === "GN-SO-01") chk(of(i => i.prog === "GN" && i.kind === "ledger" && i.priority === "P0"), "P0 ledger(s)");
      if (it.id === "CIP-REL-01") chk(of(i => i.prog === "CIP" && i.kind === "clause"), "acceptance clause(s)");
      return out;
    }

    /* --- problems of the state currently recorded (used for import validation and the verifier) --- */
    function problems(id, ctx) {
      const it = BY[id]; const r = ctx.rec(id) || {}; const s = ctx.state(id);
      if (!it) return ["Unknown item id."];
      if (!STATES.includes(s)) return [`Unsupported state '${s}'.`];
      if (s === "OPEN") return [];
      return errors(id, s, r, ctx);
    }
    function warnings(id, ctx) {
      const it = BY[id]; const w = [];
      if (it.prog === "ASPEII" && it.kind === "gate" && ctx.state(id) === "VERIFIED") {
        const cov = (it.covers || []).flatMap(rq => (children[rq] || [])); const open = cov.filter(c => ctx.state(c) !== "VERIFIED");
        if (open.length) w.push(`${open.length} clause(s) of covered requirements not yet VERIFIED; gate evidence alone does not verify them.`);
        const pre = (it.deps || []).filter(g => ctx.state(g) !== "VERIFIED"); if (pre.length) w.push(`Depends on ${pre.join(", ")}.`);
      }
      return w;
    }
    function decisionErrors(target, r) {
      const e = []; const need = (c, m) => { if (!c) e.push(m); };
      if (target === "BLOCKED") need((r.blocked_by || "").trim(), "Name what blocks the decision.");
      if (target === "DECIDED") {
        need((r.decided_by || "").trim(), "Decided-by (owner, counsel or delegated authority) required.");
        need(DECISION_REF.test((r.decision_ref || "").trim()), "Decision reference required: CONFLICT-IP-NNN, DR-IP-NNN, CONFLICT-WG-NNN, DR-WG-NNN, Q-NNN, ADR-…, ASPEII-DEC-NNN, CIP-DEC-NNN, LEGAL-… or OWNER-….");
        need(DATE.test(r.decision_date || ""), "Decision date (YYYY-MM-DD) required.");
        need((r.choice || "").trim(), "Record the option chosen (accept proposal, or the alternative in full).");
      }
      return e;
    }

    /* --- completion summary in each programme's own terms --- */
    function summary(ctx) {
      const cnt = (ids, ok) => ids.filter(x => (ok || ["VERIFIED"]).includes(ctx.state(x))).length;
      const A = of(i => i.prog === "ASPEII" && i.kind === "clause");
      const aAll = of(i => i.prog === "ASPEII");
      const C = of(i => i.prog === "CIP" && i.kind === "clause");
      const cEng = of(i => i.prog === "CIP" && ((i.kind === "gate" && i.group !== "CIP-P8") || ["scenario", "negative"].includes(i.kind)));
      const cRel = of(i => i.prog === "CIP" && ((i.kind === "gate" && i.group === "CIP-P8") || i.kind === "release"));
      const I = of(i => i.prog === "IP" && i.kind === "req");
      const iAll = of(i => i.prog === "IP");
      const W = of(i => i.prog === "WG" && i.kind === "req");
      const wAll = of(i => i.prog === "WG");
      const G0 = of(i => i.prog === "GN" && i.kind === "ledger" && i.priority === "P0");
      const GL = of(i => i.prog === "GN" && i.kind === "ledger");
      const gAll = of(i => i.prog === "GN");
      const openDec = (D.xp || []).filter(x => ctx.dec(x.id) !== "DECIDED").length + (ctx.log() || []).filter(e => e.state !== "DECIDED").length;
      return {
        ASPEII: { primary: [cnt(A), A.length, "clauses VERIFIED"], all: [cnt(aAll), aAll.length], full: cnt(aAll) === aAll.length },
        CIP: { primary: [cnt(C), C.length, "acceptance clauses PASS_WITH_EVIDENCE"], engineering: [cnt(cEng), cEng.length], release: [cnt(cRel), cRel.length], all: [cnt(of(i => i.prog === "CIP")), of(i => i.prog === "CIP").length], full: cnt(C) === C.length && cnt(cEng) === cEng.length },
        IP: { primary: [cnt(I), I.length, "requirements VERIFIED"], all: [cnt(iAll), iAll.length], full: cnt(iAll) === iAll.length },
        WG: { primary: [cnt(W), W.length, "requirements VERIFIED"], all: [cnt(wAll), wAll.length], full: wAll.length > 0 && cnt(wAll) === wAll.length },
        GN: { primary: [cnt(G0), G0.length, "P0 ledgers COMPLETE"], resolved: [cnt(GL, ["VERIFIED", "FAILED_ACCEPTED"]), GL.length], all: [cnt(gAll, ["VERIFIED", "FAILED_ACCEPTED"]), gAll.length], full: cnt(gAll, ["VERIFIED", "FAILED_ACCEPTED"]) === gAll.length },
        openDecisions: openDec,
      };
    }
    return { STATES, DSTATES, RANK, NATIVE, ASPEII_PROFILES, ASPEII_LEVELS, BY, children, byGroup, blockersOf, allowedStates, native, errors, problems, warnings, decisionErrors, summary, openBlockers, startPrereqs, closePrereqs };
  }
  const api = { build };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.ProgrammeRules = api;
})(typeof self !== "undefined" ? self : this);

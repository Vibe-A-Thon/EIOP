#!/usr/bin/env node
/* verify_programme_ledger.mjs — independent check of an EOIP programme ledger (eoip-programme-ledger-v1).
 *
 *   node tools/tracker/verify_programme_ledger.mjs --registry tools/tracker/EOIP-programme-registry.json \
 *        --ledger docs/programme/programme-ledger.json [--repo .] [--programme ASPEII|CIP|IP|GN|ALL] [--json]
 *   node tools/tracker/verify_programme_ledger.mjs --registry … --init > docs/programme/programme-ledger.json
 *
 * Exit codes (same convention as scripts/verify_aspeii_evidence.py): 0 = every item in scope is complete
 * and no problem was found; 1 = incomplete or at least one problem; 2 = malformed input or internal error.
 * With --repo, every evidence_path must exist and its SHA-256 must equal evidence_sha256
 * (file: SHA-256 of bytes; directory: SHA-256 of the sorted lines "<relative path>\t<sha256>\n").
 * The rules come from programme_rules.js, the same engine the tracker page uses.
 */
import { createRequire } from "node:module";
import { readFileSync, existsSync, statSync, readdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, relative, dirname } from "node:path";
import { fileURLToPath } from "node:url";
const require = createRequire(import.meta.url);
const here = dirname(fileURLToPath(import.meta.url));
const { build } = require(join(here, "programme_rules.js"));

function arg(name, def = null) { const i = process.argv.indexOf(name); return i > 0 ? (process.argv[i + 1] ?? def) : def; }
const flag = n => process.argv.includes(n);
function fail2(msg) { console.error("MALFORMED: " + msg); process.exit(2); }

let D, L;
try { D = JSON.parse(readFileSync(arg("--registry") || join(here, "EOIP-programme-registry.json"), "utf8")); } catch (e) { fail2("cannot read registry: " + e.message); }
if (!Array.isArray(D.items) || !D.meta) fail2("registry has no items/meta");
const R = build(D);

if (flag("--init")) {
  const items = {}; D.items.forEach(i => items[i.id] = { state: "OPEN", text_sha256: i.text_sha256, history: [] });
  const decisions = {}; (D.xp || []).forEach(x => decisions[x.id] = { state: "OPEN", history: [] });
  process.stdout.write(JSON.stringify({ schema: "eoip-programme-ledger-v1", registry_sha256: D.registry_sha256, exported_at: new Date().toISOString(), items, decisions, log: [] }, null, 2) + "\n");
  process.exitCode = 0;  // let stdout drain; process.exit() can truncate piped output
} else main();
function main() {
try { L = JSON.parse(readFileSync(arg("--ledger") || "docs/programme/programme-ledger.json", "utf8")); } catch (e) { fail2("cannot read ledger: " + e.message); }
if (L.schema !== "eoip-programme-ledger-v1") fail2(`unsupported ledger schema '${L.schema}'`);
if (!L.items || typeof L.items !== "object" || Array.isArray(L.items)) fail2("ledger.items must be an object keyed by item id");
const scope = (arg("--programme", "ALL") || "ALL").toUpperCase();
if (!["ALL", "ASPEII", "CIP", "IP", "GN"].includes(scope)) fail2("--programme must be ASPEII, CIP, IP, GN or ALL");

const problems = []; const add = (id, msg) => problems.push({ id, problem: msg });
if (L.registry_sha256 && L.registry_sha256 !== D.registry_sha256) add("(ledger)", `ledger was produced against registry ${L.registry_sha256.slice(0, 12)}…, current registry is ${D.registry_sha256.slice(0, 12)}…; requirement text may have changed — items bound to old text are STALE`);
Object.keys(L.items).forEach(id => { if (!R.BY[id]) add(id, "unknown item id (not in registry) — rejected"); });
const log = Array.isArray(L.log) ? L.log : [];
const ctx = {
  state: id => (L.items[id] && L.items[id].state) || "OPEN",
  rec: id => L.items[id] || {},
  dec: id => (L.decisions && L.decisions[id] && L.decisions[id].state) || "OPEN",
  log: () => log,
};
// decisions
(D.xp || []).forEach(x => { const r = (L.decisions || {})[x.id] || {}; const s = r.state || "OPEN"; if (!R.DSTATES.includes(s)) add(x.id, `unsupported decision state '${s}'`); else if (s !== "OPEN") R.decisionErrors(s, r).forEach(m => add(x.id, m)); });
log.forEach(e => { if (!e.id) add("(log)", "log entry without id"); (e.affects || []).forEach(a => { if (!R.BY[a]) add(e.id, `log entry affects unknown item ${a}`); }); if (e.state && e.state !== "OPEN") R.decisionErrors(e.state, e).forEach(m => add(e.id, m)); });

function sha256File(p) { return createHash("sha256").update(readFileSync(p)).digest("hex"); }
function walk(dir) { const out = []; for (const n of readdirSync(dir)) { const p = join(dir, n); if (statSync(p).isDirectory()) out.push(...walk(p)); else out.push(p); } return out; }
function sha256Path(p) {
  if (statSync(p).isDirectory()) {
    const lines = walk(p).map(f => [relative(p, f).split("\\").join("/"), sha256File(f)]).sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0).map(([r, h]) => `${r}\t${h}\n`).join("");
    return createHash("sha256").update(lines, "utf8").digest("hex");
  }
  return sha256File(p);
}
const repo = arg("--repo");
const inScope = i => scope === "ALL" || i.prog === scope;
D.items.filter(inScope).forEach(i => {
  R.problems(i.id, ctx).forEach(m => add(i.id, m));
  const r = L.items[i.id] || {}; const s = ctx.state(i.id);
  if (repo && (R.RANK[s] >= 3 || s === "FAILED_ACCEPTED") && r.evidence_path) {
    const p = join(repo, r.evidence_path);
    if (!existsSync(p)) add(i.id, `evidence_path ${r.evidence_path} does not exist in ${repo}`);
    else { const h = sha256Path(p); if (h !== (r.evidence_sha256 || "").toLowerCase()) add(i.id, `evidence digest mismatch: recorded ${String(r.evidence_sha256).slice(0, 12)}…, actual ${h.slice(0, 12)}… → STALE`); }
  }
  if (repo && R.RANK[s] >= 4 && r.verification_ref) { if (!existsSync(join(repo, r.verification_ref))) add(i.id, `verification_ref ${r.verification_ref} does not exist`); }
});
const S = R.summary(ctx);
const done = D.items.filter(inScope).filter(i => ["VERIFIED", "FAILED_ACCEPTED"].includes(ctx.state(i.id))).length;
const total = D.items.filter(inScope).length;
const blockingDecisions = (D.xp || []).filter(x => ctx.dec(x.id) !== "DECIDED" && x.blocks.some(b => scope === "ALL" || R.BY[b].prog === scope)).map(x => x.id);
const complete = problems.length === 0 && done === total && blockingDecisions.length === 0;
const report = { verdict: complete ? "PASS" : "INCOMPLETE", scope, done, total, summary: S, open_blocking_decisions: blockingDecisions, problems };
if (flag("--json")) process.stdout.write(JSON.stringify(report, null, 2) + "\n");
else {
  console.log(`EOIP programme ledger verification — scope ${scope}`);
  console.log(`  ASPEII ${S.ASPEII.primary[0]}/${S.ASPEII.primary[1]} clauses VERIFIED · all items ${S.ASPEII.all[0]}/${S.ASPEII.all[1]}`);
  console.log(`  CIP    ${S.CIP.primary[0]}/${S.CIP.primary[1]} AC PASS_WITH_EVIDENCE · engineering ${S.CIP.engineering[0]}/${S.CIP.engineering[1]} · release ${S.CIP.release[0]}/${S.CIP.release[1]}`);
  console.log(`  IP     ${S.IP.primary[0]}/${S.IP.primary[1]} REQ VERIFIED · all items ${S.IP.all[0]}/${S.IP.all[1]}`);
  console.log(`  GN     ${S.GN.primary[0]}/${S.GN.primary[1]} P0 ledgers COMPLETE · ledgers resolved ${S.GN.resolved[0]}/${S.GN.resolved[1]}`);
  console.log(`  In scope: ${done}/${total} items done; open blocking decisions: ${blockingDecisions.length}; problems: ${problems.length}`);
  problems.slice(0, 200).forEach(p => console.log(`  ✗ ${p.id}: ${p.problem}`));
  if (problems.length > 200) console.log(`  … ${problems.length - 200} more (use --json)`);
  console.log(`VERDICT: ${report.verdict}`);
}
process.exitCode = complete ? 0 : 1;
}

import { useMemo, useState, useEffect } from "react";
import {
  CheckCheck, CircleCheck, CircleX, GitBranch, GitCompareArrows, GitMerge, GitPullRequest,
  Loader2, Plus, Radar, RotateCcw, Shapes, Trash2, TriangleAlert,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "../lib/api";
import { useAuth } from "../lib/auth";
import { Card, Overline } from "./ui/Card";
import { Badge } from "./ui/Badge";
import { Button } from "./ui/Button";

type ChangeKind = "add_vertex_label" | "add_edge_label" | "add_property";
interface DraftChange {
  id: string;
  kind: ChangeKind;
  label: string;
  domain?: string;
  source?: string;
  target?: string;
  property?: string;
  propertyType?: string;
}

function buildBase(schema: any) {
  const base: any = { vertex_labels: {}, edge_labels: {}, property_keys: {} };
  Object.entries(schema?.vertex_labels || {}).forEach(([label, m]: any) => {
    base.vertex_labels[label] = { domain: m.domain, required: m.required_properties || [] };
  });
  Object.entries(schema?.edge_labels || {}).forEach(([label, m]: any) => {
    base.edge_labels[label] = { out: m.source_labels || [], in: m.target_labels || [] };
  });
  const pk = schema?.property_keys;
  if (Array.isArray(pk)) pk.forEach((k: string) => (base.property_keys[k] = "string"));
  else if (pk && typeof pk === "object") base.property_keys = { ...pk };
  return base;
}

function applyChanges(base: any, changes: DraftChange[]) {
  const next = JSON.parse(JSON.stringify(base));
  changes.forEach((c) => {
    if (c.kind === "add_vertex_label") next.vertex_labels[c.label] = { domain: c.domain || "META", required: c.property ? [c.property] : [] };
    else if (c.kind === "add_edge_label") next.edge_labels[c.label] = { out: c.source ? [c.source] : [], in: c.target ? [c.target] : [] };
    else if (c.kind === "add_property") next.property_keys[c.property || c.label] = c.propertyType || "string";
  });
  return next;
}

const STEPS = ["Draft", "Edit", "Validate", "Review", "Publish"] as const;

function StepChip({ label, state }: { label: string; state: "done" | "active" | "idle" }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={`flex h-5 w-5 items-center justify-center rounded-full text-[9px] font-bold ${state === "done" ? "bg-emerald-500/20 text-emerald-300" : state === "active" ? "bg-[var(--accent)]/20 text-cyan-300 ring-1 ring-[var(--accent)]" : "bg-[var(--bg-panel)] text-[var(--text-muted)]"}`}>
        {state === "done" ? <CircleCheck size={12} /> : STEPS.indexOf(label as any) + 1}
      </span>
      <span className={`text-[11px] ${state === "idle" ? "text-[var(--text-muted)]" : "text-[var(--text-primary)]"}`}>{label}</span>
    </div>
  );
}

export function OntologyDesigner({ schema, onRefetchSchema }: { schema: any; onRefetchSchema: () => void }) {
  const { session } = useAuth();
  const qc = useQueryClient();
  const author = session?.principal.id || "anonymous";
  const isAdmin = (session?.principal.roles || []).some((r) => r === "admin" || r === "system");

  const [branch, setBranch] = useState<string | null>(null);
  const [branchInput, setBranchInput] = useState(`feature/draft-${Date.now().toString(36)}`);
  const [changes, setChanges] = useState<DraftChange[]>([]);
  const [busy, setBusy] = useState<string | null>(null);
  const [notice, setNotice] = useState<{ tone: "ok" | "err"; msg: string } | null>(null);

  const [validateResult, setValidateResult] = useState<any>(null);
  const [diffResult, setDiffResult] = useState<any>(null);
  const [impactResult, setImpactResult] = useState<any>(null);
  const [pr, setPr] = useState<any>(null);
  const [published, setPublished] = useState<any>(null);

  const [confirmPublish, setConfirmPublish] = useState(false);
  const [confirmText, setConfirmText] = useState("");
  const [confirmRollback, setConfirmRollback] = useState(false);
  const [rollbackVersion, setRollbackVersion] = useState("1.0.0");
  const [rollbackText, setRollbackText] = useState("");

  useEffect(() => {
    if (!confirmPublish && !confirmRollback) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") { setConfirmPublish(false); setConfirmRollback(false); } };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [confirmPublish, confirmRollback]);

  // change authoring form
  const [kind, setKind] = useState<ChangeKind>("add_vertex_label");
  const [fLabel, setFLabel] = useState("");
  const [fDomain, setFDomain] = useState("");
  const [fSource, setFSource] = useState("");
  const [fTarget, setFTarget] = useState("");
  const [fProp, setFProp] = useState("");

  const domains: string[] = schema?.domains || [];
  const vertexLabels = useMemo(() => Object.keys(schema?.vertex_labels || {}).sort(), [schema]);

  const base = useMemo(() => buildBase(schema), [schema]);
  const next = useMemo(() => applyChanges(base, changes), [base, changes]);

  const validated = validateResult?.publishable === true || validateResult?.verdict === "PUBLISH_OK";

  const addChange = () => {
    if (!fLabel.trim() && kind !== "add_property") return;
    if (kind === "add_property" && !fProp.trim()) return;
    const c: DraftChange = {
      id: Math.random().toString(36).slice(2),
      kind,
      label: fLabel.trim(),
      domain: fDomain || domains[0],
      source: fSource || undefined,
      target: fTarget || undefined,
      property: fProp.trim() || undefined,
      propertyType: "string",
    };
    setChanges((p) => [...p, c]);
    setFLabel(""); setFSource(""); setFTarget(""); setFProp("");
    setValidateResult(null); setDiffResult(null); setImpactResult(null);
  };

  const run = async (name: string, fn: () => Promise<void>) => {
    setBusy(name); setNotice(null);
    try { await fn(); }
    catch (e: any) { setNotice({ tone: "err", msg: e?.problem?.detail || e?.message || `${name} failed` }); }
    finally { setBusy(null); }
  };

  const createDraft = () => run("draft", async () => {
    const r = await apiFetch<any>("/ontology/gitops/branches", { method: "POST", body: { branch_name: branchInput.trim(), base_branch: "main" } });
    setBranch(r.branch || branchInput.trim());
    setNotice({ tone: "ok", msg: `Draft branch "${r.branch}" created.` });
  });

  const doValidate = () => run("validate", async () => {
    const [v, d, imp] = await Promise.all([
      apiFetch<any>("/ontology/gitops/validate", { method: "POST", body: { old: base, new: next } }),
      apiFetch<any>("/ontology/gitops/diff", { method: "POST", body: { old: base, new: next } }),
      apiFetch<any>("/ontology/gitops/impact", { method: "POST", body: { old: base, new: next } }),
    ]);
    setValidateResult(v); setDiffResult(d); setImpactResult(imp);
  });

  const requestReview = () => run("review", async () => {
    await apiFetch<any>("/ontology/gitops/branches/commit", {
      method: "POST",
      body: { branch_name: branch, manifest: next, commit_message: `${changes.length} ontology change(s)`, author },
    });
    const p = await apiFetch<any>("/ontology/gitops/prs", {
      method: "POST",
      body: { title: `Ontology draft: ${changes.length} change(s)`, source_branch: branch, target_branch: "main", author },
    });
    setPr(p);
    setNotice({ tone: "ok", msg: `Pull request ${p.pr_id} opened for review.` });
  });

  const doPublish = () => run("publish", async () => {
    await apiFetch<any>(`/ontology/gitops/prs/${pr.pr_id}/review`, {
      method: "POST",
      body: { reviewer: author, decision: "approve", comment: "Approved via Ontology Designer" },
    }).catch(() => {});
    const merged = await apiFetch<any>(`/ontology/gitops/prs/${pr.pr_id}/merge`, {
      method: "POST",
      body: { merger: author, allow_breaking: true },
    });
    setPublished(merged);
    setConfirmPublish(false); setConfirmText("");
    setNotice({ tone: "ok", msg: `Published — merged into main.` });
    onRefetchSchema();
    qc.invalidateQueries();
    const v = await apiFetch<any>("/ontology/gitops/validate", { method: "POST", body: {} }).catch(() => null);
    if (v) setValidateResult(v);
  });

  const doRollback = () => run("rollback", async () => {
    const r = await apiFetch<any>("/ontology/gitops/rollback", { method: "POST", body: { target_version: rollbackVersion.trim(), allow_breaking: true } });
    setConfirmRollback(false); setRollbackText("");
    setNotice({ tone: "ok", msg: `Rolled back to ${r.version || rollbackVersion}.` });
    onRefetchSchema();
  });

  const stepState = (s: string): "done" | "active" | "idle" => {
    if (s === "Draft") return branch ? "done" : "active";
    if (s === "Edit") return !branch ? "idle" : changes.length ? "done" : "active";
    if (s === "Validate") return !changes.length ? "idle" : validated ? "done" : "active";
    if (s === "Review") return !validated ? "idle" : pr ? "done" : "active";
    if (s === "Publish") return !pr ? "idle" : published ? "done" : "active";
    return "idle";
  };

  const dq = diffResult?.counts || validateResult?.counts;

  if (!isAdmin) {
    return (
      <Card className="p-5 text-sm text-[var(--text-muted)]">
        <div className="flex items-center gap-2 text-amber-300"><TriangleAlert size={15} /> Requires admin role</div>
        <p className="mt-1">Ontology drafting and publishing require the <code className="font-mono">admin</code> or <code className="font-mono">system</code> role. You can still inspect the active ontology on the Overview tab.</p>
      </Card>
    );
  }

  return (
    <div className="space-y-4" data-testid="ontology-designer">
      {/* Version bar + stepper */}
      <Card className="flex flex-wrap items-center justify-between gap-4 p-3">
        <div className="flex items-center gap-3">
          <Shapes size={16} className="text-cyan-400" />
          <div>
            <Overline>Active</Overline>
            <p className="text-sm font-medium">ontology {schema?.ontology_version ?? "—"} · schema {schema?.schema_version ?? "—"}</p>
          </div>
          <div className="ml-2 border-l border-[var(--border-subtle)] pl-3">
            <Overline>Draft</Overline>
            <p className="text-sm font-medium" data-testid="ontology-draft-state">
              {branch ? <span className="flex items-center gap-1.5 text-cyan-300"><GitBranch size={13} /> {branch} ({changes.length} change{changes.length === 1 ? "" : "s"})</span> : <span className="text-[var(--text-muted)]">No draft</span>}
            </p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          {STEPS.map((s) => <StepChip key={s} label={s} state={stepState(s)} />)}
        </div>
      </Card>

      {notice && (
        <div className={`flex items-center gap-2 rounded-sm border px-3 py-2 text-xs ${notice.tone === "ok" ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-200" : "border-red-500/40 bg-red-500/10 text-red-200"}`} data-testid="ontology-notice">
          {notice.tone === "ok" ? <CircleCheck size={14} /> : <CircleX size={14} />} {notice.msg}
        </div>
      )}

      {!branch ? (
        <Card className="p-4">
          <Overline>Step 1 — Create a draft</Overline>
          <p className="mt-1 text-xs text-[var(--text-muted)]">Editing never mutates the active ontology. All edits accumulate on a branch and are published via a reviewed merge.</p>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <input data-testid="ontology-branch-input" value={branchInput} onChange={(e) => setBranchInput(e.target.value)} className="h-9 flex-1 min-w-[220px] rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--accent)]" placeholder="feature/branch-name" />
            <Button variant="primary" data-testid="ontology-create-draft" onClick={createDraft} disabled={busy === "draft" || !branchInput.trim()}>
              {busy === "draft" ? <Loader2 size={14} className="animate-spin" /> : <GitBranch size={14} />} Create draft
            </Button>
          </div>
        </Card>
      ) : (
        <div className="grid gap-4 lg:grid-cols-[1fr_380px]">
          <div className="space-y-4">
            {/* Edit */}
            <Card className="p-4">
              <Overline>Step 2 — Edit ontology (manifest)</Overline>
              <div className="mt-3 flex flex-wrap items-end gap-2">
                <div>
                  <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Change kind</label>
                  <select data-testid="ontology-change-kind" value={kind} onChange={(e) => setKind(e.target.value as ChangeKind)} className="h-8 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none">
                    <option value="add_vertex_label">Add vertex label</option>
                    <option value="add_edge_label">Add edge label</option>
                    <option value="add_property">Add property key</option>
                  </select>
                </div>
                {kind !== "add_property" && (
                  <div>
                    <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Label</label>
                    <input data-testid="ontology-field-label" value={fLabel} onChange={(e) => setFLabel(e.target.value)} placeholder="MyType" className="h-8 w-32 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]" />
                  </div>
                )}
                {kind === "add_vertex_label" && (
                  <div>
                    <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Domain</label>
                    <select data-testid="ontology-field-domain" value={fDomain} onChange={(e) => setFDomain(e.target.value)} className="h-8 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none">
                      {["", ...domains].map((d) => <option key={d} value={d}>{d || "(select domain)"}</option>)}
                    </select>
                  </div>
                )}
                {kind === "add_edge_label" && (
                  <>
                    <div>
                      <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Source</label>
                      <select data-testid="ontology-field-source" value={fSource} onChange={(e) => setFSource(e.target.value)} className="h-8 w-28 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-1.5 text-xs outline-none">
                        {["", ...vertexLabels].map((l) => <option key={l} value={l}>{l || "any"}</option>)}
                      </select>
                    </div>
                    <div>
                      <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Target</label>
                      <select data-testid="ontology-field-target" value={fTarget} onChange={(e) => setFTarget(e.target.value)} className="h-8 w-28 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-1.5 text-xs outline-none">
                        {["", ...vertexLabels].map((l) => <option key={l} value={l}>{l || "any"}</option>)}
                      </select>
                    </div>
                  </>
                )}
                {kind === "add_property" && (
                  <div>
                    <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Property key</label>
                    <input data-testid="ontology-field-property" value={fProp} onChange={(e) => setFProp(e.target.value)} placeholder="my_property" className="h-8 w-36 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]" />
                  </div>
                )}
                <Button size="sm" variant="secondary" data-testid="ontology-add-change" onClick={addChange}><Plus size={13} /> Add to draft</Button>
              </div>

              {changes.length > 0 && (
                <div className="mt-3 divide-y divide-[var(--border-subtle)] rounded-sm border border-[var(--border-subtle)]">
                  <AnimatePresence initial={false}>
                    {changes.map((c) => (
                      <motion.div key={c.id} initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="flex items-center gap-2 px-3 py-2 text-xs" data-testid="ontology-change-row">
                        <Badge tone="accent">{c.kind.replace("add_", "+")}</Badge>
                        <span className="font-mono">
                          {c.kind === "add_vertex_label" && `${c.label} · ${c.domain}`}
                          {c.kind === "add_edge_label" && `${c.label} (${c.source || "any"} → ${c.target || "any"})`}
                          {c.kind === "add_property" && `${c.property}`}
                        </span>
                        <button className="ml-auto text-[var(--text-muted)] hover:text-red-300" onClick={() => { setChanges((p) => p.filter((x) => x.id !== c.id)); setValidateResult(null); setDiffResult(null); setImpactResult(null); }}><Trash2 size={13} /></button>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
              )}
              {changes.length === 0 && <p className="mt-3 text-xs text-[var(--text-muted)]">No changes yet. Add a label, relationship or property to build the draft manifest.</p>}
            </Card>

            {/* Validate / Diff / Impact */}
            <Card className="p-4">
              <div className="flex items-center justify-between">
                <Overline>Step 3 — Validate · Diff · Impact preview</Overline>
                <Button size="sm" variant="outline" data-testid="ontology-validate" onClick={doValidate} disabled={busy === "validate" || changes.length === 0}>
                  {busy === "validate" ? <Loader2 size={13} className="animate-spin" /> : <CheckCheck size={13} />} Validate draft
                </Button>
              </div>
              {!validateResult ? (
                <p className="mt-3 text-xs text-[var(--text-muted)]">Validate the draft to compute the semantic diff, safety verdict and impact against existing data before review.</p>
              ) : (
                <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className="mt-3 space-y-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge tone={validated ? "success" : "danger"} testId="ontology-verdict">{validateResult.verdict || (validated ? "PUBLISH_OK" : "BLOCKED")}</Badge>
                    {dq && <>
                      <span className="rounded-sm border border-[var(--border-subtle)] px-2 py-0.5 font-mono text-[10px]">total {dq.total}</span>
                      <span className="rounded-sm border border-emerald-500/40 bg-emerald-500/10 px-2 py-0.5 font-mono text-[10px] text-emerald-300">+{dq.additive} additive</span>
                      <span className="rounded-sm border border-amber-500/40 bg-amber-500/10 px-2 py-0.5 font-mono text-[10px] text-amber-300">{dq.potentially_breaking} maybe-breaking</span>
                      <span className="rounded-sm border border-red-500/40 bg-red-500/10 px-2 py-0.5 font-mono text-[10px] text-red-300">{dq.breaking} breaking</span>
                    </>}
                  </div>
                  {(diffResult?.changes || []).length > 0 && (
                    <div className="space-y-1" data-testid="ontology-diff-list">
                      {(diffResult.changes || []).slice(0, 12).map((c: any, i: number) => (
                        <div key={i} className="flex items-center gap-2 rounded-sm bg-[var(--bg-void)] px-2 py-1 text-[11px]">
                          <Badge tone={c.classification === "breaking" ? "danger" : c.classification === "potentially_breaking" ? "warning" : "success"}>{c.change_type || c.kind}</Badge>
                          <span className="font-mono">{c.target || c.name}</span>
                          <span className="truncate text-[var(--text-muted)]">{c.detail || c.description}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  {impactResult && (
                    <div className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-2.5 text-[11px]" data-testid="ontology-impact">
                      <div className="flex items-center gap-2"><Radar size={12} className="text-cyan-400" /> <span className="font-medium">Impact</span>
                        <Badge tone={impactResult.risk_level === "HIGH" ? "danger" : impactResult.risk_level === "MEDIUM" ? "warning" : "success"}>{impactResult.risk_level || "LOW"}</Badge>
                      </div>
                      <p className="mt-1 text-[var(--text-muted)]">
                        Affected: {impactResult.affected_vertices_count ?? 0} vertices · {impactResult.affected_edges_count ?? 0} edges ·
                        {" "}labels [{(impactResult.affected_vertex_labels || []).join(", ") || "none"}]
                      </p>
                      {(impactResult.recommendations || []).map((r: string, i: number) => <p key={i} className="mt-0.5 text-[var(--text-secondary)]">• {r}</p>)}
                    </div>
                  )}
                </motion.div>
              )}
            </Card>
          </div>

          {/* Right: review + publish */}
          <div className="space-y-4">
            <Card className="p-4">
              <Overline>Step 4 — Request review</Overline>
              <p className="mt-1 text-xs text-[var(--text-muted)]">Commit the draft manifest and open a pull request for merge.</p>
              <Button className="mt-3 w-full justify-center" variant="secondary" data-testid="ontology-request-review" onClick={requestReview} disabled={busy === "review" || !validated}>
                {busy === "review" ? <Loader2 size={14} className="animate-spin" /> : <GitPullRequest size={14} />} Request review (open PR)
              </Button>
              {!validated && <p className="mt-2 text-[10px] text-amber-300/80">Validate the draft first — publish stays disabled until the draft is validated.</p>}
              {pr && (
                <div className="mt-3 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-2.5 text-[11px]" data-testid="ontology-pr">
                  <div className="flex items-center gap-2"><GitPullRequest size={12} className="text-cyan-400" /><span className="font-mono">{pr.pr_id}</span><Badge tone="info">{pr.status}</Badge></div>
                  <p className="mt-1 text-[var(--text-muted)]">{pr.source_branch} → {pr.target_branch}</p>
                </div>
              )}
            </Card>

            <Card className="p-4">
              <Overline>Step 5 — Publish (merge)</Overline>
              <p className="mt-1 text-xs text-[var(--text-muted)]">High-impact: merges the draft into the active ontology. Requires typed branch-name confirmation.</p>
              <Button className="mt-3 w-full justify-center" variant="primary" data-testid="ontology-publish" onClick={() => setConfirmPublish(true)} disabled={!pr || !!published}>
                <GitMerge size={14} /> Publish draft
              </Button>
              {published && (
                <div className="mt-3 rounded-sm border border-emerald-500/40 bg-emerald-500/10 p-2.5 text-[11px] text-emerald-200" data-testid="ontology-published">
                  <div className="flex items-center gap-2"><GitMerge size={12} /> Merged · {published.status || "merged"}</div>
                  {published.merged_at && <p className="mt-0.5 opacity-80">{new Date(published.merged_at).toLocaleString()}</p>}
                </div>
              )}
            </Card>

            <Card className="p-4">
              <Overline>Rollback</Overline>
              <p className="mt-1 text-xs text-[var(--text-muted)]">Roll the active ontology back to a previous semantic version. High-impact.</p>
              <div className="mt-2 flex items-center gap-2">
                <input data-testid="ontology-rollback-version" value={rollbackVersion} onChange={(e) => setRollbackVersion(e.target.value)} className="h-8 flex-1 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 font-mono text-xs outline-none" />
                <Button size="sm" variant="danger" data-testid="ontology-rollback" onClick={() => setConfirmRollback(true)}><RotateCcw size={13} /> Rollback</Button>
              </div>
            </Card>
          </div>
        </div>
      )}

      {/* Publish confirm */}
      {confirmPublish && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setConfirmPublish(false)} />
          <Card className="relative w-full max-w-sm p-4">
            <h3 className="flex items-center gap-2 font-heading text-sm font-semibold text-cyan-300"><GitMerge size={15} /> Publish ontology draft</h3>
            <p className="mt-1 text-xs text-[var(--text-muted)]">This merges <strong className="font-mono text-[var(--text-primary)]">{branch}</strong> into the active ontology. Type the branch name to confirm.</p>
            <input data-testid="ontology-publish-confirm-input" value={confirmText} onChange={(e) => setConfirmText(e.target.value)} className="mt-3 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--accent)]" placeholder={branch || ""} />
            <div className="mt-3 flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setConfirmPublish(false)}>Cancel</Button>
              <Button variant="primary" data-testid="ontology-publish-confirm" disabled={confirmText !== branch || busy === "publish"} onClick={doPublish}>
                {busy === "publish" ? <Loader2 size={14} className="animate-spin" /> : <GitMerge size={14} />} Publish
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* Rollback confirm */}
      {confirmRollback && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setConfirmRollback(false)} />
          <Card className="relative w-full max-w-sm p-4">
            <h3 className="flex items-center gap-2 font-heading text-sm font-semibold text-red-300"><RotateCcw size={15} /> Rollback ontology</h3>
            <p className="mt-1 text-xs text-[var(--text-muted)]">Rolls back to <strong className="font-mono text-[var(--text-primary)]">{rollbackVersion}</strong>. Type <strong className="font-mono text-[var(--text-primary)]">ROLLBACK</strong> to confirm.</p>
            <input data-testid="ontology-rollback-confirm-input" value={rollbackText} onChange={(e) => setRollbackText(e.target.value)} className="mt-3 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--danger)]" />
            <div className="mt-3 flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setConfirmRollback(false)}>Cancel</Button>
              <Button variant="danger" data-testid="ontology-rollback-confirm" disabled={rollbackText !== "ROLLBACK" || busy === "rollback"} onClick={doRollback}>
                {busy === "rollback" ? <Loader2 size={14} className="animate-spin" /> : <RotateCcw size={14} />} Rollback
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

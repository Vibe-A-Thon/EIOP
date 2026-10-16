import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";
import {
  History, Clock, GitCompareArrows, PlayCircle, Search, Loader2, Camera, RotateCcw, Trash2,
  Plus, ChevronRight, ChevronLeft, FileCheck, Info,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState } from "../components/ui/States";
import { shortId, relativeTime, cn } from "../lib/utils";

type Mode = "asof" | "compare" | "playback";
const MODES: { id: Mode; label: string; icon: any }[] = [
  { id: "asof", label: "As of", icon: Clock },
  { id: "compare", label: "Compare", icon: GitCompareArrows },
  { id: "playback", label: "Playback", icon: PlayCircle },
];

const nowLocal = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
const toISO = (local: string) => { try { return new Date(local).toISOString(); } catch { return ""; } };

export function Temporal() {
  const { session } = useAuth();
  const isAdmin = (session?.principal.roles || []).some((r) => r === "admin" || r === "system");
  const [mode, setMode] = useState<Mode>("asof");

  // As of
  const [validAt, setValidAt] = useState(nowLocal());
  const [knownAt, setKnownAt] = useState("");
  const [asof, setAsof] = useState<any>(null);
  const [slice, setSlice] = useState<any>(null);
  const [asofBusy, setAsofBusy] = useState(false);
  const [asofErr, setAsofErr] = useState<string | null>(null);

  // Compare
  const [fromAt, setFromAt] = useState(nowLocal());
  const [toAt, setToAt] = useState(nowLocal());
  const [diff, setDiff] = useState<any>(null);
  const [cmpBusy, setCmpBusy] = useState(false);

  // Playback
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [playback, setPlayback] = useState<any>(null);
  const [step, setStep] = useState(0);
  const [pbBusy, setPbBusy] = useState(false);

  // Snapshots
  const snapshots = useQuery({ queryKey: [session?.tenant, "snapshots-temporal"], queryFn: () => apiFetch<any>("/enterprise/snapshots"), retry: false });
  const snapList: any[] = snapshots.data?.snapshots || [];
  const [snapName, setSnapName] = useState("");
  const [snapBusy, setSnapBusy] = useState(false);
  const [confirmRestore, setConfirmRestore] = useState<any | null>(null);
  const [confirmText, setConfirmText] = useState("");

  const runAsof = async () => {
    const iso = toISO(validAt);
    if (!iso) { setAsofErr("Enter a valid date-time."); return; }
    setAsofBusy(true); setAsofErr(null); setAsof(null); setSlice(null);
    try {
      const body: any = { valid_at: iso };
      if (knownAt) body.known_at = toISO(knownAt);
      const [a, s] = await Promise.all([
        apiFetch<any>(`/graph/as-of?at=${encodeURIComponent(iso)}&limit=50`),
        apiFetch<any>("/graph/bitemporal/slice", { method: "POST", body }),
      ]);
      setAsof(a); setSlice(s);
    } catch (e: any) {
      setAsofErr(e?.problem?.detail || e?.message || "Query failed");
    } finally { setAsofBusy(false); }
  };

  const runCompare = async () => {
    const f = toISO(fromAt), t = toISO(toAt);
    if (!f || !t) return;
    setCmpBusy(true); setDiff(null);
    try {
      const r = await apiFetch<any>("/graph/bitemporal/diff", {
        method: "POST",
        body: { from_coordinate: { valid_at: f }, to_coordinate: { valid_at: t } },
      });
      setDiff(r);
    } finally { setCmpBusy(false); }
  };

  const searchRoot = async (v: string) => {
    setQ(v);
    if (!v.trim()) return setResults([]);
    try { const r = await apiFetch<any>(`/search?q=${encodeURIComponent(v.trim())}&limit=6`); setResults(r.nodes || []); }
    catch { setResults([]); }
  };
  const runPlayback = async (node: any) => {
    setResults([]); setQ(node.properties?.name || shortId(node.id)); setPbBusy(true); setPlayback(null); setStep(0);
    try {
      const r = await apiFetch<any>("/playback/stream", { method: "POST", body: { root_cid: node.id, max_depth: 3, max_events: 50 } });
      setPlayback(r);
    } finally { setPbBusy(false); }
  };

  const createSnapshot = async () => {
    if (!snapName.trim()) return;
    setSnapBusy(true);
    try {
      await apiFetch<any>("/enterprise/snapshots", { method: "POST", body: { name: snapName.trim(), snapshot_type: "FULL", tags: {} } });
      setSnapName(""); snapshots.refetch();
    } finally { setSnapBusy(false); }
  };
  const deleteSnapshot = async (id: string) => {
    setSnapBusy(true);
    try { await apiFetch<any>(`/enterprise/snapshots/${encodeURIComponent(id)}`, { method: "DELETE" }); snapshots.refetch(); }
    finally { setSnapBusy(false); }
  };
  const doRestore = async () => {
    if (!confirmRestore) return;
    setSnapBusy(true);
    try {
      await apiFetch<any>("/enterprise/snapshots/restore", { method: "POST", body: { snapshot_id: confirmRestore.snapshot_id } });
      setConfirmRestore(null); setConfirmText(""); snapshots.refetch();
    } finally { setSnapBusy(false); }
  };

  const diffSummary = diff?.summary || {};
  const events: any[] = playback?.events || [];
  const curEvent = events[step];

  return (
    <Page>
      <PageHeader title="Time Travel" overline="Bitemporal state · valid & known time · playback" icon={<History size={18} />} />

      {/* Mode selector */}
      <div className="flex items-center gap-1 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-void)] p-1" data-testid="temporal-mode-toggle">
        {MODES.map((m) => (
          <button key={m.id} data-testid={`temporal-mode-${m.id}`} onClick={() => setMode(m.id)}
            className={cn("flex items-center gap-1.5 rounded-sm px-3 py-1.5 text-xs transition-all duration-200", mode === m.id ? "bg-[var(--accent)] text-black font-semibold shadow-[0_0_14px_-4px_var(--accent)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)]")}>
            <m.icon size={13} /> {m.label}
          </button>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <div className="space-y-4">
          <AnimatePresence mode="wait">
            {/* AS OF */}
            {mode === "asof" && (
              <motion.div key="asof" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-4">
                <Card className="p-4">
                  <Overline>Temporal coordinate</Overline>
                  <div className="mt-3 flex flex-wrap items-end gap-3">
                    <div>
                      <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Valid at</label>
                      <input type="datetime-local" data-testid="temporal-valid-at" value={validAt} onChange={(e) => setValidAt(e.target.value)} className="h-9 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" />
                    </div>
                    <div>
                      <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Known at (optional)</label>
                      <input type="datetime-local" data-testid="temporal-known-at" value={knownAt} onChange={(e) => setKnownAt(e.target.value)} className="h-9 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" />
                    </div>
                    <Button variant="primary" data-testid="temporal-run-asof" onClick={runAsof} disabled={asofBusy}>
                      {asofBusy ? <Loader2 size={14} className="animate-spin" /> : <Clock size={14} />} Query state
                    </Button>
                  </div>
                  <p className="mt-2 flex items-center gap-1.5 text-[11px] text-[var(--text-muted)]"><Info size={11} /> Valid time = when a fact was true in the world; known time = when the graph learned it.</p>
                  {asofErr && <p className="mt-2 text-xs text-red-300" data-testid="temporal-asof-error">{asofErr}</p>}
                </Card>

                {(asof || slice) && (
                  <Card className="p-4" data-testid="temporal-asof-result">
                    <div className="flex items-center gap-2">
                      <Badge tone="info">as of {new Date(toISO(validAt)).toLocaleString()}</Badge>
                      {knownAt && <Badge tone="neutral">known at {new Date(toISO(knownAt)).toLocaleString()}</Badge>}
                    </div>
                    <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3">
                      <div><Overline>Entities</Overline><p className="mt-1 font-heading text-2xl font-bold">{(asof?.entities || slice?.entities || []).length}</p></div>
                      <div><Overline>Relationships</Overline><p className="mt-1 font-heading text-2xl font-bold">{(asof?.relationships || slice?.relationships || []).length}</p></div>
                      <div><Overline>Coordinate</Overline><p className="mt-1 font-mono text-xs text-[var(--text-secondary)]">valid · {slice?.coordinate?.known_at ? "known" : "latest-known"}</p></div>
                    </div>
                    {(asof?.entities || slice?.entities || []).length === 0 && (
                      <p className="mt-3 text-sm text-[var(--text-muted)]">No entities were valid at this coordinate in the current graph. The bitemporal store returns an empty slice rather than fabricating history.</p>
                    )}
                  </Card>
                )}
              </motion.div>
            )}

            {/* COMPARE */}
            {mode === "compare" && (
              <motion.div key="compare" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-4">
                <Card className="p-4">
                  <Overline>Compare two coordinates</Overline>
                  <div className="mt-3 flex flex-wrap items-end gap-3">
                    <div>
                      <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">From</label>
                      <input type="datetime-local" data-testid="temporal-from" value={fromAt} onChange={(e) => setFromAt(e.target.value)} className="h-9 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" />
                    </div>
                    <div>
                      <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">To</label>
                      <input type="datetime-local" data-testid="temporal-to" value={toAt} onChange={(e) => setToAt(e.target.value)} className="h-9 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" />
                    </div>
                    <Button variant="primary" data-testid="temporal-run-compare" onClick={runCompare} disabled={cmpBusy}>
                      {cmpBusy ? <Loader2 size={14} className="animate-spin" /> : <GitCompareArrows size={14} />} Compare
                    </Button>
                  </div>
                </Card>
                {diff && (
                  <Card className="p-4" data-testid="temporal-compare-result">
                    <Overline>Entity & relationship delta</Overline>
                    <div className="mt-3 grid grid-cols-3 gap-3">
                      {[
                        { label: "Added", v: diffSummary.entities_added ?? (diff.entities?.added?.length || 0), tone: "text-emerald-300" },
                        { label: "Removed", v: diffSummary.entities_removed ?? (diff.entities?.removed?.length || 0), tone: "text-red-300" },
                        { label: "Changed", v: diffSummary.entities_changed ?? (diff.entities?.changed?.length || 0), tone: "text-amber-300" },
                      ].map((s) => (
                        <div key={s.label} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-3">
                          <Overline>{s.label}</Overline>
                          <p className={cn("mt-1 font-heading text-2xl font-bold", s.tone)}>{s.v}</p>
                        </div>
                      ))}
                    </div>
                    {(diff.entities?.added?.length || 0) + (diff.entities?.removed?.length || 0) + (diff.entities?.changed?.length || 0) === 0 && (
                      <p className="mt-3 text-sm text-[var(--text-muted)]">No changes recorded between these coordinates.</p>
                    )}
                  </Card>
                )}
              </motion.div>
            )}

            {/* PLAYBACK */}
            {mode === "playback" && (
              <motion.div key="playback" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-4">
                <Card className="p-4">
                  <Overline>Playback from a root entity</Overline>
                  <div className="relative mt-3 max-w-md">
                    <div className="flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 focus-within:border-[var(--accent)]">
                      <Search size={15} className="text-[var(--text-muted)]" />
                      <input data-testid="temporal-playback-search" value={q} onChange={(e) => searchRoot(e.target.value)} placeholder="Search a root entity…" className="h-9 w-full bg-transparent text-sm outline-none" />
                      {pbBusy && <Loader2 size={13} className="animate-spin text-[var(--text-muted)]" />}
                    </div>
                    {results.length > 0 && (
                      <div className="absolute z-20 mt-1 w-full overflow-hidden rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-2xl">
                        {results.map((r) => (
                          <button key={r.id} data-testid="temporal-playback-result" onClick={() => runPlayback(r)} className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left transition-colors hover:bg-[var(--bg-hover)]">
                            <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">{r.label}</span>
                            <span className="truncate text-xs">{r.properties?.name || shortId(r.id)}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </Card>

                {playback && (
                  <Card className="p-4" data-testid="temporal-playback-result-panel">
                    <div className="flex items-center justify-between">
                      <Overline>Event {events.length ? step + 1 : 0} of {events.length}</Overline>
                      <div className="flex items-center gap-1">
                        <Button size="sm" variant="outline" data-testid="temporal-playback-prev" onClick={() => setStep((s) => Math.max(0, s - 1))} disabled={step === 0}><ChevronLeft size={13} /></Button>
                        <Button size="sm" variant="outline" data-testid="temporal-playback-next" onClick={() => setStep((s) => Math.min(events.length - 1, s + 1))} disabled={step >= events.length - 1}><ChevronRight size={13} /></Button>
                      </div>
                    </div>
                    {curEvent ? (
                      <motion.div key={step} initial={{ opacity: 0, x: 8 }} animate={{ opacity: 1, x: 0 }} className="mt-3 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-3">
                        <div className="flex items-center gap-2">
                          <Badge tone="accent">{curEvent.label}</Badge>
                          <span className="font-mono text-[11px] text-[var(--text-muted)]">depth {curEvent.depth}</span>
                          {curEvent.timestamp && <span className="ml-auto font-mono text-[10px] text-[var(--text-muted)]">{curEvent.timestamp}</span>}
                        </div>
                        <Link to={`/entity/${encodeURIComponent(curEvent.canonical_id)}`} className="mt-1.5 block truncate font-mono text-xs hover:text-[var(--accent)]">{curEvent.name || shortId(curEvent.canonical_id)}</Link>
                        <div className="mt-2 flex items-center gap-1 text-[10px] text-[var(--text-muted)]"><FileCheck size={11} /> evidence available via playback trail</div>
                      </motion.div>
                    ) : <EmptyState title="No events in this stream" />}
                    {/* scrubber */}
                    {events.length > 1 && (
                      <input type="range" min={0} max={events.length - 1} value={step} onChange={(e) => setStep(Number(e.target.value))} data-testid="temporal-scrubber" className="mt-3 w-full accent-[var(--accent)]" />
                    )}
                  </Card>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Snapshots drawer */}
        <Card className="h-fit" data-testid="temporal-snapshots">
          <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
            <Camera size={15} className="text-cyan-400" />
            <h3 className="font-heading text-sm font-semibold">Snapshots</h3>
            <Badge tone="neutral" className="ml-auto">{snapList.length}</Badge>
          </div>
          {isAdmin && (
            <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-3 py-2.5">
              <input data-testid="snapshot-name" value={snapName} onChange={(e) => setSnapName(e.target.value)} placeholder="Snapshot name" className="h-8 flex-1 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]" />
              <Button size="sm" variant="primary" data-testid="snapshot-create" onClick={createSnapshot} disabled={snapBusy || !snapName.trim()}>
                {snapBusy ? <Loader2 size={12} className="animate-spin" /> : <Plus size={12} />}
              </Button>
            </div>
          )}
          {snapList.length === 0 ? (
            <EmptyState title="No snapshots yet" description={isAdmin ? "Create a full snapshot to capture the current graph." : "Snapshots are created by admins."} icon={<Camera size={20} />} />
          ) : (
            <div className="divide-y divide-[var(--border-subtle)]" data-testid="snapshot-list">
              {snapList.map((s) => (
                <div key={s.snapshot_id} className="px-3 py-2.5 text-xs" data-testid="snapshot-row">
                  <div className="flex items-center gap-2">
                    <span className="min-w-0 flex-1 truncate font-medium">{s.name}</span>
                    <Badge tone={s.status === "READY" ? "success" : "neutral"}>{s.status}</Badge>
                  </div>
                  <p className="mt-0.5 font-mono text-[10px] text-[var(--text-muted)]">{s.entity_count} entities · {relativeTime(s.created_at)}</p>
                  {isAdmin && (
                    <div className="mt-1.5 flex items-center gap-1.5">
                      <Button size="sm" variant="outline" data-testid="snapshot-restore" onClick={() => setConfirmRestore(s)}><RotateCcw size={11} /> Restore</Button>
                      <Button size="sm" variant="ghost" data-testid="snapshot-delete" onClick={() => deleteSnapshot(s.snapshot_id)} className="text-[var(--text-muted)] hover:text-red-300"><Trash2 size={12} /></Button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* Restore confirm (high-impact, typed) */}
      {confirmRestore && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setConfirmRestore(null)} />
          <Card className="relative w-full max-w-sm p-4">
            <h3 className="flex items-center gap-2 font-heading text-sm font-semibold text-amber-300"><RotateCcw size={15} /> Restore snapshot</h3>
            <p className="mt-1 text-xs text-[var(--text-muted)]">Restoring <strong className="font-mono text-[var(--text-primary)]">{confirmRestore.name}</strong> is destructive and replaces the current graph state. Type the snapshot name to confirm.</p>
            <input data-testid="snapshot-restore-confirm-input" value={confirmText} onChange={(e) => setConfirmText(e.target.value)} className="mt-3 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--accent)]" placeholder={confirmRestore.name} />
            <div className="mt-3 flex justify-end gap-2">
              <Button variant="ghost" onClick={() => { setConfirmRestore(null); setConfirmText(""); }}>Cancel</Button>
              <Button variant="danger" data-testid="snapshot-restore-confirm" disabled={confirmText !== confirmRestore.name || snapBusy} onClick={doRestore}>
                {snapBusy ? <Loader2 size={14} className="animate-spin" /> : <RotateCcw size={14} />} Restore
              </Button>
            </div>
          </Card>
        </div>
      )}
    </Page>
  );
}

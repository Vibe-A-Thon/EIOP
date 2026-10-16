import { useState } from "react";
import { Link } from "react-router-dom";
import { Radar, Search, ShieldAlert, Loader2, ArrowDownToLine, ArrowUpFromLine, FlaskConical, Unplug, Scissors, GitBranch, Info } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { shortId } from "../lib/utils";
import { cn } from "../lib/utils";

const RISK_TONE: Record<string, any> = { NONE: "neutral", LOW: "info", MEDIUM: "warning", HIGH: "warning", CRITICAL: "danger" };

type Mode = "blast" | "upstream" | "whatif";
type WhatIfAction = "remove" | "isolate";

const MODES: { id: Mode; label: string; icon: any; hint: string }[] = [
  { id: "blast", label: "Blast radius", icon: ArrowDownToLine, hint: "Downstream dependency reach" },
  { id: "upstream", label: "Upstream", icon: ArrowUpFromLine, hint: "What depends on this entity" },
  { id: "whatif", label: "What-if", icon: FlaskConical, hint: "Simulate removal / isolation" },
];

export function Impact() {
  const [mode, setMode] = useState<Mode>("blast");
  const [wAction, setWAction] = useState<WhatIfAction>("remove");
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [entity, setEntity] = useState<any | null>(null);
  const [reach, setReach] = useState<any | null>(null);
  const [sim, setSim] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<any>(null);

  const search = async (value: string) => {
    setQ(value);
    if (!value.trim()) return setResults([]);
    try {
      const r = await apiFetch<any>(`/search?q=${encodeURIComponent(value.trim())}&limit=6`);
      setResults(r.nodes || []);
    } catch { setResults([]); }
  };

  const analyze = async (node: any, m: Mode = mode, action: WhatIfAction = wAction) => {
    setEntity(node); setResults([]); setQ(""); setLoading(true); setError(null); setReach(null); setSim(null);
    try {
      if (m === "whatif") {
        const s = await apiFetch<any>("/graph/what-if", { method: "POST", body: { canonical_id: node.id, action } });
        setSim(s);
      } else {
        const path = m === "upstream" ? "/graph/reverse-impact" : "/graph/blast-radius";
        const b = await apiFetch<any>(path, { method: "POST", body: { canonical_id: node.id, max_depth: 4 } });
        setReach(b);
      }
    } catch (e) { setError(e); } finally { setLoading(false); }
  };

  const switchMode = (m: Mode) => {
    setMode(m);
    if (entity) analyze(entity, m, wAction);
  };
  const switchAction = (a: WhatIfAction) => {
    setWAction(a);
    if (entity && mode === "whatif") analyze(entity, "whatif", a);
  };

  return (
    <Page>
      <PageHeader title="Impact" overline="Blast radius · upstream reach · what-if simulation" icon={<Radar size={18} />} />

      {/* Mode toggle */}
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex items-center gap-1 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-void)] p-1" data-testid="impact-mode-toggle">
          {MODES.map((m) => (
            <button
              key={m.id}
              data-testid={`impact-mode-${m.id}`}
              onClick={() => switchMode(m.id)}
              className={cn("group relative flex items-center gap-1.5 rounded-sm px-3 py-1.5 text-xs transition-all duration-200", mode === m.id ? "bg-[var(--accent)] text-black font-semibold shadow-[0_0_14px_-4px_var(--accent)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)]")}
            >
              <m.icon size={13} /> {m.label}
            </button>
          ))}
        </div>
        <span className="text-xs text-[var(--text-muted)]">{MODES.find((m) => m.id === mode)?.hint}</span>
      </div>

      <Card className="p-4">
        <Overline>Choose an entity</Overline>
        <div className="mt-2 flex flex-wrap items-end gap-3">
          <div className="relative max-w-md flex-1">
            <div className="flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 transition-colors focus-within:border-[var(--accent)] focus-within:shadow-[0_0_0_3px_var(--accent-ring)]">
              <Search size={15} className="text-[var(--text-muted)]" />
              <input data-testid="impact-search" value={q} onChange={(e) => search(e.target.value)} placeholder="Search for an entity to analyze…" className="h-9 w-full bg-transparent text-sm outline-none" />
            </div>
            {results.length > 0 && (
              <div className="absolute z-20 mt-1 w-full overflow-hidden rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-2xl">
                {results.map((r) => (
                  <button key={r.id} data-testid="impact-result" onClick={() => analyze(r)} className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left transition-colors hover:bg-[var(--bg-hover)]">
                    <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">{r.label}</span>
                    <span className="truncate text-xs">{r.properties?.name || r.properties?.title || shortId(r.id)}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
          {mode === "whatif" && (
            <div className="flex items-center gap-1 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-0.5" data-testid="whatif-action-toggle">
              {([["remove", Scissors], ["isolate", Unplug]] as const).map(([a, Icon]) => (
                <button key={a} data-testid={`whatif-action-${a}`} onClick={() => switchAction(a)} className={cn("flex items-center gap-1.5 rounded-[3px] px-2.5 py-1.5 text-xs capitalize transition-colors", wAction === a ? "bg-[var(--bg-hover)] text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]")}>
                  <Icon size={13} /> {a}
                </button>
              ))}
            </div>
          )}
        </div>
      </Card>

      {!entity && <EmptyState title="No entity selected" description={mode === "whatif" ? "Search and pick an entity to simulate its removal or isolation — no data is changed." : "Search and pick an entity to compute its dependency reach."} icon={<Radar size={22} />} />}
      {loading && <LoadingState label={mode === "whatif" ? "Running simulation" : "Computing dependency reach"} />}
      {error && <ErrorState problem={error} onRetry={() => entity && analyze(entity)} />}

      <AnimatePresence mode="wait">
        {entity && reach && mode !== "whatif" && (
          <motion.div key={`${mode}-${entity.id}`} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-4" data-testid="impact-result-panel">
            <Card className="p-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <Overline>{mode === "upstream" ? "Upstream of" : "Downstream of"}</Overline>
                  <Link to={`/entity/${encodeURIComponent(entity.id)}`} className="block font-heading text-lg font-semibold transition-colors hover:text-[var(--accent)]">
                    {entity.properties?.name || entity.properties?.title || shortId(entity.id)}
                  </Link>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2"><Overline>Risk</Overline><Badge tone={RISK_TONE[reach.risk] || "neutral"}><ShieldAlert size={11} /> {reach.risk ?? "N/A"}</Badge></div>
                  <div className="text-right"><Overline>Total affected</Overline><p className="font-heading text-2xl font-bold">{reach.total_affected ?? 0}</p></div>
                </div>
              </div>
            </Card>

            <div className="grid gap-4 md:grid-cols-2">
              <Card className="p-4">
                <Overline>Affected by depth</Overline>
                <div className="mt-3 flex items-end gap-2">
                  {reach.by_depth && Object.entries(reach.by_depth).map(([d, c]: any, i) => {
                    const max = Math.max(...Object.values<number>(reach.by_depth));
                    return (
                      <div key={d} className="flex flex-1 flex-col items-center gap-1">
                        <div className="flex h-28 w-full items-end">
                          <motion.div initial={{ height: 0 }} animate={{ height: `${(c / (max || 1)) * 100}%` }} transition={{ delay: i * 0.06, duration: 0.5, ease: "easeOut" }} className="w-full rounded-t-sm bg-gradient-to-t from-cyan-600 to-cyan-400" />
                        </div>
                        <span className="font-mono text-[10px]">{c}</span><span className="font-mono text-[9px] text-[var(--text-muted)]">d{d}</span>
                      </div>
                    );
                  })}
                </div>
              </Card>
              <Card className="p-4">
                <Overline>Affected by type</Overline>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {reach.by_type ? Object.entries(reach.by_type).map(([l, c]: any) => (
                    <span key={l} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2 py-1 font-mono text-[10px]">{l}: <strong>{c}</strong></span>
                  )) : <p className="text-sm text-[var(--text-muted)]">No breakdown available.</p>}
                </div>
              </Card>
            </div>
          </motion.div>
        )}

        {entity && sim && mode === "whatif" && (
          <motion.div key={`whatif-${entity.id}-${wAction}`} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="space-y-4" data-testid="whatif-result-panel">
            <div className="flex items-start gap-2 rounded-md border border-cyan-500/40 bg-cyan-500/10 px-3 py-2.5 text-xs text-cyan-200" data-testid="whatif-safe-banner">
              <Info size={15} className="mt-0.5 shrink-0" />
              <p><strong>Simulation only — nothing was changed.</strong> This models {wAction === "remove" ? "removing" : "isolating"} <span className="font-mono">{entity.properties?.name || shortId(entity.id)}</span> against a copy of the graph.</p>
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              {[
                { label: "Broken edges", value: sim.broken_edges, icon: Unplug, tone: "text-amber-300" },
                { label: "Affected neighbors", value: sim.affected_neighbors, icon: Radar, tone: "text-cyan-300" },
                { label: "Orphaned entities", value: sim.orphaned_entities, icon: Scissors, tone: "text-red-300" },
                { label: "Broken paths", value: sim.broken_paths, icon: GitBranch, tone: "text-purple-300" },
              ].map((s, i) => (
                <motion.div key={s.label} initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.05 }}>
                  <Card className="p-4">
                    <div className="flex items-center gap-2"><s.icon size={13} className={s.tone} /><Overline>{s.label}</Overline></div>
                    <p className="mt-1 font-heading text-2xl font-bold">{s.value ?? 0}</p>
                  </Card>
                </motion.div>
              ))}
            </div>

            <div className="grid gap-4 md:grid-cols-[1fr_1.4fr]">
              <Card className="p-4">
                <Overline>Component impact</Overline>
                <div className="mt-3 space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-[var(--text-muted)]">Graph splits apart</span>
                    <Badge tone={sim.component_split ? "danger" : "success"}>{sim.component_split ? "Yes — disconnects" : "No"}</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[var(--text-muted)]">New components formed</span>
                    <span className="font-heading text-lg font-bold">{sim.new_components ?? 0}</span>
                  </div>
                </div>
              </Card>
              <Card className="p-4">
                <Overline>Centrality changes (top neighbors)</Overline>
                {(sim.centrality_changes || []).length === 0 ? (
                  <p className="mt-2 text-sm text-[var(--text-muted)]">No measurable centrality change.</p>
                ) : (
                  <div className="mt-3 space-y-1.5">
                    {(sim.centrality_changes || []).slice(0, 6).map((c: any) => {
                      const delta = (c.degree_after ?? 0) - (c.degree_before ?? 0);
                      return (
                        <div key={c.canonical_id} className="flex items-center gap-2 rounded-sm bg-[var(--bg-void)] px-2 py-1.5 text-[11px]">
                          <Link to={`/entity/${encodeURIComponent(c.canonical_id)}`} className="flex-1 truncate font-mono hover:text-[var(--accent)]">{shortId(c.canonical_id)}</Link>
                          <span className="font-mono text-[var(--text-muted)]">{c.degree_before}</span>
                          <span className="text-[var(--text-muted)]">→</span>
                          <span className="font-mono">{c.degree_after}</span>
                          <Badge tone={delta < 0 ? "warning" : "neutral"}>{delta > 0 ? `+${delta}` : delta}</Badge>
                        </div>
                      );
                    })}
                  </div>
                )}
              </Card>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </Page>
  );
}

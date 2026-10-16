import { useState } from "react";
import { Link } from "react-router-dom";
import { Radar, Search, ShieldAlert, Loader2 } from "lucide-react";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { shortId } from "../lib/utils";

const RISK_TONE: Record<string, any> = { NONE: "neutral", LOW: "info", MEDIUM: "warning", HIGH: "warning", CRITICAL: "danger" };

export function Impact() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [entity, setEntity] = useState<any | null>(null);
  const [blast, setBlast] = useState<any | null>(null);
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

  const analyze = async (node: any) => {
    setEntity(node); setResults([]); setQ(""); setLoading(true); setError(null); setBlast(null);
    try {
      const b = await apiFetch<any>("/graph/blast-radius", { method: "POST", body: { canonical_id: node.id, max_depth: 4 } });
      setBlast(b);
    } catch (e) { setError(e); } finally { setLoading(false); }
  };

  return (
    <Page>
      <PageHeader title="Impact" overline="Blast radius & dependency reach" icon={<Radar size={18} />} />

      <Card className="p-4">
        <Overline>Choose an entity</Overline>
        <div className="relative mt-2 max-w-md">
          <div className="flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 focus-within:border-[var(--accent)]">
            <Search size={15} className="text-[var(--text-muted)]" />
            <input data-testid="impact-search" value={q} onChange={(e) => search(e.target.value)} placeholder="Search for an entity to analyze…" className="h-9 w-full bg-transparent text-sm outline-none" />
          </div>
          {results.length > 0 && (
            <div className="absolute z-20 mt-1 w-full overflow-hidden rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-xl">
              {results.map((r) => (
                <button key={r.id} data-testid="impact-result" onClick={() => analyze(r)} className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left transition-colors hover:bg-[var(--bg-hover)]">
                  <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">{r.label}</span>
                  <span className="truncate text-xs">{r.properties?.name || r.properties?.title || shortId(r.id)}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      </Card>

      {!entity && <EmptyState title="No entity selected" description="Search and pick an entity to compute its blast radius." icon={<Radar size={22} />} />}
      {loading && <LoadingState label="Computing blast radius" />}
      {error && <ErrorState problem={error} onRetry={() => entity && analyze(entity)} />}

      {entity && blast && (
        <div className="space-y-4" data-testid="impact-result-panel">
          <Card className="p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <Overline>Analyzing</Overline>
                <Link to={`/entity/${encodeURIComponent(entity.id)}`} className="block font-heading text-lg font-semibold hover:text-[var(--accent)]">
                  {entity.properties?.name || entity.properties?.title || shortId(entity.id)}
                </Link>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2"><Overline>Risk</Overline><Badge tone={RISK_TONE[blast.risk] || "neutral"}><ShieldAlert size={11} /> {blast.risk ?? "N/A"}</Badge></div>
                <div className="text-right"><Overline>Total affected</Overline><p className="font-heading text-2xl font-bold">{blast.total_affected ?? 0}</p></div>
              </div>
            </div>
          </Card>

          <div className="grid gap-4 md:grid-cols-2">
            <Card className="p-4">
              <Overline>Affected by depth</Overline>
              <div className="mt-3 flex items-end gap-2">
                {blast.by_depth && Object.entries(blast.by_depth).map(([d, c]: any) => {
                  const max = Math.max(...Object.values<number>(blast.by_depth));
                  return (
                    <div key={d} className="flex flex-1 flex-col items-center gap-1">
                      <div className="flex h-28 w-full items-end"><div className="w-full rounded-t-sm bg-[var(--accent)] transition-[height] duration-500" style={{ height: `${(c / (max || 1)) * 100}%` }} /></div>
                      <span className="font-mono text-[10px]">{c}</span><span className="font-mono text-[9px] text-[var(--text-muted)]">d{d}</span>
                    </div>
                  );
                })}
              </div>
            </Card>
            <Card className="p-4">
              <Overline>Affected by type</Overline>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {blast.by_type ? Object.entries(blast.by_type).map(([l, c]: any) => (
                  <span key={l} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2 py-1 font-mono text-[10px]">{l}: <strong>{c}</strong></span>
                )) : <p className="text-sm text-[var(--text-muted)]">No breakdown available.</p>}
              </div>
            </Card>
          </div>
        </div>
      )}
    </Page>
  );
}

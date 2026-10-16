import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Clock, Loader2, Play, TerminalSquare } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";
import { ErrorState } from "../components/ui/States";
import { ResultBanner } from "../components/ui/States";
import { shortId } from "../lib/utils";

const SAMPLES = [
  "MATCH (n) RETURN n LIMIT 25",
  "FIND Service WHERE domain = 'CODE'",
  "find all requirements",
];

export function Query() {
  const { session } = useAuth();
  const navigate = useNavigate();
  const [query, setQuery] = useState(SAMPLES[2]);
  const [result, setResult] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<any>(null);

  const history = useQuery({
    queryKey: [session?.tenant, "query-history"],
    queryFn: () => apiFetch<any>("/query/history"),
    retry: false,
  });
  const historyList: any[] = history.data?.history || history.data?.entries || (Array.isArray(history.data) ? history.data : []);

  const run = async () => {
    if (!query.trim()) return;
    setLoading(true); setError(null); setResult(null);
    try {
      const r = await apiFetch<any>("/query/eql", { method: "POST", body: { query: query.trim() } });
      setResult(r);
    } catch (e) { setError(e); } finally { setLoading(false); history.refetch(); }
  };

  const nodes: any[] = result?.nodes || result?.result?.nodes || [];

  return (
    <Page>
      <PageHeader title="Query" overline="Structured graph query (EQL)" icon={<TerminalSquare size={18} />} />

      <Card className="overflow-hidden">
        <textarea
          data-testid="query-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) run(); }}
          rows={4}
          spellCheck={false}
          className="w-full resize-none bg-transparent px-4 py-3.5 font-mono text-sm outline-none placeholder:text-[var(--text-muted)]"
          placeholder="Enter an EQL query…"
        />
        <div className="flex items-center justify-between border-t border-[var(--border-subtle)] px-3 py-2">
          <div className="flex flex-wrap gap-1.5">
            {SAMPLES.map((s) => (
              <button key={s} onClick={() => setQuery(s)} className="rounded-full border border-[var(--border-subtle)] px-2 py-0.5 font-mono text-[10px] text-[var(--text-muted)] transition-colors hover:border-[var(--border-strong)] hover:text-[var(--text-primary)]">{shortId(s).slice(0, 24)}</button>
            ))}
          </div>
          <button data-testid="query-run" onClick={run} disabled={loading || !query.trim()} className="flex items-center gap-2 rounded-sm bg-[var(--accent)] px-3.5 py-1.5 text-sm font-semibold text-black transition-colors hover:bg-[var(--accent-strong)] disabled:opacity-40">
            {loading ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />} Run
          </button>
        </div>
      </Card>

      {error && <ErrorState problem={error} onRetry={run} />}

      {result && (
        <Card data-testid="query-result">
          <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
            <h3 className="font-heading text-sm font-semibold">Result</h3>
            <Badge tone="accent">{nodes.length} rows</Badge>
          </div>
          <div className="p-3">
            <ResultBanner partial={result.partial} warnings={result.warnings} />
            {nodes.length === 0 ? (
              <p className="py-6 text-center text-sm text-[var(--text-muted)]">No rows returned.</p>
            ) : (
              <div className="max-h-[420px] divide-y divide-[var(--border-subtle)] overflow-y-auto">
                {nodes.slice(0, 100).map((n: any) => (
                  <button key={n.id} onClick={() => navigate(`/entity/${encodeURIComponent(n.id)}`)} className="flex w-full items-center gap-2.5 px-2 py-2 text-left transition-colors hover:bg-[var(--bg-hover)]">
                    <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">{n.label}</span>
                    <span className="truncate text-sm">{n.properties?.name || n.properties?.title || shortId(n.id)}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </Card>
      )}

      <Card>
        <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
          <Clock size={14} className="text-[var(--text-muted)]" />
          <h3 className="font-heading text-sm font-semibold">History</h3>
        </div>
        {historyList.length === 0 ? (
          <p className="p-5 text-center text-sm text-[var(--text-muted)]">No query history yet.</p>
        ) : (
          <div className="divide-y divide-[var(--border-subtle)]">
            {historyList.slice(0, 15).map((h, i) => (
              <button key={i} onClick={() => setQuery(h.query || h.text || "")} className="block w-full truncate px-4 py-2 text-left font-mono text-xs text-[var(--text-secondary)] transition-colors hover:bg-[var(--bg-hover)]">
                {h.query || h.text || JSON.stringify(h).slice(0, 80)}
              </button>
            ))}
          </div>
        )}
      </Card>
    </Page>
  );
}

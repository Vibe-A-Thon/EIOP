import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Crosshair,
  Filter,
  Layers,
  Loader2,
  Network,
  Search,
  Shrink,
  Waypoints,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { useShell } from "../lib/shellStore";
import { GraphCanvas, type GEdge, type GNode } from "../components/GraphCanvas";
import { ResultBanner, EmptyState, ErrorState } from "../components/ui/States";
import { ALL_FACT_CLASSES, FACT_META, factClassOf } from "../lib/factClass";
import { cn, shortId } from "../lib/utils";

const DOMAIN_COLORS: Record<string, string> = {
  META: "#64748b",
  WORK: "#06b6d4",
  CODE: "#3b82f6",
  CICD: "#8b5cf6",
  KNOWLEDGE: "#10b981",
  IDENTITY: "#f59e0b",
  AGENT: "#ec4899",
  OPS: "#ef4444",
  TEST: "#14b8a6",
  DESIGN: "#a855f7",
  INTEGRATION: "#0ea5e9",
  DECISION: "#f97316",
  PROCESS: "#22c55e",
  BUSINESS: "#eab308",
};
const domainColor = (d?: string) => DOMAIN_COLORS[d || ""] || "#64748b";

type Lens = "domain" | "fact";
const SEED = "urn:eoip:code:repo:demo";

export function GraphExplorer() {
  const { session } = useAuth();
  const { openInspector, inspectorEntityId } = useShell();

  const [nodes, setNodes] = useState<GNode[]>([]);
  const [edges, setEdges] = useState<GEdge[]>([]);
  const [meta, setMeta] = useState<{ partial?: boolean; warnings?: string[] }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);
  const [lens, setLens] = useState<Lens>("domain");
  const [hiddenFacts, setHiddenFacts] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<GNode[]>([]);
  const [searching, setSearching] = useState(false);

  const loadNeighborhood = useCallback(
    async (canonicalId: string, merge = false) => {
      setLoading(true);
      setError(null);
      try {
        const r = await apiFetch<any>("/neighborhood", {
          method: "POST",
          body: { canonical_id: canonicalId, max_depth: 2, result_limit: 120 },
        });
        setMeta({ partial: r.partial, warnings: r.warnings });
        if (merge) {
          setNodes((prev) => {
            const map = new Map(prev.map((n) => [n.id, n]));
            (r.nodes || []).forEach((n: GNode) => map.set(n.id, n));
            return [...map.values()];
          });
          setEdges((prev) => {
            const map = new Map(prev.map((e) => [e.id, e]));
            (r.edges || []).forEach((e: GEdge) => map.set(e.id, e));
            return [...map.values()];
          });
        } else {
          setNodes(r.nodes || []);
          setEdges(r.edges || []);
        }
      } catch (err) {
        setError(err);
        if (!merge) {
          setNodes([]);
          setEdges([]);
        }
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  // Auto-discover the most connected hub for a rich default view.
  const bootstrap = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const s = await apiFetch<any>("/search?q=demo&limit=50");
      const ids = (s.nodes || []).map((n: any) => n.id).slice(0, 50);
      if (ids.length === 0) throw new Error("empty");
      const metrics = await apiFetch<any>("/graph/metrics", {
        method: "POST",
        body: { canonical_ids: ids },
      });
      const hub = Object.entries(metrics).sort(
        (a: any, b: any) => (b[1].degree || 0) - (a[1].degree || 0),
      )[0]?.[0] as string;
      await loadNeighborhood(hub || ids[0]);
    } catch {
      await loadNeighborhood(SEED).catch((e) => setError(e));
    }
  }, [loadNeighborhood]);

  useEffect(() => {
    bootstrap().catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Seed search
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const ctrl = new AbortController();
    setSearching(true);
    const t = setTimeout(() => {
      apiFetch<any>(`/search?q=${encodeURIComponent(query.trim())}&limit=8`, { signal: ctrl.signal })
        .then((r) => setResults(r.nodes || []))
        .catch(() => setResults([]))
        .finally(() => setSearching(false));
    }, 200);
    return () => {
      ctrl.abort();
      clearTimeout(t);
    };
  }, [query]);

  const visibleEdges = useMemo(
    () => edges.filter((e) => !hiddenFacts.has(factClassOf(e.creation_status))),
    [edges, hiddenFacts],
  );

  const colorOf = useCallback(
    (n: GNode) => (lens === "domain" ? domainColor(n.domain) : "#475569"),
    [lens],
  );
  const edgeColorOf = useCallback(
    (e: GEdge) =>
      lens === "fact"
        ? getComputedStyle(document.documentElement)
            .getPropertyValue(FACT_META[factClassOf(e.creation_status)].color.replace("var(", "").replace(")", ""))
            .trim() || "#475569"
        : "#2a3748",
    [lens],
  );

  const activeDomains = useMemo(() => {
    const set = new Set<string>();
    nodes.forEach((n) => n.domain && set.add(n.domain));
    return [...set].sort();
  }, [nodes]);

  const toggleFact = (cls: string) =>
    setHiddenFacts((prev) => {
      const next = new Set(prev);
      next.has(cls) ? next.delete(cls) : next.add(cls);
      return next;
    });

  return (
    <div className="flex h-full flex-col">
      {/* Toolbar */}
      <div className="flex shrink-0 flex-wrap items-center gap-2 border-b border-[var(--border-subtle)] bg-[var(--bg-surface)] px-4 py-2.5">
        <div className="flex items-center gap-2">
          <Waypoints size={16} className="text-cyan-400" />
          <h1 className="font-heading text-sm font-semibold">Graph Explorer</h1>
        </div>

        {/* Seed search */}
        <div className="relative ml-2 w-64">
          <div className="flex items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-2.5 focus-within:border-[var(--accent)]">
            <Search size={14} className="text-[var(--text-muted)]" />
            <input
              data-testid="graph-seed-search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Find a seed entity…"
              className="h-8 w-full bg-transparent text-xs outline-none"
            />
            {searching && <Loader2 size={13} className="animate-spin text-[var(--text-muted)]" />}
          </div>
          {results.length > 0 && (
            <div className="absolute z-20 mt-1 max-h-72 w-80 overflow-y-auto rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-xl">
              {results.map((r) => (
                <button
                  key={r.id}
                  data-testid="graph-seed-result"
                  onClick={() => {
                    setQuery("");
                    setResults([]);
                    loadNeighborhood(r.id);
                  }}
                  className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left transition-colors hover:bg-[var(--bg-hover)]"
                >
                  <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">
                    {r.label}
                  </span>
                  <span className="truncate text-xs">
                    {r.properties?.name || r.properties?.title || shortId(r.id)}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Lens switcher */}
        <div className="ml-auto flex items-center gap-1 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-0.5">
          {(["domain", "fact"] as Lens[]).map((l) => (
            <button
              key={l}
              data-testid={`graph-lens-${l}`}
              onClick={() => setLens(l)}
              className={cn(
                "flex items-center gap-1.5 rounded-[3px] px-2.5 py-1 text-xs capitalize transition-colors",
                lens === l
                  ? "bg-[var(--bg-hover)] text-[var(--text-primary)]"
                  : "text-[var(--text-muted)] hover:text-[var(--text-primary)]",
              )}
            >
              {l === "domain" ? <Layers size={13} /> : <Network size={13} />}
              {l} lens
            </button>
          ))}
        </div>

        <button
          data-testid="graph-expand-selected"
          disabled={!inspectorEntityId}
          onClick={() => inspectorEntityId && loadNeighborhood(inspectorEntityId, true)}
          className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2.5 py-1 text-xs transition-colors hover:border-[var(--border-strong)] disabled:opacity-40"
        >
          <Crosshair size={13} /> Expand
        </button>
        <button
          data-testid="graph-reset"
          onClick={() => bootstrap()}
          className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2.5 py-1 text-xs transition-colors hover:border-[var(--border-strong)]"
        >
          <Shrink size={13} /> Reset
        </button>
      </div>

      {/* Canvas area */}
      <div className="relative min-h-0 flex-1 bg-[var(--bg-void)]">
        {loading && nodes.length === 0 ? (
          <div className="flex h-full items-center justify-center gap-2 text-sm text-[var(--text-muted)]">
            <Loader2 size={18} className="animate-spin" /> Loading subgraph…
          </div>
        ) : error && nodes.length === 0 ? (
          <ErrorState problem={error} onRetry={() => bootstrap()} />
        ) : nodes.length === 0 ? (
          <EmptyState
            title="No subgraph loaded"
            description="Search for a seed entity to render its neighborhood."
            icon={<Waypoints size={22} />}
          />
        ) : (
          <GraphCanvas
            nodes={nodes}
            edges={visibleEdges}
            colorOf={colorOf}
            edgeColorOf={edgeColorOf}
            selectedId={inspectorEntityId}
            onSelect={openInspector}
          />
        )}

        {loading && nodes.length > 0 && (
          <div className="absolute right-4 top-4 flex items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2.5 py-1.5 text-xs text-[var(--text-muted)]">
            <Loader2 size={13} className="animate-spin" /> Updating
          </div>
        )}

        {/* Stats chip */}
        <div className="absolute left-4 top-4 flex items-center gap-3 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)]/90 px-3 py-1.5 font-mono text-[11px] text-[var(--text-secondary)] backdrop-blur">
          <span>{nodes.length} nodes</span>
          <span className="text-[var(--text-muted)]">·</span>
          <span>{visibleEdges.length} edges</span>
        </div>

        {/* Partial banner */}
        {(meta.partial || (meta.warnings && meta.warnings.length > 0)) && (
          <div className="absolute bottom-4 left-4 right-4 max-w-md">
            <ResultBanner partial={meta.partial} warnings={meta.warnings} />
          </div>
        )}

        {/* Legend / filters */}
        <div className="absolute bottom-4 right-4 w-52 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-panel)]/95 p-3 backdrop-blur">
          {lens === "domain" ? (
            <>
              <div className="mb-2 flex items-center gap-1.5">
                <Layers size={12} className="text-[var(--text-muted)]" />
                <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
                  Domains
                </span>
              </div>
              <div className="grid max-h-40 grid-cols-1 gap-1 overflow-y-auto">
                {activeDomains.map((d) => (
                  <div key={d} className="flex items-center gap-2 text-xs">
                    <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: domainColor(d) }} />
                    <span className="text-[var(--text-secondary)]">{d}</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <>
              <div className="mb-2 flex items-center gap-1.5">
                <Filter size={12} className="text-[var(--text-muted)]" />
                <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
                  Fact classes
                </span>
              </div>
              <div className="space-y-1">
                {ALL_FACT_CLASSES.map((cls) => (
                  <button
                    key={cls}
                    data-testid={`graph-filter-${cls.toLowerCase()}`}
                    onClick={() => toggleFact(cls)}
                    className={cn(
                      "flex w-full items-center gap-2 rounded-[3px] px-1 py-0.5 text-left text-xs transition-opacity",
                      hiddenFacts.has(cls) ? "opacity-35" : "opacity-100",
                    )}
                  >
                    <span
                      className="h-2.5 w-2.5 rounded-full"
                      style={{ backgroundColor: `var(${FACT_META[cls].color.slice(4, -1)})` }}
                    />
                    <span className="text-[var(--text-secondary)]">{cls}</span>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

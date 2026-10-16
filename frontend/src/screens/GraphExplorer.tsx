import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Bookmark,
  BookmarkPlus,
  Crosshair,
  Download,
  Filter,
  Layers,
  Loader2,
  Network,
  Route as RouteIcon,
  Search,
  Shrink,
  Trash2,
  Upload,
  Waypoints,
  X,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { useShell } from "../lib/shellStore";
import { GraphCanvas, type GEdge, type GNode, type GraphCanvasHandle } from "../components/GraphCanvas";
import { ResultBanner, EmptyState, ErrorState } from "../components/ui/States";
import { ALL_FACT_CLASSES, FACT_META, factClassOf } from "../lib/factClass";
import { listViews, saveView, deleteView, exportViews, importViews, type SavedView } from "../lib/savedViews";
import { cn, shortId } from "../lib/utils";

const DOMAIN_COLORS: Record<string, string> = {
  META: "#64748b", WORK: "#06b6d4", CODE: "#3b82f6", CICD: "#8b5cf6",
  KNOWLEDGE: "#10b981", IDENTITY: "#f59e0b", AGENT: "#ec4899", OPS: "#ef4444",
  TEST: "#14b8a6", DESIGN: "#a855f7", INTEGRATION: "#0ea5e9", DECISION: "#f97316",
  PROCESS: "#22c55e", BUSINESS: "#eab308",
};
const domainColor = (d?: string) => DOMAIN_COLORS[(d || "").toUpperCase()] || "#64748b";
const domainFromId = (id: string) => (id.split(":")[2] || "").toUpperCase();

type Lens = "domain" | "fact";
type Mode = "explore" | "paths";
const SEED = "urn:eoip:code:repo:demo";

interface Picked {
  id: string;
  label: string;
}

/** Small inline entity search combobox. */
function EntityPicker({
  value,
  placeholder,
  testId,
  onPick,
}: {
  value: Picked | null;
  placeholder: string;
  testId: string;
  onPick: (p: Picked | null) => void;
}) {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!q.trim()) {
      setResults([]);
      return;
    }
    const ctrl = new AbortController();
    const t = setTimeout(() => {
      apiFetch<any>(`/search?q=${encodeURIComponent(q.trim())}&limit=6`, { signal: ctrl.signal })
        .then((r) => setResults(r.nodes || []))
        .catch(() => setResults([]));
    }, 200);
    return () => {
      ctrl.abort();
      clearTimeout(t);
    };
  }, [q]);

  if (value) {
    return (
      <div className="flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-panel)] px-2.5 py-1.5" data-testid={`${testId}-picked`}>
        <span className="truncate text-xs">{value.label}</span>
        <button onClick={() => onPick(null)} className="text-[var(--text-muted)] hover:text-[var(--text-primary)]">
          <X size={13} />
        </button>
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="flex items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-2.5 focus-within:border-[var(--accent)]">
        <Search size={13} className="text-[var(--text-muted)]" />
        <input
          data-testid={testId}
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setOpen(true);
          }}
          placeholder={placeholder}
          className="h-8 w-full bg-transparent text-xs outline-none"
        />
      </div>
      {open && results.length > 0 && (
        <div className="absolute z-20 mt-1 max-h-60 w-72 overflow-y-auto rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-xl">
          {results.map((r) => (
            <button
              key={r.id}
              onClick={() => {
                onPick({ id: r.id, label: r.properties?.name || r.properties?.title || shortId(r.id) });
                setQ("");
                setResults([]);
                setOpen(false);
              }}
              className="flex w-full items-center gap-2 rounded-sm px-2 py-1.5 text-left transition-colors hover:bg-[var(--bg-hover)]"
            >
              <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">
                {r.label}
              </span>
              <span className="truncate text-xs">{r.properties?.name || r.properties?.title || shortId(r.id)}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export function GraphExplorer() {
  const { session } = useAuth();
  const { openInspector, inspectorEntityId } = useShell();

  const [nodes, setNodes] = useState<GNode[]>([]);
  const [edges, setEdges] = useState<GEdge[]>([]);
  const [seeds, setSeeds] = useState<string[]>([]);
  const [meta, setMeta] = useState<{ partial?: boolean; warnings?: string[] }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);
  const [lens, setLens] = useState<Lens>("domain");
  const [mode, setMode] = useState<Mode>("explore");
  const [hiddenFacts, setHiddenFacts] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<GNode[]>([]);
  const [searching, setSearching] = useState(false);

  // Paths
  const [pathSource, setPathSource] = useState<Picked | null>(null);
  const [pathTarget, setPathTarget] = useState<Picked | null>(null);
  const [pathTargetB, setPathTargetB] = useState<Picked | null>(null);
  const [paths, setPaths] = useState<string[][]>([]);
  const [pathsB, setPathsB] = useState<string[][]>([]);
  const [pathLoading, setPathLoading] = useState(false);
  const [pathError, setPathError] = useState<string | null>(null);
  const [highlightNodes, setHighlightNodes] = useState<Set<string>>(new Set());
  const [highlightEdges, setHighlightEdges] = useState<Set<string>>(new Set());
  const canvasRef = useRef<GraphCanvasHandle>(null);

  // Saved views
  const [views, setViews] = useState<SavedView[]>([]);
  const [viewsOpen, setViewsOpen] = useState(false);
  const [newViewName, setNewViewName] = useState("");

  const principal = session?.principal.id || "anon";
  const tenant = session?.tenant || "default";
  const workspace = session?.workspace || "default";

  useEffect(() => {
    setViews(listViews(principal, tenant, workspace));
  }, [principal, tenant, workspace]);

  const loadNeighborhood = useCallback(async (canonicalId: string, merge = false) => {
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
        setSeeds((prev) => (prev.includes(canonicalId) ? prev : [...prev, canonicalId]));
      } else {
        setNodes(r.nodes || []);
        setEdges(r.edges || []);
        setSeeds([canonicalId]);
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
  }, []);

  const [labelFilter, setLabelFilter] = useState<string | null>(null);

  const bootstrap = useCallback(async () => {
    setMode("explore");
    setLoading(true);
    setError(null);
    try {
      const s = await apiFetch<any>("/search?q=demo&limit=50");
      const ids = (s.nodes || []).map((n: any) => n.id).slice(0, 50);
      if (ids.length === 0) throw new Error("empty");
      const metrics = await apiFetch<any>("/graph/metrics", { method: "POST", body: { canonical_ids: ids } });
      const hub = Object.entries(metrics).sort((a: any, b: any) => (b[1].degree || 0) - (a[1].degree || 0))[0]?.[0] as string;
      await loadNeighborhood(hub || ids[0]);
    } catch {
      await loadNeighborhood(SEED).catch((e) => setError(e));
    }
  }, [loadNeighborhood]);

  // Deep-link: /graph?label=Foo (from Meta-graph "Show instances") or /graph?seed=<id>.
  const seedByLabel = useCallback(async (label: string) => {
    setMode("explore");
    setLabelFilter(label);
    setLoading(true);
    setError(null);
    try {
      const r = await apiFetch<any>(`/search?label=${encodeURIComponent(label)}&limit=25`);
      const first = (r.nodes || [])[0];
      if (!first) { setNodes([]); setEdges([]); setSeeds([]); setLoading(false); return; }
      await loadNeighborhood(first.id);
    } catch (e) {
      setError(e); setLoading(false);
    }
  }, [loadNeighborhood]);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const label = params.get("label");
    const seed = params.get("seed");
    if (label) { seedByLabel(label).catch(() => {}); return; }
    if (seed) { loadNeighborhood(seed).catch((e) => setError(e)); return; }
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

  // Trace shortest paths (to one or two targets) and highlight on the neighborhood.
  const runPaths = async () => {
    if (!pathSource || !pathTarget) return;
    setPathLoading(true);
    setPathError(null);
    setPaths([]);
    setPathsB([]);
    setHighlightNodes(new Set());
    setHighlightEdges(new Set());
    try {
      const sp = (tid: string) =>
        apiFetch<any>("/graph/shortest-paths", {
          method: "POST",
          body: { source_id: pathSource.id, target_id: tid, max_paths: 8, max_length: 12 },
        }).then((r) => r.paths || []).catch(() => []);
      const nb = (cid: string) =>
        apiFetch<any>("/neighborhood", { method: "POST", body: { canonical_id: cid, max_depth: 1, result_limit: 80 } }).catch(() => ({ nodes: [], edges: [] }));

      const [foundA, foundB, srcNb, tgtNb, tgtBNb] = await Promise.all([
        sp(pathTarget.id),
        pathTargetB ? sp(pathTargetB.id) : Promise.resolve([] as string[][]),
        nb(pathSource.id),
        nb(pathTarget.id),
        pathTargetB ? nb(pathTargetB.id) : Promise.resolve({ nodes: [], edges: [] }),
      ]);
      setPaths(foundA);
      setPathsB(foundB);
      if (foundA.length === 0 && foundB.length === 0) {
        setPathError("No path found between these entities.");
        return;
      }

      const nodeMap = new Map<string, GNode>(nodes.map((n) => [n.id, n]));
      const edgeMap = new Map<string, GEdge>(edges.filter((e) => e.type !== "PATH").map((e) => [e.id, e]));
      [...(srcNb.nodes || []), ...(tgtNb.nodes || []), ...(tgtBNb.nodes || [])].forEach((n: GNode) => nodeMap.set(n.id, n));
      [...(srcNb.edges || []), ...(tgtNb.edges || []), ...(tgtBNb.edges || [])].forEach((e: GEdge) => edgeMap.set(e.id, e));

      const hiNodes = new Set<string>();
      const hiEdges = new Set<string>();
      const addPaths = (list: string[][], tag: string) =>
        list.forEach((p, pi) => {
          p.forEach((id, idx) => {
            hiNodes.add(id);
            if (!nodeMap.has(id)) nodeMap.set(id, { id, label: domainFromId(id), domain: domainFromId(id), properties: {} });
            if (idx > 0) {
              const eid = `path:${tag}:${pi}:${idx}`;
              edgeMap.set(eid, { id: eid, from_id: p[idx - 1], to_id: id, type: "PATH" });
              hiEdges.add(eid);
            }
          });
        });
      addPaths(foundA, "a");
      addPaths(foundB, "b");
      setNodes([...nodeMap.values()]);
      setEdges([...edgeMap.values()]);
      setHighlightNodes(hiNodes);
      setHighlightEdges(hiEdges);
      setMeta({});
    } catch (err: any) {
      setPathError(err?.problem?.detail || err?.message || "Path query failed");
    } finally {
      setPathLoading(false);
    }
  };

  const clearPaths = () => {
    setPaths([]);
    setPathsB([]);
    setPathError(null);
    setHighlightNodes(new Set());
    setHighlightEdges(new Set());
    setEdges((prev) => prev.filter((e) => e.type !== "PATH"));
  };

  // Overlap of path node-sets between the two targets (for compare).
  const compare = useMemo(() => {
    if (pathsB.length === 0) return null;
    const setA = new Set(paths.flat());
    const setB = new Set(pathsB.flat());
    let shared = 0;
    setA.forEach((id) => setB.has(id) && shared++);
    const minHops = (l: string[][]) => (l.length ? Math.min(...l.map((p) => p.length - 1)) : 0);
    return { a: { paths: paths.length, minHops: minHops(paths), reach: setA.size }, b: { paths: pathsB.length, minHops: minHops(pathsB), reach: setB.size }, shared };
  }, [paths, pathsB]);

  const visibleEdges = useMemo(
    () => edges.filter((e) => e.type === "PATH" || !hiddenFacts.has(factClassOf(e.creation_status))),
    [edges, hiddenFacts],
  );

  const colorOf = useCallback(
    (n: GNode) => (lens === "domain" ? domainColor(n.domain) : "#475569"),
    [lens],
  );
  const edgeColorOf = useCallback(
    (e: GEdge) =>
      lens === "fact"
        ? getComputedStyle(document.documentElement).getPropertyValue(FACT_META[factClassOf(e.creation_status)].color.slice(4, -1)).trim() || "#475569"
        : "#2a3748",
    [lens],
  );

  const activeDomains = useMemo(() => {
    const set = new Set<string>();
    nodes.forEach((n) => n.domain && set.add(n.domain.toUpperCase()));
    return [...set].sort();
  }, [nodes]);

  const toggleFact = (cls: string) =>
    setHiddenFacts((prev) => {
      const next = new Set(prev);
      next.has(cls) ? next.delete(cls) : next.add(cls);
      return next;
    });

  const handleSaveView = () => {
    const name = newViewName.trim() || `View ${views.length + 1}`;
    const next = saveView(principal, tenant, workspace, {
      name,
      seeds,
      lens,
      hiddenFacts: [...hiddenFacts],
      thumbnail: canvasRef.current?.getThumbnail(),
    });
    setViews(next);
    setNewViewName("");
  };

  const loadView = async (v: SavedView) => {
    setMode("explore");
    setViewsOpen(false);
    clearPaths();
    setLens(v.lens);
    setHiddenFacts(new Set(v.hiddenFacts));
    if (v.seeds.length === 0) return;
    await loadNeighborhood(v.seeds[0], false);
    for (const s of v.seeds.slice(1)) await loadNeighborhood(s, true);
  };

  const handleExportViews = () => {
    const blob = new Blob([exportViews(views)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `kgf-graph-views-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImportViews = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        setViews(importViews(principal, tenant, workspace, String(reader.result)));
      } catch {
        /* ignore invalid file */
      }
    };
    reader.readAsText(file);
    e.target.value = "";
  };

  return (
    <div className="flex h-full flex-col">
      {/* Toolbar */}
      <div className="flex shrink-0 flex-wrap items-center gap-2 border-b border-[var(--border-subtle)] bg-[var(--bg-surface)] px-4 py-2.5">
        <div className="flex items-center gap-2">
          <Waypoints size={16} className="text-cyan-400" />
          <h1 className="font-heading text-sm font-semibold">Graph Explorer</h1>
        </div>

        {/* Mode */}
        <div className="ml-2 flex items-center gap-1 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-0.5">
          {([
            { id: "explore", label: "Explore", icon: Waypoints },
            { id: "paths", label: "Impact paths", icon: RouteIcon },
          ] as const).map((m) => (
            <button
              key={m.id}
              data-testid={`graph-mode-${m.id}`}
              onClick={() => {
                setMode(m.id);
                if (m.id === "explore") clearPaths();
              }}
              className={cn(
                "flex items-center gap-1.5 rounded-[3px] px-2.5 py-1 text-xs transition-colors",
                mode === m.id ? "bg-[var(--bg-hover)] text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]",
              )}
            >
              <m.icon size={13} /> {m.label}
            </button>
          ))}
        </div>

        {mode === "explore" && (
          <div className="relative w-56">
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
            {labelFilter && (
              <div className="absolute -bottom-7 left-0 flex items-center gap-1 rounded-full border border-[var(--accent)]/40 bg-[var(--accent)]/10 px-2 py-0.5 text-[10px] text-cyan-300" data-testid="graph-label-filter">
                <Filter size={10} /> label: {labelFilter}
                <button onClick={() => { setLabelFilter(null); bootstrap(); }} className="ml-0.5 hover:text-white"><X size={11} /></button>
              </div>
            )}
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
                    <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase text-[var(--text-muted)]">{r.label}</span>
                    <span className="truncate text-xs">{r.properties?.name || r.properties?.title || shortId(r.id)}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Path pickers */}
        {mode === "paths" && (
          <div className="flex flex-1 flex-wrap items-center gap-2">
            <EntityPicker value={pathSource} placeholder="Source entity…" testId="path-source" onPick={setPathSource} />
            <RouteIcon size={14} className="text-[var(--text-muted)]" />
            <EntityPicker value={pathTarget} placeholder="Target A…" testId="path-target" onPick={setPathTarget} />
            <span className="font-mono text-[10px] text-[var(--text-muted)]">vs</span>
            <EntityPicker value={pathTargetB} placeholder="Target B (compare)…" testId="path-target-b" onPick={setPathTargetB} />
            <button
              data-testid="path-run"
              onClick={runPaths}
              disabled={!pathSource || !pathTarget || pathLoading}
              className="flex items-center gap-1.5 rounded-sm bg-[var(--accent)] px-3 py-1.5 text-xs font-semibold text-black transition-colors hover:bg-[var(--accent-strong)] disabled:opacity-40"
            >
              {pathLoading ? <Loader2 size={13} className="animate-spin" /> : <RouteIcon size={13} />} {pathTargetB ? "Compare" : "Trace paths"}
            </button>
          </div>
        )}

        {/* Lens switcher */}
        {mode === "explore" && (
          <div className="ml-auto flex items-center gap-1 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-0.5">
            {(["domain", "fact"] as Lens[]).map((l) => (
              <button
                key={l}
                data-testid={`graph-lens-${l}`}
                onClick={() => setLens(l)}
                className={cn(
                  "flex items-center gap-1.5 rounded-[3px] px-2.5 py-1 text-xs capitalize transition-colors",
                  lens === l ? "bg-[var(--bg-hover)] text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]",
                )}
              >
                {l === "domain" ? <Layers size={13} /> : <Network size={13} />} {l} lens
              </button>
            ))}
          </div>
        )}

        {/* Saved views */}
        <div className={cn("relative", mode === "paths" && "ml-auto")}>
          <button
            data-testid="graph-views-trigger"
            onClick={() => setViewsOpen((o) => !o)}
            className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2.5 py-1 text-xs transition-colors hover:border-[var(--border-strong)]"
          >
            <Bookmark size={13} /> Views {views.length > 0 && <span className="text-[var(--text-muted)]">({views.length})</span>}
          </button>
          {viewsOpen && (
            <>
              <div className="fixed inset-0 z-30" onClick={() => setViewsOpen(false)} />
              <div className="absolute right-0 z-40 mt-1 w-72 animate-fade-in rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-2 shadow-xl">
                <div className="mb-2 flex items-center gap-1.5">
                  <input
                    data-testid="graph-view-name"
                    value={newViewName}
                    onChange={(e) => setNewViewName(e.target.value)}
                    placeholder="Name this view"
                    className="h-8 w-full rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]"
                  />
                  <button
                    data-testid="graph-view-save"
                    onClick={handleSaveView}
                    disabled={seeds.length === 0}
                    className="flex shrink-0 items-center gap-1 rounded-sm bg-[var(--accent)] px-2 py-1.5 text-xs font-semibold text-black transition-colors hover:bg-[var(--accent-strong)] disabled:opacity-40"
                  >
                    <BookmarkPlus size={13} /> Save
                  </button>
                </div>
                <div className="max-h-56 space-y-0.5 overflow-y-auto">
                  {views.length === 0 ? (
                    <p className="px-2 py-3 text-center text-xs text-[var(--text-muted)]">No saved views yet.</p>
                  ) : (
                    views.map((v) => (
                      <div key={v.id} className="group flex items-center gap-2 rounded-sm px-2 py-1.5 hover:bg-[var(--bg-hover)]">
                        <button
                          data-testid="graph-view-load"
                          onClick={() => loadView(v)}
                          className="flex min-w-0 flex-1 items-center gap-2 text-left"
                        >
                          {v.thumbnail ? (
                            <img src={v.thumbnail} alt="" className="h-9 w-16 shrink-0 rounded-sm border border-[var(--border-subtle)] object-cover" />
                          ) : (
                            <span className="grid h-9 w-16 shrink-0 place-items-center rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] text-[var(--text-muted)]">
                              <Bookmark size={13} />
                            </span>
                          )}
                          <span className="min-w-0 flex-1">
                            <span className="block truncate text-xs font-medium">{v.name}</span>
                            <span className="block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                              {v.seeds.length} seed{v.seeds.length === 1 ? "" : "s"} · {v.lens} lens
                            </span>
                          </span>
                        </button>
                        <button
                          onClick={() => setViews(deleteView(principal, tenant, workspace, v.id))}
                          className="text-[var(--text-muted)] opacity-0 transition-opacity hover:text-red-400 group-hover:opacity-100"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    ))
                  )}
                </div>
                <div className="mt-2 flex items-center gap-1.5 border-t border-[var(--border-subtle)] pt-2">
                  <button
                    data-testid="graph-view-export"
                    onClick={handleExportViews}
                    disabled={views.length === 0}
                    className="flex flex-1 items-center justify-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2 py-1.5 text-xs transition-colors hover:border-[var(--border-strong)] disabled:opacity-40"
                  >
                    <Download size={12} /> Export
                  </button>
                  <label
                    data-testid="graph-view-import"
                    className="flex flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2 py-1.5 text-xs transition-colors hover:border-[var(--border-strong)]"
                  >
                    <Upload size={12} /> Import
                    <input type="file" accept="application/json" className="hidden" onChange={handleImportViews} />
                  </label>
                </div>
                <p className="mt-2 px-1 font-mono text-[9px] text-[var(--text-muted)]">
                  Saved on this device only. Export to share with teammates.
                </p>
              </div>
            </>
          )}
        </div>

        {mode === "explore" && (
          <>
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
          </>
        )}
      </div>

      {/* Canvas */}
      <div className="relative min-h-0 flex-1 bg-[var(--bg-void)]">
        {loading && nodes.length === 0 ? (
          <div className="flex h-full items-center justify-center gap-2 text-sm text-[var(--text-muted)]">
            <Loader2 size={18} className="animate-spin" /> Loading subgraph…
          </div>
        ) : error && nodes.length === 0 ? (
          <ErrorState problem={error} onRetry={() => bootstrap()} />
        ) : nodes.length === 0 ? (
          <EmptyState
            title={mode === "paths" ? "No paths traced yet" : "No subgraph loaded"}
            description={mode === "paths" ? "Pick a source and target entity, then trace the shortest paths between them." : "Search for a seed entity to render its neighborhood."}
            icon={mode === "paths" ? <RouteIcon size={22} /> : <Waypoints size={22} />}
          />
        ) : (
          <GraphCanvas
            ref={canvasRef}
            nodes={nodes}
            edges={visibleEdges}
            colorOf={colorOf}
            edgeColorOf={edgeColorOf}
            selectedId={mode === "paths" ? pathSource?.id : inspectorEntityId}
            highlightNodes={mode === "paths" ? highlightNodes : undefined}
            highlightEdges={mode === "paths" ? highlightEdges : undefined}
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
          {mode === "paths" && paths.length > 0 && (
            <>
              <span className="text-[var(--text-muted)]">·</span>
              <span className="text-cyan-400">{paths.length} paths</span>
            </>
          )}
          {mode === "explore" && meta.partial && (
            <>
              <span className="text-[var(--text-muted)]">·</span>
              <span className="text-amber-400" title="Server returned a depth/limit-bounded subgraph">bounded</span>
            </>
          )}
        </div>

        {/* Path compare summary */}
        {mode === "paths" && compare && (
          <div className="absolute right-4 top-16 w-64 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-panel)]/95 p-3 backdrop-blur" data-testid="path-compare">
            <div className="mb-2 font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Blast surface compare</div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="rounded-sm border border-cyan-500/40 bg-cyan-500/10 p-2">
                <p className="font-mono text-[9px] uppercase text-cyan-300">Target A</p>
                <p className="mt-0.5"><strong className="font-heading text-sm">{compare.a.paths}</strong> paths</p>
                <p className="text-[var(--text-muted)]">min {compare.a.minHops} hops · {compare.a.reach} nodes</p>
              </div>
              <div className="rounded-sm border border-fuchsia-500/40 bg-fuchsia-500/10 p-2">
                <p className="font-mono text-[9px] uppercase text-fuchsia-300">Target B</p>
                <p className="mt-0.5"><strong className="font-heading text-sm">{compare.b.paths}</strong> paths</p>
                <p className="text-[var(--text-muted)]">min {compare.b.minHops} hops · {compare.b.reach} nodes</p>
              </div>
            </div>
            <p className="mt-2 text-xs text-[var(--text-secondary)]">
              <strong className="font-heading">{compare.shared}</strong> shared node{compare.shared === 1 ? "" : "s"} on both surfaces
            </p>
          </div>
        )}

        {mode === "explore" && meta.warnings && meta.warnings.length > 0 && (
          <div className="absolute bottom-4 left-4 right-4 max-w-md">
            <ResultBanner warnings={meta.warnings} />
          </div>
        )}

        {/* Paths list */}
        {mode === "paths" && (paths.length > 0 || pathError) && (
          <div className="absolute bottom-4 left-4 max-h-64 w-96 overflow-y-auto rounded-md border border-[var(--border-subtle)] bg-[var(--bg-panel)]/95 p-3 backdrop-blur" data-testid="paths-list">
            {pathError ? (
              <p className="text-xs text-amber-300">{pathError}</p>
            ) : (
              <>
                <div className="mb-2 flex items-center gap-1.5">
                  <RouteIcon size={12} className="text-cyan-400" />
                  <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
                    {paths.length} shortest path{paths.length === 1 ? "" : "s"}
                  </span>
                </div>
                <div className="space-y-2">
                  {paths.map((p, i) => (
                    <div key={i} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-2">
                      <p className="mb-1 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                        Path {i + 1} · {p.length} hops
                      </p>
                      <div className="flex flex-wrap items-center gap-1">
                        {p.map((id, idx) => (
                          <span key={idx} className="flex items-center gap-1">
                            <button
                              onClick={() => openInspector(id)}
                              className="rounded-sm bg-[var(--bg-hover)] px-1.5 py-0.5 font-mono text-[10px] text-[var(--text-secondary)] transition-colors hover:text-[var(--accent)]"
                            >
                              {shortId(id)}
                            </button>
                            {idx < p.length - 1 && <span className="text-[var(--text-muted)]">→</span>}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}

        {/* Legend / filters */}
        {mode === "explore" && (
          <div className="absolute bottom-4 right-4 w-52 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-panel)]/95 p-3 backdrop-blur">
            {lens === "domain" ? (
              <>
                <div className="mb-2 flex items-center gap-1.5">
                  <Layers size={12} className="text-[var(--text-muted)]" />
                  <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Domains</span>
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
                  <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Fact classes</span>
                </div>
                <div className="space-y-1">
                  {ALL_FACT_CLASSES.map((cls) => (
                    <button
                      key={cls}
                      data-testid={`graph-filter-${cls.toLowerCase()}`}
                      onClick={() => toggleFact(cls)}
                      className={cn("flex w-full items-center gap-2 rounded-[3px] px-1 py-0.5 text-left text-xs transition-opacity", hiddenFacts.has(cls) ? "opacity-35" : "opacity-100")}
                    >
                      <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: `var(${FACT_META[cls].color.slice(4, -1)})` }} />
                      <span className="text-[var(--text-secondary)]">{cls}</span>
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

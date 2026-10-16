import { useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ChevronRight, Hash, KeyRound, Layers, Search, Shapes, TriangleAlert, Waypoints } from "lucide-react";
import { motion } from "framer-motion";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { ErrorState, LoadingState } from "../components/ui/States";
import { GraphCanvas, type GEdge, type GNode } from "../components/GraphCanvas";
import { cn, formatNumber } from "../lib/utils";

const DOMAIN_COLORS: Record<string, string> = {
  META: "#64748b", WORK: "#06b6d4", CODE: "#3b82f6", CICD: "#8b5cf6",
  KNOWLEDGE: "#10b981", IDENTITY: "#f59e0b", AGENT: "#ec4899", OPS: "#ef4444",
  TEST: "#14b8a6", DESIGN: "#a855f7", INTEGRATION: "#0ea5e9", DECISION: "#f97316",
  PROCESS: "#22c55e", BUSINESS: "#eab308",
};
const domainColor = (d?: string) => DOMAIN_COLORS[(d || "").toUpperCase()] || "#64748b";

type Show = "counts" | "properties" | "indexes";

interface TypeNode {
  label: string;
  domain: string;
  required: string[];
  optional: string[];
  instanceCount: number;
  indexes: { name: string; type: string; fields: string[] }[];
}

export function MetaGraph() {
  const { session } = useAuth();
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [show, setShow] = useState<Show>("counts");
  const [selected, setSelected] = useState<string | null>(null);
  const listRef = useRef<HTMLDivElement>(null);

  const schema = useQuery({ queryKey: [session?.tenant, "schema"], queryFn: () => apiFetch<any>("/graph/schema"), staleTime: 300_000 });
  const stats = useQuery({ queryKey: [session?.tenant, "admin-stats-meta"], queryFn: () => apiFetch<any>("/admin/stats"), retry: false });

  const schemaFetchedAt = schema.dataUpdatedAt ? new Date(schema.dataUpdatedAt) : null;
  const statsFetchedAt = stats.dataUpdatedAt ? new Date(stats.dataUpdatedAt) : null;

  const types = useMemo<TypeNode[]>(() => {
    const vl = schema.data?.vertex_labels || {};
    const idx: any[] = schema.data?.indexes || [];
    return Object.entries(vl).map(([label, meta]: any) => ({
      label,
      domain: (meta.domain || "META").toUpperCase(),
      required: meta.required_properties || [],
      optional: meta.optional_properties || [],
      instanceCount: meta.instance_count || 0,
      indexes: idx.filter((i) => i.label === label).map((i) => ({ name: i.name, type: i.type, fields: i.fields || [] })),
    }));
  }, [schema.data]);

  // A03: compare schema instance_count vs admin/stats label counts.
  const mismatches = useMemo(() => {
    const statLabels: Record<string, number> = stats.data?.labels || {};
    if (!statLabels || Object.keys(statLabels).length === 0) return [];
    const out: { label: string; schema: number; stats: number }[] = [];
    types.forEach((t) => {
      const s = statLabels[t.label];
      if (s !== undefined && s !== t.instanceCount) out.push({ label: t.label, schema: t.instanceCount, stats: s });
    });
    return out;
  }, [types, stats.data]);

  const ordered = useMemo(() => {
    const filtered = types.filter((t) => t.label.toLowerCase().includes(q.toLowerCase()));
    return filtered.sort((a, b) => (a.domain === b.domain ? a.label.localeCompare(b.label) : a.domain.localeCompare(b.domain)));
  }, [types, q]);

  const grouped = useMemo(() => {
    const m = new Map<string, TypeNode[]>();
    ordered.forEach((t) => { if (!m.has(t.domain)) m.set(t.domain, []); m.get(t.domain)!.push(t); });
    return [...m.entries()];
  }, [ordered]);

  // Graph model: vertex labels as nodes, edge labels collapsed to one edge per (src,tgt) pair.
  const { nodes, edges } = useMemo(() => {
    const present = new Set(ordered.map((t) => t.label));
    const gnodes: GNode[] = ordered.map((t) => ({ id: t.label, label: t.label, domain: t.domain, properties: { name: t.label } }));
    const el = schema.data?.edge_labels || {};
    const pairMap = new Map<string, { from: string; to: string; types: Set<string> }>();
    Object.entries(el).forEach(([etype, meta]: any) => {
      const srcs: string[] = meta.source_labels?.length ? meta.source_labels : [...present];
      const tgts: string[] = meta.target_labels?.length ? meta.target_labels : [...present];
      srcs.forEach((s) => tgts.forEach((t) => {
        if (!present.has(s) || !present.has(t)) return;
        const key = `${s}→${t}`;
        if (!pairMap.has(key)) pairMap.set(key, { from: s, to: t, types: new Set() });
        pairMap.get(key)!.types.add(etype);
      }));
    });
    const gedges: GEdge[] = [...pairMap.entries()].map(([key, v]) => ({ id: key, from_id: v.from, to_id: v.to, type: [...v.types].join(", ") }));
    return { nodes: gnodes, edges: gedges };
  }, [ordered, schema.data]);

  const selectedType = useMemo(() => types.find((t) => t.label === selected) || null, [types, selected]);

  // A04: keyboard navigation across type nodes in domain order.
  const focusIndex = selected ? ordered.findIndex((t) => t.label === selected) : -1;
  const onKeyDown = (e: React.KeyboardEvent) => {
    if (ordered.length === 0) return;
    if (e.key === "ArrowDown" || e.key === "ArrowRight") {
      e.preventDefault();
      const next = Math.min(ordered.length - 1, focusIndex + 1);
      setSelected(ordered[next < 0 ? 0 : next].label);
    } else if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
      e.preventDefault();
      const prev = focusIndex <= 0 ? 0 : focusIndex - 1;
      setSelected(ordered[prev].label);
    }
  };

  useEffect(() => {
    if (!selected || !listRef.current) return;
    const el = listRef.current.querySelector(`[data-type="${CSS.escape(selected)}"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [selected]);

  if (schema.isLoading) return <LoadingState label="Loading ontology meta-graph" />;
  if (schema.error) return <ErrorState problem={schema.error} onRetry={schema.refetch} />;

  return (
    <Page>
      <PageHeader
        title="Meta-graph"
        overline={`${nodes.length} types · ${edges.length} relationships · ontology v${schema.data?.ontology_version ?? "—"}`}
        icon={<Shapes size={18} />}
      />

      {mismatches.length > 0 && (
        <div data-testid="metagraph-mismatch-warning" className="flex items-start gap-2 rounded-md border border-amber-500/40 bg-amber-500/10 px-3 py-2.5 text-xs text-amber-200">
          <TriangleAlert size={15} className="mt-0.5 shrink-0" />
          <div>
            <p className="font-medium">Instance counts differ between two sources for {mismatches.length} type(s).</p>
            <p className="mt-0.5 text-amber-200/80">
              Schema (<code className="font-mono">/graph/schema</code>, fetched {schemaFetchedAt?.toLocaleTimeString() ?? "—"}) vs
              live stats (<code className="font-mono">/admin/stats</code>, fetched {statsFetchedAt?.toLocaleTimeString() ?? "—"}):{" "}
              {mismatches.slice(0, 5).map((m) => `${m.label} ${m.schema}≠${m.stats}`).join(" · ")}
              {mismatches.length > 5 ? " …" : ""}
            </p>
          </div>
        </div>
      )}

      <Card className="flex flex-wrap items-center gap-3 p-3">
        <div className="flex items-center gap-2 text-xs text-[var(--text-muted)]">
          <Layers size={13} /> Layout: hierarchical (domain → label)
        </div>
        <div className="flex items-center gap-1 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-0.5">
          {(["counts", "properties", "indexes"] as Show[]).map((s) => (
            <button
              key={s}
              data-testid={`metagraph-show-${s}`}
              onClick={() => setShow(s)}
              className={cn("rounded-[3px] px-2.5 py-1 text-[11px] capitalize transition-colors", show === s ? "bg-[var(--bg-hover)] text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]")}
            >
              {s}
            </button>
          ))}
        </div>
        <div className="flex min-w-[200px] flex-1 items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-2.5">
          <Search size={14} className="text-[var(--text-muted)]" />
          <input data-testid="metagraph-search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search type…" className="h-8 w-full bg-transparent text-xs outline-none" />
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-[260px_1fr_300px]">
        {/* Types tree — keyboard navigable (A04) */}
        <Card className="overflow-hidden">
          <div className="border-b border-[var(--border-subtle)] px-3 py-2"><Overline>Types ({ordered.length})</Overline></div>
          <div
            ref={listRef}
            tabIndex={0}
            role="listbox"
            aria-label="Vertex types in domain order"
            onKeyDown={onKeyDown}
            data-testid="metagraph-types-list"
            className="max-h-[560px] overflow-y-auto outline-none focus-visible:ring-1 focus-visible:ring-[var(--accent)]"
          >
            {grouped.map(([domain, items]) => (
              <div key={domain}>
                <div className="sticky top-0 flex items-center gap-1.5 bg-[var(--bg-panel)] px-3 py-1.5">
                  <span className="h-2 w-2 rounded-full" style={{ backgroundColor: domainColor(domain) }} />
                  <span className="font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">{domain}</span>
                </div>
                {items.map((t) => (
                  <button
                    key={t.label}
                    data-type={t.label}
                    data-testid="metagraph-type-item"
                    role="option"
                    aria-selected={selected === t.label}
                    onClick={() => setSelected(t.label)}
                    className={cn("flex w-full items-center justify-between gap-2 px-3 py-1.5 text-left text-xs transition-colors", selected === t.label ? "bg-[var(--accent)]/15 text-[var(--text-primary)]" : "hover:bg-[var(--bg-hover)] text-[var(--text-secondary)]")}
                  >
                    <span className="truncate">{t.label}</span>
                    <span className="font-mono text-[10px] text-[var(--text-muted)]">{formatNumber(t.instanceCount)}</span>
                  </button>
                ))}
              </div>
            ))}
          </div>
        </Card>

        {/* Canvas */}
        <Card className="relative h-[600px] overflow-hidden">
          {nodes.length === 0 ? (
            <div className="flex h-full items-center justify-center text-sm text-[var(--text-muted)]">No types match the filter.</div>
          ) : (
            <GraphCanvas
              nodes={nodes}
              edges={edges}
              selectedId={selected}
              colorOf={(n) => domainColor(n.domain)}
              edgeColorOf={() => "#2a3748"}
              onSelect={(id) => setSelected(id)}
            />
          )}
        </Card>

        {/* Inspector */}
        <Card className="overflow-hidden">
          <div className="border-b border-[var(--border-subtle)] px-3 py-2"><Overline>Selected type</Overline></div>
          {!selectedType ? (
            <div className="px-4 py-10 text-center text-xs text-[var(--text-muted)]">Select a type to inspect its properties, indexes and instances.</div>
          ) : (
            <motion.div key={selectedType.label} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.18 }} className="space-y-3 p-3" data-testid="metagraph-inspector">
              <div>
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: domainColor(selectedType.domain) }} />
                  <h3 className="font-heading text-base font-semibold">{selectedType.label}</h3>
                </div>
                <div className="mt-1 flex items-center gap-2">
                  <Badge tone="neutral">{selectedType.domain}</Badge>
                  <span className="flex items-center gap-1 font-mono text-[10px] text-[var(--text-muted)]"><Hash size={10} /> {formatNumber(selectedType.instanceCount)} instances</span>
                </div>
              </div>

              <div>
                <Overline>Required properties</Overline>
                <div className="mt-1 flex flex-wrap gap-1">
                  {selectedType.required.length ? selectedType.required.map((p) => <span key={p} className="rounded-sm border border-[var(--border-strong)] bg-[var(--bg-panel)] px-1.5 py-0.5 font-mono text-[10px]">{p}</span>) : <span className="text-[11px] text-[var(--text-muted)]">None</span>}
                </div>
              </div>

              <div>
                <Overline>Optional properties</Overline>
                <div className="mt-1 flex flex-wrap gap-1">
                  {selectedType.optional.length ? selectedType.optional.map((p) => <span key={p} className="rounded-sm border border-[var(--border-subtle)] px-1.5 py-0.5 font-mono text-[10px] text-[var(--text-secondary)]">{p}</span>) : <span className="text-[11px] text-[var(--text-muted)]">None</span>}
                </div>
              </div>

              <div>
                <Overline>Indexes</Overline>
                {selectedType.indexes.length ? (
                  <div className="mt-1 space-y-1">
                    {selectedType.indexes.map((i) => (
                      <div key={i.name} className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2 py-1 text-[10px]">
                        <KeyRound size={10} className="text-[var(--text-muted)]" />
                        <span className="font-mono">{i.name}</span>
                        <Badge tone="info" className="ml-auto">{i.type}</Badge>
                      </div>
                    ))}
                  </div>
                ) : <p className="mt-1 text-[11px] text-[var(--text-muted)]">No indexes on this label.</p>}
              </div>

              <div className="flex flex-col gap-2 pt-1">
                <Button size="sm" variant="primary" data-testid="metagraph-show-instances" onClick={() => navigate(`/graph?label=${encodeURIComponent(selectedType.label)}`)}>
                  <Waypoints size={13} /> Show instances
                </Button>
                <Button size="sm" variant="outline" data-testid="metagraph-edit-ontology" onClick={() => navigate(`/ontology?tab=designer`)}>
                  <ChevronRight size={13} /> Edit in Ontology Designer
                </Button>
              </div>
            </motion.div>
          )}
        </Card>
      </div>
    </Page>
  );
}

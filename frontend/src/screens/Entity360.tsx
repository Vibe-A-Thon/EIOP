import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowDownLeft,
  ArrowUpRight,
  Boxes,
  Code2,
  FileClock,
  GitFork,
  Radar,
  ShieldAlert,
  Waypoints,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { FactClassBadge } from "../components/FactClassBadge";
import { LoadingState, ErrorState, Skeleton, EmptyState } from "../components/ui/States";
import { cn, shortId } from "../lib/utils";

type Tab = "overview" | "relationships" | "provenance" | "impact" | "raw";
const TABS: { id: Tab; label: string; icon: any }[] = [
  { id: "overview", label: "Overview", icon: Boxes },
  { id: "relationships", label: "Relationships", icon: GitFork },
  { id: "provenance", label: "Provenance", icon: FileClock },
  { id: "impact", label: "Impact", icon: Radar },
  { id: "raw", label: "Raw", icon: Code2 },
];

const RISK_TONE: Record<string, any> = {
  NONE: "neutral",
  LOW: "info",
  MEDIUM: "warning",
  HIGH: "warning",
  CRITICAL: "danger",
};

function EdgeRow({ edge, direction }: { edge: any; direction: "out" | "in" }) {
  const target = direction === "out" ? edge.to_id : edge.from_id;
  return (
    <Link
      to={`/entity/${encodeURIComponent(target)}`}
      className="flex items-center gap-2.5 px-4 py-2.5 text-sm transition-colors hover:bg-[var(--bg-hover)]"
    >
      {direction === "out" ? (
        <ArrowUpRight size={14} className="shrink-0 text-cyan-400" />
      ) : (
        <ArrowDownLeft size={14} className="shrink-0 text-blue-400" />
      )}
      <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
        {edge.type}
      </span>
      <span className="truncate font-mono text-xs text-[var(--text-secondary)]">
        {shortId(target)}
      </span>
      <FactClassBadge creationStatus={edge.creation_status} size="sm" />
    </Link>
  );
}

export function Entity360() {
  const { id = "" } = useParams();
  const canonicalId = decodeURIComponent(id);
  const { session } = useAuth();
  const [tab, setTab] = useState<Tab>("overview");

  const entity = useQuery({
    queryKey: [session?.tenant, "entity", canonicalId],
    queryFn: () => apiFetch<any>(`/entities/${encodeURIComponent(canonicalId)}`),
  });
  const metrics = useQuery({
    queryKey: [session?.tenant, "metrics", canonicalId],
    queryFn: () => apiFetch<any>("/graph/metrics", { method: "POST", body: { canonical_ids: [canonicalId] } }),
    enabled: !!entity.data,
    retry: false,
  });
  const lineage = useQuery({
    queryKey: [session?.tenant, "lineage", canonicalId],
    queryFn: () => apiFetch<any>("/lineage", { method: "POST", body: { canonical_id: canonicalId, max_depth: 4, result_limit: 100 } }),
    enabled: tab === "provenance",
    retry: false,
  });
  const blast = useQuery({
    queryKey: [session?.tenant, "blast", canonicalId],
    queryFn: () => apiFetch<any>("/graph/blast-radius", { method: "POST", body: { canonical_id: canonicalId, max_depth: 4 } }),
    enabled: tab === "impact",
    retry: false,
  });

  if (entity.isLoading) return <LoadingState label="Loading entity" testId="entity-loading" />;
  if (entity.error) return <ErrorState problem={entity.error} onRetry={entity.refetch} />;

  const e = entity.data?.entity;
  const props = e?.properties || {};
  const name = props.name || props.title || shortId(canonicalId);
  const outgoing: any[] = entity.data?.outgoing || [];
  const incoming: any[] = entity.data?.incoming || [];
  const cm = metrics.data?.[canonicalId];

  return (
    <div className="mx-auto max-w-5xl p-6" data-testid="entity-360">
      {/* Header */}
      <div className="mb-5">
        <Link to="/graph" className="mb-2 inline-flex items-center gap-1 text-xs text-[var(--text-muted)] transition-colors hover:text-[var(--accent)]">
          <Waypoints size={12} /> Graph Explorer
        </Link>
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full border border-[var(--border-strong)] px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-[var(--text-secondary)]">
            {e?.label}
          </span>
          <FactClassBadge creationStatus={props.creation_status} />
          {props.trust_state && <Badge tone="neutral">trust: {props.trust_state}</Badge>}
        </div>
        <h1 className="mt-2 break-words font-heading text-2xl font-bold tracking-tight">{name}</h1>
        <p className="mt-1 break-all font-mono text-[11px] text-[var(--text-muted)]">{canonicalId}</p>
      </div>

      {/* Tabs */}
      <div className="mb-4 flex gap-1 border-b border-[var(--border-subtle)]">
        {TABS.map((t) => (
          <button
            key={t.id}
            data-testid={`entity-tab-${t.id}`}
            onClick={() => setTab(t.id)}
            className={cn(
              "relative flex items-center gap-1.5 px-3 py-2.5 text-sm transition-colors",
              tab === t.id
                ? "text-[var(--text-primary)]"
                : "text-[var(--text-muted)] hover:text-[var(--text-primary)]",
            )}
          >
            <t.icon size={14} />
            {t.label}
            {tab === t.id && (
              <span className="absolute bottom-0 left-0 h-[2px] w-full rounded-full bg-[var(--accent)]" />
            )}
          </button>
        ))}
      </div>

      {/* Overview */}
      {tab === "overview" && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <div className="border-b border-[var(--border-subtle)] px-4 py-3">
              <h3 className="font-heading text-sm font-semibold">Properties</h3>
            </div>
            <dl className="p-4">
              {Object.entries(props)
                .filter(([, v]) => v !== null && typeof v !== "object")
                .map(([k, v]) => (
                  <div key={k} className="flex items-start justify-between gap-4 border-b border-[var(--border-subtle)] py-2 text-xs last:border-0">
                    <dt className="shrink-0 font-mono text-[var(--text-muted)]">{k}</dt>
                    <dd className="break-all text-right text-[var(--text-secondary)]">{String(v)}</dd>
                  </div>
                ))}
            </dl>
          </Card>
          <Card>
            <div className="border-b border-[var(--border-subtle)] px-4 py-3">
              <h3 className="font-heading text-sm font-semibold">Centrality</h3>
            </div>
            <div className="p-4">
              {metrics.isLoading ? (
                <Skeleton className="h-24 w-full" />
              ) : cm ? (
                <div className="grid grid-cols-2 gap-3">
                  {[
                    ["Degree", cm.degree],
                    ["In-degree", cm.in_degree],
                    ["Out-degree", cm.out_degree],
                    ["PageRank", cm.page_rank?.toFixed?.(4) ?? cm.page_rank],
                    ["Betweenness", cm.betweenness?.toFixed?.(4) ?? cm.betweenness],
                    ["Closeness", cm.closeness?.toFixed?.(4) ?? cm.closeness],
                  ].map(([label, val]) => (
                    <div key={label as string} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-2.5">
                      <p className="font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">{label}</p>
                      <p className="font-heading text-base font-semibold">{val ?? "N/A"}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-[var(--text-muted)]">Centrality metrics not available.</p>
              )}
            </div>
          </Card>
        </div>
      )}

      {/* Relationships */}
      {tab === "relationships" && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-3">
              <h3 className="font-heading text-sm font-semibold">Outgoing</h3>
              <Badge tone="accent">{outgoing.length}</Badge>
            </div>
            <div className="max-h-[480px] divide-y divide-[var(--border-subtle)] overflow-y-auto">
              {outgoing.length === 0 ? (
                <p className="p-6 text-center text-sm text-[var(--text-muted)]">No outgoing edges.</p>
              ) : (
                outgoing.map((edge, i) => <EdgeRow key={i} edge={edge} direction="out" />)
              )}
            </div>
          </Card>
          <Card>
            <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-3">
              <h3 className="font-heading text-sm font-semibold">Incoming</h3>
              <Badge tone="info">{incoming.length}</Badge>
            </div>
            <div className="max-h-[480px] divide-y divide-[var(--border-subtle)] overflow-y-auto">
              {incoming.length === 0 ? (
                <p className="p-6 text-center text-sm text-[var(--text-muted)]">No incoming edges.</p>
              ) : (
                incoming.map((edge, i) => <EdgeRow key={i} edge={edge} direction="in" />)
              )}
            </div>
          </Card>
        </div>
      )}

      {/* Provenance */}
      {tab === "provenance" && (
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3">
            <h3 className="font-heading text-sm font-semibold">Lineage & evidence</h3>
          </div>
          <div className="p-4">
            {lineage.isLoading ? (
              <LoadingState label="Tracing lineage" />
            ) : lineage.error ? (
              <ErrorState problem={lineage.error} onRetry={lineage.refetch} />
            ) : (lineage.data?.evidence?.length || lineage.data?.nodes?.length) ? (
              <div className="space-y-4">
                <div className="flex gap-6 text-sm">
                  <span><strong className="font-heading">{lineage.data.nodes?.length ?? 0}</strong> <span className="text-[var(--text-muted)]">lineage nodes</span></span>
                  <span><strong className="font-heading">{lineage.data.edges?.length ?? 0}</strong> <span className="text-[var(--text-muted)]">edges</span></span>
                  <span><strong className="font-heading">{lineage.data.evidence?.length ?? 0}</strong> <span className="text-[var(--text-muted)]">evidence</span></span>
                </div>
                <div className="space-y-2">
                  {(lineage.data.evidence || []).slice(0, 12).map((ev: any, i: number) => (
                    <div key={i} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3 text-xs">
                      <p className="text-[var(--text-secondary)]">{ev.fact_text || ev.text || JSON.stringify(ev).slice(0, 160)}</p>
                      {ev.source_ref && <p className="mt-1 break-all font-mono text-[10px] text-[var(--text-muted)]">{ev.source_ref}</p>}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <EmptyState title="No lineage recorded" description="This entity has no provenance chain in the current graph." icon={<FileClock size={22} />} />
            )}
          </div>
        </Card>
      )}

      {/* Impact */}
      {tab === "impact" && (
        <Card>
          <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
            <ShieldAlert size={15} className="text-[var(--text-muted)]" />
            <h3 className="font-heading text-sm font-semibold">Blast radius</h3>
          </div>
          <div className="p-4">
            {blast.isLoading ? (
              <LoadingState label="Computing blast radius" />
            ) : blast.error ? (
              <ErrorState problem={blast.error} onRetry={blast.refetch} />
            ) : blast.data ? (
              <div className="space-y-5">
                <div className="flex flex-wrap items-center gap-4">
                  <div className="flex items-center gap-2">
                    <Overline>Risk</Overline>
                    <Badge tone={RISK_TONE[blast.data.risk] || "neutral"}>{blast.data.risk ?? "N/A"}</Badge>
                  </div>
                  <div className="flex items-center gap-2">
                    <Overline>Total affected</Overline>
                    <span className="font-heading text-lg font-bold">{blast.data.total_affected ?? 0}</span>
                  </div>
                </div>
                {blast.data.by_depth && (
                  <div>
                    <Overline>Affected by depth</Overline>
                    <div className="mt-2 flex items-end gap-2">
                      {Object.entries(blast.data.by_depth).map(([depth, count]: any) => {
                        const max = Math.max(...Object.values<number>(blast.data.by_depth));
                        return (
                          <div key={depth} className="flex flex-1 flex-col items-center gap-1">
                            <div className="flex h-24 w-full items-end">
                              <div
                                className="w-full rounded-t-sm bg-[var(--accent)] transition-[height] duration-500"
                                style={{ height: `${(count / (max || 1)) * 100}%` }}
                              />
                            </div>
                            <span className="font-mono text-[10px] text-[var(--text-secondary)]">{count}</span>
                            <span className="font-mono text-[9px] text-[var(--text-muted)]">d{depth}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
                {blast.data.by_type && (
                  <div>
                    <Overline>Affected by type</Overline>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {Object.entries(blast.data.by_type).map(([label, count]: any) => (
                        <span key={label} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2 py-1 font-mono text-[10px]">
                          {label}: <strong>{count}</strong>
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <EmptyState title="No impact data" icon={<Radar size={22} />} />
            )}
          </div>
        </Card>
      )}

      {/* Raw */}
      {tab === "raw" && (
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3">
            <h3 className="font-heading text-sm font-semibold">Raw entity</h3>
          </div>
          <pre className="overflow-x-auto p-4 font-mono text-[11px] leading-relaxed text-[var(--text-secondary)]">
            {JSON.stringify(entity.data, null, 2)}
          </pre>
        </Card>
      )}
    </div>
  );
}

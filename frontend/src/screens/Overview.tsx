import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import {
  Activity,
  ArrowUpRight,
  Boxes,
  GitFork,
  Layers,
  MessagesSquare,
  Network,
  ShieldCheck,
  Spline,
  Waypoints,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge, StatusDot } from "../components/ui/Badge";
import { Skeleton } from "../components/ui/States";
import { AnimatedCounter } from "../components/ui/AnimatedCounter";
import { formatNumber, relativeTime } from "../lib/utils";

function StatTile({
  label,
  value,
  icon: Icon,
  loading,
  decimals = 0,
}: {
  label: string;
  value: number | null | undefined;
  icon: any;
  loading?: boolean;
  decimals?: number;
}) {
  return (
    <Card hover className="p-4">
      <div className="flex items-center justify-between">
        <Overline>{label}</Overline>
        <Icon size={15} className="text-[var(--text-muted)]" />
      </div>
      {loading ? (
        <Skeleton className="mt-3 h-8 w-20" />
      ) : (
        <p className="mt-2 font-heading text-2xl font-bold tracking-tight">
          <AnimatedCounter value={value} decimals={decimals} />
        </p>
      )}
    </Card>
  );
}

const DOMAIN_COLORS = [
  "#06b6d4",
  "#3b82f6",
  "#8b5cf6",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#ec4899",
  "#14b8a6",
];

export function Overview() {
  const { session } = useAuth();
  const stats = useQuery({
    queryKey: [session?.tenant, "statistics"],
    queryFn: () => apiFetch<any>("/graph/statistics"),
  });
  const schema = useQuery({
    queryKey: [session?.tenant, "schema"],
    queryFn: () => apiFetch<any>("/graph/schema"),
    staleTime: 300_000,
  });
  const system = useQuery({
    queryKey: [session?.tenant, "admin-system"],
    queryFn: () => apiFetch<any>("/admin/system"),
    retry: false,
  });
  const events = useQuery({
    queryKey: [session?.tenant, "graph-events"],
    queryFn: () => apiFetch<any>("/graph/events?limit=8"),
  });

  // Domain distribution from schema vertex_labels instance_count
  const domainDist: { domain: string; count: number }[] = (() => {
    const labels = schema.data?.vertex_labels || {};
    const agg: Record<string, number> = {};
    for (const meta of Object.values<any>(labels)) {
      const d = meta.domain || "UNKNOWN";
      agg[d] = (agg[d] || 0) + (meta.instance_count || 0);
    }
    return Object.entries(agg)
      .map(([domain, count]) => ({ domain, count }))
      .filter((d) => d.count > 0)
      .sort((a, b) => b.count - a.count);
  })();
  const domainTotal = domainDist.reduce((s, d) => s + d.count, 0) || 1;

  const recent: any[] = (events.data?.events || []).slice().reverse();

  const health = [
    {
      label: "Graph store",
      status: system.data?.graph?.status,
      tone: system.data?.graph?.status === "ok" || system.data?.graph?.status === "ready" ? "success" : "warning",
    },
    {
      label: "Model",
      status: system.data?.model?.status || "N/A",
      tone:
        system.data?.model?.status === "ready"
          ? "success"
          : system.data?.model?.status === "disabled"
            ? "neutral"
            : "warning",
    },
    {
      label: "Backup",
      status: system.data?.backup?.status || "N/A",
      tone: system.data?.backup?.status === "available" ? "success" : "neutral",
    },
  ] as const;

  return (
    <div className="kgf-ambient mx-auto max-w-[1400px] space-y-6 p-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <Overline>Workbench · {session?.tenant} / {session?.workspace}</Overline>
          <h1 className="mt-1 font-heading text-3xl font-bold tracking-tight sm:text-4xl">Overview</h1>
        </div>
        <Link
          to="/ask"
          data-testid="overview-ask-cta"
          className="flex items-center gap-2 rounded-sm bg-[var(--accent)] px-3.5 py-2 text-sm font-semibold text-black shadow-[0_2px_14px_-4px_var(--accent)] transition-[background-color,box-shadow,transform] duration-150 hover:bg-[var(--accent-strong)] hover:shadow-[0_4px_20px_-4px_var(--accent)] active:scale-95"
        >
          <MessagesSquare size={15} /> Ask a question
        </Link>
      </div>

      {/* Stat tiles */}
      <div className="kgf-stagger grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-5">
        <StatTile label="Vertices" value={stats.data?.vertex_count} icon={Boxes} loading={stats.isLoading} />
        <StatTile label="Edges" value={stats.data?.edge_count} icon={GitFork} loading={stats.isLoading} />
        <StatTile label="Density" value={stats.data?.density} decimals={4} icon={Spline} loading={stats.isLoading} />
        <StatTile label="Vertex labels" value={stats.data?.vertex_label_count} icon={Layers} loading={stats.isLoading} />
        <StatTile label="Edge labels" value={stats.data?.edge_label_count} icon={Network} loading={stats.isLoading} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Domain distribution */}
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-3">
            <div className="flex items-center gap-2">
              <Waypoints size={15} className="text-[var(--text-muted)]" />
              <h3 className="font-heading text-sm font-semibold">Graph by domain</h3>
            </div>
            <Link to="/schema" className="flex items-center gap-1 text-xs text-[var(--text-muted)] transition-colors hover:text-[var(--accent)]">
              Schema <ArrowUpRight size={12} />
            </Link>
          </div>
          <div className="space-y-3 p-4">
            {schema.isLoading && <Skeleton className="h-40 w-full" />}
            {!schema.isLoading && domainDist.length === 0 && (
              <p className="py-10 text-center text-sm text-[var(--text-muted)]">No instances present.</p>
            )}
            {domainDist.map((d, i) => (
              <div key={d.domain}>
                <div className="mb-1 flex items-center justify-between text-xs">
                  <span className="font-mono uppercase tracking-wider text-[var(--text-secondary)]">
                    {d.domain}
                  </span>
                  <span className="font-mono text-[var(--text-muted)]">{formatNumber(d.count)}</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-[var(--bg-panel)]">
                  <div
                    className="h-full rounded-full transition-[width] duration-500"
                    style={{
                      width: `${(d.count / domainTotal) * 100}%`,
                      backgroundColor: DOMAIN_COLORS[i % DOMAIN_COLORS.length],
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* System health (three separate signals, never one %) */}
        <Card>
          <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
            <ShieldCheck size={15} className="text-[var(--text-muted)]" />
            <h3 className="font-heading text-sm font-semibold">System signals</h3>
          </div>
          <div className="space-y-2 p-4">
            {system.isLoading
              ? [0, 1, 2].map((i) => <Skeleton key={i} className="h-12 w-full" />)
              : health.map((h) => (
                  <div
                    key={h.label}
                    className="flex items-center justify-between rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-3 py-2.5"
                  >
                    <span className="text-sm text-[var(--text-secondary)]">{h.label}</span>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs">{String(h.status ?? "N/A")}</span>
                      <StatusDot tone={h.tone as any} />
                    </div>
                  </div>
                ))}
            <p className="pt-1 font-mono text-[10px] leading-relaxed text-[var(--text-muted)]">
              Signals reported independently — not aggregated into a single score.
            </p>
          </div>
        </Card>
      </div>

      {/* Recent activity */}
      <Card>
        <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
          <Activity size={15} className="text-[var(--text-muted)]" />
          <h3 className="font-heading text-sm font-semibold">Recent activity</h3>
          <Badge tone="accent" className="ml-1">
            {recent.length}
          </Badge>
        </div>
        <div className="divide-y divide-[var(--border-subtle)]">
          {events.isLoading && <div className="p-4"><Skeleton className="h-6 w-full" /></div>}
          {!events.isLoading && recent.length === 0 && (
            <p className="p-6 text-center text-sm text-[var(--text-muted)]">No recent events.</p>
          )}
          {recent.map((e, i) => (
            <div key={i} className="flex items-center gap-3 px-4 py-2.5 text-sm">
              <span className="font-mono text-[var(--text-secondary)]">{e.type}</span>
              <span className="ml-auto font-mono text-[11px] text-[var(--text-muted)]">
                {relativeTime(e.timestamp || e.created_at)}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

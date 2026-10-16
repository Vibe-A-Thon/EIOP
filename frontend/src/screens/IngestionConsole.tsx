import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import {
  Activity,
  AlertOctagon,
  Boxes,
  DatabaseZap,
  Plug,
  RefreshCw,
  Server,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge, StatusDot } from "../components/ui/Badge";
import { JobStatusBadge } from "../components/ModeBadges";
import { LoadingState, ErrorState, EmptyState } from "../components/ui/States";
import { Button } from "../components/ui/Button";
import { SourceOnboarding } from "../components/SourceOnboarding";
import { cn, relativeTime, shortId } from "../lib/utils";

type Tab = "runs" | "jobs" | "sources" | "dlq";
const TABS: { id: Tab; label: string; icon: any }[] = [
  { id: "runs", label: "Ingestion runs", icon: Activity },
  { id: "jobs", label: "Jobs", icon: Server },
  { id: "sources", label: "Sources", icon: Plug },
  { id: "dlq", label: "Dead-letter queue", icon: AlertOctagon },
];

const HEALTH_TONE: Record<string, any> = {
  HEALTHY: "success",
  DEGRADED: "warning",
  UNAVAILABLE: "danger",
  MISCONFIGURED: "danger",
  UNKNOWN: "neutral",
};

export function IngestionConsole() {
  const { session } = useAuth();
  const qc = useQueryClient();
  const [tab, setTab] = useState<Tab>("runs");
  const [onboarding, setOnboarding] = useState<any | null>(null);
  const t = session?.tenant;

  const runs = useQuery({
    queryKey: [t, "ingestion-runs"],
    queryFn: () => apiFetch<any>("/ingestion/runs?limit=50"),
    enabled: tab === "runs",
  });
  const jobs = useQuery({
    queryKey: [t, "admin-jobs"],
    queryFn: () => apiFetch<any>("/admin/jobs"),
    enabled: tab === "jobs",
    refetchInterval: tab === "jobs" ? 4000 : false,
  });
  const sources = useQuery({
    queryKey: [t, "sources"],
    queryFn: () => apiFetch<any>("/sources"),
    enabled: tab === "sources",
  });
  const connectors = useQuery({
    queryKey: ["connectors-catalog"],
    queryFn: () => apiFetch<any>("/connectors/catalog"),
    enabled: tab === "sources",
    staleTime: 600_000,
  });
  const dlq = useQuery({
    queryKey: [t, "admin-dlq"],
    queryFn: () => apiFetch<any>("/admin/dlq?limit=50"),
    enabled: tab === "dlq",
  });

  const runList: any[] = Array.isArray(runs.data) ? runs.data : runs.data?.runs || [];
  const jobList: any[] = Array.isArray(jobs.data) ? jobs.data : jobs.data?.jobs || [];
  const sourceList: any[] = Array.isArray(sources.data) ? sources.data : sources.data?.sources || [];
  const connectorList: any[] = connectors.data?.connectors || connectors.data || [];
  const dlqList: any[] = Array.isArray(dlq.data) ? dlq.data : dlq.data?.entries || [];

  const refresh = () => qc.invalidateQueries({ queryKey: [t] });

  return (
    <div className="mx-auto max-w-[1300px] space-y-5 p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <DatabaseZap size={18} className="text-cyan-400" />
          <div>
            <h1 className="font-heading text-2xl font-bold tracking-tight">Ingestion Console</h1>
            <p className="text-xs text-[var(--text-muted)]">
              Connect sources, watch data load, and monitor background jobs.
            </p>
          </div>
        </div>
        <Button variant="secondary" size="sm" onClick={refresh} data-testid="ingestion-refresh">
          <RefreshCw size={13} /> Refresh
        </Button>
      </div>

      <div className="flex flex-wrap gap-1 border-b border-[var(--border-subtle)]">
        {TABS.map((tb) => (
          <button
            key={tb.id}
            data-testid={`ingestion-tab-${tb.id}`}
            onClick={() => setTab(tb.id)}
            className={cn(
              "relative flex items-center gap-1.5 px-3 py-2.5 text-sm transition-colors",
              tab === tb.id ? "text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]",
            )}
          >
            <tb.icon size={14} />
            {tb.label}
            {tab === tb.id && <span className="absolute bottom-0 left-0 h-[2px] w-full rounded-full bg-[var(--accent)]" />}
          </button>
        ))}
      </div>

      {/* Runs */}
      {tab === "runs" && (
        <Card>
          {runs.isLoading ? (
            <LoadingState label="Loading ingestion runs" />
          ) : runs.error ? (
            <ErrorState problem={runs.error} onRetry={runs.refetch} />
          ) : runList.length === 0 ? (
            <EmptyState title="No ingestion runs yet" icon={<Activity size={22} />} />
          ) : (
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-[var(--border-subtle)] text-[var(--text-muted)]">
                  {["Run", "Source", "Status", "Vertices", "Edges", "Finished"].map((h) => (
                    <th key={h} className="px-4 py-2.5 font-mono text-[10px] uppercase tracking-wider">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {runList.map((r, i) => (
                  <tr key={r.canonical_id || i} className="border-b border-[var(--border-subtle)] transition-colors last:border-0 hover:bg-[var(--bg-hover)]">
                    <td className="px-4 py-2.5">
                      <div className="font-medium">{r.run_kind || "run"}</div>
                      <div className="font-mono text-[10px] text-[var(--text-muted)]">{shortId(r.canonical_id || "")}</div>
                    </td>
                    <td className="px-4 py-2.5 font-mono text-xs text-[var(--text-secondary)]">{r.source_system || "—"}</td>
                    <td className="px-4 py-2.5"><JobStatusBadge status={r.run_status || "PENDING"} /></td>
                    <td className="px-4 py-2.5 font-mono text-xs">{r.counts?.vertices ?? "—"}</td>
                    <td className="px-4 py-2.5 font-mono text-xs">{r.counts?.edges ?? "—"}</td>
                    <td className="px-4 py-2.5 font-mono text-[11px] text-[var(--text-muted)]">{relativeTime(r.finished_at || r.started_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>
      )}

      {/* Jobs */}
      {tab === "jobs" && (
        <Card>
          {jobs.isLoading ? (
            <LoadingState label="Loading jobs" />
          ) : jobs.error ? (
            <ErrorState problem={jobs.error} onRetry={jobs.refetch} />
          ) : jobList.length === 0 ? (
            <EmptyState
              title="No background jobs"
              description="Jobs appear here when you run discovery, baseline, sync or ingestion operations."
              icon={<Server size={22} />}
            />
          ) : (
            <div className="divide-y divide-[var(--border-subtle)]">
              {jobList.map((j, i) => (
                <div key={j.job_id || i} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{j.kind}</span>
                      <JobStatusBadge status={j.status} />
                    </div>
                    <p className="font-mono text-[10px] text-[var(--text-muted)]">{j.job_id} · {relativeTime(j.created_at)}</p>
                  </div>
                  {j.status === "HELD" && (
                    <Button size="sm" variant="outline" onClick={async () => { await apiFetch(`/admin/jobs/${j.job_id}/readmit`, { method: "POST" }).catch(() => {}); refresh(); }}>
                      Re-admit
                    </Button>
                  )}
                  {(j.status === "PENDING" || j.status === "HELD") && (
                    <Button size="sm" variant="ghost" onClick={async () => { await apiFetch(`/admin/jobs/${j.job_id}/cancel`, { method: "POST" }).catch(() => {}); refresh(); }}>
                      Cancel
                    </Button>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Sources */}
      {tab === "sources" && (
        <div className="space-y-5">
          <Card>
            <div className="border-b border-[var(--border-subtle)] px-4 py-3">
              <h3 className="font-heading text-sm font-semibold">Registered sources</h3>
            </div>
            {sources.isLoading ? (
              <LoadingState label="Loading sources" />
            ) : sourceList.length === 0 ? (
              <EmptyState
                title="No sources registered"
                description="This deployment has no connected sources yet. Available connectors are listed below."
                icon={<Plug size={22} />}
              />
            ) : (
              <div className="divide-y divide-[var(--border-subtle)]">
                {sourceList.map((s, i) => (
                  <div key={s.source_id || i} className="flex items-center gap-3 px-4 py-3">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{s.name}</span>
                        <Badge tone="neutral">{s.source_type}</Badge>
                      </div>
                      <p className="font-mono text-[10px] text-[var(--text-muted)]">{s.source_id}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[11px] text-[var(--text-secondary)]">{s.health || "UNKNOWN"}</span>
                      <StatusDot tone={HEALTH_TONE[s.health || "UNKNOWN"]} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <div>
            <div className="mb-2 flex items-center justify-between">
              <Overline>Available connectors ({connectorList.length})</Overline>
              <span className="font-mono text-[10px] text-[var(--text-muted)]">Click a connector to connect it</span>
            </div>
            <div className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
              {connectorList.map((c: any) => (
                <button
                  key={c.id}
                  data-testid={`connector-${c.id}`}
                  onClick={() => setOnboarding(c)}
                  className="flex items-center gap-2.5 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-surface)] p-3 text-left transition-colors hover:border-[var(--accent)] hover:bg-[var(--bg-hover)]"
                >
                  <div className="grid h-8 w-8 shrink-0 place-items-center rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] text-[var(--text-muted)]">
                    <Boxes size={15} />
                  </div>
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium capitalize">{c.name || c.id}</p>
                    <p className="font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">{c.type}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* DLQ */}
      {tab === "dlq" && (
        <Card>
          {dlq.isLoading ? (
            <LoadingState label="Loading dead-letter queue" />
          ) : dlq.error ? (
            <ErrorState problem={dlq.error} onRetry={dlq.refetch} />
          ) : dlqList.length === 0 ? (
            <EmptyState title="Dead-letter queue is empty" description="No failed ingestion events." icon={<AlertOctagon size={22} />} />
          ) : (
            <div className="divide-y divide-[var(--border-subtle)]">
              {dlqList.map((e, i) => (
                <div key={e.event_id || i} className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Badge tone="danger">{e.error_category || "error"}</Badge>
                    <span className="font-mono text-[10px] text-[var(--text-muted)]">{e.source || e.source_system} · {relativeTime(e.failed_at)}</span>
                  </div>
                  <p className="mt-1 text-sm text-[var(--text-secondary)]">{e.error}</p>
                  {e.event_id && <p className="mt-0.5 break-all font-mono text-[10px] text-[var(--text-muted)]">{e.event_id}</p>}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {onboarding && (
        <SourceOnboarding
          connector={onboarding}
          onClose={() => setOnboarding(null)}
          onDone={refresh}
        />
      )}
    </div>
  );
}

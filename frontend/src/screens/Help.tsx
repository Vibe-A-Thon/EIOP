import { useQuery } from "@tanstack/react-query";
import { BookOpen, LifeBuoy, Bell } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch, BACKEND_BASE } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, LoadingState } from "../components/ui/States";
import { relativeTime } from "../lib/utils";

export function Help() {
  const { session } = useAuth();
  const licensing = useQuery({ queryKey: ["licensing"], queryFn: () => apiFetch<any>("/licensing/status"), retry: false });
  const scenarios = useQuery({ queryKey: ["demo-scenarios"], queryFn: () => apiFetch<any>("/demo/scenarios"), retry: false });
  const inbox = useQuery({
    queryKey: [session?.principal.id, "inbox"],
    queryFn: () => apiFetch<any>(`/platform/notifications/inbox/${encodeURIComponent(session!.principal.id)}?limit=20`),
    retry: false,
  });

  const scList: any[] = scenarios.data?.scenarios || [];
  const notes: any[] = inbox.data?.notifications || inbox.data?.inbox || (Array.isArray(inbox.data) ? inbox.data : []);

  return (
    <Page>
      <PageHeader title="Help & About" overline="Guided tour, notifications & licensing" icon={<LifeBuoy size={18} />} />

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3"><BookOpen size={15} className="text-[var(--text-muted)]" /><h3 className="font-heading text-sm font-semibold">Guided tour</h3><Badge tone="warning">Demo Mode</Badge></div>
          {scenarios.isLoading ? <LoadingState label="Loading scenarios" />
            : scList.length === 0 ? <EmptyState title="No demo scenarios" />
            : <div className="divide-y divide-[var(--border-subtle)]">{scList.map((s, i) => (
                <div key={s.id || i} className="px-4 py-3">
                  <div className="flex items-center gap-2"><p className="text-sm font-medium">{s.title}</p>{s.available === false && <Badge tone="neutral">unavailable</Badge>}</div>
                  <p className="mt-0.5 text-xs text-[var(--text-muted)]">{s.story || s.description}</p>
                  {s.audience && <p className="mt-1 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">{s.audience}</p>}
                </div>
              ))}</div>}
        </Card>

        <Card>
          <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3"><Bell size={15} className="text-[var(--text-muted)]" /><h3 className="font-heading text-sm font-semibold">Notifications</h3></div>
          {inbox.isLoading ? <LoadingState label="Loading inbox" />
            : notes.length === 0 ? <EmptyState title="No notifications" />
            : <div className="divide-y divide-[var(--border-subtle)]">{notes.map((n, i) => (
                <div key={n.id || i} className="px-4 py-2.5"><p className="text-sm">{n.subject}</p><p className="truncate text-xs text-[var(--text-muted)]">{n.body} · {relativeTime(n.created_at || n.sent_at)}</p></div>
              ))}</div>}
        </Card>
      </div>

      <Card className="p-5">
        <Overline>About</Overline>
        <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3">
            <p className="font-heading text-sm font-semibold">KnowGridFlow</p>
            <p className="mt-0.5 text-xs text-[var(--text-muted)]">Enterprise Ontology & Intelligence Platform</p>
            <p className="mt-1 break-all font-mono text-[10px] text-[var(--text-muted)]">API: {BACKEND_BASE}/api/v1</p>
          </div>
          <div className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3">
            <p className="font-heading text-sm font-semibold">Licensing</p>
            {licensing.data ? (
              <div className="mt-1 space-y-0.5 text-xs">
                <p className="text-[var(--text-secondary)]">Status: <span className="font-mono">{licensing.data.status || licensing.data.state || "—"}</span></p>
                {licensing.data.degraded && <Badge tone="warning">degraded — read-only</Badge>}
              </div>
            ) : <p className="mt-1 text-xs text-[var(--text-muted)]">License status unavailable.</p>}
          </div>
        </div>
      </Card>
    </Page>
  );
}

import { useQuery } from "@tanstack/react-query";
import { SlidersHorizontal } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";
import { ErrorState, LoadingState, EmptyState } from "../components/ui/States";

export function Tenant() {
  const { session } = useAuth();
  const context = useQuery({ queryKey: [session?.tenant, "tenancy-context"], queryFn: () => apiFetch<any>("/tenancy/context"), retry: false });
  const quotas = useQuery({ queryKey: [session?.tenant, "tenancy-quotas"], queryFn: () => apiFetch<any>("/tenancy/quotas"), retry: false });
  const flags = useQuery({ queryKey: [session?.tenant, "feature-flags"], queryFn: () => apiFetch<any>("/enterprise/feature-flags"), retry: false });

  const usage = quotas.data?.usage || {};
  const spec = quotas.data?.spec || {};
  const flagList: any[] = flags.data?.flags || (Array.isArray(flags.data) ? flags.data : Object.entries(flags.data || {}).map(([name, enabled]) => ({ name, enabled })));

  return (
    <Page>
      <PageHeader title="Tenant" overline={`Tenant ${session?.tenant} · workspace ${session?.workspace}`} icon={<SlidersHorizontal size={18} />} />

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Context</h3></div>
          <div className="p-4">
            {context.isLoading ? <LoadingState label="Loading context" />
              : context.error ? <ErrorState problem={context.error} onRetry={context.refetch} />
              : <dl className="space-y-1.5">{Object.entries(context.data || {}).filter(([, v]) => typeof v !== "object").map(([k, v]) => (
                  <div key={k} className="flex justify-between border-b border-[var(--border-subtle)] py-1.5 text-xs last:border-0"><dt className="font-mono text-[var(--text-muted)]">{k}</dt><dd className="font-mono text-[var(--text-secondary)]">{String(v)}</dd></div>
                ))}</dl>}
          </div>
        </Card>

        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Quotas <span className="font-mono text-[10px] text-[var(--text-muted)]">· lane {quotas.data?.lane ?? "—"}</span></h3></div>
          <div className="p-4">
            {quotas.isLoading ? <LoadingState label="Loading quotas" />
              : quotas.error ? <ErrorState problem={quotas.error} onRetry={quotas.refetch} />
              : Object.keys(usage).length === 0 ? <EmptyState title="No quota data" />
              : <div className="space-y-3">{Object.entries(usage).map(([dim, val]: any) => {
                  const limit = spec[dim];
                  const pct = limit ? Math.min((val / limit) * 100, 100) : 0;
                  return (
                    <div key={dim}>
                      <div className="mb-1 flex justify-between text-xs"><span className="font-mono uppercase text-[var(--text-secondary)]">{dim}</span><span className="font-mono text-[var(--text-muted)]">{val}{limit ? ` / ${limit}` : ""}</span></div>
                      {limit ? <div className="h-2 overflow-hidden rounded-full bg-[var(--bg-panel)]"><div className="h-full rounded-full bg-[var(--accent)]" style={{ width: `${pct}%` }} /></div> : null}
                    </div>
                  );
                })}</div>}
          </div>
        </Card>
      </div>

      <Card>
        <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Feature flags</h3></div>
        {flags.isLoading ? <LoadingState label="Loading flags" />
          : flags.error ? <ErrorState problem={flags.error} onRetry={flags.refetch} />
          : flagList.length === 0 ? <EmptyState title="No feature flags" />
          : <div className="divide-y divide-[var(--border-subtle)]">{flagList.map((f, i) => (
              <div key={f.name || f.flag_name || i} className="flex items-center justify-between px-4 py-2.5 text-sm"><span className="font-mono">{f.name || f.flag_name}</span><Badge tone={f.enabled ? "success" : "neutral"}>{f.enabled ? "on" : "off"}</Badge></div>
            ))}</div>}
      </Card>
    </Page>
  );
}

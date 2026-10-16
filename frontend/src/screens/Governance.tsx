import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { ScrollText } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge, StatusDot } from "../components/ui/Badge";
import { Page, PageHeader, Tabs } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";

type Tab = "posture" | "roles" | "egress";

export function Governance() {
  const { session } = useAuth();
  const [tab, setTab] = useState<Tab>("posture");

  const status = useQuery({ queryKey: [session?.tenant, "sec-status"], queryFn: () => apiFetch<any>("/security/status"), enabled: tab === "posture", retry: false });
  const matrix = useQuery({ queryKey: [session?.tenant, "policy-matrix"], queryFn: () => apiFetch<any>("/security/policy-matrix"), enabled: tab === "roles", retry: false });
  const egress = useQuery({ queryKey: ["egress-endpoints-gov"], queryFn: () => apiFetch<any>("/egress/endpoints"), enabled: tab === "egress", retry: false });

  const roles = matrix.data?.roles_hierarchy ? Object.entries(matrix.data.roles_hierarchy) : [];
  const endpoints: any[] = egress.data?.endpoints || (Array.isArray(egress.data) ? egress.data : []);

  return (
    <Page>
      <PageHeader title="Governance & Security" overline="Posture, roles & egress boundary" icon={<ScrollText size={18} />} />
      <Tabs testPrefix="governance-tab" active={tab} onChange={setTab} tabs={[
        { id: "posture", label: "Security posture" }, { id: "roles", label: "Roles & policy" }, { id: "egress", label: "Egress" },
      ]} />

      {tab === "posture" && (
        <Card className="p-4">
          {status.isLoading ? <LoadingState label="Loading security status" />
            : status.error ? <ErrorState problem={status.error} onRetry={status.refetch} />
            : <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                {Object.entries(status.data || {}).map(([k, v]) => (
                  <div key={k} className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3">
                    <Overline>{k.replace(/_/g, " ")}</Overline>
                    <p className="mt-1 truncate font-mono text-sm">{String(v)}</p>
                  </div>
                ))}
              </div>}
        </Card>
      )}

      {tab === "roles" && (
        <Card>
          {matrix.isLoading ? <LoadingState label="Loading policy matrix" />
            : matrix.error ? <ErrorState problem={matrix.error} onRetry={matrix.refetch} />
            : roles.length === 0 ? <EmptyState title="No roles defined" />
            : <div className="divide-y divide-[var(--border-subtle)]">{roles.map(([name, meta]: any) => (
                <div key={name} className="px-4 py-3">
                  <div className="flex items-center gap-2"><span className="font-medium">{name}</span><Badge tone="neutral">rank {meta.rank}</Badge></div>
                  <p className="mt-1 text-xs text-[var(--text-muted)]">{meta.description}</p>
                  <div className="mt-1.5 flex flex-wrap gap-1">{(meta.permissions || []).slice(0, 10).map((p: string) => <span key={p} className="rounded-full border border-[var(--border-subtle)] px-1.5 py-0.5 font-mono text-[9px] text-[var(--text-secondary)]">{p}</span>)}</div>
                </div>
              ))}</div>}
        </Card>
      )}

      {tab === "egress" && (
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3"><p className="text-xs text-[var(--text-muted)]">Outbound network boundary. Empty = local only.</p></div>
          {egress.isLoading ? <LoadingState label="Loading egress policy" />
            : egress.error ? <ErrorState problem={egress.error} onRetry={egress.refetch} />
            : endpoints.length === 0 ? <EmptyState title="No egress endpoints — Local only" />
            : <div className="divide-y divide-[var(--border-subtle)]">{endpoints.map((e, i) => (
                <div key={e.id || i} className="flex items-center gap-3 px-4 py-2.5 text-sm">
                  <StatusDot tone={e.enabled ? "success" : "neutral"} />
                  <span className="flex-1 truncate">{e.name || e.url}</span>
                  <Badge tone={e.enabled ? "info" : "neutral"}>{e.enabled ? "enabled" : "disabled"}</Badge>
                </div>
              ))}</div>}
        </Card>
      )}
    </Page>
  );
}

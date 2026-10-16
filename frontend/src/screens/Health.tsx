import { useQuery } from "@tanstack/react-query";
import { HeartPulse } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge, StatusDot } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";
import { ErrorState, LoadingState } from "../components/ui/States";
import { formatNumber } from "../lib/utils";

const TONE = (s: string) => {
  const v = (s || "").toLowerCase();
  if (["ok", "ready", "healthy", "up", "available", "pass"].some((t) => v.includes(t))) return "success";
  if (["degraded", "warn", "partial"].some((t) => v.includes(t))) return "warning";
  if (["down", "fail", "unavailable", "error"].some((t) => v.includes(t))) return "danger";
  return "neutral";
};

export function Health() {
  const { session } = useAuth();
  const aggregate = useQuery({ queryKey: [session?.tenant, "health-agg"], queryFn: () => apiFetch<any>("/enterprise/health/live"), retry: false });
  const system = useQuery({ queryKey: [session?.tenant, "admin-system-h"], queryFn: () => apiFetch<any>("/admin/system"), retry: false });
  const caps = useQuery({ queryKey: ["product-capabilities"], queryFn: () => apiFetch<any>("/product/capabilities"), retry: false });
  const gaps = useQuery({ queryKey: ["gaps-coverage"], queryFn: () => apiFetch<any>("/gaps/coverage"), retry: false });

  const components = aggregate.data?.components || aggregate.data?.checks || {};
  const compEntries = Array.isArray(components) ? components.map((c: any) => [c.name || c.component, c.status]) : Object.entries(components);

  return (
    <Page>
      <PageHeader title="Platform Health" overline="Independent operational signals" icon={<HeartPulse size={18} />} />

      {/* Product readiness — three separate counts (R9) */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Card className="p-4"><Overline>Capabilities</Overline><p className="mt-1 font-heading text-2xl font-bold">{formatNumber((caps.data?.capabilities || caps.data || []).length ?? caps.data?.count)}</p><p className="text-xs text-[var(--text-muted)]">product capabilities</p></Card>
        <Card className="p-4"><Overline>Gap coverage</Overline><p className="mt-1 font-heading text-2xl font-bold">{gaps.data?.covered ?? gaps.data?.coverage ?? "—"}</p><p className="text-xs text-[var(--text-muted)]">tracked gaps covered</p></Card>
        <Card className="p-4"><Overline>Model</Overline><div className="mt-1 flex items-center gap-2"><p className="font-heading text-lg font-bold capitalize">{system.data?.model?.status ?? "—"}</p><StatusDot tone={TONE(system.data?.model?.status) as any} /></div><p className="text-xs text-[var(--text-muted)]">inference status</p></Card>
      </div>

      <Card>
        <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Health aggregate</h3></div>
        {aggregate.isLoading ? <LoadingState label="Loading health" />
          : aggregate.error ? <ErrorState problem={aggregate.error} onRetry={aggregate.refetch} />
          : (
            <div className="p-4">
              {aggregate.data?.status && <div className="mb-3 flex items-center gap-2"><Overline>Overall</Overline><Badge tone={TONE(aggregate.data.status) as any}>{aggregate.data.status}</Badge></div>}
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                {compEntries.map(([name, st]: any) => (
                  <div key={name} className="flex items-center justify-between rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-3 py-2">
                    <span className="truncate text-xs text-[var(--text-secondary)]">{name}</span>
                    <div className="flex items-center gap-1.5"><span className="font-mono text-[10px]">{String(typeof st === "object" ? st.status : st)}</span><StatusDot tone={TONE(typeof st === "object" ? st.status : st) as any} /></div>
                  </div>
                ))}
              </div>
            </div>
          )}
      </Card>

      <Card className="p-4">
        <Overline>System</Overline>
        <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-3">
          {["graph", "model", "backup"].map((k) => (
            <div key={k} className="flex items-center justify-between rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-3 py-2">
              <span className="text-sm capitalize text-[var(--text-secondary)]">{k}</span>
              <div className="flex items-center gap-1.5"><span className="font-mono text-xs">{String(system.data?.[k]?.status ?? "—")}</span><StatusDot tone={TONE(system.data?.[k]?.status) as any} /></div>
            </div>
          ))}
        </div>
      </Card>
    </Page>
  );
}

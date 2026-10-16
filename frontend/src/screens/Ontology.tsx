import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Network } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader, Tabs } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { formatNumber } from "../lib/utils";

type Tab = "overview" | "validation" | "drift" | "packs";

export function Ontology() {
  const { session } = useAuth();
  const [tab, setTab] = useState<Tab>("overview");

  const schema = useQuery({ queryKey: [session?.tenant, "schema"], queryFn: () => apiFetch<any>("/graph/schema"), staleTime: 300_000 });
  const validate = useQuery({ queryKey: [session?.tenant, "ont-validate"], queryFn: () => apiFetch<any>("/ontology/validate?limit=50"), enabled: tab === "validation", retry: false });
  const drift = useQuery({ queryKey: [session?.tenant, "ont-drift"], queryFn: () => apiFetch<any>("/ontology/drift"), enabled: tab === "drift", retry: false });
  const packs = useQuery({ queryKey: [session?.tenant, "domain-packs"], queryFn: () => apiFetch<any>("/domain-packs"), enabled: tab === "packs", retry: false });

  const packList: any[] = packs.data?.packs || (Array.isArray(packs.data) ? packs.data : []);
  const violations: any[] = validate.data?.violations || validate.data?.results || (Array.isArray(validate.data) ? validate.data : []);

  return (
    <Page>
      <PageHeader title="Ontology" overline={`v${schema.data?.ontology_version ?? "—"} · schema v${schema.data?.schema_version ?? "—"}`} icon={<Network size={18} />} />
      <Tabs testPrefix="ontology-tab" active={tab} onChange={setTab} tabs={[
        { id: "overview", label: "Overview" }, { id: "validation", label: "Validation" }, { id: "drift", label: "Drift" }, { id: "packs", label: "Domain packs" },
      ]} />

      {tab === "overview" && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Card className="p-4"><Overline>Domains</Overline><p className="mt-1 font-heading text-2xl font-bold">{(schema.data?.domains || []).length}</p></Card>
            <Card className="p-4"><Overline>Vertex labels</Overline><p className="mt-1 font-heading text-2xl font-bold">{formatNumber(Object.keys(schema.data?.vertex_labels || {}).length)}</p></Card>
            <Card className="p-4"><Overline>Edge labels</Overline><p className="mt-1 font-heading text-2xl font-bold">{formatNumber(Object.keys(schema.data?.edge_labels || {}).length)}</p></Card>
            <Card className="p-4"><Overline>Indexes</Overline><p className="mt-1 font-heading text-2xl font-bold">{(schema.data?.indexes || []).length}</p></Card>
          </div>
          <Card className="p-4">
            <Overline>Domains</Overline>
            <div className="mt-2 flex flex-wrap gap-1.5">{(schema.data?.domains || []).map((d: string) => <Badge key={d} tone="neutral">{d}</Badge>)}</div>
          </Card>
        </div>
      )}

      {tab === "validation" && (
        <Card>
          {validate.isLoading ? <LoadingState label="Validating ontology" />
            : validate.error ? <ErrorState problem={validate.error} onRetry={validate.refetch} />
            : violations.length === 0 ? <EmptyState title="No validation violations" description="The ontology conforms to its SHACL shapes." />
            : <div className="divide-y divide-[var(--border-subtle)]">{violations.map((v, i) => (
                <div key={i} className="px-4 py-2.5 text-sm"><Badge tone="warning">{v.severity || v.level || "violation"}</Badge> <span className="ml-2 text-[var(--text-secondary)]">{v.message || v.detail || JSON.stringify(v).slice(0, 120)}</span></div>
              ))}</div>}
        </Card>
      )}

      {tab === "drift" && (
        <Card className="p-4">
          {drift.isLoading ? <LoadingState label="Checking drift" />
            : drift.error ? <ErrorState problem={drift.error} onRetry={drift.refetch} />
            : <pre className="overflow-x-auto font-mono text-[11px] leading-relaxed text-[var(--text-secondary)]">{JSON.stringify(drift.data, null, 2)}</pre>}
        </Card>
      )}

      {tab === "packs" && (
        <Card>
          {packs.isLoading ? <LoadingState label="Loading packs" />
            : packs.error ? <ErrorState problem={packs.error} onRetry={packs.refetch} />
            : packList.length === 0 ? <EmptyState title="No domain packs available" />
            : <div className="divide-y divide-[var(--border-subtle)]">{packList.map((p, i) => (
                <div key={p.name || i} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1"><p className="font-medium capitalize">{p.name || p.id}</p><p className="truncate text-xs text-[var(--text-muted)]">{p.description || ""}</p></div>
                  {p.active && <Badge tone="success">active</Badge>}
                </div>
              ))}</div>}
        </Card>
      )}
    </Page>
  );
}

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { ShieldCheck } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader, Tabs } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { shortId } from "../lib/utils";

type Tab = "debt" | "freshness" | "duplicates" | "contradictions";

export function Quality() {
  const { session } = useAuth();
  const [tab, setTab] = useState<Tab>("debt");

  const debt = useQuery({ queryKey: [session?.tenant, "k-debt"], queryFn: () => apiFetch<any>("/knowledge/debt"), enabled: tab === "debt", retry: false });
  const fresh = useQuery({ queryKey: [session?.tenant, "k-fresh"], queryFn: () => apiFetch<any>("/knowledge/freshness?stale_days=30"), enabled: tab === "freshness", retry: false });
  const dupes = useQuery({ queryKey: [session?.tenant, "id-candidates"], queryFn: () => apiFetch<any>("/identity/candidates?status=PENDING"), enabled: tab === "duplicates", retry: false });
  const contra = useQuery({ queryKey: [session?.tenant, "truth-contra"], queryFn: () => apiFetch<any>("/truth/contradictions"), enabled: tab === "contradictions", retry: false });

  const dupeList: any[] = dupes.data?.candidates || (Array.isArray(dupes.data) ? dupes.data : []);
  const contraList: any[] = contra.data?.contradictions || (Array.isArray(contra.data) ? contra.data : []);

  return (
    <Page>
      <PageHeader title="Quality" overline="Knowledge health, identity & truth" icon={<ShieldCheck size={18} />} />
      <Tabs testPrefix="quality-tab" active={tab} onChange={setTab} tabs={[
        { id: "debt", label: "Knowledge debt" }, { id: "freshness", label: "Freshness" }, { id: "duplicates", label: "Duplicates" }, { id: "contradictions", label: "Contradictions" },
      ]} />

      {tab === "debt" && (
        <Card className="p-4">
          {debt.isLoading ? <LoadingState label="Loading knowledge debt" />
            : debt.error ? <ErrorState problem={debt.error} onRetry={debt.refetch} />
            : <pre className="overflow-x-auto font-mono text-[11px] leading-relaxed text-[var(--text-secondary)]">{JSON.stringify(debt.data, null, 2)}</pre>}
        </Card>
      )}

      {tab === "freshness" && (
        <Card className="p-4">
          {fresh.isLoading ? <LoadingState label="Loading freshness" />
            : fresh.error ? <ErrorState problem={fresh.error} onRetry={fresh.refetch} />
            : <pre className="overflow-x-auto font-mono text-[11px] leading-relaxed text-[var(--text-secondary)]">{JSON.stringify(fresh.data, null, 2)}</pre>}
        </Card>
      )}

      {tab === "duplicates" && (
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3"><p className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Pending identity candidates</p></div>
          {dupes.isLoading ? <LoadingState label="Loading candidates" />
            : dupes.error ? <ErrorState problem={dupes.error} onRetry={dupes.refetch} />
            : dupeList.length === 0 ? <EmptyState title="No pending duplicate candidates" />
            : <div className="divide-y divide-[var(--border-subtle)]">{dupeList.map((c, i) => (
                <div key={c.id || i} className="px-4 py-2.5 text-sm">
                  <Badge tone="warning">{c.candidate_type || c.kind || "merge"}</Badge>
                  <span className="ml-2 font-mono text-xs text-[var(--text-secondary)]">{(c.members || c.entities || []).map((m: any) => shortId(String(m))).join("  ≈  ") || c.summary || c.id}</span>
                </div>
              ))}</div>}
        </Card>
      )}

      {tab === "contradictions" && (
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3"><p className="text-xs text-[var(--text-muted)]">Truth/SKOS state is process-local and resets on API restart.</p></div>
          {contra.isLoading ? <LoadingState label="Loading contradictions" />
            : contra.error ? <ErrorState problem={contra.error} onRetry={contra.refetch} />
            : contraList.length === 0 ? <EmptyState title="No contradictions detected" />
            : <div className="divide-y divide-[var(--border-subtle)]">{contraList.map((c, i) => (
                <div key={i} className="px-4 py-2.5 font-mono text-xs text-[var(--text-secondary)]">{c.subject} · {c.predicate} — {JSON.stringify(c.values || c).slice(0, 100)}</div>
              ))}</div>}
        </Card>
      )}
    </Page>
  );
}

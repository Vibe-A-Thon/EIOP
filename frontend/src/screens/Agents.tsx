import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Bot } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader, Tabs } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { shortId } from "../lib/utils";

type Tab = "agents" | "proposals" | "loops" | "recovery";

export function Agents() {
  const { session } = useAuth();
  const qc = useQueryClient();
  const [tab, setTab] = useState<Tab>("agents");

  const agents = useQuery({ queryKey: [session?.tenant, "agents"], queryFn: () => apiFetch<any>("/agents"), enabled: tab === "agents", retry: false });
  const proposals = useQuery({ queryKey: [session?.tenant, "proposals"], queryFn: () => apiFetch<any>("/agents/proposals?status=PENDING"), enabled: tab === "proposals", retry: false });
  const loops = useQuery({ queryKey: [session?.tenant, "loops"], queryFn: () => apiFetch<any>("/loops/catalog"), enabled: tab === "loops", retry: false });
  const recoveries = useQuery({ queryKey: [session?.tenant, "recoveries"], queryFn: () => apiFetch<any>("/agents/mesh/recoveries?status=PENDING"), enabled: tab === "recovery", retry: false });

  const agentList: any[] = agents.data?.agents || (Array.isArray(agents.data) ? agents.data : []);
  const proposalList: any[] = proposals.data?.proposals || (Array.isArray(proposals.data) ? proposals.data : []);
  const loopList: any[] = loops.data?.loops || loops.data?.catalog || (Array.isArray(loops.data) ? loops.data : []);
  const recoveryList: any[] = recoveries.data?.recoveries || (Array.isArray(recoveries.data) ? recoveries.data : []);

  const decide = async (id: string, action: "approve" | "reject") => {
    await apiFetch(`/agents/proposals/${encodeURIComponent(id)}/${action}`, { method: "POST", body: { actor_id: session?.principal.id || "operator" } }).catch(() => {});
    qc.invalidateQueries({ queryKey: [session?.tenant, "proposals"] });
  };

  return (
    <Page>
      <PageHeader title="Agents" overline="Autonomous runs, approvals & loops" icon={<Bot size={18} />} />
      <Tabs testPrefix="agents-tab" active={tab} onChange={setTab} tabs={[
        { id: "agents", label: "Agents" }, { id: "proposals", label: "Proposals" }, { id: "loops", label: "Loops" }, { id: "recovery", label: "Recovery" },
      ]} />

      {tab === "agents" && (
        <Card>
          {agents.isLoading ? <LoadingState label="Loading agents" />
            : agents.error ? <ErrorState problem={agents.error} onRetry={agents.refetch} />
            : agentList.length === 0 ? <EmptyState title="No agents registered" icon={<Bot size={22} />} />
            : <div className="divide-y divide-[var(--border-subtle)]">{agentList.map((a, i) => (
                <div key={a.id || i} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1"><p className="font-medium">{a.id || a.name}</p><p className="truncate font-mono text-[10px] text-[var(--text-muted)]">{(a.capabilities || []).join(", ") || a.version}</p></div>
                  {a.risk && <Badge tone="warning">{a.risk}</Badge>}
                  <Badge tone={a.enabled === false ? "neutral" : "success"}>{a.enabled === false ? "disabled" : "enabled"}</Badge>
                </div>
              ))}</div>}
        </Card>
      )}

      {tab === "proposals" && (
        <Card>
          <div className="border-b border-[var(--border-subtle)] px-4 py-3"><p className="text-xs text-[var(--text-muted)]">Approval records a decision only — it does not apply the mutation.</p></div>
          {proposals.isLoading ? <LoadingState label="Loading proposals" />
            : proposals.error ? <ErrorState problem={proposals.error} onRetry={proposals.refetch} />
            : proposalList.length === 0 ? <EmptyState title="No pending proposals" />
            : <div className="divide-y divide-[var(--border-subtle)]">{proposalList.map((p, i) => (
                <div key={p.id || i} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1"><p className="truncate text-sm">{p.summary || p.title || shortId(p.id || "")}</p><p className="font-mono text-[10px] text-[var(--text-muted)]">{p.id}</p></div>
                  <Button size="sm" variant="outline" data-testid="proposal-approve" onClick={() => decide(p.id, "approve")}>Approve</Button>
                  <Button size="sm" variant="ghost" data-testid="proposal-reject" onClick={() => decide(p.id, "reject")}>Reject</Button>
                </div>
              ))}</div>}
        </Card>
      )}

      {tab === "loops" && (
        <Card>
          {loops.isLoading ? <LoadingState label="Loading loops" />
            : loops.error ? <ErrorState problem={loops.error} onRetry={loops.refetch} />
            : loopList.length === 0 ? <EmptyState title="No loops in catalog" />
            : <div className="divide-y divide-[var(--border-subtle)]">{loopList.map((l, i) => (
                <div key={l.name || i} className="px-4 py-3"><p className="font-medium">{l.name || l.id}</p><p className="truncate text-xs text-[var(--text-muted)]">{l.description || ""}</p></div>
              ))}</div>}
        </Card>
      )}

      {tab === "recovery" && (
        <Card>
          {recoveries.isLoading ? <LoadingState label="Loading recoveries" />
            : recoveries.error ? <ErrorState problem={recoveries.error} onRetry={recoveries.refetch} />
            : recoveryList.length === 0 ? <EmptyState title="No pending recoveries" />
            : <div className="divide-y divide-[var(--border-subtle)]">{recoveryList.map((r, i) => (
                <div key={r.recovery_id || i} className="px-4 py-2.5 font-mono text-xs text-[var(--text-secondary)]">{r.recovery_id || JSON.stringify(r).slice(0, 100)}</div>
              ))}</div>}
        </Card>
      )}
    </Page>
  );
}

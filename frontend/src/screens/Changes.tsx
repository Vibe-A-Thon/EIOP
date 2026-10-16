import { useQuery } from "@tanstack/react-query";
import { GitCompareArrows } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { relativeTime, shortId } from "../lib/utils";

const OP_TONE: Record<string, any> = { CREATE: "success", ADD: "success", UPDATE: "info", MODIFY: "info", DELETE: "danger", REMOVE: "danger" };

export function Changes() {
  const { session } = useAuth();
  const journal = useQuery({
    queryKey: [session?.tenant, "change-journal"],
    queryFn: () => apiFetch<any>("/change-journal?limit=80"),
    retry: false,
  });
  const stats = useQuery({
    queryKey: [session?.tenant, "diff-stats"],
    queryFn: () => apiFetch<any>("/enterprise/diff/stats"),
    retry: false,
  });

  const entries: any[] = journal.data?.entries || journal.data?.changes || (Array.isArray(journal.data) ? journal.data : []);

  return (
    <Page>
      <PageHeader title="Changes" overline="Change journal & graph diff" icon={<GitCompareArrows size={18} />} />

      {stats.data && (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {Object.entries(stats.data).filter(([, v]) => typeof v === "number").slice(0, 4).map(([k, v]: any) => (
            <Card key={k} className="p-4">
              <Overline>{k.replace(/_/g, " ")}</Overline>
              <p className="mt-1 font-heading text-2xl font-bold">{v}</p>
            </Card>
          ))}
        </div>
      )}

      <Card>
        <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Recent changes</h3></div>
        {journal.isLoading ? <LoadingState label="Loading change journal" />
          : journal.error ? <ErrorState problem={journal.error} onRetry={journal.refetch} />
          : entries.length === 0 ? <EmptyState title="No recorded changes" icon={<GitCompareArrows size={22} />} />
          : (
            <div className="divide-y divide-[var(--border-subtle)]">
              {entries.map((e, i) => {
                const op = (e.operation || e.op || e.change_type || e.kind || "CHANGE").toString().toUpperCase();
                const target = e.canonical_id || e.entity_id || e.target || e.subject;
                return (
                  <div key={e.id || e.change_id || i} className="flex items-center gap-3 px-4 py-2.5 text-sm">
                    <Badge tone={OP_TONE[op] || "neutral"}>{op}</Badge>
                    <span className="truncate font-mono text-xs text-[var(--text-secondary)]">{target ? shortId(String(target)) : e.summary || "change"}</span>
                    <span className="ml-auto shrink-0 font-mono text-[11px] text-[var(--text-muted)]">{relativeTime(e.timestamp || e.at || e.created_at || e.recorded_at)}</span>
                  </div>
                );
              })}
            </div>
          )}
      </Card>
    </Page>
  );
}

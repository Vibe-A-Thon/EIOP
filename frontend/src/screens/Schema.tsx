import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { Network, Search } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { LoadingState, ErrorState } from "../components/ui/States";
import { cn, formatNumber } from "../lib/utils";

export function Schema() {
  const { session } = useAuth();
  const [tab, setTab] = useState<"vertex" | "edge">("vertex");
  const [q, setQ] = useState("");

  const schema = useQuery({
    queryKey: [session?.tenant, "schema"],
    queryFn: () => apiFetch<any>("/graph/schema"),
    staleTime: 300_000,
  });

  const vertexRows = useMemo(() => {
    const labels = schema.data?.vertex_labels || {};
    return Object.entries(labels)
      .map(([label, meta]: any) => ({ label, ...meta }))
      .filter((r) => r.label.toLowerCase().includes(q.toLowerCase()))
      .sort((a, b) => (b.instance_count || 0) - (a.instance_count || 0));
  }, [schema.data, q]);

  const edgeRows = useMemo(() => {
    const labels = schema.data?.edge_labels || {};
    return Object.entries(labels)
      .map(([label, meta]: any) => ({ label, ...meta }))
      .filter((r) => r.label.toLowerCase().includes(q.toLowerCase()));
  }, [schema.data, q]);

  if (schema.isLoading) return <LoadingState label="Loading schema" />;
  if (schema.error) return <ErrorState problem={schema.error} onRetry={schema.refetch} />;

  return (
    <div className="mx-auto max-w-5xl space-y-5 p-6">
      <div className="flex items-center gap-2">
        <Network size={18} className="text-cyan-400" />
        <div>
          <h1 className="font-heading text-2xl font-bold tracking-tight">Schema</h1>
          <p className="text-xs text-[var(--text-muted)]">
            Ontology {schema.data?.ontology_version} · schema {schema.data?.schema_version}
          </p>
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {(schema.data?.domains || []).map((d: string) => (
          <Badge key={d} tone="neutral">{d}</Badge>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-1 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] p-0.5">
          {(["vertex", "edge"] as const).map((t) => (
            <button
              key={t}
              data-testid={`schema-tab-${t}`}
              onClick={() => setTab(t)}
              className={cn(
                "rounded-[3px] px-3 py-1.5 text-xs capitalize transition-colors",
                tab === t ? "bg-[var(--bg-hover)] text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]",
              )}
            >
              {t} labels ({t === "vertex" ? Object.keys(schema.data?.vertex_labels || {}).length : Object.keys(schema.data?.edge_labels || {}).length})
            </button>
          ))}
        </div>
        <div className="flex flex-1 items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-2.5">
          <Search size={14} className="text-[var(--text-muted)]" />
          <input
            data-testid="schema-search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Filter labels…"
            className="h-8 w-full bg-transparent text-xs outline-none"
          />
        </div>
      </div>

      <Card>
        {tab === "vertex" ? (
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-[var(--border-subtle)] text-[var(--text-muted)]">
                <th className="px-4 py-2.5 font-mono text-[10px] uppercase tracking-wider">Label</th>
                <th className="px-4 py-2.5 font-mono text-[10px] uppercase tracking-wider">Domain</th>
                <th className="px-4 py-2.5 text-right font-mono text-[10px] uppercase tracking-wider">Instances</th>
              </tr>
            </thead>
            <tbody>
              {vertexRows.map((r) => (
                <tr key={r.label} className="border-b border-[var(--border-subtle)] transition-colors last:border-0 hover:bg-[var(--bg-hover)]">
                  <td className="px-4 py-2.5 font-medium">{r.label}</td>
                  <td className="px-4 py-2.5"><Badge tone="neutral">{r.domain}</Badge></td>
                  <td className="px-4 py-2.5 text-right font-mono text-[var(--text-secondary)]">{formatNumber(r.instance_count)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-[var(--border-subtle)] text-[var(--text-muted)]">
                <th className="px-4 py-2.5 font-mono text-[10px] uppercase tracking-wider">Edge label</th>
                <th className="px-4 py-2.5 font-mono text-[10px] uppercase tracking-wider">Source → Target</th>
              </tr>
            </thead>
            <tbody>
              {edgeRows.map((r) => (
                <tr key={r.label} className="border-b border-[var(--border-subtle)] transition-colors last:border-0 hover:bg-[var(--bg-hover)]">
                  <td className="px-4 py-2.5 font-medium">{r.label}</td>
                  <td className="px-4 py-2.5 font-mono text-[11px] text-[var(--text-muted)]">
                    {(r.source_labels || []).slice(0, 3).join(", ") || "*"} → {(r.target_labels || []).slice(0, 3).join(", ") || "*"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  );
}

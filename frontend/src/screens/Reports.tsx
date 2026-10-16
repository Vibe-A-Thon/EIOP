import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { FileBarChart, Loader2, Play } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";

export function Reports() {
  const { session } = useAuth();
  const [rendering, setRendering] = useState<string | null>(null);
  const [rendered, setRendered] = useState<any | null>(null);

  const templates = useQuery({ queryKey: [session?.tenant, "report-templates"], queryFn: () => apiFetch<any>("/reports/templates"), retry: false });
  const schedules = useQuery({ queryKey: [session?.tenant, "report-schedules"], queryFn: () => apiFetch<any>("/reports/schedules"), retry: false });

  const tplList: any[] = templates.data?.templates || (Array.isArray(templates.data) ? templates.data : []);
  const schList: any[] = schedules.data?.schedules || (Array.isArray(schedules.data) ? schedules.data : []);

  const render = async (tpl: any) => {
    const id = tpl.template_id || tpl.id;
    setRendering(id); setRendered(null);
    try {
      const r = await apiFetch<any>(`/reports/render?template_id=${encodeURIComponent(id)}&report_format=json`, {
        method: "POST",
        body: { title: tpl.name || id, params: {}, findings: [], narrative: "" },
      });
      setRendered(r);
    } catch (e: any) {
      setRendered({ error: e?.problem?.detail || e?.message || "Render failed" });
    } finally { setRendering(null); }
  };

  return (
    <Page>
      <PageHeader title="Reports" overline="Templates, rendering & schedules" icon={<FileBarChart size={18} />} />

      <Card>
        <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Templates</h3></div>
        {templates.isLoading ? <LoadingState label="Loading templates" />
          : templates.error ? <ErrorState problem={templates.error} onRetry={templates.refetch} />
          : tplList.length === 0 ? <EmptyState title="No report templates" icon={<FileBarChart size={22} />} />
          : <div className="divide-y divide-[var(--border-subtle)]">{tplList.map((t, i) => {
              const id = t.template_id || t.id;
              return (
                <div key={id || i} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1"><p className="font-medium">{t.name || id}</p><p className="truncate text-xs text-[var(--text-muted)]">{t.description || t.intent || ""}</p></div>
                  <Button size="sm" variant="outline" data-testid="report-render" onClick={() => render(t)} disabled={rendering === id}>
                    {rendering === id ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />} Render
                  </Button>
                </div>
              );
            })}</div>}
      </Card>

      {rendered && (
        <Card className="p-4" data-testid="report-output">
          {rendered.error ? <p className="text-sm text-red-300">{rendered.error}</p> : (
            <>
              <div className="mb-2 flex items-center gap-2"><Badge tone="success">rendered</Badge>{rendered.sha256 && <span className="font-mono text-[10px] text-[var(--text-muted)]">sha {String(rendered.sha256).slice(0, 12)}</span>}</div>
              <pre className="max-h-80 overflow-auto font-mono text-[11px] leading-relaxed text-[var(--text-secondary)]">{JSON.stringify(rendered, null, 2)}</pre>
            </>
          )}
        </Card>
      )}

      <Card>
        <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Schedules</h3></div>
        {schList.length === 0 ? <EmptyState title="No scheduled reports" />
          : <div className="divide-y divide-[var(--border-subtle)]">{schList.map((s, i) => (
              <div key={s.id || i} className="flex items-center gap-3 px-4 py-2.5 text-sm"><span className="flex-1 truncate">{s.name || s.template_id}</span><Badge tone="info">{s.recurrence || "—"}</Badge></div>
            ))}</div>}
      </Card>
    </Page>
  );
}

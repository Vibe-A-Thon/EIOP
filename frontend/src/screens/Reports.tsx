import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { CalendarClock, FileBarChart, Loader2, Play, Plus, Trash2, Zap } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { relativeTime } from "../lib/utils";

const RECURRENCES = ["daily", "weekly", "monthly"] as const;

export function Reports() {
  const { session } = useAuth();
  const qc = useQueryClient();
  const [rendering, setRendering] = useState<string | null>(null);
  const [rendered, setRendered] = useState<any | null>(null);

  // schedule form
  const [sTemplate, setSTemplate] = useState("");
  const [sName, setSName] = useState("");
  const [sRecurrence, setSRecurrence] = useState<(typeof RECURRENCES)[number]>("weekly");
  const [sFormat, setSFormat] = useState("json");
  const [creating, setCreating] = useState(false);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const templates = useQuery({ queryKey: [session?.tenant, "report-templates"], queryFn: () => apiFetch<any>("/reports/templates"), retry: false });
  const schedules = useQuery({ queryKey: [session?.tenant, "report-schedules"], queryFn: () => apiFetch<any>("/reports/schedules"), retry: false });
  const due = useQuery({ queryKey: [session?.tenant, "report-schedules-due"], queryFn: () => apiFetch<any>("/reports/schedules/due"), retry: false });

  const tplList: any[] = templates.data?.templates || (Array.isArray(templates.data) ? templates.data : []);
  const schList: any[] = schedules.data?.schedules || (Array.isArray(schedules.data) ? schedules.data : []);
  const dueList: any[] = due.data?.schedules || (Array.isArray(due.data) ? due.data : []);
  const dueIds = useMemo(() => new Set(dueList.map((d) => d.schedule_id)), [dueList]);

  const refetchSchedules = () => { schedules.refetch(); due.refetch(); qc.invalidateQueries({ queryKey: [session?.tenant, "report-schedules"] }); };

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

  const createSchedule = async () => {
    const tpl = sTemplate || tplList[0]?.template_id || tplList[0]?.id;
    if (!tpl) return;
    const name = sName.trim() || `${tpl} (${sRecurrence})`;
    setCreating(true); setNotice(null);
    try {
      const qs = new URLSearchParams({ template_id: tpl, name, recurrence: sRecurrence, report_format: sFormat });
      await apiFetch<any>(`/reports/schedules?${qs.toString()}`, { method: "POST" });
      setSName(""); setNotice(`Schedule "${name}" created.`);
      refetchSchedules();
    } catch (e: any) {
      setNotice(e?.problem?.detail || e?.message || "Could not create schedule");
    } finally { setCreating(false); }
  };

  const markRun = async (id: string) => {
    setBusyId(id);
    try { await apiFetch<any>(`/reports/schedules/${encodeURIComponent(id)}/mark-run`, { method: "POST" }); refetchSchedules(); }
    finally { setBusyId(null); }
  };

  const removeSchedule = async (id: string) => {
    setBusyId(id);
    try { await apiFetch<any>(`/reports/schedules/${encodeURIComponent(id)}`, { method: "DELETE" }); refetchSchedules(); }
    finally { setBusyId(null); }
  };

  return (
    <Page>
      <PageHeader title="Reports" overline="Templates · rendering · recurring schedules" icon={<FileBarChart size={18} />} />

      <Card>
        <div className="border-b border-[var(--border-subtle)] px-4 py-3"><h3 className="font-heading text-sm font-semibold">Templates</h3></div>
        {templates.isLoading ? <LoadingState label="Loading templates" />
          : templates.error ? <ErrorState problem={templates.error} onRetry={templates.refetch} />
          : tplList.length === 0 ? <EmptyState title="No report templates" icon={<FileBarChart size={22} />} />
          : <div className="divide-y divide-[var(--border-subtle)]">{tplList.map((t, i) => {
              const id = t.template_id || t.id;
              return (
                <div key={id || i} className="flex items-center gap-3 px-4 py-3 transition-colors hover:bg-[var(--bg-hover)]/40">
                  <div className="min-w-0 flex-1"><p className="font-medium">{t.name || id}</p><p className="truncate text-xs text-[var(--text-muted)]">{t.description || t.intent || ""}</p></div>
                  <Button size="sm" variant="outline" data-testid="report-render" onClick={() => render(t)} disabled={rendering === id}>
                    {rendering === id ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />} Render
                  </Button>
                </div>
              );
            })}</div>}
      </Card>

      <AnimatePresence>
        {rendered && (
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
            <Card className="p-4" data-testid="report-output">
              {rendered.error ? <p className="text-sm text-red-300">{rendered.error}</p> : (
                <>
                  <div className="mb-2 flex items-center gap-2"><Badge tone="success">rendered</Badge>{rendered.sha256 && <span className="font-mono text-[10px] text-[var(--text-muted)]">sha {String(rendered.sha256).slice(0, 12)}</span>}</div>
                  <pre className="max-h-80 overflow-auto font-mono text-[11px] leading-relaxed text-[var(--text-secondary)]">{JSON.stringify(rendered, null, 2)}</pre>
                </>
              )}
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Schedules */}
      <Card>
        <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-3">
          <h3 className="flex items-center gap-2 font-heading text-sm font-semibold"><CalendarClock size={15} className="text-cyan-400" /> Recurring schedules</h3>
          {dueList.length > 0 && <Badge tone="warning" testId="schedules-due-count"><Zap size={10} /> {dueList.length} due now</Badge>}
        </div>

        {/* Create form */}
        <div className="flex flex-wrap items-end gap-2 border-b border-[var(--border-subtle)] bg-[var(--bg-void)]/40 px-4 py-3" data-testid="schedule-create-form">
          <div className="min-w-[180px] flex-1">
            <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Template</label>
            <select data-testid="schedule-template" value={sTemplate} onChange={(e) => setSTemplate(e.target.value)} className="h-8 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]">
              <option value="">{tplList[0] ? `${tplList[0].name || tplList[0].template_id} (default)` : "No templates"}</option>
              {tplList.map((t) => { const id = t.template_id || t.id; return <option key={id} value={id}>{t.name || id}</option>; })}
            </select>
          </div>
          <div className="min-w-[160px] flex-1">
            <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Name</label>
            <input data-testid="schedule-name" value={sName} onChange={(e) => setSName(e.target.value)} placeholder="Weekly impact digest" className="h-8 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]" />
          </div>
          <div>
            <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Recurrence</label>
            <select data-testid="schedule-recurrence" value={sRecurrence} onChange={(e) => setSRecurrence(e.target.value as any)} className="h-8 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs capitalize outline-none focus:border-[var(--accent)]">
              {RECURRENCES.map((r) => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label className="mb-1 block font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">Format</label>
            <select data-testid="schedule-format" value={sFormat} onChange={(e) => setSFormat(e.target.value)} className="h-8 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2 text-xs outline-none focus:border-[var(--accent)]">
              {["json", "markdown"].map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <Button size="sm" variant="primary" data-testid="schedule-create" onClick={createSchedule} disabled={creating || tplList.length === 0}>
            {creating ? <Loader2 size={13} className="animate-spin" /> : <Plus size={13} />} Schedule
          </Button>
        </div>

        {notice && <div className="px-4 py-2 text-xs text-cyan-300" data-testid="schedule-notice">{notice}</div>}

        {schList.length === 0 ? <EmptyState title="No scheduled reports" description="Create a recurring schedule above to generate reports automatically." icon={<CalendarClock size={22} />} />
          : <div className="divide-y divide-[var(--border-subtle)]" data-testid="schedule-list">
              <AnimatePresence initial={false}>
                {schList.map((s) => {
                  const id = s.schedule_id || s.id;
                  const isDue = dueIds.has(id);
                  return (
                    <motion.div key={id} layout initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, x: -12 }} className="flex items-center gap-3 px-4 py-3" data-testid="schedule-row">
                      <div className="min-w-0 flex-1">
                        <p className="flex items-center gap-2 font-medium">{s.name || s.template_id}{isDue && <Badge tone="warning"><Zap size={9} /> due</Badge>}</p>
                        <p className="truncate font-mono text-[11px] text-[var(--text-muted)]">{s.template_id} · {s.report_format} · last run {s.last_run_at ? relativeTime(s.last_run_at) : "never"}</p>
                      </div>
                      <Badge tone="info" className="capitalize">{s.recurrence}</Badge>
                      <Button size="sm" variant="outline" data-testid="schedule-mark-run" onClick={() => markRun(id)} disabled={busyId === id}>
                        {busyId === id ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />} Mark run
                      </Button>
                      <Button size="sm" variant="ghost" data-testid="schedule-delete" onClick={() => removeSchedule(id)} disabled={busyId === id} className="text-[var(--text-muted)] hover:text-red-300">
                        <Trash2 size={13} />
                      </Button>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
            </div>}
      </Card>
    </Page>
  );
}

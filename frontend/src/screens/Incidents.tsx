import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Activity, Plus, X } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { relativeTime } from "../lib/utils";

const SEV_TONE: Record<string, any> = { SEV1: "danger", SEV2: "danger", SEV3: "warning", SEV4: "info" };
const STATE_TONE: Record<string, any> = { OPEN: "danger", INVESTIGATING: "warning", MITIGATED: "info", RESOLVED: "success", CLOSED: "neutral" };

export function Incidents() {
  const { session } = useAuth();
  const qc = useQueryClient();
  const [showNew, setShowNew] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", severity: "SEV3" });
  const [busy, setBusy] = useState(false);

  const incidents = useQuery({
    queryKey: [session?.tenant, "incidents"],
    queryFn: () => apiFetch<any>("/platform/incidents?limit=50"),
    retry: false,
  });
  const list: any[] = incidents.data?.incidents || (Array.isArray(incidents.data) ? incidents.data : []);

  const create = async () => {
    setBusy(true);
    try {
      await apiFetch("/platform/incidents", {
        method: "POST",
        body: { title: form.title, description: form.description, severity: form.severity, reporter: session?.principal.username || "operator" },
      });
      setShowNew(false); setForm({ title: "", description: "", severity: "SEV3" });
      qc.invalidateQueries({ queryKey: [session?.tenant, "incidents"] });
    } catch { /* surfaced via list refresh */ } finally { setBusy(false); }
  };

  return (
    <Page>
      <PageHeader title="Incidents" overline="Operational incidents & triage" icon={<Activity size={18} />}
        actions={<Button variant="primary" data-testid="incident-new" onClick={() => setShowNew(true)}><Plus size={14} /> New incident</Button>} />

      <Card>
        {incidents.isLoading ? <LoadingState label="Loading incidents" />
          : incidents.error ? <ErrorState problem={incidents.error} onRetry={incidents.refetch} />
          : list.length === 0 ? <EmptyState title="No incidents" description="Declare an incident to begin triage and correlation." icon={<Activity size={22} />} />
          : (
            <div className="divide-y divide-[var(--border-subtle)]">
              {list.map((inc, i) => (
                <div key={inc.id || inc.incident_id || i} className="flex items-center gap-3 px-4 py-3">
                  <Badge tone={SEV_TONE[inc.severity] || "neutral"}>{inc.severity}</Badge>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium">{inc.title}</p>
                    <p className="truncate font-mono text-[10px] text-[var(--text-muted)]">{inc.id || inc.incident_id} · {relativeTime(inc.created_at || inc.opened_at)}</p>
                  </div>
                  <Badge tone={STATE_TONE[(inc.state || inc.status || "").toUpperCase()] || "neutral"}>{inc.state || inc.status || "—"}</Badge>
                </div>
              ))}
            </div>
          )}
      </Card>

      {showNew && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4" data-testid="incident-modal">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setShowNew(false)} />
          <Card className="relative w-full max-w-md animate-fade-in">
            <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-3">
              <h3 className="font-heading text-sm font-semibold">Declare incident</h3>
              <button onClick={() => setShowNew(false)} className="text-[var(--text-muted)] hover:text-[var(--text-primary)]"><X size={15} /></button>
            </div>
            <div className="space-y-3 p-4">
              <input data-testid="incident-title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="Title" className="h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" />
              <textarea data-testid="incident-desc" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="Description" rows={3} className="w-full resize-none rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 py-2 text-sm outline-none focus:border-[var(--accent)]" />
              <select data-testid="incident-sev" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })} className="h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none">
                {["SEV1", "SEV2", "SEV3", "SEV4"].map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div className="flex justify-end gap-2 border-t border-[var(--border-subtle)] px-4 py-3">
              <Button variant="ghost" onClick={() => setShowNew(false)}>Cancel</Button>
              <Button variant="primary" data-testid="incident-create" onClick={create} disabled={busy || !form.title.trim() || !form.description.trim()}>Declare</Button>
            </div>
          </Card>
        </div>
      )}
    </Page>
  );
}

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Activity, ChevronUp, Radio } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { StatusDot } from "../components/ui/Badge";
import { cn, relativeTime } from "../lib/utils";

interface GraphEvent {
  id?: string;
  event_id?: string;
  type?: string;
  timestamp?: string;
  created_at?: string;
  payload?: Record<string, any>;
}

function groupOf(type?: string): string {
  const t = (type || "").toLowerCase();
  if (t.startsWith("vertex") || t.startsWith("edge") || t.includes("entity") || t.includes("relation"))
    return "Graph";
  if (t.includes("ingest") || t.includes("source")) return "Ingestion";
  if (t.includes("valid") || t.includes("quality")) return "Validation";
  if (t.includes("ontology") || t.includes("version")) return "Ontology";
  if (t.includes("identity")) return "Identity";
  if (t.includes("trust")) return "Trust";
  return "Other";
}

export function Dock() {
  const { session } = useAuth();
  const [open, setOpen] = useState(false);

  const { data, isError } = useQuery({
    queryKey: [session?.tenant, "graph-events"],
    queryFn: () => apiFetch<any>("/graph/events?limit=50"),
    refetchInterval: document.visibilityState === "visible" ? 5000 : 30000,
  });

  const events: GraphEvent[] = (data?.events || []).slice().reverse();
  const latest = events[0];

  return (
    <div
      data-testid="activity-dock"
      className="shrink-0 border-t border-[var(--border-subtle)] bg-[var(--bg-surface)]"
    >
      <button
        onClick={() => setOpen((o) => !o)}
        data-testid="activity-dock-toggle"
        className="flex h-9 w-full items-center gap-3 px-4 text-xs transition-colors hover:bg-[var(--bg-hover)]"
      >
        <span className="flex items-center gap-1.5 font-mono uppercase tracking-wider text-[var(--text-muted)]">
          <Radio size={12} /> Live updates: polling
        </span>
        <StatusDot tone={isError ? "danger" : "success"} pulse={!isError} />
        <span className="text-[var(--text-secondary)]">
          {events.length} event{events.length === 1 ? "" : "s"}
        </span>
        {latest && !open && (
          <span className="ml-2 flex items-center gap-2 truncate font-mono text-[11px] text-[var(--text-muted)]">
            <Activity size={11} />
            <span className="truncate">{latest.type}</span>
          </span>
        )}
        <ChevronUp
          size={14}
          className={cn("ml-auto text-[var(--text-muted)] transition-transform", open && "rotate-180")}
        />
      </button>

      {open && (
        <div className="max-h-56 overflow-y-auto border-t border-[var(--border-subtle)] p-2 animate-fade-in">
          {events.length === 0 ? (
            <p className="py-6 text-center text-xs text-[var(--text-muted)]">No recent activity.</p>
          ) : (
            <ul className="space-y-0.5">
              {events.map((e, i) => (
                <li
                  key={e.id || e.event_id || i}
                  className="flex items-center gap-3 rounded-sm px-2 py-1.5 text-xs transition-colors hover:bg-[var(--bg-hover)]"
                >
                  <span className="w-20 shrink-0 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                    {groupOf(e.type)}
                  </span>
                  <span className="truncate font-mono text-[var(--text-secondary)]">{e.type}</span>
                  <span className="ml-auto shrink-0 font-mono text-[10px] text-[var(--text-muted)]">
                    {relativeTime(e.timestamp || e.created_at)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

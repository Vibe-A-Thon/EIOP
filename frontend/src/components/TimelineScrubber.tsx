import { useMemo, useRef, useState } from "react";
import { BarChart3, MapPin } from "lucide-react";
import { Overline } from "./ui/Card";

export interface TimelineEvent {
  iso: string;
  t: number;
  changes: number;
  label: string;
  status?: string;
}

interface Props {
  events: TimelineEvent[];
  mode: "asof" | "compare" | "playback";
  valueIso?: string;      // asof playhead
  fromIso?: string;       // compare from
  toIso?: string;         // compare to
  onPick?: (iso: string) => void;        // asof click
  onRange?: (fromIso: string, toIso: string) => void; // compare click
}

const BUCKETS = 32;

export function TimelineScrubber({ events, mode, valueIso, fromIso, toIso, onPick, onRange }: Props) {
  const trackRef = useRef<HTMLDivElement>(null);
  const [hover, setHover] = useState<{ x: number; iso: string } | null>(null);

  const { min, max, buckets, maxCount, total } = useMemo(() => {
    const times = events.map((e) => e.t).filter((n) => Number.isFinite(n));
    let lo = times.length ? Math.min(...times) : Date.now() - 3600_000;
    let hi = times.length ? Math.max(...times) : Date.now();
    if (hi - lo < 60_000) { const pad = 1800_000; lo -= pad; hi += pad; } // expand tiny spans
    const span = hi - lo || 1;
    const b = Array.from({ length: BUCKETS }, () => 0);
    events.forEach((e) => {
      const idx = Math.min(BUCKETS - 1, Math.max(0, Math.floor(((e.t - lo) / span) * BUCKETS)));
      if (Number.isFinite(e.t)) b[idx] += e.changes || 1;
    });
    return { min: lo, max: hi, buckets: b, maxCount: Math.max(1, ...b), total: events.length };
  }, [events]);

  const span = max - min || 1;
  const pct = (iso?: string) => {
    if (!iso) return null;
    const t = new Date(iso).getTime();
    if (!Number.isFinite(t)) return null;
    return Math.min(100, Math.max(0, ((t - min) / span) * 100));
  };
  const isoAtX = (clientX: number) => {
    const el = trackRef.current;
    if (!el) return new Date(min).toISOString();
    const r = el.getBoundingClientRect();
    const ratio = Math.min(1, Math.max(0, (clientX - r.left) / r.width));
    return new Date(min + ratio * span).toISOString();
  };

  const handleClick = (e: React.MouseEvent) => {
    const iso = isoAtX(e.clientX);
    if (mode === "asof") onPick?.(iso);
    else if (mode === "compare") {
      // set the nearer of from/to
      const t = new Date(iso).getTime();
      const fT = fromIso ? new Date(fromIso).getTime() : min;
      const tT = toIso ? new Date(toIso).getTime() : max;
      if (Math.abs(t - fT) <= Math.abs(t - tT)) onRange?.(iso, toIso || new Date(max).toISOString());
      else onRange?.(fromIso || new Date(min).toISOString(), iso);
    }
  };

  const valuePct = pct(valueIso);
  const fromPct = pct(fromIso);
  const toPct = pct(toIso);

  return (
    <div data-testid="timeline-scrubber">
      <div className="flex items-center justify-between">
        <Overline>
          <span className="flex items-center gap-1.5"><BarChart3 size={12} /> Change-count timeline</span>
        </Overline>
        <span className="font-mono text-[10px] text-[var(--text-muted)]">{total} change event{total === 1 ? "" : "s"} · {new Date(min).toLocaleDateString()} → {new Date(max).toLocaleDateString()}</span>
      </div>

      {/* Histogram + track */}
      <div
        ref={trackRef}
        onClick={handleClick}
        onMouseMove={(e) => setHover({ x: e.nativeEvent.offsetX, iso: isoAtX(e.clientX) })}
        onMouseLeave={() => setHover(null)}
        className="group relative mt-2 h-24 cursor-crosshair select-none rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-1 pt-2"
        role="slider"
        aria-label="Change-count timeline scrubber"
      >
        {/* bars */}
        <div className="flex h-16 items-end gap-[2px]">
          {buckets.map((c, i) => (
            <div key={i} className="flex-1" title={c ? `${c} changes` : ""}>
              <div
                className="w-full rounded-t-[1px] bg-gradient-to-t from-cyan-700/70 to-cyan-400 transition-[height] duration-300"
                style={{ height: `${(c / maxCount) * 100}%`, opacity: c ? 1 : 0.12 }}
              />
            </div>
          ))}
        </div>

        {/* compare range shading */}
        {mode === "compare" && fromPct != null && toPct != null && (
          <div className="pointer-events-none absolute inset-y-0 bg-[var(--accent)]/10" style={{ left: `${Math.min(fromPct, toPct)}%`, width: `${Math.abs(toPct - fromPct)}%` }} />
        )}

        {/* playhead(s) */}
        {mode === "asof" && valuePct != null && (
          <Playhead pct={valuePct} tone="accent" label="valid at" testId="scrubber-playhead-asof" />
        )}
        {mode === "compare" && fromPct != null && <Playhead pct={fromPct} tone="info" label="from" testId="scrubber-handle-from" />}
        {mode === "compare" && toPct != null && <Playhead pct={toPct} tone="accent" label="to" testId="scrubber-handle-to" />}

        {/* run markers */}
        {events.map((e, i) => {
          const p = pct(e.iso);
          if (p == null) return null;
          return (
            <span key={i} className="pointer-events-none absolute bottom-6 -translate-x-1/2" style={{ left: `${p}%` }} title={`${e.label} · ${e.changes} changes`}>
              <MapPin size={11} className={e.status === "PARTIAL" ? "text-amber-400" : "text-emerald-400"} />
            </span>
          );
        })}

        {/* hover guide */}
        {hover && (
          <div className="pointer-events-none absolute top-0 z-10 -translate-x-1/2 rounded-sm bg-[var(--bg-panel)] px-1.5 py-0.5 font-mono text-[9px] text-[var(--text-secondary)] shadow" style={{ left: hover.x }}>
            {new Date(hover.iso).toLocaleString()}
          </div>
        )}

        {/* axis labels */}
        <div className="absolute inset-x-1 bottom-0.5 flex justify-between font-mono text-[9px] text-[var(--text-muted)]">
          <span>{new Date(min).toLocaleTimeString()}</span>
          <span className="opacity-70">{mode === "asof" ? "click to set valid-at" : mode === "compare" ? "click to set nearest handle" : "graph change events"}</span>
          <span>{new Date(max).toLocaleTimeString()}</span>
        </div>
      </div>
    </div>
  );
}

function Playhead({ pct, tone, label, testId }: { pct: number; tone: "accent" | "info"; label: string; testId: string }) {
  const color = tone === "accent" ? "var(--accent)" : "#3b82f6";
  return (
    <div className="pointer-events-none absolute inset-y-0 z-20 -translate-x-1/2" style={{ left: `${pct}%` }} data-testid={testId}>
      <div className="h-16 w-[2px]" style={{ backgroundColor: color }} />
      <span className="absolute -top-0.5 left-1/2 -translate-x-1/2 rounded-full px-1.5 py-0.5 text-[8px] font-semibold text-black" style={{ backgroundColor: color }}>{label}</span>
    </div>
  );
}

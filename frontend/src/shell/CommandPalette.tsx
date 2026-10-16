import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowRight, CornerDownLeft, Search, Loader2 } from "lucide-react";
import { useShell } from "../lib/shellStore";
import { apiFetch } from "../lib/api";
import { NAV_ITEMS } from "./nav";
import { FactClassBadge } from "../components/FactClassBadge";
import { cn, shortId } from "../lib/utils";

interface Hit {
  id: string;
  label: string;
  domain?: string;
  properties?: Record<string, any>;
}

export function CommandPalette() {
  const { paletteOpen, togglePalette } = useShell();
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [hits, setHits] = useState<Hit[]>([]);
  const [loading, setLoading] = useState(false);
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        togglePalette();
      }
      if (e.key === "Escape") togglePalette(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [togglePalette]);

  useEffect(() => {
    if (paletteOpen) {
      setTimeout(() => inputRef.current?.focus(), 30);
    } else {
      setQ("");
      setHits([]);
      setActive(0);
    }
  }, [paletteOpen]);

  useEffect(() => {
    if (!q.trim()) {
      setHits([]);
      return;
    }
    const ctrl = new AbortController();
    setLoading(true);
    const t = setTimeout(() => {
      apiFetch<any>(`/search?q=${encodeURIComponent(q.trim())}&limit=8`, { signal: ctrl.signal })
        .then((r) => setHits(r.nodes || []))
        .catch(() => setHits([]))
        .finally(() => setLoading(false));
    }, 180);
    return () => {
      ctrl.abort();
      clearTimeout(t);
    };
  }, [q]);

  if (!paletteOpen) return null;

  const navMatches = NAV_ITEMS.filter((n) =>
    n.label.toLowerCase().includes(q.trim().toLowerCase()),
  );
  const flatCount = navMatches.length + hits.length;

  const go = (idx: number) => {
    if (idx < navMatches.length) {
      navigate(navMatches[idx].to);
    } else {
      const hit = hits[idx - navMatches.length];
      if (hit) navigate(`/entity/${encodeURIComponent(hit.id)}`);
    }
    togglePalette(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[12vh]" data-testid="command-palette">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => togglePalette(false)} />
      <div className="relative w-full max-w-xl animate-fade-in overflow-hidden rounded-lg border border-[var(--border-strong)] bg-[var(--bg-surface)] shadow-2xl">
        <div className="flex items-center gap-3 border-b border-[var(--border-subtle)] px-4">
          <Search size={17} className="text-[var(--text-muted)]" />
          <input
            ref={inputRef}
            data-testid="command-palette-input"
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setActive(0);
            }}
            onKeyDown={(e) => {
              if (e.key === "ArrowDown") {
                e.preventDefault();
                setActive((a) => Math.min(a + 1, flatCount - 1));
              } else if (e.key === "ArrowUp") {
                e.preventDefault();
                setActive((a) => Math.max(a - 1, 0));
              } else if (e.key === "Enter") {
                go(active);
              }
            }}
            placeholder="Search entities or jump to a screen…"
            className="h-12 w-full bg-transparent text-sm outline-none placeholder:text-[var(--text-muted)]"
          />
          {loading && <Loader2 size={15} className="animate-spin text-[var(--text-muted)]" />}
        </div>

        <div className="max-h-[52vh] overflow-y-auto p-1.5">
          {navMatches.length > 0 && (
            <div className="px-2 py-1 font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
              Navigate
            </div>
          )}
          {navMatches.map((n, i) => (
            <button
              key={n.id}
              onClick={() => go(i)}
              onMouseEnter={() => setActive(i)}
              className={cn(
                "flex w-full items-center gap-3 rounded-sm px-2.5 py-2 text-left text-sm transition-colors",
                active === i ? "bg-[var(--bg-hover)]" : "hover:bg-[var(--bg-hover)]",
              )}
            >
              <n.icon size={15} className="text-[var(--text-muted)]" />
              <span>{n.label}</span>
              <ArrowRight size={13} className="ml-auto text-[var(--text-muted)]" />
            </button>
          ))}

          {hits.length > 0 && (
            <div className="mt-1 px-2 py-1 font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
              Entities
            </div>
          )}
          {hits.map((h, i) => {
            const idx = navMatches.length + i;
            return (
              <button
                key={h.id}
                data-testid="command-palette-result"
                onClick={() => go(idx)}
                onMouseEnter={() => setActive(idx)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-sm px-2.5 py-2 text-left transition-colors",
                  active === idx ? "bg-[var(--bg-hover)]" : "hover:bg-[var(--bg-hover)]",
                )}
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="truncate text-sm">
                      {h.properties?.name || h.properties?.title || shortId(h.id)}
                    </span>
                    <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                      {h.label}
                    </span>
                  </div>
                  <p className="truncate font-mono text-[10px] text-[var(--text-muted)]">{h.id}</p>
                </div>
                <FactClassBadge creationStatus={h.properties?.creation_status} size="sm" />
              </button>
            );
          })}

          {q.trim() && !loading && flatCount === 0 && (
            <div className="px-3 py-6 text-center text-sm text-[var(--text-muted)]">
              No matches for “{q}”
            </div>
          )}
          {!q.trim() && (
            <div className="px-3 py-6 text-center text-xs text-[var(--text-muted)]">
              Type to search the knowledge graph.
            </div>
          )}
        </div>

        <div className="flex items-center gap-4 border-t border-[var(--border-subtle)] px-4 py-2 font-mono text-[10px] text-[var(--text-muted)]">
          <span className="flex items-center gap-1">
            <CornerDownLeft size={11} /> open
          </span>
          <span>↑↓ navigate</span>
          <span>esc close</span>
        </div>
      </div>
    </div>
  );
}

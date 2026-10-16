import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import {
  ChevronDown,
  Database,
  LogOut,
  Monitor,
  Palette,
  Search,
  TerminalSquare,
  UserRound,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { useTheme, THEMES, type ThemeName } from "../lib/theme";
import { useShell } from "../lib/shellStore";
import { apiFetch } from "../lib/api";
import { StatusDot } from "../components/ui/Badge";
import { cn } from "../lib/utils";

function BackendChip() {
  const { data, isError } = useQuery({
    queryKey: ["graph-backend"],
    queryFn: () => apiFetch<any>("/graph/backend"),
    staleTime: 60_000,
  });
  const active = data?.active_backend || data?.configured_backend;
  const ping = data?.ping;
  const ok = !isError && (ping === undefined || ping === true || ping === "ok" || ping?.ok);
  return (
    <div
      data-testid="backend-status-chip"
      className="hidden items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2.5 py-1.5 md:flex"
      title={`Graph backend: ${active || "unknown"}`}
    >
      <Database size={13} className="text-[var(--text-muted)]" />
      <span className="font-mono text-[11px] text-[var(--text-secondary)]">
        {active || "backend"}
      </span>
      <StatusDot tone={isError ? "danger" : ok ? "success" : "warning"} pulse={ok} />
    </div>
  );
}

function ThemeMenu() {
  const { theme, setTheme } = useTheme();
  const [open, setOpen] = useState(false);
  return (
    <div className="relative">
      <button
        data-testid="theme-toggle-button"
        onClick={() => setOpen((o) => !o)}
        className="grid h-9 w-9 place-items-center rounded-sm text-[var(--text-secondary)] transition-colors hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
        title="Theme"
      >
        <Palette size={16} />
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-30" onClick={() => setOpen(false)} />
          <div className="absolute right-0 z-40 mt-1 w-52 animate-fade-in rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-xl">
            {THEMES.map((t) => (
              <button
                key={t.id}
                data-testid={`theme-option-${t.id}`}
                onClick={() => {
                  setTheme(t.id as ThemeName);
                  setOpen(false);
                }}
                className={cn(
                  "flex w-full items-center gap-2 rounded-sm px-2.5 py-1.5 text-left text-sm transition-colors hover:bg-[var(--bg-hover)]",
                  theme === t.id ? "text-[var(--accent)]" : "text-[var(--text-secondary)]",
                )}
              >
                <Monitor size={14} />
                {t.label}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export function TopBar() {
  const { session, signOut } = useAuth();
  const { togglePalette } = useShell();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="flex h-14 shrink-0 items-center gap-3 border-b border-[var(--border-subtle)] bg-[var(--bg-surface)] px-3">
      {/* Scope */}
      <button
        data-testid="tenant-select-dropdown"
        className="flex items-center gap-2 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2.5 py-1.5 text-sm transition-colors hover:border-[var(--border-strong)]"
        title="Tenant / workspace scope"
      >
        <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
          tenant
        </span>
        <span className="font-medium">{session?.tenant}</span>
        <span className="text-[var(--text-muted)]">/</span>
        <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
          ws
        </span>
        <span className="font-medium">{session?.workspace}</span>
        <ChevronDown size={13} className="text-[var(--text-muted)]" />
      </button>

      {/* Global search → command palette */}
      <button
        data-testid="global-search-trigger"
        onClick={() => togglePalette(true)}
        className="group flex h-9 flex-1 items-center gap-2.5 rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-void)] px-3 text-sm text-[var(--text-muted)] transition-colors hover:border-[var(--border-strong)]"
      >
        <Search size={15} />
        <span>Search entities, run commands…</span>
        <kbd className="ml-auto hidden items-center gap-1 rounded border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[10px] text-[var(--text-muted)] sm:flex">
          ⌘K
        </kbd>
      </button>

      <BackendChip />

      <button
        data-testid="command-palette-trigger"
        onClick={() => togglePalette(true)}
        className="grid h-9 w-9 place-items-center rounded-sm text-[var(--text-secondary)] transition-colors hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
        title="Command palette (⌘K)"
      >
        <TerminalSquare size={16} />
      </button>

      <ThemeMenu />

      {/* Principal */}
      <div className="relative">
        <button
          data-testid="principal-menu-trigger"
          onClick={() => setMenuOpen((o) => !o)}
          className="flex items-center gap-2 rounded-sm px-1.5 py-1 transition-colors hover:bg-[var(--bg-hover)]"
        >
          <div className="grid h-7 w-7 place-items-center rounded-full border border-[var(--border-strong)] bg-[var(--bg-panel)] text-[var(--text-secondary)]">
            <UserRound size={15} />
          </div>
          <ChevronDown size={13} className="text-[var(--text-muted)]" />
        </button>
        {menuOpen && (
          <>
            <div className="fixed inset-0 z-30" onClick={() => setMenuOpen(false)} />
            <div className="absolute right-0 z-40 mt-1 w-64 animate-fade-in rounded-md border border-[var(--border-strong)] bg-[var(--bg-panel)] p-1 shadow-xl">
              <div className="px-2.5 py-2">
                <p className="truncate text-sm font-medium">{session?.principal.username}</p>
                <p className="truncate font-mono text-[10px] text-[var(--text-muted)]">
                  {session?.principal.label}
                </p>
                <div className="mt-1.5 flex flex-wrap gap-1">
                  {session?.principal.roles.map((r) => (
                    <span
                      key={r}
                      className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-secondary)]"
                    >
                      {r}
                    </span>
                  ))}
                </div>
              </div>
              <div className="my-1 h-px bg-[var(--border-subtle)]" />
              <button
                data-testid="signout-button"
                onClick={() => {
                  signOut();
                  navigate("/signin", { replace: true });
                }}
                className="flex w-full items-center gap-2 rounded-sm px-2.5 py-1.5 text-left text-sm text-red-300 transition-colors hover:bg-red-500/10"
              >
                <LogOut size={14} />
                Sign out
              </button>
            </div>
          </>
        )}
      </div>
    </header>
  );
}

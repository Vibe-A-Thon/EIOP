import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import { PanelLeftClose, PanelLeftOpen, Waypoints } from "lucide-react";
import { NAV_GROUPS } from "./nav";
import { useShell } from "../lib/shellStore";
import { useAuth } from "../lib/auth";
import { cn } from "../lib/utils";

export function NavRail() {
  const { railCollapsed, toggleRail } = useShell();
  const { session } = useAuth();
  const roles = session?.principal.roles || [];
  const isAdmin = roles.some((r) => r === "admin" || r === "system" || r === "superadmin");

  return (
    <nav
      data-testid="app-shell-nav-rail"
      className={cn(
        "flex shrink-0 flex-col border-r border-[var(--border-subtle)] bg-[var(--bg-surface)] transition-[width] duration-200",
        railCollapsed ? "w-[60px]" : "w-[232px]",
      )}
    >
      <div className="flex h-14 items-center gap-2.5 border-b border-[var(--border-subtle)] px-4">
        <div className="grid h-8 w-8 shrink-0 place-items-center rounded-md border border-cyan-500/40 bg-cyan-500/10 text-cyan-300">
          <Waypoints size={16} />
        </div>
        {!railCollapsed && (
          <div className="min-w-0 animate-fade-in">
            <p className="truncate font-heading text-sm font-bold tracking-tight">KnowGridFlow</p>
            <p className="truncate font-mono text-[9px] uppercase tracking-[0.16em] text-[var(--text-muted)]">
              EOIP
            </p>
          </div>
        )}
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto p-2">
        {NAV_GROUPS.map((group) => {
          const items = group.items.filter((item) => !item.adminOnly || isAdmin);
          if (items.length === 0) return null;
          return (
          <div key={group.label}>
            {!railCollapsed && (
              <p className="px-2.5 pb-1 pt-1 font-mono text-[9px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
                {group.label}
              </p>
            )}
            <div className="space-y-0.5">
              {items.map((item) => (
                <NavLink
                  key={item.id}
                  to={item.to}
                  data-testid={`app-shell-nav-${item.id}`}
                  title={railCollapsed ? item.label : undefined}
                  className={({ isActive }) =>
                    cn(
                      "group relative flex items-center gap-3 rounded-sm px-2.5 py-1.5 text-sm transition-[background-color,color] duration-150",
                      isActive
                        ? "bg-[var(--bg-hover)] text-[var(--text-primary)]"
                        : "text-[var(--text-secondary)] hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]",
                    )
                  }
                >
                  {({ isActive }) => (
                    <>
                      {isActive && (
                        <motion.span
                          layoutId="nav-active-indicator"
                          className="absolute left-0 top-1/2 h-5 w-[2.5px] -translate-y-1/2 rounded-full bg-[var(--accent)] shadow-[0_0_8px_0_var(--accent)]"
                          transition={{ type: "spring", stiffness: 500, damping: 36 }}
                        />
                      )}
                      <item.icon size={16} className="shrink-0 transition-transform duration-150 group-hover:scale-110 group-active:scale-95" />
                      {!railCollapsed && <span className="truncate">{item.label}</span>}
                    </>
                  )}
                </NavLink>
              ))}
            </div>
          </div>
          );
        })}
      </div>

      <button
        onClick={toggleRail}
        data-testid="app-shell-rail-toggle"
        className="flex h-11 items-center gap-3 border-t border-[var(--border-subtle)] px-3.5 text-[var(--text-muted)] transition-colors hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
      >
        {railCollapsed ? <PanelLeftOpen size={17} /> : <PanelLeftClose size={17} />}
        {!railCollapsed && <span className="text-xs">Collapse</span>}
      </button>
    </nav>
  );
}

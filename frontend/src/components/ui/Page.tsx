import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { Overline } from "./Card";

export function PageHeader({
  title,
  overline,
  icon,
  actions,
}: {
  title: string;
  overline?: string;
  icon?: ReactNode;
  actions?: ReactNode;
}) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3">
      <div className="flex items-center gap-2.5">
        {icon && <span className="text-cyan-400">{icon}</span>}
        <div>
          {overline && <Overline>{overline}</Overline>}
          <h1 className="font-heading text-2xl font-bold tracking-tight">{title}</h1>
        </div>
      </div>
      {actions}
    </div>
  );
}

export function Page({ children }: { children: ReactNode }) {
  return <div className="mx-auto max-w-[1300px] space-y-5 p-6">{children}</div>;
}

export function Tabs<T extends string>({
  tabs,
  active,
  onChange,
  testPrefix,
}: {
  tabs: { id: T; label: string }[];
  active: T;
  onChange: (id: T) => void;
  testPrefix: string;
}) {
  return (
    <div className="flex flex-wrap gap-1 border-b border-[var(--border-subtle)]">
      {tabs.map((t) => (
        <button
          key={t.id}
          data-testid={`${testPrefix}-${t.id}`}
          onClick={() => onChange(t.id)}
          className={`relative px-3 py-2.5 text-sm transition-colors ${active === t.id ? "text-[var(--text-primary)]" : "text-[var(--text-muted)] hover:text-[var(--text-primary)]"}`}
        >
          {t.label}
          {active === t.id && (
            <motion.span
              layoutId={`tab-indicator-${testPrefix}`}
              className="absolute bottom-0 left-0 h-[2px] w-full rounded-full bg-[var(--accent)]"
              transition={{ type: "spring", stiffness: 420, damping: 34 }}
            />
          )}
        </button>
      ))}
    </div>
  );
}

import {
  BadgeCheck,
  FunctionSquare,
  Sparkles,
  CircleHelp,
  UserCheck,
  CircleDashed,
  type LucideIcon,
} from "lucide-react";
import { FACT_META, factClassOf, type FactClass } from "../lib/factClass";
import { cn } from "../lib/utils";

const ICONS: Record<FactClass, LucideIcon> = {
  Deterministic: BadgeCheck,
  Derived: FunctionSquare,
  Inferred: Sparkles,
  Ambiguous: CircleHelp,
  "Human-confirmed": UserCheck,
  Unknown: CircleDashed,
};

export function FactClassBadge({
  creationStatus,
  cls,
  size = "md",
}: {
  creationStatus?: string | null;
  cls?: FactClass;
  size?: "sm" | "md";
}) {
  const resolved = cls ?? factClassOf(creationStatus);
  const meta = FACT_META[resolved];
  const Icon = ICONS[resolved];
  return (
    <span
      data-testid={`fact-class-badge-${resolved.toLowerCase()}`}
      title={`Fact class: ${meta.cls}`}
      className={cn(
        "inline-flex items-center gap-1 rounded-full border font-mono uppercase tracking-wider",
        meta.badge,
        size === "sm" ? "px-1.5 py-0.5 text-[9px]" : "px-2 py-0.5 text-[10px]",
      )}
    >
      <Icon size={size === "sm" ? 10 : 12} />
      {meta.cls}
    </span>
  );
}

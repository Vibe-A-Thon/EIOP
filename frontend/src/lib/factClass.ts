export type FactClass =
  | "Deterministic"
  | "Derived"
  | "Inferred"
  | "Ambiguous"
  | "Human-confirmed"
  | "Unknown";

interface FactMeta {
  cls: FactClass;
  color: string; // css var
  badge: string; // tailwind classes
  icon: string; // lucide name (used by FactClassBadge switch)
  edge: string;
}

const MAP: Record<string, FactClass> = {
  DETERMINISTIC: "Deterministic",
  ASSERTED: "Deterministic",
  asserted: "Deterministic",
  DERIVED: "Derived",
  INFERRED: "Inferred",
  inferred: "Inferred",
  "model-generated": "Inferred",
  AMBIGUOUS: "Ambiguous",
  HUMAN_CONFIRMED: "Human-confirmed",
  MANUAL: "Human-confirmed",
  CURATED: "Human-confirmed",
  "human-confirmed": "Human-confirmed",
};

export const FACT_META: Record<FactClass, FactMeta> = {
  Deterministic: {
    cls: "Deterministic",
    color: "var(--fact-deterministic)",
    badge: "text-cyan-300 border-cyan-500/40 bg-cyan-500/10",
    icon: "badge-check",
    edge: "solid",
  },
  Derived: {
    cls: "Derived",
    color: "var(--fact-derived)",
    badge: "text-blue-300 border-blue-500/40 bg-blue-500/10",
    icon: "function-square",
    edge: "solid",
  },
  Inferred: {
    cls: "Inferred",
    color: "var(--fact-inferred)",
    badge: "text-violet-300 border-violet-500/40 bg-violet-500/10",
    icon: "sparkles",
    edge: "dashed",
  },
  Ambiguous: {
    cls: "Ambiguous",
    color: "var(--fact-ambiguous)",
    badge: "text-amber-300 border-amber-500/40 bg-amber-500/10",
    icon: "circle-help",
    edge: "dotted",
  },
  "Human-confirmed": {
    cls: "Human-confirmed",
    color: "var(--fact-human)",
    badge: "text-emerald-300 border-emerald-500/40 bg-emerald-500/10",
    icon: "user-check",
    edge: "solid",
  },
  Unknown: {
    cls: "Unknown",
    color: "var(--fact-unknown)",
    badge: "text-slate-300 border-slate-500/40 bg-slate-500/10",
    icon: "circle-dashed",
    edge: "solid",
  },
};

export function factClassOf(creationStatus?: string | null): FactClass {
  if (!creationStatus) return "Unknown";
  return MAP[creationStatus] ?? "Unknown";
}

export const ALL_FACT_CLASSES: FactClass[] = [
  "Deterministic",
  "Derived",
  "Inferred",
  "Ambiguous",
  "Human-confirmed",
  "Unknown",
];

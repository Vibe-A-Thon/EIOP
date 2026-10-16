import { Link } from "react-router-dom";
import { Users, Share2, FileBarChart, Activity, ArrowRight, CircleAlert } from "lucide-react";
import { motion } from "framer-motion";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Page, PageHeader } from "../components/ui/Page";

// SCR-020 — Collaboration. Backend is BACKEND-MISSING-016 (no collaboration WS/REST).
// Per spec this renders a single MissingBackendState with working links to what IS
// available. No local-only comments and no fake presence (GUI-A025). No network call.

const ALTERNATIVES = [
  {
    icon: Share2,
    title: "Share a view",
    description: "Encode filters, focus, lens and selection into a URL, or export the current graph as JSON to hand off.",
    to: "/graph",
    cta: "Open Graph Explorer",
    testId: "collab-alt-share-view",
  },
  {
    icon: FileBarChart,
    title: "Share a report",
    description: "Render any template and distribute the artifact, or set a recurring schedule for automatic generation.",
    to: "/reports",
    cta: "Open Reports",
    testId: "collab-alt-reports",
  },
  {
    icon: Activity,
    title: "Follow activity",
    description: "Track graph changes, ingestion, validation and ontology events as they happen in the activity dock.",
    to: "/overview",
    cta: "Open Overview",
    testId: "collab-alt-activity",
  },
];

export function Collaboration() {
  return (
    <Page>
      <PageHeader title="Collaboration" overline="Comments · mentions · presence · shared views" icon={<Users size={18} />} />

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }}>
        <Card className="overflow-hidden" data-testid="collaboration-missing-backend">
          <div className="flex flex-col items-center gap-4 border-b border-[var(--border-subtle)] bg-gradient-to-b from-[var(--bg-panel)]/60 to-transparent px-6 py-12 text-center">
            <div className="relative">
              <span className="absolute inset-0 animate-ping rounded-full bg-amber-500/20" />
              <div className="relative rounded-full border border-amber-500/40 bg-amber-500/10 p-4 text-amber-300">
                <CircleAlert size={26} />
              </div>
            </div>
            <div>
              <h2 className="font-heading text-xl font-bold tracking-tight">Collaboration is not available in this deployment</h2>
              <p className="mx-auto mt-2 max-w-lg text-sm text-[var(--text-muted)]">
                Real-time comments, @mentions, presence and shared annotations require a collaboration
                service that this deployment does not provide. No comments or presence are simulated
                locally — the data you see across KnowGridFlow is always real.
              </p>
            </div>
            <Badge tone="warning" testId="collab-contract-badge">contract · BACKEND-MISSING-016</Badge>
          </div>

          <div className="px-6 py-5">
            <Overline>Available instead</Overline>
            <div className="mt-3 grid gap-3 md:grid-cols-3">
              {ALTERNATIVES.map((a, i) => (
                <motion.div
                  key={a.title}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + i * 0.07, duration: 0.25 }}
                >
                  <Link to={a.to} data-testid={a.testId} className="group block h-full">
                    <Card hover className="flex h-full flex-col gap-3 p-4">
                      <div className="flex h-9 w-9 items-center justify-center rounded-md border border-[var(--border-subtle)] bg-[var(--bg-panel)] text-cyan-400 transition-colors group-hover:border-[var(--accent)]/50">
                        <a.icon size={17} />
                      </div>
                      <div className="flex-1">
                        <p className="font-heading text-sm font-semibold">{a.title}</p>
                        <p className="mt-1 text-xs leading-relaxed text-[var(--text-muted)]">{a.description}</p>
                      </div>
                      <span className="flex items-center gap-1 text-xs font-medium text-[var(--accent)]">
                        {a.cta}
                        <ArrowRight size={13} className="transition-transform group-hover:translate-x-1" />
                      </span>
                    </Card>
                  </Link>
                </motion.div>
              ))}
            </div>
          </div>
        </Card>
      </motion.div>
    </Page>
  );
}

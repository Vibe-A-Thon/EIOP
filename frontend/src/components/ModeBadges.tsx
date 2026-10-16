import {
  Ban,
  CircleCheck,
  CircleX,
  Clock,
  Database,
  FileText,
  LoaderCircle,
  MessageSquareText,
  PauseCircle,
  Radar,
  TestTube,
  TriangleAlert,
  type LucideIcon,
} from "lucide-react";
import { Badge } from "./ui/Badge";

type Tone = "neutral" | "success" | "info" | "warning" | "danger" | "accent";

const ANSWER_MODES: Record<string, { tone: Tone; icon: LucideIcon; label: string }> = {
  Deterministic: { tone: "accent", icon: Database, label: "Deterministic" },
  Narrated: { tone: "info", icon: MessageSquareText, label: "Narrated" },
  Exploratory: { tone: "warning", icon: Radar, label: "Exploratory" },
  Report: { tone: "neutral", icon: FileText, label: "Report" },
  Simulated: { tone: "warning", icon: TestTube, label: "Simulated (not model inference)" },
  Abstained: { tone: "neutral", icon: Ban, label: "Abstained" },
};

export function AnswerModeBadge({ mode }: { mode: string }) {
  const meta = ANSWER_MODES[mode] || ANSWER_MODES.Deterministic;
  const Icon = meta.icon;
  return (
    <Badge tone={meta.tone} testId={`answer-mode-badge-${mode.toLowerCase()}`} icon={<Icon size={11} />}>
      {meta.label}
    </Badge>
  );
}

const JOB_STATUS: Record<
  string,
  { tone: Tone; icon: LucideIcon; label: string; spin?: boolean }
> = {
  PENDING: { tone: "neutral", icon: Clock, label: "Queued" },
  RUNNING: { tone: "info", icon: LoaderCircle, label: "Running", spin: true },
  HELD: { tone: "warning", icon: PauseCircle, label: "Held — needs operator" },
  SUCCEEDED: { tone: "success", icon: CircleCheck, label: "Succeeded" },
  PARTIAL: { tone: "warning", icon: TriangleAlert, label: "Partial" },
  FAILED: { tone: "danger", icon: CircleX, label: "Failed" },
  CANCELLED: { tone: "neutral", icon: Ban, label: "Cancelled" },
  DONE: { tone: "success", icon: CircleCheck, label: "Succeeded" },
};

export function JobStatusBadge({ status }: { status: string }) {
  const meta = JOB_STATUS[status] || { tone: "neutral" as Tone, icon: Clock, label: status };
  const Icon = meta.icon;
  return (
    <Badge tone={meta.tone} testId={`job-status-${status.toLowerCase()}`} icon={<Icon size={11} className={meta.spin ? "animate-spin" : ""} />}>
      {meta.label}
    </Badge>
  );
}

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  CornerDownLeft,
  Lightbulb,
  Loader2,
  Lock,
  Quote,
  Send,
  Sparkles,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch, type ApiProblem } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { AnswerModeBadge } from "../components/ModeBadges";
import { FactClassBadge } from "../components/FactClassBadge";
import { ErrorState } from "../components/ui/States";
import { shortId } from "../lib/utils";

interface NlResult {
  interpretation?: { plan?: any };
  result?: any;
  answer?: string;
  confidence?: number | string;
  engine?: string;
  highlights?: any[];
  followups?: string[];
  warnings?: string[];
}

function deriveMode(r: NlResult): string {
  if (!r.answer && (r.result?.partial || !r.interpretation?.plan)) return "Abstained";
  if (r.engine && /model|llm|opus|frontier/i.test(r.engine)) return "Narrated";
  return "Deterministic";
}

export function Ask() {
  const { session } = useAuth();
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [submitted, setSubmitted] = useState<string | null>(null);
  const [result, setResult] = useState<NlResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiProblem | null>(null);

  // Boundary badge — local only unless egress endpoints are enabled
  const egress = useQuery({
    queryKey: ["egress-endpoints"],
    queryFn: () => apiFetch<any>("/egress/endpoints"),
    retry: false,
  });
  const enabledEgress = (egress.data?.endpoints || egress.data || []).filter?.(
    (e: any) => e?.enabled,
  );
  const boundary = egress.isError
    ? { label: "Egress status unknown", tone: "warning" as const }
    : enabledEgress && enabledEgress.length > 0
      ? { label: `Approved external: ${enabledEgress[0].name}`, tone: "info" as const }
      : { label: "Local only", tone: "neutral" as const };

  const intents = useQuery({
    queryKey: ["suggest-intents"],
    queryFn: () => apiFetch<any>("/suggest/intents"),
    retry: false,
    staleTime: 300_000,
  });
  const starters: string[] = (() => {
    const raw = intents.data?.intents || intents.data?.candidates || intents.data || [];
    const list = Array.isArray(raw) ? raw : [];
    return list
      .map((i: any) => (typeof i === "string" ? i : i.example || i.question || i.label || i.name))
      .filter(Boolean)
      .slice(0, 6);
  })();

  const run = async (q: string) => {
    const query = q.trim();
    if (!query) return;
    setSubmitted(query);
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const r = await apiFetch<NlResult>("/query/nl", { method: "POST", body: { question: query } });
      setResult(r);
    } catch (err: any) {
      setError(err?.problem || { status: 0, title: "Error", detail: err?.message });
    } finally {
      setLoading(false);
    }
  };

  const nodes: any[] = result?.result?.nodes || [];
  const evidence: any[] = result?.result?.evidence || result?.highlights || [];
  const mode = result ? deriveMode(result) : null;

  return (
    <div className="mx-auto max-w-4xl space-y-5 p-6">
      <div className="flex items-center justify-between">
        <div>
          <Overline>Evidence-first query</Overline>
          <h1 className="mt-1 font-heading text-2xl font-bold tracking-tight">Ask</h1>
        </div>
        <Badge
          tone={boundary.tone}
          testId="ask-boundary-badge"
          icon={<Lock size={11} />}
        >
          {boundary.label}
        </Badge>
      </div>

      {/* Composer */}
      <Card className="overflow-hidden">
        <textarea
          data-testid="ask-query-input"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) run(question);
          }}
          rows={3}
          placeholder="Ask about traceability, impact, ownership, or evidence…  e.g. “What implements EOIP-1?”"
          className="w-full resize-none bg-transparent px-4 py-3.5 text-sm outline-none placeholder:text-[var(--text-muted)]"
        />
        <div className="flex items-center justify-between border-t border-[var(--border-subtle)] px-3 py-2">
          <span className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
            <CornerDownLeft size={11} /> ⌘ + Enter to run
          </span>
          <button
            data-testid="ask-submit-button"
            onClick={() => run(question)}
            disabled={loading || !question.trim()}
            className="flex items-center gap-2 rounded-sm bg-[var(--accent)] px-3.5 py-1.5 text-sm font-semibold text-black transition-colors hover:bg-[var(--accent-strong)] disabled:opacity-40"
          >
            {loading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
            Run
          </button>
        </div>
      </Card>

      {/* Suggestion cards */}
      {!result && !loading && starters.length > 0 && (
        <div>
          <div className="mb-2 flex items-center gap-1.5">
            <Lightbulb size={13} className="text-[var(--text-muted)]" />
            <Overline>Suggested questions</Overline>
          </div>
          <div className="grid gap-2 sm:grid-cols-2">
            {starters.map((s, i) => (
              <button
                key={i}
                data-testid={`ask-suggestion-${i}`}
                onClick={() => {
                  setQuestion(s);
                  run(s);
                }}
                className="group flex items-start gap-2.5 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-surface)] p-3 text-left text-sm transition-colors hover:border-[var(--border-strong)] hover:bg-[var(--bg-hover)]"
              >
                <Sparkles size={14} className="mt-0.5 shrink-0 text-cyan-400" />
                <span className="text-[var(--text-secondary)] group-hover:text-[var(--text-primary)]">
                  {s}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Result */}
      {error && <ErrorState problem={error} onRetry={() => submitted && run(submitted)} />}

      {loading && (
        <Card className="p-5">
          <div className="flex items-center gap-2 text-sm text-[var(--text-muted)]">
            <Loader2 size={16} className="animate-spin" /> Interpreting against the graph…
          </div>
        </Card>
      )}

      {result && (
        <div className="animate-fade-in space-y-4" data-testid="ask-result">
          <Card>
            <div className="flex flex-wrap items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
              {mode && <AnswerModeBadge mode={mode} />}
              {result.engine && (
                <Badge tone="neutral">engine: {result.engine}</Badge>
              )}
              {result.confidence !== undefined && result.confidence !== null && (
                <Badge tone="accent">
                  confidence: {typeof result.confidence === "number" ? result.confidence.toFixed(2) : result.confidence}
                </Badge>
              )}
            </div>
            <div className="p-4">
              <p className="mb-1 font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
                Question
              </p>
              <p className="mb-4 text-sm text-[var(--text-secondary)]">{submitted}</p>

              {result.answer ? (
                <p className="whitespace-pre-wrap text-[15px] leading-relaxed">{result.answer}</p>
              ) : !result.interpretation?.plan ? (
                <div className="rounded-sm border border-amber-500/40 bg-amber-500/10 px-3 py-2.5 text-sm text-amber-200">
                  Could not interpret this question — try refining it.
                </div>
              ) : (
                <p className="text-sm text-[var(--text-muted)]">
                  No narrative answer returned. Review the matched entities and evidence below.
                </p>
              )}

              {result.followups && result.followups.length > 0 && (
                <div className="mt-4">
                  <Overline>Follow-ups</Overline>
                  <div className="mt-1.5 flex flex-wrap gap-2">
                    {result.followups.map((f, i) => (
                      <button
                        key={i}
                        onClick={() => {
                          setQuestion(f);
                          run(f);
                        }}
                        className="rounded-full border border-[var(--border-subtle)] px-2.5 py-1 text-xs text-[var(--text-secondary)] transition-colors hover:border-[var(--border-strong)] hover:text-[var(--text-primary)]"
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Card>

          {/* Matched entities */}
          {nodes.length > 0 && (
            <Card>
              <div className="border-b border-[var(--border-subtle)] px-4 py-3">
                <h3 className="font-heading text-sm font-semibold">Matched entities ({nodes.length})</h3>
              </div>
              <div className="divide-y divide-[var(--border-subtle)]">
                {nodes.slice(0, 10).map((n: any) => (
                  <button
                    key={n.id}
                    onClick={() => navigate(`/entity/${encodeURIComponent(n.id)}`)}
                    className="flex w-full items-center gap-3 px-4 py-2.5 text-left transition-colors hover:bg-[var(--bg-hover)]"
                  >
                    <span className="rounded-full border border-[var(--border-strong)] px-1.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                      {n.label}
                    </span>
                    <span className="truncate text-sm">
                      {n.properties?.name || n.properties?.title || shortId(n.id)}
                    </span>
                    <FactClassBadge creationStatus={n.properties?.creation_status} size="sm" />
                  </button>
                ))}
              </div>
            </Card>
          )}

          {/* Evidence */}
          {evidence.length > 0 && (
            <Card>
              <div className="flex items-center gap-2 border-b border-[var(--border-subtle)] px-4 py-3">
                <Quote size={14} className="text-[var(--text-muted)]" />
                <h3 className="font-heading text-sm font-semibold">Evidence ({evidence.length})</h3>
              </div>
              <div className="space-y-2 p-4">
                {evidence.slice(0, 8).map((ev: any, i: number) => (
                  <div
                    key={i}
                    className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3 text-xs"
                  >
                    <p className="text-[var(--text-secondary)]">
                      {ev.fact_text || ev.text || ev.snippet || JSON.stringify(ev).slice(0, 180)}
                    </p>
                    {(ev.source_ref || ev.canonical_id) && (
                      <p className="mt-1 break-all font-mono text-[10px] text-[var(--text-muted)]">
                        {ev.source_ref || ev.canonical_id}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

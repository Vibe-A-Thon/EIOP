import { uuid } from "./utils";

const BASE = (import.meta.env.REACT_APP_BACKEND_URL as string | undefined)?.replace(/\/$/, "") || "";

export interface ApiProblem {
  status: number;
  title: string;
  detail: string;
  code?: string;
  category?: string;
  correlationId?: string;
  fields?: Array<{ field: string; message: string }>;
}

export class ApiError extends Error {
  problem: ApiProblem;
  constructor(problem: ApiProblem) {
    super(problem.detail || problem.title);
    this.problem = problem;
  }
}

/** Token + tenant live in memory only (R5: never in localStorage). */
let authToken: string | null = null;
let activeTenant: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}
export function getAuthToken() {
  return authToken;
}
export function setActiveTenant(tenant: string | null) {
  activeTenant = tenant;
}
export function getActiveTenant() {
  return activeTenant;
}

interface RequestOptions {
  method?: string;
  body?: unknown;
  signal?: AbortSignal;
  tenant?: string | null;
  principal?: string | null;
  headers?: Record<string, string>;
}

async function normalizeError(res: Response, correlationId: string): Promise<ApiProblem> {
  let detail = res.statusText || "Request failed";
  let title = res.statusText || "Error";
  let code: string | undefined;
  let category: string | undefined;
  let fields: ApiProblem["fields"];
  try {
    const data = await res.json();
    if (data && typeof data === "object") {
      if (typeof data.detail === "string") {
        detail = data.detail;
      } else if (Array.isArray(data.detail)) {
        fields = data.detail.map((d: any) => ({
          field: Array.isArray(d.loc) ? d.loc.join(".") : String(d.loc ?? "field"),
          message: d.msg ?? "Invalid",
        }));
        detail = "Validation failed";
      }
      if (data.title) title = data.title;
      if (data.detail && typeof data.detail === "string") detail = data.detail;
      if (data.error) {
        code = data.error.code;
        category = data.error.category;
        detail = data.error.message || detail;
      }
      if (data.correlation_id) correlationId = data.correlation_id;
    }
  } catch {
    /* non-JSON error body */
  }
  return { status: res.status, title, detail, code, category, correlationId, fields };
}

export async function apiFetch<T = unknown>(path: string, opts: RequestOptions = {}): Promise<T> {
  const correlationId = uuid();
  const headers: Record<string, string> = {
    Accept: "application/json",
    "X-Correlation-ID": correlationId,
    ...opts.headers,
  };
  if (authToken) headers.Authorization = `Bearer ${authToken}`;
  const tenant = opts.tenant !== undefined ? opts.tenant : activeTenant;
  if (tenant) headers["X-Tenant-Id"] = tenant;
  if (opts.principal) headers["X-Principal"] = opts.principal;

  let body: BodyInit | undefined;
  if (opts.body !== undefined && opts.body !== null) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(opts.body);
  }

  const res = await fetch(`${BASE}/api/v1${path}`, {
    method: opts.method || "GET",
    headers,
    body,
    signal: opts.signal,
  });

  if (!res.ok) {
    throw new ApiError(await normalizeError(res, correlationId));
  }
  if (res.status === 204) return undefined as T;
  const text = await res.text();
  return text ? (JSON.parse(text) as T) : (undefined as T);
}

/** Streaming POST (SSE over fetch) for brain/llm/stream. */
export async function* streamSSE(
  path: string,
  body: unknown,
  signal: AbortSignal,
  tenant?: string | null,
): AsyncGenerator<any> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "text/event-stream",
    "X-Correlation-ID": uuid(),
  };
  if (authToken) headers.Authorization = `Bearer ${authToken}`;
  const t = tenant !== undefined ? tenant : activeTenant;
  if (t) headers["X-Tenant-Id"] = t;

  const res = await fetch(`${BASE}/api/v1${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok || !res.body) {
    throw new ApiError({ status: res.status, title: "Stream failed", detail: res.statusText });
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split("\n\n");
    buffer = frames.pop() || "";
    for (const frame of frames) {
      const line = frame.split("\n").find((l) => l.startsWith("data:"));
      if (!line) continue;
      const payload = line.slice(5).trim();
      if (payload === "[DONE]") return;
      try {
        yield JSON.parse(payload);
      } catch {
        /* ignore malformed frame */
      }
    }
  }
}

export const BACKEND_BASE = BASE;

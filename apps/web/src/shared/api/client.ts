export class ApiError extends Error {
  status: number;
  correlationId: string | null;
  constructor(message: string, status = 0, correlationId: string | null = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.correlationId = correlationId;
  }
}

export interface RequestOptions {
  contentType?: string;
  signal?: AbortSignal;
}

function errorMessage(data: unknown, status: number): string {
  if (data && typeof data === 'object') {
    const problem = data as Record<string, unknown>;
    if (typeof problem.detail === 'string') return problem.detail;
    if (typeof problem.title === 'string') return problem.title;
    if (Array.isArray(problem.detail)) return 'Some fields are invalid. Review the submitted values.';
  }
  return `Request failed (${status})`;
}

/** One in-memory credential and cancellable request lifetime per connection. */
export function createApiClient(token: string, fetcher: typeof fetch = fetch) {
  const pending = new Set<AbortController>();
  let disposed = false;
  async function api(path: string, body?: unknown, method?: string, options: RequestOptions = {}): Promise<unknown> {
    if (disposed) throw new DOMException('Connection closed', 'AbortError');
    const url = new URL(path, globalThis.location?.origin || 'http://localhost');
    const origin = globalThis.location?.origin || 'http://localhost';
    if (url.origin !== origin || !path.startsWith('/') || path.startsWith('//')) {
      throw new ApiError('Only this deployment can receive authenticated requests.');
    }
    const controller = new AbortController();
    const abort = () => controller.abort();
    options.signal?.addEventListener('abort', abort, {once: true});
    if (options.signal?.aborted) controller.abort();
    pending.add(controller);
    try {
      const contentType = options.contentType || 'application/json';
      const response = await fetcher(path, {
        method: method || (body === undefined ? 'GET' : 'POST'),
        headers: {
          Authorization: `Bearer ${token}`,
          'X-Request-ID': crypto.randomUUID(),
          ...(body === undefined ? {} : {'Content-Type': contentType}),
        },
        credentials: 'same-origin',
        cache: 'no-store',
        redirect: 'error',
        signal: controller.signal,
        ...(body === undefined ? {} : {body: contentType === 'application/json' ? JSON.stringify(body) : String(body)}),
      });
      const text = response.status === 204 ? '' : await response.text();
      if (disposed || controller.signal.aborted) throw new DOMException('Connection closed', 'AbortError');
      let data: unknown = text || null;
      if (text && response.headers.get('content-type')?.includes('json')) {
        try { data = JSON.parse(text); }
        catch { throw new ApiError('The service returned an unreadable response.', response.status); }
      }
      if (!response.ok) {
        throw new ApiError(errorMessage(data, response.status), response.status,
          response.headers.get('X-Correlation-ID') || response.headers.get('X-Request-ID'));
      }
      return data;
    } finally {
      pending.delete(controller);
      options.signal?.removeEventListener('abort', abort);
    }
  }
  api.dispose = () => {
    disposed = true;
    for (const request of pending) request.abort();
    pending.clear();
  };
  return api;
}

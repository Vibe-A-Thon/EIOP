export interface SavedView {
  id: string;
  name: string;
  seeds: string[];
  lens: "domain" | "fact";
  hiddenFacts: string[];
  thumbnail?: string;
  createdAt: string;
}

const KEY_PREFIX = "kgf.views";

function keyFor(principal: string, tenant: string, workspace: string) {
  return `${KEY_PREFIX}:${principal}:${tenant}:${workspace}`;
}

export function listViews(principal: string, tenant: string, workspace: string): SavedView[] {
  try {
    const raw = localStorage.getItem(keyFor(principal, tenant, workspace));
    return raw ? (JSON.parse(raw) as SavedView[]) : [];
  } catch {
    return [];
  }
}

export function saveView(
  principal: string,
  tenant: string,
  workspace: string,
  view: Omit<SavedView, "id" | "createdAt">,
): SavedView[] {
  const views = listViews(principal, tenant, workspace);
  const entry: SavedView = {
    ...view,
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
    createdAt: new Date().toISOString(),
  };  const next = [entry, ...views].slice(0, 30);
  localStorage.setItem(keyFor(principal, tenant, workspace), JSON.stringify(next));
  return next;
}

export function deleteView(
  principal: string,
  tenant: string,
  workspace: string,
  id: string,
): SavedView[] {
  const next = listViews(principal, tenant, workspace).filter((v) => v.id !== id);
  localStorage.setItem(keyFor(principal, tenant, workspace), JSON.stringify(next));
  return next;
}

export function exportViews(views: SavedView[]): string {
  return JSON.stringify({ kind: "kgf.views", version: 1, views }, null, 2);
}

/** Merge imported views into the current scope, de-duping by id. */
export function importViews(
  principal: string,
  tenant: string,
  workspace: string,
  json: string,
): SavedView[] {
  const parsed = JSON.parse(json);
  const incoming: SavedView[] = Array.isArray(parsed) ? parsed : parsed?.views || [];
  if (!Array.isArray(incoming)) throw new Error("Invalid views file");
  const current = listViews(principal, tenant, workspace);
  const byId = new Map(current.map((v) => [v.id, v]));
  for (const v of incoming) {
    if (!v?.name || !Array.isArray(v?.seeds)) continue;
    const entry: SavedView = {
      id: v.id || `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      name: v.name,
      seeds: v.seeds,
      lens: v.lens === "fact" ? "fact" : "domain",
      hiddenFacts: Array.isArray(v.hiddenFacts) ? v.hiddenFacts : [],
      thumbnail: typeof v.thumbnail === "string" ? v.thumbnail : undefined,
      createdAt: v.createdAt || new Date().toISOString(),
    };
    byId.set(entry.id, entry);
  }
  const next = [...byId.values()].slice(0, 50);
  localStorage.setItem(keyFor(principal, tenant, workspace), JSON.stringify(next));
  return next;
}

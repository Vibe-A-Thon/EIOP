export interface SavedView {
  id: string;
  name: string;
  seeds: string[];
  lens: "domain" | "fact";
  hiddenFacts: string[];
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
  };
  const next = [entry, ...views].slice(0, 30);
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

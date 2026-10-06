export function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

export function loadArtifacts(key) {
  try {
    const parsed = JSON.parse(localStorage.getItem(key) || '[]');
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function saveArtifacts(key, items) {
  try {
    localStorage.setItem(key, JSON.stringify(items));
  } catch {
    // storage full or unavailable — artifacts remain session-local
  }
}

export function flattenJson(value, prefix = '', out = []) {
  if (value === null || typeof value !== 'object') {
    out.push({path: prefix || '$', type: typeof value});
    return out;
  }
  if (Array.isArray(value)) {
    if (!value.length) {
      out.push({path: prefix, type: 'array'});
      return out;
    }
    value.slice(0, 20).forEach((item, index) => flattenJson(item, `${prefix}[${index}]`, out));
    return out;
  }
  for (const [key, child] of Object.entries(value)) {
    flattenJson(child, prefix ? `${prefix}.${key}` : key, out);
  }
  return out;
}

export function schemaLabels(schema) {
  return Object.keys(schema?.vertex_labels || {});
}

export function schemaEdgeLabels(schema) {
  return Object.keys(schema?.edge_labels || {});
}

export function labelProperties(schema, label) {
  const entry = schema?.vertex_labels?.[label];
  const props = entry?.properties || entry?.property_keys || [];
  if (Array.isArray(props)) return props;
  if (props && typeof props === 'object') return Object.keys(props);
  return [];
}

export function uid(prefix) {
  return `${prefix}-${Math.random().toString(36).slice(2, 8)}`;
}

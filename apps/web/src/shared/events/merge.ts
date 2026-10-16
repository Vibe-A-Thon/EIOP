export interface GraphEvent {
  event_id: number;
  type: string;
  data: Record<string, unknown>;
  timestamp?: string;
}

export function mergeEvents(previous: GraphEvent[], incoming: unknown, cursor: number, maximum = 1000) {
  if (!Array.isArray(incoming)) throw new Error('Event service returned an unsupported response.');
  const accepted = incoming.map(value => {
    if (!value || !Number.isSafeInteger(value.event_id) || value.event_id < 1 || typeof value.type !== 'string'
      || !value.data || typeof value.data !== 'object' || Array.isArray(value.data)) {
      throw new Error('Event service returned an invalid event.');
    }
    return value as GraphEvent;
  }).filter(event => event.event_id > cursor).sort((left, right) => left.event_id - right.event_id);
  const records = new Map(previous.map(event => [event.event_id, event]));
  for (const event of accepted) records.set(event.event_id, event);
  return {events: [...records.values()].sort((left, right) => left.event_id - right.event_id).slice(-maximum),
    cursor: accepted.length ? accepted[accepted.length - 1].event_id : cursor};
}

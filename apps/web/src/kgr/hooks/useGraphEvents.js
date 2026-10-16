import {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import {createApiClient} from '../../shared/api/client.ts';
import {mergeEvents} from '../../shared/events/merge.ts';

export default function useGraphEvents(apiBase, token, request) {
  const fallback = useMemo(() => request ? null : createApiClient(token || ''), [request, token]);
  const api = request || fallback;
  const [events, setEvents] = useState([]);
  const [status, setStatus] = useState('disconnected');
  const paused = useRef(false);
  const cursor = useRef(0);
  const snapshot = useRef([]);
  useEffect(() => () => fallback?.dispose(), [fallback]);

  useEffect(() => {
    if (!apiBase || !api) return;
    let active = true, stopped = false, timer, controller, failures = 0;
    snapshot.current = [];
    cursor.current = 0; paused.current = false;
    setEvents([]); setStatus('connecting');
    async function poll() {
      if (!active) return;
      if (paused.current || document.hidden) {timer = setTimeout(poll, 1000); return;}
      controller = new AbortController();
      let delay = 2000;
      try {
        const data = await api(`/api/v1/graph/events?since_id=${cursor.current}&limit=100`, undefined, undefined, {signal: controller.signal});
        if (!active || paused.current) return;
        if (data?.gap === true) {stopped = true; setStatus('stale'); return;}
        const merged = mergeEvents(snapshot.current, data?.events, cursor.current);
        snapshot.current = merged.events; cursor.current = merged.cursor;
        setEvents(snapshot.current); setStatus('polling'); failures = 0;
        if (data.events.length === 100) delay = 250;
      } catch (error) {
        if (!active || error.name === 'AbortError') return;
        if (error.status === 401 || error.status === 403) {stopped = true; setStatus('unauthorized'); return;}
        setStatus('disconnected');
        delay = Math.min(30000, 1000 * 2 ** Math.min(++failures, 5)) * (.8 + Math.random() * .4);
      } finally {
        if (active && !stopped) timer = setTimeout(poll, delay);
      }
    }
    poll();
    return () => {active = false; clearTimeout(timer); controller?.abort();};
  }, [apiBase, api]);
  const pause = useCallback(() => {paused.current = true; setStatus('paused');}, []);
  const resume = useCallback(() => {paused.current = false; setStatus('connecting');}, []);
  const clear = useCallback(() => {snapshot.current = []; setEvents([]);}, []);
  return {events, status, pause, resume, clear};
}

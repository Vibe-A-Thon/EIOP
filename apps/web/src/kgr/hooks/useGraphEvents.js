import {useCallback, useEffect, useRef, useState} from 'react';

const MAX_EVENTS = 1000;
const RECONNECT_DELAYS = [1000, 2000, 4000, 8000, 16000, 30000];

export default function useGraphEvents(apiBase) {
  const [events, setEvents] = useState([]);
  const [status, setStatus] = useState('disconnected');
  const wsRef = useRef(null);
  const reconnectAttempt = useRef(0);
  const lastEventId = useRef(0);
  const paused = useRef(false);

  const connect = useCallback(() => {
    if (!apiBase) return;
    const wsUrl = apiBase.replace(/^http/, 'ws') + '/ws/graph/events';
    setStatus('connecting');

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setStatus('connected');
        reconnectAttempt.current = 0;
        if (lastEventId.current > 0) {
          fetch(`${apiBase}/api/v1/graph/events?since_id=${lastEventId.current}&limit=100`)
            .then(r => r.json())
            .then(data => {
              if (data.events?.length) {
                setEvents(prev => {
                  const merged = [...prev, ...data.events];
                  return merged.slice(-MAX_EVENTS);
                });
                const maxId = Math.max(...data.events.map(e => e.event_id));
                if (maxId > lastEventId.current) lastEventId.current = maxId;
              }
            })
            .catch(() => {});
        }
      };

      ws.onmessage = (e) => {
        if (paused.current) return;
        try {
          const event = JSON.parse(e.data);
          if (event.event_id > lastEventId.current) {
            lastEventId.current = event.event_id;
          }
          setEvents(prev => [...prev.slice(-(MAX_EVENTS - 1)), event]);
        } catch (_) {}
      };

      ws.onclose = () => {
        setStatus('disconnected');
        wsRef.current = null;
        const delay = RECONNECT_DELAYS[Math.min(reconnectAttempt.current, RECONNECT_DELAYS.length - 1)];
        reconnectAttempt.current++;
        setTimeout(connect, delay);
      };

      ws.onerror = () => {
        ws.close();
      };

      wsRef.current = ws;
    } catch (_) {
      setStatus('error');
    }
  }, [apiBase]);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [connect]);

  const pause = useCallback(() => { paused.current = true; }, []);
  const resume = useCallback(() => { paused.current = false; }, []);
  const clear = useCallback(() => setEvents([]), []);

  return {events, status, pause, resume, clear};
}

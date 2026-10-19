import { useCallback, useEffect, useRef, useState } from 'react';
import type { Snapshot } from './types';

export type View = 'participant' | 'host' | 'display';
type Result = Snapshot | { error: string; state?: Snapshot };
export default function useClassroom(view: View) {
  const [state, setState] = useState<Snapshot | null>(null);
  const [error, setError] = useState('');
  const [connected, setConnected] = useState(true);
  const [busy, setBusy] = useState(false);
  const participant = useRef('');
  const latest = useRef(0);
  const sync = useRef({ server: 0, received: performance.now() });
  const mounted = useRef(true);
  const mutating = useRef(false);
  const accept = useCallback((s: Snapshot) => {
    if (!mounted.current || s.revision < latest.current) return;
    latest.current = s.revision;
    sync.current = { server: s.now, received: performance.now() };
    if (s.participantId) { participant.current = s.participantId; sessionStorage.setItem('design-lab-participant', s.participantId); }
    setState(s); setConnected(true);
  }, []);
  const request = useCallback(async (path: string, body?: object, signal?: AbortSignal) => {
    const response = await fetch(path, {
      method: body ? 'POST' : 'GET', headers: { 'Content-Type': 'application/json', 'X-Participant': participant.current },
      body: body ? JSON.stringify({ ...body, participantId: participant.current }) : undefined, signal,
    });
    const data: Result = await response.json();
    if ('error' in data) { if (data.state) accept(data.state); throw new Error(data.error); }
    accept(data); return data;
  }, [accept]);
  const refresh = useCallback(() => request(view === 'host' ? '/api/host/state' : view === 'display' ? '/api/display' : '/api/state'), [view, request]);
  useEffect(() => {
    mounted.current = true;
    let disposed = false;
    let timer = 0;
    const controller = new AbortController();
    const poll = async () => {
      try {
        const data = await request(view === 'host' ? '/api/host/state' : view === 'display' ? '/api/display' : '/api/state', undefined, controller.signal);
        if (data.phase === 'closed') return;
      } catch (err) { if (!disposed && !(err instanceof DOMException && err.name === 'AbortError')) setConnected(false); }
      if (!disposed) timer = window.setTimeout(poll, 650);
    };
    const start = async () => {
      try {
        if (view === 'participant') {
          participant.current = sessionStorage.getItem('design-lab-participant') || '';
          await request('/api/join', {}, controller.signal);
        }
        if (!disposed) await poll();
      } catch (err) { if (!disposed) { setError(err instanceof Error ? err.message : 'Could not connect to the lab.'); setConnected(false); } }
    };
    void start();
    return () => { disposed = true; mounted.current = false; controller.abort(); clearTimeout(timer); };
  }, [request, view]);
  const act = useCallback(async (path: string, body: object = {}) => {
    if (mutating.current) return;
    mutating.current = true; setBusy(true); setError('');
    try { return await request(path, body); }
    catch (err) { setError(err instanceof Error ? err.message : 'Please try again.'); }
    finally { mutating.current = false; if (mounted.current) setBusy(false); }
  }, [request]);
  const now = useCallback(() => sync.current.server + performance.now() - sync.current.received, []);
  return { state, error, connected, busy, act, refresh, now };
}

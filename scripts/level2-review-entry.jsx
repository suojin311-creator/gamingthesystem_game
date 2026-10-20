import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import film from 'virtual:level2-cinematic-film';
import './level2-review.css';

const CHANNEL = 'level2-cinematic';
const choices = {
  'visible-heavy': { label: 'Visible', kind: 'three', branch: 'visible', ids: ['prep', 'part', 'focus'] },
  'quality-heavy': { label: 'Quality', kind: 'three', branch: 'quality', ids: ['discuss', 'reflect', 'peer'] },
  'mixed-broad': { label: 'Mixed', kind: 'three', branch: 'mixed', ids: ['prep', 'discuss', 'peer'] },
  six: { label: 'Six', kind: 'six', branch: 'mixed', ids: ['prep', 'discuss', 'peer'] },
  '100': { label: '100 · Final', kind: 'checklist', branch: 'mixed', ids: ['prep', 'discuss', 'peer'] },
};
function Review() {
  const query = new URLSearchParams(location.search);
  const state = query.get('state') === 'final' ? '100' : query.get('state') ?? 'mixed-broad';
  const plan = state === 'full' ? ['mixed-broad', 'six', '100'] : [choices[state] ? state : 'mixed-broad'];
  const [index, setIndex] = useState(0);
  const [run, setRun] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [elapsed, setElapsed] = useState(0);
  const [duration, setDuration] = useState(0);
  const [speed, setSpeed] = useState(1);
  const [done, setDone] = useState(false);
  const [events, setEvents] = useState([]);
  const frame = useRef(null);
  const token = useMemo(() => crypto.randomUUID(), [run, index]);
  const item = choices[plan[index]];
  const request = useMemo(() => ({ sceneId: item.kind === 'three' ? `level2.three.${item.branch}` : `level2.${item.kind}`, kind: item.kind, branch: item.branch, selectedMetricIds: item.ids, metricCount: item.kind === 'three' ? 3 : item.kind === 'six' ? 6 : 100, playerName: 'Review' }), [item]);
  const control = (action, value) => frame.current?.contentWindow?.postMessage({ channel: CHANNEL, type: 'control', runId: token, action, value }, '*');
  useEffect(() => {
    const receive = event => {
      const data = event.data;
      if (event.source !== frame.current?.contentWindow || data?.channel !== CHANNEL) return;
      if (data.type === 'ready') frame.current.contentWindow.postMessage({ channel: CHANNEL, type: 'start', runId: token, request, preview: true, reducedMotion: query.get('reduced') === '1' || matchMedia('(prefers-reduced-motion: reduce)').matches }, '*');
      if (data.runId !== token) return;
      if (data.type === 'progress') { setElapsed(data.elapsed); setDuration(data.duration); }
      if (data.type === 'complete') { setDone(true); setPlaying(false); setEvents(previous => previous.includes(token) ? previous : [...previous, token]); }
    };
    window.addEventListener('message', receive);
    return () => window.removeEventListener('message', receive);
  }, [token, request]);
  useEffect(() => {
    if (!done || index >= plan.length - 1) return;
    const timer = setTimeout(() => { setIndex(index + 1); setDone(false); setPlaying(true); setElapsed(0); setDuration(0); setSpeed(1); }, 900);
    return () => clearTimeout(timer);
  }, [done, index, plan.length]);
  const replay = () => { setIndex(0); setRun(run + 1); setDone(false); setPlaying(true); setElapsed(0); setDuration(0); setSpeed(1); setEvents([]); };
  return <main className="level2-review">
    <header><h1>Level 2 animation preview</h1><a href="./START-HERE.html">All previews</a></header>
    <nav aria-label="Animation clips">{['visible-heavy', 'quality-heavy', 'mixed-broad', 'six', '100'].map(id => <a key={id} href={`?state=${id}`} aria-current={plan[index] === id ? 'page' : undefined}>{choices[id].label}</a>)}<a href="?state=full">All placeholder clips</a></nav>
    <div className="review-controls">
      <button disabled={!duration || done} onClick={() => { control(playing ? 'pause' : 'play'); setPlaying(!playing); }}>{playing ? 'Pause' : 'Play'}</button>
      <button onClick={replay}>Replay</button>
      <label>Speed <select aria-label="Speed" value={speed} onChange={event => { const value = Number(event.target.value); setSpeed(value); control('speed', value); }}><option value={1}>1×</option><option value={2}>2×</option><option value={4}>4×</option></select></label>
      <label className="review-scrub">Preview time <input aria-label="Preview time" type="range" min={0} max={duration || 1} step={.05} value={elapsed} disabled={!duration || done} onChange={event => { const value = Number(event.target.value); control('seek', value); setElapsed(value); setPlaying(false); }} /></label>
      <output>{elapsed.toFixed(1)} / {duration.toFixed(1)}s</output>
    </div>
    <div className="review-stage"><iframe key={token} ref={frame} title="Level 2 classroom animation" srcDoc={film} /></div>
    <footer data-completion-count={events.length} data-complete={done} data-kind={item.kind}>Silent preview · {done ? 'Clip complete' : playing ? 'Playing' : 'Paused'}</footer>
  </main>;
}
createRoot(document.getElementById('root')).render(<Review />);

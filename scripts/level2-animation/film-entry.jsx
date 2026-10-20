import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Level2ConsequencesSequence } from '@partner/cinematics/level2/Level2ConsequencesSequence';
import { getLevel2Shots, shotAt } from '@partner/cinematics/level2/level2Timeline';
import { level2Performance } from '@partner/cinematics/level2/level2Performance';
import { DialogueLayer } from '@partner/cinematics/shared/engine/DialogueLayer/DialogueLayer';
import neutral from '@partner-assets/characters/alex-rig/production/base/ALEX-PROD-001 — Seated Alex Neutral.png';
import blink from '@partner-assets/characters/alex-rig/production/expressions/ALEX-PROD-002 — Blink.png';
import pleased from '@partner-assets/characters/alex-rig/production/expressions/ALEX-PROD-003 — Pleased.png';
import uncertain from '@partner-assets/characters/alex-rig/production/expressions/ALEX-PROD-004 — Uncertain.png';
import hand from '@partner-assets/characters/alex-rig/production/actions/checking/ALEX-HAND-CHECKING.png';
import look from '@partner-assets/characters/alex-rig/production/actions/checking/ALEX-PROD-005-CLEAN.png';
import classroom from '@partner-scenes/REF-L2-003 — Mixed : Broad Classroom.png?inline';
import { SPEAKER_COLORS, CAPTION_SHADOW } from '../../src/shared/data/cinematicPalette.js';
import { COVER_SECONDS, createPacing, sampleAt, finalCover } from './pacing.mjs';
import { dissolveFrame } from '../cinematic-dissolve.mjs';
import './film.css';

const CHANNEL = 'level2-cinematic';
const METRICS = {
  prep: 'pre-class-preparation', part: 'in-class-participation', focus: 'on-task-focus',
  discuss: 'in-class-discussion-quality', reflect: 'learning-reflection-quality', peer: 'online-peer-response-quality',
};
const CATEGORIES = { visible: 'visible-behaviour-heavy', quality: 'quality-depth-heavy', mixed: 'mixed-broad' };
const IGNORE = () => {};
function makeRequest(config) {
  const input = config.request;
  return { requestId: config.runId, cinematicId: 'level2', level: 2, input: {
    phase: input.kind === 'checklist' ? '100' : input.kind,
    selectedMetrics: input.kind === 'three' ? input.selectedMetricIds.map(id => METRICS[id]) : Object.values(METRICS),
    ...(input.kind === 'three' ? { resultCategory: CATEGORIES[input.branch] } : {}),
  } };
}
function keyAt(shots, sample) {
  const current = shotAt(shots, sample.sourceSeconds);
  const acting = level2Performance(current.shot.id, current.time);
  return `${current.shot.id}:${acting.view}:${acting.expression === 'uncertain' ? 'uncertain' : 'base'}`;
}

function Film({ config }) {
  const request = useMemo(() => makeRequest(config), [config]);
  const shots = useMemo(() => getLevel2Shots(request), [request]);
  const pacing = useMemo(() => createPacing(config.request.kind, shots), [config.request.kind, shots]);
  const [elapsed, setElapsed] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [handoff, setHandoff] = useState('idle');
  const [finished, setFinished] = useState(false);
  const clock = useRef(0);
  const phase = useRef('idle');
  const pending = useRef(0);
  const complete = useRef(false);
  const surface = useRef(null);
  const transition = useRef(null);
  const visible = useRef(!document.hidden);
  const lastKey = useRef(keyAt(shots, sampleAt(pacing, 0)));
  const speed = useRef(1);
  const move = value => { phase.current = value; setHandoff(value); };
  const commit = () => {
    clock.current = pending.current;
    lastKey.current = keyAt(shots, sampleAt(pacing, clock.current));
    setElapsed(clock.current);
  };
  useEffect(() => () => transition.current?.cancel(), []);
  useEffect(() => {
    const visibility = () => { visible.current = !document.hidden; };
    document.addEventListener('visibilitychange', visibility);
    return () => document.removeEventListener('visibilitychange', visibility);
  }, []);
  useEffect(() => {
    if (!config.preview) return;
    const control = event => {
      const data = event.data;
      if (event.source !== window.parent || data?.channel !== CHANNEL || data.runId !== config.runId || data.type !== 'control') return;
      if (data.action === 'play') { setPlaying(true); transition.current?.play(); }
      if (data.action === 'pause') { setPlaying(false); transition.current?.pause(); }
      if (data.action === 'speed' && [1, 2, 4].includes(data.value)) speed.current = data.value;
      if (data.action === 'seek' && Number.isFinite(data.value) && !complete.current) {
        transition.current?.cancel();
        clock.current = Math.max(0, Math.min(pacing.duration - .001, data.value));
        lastKey.current = keyAt(shots, sampleAt(pacing, clock.current));
        setElapsed(clock.current); setPlaying(false); move('idle');
      }
    };
    window.addEventListener('message', control);
    return () => window.removeEventListener('message', control);
  }, [config, pacing, shots]);
  useEffect(() => {
    if (!playing || finished) return;
    let frame = 0;
    let previous = performance.now();
    let lastProgress = -1;
    const tick = now => {
      if (visible.current && phase.current === 'idle') {
        const next = Math.min(pacing.duration, clock.current + Math.min(now - previous, 100) / 1000 * speed.current);
        const nextKey = keyAt(shots, sampleAt(pacing, next));
        if (nextKey !== lastKey.current) {
          pending.current = next; move('dissolving');
          transition.current = dissolveFrame(surface.current, commit, { duration: COVER_SECONDS * 1000, reducedMotion: config.reducedMotion });
          transition.current.finished.then(() => move('idle'));
        }
        else { clock.current = next; setElapsed(next); }
      }
      previous = now;
      if (config.preview && now - lastProgress >= 150) {
        window.parent.postMessage({ channel: CHANNEL, type: 'progress', runId: config.runId, elapsed: clock.current, duration: pacing.duration, playing: true }, '*');
        lastProgress = now;
      }
      if (clock.current >= pacing.duration) { complete.current = true; setFinished(true); }
      else frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing, finished, config, pacing, shots]);
  useEffect(() => {
    if (!finished) return;
    let second = 0;
    const first = requestAnimationFrame(() => { second = requestAnimationFrame(() => {
      window.parent.postMessage({ channel: CHANNEL, type: 'complete', runId: config.runId }, '*');
    }); });
    return () => { cancelAnimationFrame(first); cancelAnimationFrame(second); };
  }, [finished, config.runId]);
  const sample = sampleAt(pacing, elapsed);
  const current = shotAt(shots, sample.sourceSeconds);
  const line = sample.dialogue;
  const player = line?.speaker === 'You';
  const color = SPEAKER_COLORS[player ? 'player' : 'alex'];
  const captionStyle = { color, WebkitTextStroke: '.035em #172019', paintOrder: 'stroke fill', textShadow: CAPTION_SHADOW, fontStyle: player ? 'italic' : 'normal' };
  return <main ref={surface} className="l2-film" data-kind={config.request.kind} data-scene-id={config.request.sceneId} data-shot={current.shot.id} data-elapsed={elapsed.toFixed(3)} data-duration={pacing.duration.toFixed(3)} data-handoff={handoff} data-finished={finished} data-player-name={config.request.playerName}>
    <Level2ConsequencesSequence request={request} elapsed={sample.sourceSeconds} active={playing && !finished && visible.current} reducedMotion={config.reducedMotion} onComplete={IGNORE} />
    {line && <div className="l2-spoken" data-speaker={player ? 'player' : 'alex'} style={captionStyle}>
      <p className="l2-speaker" style={{ ...captionStyle, fontStyle: 'normal' }}>{player ? 'You' : 'Alex'}</p>
      <DialogueLayer style={captionStyle}>{line.text}</DialogueLayer>
    </div>}
    <div className="l2-film-cover" aria-hidden="true" style={{ opacity: finished ? 1 : finalCover(pacing, elapsed) }} />
  </main>;
}

function Entry() {
  const [config, setConfig] = useState(null);
  const [failed, setFailed] = useState(false);
  const started = useRef(false);
  useEffect(() => {
    const receive = event => {
      const data = event.data;
      const request = data?.request;
      if (event.source !== window.parent || data?.channel !== CHANNEL || data.type !== 'start' || started.current || typeof data.runId !== 'string') return;
      if (!request || !['three', 'six', 'checklist'].includes(request.kind) || !CATEGORIES[request.branch] || request.selectedMetricIds?.length !== 3 || new Set(request.selectedMetricIds).size !== 3 || request.selectedMetricIds.some(id => !METRICS[id]) || typeof request.playerName !== 'string') return;
      started.current = true;
      const plates = [neutral, blink, pleased, uncertain, hand, look, ...(request.kind === 'checklist' ? [classroom] : [])];
      Promise.all(plates.map(src => { const image = new Image(); image.src = src; return image.decode(); }))
        .then(() => setConfig(data), () => setFailed(true));
    };
    window.addEventListener('message', receive);
    window.parent.postMessage({ channel: CHANNEL, type: 'ready' }, '*');
    return () => window.removeEventListener('message', receive);
  }, []);
  return config ? <Film config={config} /> : <p className="l2-film-loading" role="status">{failed ? 'The classroom could not load. Please reopen the game.' : 'Preparing the classroom…'}</p>;
}
createRoot(document.getElementById('root')).render(<Entry />);

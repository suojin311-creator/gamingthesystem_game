import { useEffect, useRef, useState } from 'react';
import type { Phase } from '../state';
import type { Cue } from '../useFeedback';

type Line = { speaker: 'Maya' | 'Alex'; text: string };

function TypingDots({ speaker }: { speaker: string }) {
  return <span className="typing-indicator" role="status" aria-label={`${speaker} is typing`}><i /><i /><i /></span>;
}

export default function Dialogue({ phase, playerName, studentQuote, enabled, paused = false, play, onSettled }: {
  phase: Phase; playerName: string; studentQuote?: string; enabled: boolean;
  play: (cue: Cue) => void; onSettled: () => void;
  paused?: boolean;
}) {
  const single: Record<Phase, string> = {
    choose: 'Where should I start?', predict: 'What do I expect students to do?',
    result: 'Looking good. Let’s check the classroom.', cinematic: '',
    review: 'The score is up. What about learning?', complete: 'Maybe one metric is too narrow.',
  };
  const lines: Line[] = [{ speaker: 'Maya', text: single[phase] }];
  if (phase === 'review') lines.push({ speaker: 'Alex', text: studentQuote || 'I met the criteria.' });

  const [beat, setBeat] = useState(0);
  const [inView, setInView] = useState(false);
  const [pageVisible, setPageVisible] = useState(!document.hidden);
  const container = useRef<HTMLElement>(null);
  const remaining = useRef(650);
  const lastSound = useRef(-1);
  const settled = useRef(false);
  const callback = useRef(onSettled);
  callback.current = onSettled;
  const lastBeat = lines.length * 2 - 1;

  useEffect(() => {
    const observer = new IntersectionObserver(entries => setInView(entries[0].isIntersecting), { threshold: 0.1 });
    if (container.current) observer.observe(container.current);
    const visibility = () => setPageVisible(!document.hidden);
    document.addEventListener('visibilitychange', visibility);
    return () => { observer.disconnect(); document.removeEventListener('visibilitychange', visibility); };
  }, []);

  useEffect(() => {
    if (!enabled || paused || !inView || !pageVisible) return;
    if (beat % 2 === 1 && lastSound.current !== beat) { play('message'); lastSound.current = beat; }
    if (beat === lastBeat) {
      if (!settled.current) { settled.current = true; callback.current(); }
      return;
    }
    const delay = remaining.current;
    const start = performance.now();
    let fired = false;
    const timer = window.setTimeout(() => {
      fired = true;
      remaining.current = beat % 2 === 0 ? 1400 : 650;
      setBeat(value => value + 1);
    }, delay);
    return () => { window.clearTimeout(timer); if (!fired) remaining.current = Math.max(0, delay - (performance.now() - start)); };
  }, [beat, enabled, paused, inView, pageVisible, lastBeat, play]);

  return <section ref={container} className={`dialogue-strip ${phase === 'review' ? 'two-voices' : ''}`} aria-label="Character dialogue">
    {enabled && lines.map((line, index) => {
      if (beat < index * 2) return null;
      const name = line.speaker === 'Maya' ? playerName : 'Alex';
      const typing = beat === index * 2;
      const alex = line.speaker === 'Alex';
      return <div key={index} className={`dialogue-character ${alex ? 'alex-character' : 'maya-character'}`} data-speaker={line.speaker} data-order={index}>
        <span className={`avatar ${alex ? 'alex-avatar' : 'maya-avatar'}`} aria-hidden="true">{name.charAt(0).toUpperCase()}</span>
        <div className={`speech-bubble ${alex ? 'alex-bubble' : 'maya-bubble'} ${typing ? 'is-typing' : 'message-arrived'}`}>
          <span className="speaker-name">{name}</span>
          {typing ? <TypingDots speaker={name} /> : <p aria-live="polite">{line.text}</p>}
        </div>
      </div>;
    })}
  </section>;
}

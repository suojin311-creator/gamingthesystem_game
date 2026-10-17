import { useEffect, useRef, useState } from 'react';
import type { Cue } from '../hooks/useFeedback';
import { readingTime } from '../utils/readingTime';
import '../styles/conversation.css';

export type ConversationLine = { speaker: 'Maya' | 'Alex'; name: string; text: string; delivery?: 'thought' | 'speech' };

export default function Conversation({ lines, enabled = true, paused = false, play, onSettled, onLastMessage, typingDelay = 650, readDelay = readingTime }: {
  lines: ConversationLine[]; enabled?: boolean; paused?: boolean;
  play: (cue: Cue) => void; onSettled: () => void;
  onLastMessage?: () => void; typingDelay?: number; readDelay?: (text: string) => number;
}) {
  const [beat, setBeat] = useState(0);
  const [inView, setInView] = useState(false);
  const [pageVisible, setPageVisible] = useState(!document.hidden);
  const container = useRef<HTMLElement>(null);
  const remaining = useRef(typingDelay);
  const lastSound = useRef(-1);
  const settled = useRef(false);
  const lastMessageReported = useRef(false);
  const callback = useRef(onSettled);
  callback.current = onSettled;
  const lastMessageCallback = useRef(onLastMessage);
  lastMessageCallback.current = onLastMessage;
  const lastBeat = lines.length * 2 - 1;

  useEffect(() => {
    const observer = new IntersectionObserver(entries => setInView(entries[0].isIntersecting), { threshold: 0.1 });
    if (container.current) observer.observe(container.current);
    const visibility = () => setPageVisible(!document.hidden);
    document.addEventListener('visibilitychange', visibility);
    return () => { observer.disconnect(); document.removeEventListener('visibilitychange', visibility); };
  }, []);

  useEffect(() => {
    if (!enabled || paused || !inView || !pageVisible || !lines.length) return;
    if (beat % 2 === 1 && lastSound.current !== beat) { play('message'); lastSound.current = beat; }
    if (beat === lastBeat && !lastMessageReported.current) {
      lastMessageReported.current = true;
      lastMessageCallback.current?.();
    }
    if (settled.current) return;
    const delay = remaining.current;
    const start = performance.now();
    let fired = false;
    const timer = window.setTimeout(() => {
      fired = true;
      if (beat === lastBeat) { settled.current = true; callback.current(); return; }
      remaining.current = beat % 2 === 0 ? readDelay(lines[Math.floor(beat / 2)].text) : typingDelay;
      setBeat(value => value + 1);
    }, delay);
    return () => { window.clearTimeout(timer); if (!fired) remaining.current = Math.max(0, delay - (performance.now() - start)); };
  }, [beat, enabled, paused, inView, pageVisible, lastBeat, play, lines, typingDelay, readDelay]);

  useEffect(() => {
    if (!enabled || paused || !inView || !pageVisible || beat % 2 === 0) return;
    // Keep a newly arrived reply visible when a conversation grows on a small screen.
    const frame = requestAnimationFrame(() => {
      const message = container.current?.querySelector<HTMLElement>(`[data-order="${Math.floor(beat / 2)}"]`);
      const rect = message?.getBoundingClientRect();
      if (rect && rect.bottom > innerHeight - 18) message?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
    return () => cancelAnimationFrame(frame);
  }, [beat, enabled, paused, inView, pageVisible]);

  return <section ref={container} className={`dialogue-strip conversation ${lines.length > 1 ? 'two-voices' : ''}`} aria-label="Character dialogue">
    {enabled && lines.map((line, index) => {
      if (beat < index * 2) return null;
      const typing = beat === index * 2;
      const alex = line.speaker === 'Alex';
      const thought = line.delivery === 'thought';
      const continuation = index > 0 && lines[index - 1].speaker === line.speaker && lines[index - 1].name === line.name;
      return <div key={index} className={`dialogue-character ${alex ? 'alex-character' : 'maya-character'} ${continuation ? 'message-continuation' : ''}`} data-speaker={line.speaker} data-order={index}>
        <span className={`avatar ${alex ? 'alex-avatar' : 'maya-avatar'}`} aria-hidden="true">{line.name.charAt(0).toUpperCase()}</span>
        <div className={`speech-bubble ${alex ? 'alex-bubble' : 'maya-bubble'} ${thought ? 'thought-bubble' : ''} ${typing ? 'is-typing' : 'message-arrived'}`} data-delivery={thought ? 'thought' : 'speech'}>
          {thought && <svg className="thought-cloud" viewBox="0 0 400 140" preserveAspectRatio="none" aria-hidden="true"><path vectorEffect="non-scaling-stroke" d="M50 126C22 130 7 111 16 94C-2 75 12 51 35 50C29 25 52 7 78 15C95-3 130-2 149 8C175-7 216-3 236 13C264 0 295 5 308 23C339 17 363 28 366 47C398 54 404 76 387 94C403 111 380 131 354 127C335 144 300 143 284 130C253 146 213 140 201 132C176 146 136 141 121 129C95 143 66 142 50 126Z" /></svg>}
          <div className="message-labels"><span className={`speaker-name ${continuation ? 'sr-only' : ''}`}>{line.name}</span>{thought && <small className="thought-label">Thinking</small>}</div>
          {typing ? <span className="typing-indicator" role="status" aria-label={`${line.name} is ${thought ? 'thinking' : 'typing'}`}><i /><i /><i /></span> : <p aria-live="polite">{line.text}</p>}
        </div>
      </div>;
    })}
  </section>;
}

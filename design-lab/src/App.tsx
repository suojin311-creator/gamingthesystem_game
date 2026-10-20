import { useEffect, useRef, useState, type ReactNode } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import useRankingSound from './useRankingSound';
import useClassroom, { type View } from './useClassroom';
import type { Choice, Snapshot } from './types';
import { Arrow, Bomb, Check, Clock, Flower } from './Icons';

const PROMPT = 'How would you know Alex is really learning?';
const QUESTIONS = {
  question1: 'Did the most flowers mean the deepest thinking?',
  question2: 'Did knowing there would be a ranking change what you wrote?',
};
const phaseLabels: Record<string, string> = { lobby: 'Gathering', writing: 'Writing', review: 'Sharing', ranking: 'The ranking', question1: 'A question', question2: 'A question', ending: 'Goodhart’s Law', empty: 'Closing', closed: 'Classroom closed' };
function useTime(now: () => number) { const [time, setTime] = useState(now); useEffect(() => { const t = setInterval(() => setTime(now()), 80); return () => clearInterval(t); }, [now]); return time; }
function remaining(deadline: number, now: number) { return Math.max(0, Math.ceil((deadline - now) / 1000)); }
function formatTime(n: number) { return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, '0')}`; }
function Timer({ seconds, label }: { seconds: number; label?: string }) { return <div className={`timer ${seconds <= 5 ? 'last-seconds' : ''}`}><Clock />{label && <span>{label}</span>}<strong>{formatTime(seconds)}</strong></div>; }
function Brand({ view, phase, sound }: { view: View; phase?: string; sound: ReturnType<typeof useRankingSound> }) { return <header className="lab-header"><div className="wordmark"><span className="emblem">g<span>s</span></span><span>GAMING<br/><b>THE SYSTEM</b></span></div><div className="lab-header-title">DESIGN LAB</div><div className="header-controls"><button type="button" className="sound-toggle" aria-pressed={!sound.muted} disabled={!sound.available} onClick={sound.toggle}>{sound.available ? sound.muted ? 'Sound off' : 'Sound on' : 'No audio'}</button><span className="phase-pill"><i/>{view === 'host' ? 'Host controls' : phaseLabels[phase || 'lobby']}</span></div></header>; }
function Button({ children, disabled, onClick, secondary = false }: { children: ReactNode; disabled?: boolean; onClick: () => void; secondary?: boolean }) { return <button type="button" className={secondary ? 'button secondary' : 'button primary'} disabled={disabled} onClick={onClick}>{children}<Arrow /></button>; }
function Waiting({ title, children }: { title: string; children: ReactNode }) { return <section className="waiting paper"><div className="waiting-illustration" aria-hidden="true"><span/><span/><span/></div><h1>{title}</h1><div className="waiting-copy">{children}</div></section>; }

function Ranking({ state, now }: { state: Snapshot; now: number }) {
  const body = useRef<HTMLDivElement>(null);
  const reduced = useReducedMotion();
  const n = state.ranking.length;
  const isScan = state.phase === 'ranking';
  const progress = isScan ? Math.min(1, Math.max(0, (now - state.startedAt) / state.rankingMs)) : 1;
  const position = (n - 1) * progress * progress;
  const active = Math.min(n - 1, Math.floor(position));
  useEffect(() => {
    if (!body.current) return;
    const y = Math.max(0, position * 88 - body.current.clientHeight / 2 + 44);
    body.current.scrollTop = y;
  }, [position]);
  return <section className={`ranking paper ${isScan ? 'scanning' : ''}`} aria-label="Final flower ranking">
    <div className="section-top"><span className="eyebrow">THE RESULTS</span><span>{n} reflections</span></div>
    <h1>Flowers received.</h1>
    <div className="rank-head"><span>Rank</span><span>Reflection</span><span><Flower/><span className="sr-only">Flowers</span></span></div>
    <div className="rank-window" ref={body} tabIndex={-1}><div className="rank-body">
      {state.ranking.map((r, i) => <div className="rank-row" data-active={i === active} key={r.id}><strong className="rank-number">{String(r.rank).padStart(2, '0')}</strong><div><span className="rank-label">{r.label}</span><p>{r.text}</p></div><strong className="flower-count">{r.flowers}</strong></div>)}
      {!!n && <div aria-hidden="true" className="scan-frame" style={{ transform: `translateY(${position * 88}px)`, transitionDuration: reduced ? '0s' : '80ms' }}/>}
    </div></div>
  </section>;
}

function Closing() {
  return <section className="closing paper" aria-label="Goodhart’s Law"><div className="portrait-panel"><img src="/goodhart.png" alt="An illustrated half-length portrait of Charles Goodhart."/></div><div className="closing-copy"><span className="eyebrow">ONE LAST THOUGHT</span><h1>Goodhart’s Law.</h1><blockquote>“When a measure becomes a target, it ceases to be a good measure.”</blockquote><p className="attribution">Charles Goodhart</p><div className="closing-rule"/></div></section>;
}

type Lab = ReturnType<typeof useClassroom>;
function Participant({ lab, time }: { lab: Lab; time: number }) {
  const { state: s, act, busy, refresh } = lab;
  const [text, setText] = useState('');
  const [expired, setExpired] = useState('');
  const [reaction, setReaction] = useState<Choice | ''>('');
  const reduced = useReducedMotion();
  const card = s?.card;
  useEffect(() => { setExpired(''); setReaction(''); }, [card?.id]);
  useEffect(() => {
    if (!card || s?.phase !== 'review') return;
    const timer = window.setTimeout(() => { setExpired(card.id); void refresh().catch(() => undefined); }, Math.max(0, card.deadline - lab.now()));
    return () => clearTimeout(timer);
  }, [card?.id, card?.deadline, s?.phase, lab.now, refresh]);
  if (!s) return null;
  if (s.phase === 'lobby') return <section className="intro paper"><div className="intro-copy"><span className="eyebrow">AFTER THE GAME</span><h1>Design Lab.</h1><p className="intro-main">Your reflection will be shared anonymously.</p><p>Everyone will vote, and a ranking will follow.</p><div className="gathering"><span className="pulsing-dot"/><span>Waiting for the lab to begin.</span></div></div><aside className="intro-aside"><div className="giant-flower"><Flower/></div><div className="intro-number">{String(s.joined).padStart(2, '0')}<span>participants joined</span></div><span className="quiet-label">A different perspective starts here.</span></aside></section>;
  if (s.phase === 'writing') {
    if (s.hasSubmitted || s.isAudience) return <><div className="above-paper"><span className="eyebrow">WRITING</span><Timer seconds={remaining(s.deadline, time)}/></div><Waiting title={s.hasSubmitted ? 'Submitted.' : 'You’re in the audience.'}><p>Waiting for the sharing round.</p><span className="submitted-mark"><Check/></span></Waiting></>;
    return <section className="writing paper"><div className="section-top"><span className="eyebrow">YOUR REFLECTION</span><Timer seconds={remaining(s.deadline, time)}/></div><h1 id="reflection-question">{PROMPT}</h1><form onSubmit={e => { e.preventDefault(); void act('/api/submit', { text }); }}><textarea aria-labelledby="reflection-question" value={text} maxLength={240} onChange={e => setText(e.target.value)} autoFocus disabled={busy}/><div className="input-meta"><span>{text.length} / 240</span></div><div className="action-row"><button className="button primary" disabled={!text.trim() || busy} type="submit">Submit<Arrow/></button></div></form></section>;
  }
  if (s.phase === 'review') {
    if (s.finished || !card) return <Waiting title="You’ve reached the end."><p>Waiting for everyone to finish.</p><span className="waiting-count">{s.finishedCount} / {s.joined} finished</span></Waiting>;
    if (expired === card.id) return <Waiting title="Next reflection…"><p>Moving on.</p></Waiting>;
    const vote = async (choice: Choice) => { const result = await act('/api/vote', { reflectionId: card.id, choice }); if (result?.card?.id === card.id && result.card.vote === choice) setReaction(choice); };
    return <section className="review-area"><div className="above-paper"><span className="eyebrow">ANONYMOUS REFLECTIONS <span className="review-count">{String(s.cursor + 1).padStart(2, '0')} / {String(s.reflectionCount).padStart(2, '0')}</span></span><Timer seconds={remaining(card.deadline, time)}/></div><motion.article className="reflection paper" key={card.id} initial={{ opacity: 0, y: reduced ? 0 : 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: reduced ? .01 : .15 }}><div className="section-top"><span className="eyebrow">{card.label}</span>{card.own && <span className="own-label">Your reflection</span>}</div><p className="reflection-text">{card.text}</p><div className="vote-zone">{card.own ? <div className="own-flower"><Flower/></div> : <><span className="choose-label">Choose one.</span><div className="vote-options"><button className="vote-button agree" disabled={!!card.vote || busy} aria-pressed={card.vote === 'flower'} onClick={() => void vote('flower')}><Flower/><span>Agree</span>{card.vote === 'flower' && <Check/>}</button><button className="vote-button disagree" disabled={!!card.vote || busy} aria-pressed={card.vote === 'bomb'} onClick={() => void vote('bomb')}><Bomb/><span>Disagree</span>{card.vote === 'bomb' && <Check/>}</button></div></>}{reaction && !reduced && <motion.div className={`reaction-burst ${reaction}`} aria-hidden="true" initial={{ opacity: 1, scale: .8, y: 0, rotate: -12 }} animate={{ opacity: 0, scale: 1.6, y: -70, rotate: 15 }} transition={{ duration: .75 }}>{reaction === 'flower' ? <Flower/> : <Bomb/>}</motion.div>}</div></motion.article><div className="review-actions"><span className="quiet-label">{card.label}</span><Button disabled={busy || (!card.vote && !card.own)} onClick={() => void act('/api/next', { reflectionId: card.id })}>Next</Button></div></section>;
  }
  return <SharedPresentation state={s} time={time}/>;
}

function SharedPresentation({ state: s, time }: { state: Snapshot; time: number }) {
  const reduced = useReducedMotion();
  if (s.phase === 'ending') return <Closing/>;
  if (s.phase === 'empty') return <Waiting title="No reflections this time."><p>Waiting for the closing thought.</p></Waiting>;
  if (s.phase === 'closed') return <Waiting title="Thank you for taking part."><p>The classroom is now closed.</p></Waiting>;
  const question = s.phase === 'question1' || s.phase === 'question2' ? QUESTIONS[s.phase] : null;
  if (s.phase === 'ranking' || question) return <div className={`results-stage ${question ? 'asking' : ''}`}><Ranking state={s} now={time}/>{question && <motion.div className="question-overlay" key={s.phase} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: reduced ? .01 : .25 }}><motion.h1 initial={{ y: reduced ? 0 : 18 }} animate={{ y: 0 }} transition={{ duration: .3 }}>{question}</motion.h1></motion.div>}</div>;
  if (s.phase === 'lobby') return <Waiting title="Design Lab."><p>{s.joined} participants have joined.</p></Waiting>;
  if (s.phase === 'writing') return <section className="display-writing paper"><div className="section-top"><span className="eyebrow">YOUR REFLECTION</span><Timer seconds={remaining(s.deadline, time)}/></div><h1>{PROMPT}</h1></section>;
  return <Waiting title="Different ideas. One classroom."><p>Everyone is exploring the reflections at their own pace.</p><span className="waiting-count">{s.finishedCount} / {s.joined} finished</span><Timer seconds={remaining(s.deadline, time)}/></Waiting>;
}

function Host({ lab, time }: { lab: Lab; time: number }) {
  const s = lab.state!;
  const [copied, setCopied] = useState(false);
  const [confirmClose, setConfirmClose] = useState(false);
  const share = s.joinUrls?.[0] || window.location.origin;
  const input = useRef<HTMLInputElement>(null);
  const copy = async () => { try { await navigator.clipboard.writeText(share); setCopied(true); } catch { input.current?.select(); document.execCommand('copy'); setCopied(true); } };
  const steps = ['Gathering', 'Writing', 'Sharing', 'Reflection'];
  const step = s.phase === 'lobby' ? 0 : s.phase === 'writing' ? 1 : s.phase === 'review' ? 2 : 3;
  return <div className="host-layout"><section className="host-main paper"><span className="eyebrow">CLASSROOM CONTROLS</span><h1>{s.phase === 'lobby' ? 'Ready when everyone is.' : s.phase === 'writing' ? 'Give the ideas a moment.' : s.phase === 'review' ? 'Let every perspective be seen.' : 'Leave space to think.'}</h1><ol className="host-steps">{steps.map((label, i) => <li key={label} data-current={i === step} data-done={i < step}><span>{i < step ? <Check/> : `0${i + 1}`}</span>{label}</li>)}</ol><div className="host-stats"><div><strong>{String(s.joined).padStart(2, '0')}</strong><span>participants joined</span></div><div><strong>{String(s.submitted).padStart(2, '0')}</strong><span>reflections submitted</span></div>{s.phase === 'review' ? <div><strong>{String(s.finishedCount).padStart(2, '0')}</strong><span>finished sharing</span></div> : <div><strong>{Math.round(s.writingMs / 1000)}<small>s</small></strong><span>writing time</span></div>}</div>{(s.phase === 'writing' || s.phase === 'review') && <div className="host-deadline"><Timer seconds={remaining(s.deadline, time)} label={s.phase === 'writing' ? 'Writing closes in' : 'Sharing closes in'}/></div>}<div className="host-primary">{s.phase === 'lobby' ? <Button disabled={!s.joined || lab.busy} onClick={() => void lab.act('/api/host/start')}>Start writing</Button> : s.phase === 'empty' ? <Button disabled={lab.busy} onClick={() => void lab.act('/api/host/ending')}>Show Goodhart’s Law</Button> : <span className="host-status"><span className="pulsing-dot"/>{s.phase === 'closed' ? 'Classroom closed' : s.phase === 'ending' ? 'The closing thought is on screen.' : s.phase === 'question1' || s.phase === 'question2' ? 'The closing questions advance automatically.' : s.phase === 'ranking' ? 'The ranking is on screen.' : 'The activity is running.'}</span>}</div></section><aside className="host-share paper"><span className="eyebrow">INVITE THE CLASS</span><h2>One link.<br/>Everyone’s ideas.</h2><label htmlFor="share-link">Share this link with the class.</label><div className="share-input"><input ref={input} id="share-link" readOnly value={share} onFocus={e => e.currentTarget.select()}/><button type="button" onClick={() => void copy()}>{copied ? 'Copied' : 'Copy'}</button></div>{s.joinUrls && s.joinUrls.length > 1 && <details><summary>Other local addresses</summary>{s.joinUrls.slice(1).map(url => <p className="alternate-url" key={url}>{url}</p>)}</details>}<a className="host-link" href="/" target="_blank" rel="noreferrer">Join as a participant<Arrow/></a><a className="host-link" href="/display" target="_blank" rel="noreferrer">Open classroom display<Arrow/></a><p className="host-note">Join the activity in a separate tab if you’re taking part too. Start writing when everyone has arrived.</p></aside>{step === 3 && s.phase !== 'closed' && <section className="host-preview"><SharedPresentation state={s} time={time}/></section>}<footer className="host-footer"><span>Design Lab · Gaming the System</span>{s.phase !== 'closed' && <button className="text-button" onClick={() => setConfirmClose(true)}>Close classroom</button>}</footer>{confirmClose && <div className="dialog-backdrop"><section role="dialog" aria-modal="true" aria-labelledby="close-title" className="close-dialog paper"><h2 id="close-title">Close the classroom?</h2><p>Everyone will be disconnected and this session will be cleared.</p><div className="action-row"><button className="text-button" onClick={() => setConfirmClose(false)}>Keep open</button><Button onClick={() => { setConfirmClose(false); void lab.act('/api/host/close'); }}>Close classroom</Button></div></section></div>}</div>;
}

export default function App() {
  const view: View = location.pathname === '/host' ? 'host' : location.pathname === '/display' ? 'display' : 'participant';
  const lab = useClassroom(view);
  const time = useTime(lab.now);
  const sound = useRankingSound(lab.state,time);
  return <div className={`lab-shell view-${view}`} onPointerDown={sound.unlock} onKeyDown={sound.unlock}><Brand view={view} phase={lab.state?.phase} sound={sound}/><main className="lab-main">{!lab.connected && lab.state?.phase !== 'closed' && <div className="connection-note" role="status">{lab.state ? 'Reconnecting to the classroom…' : 'Connecting to the classroom…'}</div>}{lab.error && <div className="error-note" role="alert">{lab.error}</div>}{!lab.state ? <Waiting title="Design Lab."><p>Connecting to the classroom…</p></Waiting> : view === 'host' ? <Host lab={lab} time={time}/> : view === 'display' ? <SharedPresentation state={lab.state} time={time}/> : <Participant lab={lab} time={time}/>}</main><div className="page-footer" aria-hidden="true"><span>GAMING THE SYSTEM</span><span>A little distance from the numbers.</span></div></div>;
}
